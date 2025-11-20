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
        from escpos.printer import Usb
        from dotenv import load_dotenv
        import traceback
        from datetime import datetime
        
        load_dotenv()
        
        # USB Vendor and Product ID from environment
        USB_VENDOR_ID = int(os.getenv("USB_VENDOR_ID", "0x0FE6"), 16)
        USB_PRODUCT_ID = int(os.getenv("USB_PRODUCT_ID", "0x811E"), 16)
        
        print(f"Attempting to connect to printer...")
        print(f"USB Vendor ID: 0x{USB_VENDOR_ID:04X}")
        print(f"USB Product ID: 0x{USB_PRODUCT_ID:04X}\n")
        
        try:
            printer = Usb(USB_VENDOR_ID, USB_PRODUCT_ID)
            print("✓ Printer connected successfully!\n")
        except Exception as e:
            print(f"✗ Failed to connect to printer: {e}")
            print("\nTroubleshooting:")
            print("1. Ensure printer is powered on and connected via USB")
            print("2. On Windows, install libusb from: https://github.com/libusb/libusb/releases")
            print("3. Extract libusb-1.0.dll to C:\\Windows\\System32")
            print("4. Verify USB_VENDOR_ID and USB_PRODUCT_ID in .env file")
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
        from escpos.printer import Usb
        from dotenv import load_dotenv
        
        USB_VENDOR_ID = int(os.getenv("USB_VENDOR_ID", "0x0FE6"), 16)
        USB_PRODUCT_ID = int(os.getenv("USB_PRODUCT_ID", "0x811E"), 16)
        
        print(f"Connecting to printer...")
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
        print("3. Test print (verify printer setup)")
        print("4. Print ticket (from XML)")
        print("5. Start web server")
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
            return test_print()
        elif choice == "4":
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
                
        elif choice == "5":
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
    elif args.command == "server":
        return start_server(host=args.host, port=args.port)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
