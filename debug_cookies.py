#!/usr/bin/env python3
"""
Debug script to check cookie file and environment variable setup
"""
import os
import sys

def debug_cookies():
    print("🔍 Cookie Debug Information")
    print("=" * 50)
    
    # Check environment variable
    env_path = os.getenv('YOUTUBE_COOKIES_PATH')
    print(f"YOUTUBE_COOKIES_PATH environment variable: {env_path}")
    
    if env_path:
        print(f"✅ Environment variable is set")
        
        # Check if file exists
        if os.path.exists(env_path):
            print(f"✅ File exists at: {env_path}")
            
            # Check file size
            file_size = os.path.getsize(env_path)
            print(f"📁 File size: {file_size} bytes")
            
            # Check file permissions
            print(f"📋 File readable: {os.access(env_path, os.R_OK)}")
            
            # Show first few lines to verify format
            try:
                with open(env_path, 'r') as f:
                    lines = f.readlines()[:5]
                    print(f"📄 First few lines of cookies file:")
                    for i, line in enumerate(lines, 1):
                        print(f"   {i}: {line.strip()[:80]}...")
            except Exception as e:
                print(f"❌ Error reading file: {e}")
                
        else:
            print(f"❌ File does NOT exist at: {env_path}")
            
            # Check if directory exists
            dir_path = os.path.dirname(env_path)
            if os.path.exists(dir_path):
                print(f"📂 Directory exists: {dir_path}")
                
                # List files in directory
                try:
                    files = os.listdir(dir_path)
                    print(f"📋 Files in directory: {files}")
                except Exception as e:
                    print(f"❌ Error listing directory: {e}")
            else:
                print(f"❌ Directory does NOT exist: {dir_path}")
    else:
        print(f"❌ Environment variable is NOT set")
    
    # Check for cookies.txt in current directory
    print("\n🔍 Checking for cookies.txt in current directory...")
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    local_cookies = os.path.join(current_dir, 'cookies.txt')
    if os.path.exists(local_cookies):
        print(f"✅ Found cookies.txt in current directory: {local_cookies}")
        file_size = os.path.getsize(local_cookies)
        print(f"📁 File size: {file_size} bytes")
    else:
        print(f"❌ No cookies.txt found in current directory")
    
    # Check common cookie locations
    print("\n🔍 Checking common cookie locations...")
    common_paths = [
        '/app/cookies.txt',
        '/root/cookies.txt',
        '/root/socialmedia-audio-extractor/cookies.txt',
        './cookies.txt'
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            print(f"✅ Found: {path}")
        else:
            print(f"❌ Not found: {path}")
    
    print("\n" + "=" * 50)
    print("Debug complete!")

if __name__ == "__main__":
    debug_cookies() 