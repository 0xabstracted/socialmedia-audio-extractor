#!/usr/bin/env python3
"""
Advanced YouTube Extractor with Multiple Fallback Strategies
Implements various methods to bypass YouTube's bot detection
"""
import os
import random
import time
import json
from typing import Optional, Dict, Any

import yt_dlp

class AdvancedYouTubeExtractor:
    """Advanced YouTube extractor with multiple fallback strategies"""
    
    def __init__(self, cookies_path: str = None):
        self.cookies_path = cookies_path or 'cookies.txt'
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1'
        ]
    
    def get_base_opts(self) -> Dict[str, Any]:
        """Get base yt-dlp options"""
        opts = {
            'no_warnings': True,
            'quiet': True,
            'no_playlist': True,
            'writeinfojson': False,
            'writethumbnail': False,
            'user_agent': random.choice(self.user_agents),
            'referer': 'https://www.youtube.com/',
            'origin': 'https://www.youtube.com',
            'sleep_interval': random.uniform(1, 3),
            'max_sleep_interval': random.uniform(5, 8),
            'socket_timeout': 60,
            'retries': 2,
        }
        
        # Add cookies if available
        if os.path.exists(self.cookies_path):
            opts['cookiefile'] = self.cookies_path
        
        return opts
    
    def strategy_1_web_client(self, url: str) -> Optional[Dict[str, Any]]:
        """Strategy 1: Standard web client with enhanced headers"""
        print("🌐 Trying Strategy 1: Web client with enhanced headers...")
        
        opts = self.get_base_opts()
        opts.update({
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['web'],
                    'skip': ['dash', 'hls'],
                }
            }
        })
        
        return self._try_extract(url, opts)
    
    def strategy_2_android_client(self, url: str) -> Optional[Dict[str, Any]]:
        """Strategy 2: Android client (often bypasses restrictions)"""
        print("📱 Trying Strategy 2: Android client...")
        
        opts = self.get_base_opts()
        opts.update({
            'user_agent': 'com.google.android.youtube/17.31.35 (Linux; U; Android 11) gzip',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],
                    'skip': ['dash', 'hls'],
                }
            }
        })
        
        return self._try_extract(url, opts)
    
    def strategy_3_ios_client(self, url: str) -> Optional[Dict[str, Any]]:
        """Strategy 3: iOS client"""
        print("📱 Trying Strategy 3: iOS client...")
        
        opts = self.get_base_opts()
        opts.update({
            'user_agent': 'com.google.ios.youtube/17.31.4 (iPhone14,3; U; CPU iOS 15_6 like Mac OS X)',
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios'],
                    'skip': ['dash', 'hls'],
                }
            }
        })
        
        return self._try_extract(url, opts)
    
    def strategy_4_tv_client(self, url: str) -> Optional[Dict[str, Any]]:
        """Strategy 4: TV client (sometimes works for restricted content)"""
        print("📺 Trying Strategy 4: TV client...")
        
        opts = self.get_base_opts()
        opts.update({
            'user_agent': 'Mozilla/5.0 (ChromiumStylePlatform) Cobalt/Version',
            'extractor_args': {
                'youtube': {
                    'player_client': ['tv_embedded'],
                    'skip': ['dash', 'hls'],
                }
            }
        })
        
        return self._try_extract(url, opts)
    
    def strategy_5_embedded_client(self, url: str) -> Optional[Dict[str, Any]]:
        """Strategy 5: Embedded client"""
        print("🔗 Trying Strategy 5: Embedded client...")
        
        opts = self.get_base_opts()
        opts.update({
            'referer': 'https://www.google.com/',
            'extractor_args': {
                'youtube': {
                    'player_client': ['web_embedded'],
                    'skip': ['dash', 'hls'],
                }
            }
        })
        
        return self._try_extract(url, opts)
    
    def strategy_6_minimal_client(self, url: str) -> Optional[Dict[str, Any]]:
        """Strategy 6: Minimal configuration"""
        print("⚡ Trying Strategy 6: Minimal configuration...")
        
        opts = {
            'quiet': True,
            'no_warnings': True,
            'user_agent': random.choice(self.user_agents),
        }
        
        # Only add cookies if they exist
        if os.path.exists(self.cookies_path):
            opts['cookiefile'] = self.cookies_path
        
        return self._try_extract(url, opts)
    
    def _try_extract(self, url: str, opts: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Try to extract with given options"""
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            print(f"   ❌ Failed: {str(e)[:100]}...")
            return None
    
    def extract_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract video info using multiple strategies"""
        print(f"\n🎯 Extracting info for: {url}")
        print("=" * 60)
        
        strategies = [
            self.strategy_1_web_client,
            self.strategy_2_android_client,
            self.strategy_3_ios_client,
            self.strategy_4_tv_client,
            self.strategy_5_embedded_client,
            self.strategy_6_minimal_client,
        ]
        
        for i, strategy in enumerate(strategies, 1):
            try:
                result = strategy(url)
                if result:
                    print(f"✅ SUCCESS with Strategy {i}!")
                    return result
                
                # Add delay between strategies to avoid rate limiting
                if i < len(strategies):
                    delay = random.uniform(2, 5)
                    print(f"   ⏱️  Waiting {delay:.1f}s before next strategy...")
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"   ❌ Strategy {i} failed: {str(e)[:100]}...")
                continue
        
        print("❌ All strategies failed")
        return None
    
    def extract_audio_url(self, url: str) -> Optional[str]:
        """Extract audio URL from video"""
        info = self.extract_info(url)
        if not info:
            return None
        
        # Try to find audio-only format
        formats = info.get('formats', [])
        audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
        
        if audio_formats:
            # Sort by quality (prefer higher bitrate)
            audio_formats.sort(key=lambda x: x.get('abr', 0), reverse=True)
            return audio_formats[0]['url']
        
        # Fallback to best format with audio
        best_format = info.get('url')
        return best_format

def test_extractor():
    """Test the advanced extractor"""
    extractor = AdvancedYouTubeExtractor()
    
    # Test URLs that often trigger bot detection
    test_urls = [
        "https://www.youtube.com/shorts/N8tJFeMXrr8",  # Your problematic URL
        "https://www.youtube.com/shorts/dQw4w9WgXcQ",  # Rick Roll (often works)
    ]
    
    for url in test_urls:
        print(f"\n{'='*80}")
        print(f"Testing: {url}")
        print('='*80)
        
        info = extractor.extract_info(url)
        if info:
            print(f"\n📋 Success! Video Info:")
            print(f"   Title: {info.get('title', 'N/A')}")
            print(f"   Duration: {info.get('duration', 'N/A')} seconds")
            print(f"   Uploader: {info.get('uploader', 'N/A')}")
            print(f"   View Count: {info.get('view_count', 'N/A')}")
        else:
            print(f"\n❌ Failed to extract info from {url}")

if __name__ == "__main__":
    test_extractor() 