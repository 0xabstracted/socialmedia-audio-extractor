"""
Social Media Audio Extractor API
Extracts audio from YouTube Shorts and Instagram Reels
Optimized for n8n integration with binary data return
"""

import os
import tempfile
import asyncio
import logging
from typing import Optional
from pathlib import Path
import random

from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import yt_dlp
import aiofiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from advanced_youtube_extractor import AdvancedYouTubeExtractor
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Social Media Audio Extractor",
    description="Extract audio from YouTube Shorts and Instagram Reels",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class AudioExtractionRequest(BaseModel):
    url: HttpUrl
    format: str = "mp3"
    quality: str = "192"
    return_url: bool = False  # If True, return download URL instead of binary data

class AudioExtractionResponse(BaseModel):
    success: bool
    message: str
    filename: Optional[str] = None
    duration: Optional[float] = None
    file_size: Optional[int] = None

# yt-dlp configuration
def get_ydl_opts(output_format: str = "mp3", quality: str = "192", cookies_path: str = None) -> dict:
    """Configure yt-dlp options for audio extraction with enhanced anti-bot protection"""
    temp_dir = tempfile.gettempdir()
    
    # Randomize user agents to avoid detection
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    ]
    
    opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': output_format,
            'preferredquality': quality,
        }],
        'extractaudio': True,
        'audioformat': output_format,
        'audioquality': quality,
        'no_warnings': True,
        'quiet': True,
        'no_playlist': True,
        'writeinfojson': False,
        'writethumbnail': False,
        
        # Enhanced anti-bot protection measures
        'user_agent': random.choice(user_agents),
        'referer': 'https://www.youtube.com/',
        'origin': 'https://www.youtube.com',
        'sleep_interval': random.uniform(1, 3),  # Random delay between 1-3 seconds
        'max_sleep_interval': random.uniform(5, 10),  # Random max delay 5-10 seconds
        'sleep_interval_requests': random.uniform(0.5, 1.5),  # Delay between HTTP requests
        
        # Add more realistic browser headers
        'http_headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        },
        
        # YouTube specific optimizations
        'extractor_args': {
            'youtube': {
                'skip': ['dash', 'hls'],  # Skip complex formats
                'player_skip': ['configs'],  # Skip some player configs that might trigger bot detection
                'player_client': ['android', 'web'],  # Try multiple clients
                'comment_sort': ['top'],  # Don't load all comments
                'max_comments': [0],  # Don't load comments at all
                'include_live_chat': False,
            }
        },
        
        # Additional anti-detection measures
        'socket_timeout': 60,
        'retries': 3,
        'fragment_retries': 3,
        'file_access_retries': 3,
        'retry_sleep_functions': {
            'http': lambda n: random.uniform(1, 3) * n,
            'fragment': lambda n: random.uniform(1, 2) * n,
            'file_access': lambda n: random.uniform(0.5, 1.5) * n,
        },
    }
    
    # Add cookies with fallback to default location
    cookies_to_use = None
    
    if cookies_path and os.path.exists(cookies_path):
        cookies_to_use = cookies_path
        logger.info(f"Using provided cookies from: {cookies_path}")
    elif os.getenv('YOUTUBE_COOKIES_PATH'):
        env_cookies_path = os.getenv('YOUTUBE_COOKIES_PATH')
        logger.info(f"Environment YOUTUBE_COOKIES_PATH set to: {env_cookies_path}")
        if os.path.exists(env_cookies_path):
            cookies_to_use = env_cookies_path
            logger.info(f"Using cookies from environment: {env_cookies_path}")
        else:
            logger.error(f"Cookies file not found at environment path: {env_cookies_path}")
    else:
        # Fallback to default cookies.txt in current directory
        default_cookies_path = os.path.join(os.getcwd(), 'cookies.txt')
        if os.path.exists(default_cookies_path):
            cookies_to_use = default_cookies_path
            logger.info(f"Using default cookies from: {default_cookies_path}")
        else:
            logger.warning("No cookies file found in any location")
    
    if cookies_to_use:
        opts['cookiefile'] = cookies_to_use
        logger.info(f"Cookies configured successfully: {cookies_to_use}")
    else:
        logger.warning("No cookies available - may encounter bot detection on some videos")
        logger.info("Tip: Place cookies.txt in project directory or set YOUTUBE_COOKIES_PATH environment variable")
    
    return opts

async def extract_audio_async(url: str, output_format: str = "mp3", quality: str = "192") -> tuple[str, dict]:
    """Asynchronously extract audio using yt-dlp with advanced fallback"""
    
    def extract_audio():
        ydl_opts = get_ydl_opts(output_format, quality)
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info first
                info = ydl.extract_info(url, download=False)
                
                # Download and extract audio
                ydl.download([url])
                
                # Find the extracted audio file
                temp_dir = tempfile.gettempdir()
                title = info.get('title', 'audio')
                
                # Clean filename
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                audio_file = os.path.join(temp_dir, f"{safe_title}.{output_format}")
                
                # Sometimes yt-dlp creates files with different names
                if not os.path.exists(audio_file):
                    # Look for any audio files in temp directory created recently
                    import glob
                    pattern = os.path.join(temp_dir, f"*.{output_format}")
                    files = glob.glob(pattern)
                    if files:
                        # Get the most recent file
                        audio_file = max(files, key=os.path.getctime)
                
                return audio_file, info
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Standard audio extraction failed: {error_msg}")
            
            # Check if it's a bot detection error
            if any(keyword in error_msg.lower() for keyword in ['bot', 'sign in', 'confirm', 'not available']):
                logger.info("Bot detection in audio extraction, trying advanced method...")
                
                # For advanced extraction, we need to get the direct audio URL
                extractor = AdvancedYouTubeExtractor()
                info = extractor.extract_info(url)
                
                if info:
                    # For now, if advanced method works for info, retry standard download
                    # with the info we got (sometimes the second attempt works)
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                        
                        temp_dir = tempfile.gettempdir()
                        title = info.get('title', 'audio')
                        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                        audio_file = os.path.join(temp_dir, f"{safe_title}.{output_format}")
                        
                        if not os.path.exists(audio_file):
                            import glob
                            pattern = os.path.join(temp_dir, f"*.{output_format}")
                            files = glob.glob(pattern)
                            if files:
                                audio_file = max(files, key=os.path.getctime)
                        
                        return audio_file, info
                else:
                    raise Exception("Advanced extraction also failed")
            else:
                raise e
    
    # Run in thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, extract_audio)

def cleanup_file(filepath: str):
    """Background task to clean up temporary files"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"Cleaned up temporary file: {filepath}")
    except Exception as e:
        logger.error(f"Error cleaning up file {filepath}: {e}")

def validate_url(url: str) -> bool:
    """Validate if URL is from supported platforms"""
    supported_platforms = [
        'youtube.com/shorts/',
        'youtu.be/',
        'instagram.com/reel/',
        'instagram.com/p/',
        'instagram.com/tv/',
    ]
    
    return any(platform in url.lower() for platform in supported_platforms)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Social Media Audio Extractor",
        "status": "healthy",
        "version": "1.0.0",
        "supported_platforms": ["YouTube Shorts", "Instagram Reels"]
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "yt_dlp_version": yt_dlp.version.__version__
    }

@app.get("/files/{filename}")
async def serve_file(filename: str):
    """Serve audio files for download"""
    import os
    from fastapi.responses import FileResponse
    
    # Security: Only allow mp3, wav, m4a files
    allowed_extensions = ['.mp3', '.wav', '.m4a']
    file_ext = os.path.splitext(filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Look for file in temp directory
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="audio/mpeg"
    )

@app.post("/extract-audio")
@limiter.limit("10/minute")
async def extract_audio(
    request: Request,
    extraction_request: AudioExtractionRequest,
    background_tasks: BackgroundTasks
):
    """Extract audio from social media URL and return binary data"""
    
    url = str(extraction_request.url)
    
    # Validate URL
    if not validate_url(url):
        raise HTTPException(
            status_code=400, 
            detail="URL must be from YouTube Shorts or Instagram Reels"
        )
    
    try:
        logger.info(f"Extracting audio from: {url}")
        
        # Extract audio
        audio_file_path, info = await extract_audio_async(
            url, 
            extraction_request.format, 
            extraction_request.quality
        )
        
        if not os.path.exists(audio_file_path):
            raise HTTPException(status_code=500, detail="Audio extraction failed")
        
        # Get file info
        file_size = os.path.getsize(audio_file_path)
        duration = info.get('duration', 0)
        title = info.get('title', 'audio')
        
        logger.info(f"Successfully extracted audio: {title} ({file_size} bytes)")
        
        # Check if user wants URL instead of binary data
        if extraction_request.return_url:
            # Return download URL instead of binary data
            filename = os.path.basename(audio_file_path)
            download_url = f"/files/{filename}"
            
            # Don't schedule cleanup if returning URL
            return {
                "success": True,
                "download_url": download_url,
                "filename": filename,
                "title": title,
                "duration": duration,
                "file_size": file_size,
                "message": f"Audio extracted successfully. Download at: {download_url}"
            }
        else:
            # Read file as binary data
            async with aiofiles.open(audio_file_path, 'rb') as f:
                audio_data = await f.read()
            
            # Schedule cleanup
            background_tasks.add_task(cleanup_file, audio_file_path)
            
            # Return binary data with appropriate headers
            headers = {
                "Content-Type": "audio/mpeg",
                "Content-Disposition": f'attachment; filename="{title}.{extraction_request.format}"',
                "X-Audio-Duration": str(duration),
                "X-File-Size": str(file_size),
                "X-Original-Title": title
            }
            
            return Response(content=audio_data, headers=headers, media_type="audio/mpeg")
        
    except Exception as e:
        logger.error(f"Error extracting audio from {url}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Audio extraction failed: {str(e)}")

@app.post("/extract-audio-info")
@limiter.limit("20/minute")
async def extract_audio_info(
    request: Request,
    extraction_request: AudioExtractionRequest
):
    """Get audio info without downloading (for preview/validation)"""
    
    url = str(extraction_request.url)
    
    if not validate_url(url):
        raise HTTPException(
            status_code=400, 
            detail="URL must be from YouTube Shorts or Instagram Reels"
        )
    
    try:
        # Use the same anti-bot configuration for info extraction
        ydl_opts = get_ydl_opts()
        ydl_opts.update({
            'skip_download': True,  # Don't download for info extraction
        })
        
        def get_info():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)
        
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, get_info)
        
        return {
            "success": True,
            "title": info.get('title'),
            "duration": info.get('duration'),
            "uploader": info.get('uploader'),
            "upload_date": info.get('upload_date'),
            "view_count": info.get('view_count'),
            "platform": info.get('extractor_key'),
            "thumbnail": info.get('thumbnail')
        }
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Standard extraction failed for {url}: {error_msg}")
        
        # Check if it's a bot detection error
        if any(keyword in error_msg.lower() for keyword in ['bot', 'sign in', 'confirm', 'not available']):
            logger.info("Bot detection suspected, trying advanced extractor...")
            
            try:
                # Use advanced extractor as fallback
                def get_info_advanced():
                    extractor = AdvancedYouTubeExtractor()
                    return extractor.extract_info(url)
                
                info = await loop.run_in_executor(None, get_info_advanced)
                
                if info:
                    logger.info("Advanced extractor succeeded!")
                    return {
                        "success": True,
                        "title": info.get('title'),
                        "duration": info.get('duration'),
                        "uploader": info.get('uploader'),
                        "upload_date": info.get('upload_date'),
                        "view_count": info.get('view_count'),
                        "platform": info.get('extractor_key'),
                        "thumbnail": info.get('thumbnail'),
                        "extraction_method": "advanced_fallback"
                    }
                else:
                    logger.error("Advanced extractor also failed")
                    
            except Exception as advanced_error:
                logger.error(f"Advanced extractor failed: {advanced_error}")
        
        raise HTTPException(status_code=500, detail=f"Failed to get audio info: {error_msg}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 