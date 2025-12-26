import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import date
import logging
logging.basicConfig(filename=f"loggs/{date.today().strftime("%d-%m-%Y")}_log.log",filemode="a",level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')


def _get_credentials(scopes, client_secret='creds/oauth_secret.json', token_file='creds/token.json'):
    """Return credentials for Google API access.

    Priority order:
      1. SERVICE ACCOUNT JSON provided via env var `GDRIVE_SERVICE_ACCOUNT_JSON`
      2. TOKEN JSON provided via env var `GDRIVE_TOKEN_JSON` (written to `creds/token.json`)
      3. Existing `creds/token.json` file (non-interactive)
      4. Local interactive OAuth using `creds/oauth_secret.json` (only if not running in CI)

    Raises if no usable credentials are available in CI.
    """
    SCOPES = scopes

    # 1) Service account via environment secret
    sa_json = os.getenv('GDRIVE_SERVICE_ACCOUNT_JSON')
    if sa_json:
        os.makedirs(os.path.dirname(client_secret), exist_ok=True)
        sa_path = 'creds/sa_key.json'
        with open(sa_path, 'w') as f:
            f.write(sa_json)
        logging.info('Using service account credentials from env GDRIVE_SERVICE_ACCOUNT_JSON')
        return ServiceAccountCredentials.from_service_account_file(sa_path, scopes=SCOPES)

    # 2) Token JSON via env
    token_env = os.getenv('GDRIVE_TOKEN_JSON')
    if token_env:
        os.makedirs(os.path.dirname(token_file), exist_ok=True)
        with open(token_file, 'w') as f:
            f.write(token_env)
        logging.info('Wrote token.json from env GDRIVE_TOKEN_JSON')
        return Credentials.from_authorized_user_file(token_file, SCOPES)

    # 3) Existing token file
    if os.path.exists(token_file):
        logging.info('Loading credentials from existing token file')
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        return creds

    # 4) Interactive flow (only allowed locally)
    if os.path.exists(client_secret) and os.getenv('CI') is None:
        flow = InstalledAppFlow.from_client_secrets_file(client_secret, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
        logging.info('Completed local OAuth flow and wrote token file')
        return creds

    # No credentials available
    raise RuntimeError('No valid Google credentials found. Provide a service account via the GDRIVE_SERVICE_ACCOUNT_JSON secret, or provide a token JSON via GDRIVE_TOKEN_JSON, or run the interactive flow locally to create creds/token.json.')
 
def upload_to_cloud(name,file_id):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    CLIENT_SECRET = 'creds/oauth_secret.json'
    TOKEN_FILE = 'creds/token.json'
    DATE = date.today().strftime("%d-%m-%Y")
    # Obtain credentials non-interactively where possible.
    creds = _get_credentials(SCOPES, client_secret=CLIENT_SECRET, token_file=TOKEN_FILE)

    # Refresh if needed
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        raise RuntimeError('Obtained invalid or expired credentials. Check your credentials/secrets.')

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


