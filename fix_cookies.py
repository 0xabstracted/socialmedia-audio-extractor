#!/usr/bin/env python3
"""
Fixed Cookie Export - Multiple Methods
Handles Chrome encryption issues on macOS
"""

import os
import sys
import subprocess
import shutil

def method1_direct_yt_dlp():
    """Method 1: Direct yt-dlp with simpler URL"""
    print("🔄 Method 1: Direct export with simple URL...")
    
    try:
        cmd = [
            'yt-dlp',
            '--cookies-from-browser', 'chrome',
            '--cookies', 'cookies.txt',
            '--no-warnings',
            'https://www.youtube.com/shorts/dQw4w9WgXcQ'  # Use actual video instead of robots.txt
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and os.path.exists('cookies.txt'):
            file_size = os.path.getsize('cookies.txt')
            if file_size > 0:
                print(f"✅ Method 1 SUCCESS: cookies.txt created ({file_size} bytes)")
                return True
        
        print(f"❌ Method 1 failed: {result.stderr}")
        return False
        
    except Exception as e:
        print(f"❌ Method 1 error: {e}")
        return False

def method2_firefox_fallback():
    """Method 2: Try Firefox if available"""
    print("🔄 Method 2: Trying Firefox browser...")
    
    try:
        cmd = [
            'yt-dlp',
            '--cookies-from-browser', 'firefox',
            '--cookies', 'cookies_firefox.txt',
            '--no-warnings',
            'https://www.youtube.com/shorts/dQw4w9WgXcQ'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and os.path.exists('cookies_firefox.txt'):
            file_size = os.path.getsize('cookies_firefox.txt')
            if file_size > 0:
                # Rename to standard name
                os.rename('cookies_firefox.txt', 'cookies.txt')
                print(f"✅ Method 2 SUCCESS: Firefox cookies exported ({file_size} bytes)")
                return True
        
        print(f"❌ Method 2 failed: {result.stderr}")
        return False
        
    except Exception as e:
        print(f"❌ Method 2 error: {e}")
        return False

def method3_chrome_no_encryption():
    """Method 3: Try Chrome with different approach"""
    print("🔄 Method 3: Chrome with skip-download...")
    
    try:
        cmd = [
            'yt-dlp',
            '--cookies-from-browser', 'chrome',
            '--cookies', 'cookies.txt',
            '--skip-download',
            '--print', 'title',
            'https://www.youtube.com/shorts/dQw4w9WgXcQ'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if os.path.exists('cookies.txt'):
            file_size = os.path.getsize('cookies.txt')
            if file_size > 0:
                print(f"✅ Method 3 SUCCESS: cookies.txt created ({file_size} bytes)")
                return True
        
        print(f"❌ Method 3 failed: {result.stderr}")
        return False
        
    except Exception as e:
        print(f"❌ Method 3 error: {e}")
        return False

def method4_manual_instructions():
    """Method 4: Manual cookie export instructions"""
    print("\n🔄 Method 4: Manual Export Instructions")
    print("=" * 50)
    print("Since automatic export failed, here's how to do it manually:")
    print()
    print("📋 OPTION A: Browser Extension")
    print("1. Install 'Get cookies.txt LOCALLY' Chrome extension")
    print("2. Go to https://www.youtube.com")
    print("3. Click the extension icon")
    print("4. Save as 'cookies.txt'")
    print()
    print("📋 OPTION B: yt-dlp with login")
    print("Run this command and enter your YouTube credentials:")
    print("yt-dlp --username YOUR_EMAIL --password YOUR_PASSWORD --cookies cookies.txt --skip-download https://www.youtube.com/shorts/dQw4w9WgXcQ")
    print()
    print("📋 OPTION C: Continue without cookies")
    print("The API will try automatic browser cookie extraction on the server")
    
    return False

def test_cookies():
    """Test if cookies work"""
    if not os.path.exists('cookies.txt'):
        return False
    
    try:
        print("🧪 Testing cookies...")
        cmd = [
            'yt-dlp',
            '--cookies', 'cookies.txt',
            '--skip-download',
            '--print', 'title',
            'https://www.youtube.com/shorts/dQw4w9WgXcQ'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and result.stdout.strip():
            print(f"✅ Cookies test PASSED: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Cookies test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Cookie test error: {e}")
        return False

def main():
    """Try multiple methods to export cookies"""
    print("🍪 Cookie Export Fix - Multiple Methods")
    print("=" * 50)
    
    # Try methods in order
    methods = [
        method1_direct_yt_dlp,
        method2_firefox_fallback, 
        method3_chrome_no_encryption
    ]
    
    for i, method in enumerate(methods, 1):
        if method():
            # Test the cookies
            if test_cookies():
                print(f"\n🎉 SUCCESS! Method {i} worked!")
                print(f"📁 cookies.txt created: {os.path.getsize('cookies.txt')} bytes")
                print("\n📋 Next steps:")
                print("1. Copy cookies.txt to your server")
                print("2. Set: export YOUTUBE_COOKIES_PATH=/path/to/cookies.txt")
                print("3. Restart your API container")
                return
            else:
                print(f"⚠️ Method {i} created cookies but they don't work")
    
    # If all methods failed
    print("\n❌ All automatic methods failed")
    method4_manual_instructions()

if __name__ == "__main__":
    main() 