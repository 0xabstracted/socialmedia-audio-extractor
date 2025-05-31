#!/usr/bin/env python3
"""
Advanced Cookie Refresh Script for YouTube API
Handles multiple browser types and provides detailed guidance
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_yt_dlp():
    """Check if yt-dlp is available"""
    try:
        result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True)
        print(f"✅ yt-dlp found: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("❌ yt-dlp not found. Installing...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'yt-dlp'], check=True)
            print("✅ yt-dlp installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install yt-dlp")
            return False

def extract_cookies_chrome():
    """Extract cookies from Chrome browser"""
    print("\n🔍 Attempting to extract cookies from Chrome...")
    
    try:
        # Backup old cookies
        if os.path.exists('cookies.txt'):
            shutil.copy('cookies.txt', 'cookies_backup.txt')
            print("📁 Backed up existing cookies to cookies_backup.txt")
        
        # Extract fresh cookies from Chrome
        cmd = [
            'yt-dlp',
            '--cookies-from-browser', 'chrome',
            '--cookies', 'cookies.txt',
            '--no-download',
            'https://www.youtube.com'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists('cookies.txt'):
            file_size = os.path.getsize('cookies.txt')
            print(f"✅ Successfully extracted Chrome cookies ({file_size} bytes)")
            return True
        else:
            print(f"❌ Failed to extract Chrome cookies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error extracting Chrome cookies: {e}")
        return False

def extract_cookies_firefox():
    """Extract cookies from Firefox browser"""
    print("\n🔍 Attempting to extract cookies from Firefox...")
    
    try:
        cmd = [
            'yt-dlp',
            '--cookies-from-browser', 'firefox',
            '--cookies', 'cookies_firefox.txt',
            '--no-download',
            'https://www.youtube.com'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists('cookies_firefox.txt'):
            file_size = os.path.getsize('cookies_firefox.txt')
            print(f"✅ Successfully extracted Firefox cookies ({file_size} bytes)")
            
            # Use Firefox cookies as main if Chrome failed
            if not os.path.exists('cookies.txt') or os.path.getsize('cookies.txt') < 1000:
                shutil.copy('cookies_firefox.txt', 'cookies.txt')
                print("✅ Set Firefox cookies as primary cookies.txt")
            
            return True
        else:
            print(f"❌ Failed to extract Firefox cookies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error extracting Firefox cookies: {e}")
        return False

def extract_cookies_edge():
    """Extract cookies from Edge browser"""
    print("\n🔍 Attempting to extract cookies from Edge...")
    
    try:
        cmd = [
            'yt-dlp',
            '--cookies-from-browser', 'edge',
            '--cookies', 'cookies_edge.txt',
            '--no-download',
            'https://www.youtube.com'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists('cookies_edge.txt'):
            file_size = os.path.getsize('cookies_edge.txt')
            print(f"✅ Successfully extracted Edge cookies ({file_size} bytes)")
            
            # Use Edge cookies as main if others failed
            if not os.path.exists('cookies.txt') or os.path.getsize('cookies.txt') < 1000:
                shutil.copy('cookies_edge.txt', 'cookies.txt')
                print("✅ Set Edge cookies as primary cookies.txt")
            
            return True
        else:
            print(f"❌ Failed to extract Edge cookies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error extracting Edge cookies: {e}")
        return False

def validate_cookies():
    """Validate that cookies contain YouTube data"""
    if not os.path.exists('cookies.txt'):
        print("❌ No cookies.txt file found")
        return False
    
    try:
        with open('cookies.txt', 'r') as f:
            content = f.read()
            
        youtube_cookies = content.count('youtube.com')
        googlevideo_cookies = content.count('googlevideo.com')
        
        print(f"\n📊 Cookie Analysis:")
        print(f"   - YouTube cookies: {youtube_cookies}")
        print(f"   - Google Video cookies: {googlevideo_cookies}")
        
        if youtube_cookies > 0:
            print("✅ Cookies contain YouTube data")
            return True
        else:
            print("❌ No YouTube cookies found")
            return False
            
    except Exception as e:
        print(f"❌ Error validating cookies: {e}")
        return False

def test_cookies():
    """Test cookies with a simple YouTube request"""
    print("\n🧪 Testing cookies with YouTube...")
    
    try:
        cmd = [
            'yt-dlp',
            '--cookies', 'cookies.txt',
            '--no-download',
            '--get-title',
            'https://www.youtube.com/shorts/dQw4w9WgXcQ'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Cookies working! Test extraction successful")
            print(f"   Title: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Cookie test failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Cookie test timed out - possible bot detection")
        return False
    except Exception as e:
        print(f"❌ Error testing cookies: {e}")
        return False

def manual_cookie_instructions():
    """Provide manual cookie extraction instructions"""
    print("\n" + "="*60)
    print("📋 MANUAL COOKIE EXTRACTION INSTRUCTIONS")
    print("="*60)
    print("""
If automatic extraction failed, follow these steps:

1. 🔐 PRIVATE BROWSING METHOD (RECOMMENDED):
   - Open an incognito/private browser window
   - Log into YouTube with a throwaway account
   - Navigate to: https://www.youtube.com/robots.txt
   - Install browser extension: "Get cookies.txt LOCALLY"
   - Export cookies as "cookies.txt"
   - Close private window immediately

2. 🧩 BROWSER EXTENSION METHOD:
   - Install extension: "Get cookies.txt LOCALLY" 
   - Go to YouTube.com (while logged in)
   - Click extension icon
   - Export as "cookies.txt"
   - Place in your project directory

3. 🔄 ALTERNATIVE BROWSERS:
   - Try different browsers if one doesn't work
   - Use different YouTube accounts
   - Clear browser cache before extracting

4. 🔒 SECURITY TIPS:
   - Use a separate account for API access
   - Don't use your main YouTube account
   - Refresh cookies weekly if using frequently

After manual extraction, run this script again to validate.
""")

def main():
    print("🍪 YouTube Cookie Refresh Tool")
    print("=" * 50)
    
    # Check if yt-dlp is available
    if not check_yt_dlp():
        print("❌ Cannot proceed without yt-dlp")
        return False
    
    success = False
    
    # Try different browsers
    browsers = [
        ("Chrome", extract_cookies_chrome),
        ("Firefox", extract_cookies_firefox),
        ("Edge", extract_cookies_edge),
    ]
    
    for browser_name, extract_func in browsers:
        print(f"\n{'='*20} {browser_name} {'='*20}")
        if extract_func():
            success = True
            break
    
    if success:
        # Validate cookies
        if validate_cookies():
            # Test cookies
            if test_cookies():
                print("\n🎉 SUCCESS! Cookies refreshed and tested successfully")
                print("✅ Your API should now work with YouTube Shorts")
                return True
            else:
                print("\n⚠️  Cookies extracted but test failed")
                print("💡 Try using different account or browser")
        else:
            print("\n❌ Cookie validation failed")
    
    if not success:
        print("\n❌ Automatic cookie extraction failed for all browsers")
        manual_cookie_instructions()
    
    return success

if __name__ == "__main__":
    main() 