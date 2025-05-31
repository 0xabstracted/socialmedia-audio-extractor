#!/usr/bin/env python3
"""
Dynamic Cookie Manager for YouTube Audio Extractor
Handles automatic cookie refresh, validation, and hot-reloading
"""

import os
import time
import threading
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import subprocess
import tempfile

logger = logging.getLogger(__name__)

class CookieManager:
    """Manages YouTube cookies with automatic refresh and validation"""
    
    def __init__(self, cookie_path: str = "cookies.txt", refresh_interval_hours: int = 12):
        self.cookie_path = Path(cookie_path)
        self.refresh_interval = timedelta(hours=refresh_interval_hours)
        self.last_refresh = None
        self.last_modified = None
        self._lock = threading.Lock()
        self._cookies_valid = None
        self._last_validation = None
        
        # Auto-refresh thread
        self._stop_refresh = threading.Event()
        self._refresh_thread = None
        
        logger.info(f"Cookie manager initialized with path: {self.cookie_path}")
    
    def start_auto_refresh(self):
        """Start automatic cookie refresh thread"""
        if self._refresh_thread and self._refresh_thread.is_alive():
            return
            
        self._stop_refresh.clear()
        self._refresh_thread = threading.Thread(target=self._auto_refresh_loop, daemon=True)
        self._refresh_thread.start()
        logger.info("Auto-refresh thread started")
    
    def stop_auto_refresh(self):
        """Stop automatic cookie refresh thread"""
        if self._refresh_thread:
            self._stop_refresh.set()
            self._refresh_thread.join(timeout=5)
            logger.info("Auto-refresh thread stopped")
    
    def _auto_refresh_loop(self):
        """Background thread for automatic cookie refresh"""
        while not self._stop_refresh.wait(timeout=3600):  # Check every hour
            try:
                if self._should_refresh_cookies():
                    logger.info("Auto-refreshing cookies...")
                    self.refresh_cookies()
            except Exception as e:
                logger.error(f"Auto-refresh failed: {e}")
    
    def _should_refresh_cookies(self) -> bool:
        """Check if cookies should be refreshed"""
        if not self.cookie_path.exists():
            return True
            
        # Check if file is too old
        file_age = datetime.now() - datetime.fromtimestamp(self.cookie_path.stat().st_mtime)
        if file_age > self.refresh_interval:
            return True
            
        # Check if cookies are invalid
        if not self.validate_cookies():
            return True
            
        return False
    
    def get_cookies_path(self) -> str:
        """Get current cookies file path, refreshing if needed"""
        with self._lock:
            # Check if file was modified externally
            if self.cookie_path.exists():
                try:
                    current_modified = self.cookie_path.stat().st_mtime
                    if self.last_modified != current_modified:
                        self.last_modified = current_modified
                        self._cookies_valid = None  # Force revalidation
                        logger.info("Cookies file was modified externally, will revalidate")
                except PermissionError as e:
                    logger.warning(f"Cannot access cookie file stats: {e}")
            
            # Check if we can write to the cookies directory
            try:
                # Test write permissions
                test_file = self.cookie_path.parent / ".write_test"
                test_file.touch()
                test_file.unlink()
            except (PermissionError, OSError) as e:
                logger.error(f"No write permissions for cookie directory: {e}")
                logger.info("Cookie auto-refresh disabled due to read-only filesystem")
                return str(self.cookie_path) if self.cookie_path.exists() else None
            
            # Refresh if needed and we have write permissions
            if self._should_refresh_cookies():
                logger.warning("Cookies need refresh, attempting automatic refresh...")
                try:
                    self.refresh_cookies()
                except Exception as e:
                    logger.error(f"Failed to refresh cookies: {e}")
            
            return str(self.cookie_path)
    
    def validate_cookies(self, force: bool = False) -> bool:
        """Validate cookies by testing with yt-dlp"""
        if not force and self._cookies_valid is not None:
            # Use cached validation if recent (within 5 minutes)
            if self._last_validation and (datetime.now() - self._last_validation) < timedelta(minutes=5):
                return self._cookies_valid
        
        if not self.cookie_path.exists():
            self._cookies_valid = False
            return False
        
        try:
            # Test cookies with a simple YouTube request
            test_url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"  # Rick Roll - always available
            
            import yt_dlp
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'cookiefile': str(self.cookie_path),
                'extract_flat': True,
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(test_url, download=False)
                
            self._cookies_valid = True
            self._last_validation = datetime.now()
            logger.info("Cookie validation successful")
            return True
            
        except Exception as e:
            self._cookies_valid = False
            self._last_validation = datetime.now()
            logger.warning(f"Cookie validation failed: {e}")
            return False
    
    def refresh_cookies(self) -> bool:
        """Refresh cookies from browser"""
        try:
            # Import the refresh script functionality
            import sys
            sys.path.append('scripts/cookies')
            
            # Try different browsers in order of preference
            browsers = ['chrome', 'firefox', 'edge']
            
            for browser in browsers:
                try:
                    logger.info(f"Attempting to extract cookies from {browser}...")
                    
                    # Create backup of existing cookies
                    if self.cookie_path.exists():
                        backup_path = self.cookie_path.with_suffix('.backup')
                        self.cookie_path.rename(backup_path)
                        logger.info(f"Backed up existing cookies to {backup_path}")
                    
                    # Extract cookies using browser_cookie3 or similar
                    success = self._extract_cookies_from_browser(browser)
                    
                    if success and self.validate_cookies(force=True):
                        self.last_refresh = datetime.now()
                        self.last_modified = self.cookie_path.stat().st_mtime
                        logger.info(f"Successfully refreshed cookies from {browser}")
                        return True
                    
                except Exception as e:
                    logger.warning(f"Failed to extract from {browser}: {e}")
                    continue
            
            logger.error("Failed to refresh cookies from any browser")
            return False
            
        except Exception as e:
            logger.error(f"Cookie refresh failed: {e}")
            return False
    
    def _extract_cookies_from_browser(self, browser: str) -> bool:
        """Extract cookies from specified browser"""
        try:
            # Use yt-dlp's built-in cookie extraction
            cmd = [
                'yt-dlp',
                '--cookies-from-browser', browser,
                '--cookies', str(self.cookie_path),
                '--extract-flat',
                '--skip-download',
                'https://www.youtube.com/shorts/dQw4w9WgXcQ'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and self.cookie_path.exists():
                return True
            else:
                logger.warning(f"yt-dlp cookie extraction failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.warning(f"Cookie extraction from {browser} timed out")
            return False
        except Exception as e:
            logger.warning(f"Cookie extraction error: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cookie manager statistics"""
        stats = {
            "cookie_path": str(self.cookie_path),
            "cookies_exist": self.cookie_path.exists(),
            "last_refresh": self.last_refresh.isoformat() if self.last_refresh else None,
            "last_validation": self._last_validation.isoformat() if self._last_validation else None,
            "cookies_valid": self._cookies_valid,
            "auto_refresh_active": self._refresh_thread and self._refresh_thread.is_alive(),
        }
        
        if self.cookie_path.exists():
            stat = self.cookie_path.stat()
            stats.update({
                "file_size": stat.st_size,
                "file_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "file_age_hours": (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).total_seconds() / 3600
            })
        
        return stats

# Global cookie manager instance
_cookie_manager = None

def get_cookie_manager() -> CookieManager:
    """Get or create global cookie manager instance"""
    global _cookie_manager
    if _cookie_manager is None:
        cookie_path = os.getenv('YOUTUBE_COOKIES_PATH', 'cookies.txt')
        _cookie_manager = CookieManager(cookie_path)
        _cookie_manager.start_auto_refresh()
    return _cookie_manager

def shutdown_cookie_manager():
    """Shutdown global cookie manager"""
    global _cookie_manager
    if _cookie_manager:
        _cookie_manager.stop_auto_refresh()
        _cookie_manager = None 