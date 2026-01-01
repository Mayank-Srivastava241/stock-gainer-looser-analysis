import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import date

def upload_to_cloud(name, file_id):
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service_account_info = json.loads(
        os.environ["GDRIVE_SERVICE_ACCOUNT"]
    )

    creds = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES
    )

    service = build('drive', 'v3', credentials=creds)

    DATE = date.today().strftime("%d-%m-%Y")

    file_metadata = {
        'name': f'{DATE}-{name}',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [file_id]
    }

    if name == "gainer":
        filepath = "Data/gdata.csv"
    elif name == "result":
        filepath = "Data/comparison_result.csv"
    else:
        filepath = "Data/ldata.csv"

    media = MediaFileUpload(filepath, mimetype="text/csv")

    service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    print(f"{name} file uploaded successfully")
