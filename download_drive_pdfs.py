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

def list_files_recursive(service, folder_id, base_path='downloads', pdf_count=0, folder_count=0):
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
                    # Create folder in local filesystem
                    new_base_path = os.path.join(base_path, file['name'])
                    os.makedirs(new_base_path, exist_ok=True)
                    # Recursively list files in subfolder
                    sub_results = list_files_recursive(service, file['id'], new_base_path, pdf_count, folder_count)
                    results.extend(sub_results)
                elif file['mimeType'] == 'application/pdf':
                    # Add PDF file to download list
                    pdf_count += 1
                    print(f"Found PDF ({pdf_count}): {file['name']}")
                    results.append({
                        'id': file['id'],
                        'name': file['name'],
                        'path': base_path
                    })
            
            page_token = response.get('nextPageToken')
            if not page_token:
                break
                
        except Exception as e:
            print(f'An error occurred: {e}')
            break
    
    return results

def download_files(service, files):
    """Download the list of files."""
    for file in files:
        try:
            request = service.files().get_media(fileId=file['id'])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            
            print(f"Downloading {file['name']}...")
            while done is False:
                status, done = downloader.next_chunk()
                if status:
                    print(f"Download {int(status.progress() * 100)}%")
            
            # Save the file
            fh.seek(0)
            file_path = os.path.join(file['path'], file['name'])
            with open(file_path, 'wb') as f:
                f.write(fh.read())
                print(f"Saved to {file_path}")
                
        except Exception as e:
            print(f"Error downloading {file['name']}: {e}")

def main():
    # Create downloads directory
    os.makedirs('downloads', exist_ok=True)
    
    print("Authenticating...")
    service = get_google_drive_service()
    
    # Replace with your shared folder ID
    folder_id = input("Enter the shared folder ID: ")
    
    print("\nListing PDF files...")
    files = list_files_recursive(service, folder_id)
    
    if not files:
        print("No PDF files found in the folder.")
        return
    
    print(f"\nFound {len(files)} PDF files. Starting download...")
    download_files(service, files)
    print("\nDownload completed!")

if __name__ == '__main__':
    main()