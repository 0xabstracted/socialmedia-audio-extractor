#!/usr/bin/env python3
"""
YouTube Cookies Export Utility
Helps export cookies for the Social Media Audio Extractor API
"""

import os
import sys
import subprocess
import shutil

def check_yt_dlp():
    """Check if yt-dlp is installed"""
    if not shutil.which('yt-dlp'):
        print("❌ yt-dlp not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'yt-dlp'], check=True)
    else:
        print("✅ yt-dlp found")

def export_cookies(browser='chrome', output_path='cookies.txt'):
    """Export cookies from browser"""
    try:
        print(f"🍪 Exporting cookies from {browser}...")
        
        cmd = [
            'yt-dlp',
            '--cookies-from-browser', browser,
            '--cookies', output_path,
            'https://www.youtube.com/robots.txt'  # Safe URL that doesn't require much data
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_path):
            print(f"✅ Cookies exported successfully to: {output_path}")
            
            # Check file size
            file_size = os.path.getsize(output_path)
            if file_size > 0:
                print(f"📁 File size: {file_size} bytes")
                
                # Set secure permissions
                os.chmod(output_path, 0o600)
                print("🔒 Set secure file permissions (600)")
                
                return True
            else:
                print("⚠️ Warning: Cookies file is empty - you might not be logged into YouTube")
                return False
        else:
            print(f"❌ Failed to export cookies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error exporting cookies: {e}")
        return False

def test_cookies(cookies_path='cookies.txt'):
    """Test if cookies work with yt-dlp"""
    if not os.path.exists(cookies_path):
        print(f"❌ Cookies file not found: {cookies_path}")
        return False
    
    try:
        print("🧪 Testing cookies with YouTube...")
        
        cmd = [
            'yt-dlp',
            '--cookies', cookies_path,
            '--skip-download',
            '--print', 'title',
            'https://www.youtube.com/shorts/dQw4w9WgXcQ'  # Test video
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Cookies are working! YouTube access successful")
            if result.stdout.strip():
                print(f"📺 Video title: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Cookies test failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Test timed out - cookies might be working but slowly")
        return False
    except Exception as e:
        print(f"❌ Error testing cookies: {e}")
        return False

def main():
    """Main function"""
    print("🎵 YouTube Cookies Export Utility")
    print("=" * 50)
    
    # Check yt-dlp installation
    check_yt_dlp()
    
    # Get browser choice
    browser = input("\nSelect browser (chrome/firefox/edge) [chrome]: ").strip().lower() or 'chrome'
    
    # Get output path
    output_path = input("Output path for cookies [cookies.txt]: ").strip() or 'cookies.txt'
    
    # Export cookies
    if export_cookies(browser, output_path):
        # Test cookies
        if test_cookies(output_path):
            print("\n🎉 SUCCESS! Your cookies are ready to use.")
            print(f"\n📋 Next steps:")
            print(f"1. Copy {output_path} to your server")
            print(f"2. Set environment variable: export YOUTUBE_COOKIES_PATH=/path/to/{output_path}")
            print(f"3. Restart your API container")
            print(f"4. Test with your YouTube URLs")
        else:
            print("\n⚠️ Cookies exported but may not be working correctly.")
            print("Try logging into YouTube in your browser and re-export.")
    else:
        print("\n❌ Cookie export failed. Please check:")
        print("1. You're logged into YouTube in your browser")
        print("2. The browser name is correct (chrome/firefox/edge)")
        print("3. You have permission to write files in this directory")

if __name__ == "__main__":
    main() 