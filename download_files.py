import csv
import webbrowser
import os

def read_download_links(csv_file):
    """Read download links from the CSV file"""
    download_links = []
    try:
        with open(csv_file, 'r') as file:
            # Skip the header row
            next(file)
            csv_reader = csv.reader(file, delimiter=',', quotechar='"')
            for row in csv_reader:
                if len(row) >= 5:  # Ensure row has enough columns
                    download_link = row[4].strip()  # Extract download link
                    if download_link and 'drive.google.com' in download_link:
                        download_links.append(download_link)
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return []
    
    return download_links

def open_downloads_in_browser(links):
    """Open each download link in the default browser"""
    if not links:
        print("No valid download links found in the CSV file.")
        return
    
    print(f"Found {len(links)} download links. Opening in browser...")
    for link in links:
        try:
            webbrowser.open(link)
            print(f"Opened: {link}")
        except Exception as e:
            print(f"Error opening link {link}: {str(e)}")

def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, 'bintang.csv')
    
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found")
        return
    
    # Read download links and open in browser
    links = read_download_links(csv_file)
    open_downloads_in_browser(links)

if __name__ == '__main__':
    main()