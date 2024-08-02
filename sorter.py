from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import SCOPES, CREDENTIALS_FILE, TOKEN_FILE

def get_drive_service():
    #

def sort_files(service):
    #

def main():
    service = get_drive_service()
    sort_files(service)

if __name__ == '__main__':
    main()