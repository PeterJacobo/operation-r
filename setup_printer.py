#!/usr/bin/env python3
"""
Printer Setup Wizard - Interactive configuration for printer connection
"""

import os
import sys
import re
from pathlib import Path


def print_header():
    """Print the setup wizard header"""
    print("\n" + "=" * 60)
    print("  OPERATION R - Printer Setup Wizard")
    print("=" * 60)
    print("\nThis wizard will help you configure your printer connection.")
    print("You can choose between USB or network connection.\n")


def get_connection_type():
    """
    Prompt user to select connection type.
    
    Returns:
        'usb' or 'network'
    """
    print("Select your printer connection type:")
    print("  1. USB (Direct USB connection)")
    print("  2. Network (IP address connection)")
    print()
    
    while True:
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == '1':
            return 'usb'
        elif choice == '2':
            return 'network'
        else:
            print("Invalid choice. Please enter 1 or 2.")


def setup_usb_printer():
    """
    Configure USB printer settings.
    
    Returns:
        Dictionary with USB configuration
    """
    print("\n" + "-" * 60)
    print("USB Printer Configuration")
    print("-" * 60)
    print("\nTo find your printer's USB IDs:")
    print("  Windows: Use Device Manager or lsusb")
    print("  Linux/Mac: Run 'lsusb' in terminal")
    print("\nDefault values are for Rongta RP332 (VID: 0x0FE6, PID: 0x811E)")
    print()
    
    # Get vendor ID
    while True:
        vendor_id = input("USB Vendor ID [0x0FE6]: ").strip() or "0x0FE6"
        if re.match(r'^0x[0-9A-Fa-f]{4}$', vendor_id):
            break
        print("Invalid format. Use format: 0x0FE6")
    
    # Get product ID
    while True:
        product_id = input("USB Product ID [0x811E]: ").strip() or "0x811E"
        if re.match(r'^0x[0-9A-Fa-f]{4}$', product_id):
            break
        print("Invalid format. Use format: 0x811E")
    
    return {
        'PRINTER_CONNECTION_TYPE': 'usb',
        'USB_VENDOR_ID': vendor_id,
        'USB_PRODUCT_ID': product_id
    }


def setup_network_printer():
    """
    Configure network printer settings.
    
    Returns:
        Dictionary with network configuration
    """
    print("\n" + "-" * 60)
    print("Network Printer Configuration")
    print("-" * 60)
    print("\nYou'll need:")
    print("  - Printer's IP address (e.g., 192.168.1.100)")
    print("  - Port number (usually 9100 for thermal printers)")
    print("\nTo find your printer's IP:")
    print("  - Check printer's network settings menu")
    print("  - Print a network configuration page from printer")
    print("  - Check your router's connected devices")
    print()
    
    # Get IP address
    while True:
        ip_address = input("Printer IP address: ").strip()
        # Basic IP validation
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip_address):
            # Check each octet is 0-255
            octets = [int(x) for x in ip_address.split('.')]
            if all(0 <= x <= 255 for x in octets):
                break
        print("Invalid IP address. Use format: 192.168.1.100")
    
    # Get port
    while True:
        port = input("Printer port [9100]: ").strip() or "9100"
        if port.isdigit() and 1 <= int(port) <= 65535:
            break
        print("Invalid port. Must be between 1 and 65535.")
    
    return {
        'PRINTER_CONNECTION_TYPE': 'network',
        'PRINTER_IP': ip_address,
        'PRINTER_PORT': port
    }


def test_connection(config):
    """
    Test the printer connection with the provided configuration.
    
    Args:
        config: Dictionary with printer configuration
        
    Returns:
        bool: True if connection successful
    """
    print("\n" + "-" * 60)
    print("Testing printer connection...")
    print("-" * 60)
    
    # Temporarily set environment variables for testing
    for key, value in config.items():
        os.environ[key] = value
    
    try:
        from printer_config import test_printer_connection
        
        success, message = test_printer_connection()
        print(message)
        
        if success:
            print("\n✓ Connection test successful!")
            return True
        else:
            print("\n✗ Connection test failed.")
            return False
            
    except Exception as e:
        print(f"\n✗ Error during connection test: {e}")
        return False


def save_configuration(config):
    """
    Save configuration to .env file.
    
    Args:
        config: Dictionary with printer configuration
    """
    env_path = Path('.env')
    
    # Read existing .env file if it exists
    existing_config = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    existing_config[key.strip()] = value.strip()
    
    # Update with new printer configuration
    existing_config.update(config)
    
    # Write back to .env file
    with open(env_path, 'w') as f:
        f.write("# Operation R Configuration\n")
        f.write("# Generated by setup wizard\n\n")
        
        # Printer settings
        f.write("# Printer Configuration\n")
        f.write(f"PRINTER_CONNECTION_TYPE={existing_config.get('PRINTER_CONNECTION_TYPE', 'usb')}\n")
        
        if existing_config.get('PRINTER_CONNECTION_TYPE') == 'usb':
            f.write(f"USB_VENDOR_ID={existing_config.get('USB_VENDOR_ID', '0x0FE6')}\n")
            f.write(f"USB_PRODUCT_ID={existing_config.get('USB_PRODUCT_ID', '0x811E')}\n")
            if 'PRINTER_IP' in existing_config:
                f.write(f"# PRINTER_IP={existing_config['PRINTER_IP']}\n")
            if 'PRINTER_PORT' in existing_config:
                f.write(f"# PRINTER_PORT={existing_config['PRINTER_PORT']}\n")
        else:
            f.write(f"PRINTER_IP={existing_config.get('PRINTER_IP', '192.168.1.100')}\n")
            f.write(f"PRINTER_PORT={existing_config.get('PRINTER_PORT', '9100')}\n")
            if 'USB_VENDOR_ID' in existing_config:
                f.write(f"# USB_VENDOR_ID={existing_config['USB_VENDOR_ID']}\n")
            if 'USB_PRODUCT_ID' in existing_config:
                f.write(f"# USB_PRODUCT_ID={existing_config['USB_PRODUCT_ID']}\n")
        
        f.write("\n")
        
        # Other settings (preserve if they exist)
        other_keys = [
            'EMAIL_USER', 'EMAIL_PASS', 'JIRA_API_TOKEN', 
            'NGROK_AUTHTOKEN', 'ATLASSIAN_CLOUD_ID'
        ]
        
        has_other_settings = any(key in existing_config for key in other_keys)
        if has_other_settings:
            f.write("# Email Configuration\n")
            if 'EMAIL_USER' in existing_config:
                f.write(f"EMAIL_USER={existing_config['EMAIL_USER']}\n")
            if 'EMAIL_PASS' in existing_config:
                f.write(f"EMAIL_PASS={existing_config['EMAIL_PASS']}\n")
            
            f.write("\n# Jira/Atlassian Configuration\n")
            if 'JIRA_API_TOKEN' in existing_config:
                f.write(f"JIRA_API_TOKEN={existing_config['JIRA_API_TOKEN']}\n")
            if 'ATLASSIAN_CLOUD_ID' in existing_config:
                f.write(f"ATLASSIAN_CLOUD_ID={existing_config['ATLASSIAN_CLOUD_ID']}\n")
            
            if 'NGROK_AUTHTOKEN' in existing_config:
                f.write(f"\n# Ngrok Configuration\n")
                f.write(f"NGROK_AUTHTOKEN={existing_config['NGROK_AUTHTOKEN']}\n")
    
    print("\n✓ Configuration saved to .env file")


def main():
    """Main setup wizard flow"""
    print_header()
    
    # Get connection type
    connection_type = get_connection_type()
    
    # Configure based on connection type
    if connection_type == 'usb':
        config = setup_usb_printer()
    else:
        config = setup_network_printer()
    
    # Ask if user wants to test connection
    print("\n" + "-" * 60)
    test = input("\nTest printer connection now? (y/n) [y]: ").strip().lower()
    
    if test in ('', 'y', 'yes'):
        connection_ok = test_connection(config)
        
        if not connection_ok:
            retry = input("\nRetry setup? (y/n) [y]: ").strip().lower()
            if retry in ('', 'y', 'yes'):
                print("\n")
                return main()  # Restart wizard
            else:
                save_anyway = input("\nSave configuration anyway? (y/n) [n]: ").strip().lower()
                if save_anyway not in ('y', 'yes'):
                    print("\nSetup cancelled.")
                    return 1
    
    # Save configuration
    save_configuration(config)
    
    # Print summary
    print("\n" + "=" * 60)
    print("  Setup Complete!")
    print("=" * 60)
    print("\nPrinter Configuration:")
    print(f"  Connection Type: {config['PRINTER_CONNECTION_TYPE'].upper()}")
    
    if config['PRINTER_CONNECTION_TYPE'] == 'usb':
        print(f"  USB Vendor ID: {config['USB_VENDOR_ID']}")
        print(f"  USB Product ID: {config['USB_PRODUCT_ID']}")
    else:
        print(f"  IP Address: {config['PRINTER_IP']}")
        print(f"  Port: {config['PRINTER_PORT']}")
    
    print("\nNext steps:")
    print("  - Test printing: python main.py test-print")
    print("  - Print a label: python print_label.py 'Your Text'")
    print("  - Print a ticket: python print_ticket.py tickets/ISSUE-123.xml")
    print("\nTo reconfigure, run: python main.py setup")
    print()
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
