# drive_processor.py

from __future__ import print_function
import os.path
import os
import json
import io

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


class GoogleDriveProcessor:
    def __init__(self, folder_id, local_download_dir="downloads", record_file="processed_files.json"):
        self.folder_id = folder_id
        self.local_download_dir = local_download_dir
        self.record_file = record_file

        os.makedirs(local_download_dir, exist_ok=True)

        # Load record of processed files
        if os.path.exists(record_file):
            with open(record_file, "r") as f:
                self.processed_files = json.load(f)
        else:
            self.processed_files = {}

        # Setup Google Drive API service
        self.creds = None
        self.SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('drive', 'v3', credentials=self.creds)

    def sync_drive(self):
        """
        Downloads new or updated files from Drive folder.
        """
        query = f"'{self.folder_id}' in parents and trashed = false"
        results = self.service.files().list(
            q=query,
            pageSize=1000,
            fields="files(id, name, modifiedTime)"
        ).execute()

        items = results.get('files', [])
        downloaded_files = []

        if not items:
            print("No files found.")
        else:
            for file in items:
                file_id = file['id']
                file_name = file['name']
                modified_time = file['modifiedTime']

                if file_id not in self.processed_files or modified_time != self.processed_files[file_id]:
                    # Download file
                    request = self.service.files().get_media(fileId=file_id)
                    file_path = os.path.join(self.local_download_dir, file_name)
                    fh = io.FileIO(file_path, 'wb')
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                        if status:
                            print(f"Downloading {file_name}: {int(status.progress() * 100)}%")

                    print(f"Downloaded/Updated: {file_name}")
                    self.processed_files[file_id] = modified_time
                    downloaded_files.append(file_path)
                else:
                    print(f"Skipped unchanged: {file_name}")

        # Save updated record
        with open(self.record_file, "w") as f:
            json.dump(self.processed_files, f, indent=2)

        return downloaded_files
