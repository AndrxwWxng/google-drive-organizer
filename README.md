# Google Drive File Sorter

## Description

This project is a Python-based application that helps users organize and sort their Google Drive files. It provides a simple graphical user interface (GUI) that allows users to sort their files based on keywords.

## Features

- Connect to Google Drive using OAuth 2.0
- Sort files by keywords
- Display sorted files in a user-friendly GUI
- Easy-to-use interface for file management

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- A Google Cloud Platform account with Google Drive API enabled
- Required Python libraries: `google-auth-oauthlib`, `google-auth-httplib2`, `google-api-python-client`, `tkinter`

## Installation

1. Clone this repository:
   git clone https://github.com/AndrxwWxng/google-drive-organizer.git
2. Navigate to the project directory:
   cd google-drive-file-sorter
3. Install the required packages:
   pip install -r requirements.txt
4. Place your `credentials.json` file in the project directory. (See "Setting up Google Cloud Credentials" below if you haven't done this yet)

## Usage

1. Run the application:
   python gui.py
2. Enter a keyword in the text field
3. Click "Sort Files" to organize your Google Drive files
4. View the sorted files in the application window

## Setting up Google Cloud Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Drive API for your project
4. Create credentials (OAuth client ID) for a desktop application
5. Download the credentials file and rename it to `credentials.json`
6. Place `credentials.json` in the project directory

## File Structure

- `gui.py`: Contains the GUI implementation
- `sorter.py`: Implements the file sorting logic
- `config.py`: Stores configuration variables
- `requirements.txt`: Lists all the Python dependencies
