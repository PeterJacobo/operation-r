#!/usr/bin/env python3
"""
Print Barcode - Generate and print scannable barcodes from text input
"""

import sys
import argparse
from dotenv import load_dotenv
from printer_config import get_printer, PrinterConnectionError

# Load environment variables
load_dotenv()

# List of supported barcode types
SUPPORTED_BARCODES = [
    'CODE128',     # Most versatile, supports alphanumeric
    'CODE39',      # Alphanumeric, widely supported
    'EAN13',       # 13-digit retail barcodes (12 digits + checksum)
    'EAN8',        # 8-digit retail barcodes (7 digits + checksum)
    'UPC-A',       # 12-digit North American retail
    'ITF',         # Interleaved 2 of 5, numeric only
    'CODABAR',     # Numeric with special chars (-, $, :, /, ., +)
    'CODE93',      # Similar to CODE39 but more compact
]

# Character validation rules for each barcode type
BARCODE_RULES = {
    'CODE39': {
        'allowed_chars': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-. $/+%',
        'description': 'Uppercase letters, digits, and - . $ / + % space',
        'example': 'ABC-123',
        'note': 'Does not support lowercase or underscores'
    },
    'CODE93': {
        'allowed_chars': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-. $/+%',
        'description': 'Uppercase letters, digits, and - . $ / + % space',
        'example': 'ABC-123',
        'note': 'Similar to CODE39, no lowercase or underscores'
    },
    'ITF': {
        'allowed_chars': '0123456789',
        'description': 'Numeric only, even number of digits required',
        'example': '123456',
        'note': 'Must have even length'
    },
    'EAN13': {
        'allowed_chars': '0123456789',
        'description': '12 or 13 digits (checksum auto-calculated)',
        'example': '1234567890128',
        'note': 'Exactly 12 or 13 digits'
    },
    'EAN8': {
        'allowed_chars': '0123456789',
        'description': '7 or 8 digits (checksum auto-calculated)',
        'example': '12345670',
        'note': 'Exactly 7 or 8 digits'
    },
    'UPCA': {
        'allowed_chars': '0123456789',
        'description': '11 or 12 digits',
        'example': '012345678905',
        'note': 'Exactly 11 or 12 digits'
    },
    'CODABAR': {
        'allowed_chars': '0123456789-$:/.+',
        'description': 'Numeric and - $ : / . +',
        'example': 'A123B',
        'note': 'Often uses start/stop chars (A, B, C, D)'
    }
}


def validate_barcode_content(text, barcode_type):
    """
    Validate that the text is compatible with the barcode type.
    
    Args:
        text: Text to validate
        barcode_type: Type of barcode
    
    Returns:
        tuple: (is_valid, error_message, suggestion)
    """
    bc_upper = barcode_type.upper().replace('-', '')
    
    # CODE128 accepts almost anything
    if bc_upper == 'CODE128':
        return True, None, None
    
    # Get validation rules for this barcode type
    rules = BARCODE_RULES.get(bc_upper)
    if not rules:
        return True, None, None  # No specific rules, let printer handle it
    
    # Check character validity
    invalid_chars = set()
    for char in text:
        if char not in rules['allowed_chars']:
            invalid_chars.add(char)
    
    if invalid_chars:
        invalid_list = ', '.join(f"'{c}'" for c in sorted(invalid_chars))
        error_msg = f"Invalid characters for {barcode_type}: {invalid_list}"
        suggestion = f"Try CODE128 instead, which supports all characters"
        
        # Special suggestions for common issues
        if '_' in invalid_chars:
            suggestion = f"Replace underscores with hyphens (use '-' instead of '_'), or use CODE128"
        elif any(c.islower() for c in invalid_chars):
            suggestion = f"Convert to uppercase ('{text.upper()}'), or use CODE128"
        
        return False, error_msg, suggestion
    
    # Additional length checks
    if bc_upper == 'ITF' and len(text) % 2 != 0:
        return False, "ITF requires even number of digits", f"Add a leading zero: '0{text}' or use CODE128"
    
    if bc_upper == 'EAN13' and len(text) not in [12, 13]:
        return False, f"EAN13 requires 12 or 13 digits (got {len(text)})", "Use CODE128 for variable-length codes"
    
    if bc_upper == 'EAN8' and len(text) not in [7, 8]:
        return False, f"EAN8 requires 7 or 8 digits (got {len(text)})", "Use CODE128 or EAN13 instead"
    
    if bc_upper == 'UPCA' and len(text) not in [11, 12]:
        return False, f"UPC-A requires 11 or 12 digits (got {len(text)})", "Use CODE128 for variable-length codes"
    
    return True, None, None


def print_barcode(text, barcode_type='CODE128', height=100, width=3, 
                  position='BELOW', font='A'):
    """
    Print a barcode with the given text and format.
    
    Args:
        text: Text/data to encode in the barcode
        barcode_type: Type of barcode (CODE128, CODE39, EAN13, etc.)
        height: Barcode height in dots (1-255)
        width: Barcode module width in dots (2-6)
        position: Text position relative to barcode (ABOVE, BELOW, BOTH, OFF)
        font: Font for text (A or B)
    
    Returns:
        0 on success, 1 on failure
    """
    # Validate barcode type
    bc_upper = barcode_type.upper().replace('-', '').replace('_', '')
    if bc_upper not in [b.replace('-', '').replace('_', '') for b in SUPPORTED_BARCODES]:
        print(f"✗ Unsupported barcode type: {barcode_type}")
        print(f"\nSupported types: {', '.join(SUPPORTED_BARCODES)}")
        return 1
    
    # Validate content before connecting to printer
    is_valid, error_msg, suggestion = validate_barcode_content(text, barcode_type)
    if not is_valid:
        print(f"✗ {error_msg}")
        print(f"\n💡 Suggestion: {suggestion}")
        
        # Show what characters are allowed
        rules = BARCODE_RULES.get(bc_upper)
        if rules:
            print(f"\n{barcode_type} supports: {rules['description']}")
            print(f"Example: {rules['example']}")
            if rules.get('note'):
                print(f"Note: {rules['note']}")
        
        return 1
    
    try:
        # Connect to printer
        print("Connecting to printer...")
        try:
            printer = get_printer()
            print("✓ Printer connected\n")
        except PrinterConnectionError as e:
            print(f"✗ {e}")
            return 1
        
        # Print header
        printer.set(align='center', bold=True, double_width=True)
        printer.text("BARCODE\n")
        printer.set(align='center', bold=False, double_width=False)
        printer.text(f"Type: {barcode_type.upper()}\n")
        printer.text("\n")
        
        # Print the barcode
        print(f"Generating {barcode_type} barcode...")
        print(f"Content: {text}")
        
        try:
            # Try hardware barcode first
            printer.barcode(
                code=text,
                bc=barcode_type.upper(),
                height=height,
                width=width,
                pos=position.upper(),
                font=font.upper(),
                align_ct=True,
                check=True
            )
            print("✓ Using hardware barcode renderer")
        except Exception as barcode_error:
            # Hardware failed, try software rendering with image
            print(f"\n⚠ Hardware barcode not supported, using software renderer...")
            try:
                # Import barcode generation library
                import barcode
                from barcode.writer import ImageWriter
                from PIL import Image
                import io
                
                # Map barcode type names
                bc_type_map = {
                    'CODE128': 'code128',
                    'CODE39': 'code39',
                    'EAN13': 'ean13',
                    'EAN8': 'ean8',
                    'UPCA': 'upca',
                    'ITF': 'itf',
                    'CODE93': 'code93',
                }
                
                bc_lower = bc_type_map.get(barcode_type.upper().replace('-', ''))
                if not bc_lower:
                    raise Exception(f"Software renderer doesn't support {barcode_type}")
                
                # Generate barcode image
                barcode_class = barcode.get_barcode_class(bc_lower)
                
                # Create barcode with custom options
                writer_options = {
                    'module_height': height / 10,  # Convert dots to mm (approximate)
                    'module_width': width * 0.3,
                    'quiet_zone': 6.5,
                    'font_size': 10 if font.upper() == 'A' else 8,
                    'text_distance': 3,
                }
                
                # Show/hide text based on position
                if position.upper() == 'OFF':
                    writer_options['write_text'] = False
                
                barcode_instance = barcode_class(text, writer=ImageWriter())
                
                # Render to image in memory
                buffer = io.BytesIO()
                barcode_instance.write(buffer, options=writer_options)
                buffer.seek(0)
                
                # Open and print the image
                img = Image.open(buffer)
                
                # Add spacing before barcode
                printer.text("\n")
                
                # Print the barcode image
                printer.image(img, high_density_vertical=True, high_density_horizontal=True, center=True)
                
                print("✓ Using software barcode renderer")
                
            except ImportError as import_err:
                print(f"\n✗ Software barcode requires additional packages:")
                print("   pip install python-barcode Pillow")
                print("\nAlternatively, your printer may not support this barcode type.")
                print(f"Suggestion: Try CODE128 which has broader hardware support.")
                printer.cut()
                return 1
            except Exception as sw_error:
                print(f"✗ Barcode generation failed: {sw_error}")
                print("\nTroubleshooting:")
                print(f"1. Verify text format is valid for {barcode_type}")
                print(f"2. Check barcode type requirements:")
                if 'EAN' in barcode_type.upper():
                    print("   - EAN13 requires 12 or 13 digits")
                    print("   - EAN8 requires 7 or 8 digits")
                elif 'UPC' in barcode_type.upper():
                    print("   - UPC-A requires 11 or 12 digits")
                elif 'ITF' in barcode_type.upper():
                    print("   - ITF requires even number of digits")
                else:
                    print(f"   - {barcode_type} may have specific format requirements")
                print(f"\n3. Try a different barcode type (CODE128 is most versatile)")
                printer.cut()
                return 1
                return 1
        
        # Add some spacing and footer
        printer.text("\n")
        printer.set(align='center')
        printer.text("Scan to decode\n")
        printer.text("\n\n")
        
        # Cut the paper
        printer.cut()
        
        print("\n✓ Barcode printed successfully!")
        print("\nTest by scanning with a barcode scanner or mobile app.")
        
        return 0
        
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def list_barcode_types():
    """Print a list of supported barcode types with descriptions."""
    print("\n📊 Supported Barcode Types")
    print("=" * 70)
    
    descriptions = {
        'CODE128': ('Alphanumeric + special chars (most versatile)', 'ABC123_-./'),
        'CODE39': ('Uppercase, digits, - . $ / + % space only', 'ABC-123'),
        'EAN13': ('13-digit retail product codes', '1234567890128'),
        'EAN8': ('8-digit compact retail codes', '12345670'),
        'UPC-A': ('12-digit North American retail', '012345678905'),
        'ITF': ('Numeric only, even length required', '123456'),
        'CODABAR': ('Numeric + special chars (- $ : / . +)', 'A123B'),
        'CODE93': ('Uppercase, digits, similar to CODE39', 'ABC-123'),
    }
    
    for barcode in SUPPORTED_BARCODES:
        desc, example = descriptions.get(barcode, ('No description', 'N/A'))
        print(f"  {barcode:<12} - {desc}")
        print(f"               Example: {example}")
    
    print("\n" + "=" * 70)
    print("\n💡 Tips:")
    print("  • CODE128 is recommended for general use (supports most chars)")
    print("  • CODE39/CODE93 do NOT support lowercase or underscores")
    print("  • Replace underscores with hyphens: 'PEJ_Bacon' → 'PEJ-BACON'")
    print("  • EAN13/UPC-A for product codes (specific length required)")
    print("  • Use --list-examples to see detailed format examples\n")


def list_examples():
    """Print example barcode formats and usage."""
    print("\n📋 Barcode Format Examples")
    print("=" * 60)
    
    examples = [
        ("CODE128", "Hello123", "Alphanumeric text"),
        ("CODE128", "TICKET-2024-001", "Ticket numbers"),
        ("CODE39", "ABC-123", "Simple alphanumeric"),
        ("EAN13", "1234567890128", "13-digit product code"),
        ("EAN8", "12345670", "8-digit compact code"),
        ("UPC-A", "012345678905", "12-digit UPC"),
        ("ITF", "123456", "Even-length numeric"),
        ("CODABAR", "A123B", "Numeric with start/stop chars"),
    ]
    
    for barcode_type, example, description in examples:
        print(f"\n{barcode_type}:")
        print(f"  Example: {example}")
        print(f"  Use: {description}")
    
    print("\n" + "=" * 60)
    print("\n🚀 Quick Start:")
    print('  python print_barcode.py "Hello123"')
    print('  python print_barcode.py "1234567890128" --type EAN13')
    print('  python print_barcode.py "TICKET-001" --type CODE39 --height 120\n')


def main():
    """Main entry point for the barcode printer."""
    parser = argparse.ArgumentParser(
        description='Generate and print scannable barcodes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s "Hello World"                    # CODE128 barcode (default)
  %(prog)s "ABC123" --type CODE39           # CODE39 barcode
  %(prog)s "1234567890128" --type EAN13     # EAN13 product code
  %(prog)s "TICKET-2024-001" --height 150   # Taller barcode
  %(prog)s --list                           # Show supported types
  %(prog)s --list-examples                  # Show format examples
        '''
    )
    
    parser.add_argument(
        'text',
        nargs='?',
        help='Text or data to encode in the barcode'
    )
    
    parser.add_argument(
        '-t', '--type',
        default='CODE128',
        help='Barcode type (default: CODE128). Use --list to see all types'
    )
    
    parser.add_argument(
        '--height',
        type=int,
        default=100,
        help='Barcode height in dots, 1-255 (default: 100)'
    )
    
    parser.add_argument(
        '--width',
        type=int,
        default=3,
        help='Barcode module width in dots, 2-6 (default: 3)'
    )
    
    parser.add_argument(
        '--position',
        choices=['ABOVE', 'BELOW', 'BOTH', 'OFF'],
        default='BELOW',
        help='Position of human-readable text (default: BELOW)'
    )
    
    parser.add_argument(
        '--font',
        choices=['A', 'B'],
        default='A',
        help='Font for human-readable text (default: A)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all supported barcode types'
    )
    
    parser.add_argument(
        '--list-examples',
        action='store_true',
        help='Show barcode format examples'
    )
    
    args = parser.parse_args()
    
    # Handle list commands
    if args.list:
        list_barcode_types()
        return 0
    
    if args.list_examples:
        list_examples()
        return 0
    
    # Validate that text was provided
    if not args.text:
        parser.error('text is required (unless using --list or --list-examples)')
    
    # Validate parameters
    if not (1 <= args.height <= 255):
        print("✗ Error: Height must be between 1 and 255")
        return 1
    
    if not (2 <= args.width <= 6):
        print("✗ Error: Width must be between 2 and 6")
        return 1
    
    # Print the barcode
    return print_barcode(
        text=args.text,
        barcode_type=args.type,
        height=args.height,
        width=args.width,
        position=args.position,
        font=args.font
    )


if __name__ == "__main__":
    sys.exit(main())
