#!/usr/bin/env python3
"""
Operation R - CLI Tool for Email-to-Printer System
Manages email fetching, label management, and Flask web server
"""

import argparse
import sys
import subprocess
import os


def fetch_emails():
    """Launch the email fetching service"""
    print("Starting email fetching service...")
    print("This will run continuously and check for emails every 10 minutes.")
    print("Press Ctrl+C to stop.\n")
    try:
        subprocess.run([sys.executable, "fetch_emails.py"])
    except KeyboardInterrupt:
        print("\nEmail fetching service stopped.")
    except Exception as e:
        print(f"Error running fetch_emails: {e}")
        return 1
    return 0


def reset_labels():
    """Reset printed labels on emails"""
    print("Resetting printed labels...\n")
    try:
        subprocess.run([sys.executable, "reset_printed_labels.py"])
    except Exception as e:
        print(f"Error running reset_printed_labels: {e}")
        return 1
    return 0


def test_print():
    """Print a test page to verify printer setup"""
    print("Testing printer connection and functionality...\n")
    
    try:
        from printer_config import get_printer, PrinterConnectionError, get_connection_info
        from dotenv import load_dotenv
        import traceback
        from datetime import datetime
        
        load_dotenv()
        
        # Display connection info
        conn_info = get_connection_info()
        print(f"Attempting to connect to printer...")
        print(f"Connection Type: {conn_info['connection_type'].upper()}")
        
        if conn_info['connection_type'] == 'usb':
            print(f"USB Vendor ID: {conn_info['vendor_id']}")
            print(f"USB Product ID: {conn_info['product_id']}\n")
        else:
            print(f"Network IP: {conn_info['printer_ip']}")
            print(f"Network Port: {conn_info['printer_port']}\n")
        
        try:
            printer = get_printer()
            print("✓ Printer connected successfully!\n")
        except PrinterConnectionError as e:
            print(f"✗ {e}")
            return 1
        
        # Print test page with ASCII art
        print("Printing test page...\n")
        
        try:
            # Header
            printer.set(align='center', bold=True, double_width=True)
            printer.text("OPERATION R\n")
            printer.set(align='center', bold=False, double_width=False)
            printer.text("Printer Test Page\n")
            printer.text(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            printer.text("\n")
            
            # ASCII Art - Cat with Bubble Tea (designed for 80mm paper)
            printer.set(align='center', bold=False)
            cat_art = """  /\\_/\\  
 ( o.o ) 
  > ^ <  Meow!
 /|   |\\
(_|   |_)
   | |
   |_| __
      |  |
      |O| Bubble!
      |__|
      |::|
"""
            printer.text(cat_art)
            printer.text("\n")
            
            # Test different text styles
            printer.set(align='left', bold=False)
            printer.text("Text Styles:\n")
            printer.text("--------------------\n")
            
            printer.set(bold=True)
            printer.text("Bold Text\n")
            
            printer.set(bold=False, underline=1)
            printer.text("Underlined Text\n")
            
            printer.set(underline=0, invert=True)
            printer.text("Inverted Text\n")
            
            printer.set(invert=False)
            printer.text("Normal Text\n")
            
            printer.text("--------------------\n\n")
            
            # Test alignment
            printer.set(align='left')
            printer.text("Left aligned\n")
            printer.set(align='center')
            printer.text("Center aligned\n")
            printer.set(align='right')
            printer.text("Right aligned\n\n")
            
            # Footer
            printer.set(align='center', bold=True)
            printer.text("Test Complete!\n")
            printer.set(bold=False)
            printer.text("If you can read this,\n")
            printer.text("your printer is working!\n\n")
            
            # Cut the paper
            printer.cut()
            
            print("✓ Test page printed successfully!")
            print("\nVerify the following on your printout:")
            print("  - ASCII cat with bubble tea is visible")
            print("  - Text styles (bold, underline, inverted) display correctly")
            print("  - Text alignment (left, center, right) works properly")
            print("  - Paper cuts cleanly")
            
        except Exception as print_error:
            print(f"✗ Error during printing: {print_error}")
            traceback.print_exc()
            return 1
            
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


def print_ticket(issue_key, cloud_id=None):
    """Print a Jira ticket"""
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Get cloud_id from environment if not provided
    if not cloud_id:
        cloud_id = os.getenv("ATLASSIAN_CLOUD_ID")
    
    if not cloud_id:
        print("Error: ATLASSIAN_CLOUD_ID not found in environment or arguments")
        print("Set it in .env file or pass --cloud-id argument")
        return 1
    
    print(f"Fetching Jira issue: {issue_key}...\n")
    
    try:
        # Check if MCP tools are available (only in copilot context)
        try:
            # Fetch the Jira issue using MCP Atlassian tool
            issue_data = mcp_atlassian_getJiraIssue(
                cloudId=cloud_id,
                issueIdOrKey=issue_key
            )
        except NameError:
            print("✗ MCP Atlassian tools are not available in this context")
            print("\nThis feature requires GitHub Copilot with MCP integration.")
            print("Please use one of these methods:")
            print(f"  1. Ask Copilot: 'Print Jira ticket {issue_key}'")
            print(f"  2. Ask Copilot: 'Fetch and print {issue_key} to the thermal printer'")
            print("\nAlternatively, you can use the print_ticket.py script directly")
            print("(but it currently uses sample data - MCP integration required for real data)")
            return 1
        
        print("✓ Issue fetched successfully\n")
        
        # Extract fields from the fetched issue
        fields = issue_data.get('fields', {})
        key = issue_data.get('key', issue_key)
        summary = fields.get('summary', 'No Summary')
        
        # Handle description which might be in ADF (Atlassian Document Format)
        description_field = fields.get('description', '')
        if isinstance(description_field, dict):
            # Extract plain text from ADF format
            description = extract_text_from_adf(description_field)
        else:
            description = description_field or ''
        
        status = fields.get('status', {}).get('name', 'Unknown')
        priority_obj = fields.get('priority')
        priority = priority_obj.get('name', 'None') if priority_obj else 'None'
        
        assignee_obj = fields.get('assignee')
        assignee = assignee_obj.get('displayName', 'Unassigned') if assignee_obj else 'Unassigned'
        
        issue_type = fields.get('issuetype', {}).get('name', 'Task')
        labels = fields.get('labels', [])
        
    except Exception as fetch_error:
        print(f"✗ Error fetching Jira issue: {fetch_error}")
        print("\nTroubleshooting:")
        print("1. Verify ATLASSIAN_CLOUD_ID is correct in .env")
        print("2. Ensure you have access to the issue")
        print("3. Check that the issue key is correct (e.g., PROJ-123)")
        print("4. Make sure MCP Atlassian tools are properly configured")
        return 1
    
    # Now print the ticket
    try:
        from printer_config import get_printer, PrinterConnectionError
        from dotenv import load_dotenv
        
        print(f"Connecting to printer...")
        try:
            printer = get_printer()
            print("✓ Printer connected\n")
        except PrinterConnectionError as e:
            print(f"✗ {e}")
            return 1
        
        print("Printing ticket...\n")
        
        # Helper function for text wrapping
        def wrap_text(text, width=24):
            if not text:
                return ""
            words = text.split()
            lines = []
            current_line = []
            current_length = 0
            for word in words:
                word_length = len(word)
                if current_length + word_length + len(current_line) <= width:
                    current_line.append(word)
                    current_length += word_length
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = word_length
            if current_line:
                lines.append(' '.join(current_line))
            return '\n'.join(lines)
        
        def truncate_text(text, max_length=500):
            if not text or len(text) <= max_length:
                return text
            return text[:max_length-3] + "..."
        
        # Print the ticket
        try:
            # Header with issue key
            printer.set(align='center', bold=True, double_height=True, double_width=True)
            printer.text(f"{key}\n")
            
            printer.set(align='center', bold=False, double_height=False, double_width=False)
            printer.text(f"[{issue_type}]\n")
            printer.text("\n")
            
            # Summary (wrapped)
            printer.set(align='left', bold=True, width=1, height=1)
            wrapped_summary = wrap_text(summary, width=24)
            printer.text(f"{wrapped_summary}\n")
            printer.text("\n")
            
            # Divider
            printer.set(bold=False)
            printer.text("========================\n")
            
            # Status and Priority
            printer.set(bold=True)
            printer.text(f"Status: ")
            printer.set(bold=False)
            printer.text(f"{status}\n")
            
            printer.set(bold=True)
            printer.text(f"Priority: ")
            printer.set(bold=False)
            printer.text(f"{priority}\n")
            
            printer.set(bold=True)
            printer.text(f"Assignee: ")
            printer.set(bold=False)
            printer.text(f"{assignee}\n")
            
            # Labels if any
            if labels:
                printer.set(bold=True)
                printer.text(f"Labels: ")
                printer.set(bold=False)
                printer.text(f"{', '.join(labels[:3])}\n")
            
            printer.text("========================\n")
            
            # Description (if available)
            if description:
                printer.text("\n")
                printer.set(bold=True)
                printer.text("Description:\n")
                printer.set(bold=False)
                
                desc_text = truncate_text(description, max_length=500)
                wrapped_desc = wrap_text(desc_text, width=24)
                printer.text(f"{wrapped_desc}\n")
            
            # Footer
            printer.text("\n")
            printer.set(align='center')
            printer.text("- - - - - - - - -\n")
            printer.text("Operation R\n")
            printer.text("\n")
            
            # Cut paper
            printer.cut()
            
            print("✓ Ticket printed successfully!")
            print(f"\nPrinted: {key} - {summary}")
            
        except Exception as print_error:
            print(f"✗ Error during printing: {print_error}")
            import traceback
            traceback.print_exc()
            return 1
            
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


def extract_text_from_adf(adf_content):
    """Extract plain text from Atlassian Document Format (ADF)"""
    if not adf_content:
        return ""
    
    def extract_text(node):
        if isinstance(node, str):
            return node
        
        if isinstance(node, dict):
            node_type = node.get('type', '')
            
            if node_type == 'text':
                return node.get('text', '')
            
            content = node.get('content', [])
            if content:
                texts = [extract_text(child) for child in content]
                
                if node_type in ['paragraph', 'heading', 'codeBlock']:
                    return '\n'.join(filter(None, texts)) + '\n'
                else:
                    return ' '.join(filter(None, texts))
        
        if isinstance(node, list):
            return ' '.join(extract_text(item) for item in node)
        
        return ""
    
    text = extract_text(adf_content)
    return ' '.join(text.split())


def start_server(host="0.0.0.0", port=5000):
    """Start the Flask web server for API endpoints"""
    print(f"Starting Flask web server on {host}:{port}...")
    print("Available endpoints:")
    print("  - POST /print - Print a task")
    print("  - POST /jira-webhook - Receive Jira webhooks")
    print("\nPress Ctrl+C to stop.\n")
    
    try:
        from flask import Flask, request, jsonify
        from escpos.printer import Usb
        import traceback
        
        app = Flask(__name__)
        
        # USB Vendor and Product ID
        USB_VENDOR_ID = int(os.getenv("USB_VENDOR_ID", "0x1fc9"), 16)
        USB_PRODUCT_ID = int(os.getenv("USB_PRODUCT_ID", "0x2016"), 16)
        
        # Initialize printer
        try:
            printer = Usb(USB_VENDOR_ID, USB_PRODUCT_ID)
            print("Printer connected successfully.")
        except Exception as e:
            printer = None
            print(f"Warning: Printer connection failed: {e}")
        
        @app.route("/print", methods=["POST"])
        def print_task():
            if not printer:
                return jsonify({"error": "Printer not connected"}), 500
            
            data = request.get_json()
            task = data.get("task", "Test task from Operation R")
            source = data.get("source", "manual")
            
            try:
                printer.set(align='center', bold=True)
                printer.text(f"Task from {source}:\n")
                printer.text(f"{task}\n")
                printer.text("\n---\n")
                printer.cut()
                return jsonify({"status": "Printed successfully"}), 200
            except Exception as e:
                print("Error during printing:")
                traceback.print_exc()
                return jsonify({"error": str(e)}), 500
        
        @app.route("/jira-webhook", methods=["POST"])
        def jira_webhook():
            if not printer:
                return jsonify({"error": "Printer not connected"}), 500
            
            data = request.get_json()
            issue = data.get("issue", {})
            fields = issue.get("fields", {})
            summary = fields.get("summary", "No summary")
            key = issue.get("key", "No key")
            status = fields.get("status", {}).get("name", "Unknown")
            
            try:
                printer.set(align='center', bold=True)
                printer.text(f"Jira Task: {key}\n")
                printer.text(f"{summary}\n")
                printer.text(f"Status: {status}\n")
                printer.text("\n\n")
                printer.cut()
                return jsonify({"status": "Printed from Jira"}), 200
            except Exception as e:
                print("Error during printing:")
                traceback.print_exc()
                return jsonify({"error": str(e)}), 500
        
        app.run(host=host, port=port)
        
    except KeyboardInterrupt:
        print("\nFlask server stopped.")
    except Exception as e:
        print(f"Error running Flask server: {e}")
        return 1
    return 0


def interactive_menu():
    """Display interactive menu for selecting features"""
    import glob
    
    while True:
        print("\n" + "=" * 40)
        print("Operation R - Main Menu")
        print("=" * 40)
        print("1. Fetch emails (start monitoring service)")
        print("2. Reset labels (remove 'Printed' labels)")
        print("3. Setup printer (configure USB/network)")
        print("4. Test print (verify printer setup)")
        print("5. Print ticket (from XML)")
        print("6. Print label (large text, rotated 90°)")
        print("7. Print barcode (scannable barcode)")
        print("8. ASCII Animals 🐾 (AI-generated art)")
        print("9. Start web server")
        print("0. Exit")
        print("=" * 40)
        
        choice = input("\nSelect option: ").strip()
        
        if choice == "0":
            print("Goodbye!")
            return 0
        elif choice == "1":
            return fetch_emails()
        elif choice == "2":
            return reset_labels()
        elif choice == "3":
            # Run printer setup wizard
            import subprocess
            result = subprocess.run([sys.executable, "setup_printer.py"])
            input("\nPress Enter to continue...")
            continue
        elif choice == "4":
            return test_print()
        elif choice == "5":
            # Scan tickets directory
            tickets_dir = os.path.join(os.path.dirname(__file__), "tickets")
            if not os.path.exists(tickets_dir):
                print(f"\n✗ Tickets directory not found: {tickets_dir}")
                input("\nPress Enter to continue...")
                continue
            
            xml_files = sorted(glob.glob(os.path.join(tickets_dir, "*.xml")))
            
            if not xml_files:
                print(f"\n✗ No XML files found in {tickets_dir}")
                input("\nPress Enter to continue...")
                continue
            
            # Display ticket selection menu
            print("\n" + "-" * 40)
            print("Available Tickets:")
            print("-" * 40)
            for i, xml_file in enumerate(xml_files, 1):
                ticket_name = os.path.basename(xml_file)
                print(f"{i}. {ticket_name}")
            print("0. Back to main menu")
            print("-" * 40)
            
            ticket_choice = input("\nSelect ticket to print: ").strip()
            
            if ticket_choice == "0":
                continue
            
            try:
                ticket_index = int(ticket_choice) - 1
                if 0 <= ticket_index < len(xml_files):
                    selected_file = xml_files[ticket_index]
                    import subprocess
                    result = subprocess.run([sys.executable, "print_ticket.py", selected_file])
                    if result.returncode == 0:
                        input("\nPress Enter to continue...")
                    else:
                        input("\nPrinting failed. Press Enter to continue...")
                else:
                    print("✗ Invalid selection")
                    input("\nPress Enter to continue...")
            except ValueError:
                print("✗ Invalid input")
                input("\nPress Enter to continue...")
                
        elif choice == "6":
            # Print label
            print("\n" + "-" * 40)
            print("Print Label (Large Text)")
            print("-" * 40)
            print("Text will be printed in large ASCII letters,")
            print("rotated 90° for lengthwise visibility.")
            print("-" * 40)
            
            label_text = input("\nEnter text for label: ").strip()
            
            if not label_text:
                print("✗ No text entered")
                input("\nPress Enter to continue...")
                continue
            
            if len(label_text) > 20:
                print(f"\nWarning: Text is {len(label_text)} characters long.")
                print("Label may be very lengthy.")
                confirm = input("Continue? (y/n): ").strip().lower()
                if confirm != 'y':
                    print("Cancelled")
                    input("\nPress Enter to continue...")
                    continue
            
            import subprocess
            result = subprocess.run([sys.executable, "print_label.py"] + label_text.split())
            if result.returncode == 0:
                input("\nPress Enter to continue...")
            else:
                input("\nPrinting failed. Press Enter to continue...")
                
        elif choice == "7":
            # Print barcode
            print("\n" + "-" * 40)
            print("Print Barcode (Scannable)")
            print("-" * 40)
            print("Generate barcodes for tickets, inventory, URLs, etc.")
            print("-" * 40)
            
            # Show barcode type menu
            print("\nSupported Barcode Types:")
            print("1. CODE128 (recommended for general use)")
            print("2. CODE39 (simple alphanumeric)")
            print("3. EAN13 (13-digit product codes)")
            print("4. EAN8 (8-digit compact codes)")
            print("5. UPC-A (12-digit retail)")
            print("6. ITF (numeric shipping/warehouse)")
            print("7. More options...")
            print("0. Back to main menu")
            
            bc_choice = input("\nSelect barcode type (default: 1): ").strip() or "1"
            
            if bc_choice == "0":
                continue
            
            barcode_types = {
                "1": "CODE128",
                "2": "CODE39",
                "3": "EAN13",
                "4": "EAN8",
                "5": "UPC-A",
                "6": "ITF",
                "7": None  # Show all options
            }
            
            barcode_type = barcode_types.get(bc_choice, "CODE128")
            
            if barcode_type is None:
                # Show all barcode types
                import subprocess
                subprocess.run([sys.executable, "print_barcode.py", "--list"])
                barcode_type = input("\nEnter barcode type: ").strip().upper() or "CODE128"
            
            # Get barcode text
            print(f"\nBarcode Type: {barcode_type}")
            barcode_text = input("Enter text/data to encode: ").strip()
            
            if not barcode_text:
                print("✗ No text entered")
                input("\nPress Enter to continue...")
                continue
            
            # Optional: Get custom height
            height_input = input("Barcode height (50-255, default: 100): ").strip()
            height = 100
            if height_input:
                try:
                    height = int(height_input)
                    if not (50 <= height <= 255):
                        print("Height out of range, using default (100)")
                        height = 100
                except ValueError:
                    print("Invalid height, using default (100)")
                    height = 100
            
            import subprocess
            cmd = [sys.executable, "print_barcode.py", barcode_text, 
                   "--type", barcode_type, "--height", str(height)]
            result = subprocess.run(cmd)
            if result.returncode == 0:
                input("\nPress Enter to continue...")
            else:
                input("\nBarcode printing failed. Press Enter to continue...")
                
        elif choice == "8":            # ASCII Animals
            import subprocess
            result = subprocess.run([sys.executable, "ascii_animals.py"])
            input("\nPress Enter to continue...")
            
        elif choice == "9":            
            print("\nStarting web server...")
            print("Host: 0.0.0.0")
            print("Port: 5000")
            return start_server(host="0.0.0.0", port=5000)
        else:
            print("✗ Invalid option")
            input("\nPress Enter to continue...")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog="operation-r",
        description="Operation R - Email-to-Printer System CLI",
        epilog="For more information, see README.md"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Fetch emails command
    fetch_parser = subparsers.add_parser(
        "fetch",
        help="Start the email fetching service"
    )
    
    # Reset labels command
    reset_parser = subparsers.add_parser(
        "reset-labels",
        help="Remove 'Printed' label from all emails"
    )
    
    # Setup printer command
    setup_parser = subparsers.add_parser(
        "setup",
        help="Run interactive printer setup wizard"
    )
    
    # Test print command
    test_parser = subparsers.add_parser(
        "test-print",
        help="Print a test page to verify printer setup"
    )
    
    # Print ticket command
    ticket_parser = subparsers.add_parser(
        "print-ticket",
        help="Print a Jira ticket to the thermal printer from XML export"
    )
    ticket_parser.add_argument(
        "xml_file",
        nargs="?",
        help="Path to Jira XML export file (optional, will show selection menu if omitted)"
    )
    
    # Print label command
    label_parser = subparsers.add_parser(
        "print-label",
        help="Print large text label rotated 90 degrees"
    )
    label_parser.add_argument(
        "text",
        nargs="+",
        help="Text to print on label"
    )
    
    # Print barcode command
    barcode_parser = subparsers.add_parser(
        "barcode",
        help="Generate and print scannable barcodes"
    )
    barcode_parser.add_argument(
        "text",
        nargs="?",
        help="Text or data to encode in the barcode"
    )
    barcode_parser.add_argument(
        "-t", "--type",
        default="CODE128",
        help="Barcode type (CODE128, CODE39, EAN13, etc.)"
    )
    barcode_parser.add_argument(
        "--height",
        type=int,
        default=100,
        help="Barcode height in dots (1-255, default: 100)"
    )
    barcode_parser.add_argument(
        "--width",
        type=int,
        default=3,
        help="Barcode module width in dots (2-6, default: 3)"
    )
    barcode_parser.add_argument(
        "--position",
        choices=['ABOVE', 'BELOW', 'BOTH', 'OFF'],
        default="BELOW",
        help="Position of human-readable text (default: BELOW)"
    )
    barcode_parser.add_argument(
        "--list",
        action="store_true",
        help="List all supported barcode types"
    )
    barcode_parser.add_argument(
        "--list-examples",
        action="store_true",
        help="Show barcode format examples"
    )
    
    # ASCII Animals command
    animals_parser = subparsers.add_parser(
        "animals",
        help="Generate AI-powered ASCII art of animals 🐾"
    )
    animals_parser.add_argument(
        "animal",
        nargs="?",
        help="Animal to generate (leave empty for interactive mode)"
    )
    animals_parser.add_argument(
        "--list",
        action="store_true",
        help="List available animals"
    )
    
    # Server command
    server_parser = subparsers.add_parser(
        "server",
        help="Start the Flask web server for API endpoints"
    )
    server_parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind the server to (default: 0.0.0.0)"
    )
    server_parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port to bind the server to (default: 5000)"
    )
    
    args = parser.parse_args()
    
    # If no command provided, show interactive menu
    if not args.command:
        return interactive_menu()
    
    # Route to appropriate function
    if args.command == "fetch":
        return fetch_emails()
    elif args.command == "reset-labels":
        return reset_labels()
    elif args.command == "setup":
        # Launch printer setup wizard
        import subprocess
        result = subprocess.run([sys.executable, "setup_printer.py"])
        return result.returncode
    elif args.command == "test-print":
        return test_print()
    elif args.command == "print-ticket":
        if args.xml_file:
            # Direct file path provided
            import subprocess
            result = subprocess.run([sys.executable, "print_ticket.py", args.xml_file])
            return result.returncode
        else:
            # Show ticket selection from tickets directory
            import glob
            tickets_dir = os.path.join(os.path.dirname(__file__), "tickets")
            if not os.path.exists(tickets_dir):
                print(f"✗ Tickets directory not found: {tickets_dir}")
                return 1
            
            xml_files = sorted(glob.glob(os.path.join(tickets_dir, "*.xml")))
            
            if not xml_files:
                print(f"✗ No XML files found in {tickets_dir}")
                return 1
            
            # Display ticket selection menu
            print("\nAvailable Tickets:")
            print("-" * 40)
            for i, xml_file in enumerate(xml_files, 1):
                ticket_name = os.path.basename(xml_file)
                print(f"{i}. {ticket_name}")
            print("-" * 40)
            
            ticket_choice = input("\nSelect ticket to print (number): ").strip()
            
            try:
                ticket_index = int(ticket_choice) - 1
                if 0 <= ticket_index < len(xml_files):
                    selected_file = xml_files[ticket_index]
                    import subprocess
                    result = subprocess.run([sys.executable, "print_ticket.py", selected_file])
                    return result.returncode
                else:
                    print("✗ Invalid selection")
                    return 1
            except ValueError:
                print("✗ Invalid input")
                return 1
    elif args.command == "print-label":
        # Print label with provided text
        label_text = ' '.join(args.text)
        import subprocess
        result = subprocess.run([sys.executable, "print_label.py"] + args.text)
        return result.returncode
    elif args.command == "barcode":
        # Print barcode
        import subprocess
        cmd = [sys.executable, "print_barcode.py"]
        
        if args.list:
            cmd.append("--list")
        elif args.list_examples:
            cmd.append("--list-examples")
        elif args.text:
            cmd.append(args.text)
            if args.type:
                cmd.extend(["--type", args.type])
            if args.height != 100:
                cmd.extend(["--height", str(args.height)])
            if args.width != 3:
                cmd.extend(["--width", str(args.width)])
            if args.position != "BELOW":
                cmd.extend(["--position", args.position])
        else:
            print("✗ Error: text is required (unless using --list or --list-examples)")
            return 1
        
        result = subprocess.run(cmd)
        return result.returncode
    elif args.command == "animals":
        # ASCII Animals
        import subprocess
        cmd = [sys.executable, "ascii_animals.py"]
        if args.list:
            cmd.append("--list")
        elif args.animal:
            cmd.append(args.animal)
        result = subprocess.run(cmd)
        return result.returncode
    elif args.command == "server":
        return start_server(host=args.host, port=args.port)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
