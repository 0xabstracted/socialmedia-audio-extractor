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

from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import yt_dlp
import aiofiles
from slowapi import Limiter, _rate_limit_exceeded_handler
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

class AudioExtractionResponse(BaseModel):
    success: bool
    message: str
    filename: Optional[str] = None
    duration: Optional[float] = None
    file_size: Optional[int] = None

# yt-dlp configuration
def get_ydl_opts(output_format: str = "mp3", quality: str = "192") -> dict:
    """Configure yt-dlp options for audio extraction"""
    temp_dir = tempfile.gettempdir()
    
    return {
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
    }

async def extract_audio_async(url: str, output_format: str = "mp3", quality: str = "192") -> tuple[str, dict]:
    """Asynchronously extract audio using yt-dlp"""
    
    def extract_audio():
        ydl_opts = get_ydl_opts(output_format, quality)
        
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
        
        # Read file as binary data
        async with aiofiles.open(audio_file_path, 'rb') as f:
            audio_data = await f.read()
        
        # Get file info
        file_size = len(audio_data)
        duration = info.get('duration', 0)
        title = info.get('title', 'audio')
        
        # Schedule cleanup
        background_tasks.add_task(cleanup_file, audio_file_path)
        
        logger.info(f"Successfully extracted audio: {title} ({file_size} bytes)")
        
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
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'no_playlist': True,
        }
        
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
        logger.error(f"Error getting info for {url}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get audio info: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 