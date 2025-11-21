#!/usr/bin/env python3
"""
Print Label - Print large ASCII text labels rotated 90 degrees for visibility
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get USB configuration from environment
USB_VENDOR_ID = int(os.getenv('USB_VENDOR_ID', '0x0FE6'), 16)
USB_PRODUCT_ID = int(os.getenv('USB_PRODUCT_ID', '0x811E'), 16)

# ASCII art font dictionary for large letters (7 lines tall, wider spacing)
ASCII_FONT = {
    'A': [
        "    ###    ",
        "   ## ##   ",
        "  ##   ##  ",
        " ##     ## ",
        " ######### ",
        " ##     ## ",
        " ##     ## "
    ],
    'B': [
        " ########  ",
        " ##     ## ",
        " ##     ## ",
        " ########  ",
        " ##     ## ",
        " ##     ## ",
        " ########  "
    ],
    'C': [
        "   ######  ",
        "  ##    ## ",
        " ##        ",
        " ##        ",
        " ##        ",
        "  ##    ## ",
        "   ######  "
    ],
    'D': [
        " ########  ",
        " ##     ## ",
        " ##      ##",
        " ##      ##",
        " ##      ##",
        " ##     ## ",
        " ########  "
    ],
    'E': [
        " ######### ",
        " ##        ",
        " ##        ",
        " #######   ",
        " ##        ",
        " ##        ",
        " ######### "
    ],
    'F': [
        " ######### ",
        " ##        ",
        " ##        ",
        " #######   ",
        " ##        ",
        " ##        ",
        " ##        "
    ],
    'G': [
        "   ######  ",
        "  ##    ## ",
        " ##        ",
        " ##   #### ",
        " ##     ## ",
        "  ##    ## ",
        "   ######  "
    ],
    'H': [
        " ##     ## ",
        " ##     ## ",
        " ##     ## ",
        " ######### ",
        " ##     ## ",
        " ##     ## ",
        " ##     ## "
    ],
    'I': [
        " ######### ",
        "     ##    ",
        "     ##    ",
        "     ##    ",
        "     ##    ",
        "     ##    ",
        " ######### "
    ],
    'J': [
        " ######### ",
        "       ##  ",
        "       ##  ",
        "       ##  ",
        " ##    ##  ",
        " ##    ##  ",
        "  ######   "
    ],
    'K': [
        " ##     ## ",
        " ##    ##  ",
        " ##   ##   ",
        " ######    ",
        " ##   ##   ",
        " ##    ##  ",
        " ##     ## "
    ],
    'L': [
        " ##        ",
        " ##        ",
        " ##        ",
        " ##        ",
        " ##        ",
        " ##        ",
        " ######### "
    ],
    'M': [
        " ##     ## ",
        " ###   ### ",
        " #### #### ",
        " ## ### ## ",
        " ##  #  ## ",
        " ##     ## ",
        " ##     ## "
    ],
    'N': [
        " ##     ## ",
        " ###    ## ",
        " ####   ## ",
        " ## ##  ## ",
        " ##  ## ## ",
        " ##   #### ",
        " ##    ### "
    ],
    'O': [
        "   ######  ",
        "  ##    ## ",
        " ##      ##",
        " ##      ##",
        " ##      ##",
        "  ##    ## ",
        "   ######  "
    ],
    'P': [
        " ########  ",
        " ##     ## ",
        " ##     ## ",
        " ########  ",
        " ##        ",
        " ##        ",
        " ##        "
    ],
    'Q': [
        "   ######  ",
        "  ##    ## ",
        " ##      ##",
        " ##      ##",
        " ##   ## ##",
        "  ##    ## ",
        "   ###### ##"
    ],
    'R': [
        " ########  ",
        " ##     ## ",
        " ##     ## ",
        " ########  ",
        " ##   ##   ",
        " ##    ##  ",
        " ##     ## "
    ],
    'S': [
        "   ######  ",
        "  ##    ## ",
        " ##        ",
        "   ######  ",
        "        ## ",
        "  ##    ## ",
        "   ######  "
    ],
    'T': [
        " ######### ",
        "     ##    ",
        "     ##    ",
        "     ##    ",
        "     ##    ",
        "     ##    ",
        "     ##    "
    ],
    'U': [
        " ##     ## ",
        " ##     ## ",
        " ##     ## ",
        " ##     ## ",
        " ##     ## ",
        " ##     ## ",
        "   ######  "
    ],
    'V': [
        " ##     ## ",
        " ##     ## ",
        " ##     ## ",
        " ##     ## ",
        "  ##   ##  ",
        "   ## ##   ",
        "    ###    "
    ],
    'W': [
        " ##     ## ",
        " ##     ## ",
        " ##  #  ## ",
        " ## ### ## ",
        " #### #### ",
        " ###   ### ",
        " ##     ## "
    ],
    'X': [
        " ##     ## ",
        "  ##   ##  ",
        "   ## ##   ",
        "    ###    ",
        "   ## ##   ",
        "  ##   ##  ",
        " ##     ## "
    ],
    'Y': [
        " ##     ## ",
        "  ##   ##  ",
        "   ## ##   ",
        "    ###    ",
        "     ##    ",
        "     ##    ",
        "     ##    "
    ],
    'Z': [
        " ######### ",
        "       ##  ",
        "      ##   ",
        "     ##    ",
        "    ##     ",
        "   ##      ",
        " ######### "
    ],
    '0': [
        "   ######  ",
        "  ##   ### ",
        " ##   # ## ",
        " ##  #  ## ",
        " ## #   ## ",
        " ###    ## ",
        "  ######   "
    ],
    '1': [
        "    ###    ",
        "   ####    ",
        "  # ##     ",
        "    ##     ",
        "    ##     ",
        "    ##     ",
        " ######### "
    ],
    '2': [
        "   ######  ",
        "  ##    ## ",
        "        ## ",
        "      ##   ",
        "    ##     ",
        "   ##      ",
        " ######### "
    ],
    '3': [
        "   ######  ",
        "  ##    ## ",
        "        ## ",
        "    #####  ",
        "        ## ",
        "  ##    ## ",
        "   ######  "
    ],
    '4': [
        "      ###  ",
        "     ####  ",
        "    ## ##  ",
        "   ##  ##  ",
        " ######### ",
        "       ##  ",
        "       ##  "
    ],
    '5': [
        " ######### ",
        " ##        ",
        " ##        ",
        " ########  ",
        "        ## ",
        "  ##    ## ",
        "   ######  "
    ],
    '6': [
        "   ######  ",
        "  ##    ## ",
        " ##        ",
        " ########  ",
        " ##     ## ",
        " ##     ## ",
        "  ######   "
    ],
    '7': [
        " ######### ",
        "        ## ",
        "       ##  ",
        "      ##   ",
        "     ##    ",
        "    ##     ",
        "   ##      "
    ],
    '8': [
        "   ######  ",
        "  ##    ## ",
        "  ##    ## ",
        "   ######  ",
        "  ##    ## ",
        "  ##    ## ",
        "   ######  "
    ],
    '9': [
        "   ######  ",
        "  ##    ## ",
        "  ##    ## ",
        "   ####### ",
        "        ## ",
        "  ##    ## ",
        "   ######  "
    ],
    ' ': [
        "      ",
        "      ",
        "      ",
        "      ",
        "      ",
        "      ",
        "      "
    ],
    '-': [
        "           ",
        "           ",
        "           ",
        " ######### ",
        "           ",
        "           ",
        "           "
    ],
    '_': [
        "           ",
        "           ",
        "           ",
        "           ",
        "           ",
        "           ",
        " ######### "
    ],
    '.': [
        "      ",
        "      ",
        "      ",
        "      ",
        "      ",
        " ###  ",
        " ###  "
    ],
    '!': [
        "   ##   ",
        "   ##   ",
        "   ##   ",
        "   ##   ",
        "        ",
        "   ##   ",
        "   ##   "
    ],
    '?': [
        "   ######  ",
        "  ##    ## ",
        "        ## ",
        "      ##   ",
        "     ##    ",
        "           ",
        "     ##    "
    ],
    '/': [
        "        ## ",
        "       ##  ",
        "      ##   ",
        "     ##    ",
        "    ##     ",
        "   ##      ",
        "  ##       "
    ],
    ':': [
        "      ",
        "  ##  ",
        "  ##  ",
        "      ",
        "  ##  ",
        "  ##  ",
        "      "
    ],
}

def text_to_ascii_art(text):
    """Convert text to ASCII art using large letters"""
    text = text.upper()
    lines = ["", "", "", "", "", "", ""]
    
    for char in text:
        if char in ASCII_FONT:
            char_lines = ASCII_FONT[char]
            for i in range(7):
                lines[i] += char_lines[i] + "  "  # Add spacing between letters
        else:
            # Unknown character, use space
            for i in range(7):
                lines[i] += "        "
    
    return lines

def rotate_90_degrees(lines):
    """Rotate ASCII art 90 degrees clockwise for lengthwise printing"""
    if not lines:
        return []
    
    # Get max width
    max_width = max(len(line) for line in lines)
    
    # Pad all lines to same width
    padded_lines = [line.ljust(max_width) for line in lines]
    
    # Rotate: read columns from bottom to top, left to right
    rotated = []
    for col in range(max_width):
        rotated_line = ""
        for row in range(len(padded_lines) - 1, -1, -1):
            rotated_line += padded_lines[row][col]
        rotated.append(rotated_line)
    
    return rotated

def print_label(text):
    """Print a large text label rotated 90 degrees"""
    
    try:
        from escpos.printer import Usb
        
        print(f"Creating label: {text}")
        
        # Convert text to ASCII art
        ascii_lines = text_to_ascii_art(text)
        
        # Rotate 90 degrees for lengthwise printing
        rotated_lines = rotate_90_degrees(ascii_lines)
        
        print(f"✓ Label generated ({len(rotated_lines)} lines)\n")
        
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
        
        # Print label
        print("Printing label...")
        
        # Add some spacing at the top
        printer.text("\n\n")
        
        # Print each rotated line with double width
        printer.set(align='left', bold=True, double_width=True)
        for line in rotated_lines:
            printer.text(line + "\n")
        
        # Reset to normal width
        printer.set(double_width=False)
        
        # Add spacing at bottom
        printer.text("\n\n")
        
        # Cut paper
        printer.cut()
        
        print("✓ Label printed successfully!")
        return 0
        
    except Exception as e:
        print(f"✗ Error printing label: {e}")
        import traceback
        traceback.print_exc()
        return 1

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Print large text label rotated 90 degrees')
    parser.add_argument('text', nargs='+', help='Text to print on label')
    
    args = parser.parse_args()
    
    # Join all text arguments into a single string
    text = ' '.join(args.text)
    
    if len(text) > 20:
        print("Warning: Text is long, label may be very lengthy")
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled")
            return 0
    
    return print_label(text)


if __name__ == "__main__":
    sys.exit(main())
