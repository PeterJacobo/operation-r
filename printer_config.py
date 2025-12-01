#!/usr/bin/env python3
"""
Printer Configuration Module - Handles both USB and Network printer connections
"""

import os
from dotenv import load_dotenv
from escpos.printer import Usb, Network
from typing import Optional

# Load environment variables
load_dotenv()


class PrinterConnectionError(Exception):
    """Exception raised when printer connection fails"""
    pass


def get_printer():
    """
    Get a printer instance based on configuration in .env file.
    
    Supports two connection types:
    - USB: Direct USB connection using vendor/product IDs
    - Network: Network connection using IP address and port
    
    Returns:
        An escpos printer object (Usb or Network)
        
    Raises:
        PrinterConnectionError: If connection fails or configuration is invalid
    """
    connection_type = os.getenv('PRINTER_CONNECTION_TYPE', 'usb').lower()
    
    try:
        if connection_type == 'usb':
            return _get_usb_printer()
        elif connection_type == 'network':
            return _get_network_printer()
        else:
            raise PrinterConnectionError(
                f"Invalid PRINTER_CONNECTION_TYPE: {connection_type}. "
                "Must be 'usb' or 'network'"
            )
    except Exception as e:
        raise PrinterConnectionError(f"Failed to connect to printer: {e}")


def _get_usb_printer() -> Usb:
    """
    Create a USB printer connection.
    
    Returns:
        Usb printer object
        
    Raises:
        PrinterConnectionError: If USB connection fails
    """
    try:
        vendor_id = int(os.getenv('USB_VENDOR_ID', '0x0FE6'), 16)
        product_id = int(os.getenv('USB_PRODUCT_ID', '0x811E'), 16)
        
        printer = Usb(vendor_id, product_id)
        return printer
        
    except ValueError as e:
        raise PrinterConnectionError(
            f"Invalid USB_VENDOR_ID or USB_PRODUCT_ID format: {e}"
        )
    except Exception as e:
        raise PrinterConnectionError(
            f"Failed to connect to USB printer: {e}\n\n"
            "Troubleshooting:\n"
            "1. Ensure printer is powered on and connected via USB\n"
            "2. On Windows, install libusb from: https://github.com/libusb/libusb/releases\n"
            "3. Extract libusb-1.0.dll to C:\\Windows\\System32\n"
            "4. Verify USB_VENDOR_ID and USB_PRODUCT_ID in .env file"
        )


def _get_network_printer() -> Network:
    """
    Create a network printer connection.
    
    Returns:
        Network printer object
        
    Raises:
        PrinterConnectionError: If network connection fails
    """
    try:
        printer_ip = os.getenv('PRINTER_IP')
        if not printer_ip:
            raise PrinterConnectionError(
                "PRINTER_IP not set in .env file. "
                "Run 'python main.py setup' to configure your printer."
            )
        
        # Default port for most thermal printers is 9100
        printer_port = int(os.getenv('PRINTER_PORT', '9100'))
        
        printer = Network(printer_ip, printer_port)
        return printer
        
    except ValueError as e:
        raise PrinterConnectionError(
            f"Invalid PRINTER_PORT format: {e}"
        )
    except Exception as e:
        raise PrinterConnectionError(
            f"Failed to connect to network printer at {printer_ip}:{printer_port}: {e}\n\n"
            "Troubleshooting:\n"
            "1. Verify printer is powered on and connected to network\n"
            "2. Check that PRINTER_IP is correct in .env file\n"
            "3. Ensure printer port (default 9100) is correct\n"
            "4. Ping the printer IP to verify network connectivity\n"
            "5. Check firewall settings allow connection to printer port"
        )


def test_printer_connection() -> tuple[bool, str]:
    """
    Test the printer connection without printing anything.
    
    Returns:
        A tuple of (success: bool, message: str)
    """
    connection_type = os.getenv('PRINTER_CONNECTION_TYPE', 'usb').lower()
    
    try:
        printer = get_printer()
        
        # Connection successful
        if connection_type == 'usb':
            vendor_id = os.getenv('USB_VENDOR_ID', '0x0FE6')
            product_id = os.getenv('USB_PRODUCT_ID', '0x811E')
            message = f"✓ Successfully connected to USB printer (VID: {vendor_id}, PID: {product_id})"
        else:
            printer_ip = os.getenv('PRINTER_IP')
            printer_port = os.getenv('PRINTER_PORT', '9100')
            message = f"✓ Successfully connected to network printer at {printer_ip}:{printer_port}"
        
        return True, message
        
    except PrinterConnectionError as e:
        return False, f"✗ Connection failed: {e}"
    except Exception as e:
        return False, f"✗ Unexpected error: {e}"


def get_connection_info() -> dict:
    """
    Get current printer connection configuration.
    
    Returns:
        Dictionary with connection details
    """
    connection_type = os.getenv('PRINTER_CONNECTION_TYPE', 'usb').lower()
    
    info = {
        'connection_type': connection_type
    }
    
    if connection_type == 'usb':
        info['vendor_id'] = os.getenv('USB_VENDOR_ID', '0x0FE6')
        info['product_id'] = os.getenv('USB_PRODUCT_ID', '0x811E')
    elif connection_type == 'network':
        info['printer_ip'] = os.getenv('PRINTER_IP', 'Not configured')
        info['printer_port'] = os.getenv('PRINTER_PORT', '9100')
    
    return info
