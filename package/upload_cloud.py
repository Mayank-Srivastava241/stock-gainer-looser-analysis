import os
import json
from datetime import date
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def upload_to_cloud(name, file_id):
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    # Read service account JSON from environment variable
    service_account_info = json.loads(
        os.environ["GDRIVE_SERVICE_ACCOUNT"]
    )

    # Create credentials
    creds = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES
    )

    # Build Drive service
    service = build("drive", "v3", credentials=creds)

    DATE = date.today().strftime("%d-%m-%Y")

    # Decide which file to upload
    if name == "gainer":
        filepath = "Data/gdata.csv"
    elif name == "result":
        filepath = "Data/comparison_result.csv"
    else:
        filepath = "Data/ldata.csv"

    # Metadata: upload CSV as Google Sheet into existing folder
    file_metadata = {
        "name": f"{DATE}-{name}",
        "mimeType": "application/vnd.google-apps.spreadsheet",
        "parents": [file_id]
    }

    media = MediaFileUpload(
        filepath,
        mimetype="text/csv",
        resumable=False
    )

    # Upload file
    service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    print(f"{name} file uploaded successfully")
