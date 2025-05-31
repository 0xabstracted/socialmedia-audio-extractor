#!/usr/bin/env python3
"""
Test script to verify enhanced API functionality
Tests the problematic URL with fresh cookies and enhanced config
"""
import requests
import time
import json

# Your server URL - update this to match your actual server
BASE_URL = "http://localhost:8000"  # Change to your server URL

def test_problematic_url():
    """Test the URL that was previously failing"""
    
    # The URL that was causing bot detection issues
    problematic_url = "https://www.youtube.com/shorts/N8tJFeMXrr8"
    
    print(f"🧪 Testing enhanced API with problematic URL...")
    print(f"URL: {problematic_url}")
    print("=" * 60)
    
    # Test 1: Info extraction
    print("\n1️⃣  Testing info extraction...")
    
    payload = {
        "url": problematic_url,
        "format": "mp3",
        "quality": "192"
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/extract-audio-info", json=payload, timeout=30)
        end_time = time.time()
        
        print(f"⏱️  Response time: {end_time - start_time:.2f} seconds")
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS! Info extraction worked")
            print(f"   Title: {data.get('title', 'N/A')}")
            print(f"   Duration: {data.get('duration', 'N/A')} seconds")
            print(f"   Uploader: {data.get('uploader', 'N/A')}")
            print(f"   Extraction Method: {data.get('extraction_method', 'standard')}")
            
            # Test 2: Audio extraction
            print("\n2️⃣  Testing audio extraction...")
            
            payload["return_url"] = True  # Get URL instead of binary data for testing
            
            try:
                start_time = time.time()
                audio_response = requests.post(f"{BASE_URL}/extract-audio", json=payload, timeout=60)
                end_time = time.time()
                
                print(f"⏱️  Audio extraction time: {end_time - start_time:.2f} seconds")
                print(f"📊 Status code: {audio_response.status_code}")
                
                if audio_response.status_code == 200:
                    audio_data = audio_response.json()
                    print("✅ SUCCESS! Audio extraction worked")
                    print(f"   Download URL: {audio_data.get('download_url', 'N/A')}")
                    print(f"   File size: {audio_data.get('file_size', 'N/A')} bytes")
                else:
                    print("❌ Audio extraction failed")
                    print(f"   Error: {audio_response.text}")
                    
            except requests.exceptions.Timeout:
                print("❌ Audio extraction timed out")
            except Exception as e:
                print(f"❌ Audio extraction error: {e}")
                
        else:
            print("❌ Info extraction failed")
            print(f"   Error: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Info extraction timed out")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure your API server is running.")
        print(f"   Trying to connect to: {BASE_URL}")
        print("   Update BASE_URL in this script to match your server")
    except Exception as e:
        print(f"❌ Info extraction error: {e}")

def test_working_url():
    """Test with a URL that usually works to verify server is functioning"""
    
    working_url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
    
    print(f"\n\n🧪 Testing with known working URL (control test)...")
    print(f"URL: {working_url}")
    print("=" * 60)
    
    payload = {
        "url": working_url,
        "format": "mp3",
        "quality": "192"
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/extract-audio-info", json=payload, timeout=30)
        end_time = time.time()
        
        print(f"⏱️  Response time: {end_time - start_time:.2f} seconds")
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Control test passed - server is working")
            print(f"   Title: {data.get('title', 'N/A')}")
        else:
            print("❌ Control test failed - server issue")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Control test error: {e}")

def main():
    print("🚀 Enhanced YouTube API Test Suite")
    print("Testing fresh cookies and enhanced bot detection bypass")
    print("=" * 70)
    
    # Test the problematic URL first
    test_problematic_url()
    
    # Test a control URL
    test_working_url()
    
    print("\n" + "=" * 70)
    print("📋 Summary:")
    print("- If both tests pass: Your enhancements are working! 🎉")
    print("- If only control passes: Bot detection still needs work 🔧")
    print("- If both fail: Check server status and cookies 🛠️")
    print("\n💡 Tips if still failing:")
    print("- Try refreshing cookies again with: python3 refresh_cookies.py")
    print("- Check server logs for detailed error messages")
    print("- Consider using a different YouTube account for cookies")

if __name__ == "__main__":
    main() 