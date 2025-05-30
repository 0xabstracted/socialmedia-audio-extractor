#!/usr/bin/env python3
"""
Test script to demonstrate different methods of downloading MP3 files
"""
import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"  # Change to your server URL
# BASE_URL = "https://your-domain.com"  # For production

# Test URLs
test_urls = {
    "instagram_reel": "https://www.instagram.com/reel/DKRCV3gJIFZ",
}

def test_binary_download():
    """Method 1: Download MP3 as binary data (default behavior)"""
    print("🎵 Method 1: Binary Download")
    print("=" * 50)
    
    url = test_urls["instagram_reel"]
    payload = {
        "url": url,
        "format": "mp3",
        "quality": "192"
    }
    
    print(f"Extracting audio from: {url}")
    start_time = time.time()
    
    response = requests.post(f"{BASE_URL}/extract-audio", json=payload)
    
    if response.status_code == 200:
        # Save the binary data as MP3 file
        filename = f"binary_download_{int(time.time())}.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)
        
        duration = response.headers.get('X-Audio-Duration', 'Unknown')
        file_size = response.headers.get('X-File-Size', len(response.content))
        title = response.headers.get('X-Original-Title', 'Unknown')
        
        print(f"✅ Success!")
        print(f"   File saved: {filename}")
        print(f"   Title: {title}")
        print(f"   Duration: {duration} seconds")
        print(f"   File size: {file_size} bytes")
        print(f"   Processing time: {time.time() - start_time:.2f} seconds")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   {response.text}")
    
    print()

def test_url_download():
    """Method 2: Get download URL and fetch file separately"""
    print("🔗 Method 2: URL Download")
    print("=" * 50)
    
    url = test_urls["instagram_reel"]
    payload = {
        "url": url,
        "format": "mp3",
        "quality": "192",
        "return_url": True  # Request URL instead of binary data
    }
    
    print(f"Extracting audio from: {url}")
    start_time = time.time()
    
    response = requests.post(f"{BASE_URL}/extract-audio", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        download_url = data.get('download_url')
        
        print(f"✅ Extraction successful!")
        print(f"   Download URL: {BASE_URL}{download_url}")
        print(f"   Title: {data.get('title')}")
        print(f"   Duration: {data.get('duration')} seconds")
        print(f"   File size: {data.get('file_size')} bytes")
        
        # Now download the file using the URL
        print(f"🔽 Downloading file...")
        download_response = requests.get(f"{BASE_URL}{download_url}")
        
        if download_response.status_code == 200:
            filename = f"url_download_{int(time.time())}.mp3"
            with open(filename, "wb") as f:
                f.write(download_response.content)
            
            print(f"✅ File downloaded: {filename}")
            print(f"   Total time: {time.time() - start_time:.2f} seconds")
        else:
            print(f"❌ Download failed: {download_response.status_code}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   {response.text}")
    
    print()

def demo_curl_commands():
    """Method 3: Show cURL commands for server access"""
    print("💻 Method 3: Command Line Examples")
    print("=" * 50)
    
    print("🔹 Binary download with cURL:")
    print(f"""curl -X POST "{BASE_URL}/extract-audio" \\
  -H "Content-Type: application/json" \\
  -d '{{"url": "https://www.instagram.com/reel/DKRCV3gJIFZ", "format": "mp3"}}' \\
  --output downloaded_audio.mp3""")
    
    print("\n🔹 Get download URL with cURL:")
    print(f"""curl -X POST "{BASE_URL}/extract-audio" \\
  -H "Content-Type: application/json" \\
  -d '{{"url": "https://www.instagram.com/reel/DKRCV3gJIFZ", "return_url": true}}'""")
    
    print("\n🔹 Download using the returned URL:")
    print(f"""curl "{BASE_URL}/files/filename.mp3" --output my_audio.mp3""")
    
    print()

def demo_ssh_methods():
    """Method 4: Show SSH/SCP methods for server file access"""
    print("🖥️  Method 4: Server Access Methods")
    print("=" * 50)
    
    print("🔹 SSH into your Hostinger server:")
    print("ssh username@your-server-ip")
    
    print("\n🔹 Find MP3 files in temp directory:")
    print("find /tmp -name '*.mp3' -type f")
    
    print("\n🔹 Download files using SCP:")
    print("scp username@your-server-ip:/tmp/filename.mp3 ./local-file.mp3")
    
    print("\n🔹 Download files using rsync:")
    print("rsync -avz username@your-server-ip:/tmp/*.mp3 ./downloads/")
    
    print()

if __name__ == "__main__":
    print("🎵 Social Media Audio Extractor - Download Methods Demo")
    print("=" * 60)
    print()
    
    # Test binary download
    test_binary_download()
    
    # Test URL download
    test_url_download()
    
    # Show command line examples
    demo_curl_commands()
    
    # Show server access methods
    demo_ssh_methods()
    
    print("=" * 60)
    print("✅ Demo completed! Check the downloaded MP3 files.") 