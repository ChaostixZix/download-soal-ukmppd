import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_google_drive_service():
    """Get an authorized Google Drive service instance."""
    creds = None
    
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    d
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def list_files_recursive(service, folder_id, base_path='downloads', pdf_count=0, folder_count=0, existing_files=None):
    """List all PDF files in the folder and its subfolders."""
    results = []
    folder_count += 1
    page_token = None
    
    while True:
        try:
            # List files in the current folder
            response = service.files().list(
                q=f"'{folder_id}' in parents",
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType)',
                pageToken=page_token
            ).execute()
            
            files = response.get('files', [])
            print(f"\nScanning folder {folder_count}: {base_path}")
            print(f"Found {len(files)} items in current folder")
            
            for file in files:
                if file['mimeType'] == 'application/vnd.google-apps.folder':
                    new_base_path = os.path.join(base_path, file['name'])
                    os.makedirs(new_base_path, exist_ok=True)
                    sub_results = list_files_recursive(service, file['id'], new_base_path, pdf_count, folder_count, existing_files)
                    results.extend(sub_results)
                elif file['mimeType'] == 'application/pdf':
                    file_path = os.path.join(base_path, file['name'])
                    if file_path not in existing_files:
                        pdf_count += 1
                        print(f"Found new PDF ({pdf_count}): {file['name']}")
                        results.append({
                            'id': file['id'],
                            'name': file['name'],
                            'path': base_path
                        })
                    else:
                        print(f"Skipping existing PDF: {file['name']}")
            
            page_token = response.get('nextPageToken')
            if not page_token:
                break
                
        except Exception as e:
            print(f'An error occurred: {e}')
            break
    
    return results

def download_files(service, files):
    """Download the list of files."""
    total_files = len(files)
    for index, file in enumerate(files, 1):
        try:
            print(f"\nDownloading file {index}/{total_files}: {file['name']}...")
            request = service.files().get_media(fileId=file['id'])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            
            while done is False:
                status, done = downloader.next_chunk()
                if status:
                    print(f"Download {int(status.progress() * 100)}%")
            
            fh.seek(0)
            file_path = os.path.join(file['path'], file['name'])
            with open(file_path, 'wb') as f:
                f.write(fh.read())
                print(f"Saved to {file_path}")
                
        except Exception as e:
            print(f"Error downloading {file['name']}: {e}")

def get_existing_files(directories):
    """Get list of existing PDF files in the specified directories."""
    existing_files = set()
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    full_path = os.path.join(root, file)
                    existing_files.add(full_path)
    return existing_files

def main():
    # Create directories
    for directory in ['downloads', 'departments']:
        os.makedirs(directory, exist_ok=True)
    
    # Get existing files
    existing_files = get_existing_files(['downloads', 'departments'])
    print(f"Found {len(existing_files)} existing PDF files")
    
    print("Authenticating...")
    service = get_google_drive_service()
    
    folder_id = input("Enter the shared folder ID: ")
    
    print("\nListing PDF files...")
    files = list_files_recursive(service, folder_id, base_path='downloads', existing_files=existing_files)
    
    if not files:
        print("No new PDF files found to download.")
        return
    
    print(f"\nFound {len(files)} new PDF files. Starting download...")
    download_files(service, files)
    print("\nDownload completed!")

if __name__ == '__main__':
    main()