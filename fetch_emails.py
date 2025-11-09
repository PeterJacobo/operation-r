from googleapiclient.discovery import build
import base64, email, os
from escpos.printer import Usb
from dotenv import load_dotenv
from auth_gmail import authenticate

load_dotenv()

USB_VENDOR_ID = int(os.getenv("USB_VENDOR_ID", "0x1fc9"), 16)
USB_PRODUCT_ID = int(os.getenv("USB_PRODUCT_ID", "0x2016"), 16)

creds = authenticate()
service = build('gmail', 'v1', credentials=creds)

results = service.users().messages().list(userId='me', q='is:unread').execute()
messages = results.get('messages', [])

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

    printer = Usb(USB_VENDOR_ID, USB_PRODUCT_ID)
    printer.text(f"From: {sender}\nSubject: {subject}\n\n{body[:500]}\n")
    printer.cut()