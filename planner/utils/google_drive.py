import io
import os
import json
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import environ

env = environ.Env()
environ.Env.read_env()

encoded_creds = env('GOOGLE_SERVICE_ACCOUNT_BASE64')
SERVICE_ACCOUNT_INFO = json.loads(base64.b64decode(encoded_creds))

# 🔥 THIS IS THE FIX
SERVICE_ACCOUNT_INFO['private_key'] = SERVICE_ACCOUNT_INFO['private_key'].replace("\\n", "\n")
SCOPES = ['https://www.googleapis.com/auth/drive.file']
PARENT_FOLDER_ID = env('GOOGLE_DRIVE_FOLDER_ID')

def get_or_create_user_folder(service, username, parent_folder_id):
    query = f"mimeType='application/vnd.google-apps.folder' and name='{username}' and '{parent_folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    
    if items:
        return items[0]['id']
    
    folder_metadata = {
        'name': username,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    return folder.get('id')

def upload_to_google_drive(file, filename, mimetype, username):
    credentials = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_INFO, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    user_folder_id = get_or_create_user_folder(service, username, PARENT_FOLDER_ID)

    file_metadata = {
        'name': filename,
        'parents': [user_folder_id]
    }

    media = MediaIoBaseUpload(file, mimetype=mimetype, resumable=True)

    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink, webContentLink'
    ).execute()

    service.permissions().create(
        fileId=uploaded_file['id'],
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()

    return uploaded_file['webViewLink']
