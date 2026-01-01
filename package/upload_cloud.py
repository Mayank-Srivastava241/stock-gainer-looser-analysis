import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import date
import logging
logging.basicConfig(filename=f"loggs/{date.today().strftime("%d-%m-%Y")}_log.log",filemode="a",level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
 
def upload_to_cloud(name,file_id):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    CLIENT_SECRET = 'creds/oauth_secret.json'
    TOKEN_FILE = 'creds/token.json'
    DATE = date.today().strftime("%d-%m-%Y")
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid creds, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for next runs
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    # Build service
    service = build('drive', 'v3', credentials=creds)

    # File metadata (convert CSV → Google Sheet)
    file_metadata = {
        'name': f'{DATE}-{name}',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [f'{file_id}']
    }
    if(name == "gainer"):
        media = MediaFileUpload(
            'Data/gdata.csv',
            mimetype='text/csv',
            resumable=False
        )
    elif(name == "result"):
        media = MediaFileUpload(
            'Data/comparison_result.csv',
            mimetype='text/csv',
            resumable=False
        )
    else:
        media = MediaFileUpload(
            'Data/ldata.csv',
            mimetype='text/csv',
            resumable=False
        )

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    logging.info(f" {name} File uploaded successfully.")
    print(f" {name} File uploaded successfully.")


