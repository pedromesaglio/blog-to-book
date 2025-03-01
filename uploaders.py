import os
import logging
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import requests
from typing import Optional, Dict
from config import UPLOAD_SERVICES

logger = logging.getLogger(__name__)

class GoogleDriveUploader:
    def __init__(self, config: Dict):
        self.credentials = Credentials(
            token=None,
            refresh_token=config['refresh_token'],
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            token_uri="https://oauth2.googleapis.com/token"
        )
        self.service = build('drive', 'v3', credentials=self.credentials)
        self.folder_id = config.get('folder_id')
    
    def upload(self, file_path: str) -> str:
        try:
            file_metadata = {'name': os.path.basename(file_path)}
            if self.folder_id:
                file_metadata['parents'] = [self.folder_id]
                
            media = MediaFileUpload(file_path)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='webViewLink'
            ).execute()
            
            logger.info(f"✅ Uploaded to Google Drive: {file['webViewLink']}")
            return file['webViewLink']
        except Exception as e:
            logger.error(f"🚨 Google Drive upload failed: {str(e)}")
            raise

class HttpUploader:
    def __init__(self, config: Dict):
        self.api_url = config['api_url']
        self.api_key = config['api_key']
    
    def upload(self, file_path: str) -> str:
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                headers = {'Authorization': f"Bearer {self.api_key}"}
                response = requests.post(
                    self.api_url,
                    files=files,
                    headers=headers,
                    timeout=30
                )
            response.raise_for_status()
            return response.json()['url']
        except Exception as e:
            logger.error(f"HTTP upload failed: {str(e)}")
            raise