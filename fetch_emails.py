from googleapiclient.discovery import build
import base64, email, os, time, sys
from dotenv import load_dotenv
from auth_gmail import authenticate

# Force output flushing for Docker logs
sys.stdout.reconfigure(line_buffering=True)

print("Starting fetch_emails.py...", flush=True)

load_dotenv()

print("Environment loaded", flush=True)

USB_VENDOR_ID = int(os.getenv("USB_VENDOR_ID", "0x0FE6"), 16)
USB_PRODUCT_ID = int(os.getenv("USB_PRODUCT_ID", "0x811E"), 16)

print("Authenticating with Gmail...", flush=True)
creds = authenticate()
print("Gmail authentication successful", flush=True)

service = build('gmail', 'v1', credentials=creds)
print("Gmail service built", flush=True)

# Get label IDs
labels_response = service.users().labels().list(userId='me').execute()
labels = labels_response.get('labels', [])

kanban_label_id = next((label['id'] for label in labels if label['name'] == 'KanbanPrint'), None)
printed_label_id = next((label['id'] for label in labels if label['name'] == 'Printed'), None)

if not kanban_label_id:
    print("Error: 'KanbanPrint' label not found. Please create it in Gmail.")
    exit(1)

if not printed_label_id:
    # Create the Printed label if it doesn't exist
    new_label = {
        'name': 'Printed',
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show'
    }
    created_label = service.users().labels().create(userId='me', body=new_label).execute()
    printed_label_id = created_label['id']

# Initialize printer
try:
    from escpos.printer import Usb
    printer = Usb(USB_VENDOR_ID, USB_PRODUCT_ID)
    print("Printer connected successfully.")
except Exception as e:
    print(f"Warning: Could not connect to USB printer: {e}")
    print("On Windows, you need to install libusb. Download from: https://github.com/libusb/libusb/releases")
    print("Extract libusb-1.0.dll to C:\\Windows\\System32 (or your Python directory)")
    print("\nContinuing without printer for testing...")
    printer = None

print("Starting email monitoring (checking every 10 minutes)...")

while True:
    try:
        # Query for emails with KanbanPrint label but without Printed label
        # Use labelIds parameter instead of query string
        results = service.users().messages().list(
            userId='me',
            labelIds=[kanban_label_id]
        ).execute()
        messages = results.get('messages', [])
        
        # Filter out messages that already have the Printed label
        filtered_messages = []
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='minimal').execute()
            if printed_label_id not in msg_data.get('labelIds', []):
                filtered_messages.append(msg)
        
        messages = filtered_messages

        if messages:
            print(f"Found {len(messages)} email(s) to print...")
            
            for msg in messages:
                msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
                headers = msg_data['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')

                body = ""
                parts = msg_data['payload'].get('parts', [])
                for part in parts:
                    if part['mimeType'] == 'text/plain':
                        data = part['body']['data']
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
                        break

                # Print the email
                if printer:
                    try:
                        printer.text(f"From: {sender}\nSubject: {subject}\n\n{body[:500]}\n")
                        printer.cut()
                        print(f"Printed: {subject}")
                    except Exception as print_error:
                        print(f"Error printing: {print_error}")
                        print("Libusb backend not available. Install libusb-1.0.dll for Windows.")
                        print(f"[TEST MODE] Would print: {subject}")
                else:
                    print(f"[TEST MODE] Would print: {subject}")
                
                # Add the Printed label
                service.users().messages().modify(
                    userId='me',
                    id=msg['id'],
                    body={'addLabelIds': [printed_label_id]}
                ).execute()
                
        # Wait 10 minutes before checking again
        time.sleep(600)
        
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(600)