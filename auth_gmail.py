from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle, os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            auth_url, _ = flow.authorization_url(prompt='consent')

            print("Go to this URL:", auth_url)
            code = input("Enter the authorization code: ")
            creds = flow.fetch_token(code=code)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds