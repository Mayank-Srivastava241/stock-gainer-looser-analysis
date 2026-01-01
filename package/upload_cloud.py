import os
import json
from datetime import date
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def upload_to_cloud(name, file_id):
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    # Load service account JSON from environment variable
    service_account_info = json.loads(
        os.environ["GDRIVE_SERVICE_ACCOUNT"]
    )

    creds = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES
    )

    service = build("drive", "v3", credentials=creds)

    DATE = date.today().strftime("%d-%m-%Y")

    # -------- ORIGINAL IMPORTANT IF LOGIC (PRESERVED) --------
    if name == "gainer":
        filepath = "Data/gdata.csv"
    elif name == "result":
        filepath = "Data/comparison_result.csv"
    else:
        filepath = "Data/ldata.csv"
    # ---------------------------------------------------------

    # Upload as CSV (no Google Sheet conversion)
    file_metadata = {
        "name": f"{DATE}-{name}.csv",
        "parents": [file_id]
    }

    media = MediaFileUpload(
        filepath,
        mimetype="text/csv",
        resumable=False
    )

    service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    print(f"{name}.csv uploaded successfully")
