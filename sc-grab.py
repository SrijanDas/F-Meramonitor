import requests
import json
from datetime import datetime
import os
from pathlib import Path
import dotenv
import sys
from dateutil.parser import parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import signal
import threading

dotenv.load_dotenv()

def clean_filename(filename):
    """Clean filename by removing query parameters and special characters."""
    filename = filename.split('?')[0]
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def download_single_image(blob, download_dir, shutdown_event):
    """Download a single image from Azure Blob Storage."""
    if shutdown_event.is_set():
        return None
    
    filename = os.path.basename(blob['original'])
    cleaned_filename = clean_filename(filename)
    file_path = download_dir / cleaned_filename
    
    try:
        response = requests.get(blob['original'], stream=True)
        response.raise_for_status()
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if shutdown_event.is_set():
                    f.close()
                    os.remove(file_path)
                    return None
                f.write(chunk)
        return cleaned_filename
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return None

def download_images(date_str, max_workers=5):
    """
    Download images from Azure Blob Storage for a given date using parallel processing.
    
    Args:
        date_str (str): Date in format 'YYYY-MM-DD' or convertable to this format.
        max_workers (int): Number of parallel downloads to run. Defaults to 5.
    """
    date_str = parse(date_str, fuzzy=True).strftime("%Y-%m-%d")
    print(f'Intializing download for date: {date_str}')
    
    base_url = "https://api.meramonitor.com/api/v1/CloudStorageScreenshots/GetScreenshots"
    params = {
        "Email": "gladson@dezyit.com",
        "ReportDate": f"{date_str}T00:00:00Z",
        "OrganizationId": "676d0c4fae3947ba81b6d3e0",
        "UserId": "676d0f43ae3947ba81b7f31c"
    }
    
    token = os.getenv("API_TOKEN")
    if not token:
        raise ValueError("API_TOKEN not found in environment variables")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = json.loads(response.text)
        print(f'Captured json data, Images Count: {len(data["blobResponse"])}')
        
        download_dir = Path(f"downloads/{date_str}")
        download_dir.mkdir(parents=True, exist_ok=True)
        
        shutdown_event = threading.Event()
        original_handler = signal.getsignal(signal.SIGINT)
        
        def signal_handler(_, __):
            print("\nReceived Ctrl+C, initiating shutdown...")
            shutdown_event.set()
            signal.signal(signal.SIGINT, original_handler)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(download_single_image, blob, download_dir, shutdown_event): 
                      os.path.basename(blob['original']) 
                      for blob in data['blobResponse']}
            
            completed = 0
            total = len(futures)
            
            for future in as_completed(futures):
                if shutdown_event.is_set():
                    print("Cancelling remaining downloads...")
                    for f in futures:
                        f.cancel()
                    break
                
                filename = futures[future]
                try:
                    result = future.result()
                    if result:
                        completed += 1
                        print(f"Successfully downloaded {result} ({completed}/{total})")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        
        if shutdown_event.is_set():
            print("Shutdown completed. Partial download may exist.")
        else:
            print(f"Download completed. Total files: {completed}/{total}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage: python sc-grab.py 25-12-2025 (format not a issue)
    argv = sys.argv
    date_str = argv[1] if len(argv) > 1 else datetime.now().strftime("%Y-%m-%d")
    download_images(date_str, 80)