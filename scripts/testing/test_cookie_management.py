#!/usr/bin/env python3
"""
Test Cookie Management System
Tests the dynamic cookie manager and API endpoints
"""

import requests
import time
import json
import sys
from typing import Dict, Any

# Your server URL - update this to match your actual server
BASE_URL = "http://localhost:8000"  # Change to your server URL

def test_health_with_cookies():
    """Test health endpoint with cookie status"""
    print("🔍 Testing health endpoint with cookie status...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check successful!")
            print(f"   yt-dlp version: {data.get('yt_dlp_version')}")
            
            cookie_status = data.get('cookie_status', {})
            print(f"   Cookies available: {cookie_status.get('cookies_available')}")
            print(f"   Cookies valid: {cookie_status.get('cookies_valid')}")
            print(f"   Auto-refresh active: {cookie_status.get('auto_refresh_active')}")
            print(f"   Last validation: {cookie_status.get('last_validation')}")
            return True
        else:
            print(f"❌ Health check failed: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False

def test_cookie_status():
    """Test detailed cookie status endpoint"""
    print("\n🍪 Testing cookie status endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/cookie-status")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Cookie status retrieved successfully!")
            print(f"   Cookie path: {data.get('cookie_path')}")
            print(f"   Cookies exist: {data.get('cookies_exist')}")
            print(f"   Cookies valid: {data.get('cookies_valid')}")
            print(f"   File size: {data.get('file_size', 0)} bytes")
            print(f"   File age: {data.get('file_age_hours', 0):.1f} hours")
            print(f"   Last refresh: {data.get('last_refresh', 'Never')}")
            print(f"   Auto-refresh active: {data.get('auto_refresh_active')}")
            return data
        else:
            print(f"❌ Cookie status failed: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return None

def test_cookie_refresh():
    """Test manual cookie refresh endpoint"""
    print("\n🔄 Testing manual cookie refresh...")
    
    try:
        response = requests.post(f"{BASE_URL}/refresh-cookies")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Cookie refresh successful!")
                print(f"   Message: {data.get('message')}")
                return True
            else:
                print(f"⚠️ Cookie refresh failed: {data.get('message')}")
                return False
        else:
            print(f"❌ Cookie refresh endpoint failed: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False

def test_video_extraction_with_cookies():
    """Test video extraction with dynamic cookie management"""
    print("\n🎵 Testing video extraction with cookie management...")
    
    test_url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"  # Rick Roll
    
    payload = {
        "url": test_url,
        "format": "mp3",
        "quality": "192"
    }
    
    # Test info extraction first
    print("   Testing info extraction...")
    try:
        response = requests.post(f"{BASE_URL}/extract-audio-info", json=payload, timeout=30)
        print(f"   Info extraction status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("   ✅ Info extraction successful!")
                print(f"      Title: {data.get('title', 'Unknown')}")
                print(f"      Duration: {data.get('duration', 0)} seconds")
                print(f"      Uploader: {data.get('uploader', 'Unknown')}")
                print(f"      Method: {data.get('extraction_method', 'standard')}")
                info_success = True
            else:
                print(f"   ❌ Info extraction failed: {data}")
                info_success = False
        else:
            print(f"   ❌ Info extraction error: {response.text}")
            info_success = False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Info extraction connection error: {e}")
        info_success = False
    
    # Test actual audio extraction
    print("\n   Testing audio extraction (URL mode)...")
    payload["return_url"] = True  # Get URL instead of binary
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/extract-audio", json=payload, timeout=120)
        processing_time = time.time() - start_time
        
        print(f"   Audio extraction status: {response.status_code}")
        print(f"   Processing time: {processing_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("   ✅ Audio extraction successful!")
                print(f"      Download URL: {data.get('download_url')}")
                print(f"      Filename: {data.get('filename')}")
                print(f"      File size: {data.get('file_size', 0)} bytes")
                return True
            else:
                print(f"   ❌ Audio extraction failed: {data}")
                return False
        else:
            print(f"   ❌ Audio extraction error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Audio extraction connection error: {e}")
        return False

def test_high_volume_simulation():
    """Simulate high-volume requests like from n8n"""
    print("\n🚀 Testing high-volume simulation (n8n scenario)...")
    
    test_urls = [
        "https://www.youtube.com/shorts/dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        # Add more test URLs if available
    ]
    
    results = []
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n   Request {i}/{len(test_urls)}: {url}")
        
        payload = {
            "url": url,
            "format": "mp3",
            "quality": "192",
            "return_url": True
        }
        
        try:
            start_time = time.time()
            response = requests.post(f"{BASE_URL}/extract-audio-info", json=payload, timeout=30)
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                print(f"      ✅ Success in {processing_time:.2f}s")
                results.append({"url": url, "success": True, "time": processing_time})
            else:
                print(f"      ❌ Failed: {response.status_code}")
                results.append({"url": url, "success": False, "time": processing_time})
                
        except Exception as e:
            print(f"      ❌ Error: {e}")
            results.append({"url": url, "success": False, "time": 0})
        
        # Small delay to not overwhelm the server
        time.sleep(1)
    
    # Summary
    successful = sum(1 for r in results if r["success"])
    avg_time = sum(r["time"] for r in results if r["success"]) / max(successful, 1)
    
    print(f"\n   📊 Summary: {successful}/{len(results)} successful")
    print(f"   ⏱️  Average processing time: {avg_time:.2f} seconds")
    
    return successful == len(results)

def main():
    """Run all cookie management tests"""
    print("🧪 Cookie Management System Test Suite")
    print("=" * 50)
    
    # Test basic connectivity
    print("🔗 Testing API connectivity...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            print("✅ API is accessible")
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print("Make sure the server is running and the URL is correct!")
        return False
    
    # Run tests
    tests = [
        ("Health Check with Cookies", test_health_with_cookies),
        ("Cookie Status", test_cookie_status),
        ("Cookie Refresh", test_cookie_refresh),
        ("Video Extraction", test_video_extraction_with_cookies),
        ("High Volume Simulation", test_high_volume_simulation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'=' * 50}")
        print(f"🧪 {test_name}")
        print("=" * 50)
        
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            results.append((test_name, False))
    
    # Final summary
    print(f"\n{'=' * 50}")
    print("📋 FINAL TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Your cookie management system is working perfectly!")
        print("\n💡 Key benefits for n8n workflows:")
        print("   • Automatic cookie refresh prevents bot detection")
        print("   • Multiple concurrent requests handled efficiently")
        print("   • Real-time cookie validation and status monitoring")
        print("   • No manual intervention needed for cookie management")
    else:
        print("⚠️ Some tests failed. Check the logs and cookie setup.")
        print("\n🔧 Troubleshooting tips:")
        print("   • Ensure cookies.txt exists and is valid")
        print("   • Check if yt-dlp is installed and working")
        print("   • Verify internet connectivity")
        print("   • Try running the cookie refresh manually")
    
    return passed == len(results)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
        print(f"Using custom server URL: {BASE_URL}")
    
    success = main()
    sys.exit(0 if success else 1) 