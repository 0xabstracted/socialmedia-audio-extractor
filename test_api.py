"""
Test script for Social Media Audio Extractor API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

# Test URLs (replace with actual test URLs)
TEST_URLS = {
    "youtube_short": "https://www.youtube.com/shorts/N8tJFeMXrr8",  # Replace with actual URL
    "instagram_reel": "https://www.instagram.com/reel/DKRCV3gJIFZ",  # Replace with actual URL
}

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_root_endpoint():
    """Test root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_audio_info(url):
    """Test audio info extraction (no download)"""
    print(f"Testing audio info for: {url}")
    
    payload = {
        "url": url,
        "format": "mp3",
        "quality": "192"
    }
    
    response = requests.post(f"{BASE_URL}/extract-audio-info", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Title: {data.get('title')}")
        print(f"Duration: {data.get('duration')} seconds")
        print(f"Uploader: {data.get('uploader')}")
        print(f"Platform: {data.get('platform')}")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)

def test_audio_extraction(url, save_file=False):
    """Test audio extraction and download"""
    print(f"Testing audio extraction for: {url}")
    
    payload = {
        "url": url,
        "format": "mp3",
        "quality": "192"
    }
    
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/extract-audio", json=payload)
    end_time = time.time()
    
    print(f"Status: {response.status_code}")
    print(f"Processing time: {end_time - start_time:.2f} seconds")
    
    if response.status_code == 200:
        # Check headers
        headers = response.headers
        print(f"Content-Type: {headers.get('Content-Type')}")
        print(f"File-Size: {headers.get('X-File-Size')} bytes")
        print(f"Duration: {headers.get('X-Audio-Duration')} seconds")
        print(f"Original-Title: {headers.get('X-Original-Title')}")
        
        # Save file if requested
        if save_file:
            filename = headers.get('Content-Disposition', 'audio.mp3').split('filename=')[-1].strip('"')
            with open(f"test_{filename}", 'wb') as f:
                f.write(response.content)
            print(f"Audio saved as: test_{filename}")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)

def test_rate_limiting():
    """Test rate limiting"""
    print("Testing rate limiting (making rapid requests)...")
    
    payload = {
        "url": "https://youtube.com/shorts/invalid",  # Invalid URL for quick response
        "format": "mp3"
    }
    
    for i in range(5):
        response = requests.post(f"{BASE_URL}/extract-audio-info", json=payload)
        print(f"Request {i+1}: Status {response.status_code}")
        
        if response.status_code == 429:
            print("Rate limit reached (as expected)")
            break
    
    print("-" * 50)

def test_invalid_urls():
    """Test with invalid URLs"""
    print("Testing invalid URLs...")
    
    invalid_urls = [
        "https://example.com",
        "https://facebook.com/video",
        "not-a-url",
        "https://youtube.com/watch?v=invalid"
    ]
    
    for url in invalid_urls:
        payload = {"url": url}
        response = requests.post(f"{BASE_URL}/extract-audio-info", json=payload)
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:100]}...")
        print("-" * 30)

def main():
    """Run all tests"""
    print("=" * 60)
    print("SOCIAL MEDIA AUDIO EXTRACTOR API TESTS")
    print("=" * 60)
    
    # Basic endpoint tests
    test_health_check()
    test_root_endpoint()
    
    # Invalid URL tests
    test_invalid_urls()
    
    # Rate limiting test
    test_rate_limiting()
    
    # Note: Actual URL tests commented out - replace with real URLs to test
    print("NOTE: To test with real URLs, update the TEST_URLS dictionary")
    print("with actual YouTube Shorts or Instagram Reels URLs")
    
    # Uncomment these lines and add real URLs to test actual extraction
    # for platform, url in TEST_URLS.items():
    #     print(f"\nTesting {platform}:")
    #     test_audio_info(url)
    #     test_audio_extraction(url, save_file=True)

if __name__ == "__main__":
    main() 