from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import SCOPES, CREDENTIALS_FILE, TOKEN_FILE

def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def search_files(service, keyword):
    query = f"name contains '{keyword}' and mimeType != 'application/vnd.google-apps.folder'"
    return search_items(service, query)

def search_folders(service, keyword):
    query = f"name contains '{keyword}' and mimeType = 'application/vnd.google-apps.folder'"
    return search_items(service, query)

def search_items(service, query):
    results = service.files().list(
        q=query,
        pageSize=1000,
        fields="nextPageToken, files(id, name)"
    ).execute()
    items = results.get('files', [])
    return sorted(items, key=lambda x: x['name'].lower())

def create_folder(service, folder_name):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    return folder.get('id')

def move_files_to_folder(service, file_ids, folder_id):
    for file_id in file_ids:
        file_metadata = service.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ','.join(file_metadata.get('parents', []))
        
        service.files().update(
            fileId=file_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()