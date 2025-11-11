from googleapiclient.discovery import build
from auth_gmail import authenticate

creds = authenticate()
service = build('gmail', 'v1', credentials=creds)

# Get label IDs
labels_response = service.users().labels().list(userId='me').execute()
labels = labels_response.get('labels', [])

printed_label_id = next((label['id'] for label in labels if label['name'] == 'Printed'), None)

if not printed_label_id:
    print("No 'Printed' label found.")
    exit(0)

# Get all messages with Printed label
results = service.users().messages().list(userId='me', labelIds=[printed_label_id]).execute()
messages = results.get('messages', [])

if not messages:
    print("No emails have the 'Printed' label.")
else:
    print(f"Found {len(messages)} email(s) with 'Printed' label. Removing...")
    
    for msg in messages:
        service.users().messages().modify(
            userId='me',
            id=msg['id'],
            body={'removeLabelIds': [printed_label_id]}
        ).execute()
    
    print(f"Removed 'Printed' label from {len(messages)} email(s).")
