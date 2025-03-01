"""
Módulo para subir archivos a servicios en la nube.
"""
import os
import logging
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from typing import Optional

logger = logging.getLogger(__name__)

class GoogleDriveUploader:
    """Sube archivos a Google Drive."""
    
    def __init__(self, client_id: str, client_secret: str, refresh_token: str):
        self.credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret
        )
        self.service = build("drive", "v3", credentials=self.credentials)
    
    def upload(self, file_path: str, folder_id: Optional[str] = None) -> str:
        """Sube un archivo a Google Drive y retorna el enlace público."""
        file_name = os.path.basename(file_path)
        media = MediaFileUpload(file_path, resumable=True)
        
        file_metadata = {
            "name": file_name,
            "parents": [folder_id] if folder_id else []
        }
        
        try:
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id, webViewLink"
            ).execute()
            
            logger.info(f"Archivo subido a Google Drive: {file['webViewLink']}")
            return file["webViewLink"]
        except Exception as e:
            logger.error(f"Error al subir a Google Drive: {e}")
            raise

class HttpUploader:
    """Sube archivos a un servidor vía HTTP POST (ejemplo genérico)."""
    
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
    
    def upload(self, file_path: str) -> str:
        """Sube un archivo a un servidor remoto."""
        try:
            with open(file_path, "rb") as file:
                files = {"file": (os.path.basename(file_path), file)}
                headers = {"Authorization": f"Bearer {self.api_key}"}
                
                response = requests.post(
                    self.api_url,
                    files=files,
                    headers=headers,
                    timeout=30
                )
                
            response.raise_for_status()
            logger.info(f"Archivo subido exitosamente: {response.json()}")
            return response.json()["url"]
        except Exception as e:
            logger.error(f"Error en subida HTTP: {e}")
            raise