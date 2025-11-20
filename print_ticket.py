#!/usr/bin/env python3
"""
Print Jira Ticket - Print a Jira issue to thermal printer from XML export
"""

import os
import sys
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
from html import unescape
import re

# Load environment variables
load_dotenv()

# Get USB configuration from environment
USB_VENDOR_ID = int(os.getenv('USB_VENDOR_ID', '0x0FE6'), 16)
USB_PRODUCT_ID = int(os.getenv('USB_PRODUCT_ID', '0x811E'), 16)

def strip_html(text):
    """Remove HTML tags and decode entities from text"""
    if not text:
        return ""
    
    # Decode HTML entities
    text = unescape(text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def wrap_text(text, width=24):
    """Wrap text to specified width for thermal printer"""
    if not text:
        return []
    
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        word_length = len(word)
        
        # If adding this word would exceed width, start new line
        if current_length + word_length + len(current_line) > width:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = []
                current_length = 0
        
        current_line.append(word)
        current_length += word_length
    
    # Add remaining words
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def truncate_text(text, max_chars=400):
    """Truncate text to maximum character count"""
    if not text or len(text) <= max_chars:
        return text
    
    return text[:max_chars] + "..."

def parse_jira_xml(xml_file):
    """Parse Jira XML export and extract ticket data"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Find the item element
    item = root.find('.//item')
    if item is None:
        raise ValueError("No item found in XML")
    
    # Extract fields
    data = {
        'key': item.findtext('key', ''),
        'summary': item.findtext('summary', ''),
        'description': strip_html(item.findtext('description', '')),
        'type': item.findtext('type', ''),
        'status': item.findtext('status', ''),
        'priority': item.findtext('priority', ''),
        'assignee': item.findtext('assignee', 'Unassigned'),
        'reporter': item.findtext('reporter', ''),
        'created': item.findtext('created', ''),
        'labels': []
    }
    
    # Extract labels
    labels = item.find('labels')
    if labels is not None:
        data['labels'] = [label.text for label in labels.findall('label') if label.text]
    
    return data

def print_jira_ticket(xml_file):
    """Print a Jira ticket from XML export to thermal printer"""
    
    try:
        from escpos.printer import Usb
        
        # Parse XML
        print(f"Parsing XML file: {xml_file}")
        ticket = parse_jira_xml(xml_file)
        print(f"✓ Parsed ticket: {ticket['key']}\n")
        
        # Connect to printer
        print("Connecting to printer...")
        try:
            printer = Usb(USB_VENDOR_ID, USB_PRODUCT_ID)
            print("✓ Printer connected\n")
        except Exception as e:
            print(f"✗ Failed to connect to printer: {e}")
            print("\nTroubleshooting:")
            print("1. Ensure printer is powered on and connected via USB")
            print("2. On Windows, install libusb from: https://github.com/libusb/libusb/releases")
            print("3. Extract libusb-1.0.dll to C:\\Windows\\System32")
            return 1
        
        # Print ticket
        print("Printing ticket...")
        
        # Header
        printer.set(align='center', bold=True, width=2, height=2)
        printer.text(f"{ticket['key']}\n")
        
        printer.set(align='center', bold=False, width=1, height=1)
        printer.text("=" * 24 + "\n\n")
        
        # Summary
        printer.set(align='left', bold=True)
        for line in wrap_text(ticket['summary']):
            printer.text(line + "\n")
        printer.text("\n")
        
        # Metadata
        printer.set(bold=False)
        printer.text(f"Type: {ticket['type']}\n")
        printer.text(f"Status: {ticket['status']}\n")
        printer.text(f"Priority: {ticket['priority']}\n")
        printer.text(f"Assignee: {ticket['assignee']}\n")
        
        # Labels
        if ticket['labels']:
            labels_str = ", ".join(ticket['labels'])
            printer.text(f"Labels: ")
            for line in wrap_text(labels_str):
                printer.text(line + "\n")
        
        printer.text("\n")
        
        # Footer
        printer.text("=" * 24 + "\n")
        printer.set(align='center')
        printer.text("Operation R\n")
        printer.text("=" * 24 + "\n\n")
        
        # Cut paper
        printer.cut()
        
        print("✓ Ticket printed successfully!")
        return 0
        
    except FileNotFoundError:
        print(f"✗ Error: XML file not found: {xml_file}")
        return 1
    except ET.ParseError as e:
        print(f"✗ Error parsing XML: {e}")
        return 1
    except Exception as e:
        print(f"✗ Error printing ticket: {e}")
        import traceback
        traceback.print_exc()
        return 1

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Print Jira ticket from XML export')
    parser.add_argument('xml_file', help='Path to Jira XML export file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.xml_file):
        print(f"Error: File not found: {args.xml_file}")
        return 1
    
    return print_jira_ticket(args.xml_file)


if __name__ == "__main__":
    sys.exit(main())
