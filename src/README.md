# Source Code 💻

This directory contains the main application source code.

## 📁 Files

### 🎯 [main.py](main.py)
**Purpose:** Main FastAPI application entry point

**Features:**
- FastAPI server setup with CORS and rate limiting
- Audio extraction endpoints (`/extract-audio`, `/extract-audio-info`)
- Health check endpoint (`/health`)
- File serving endpoint (`/files/{filename}`)
- Comprehensive error handling and logging

**Key Components:**
- `AudioExtractionRequest` - Pydantic model for request validation
- `get_ydl_opts()` - yt-dlp configuration with anti-bot measures
- Rate limiting: 10 extractions/minute, 20 info requests/minute

### 🛡️ [advanced_youtube_extractor.py](advanced_youtube_extractor.py)
**Purpose:** Advanced YouTube extraction with multiple fallback strategies

**Features:**
- Multiple client simulation (Android, iOS, TV, Web)
- Randomized user agents and headers
- Proxy rotation support
- Comprehensive error handling
- Fallback extraction methods

**Key Components:**
- `AdvancedYouTubeExtractor` class
- Multiple extraction strategies for bot detection bypass
- Smart retry logic with exponential backoff

### 📦 [requirements.txt](requirements.txt)
**Purpose:** Python dependencies for the application

**Key Dependencies:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `yt-dlp` - YouTube video/audio extraction
- `aiofiles` - Async file operations
- `slowapi` - Rate limiting
- `requests` - HTTP client

### 🐳 [Dockerfile](Dockerfile)
**Purpose:** Container configuration for deployment

**Features:**
- Python 3.11 slim base image
- FFmpeg installation for audio processing
- Health checks for monitoring
- Multi-worker configuration for production

## 🚀 Running the Application

### Local Development
```bash
cd src
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production
```bash
cd src
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
```

### Docker
```bash
# From project root
docker build -t youtube-audio-extractor ./src
docker run -p 8000:8000 -v ./cookies.txt:/app/cookies.txt:ro youtube-audio-extractor
```

## 🔧 Configuration

### Environment Variables
- `YOUTUBE_COOKIES_PATH` - Path to cookies file (default: `cookies.txt`)
- `LOG_LEVEL` - Logging level (default: `INFO`)
- `PYTHONUNBUFFERED` - Disable Python output buffering

### yt-dlp Configuration
The application automatically configures yt-dlp with:
- Enhanced user agent rotation
- Multiple client types (Android, iOS, TV, Web)
- Cookie-based authentication
- Anti-bot detection measures
- Format selection for optimal quality

## 📊 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Service information |
| `/health` | GET | Health check |
| `/extract-audio-info` | POST | Get video metadata |
| `/extract-audio` | POST | Extract audio file |
| `/files/{filename}` | GET | Serve audio files |

## 🛡️ Security Features

- **Input Validation**: URL format validation using Pydantic
- **Rate Limiting**: Per-IP rate limits to prevent abuse
- **Error Sanitization**: Safe error messages without sensitive data
- **File Type Validation**: Only approved audio formats served
- **CORS Configuration**: Controlled cross-origin access

## 🔍 Logging

The application provides structured logging:
- Request/response logging with timing
- Error tracking with stack traces
- yt-dlp operation logging
- Health check status logging

**Log Levels:**
- `DEBUG` - Detailed operation logs
- `INFO` - General information (default)
- `WARNING` - Non-critical issues
- `ERROR` - Application errors

## 🚨 Error Handling

### Common Error Types
- **Bot Detection**: Handled by advanced extractor fallbacks
- **Invalid URLs**: Validated before processing
- **Rate Limiting**: Graceful rejection with retry headers
- **File Not Found**: 404 responses for missing files
- **Processing Errors**: Detailed error messages for debugging

### Monitoring
- Health endpoint for uptime monitoring
- Structured logs for error tracking
- Request timing for performance monitoring

## 🔄 Development Workflow

### Adding New Features
1. Update `main.py` for new endpoints
2. Add corresponding logic to extractors
3. Update `requirements.txt` if needed
4. Add tests in `../scripts/testing/`
5. Update documentation in `../docs/`

### Code Style
- Follow PEP 8 style guidelines
- Use type hints for better code clarity
- Add docstrings for functions and classes
- Handle errors gracefully with appropriate logging

---

**API Documentation:** See [../docs/api/API_REFERENCE.md](../docs/api/API_REFERENCE.md)
**Deployment Guide:** See [../docs/deployment/AWS_DEPLOYMENT_GUIDE.md](../docs/deployment/AWS_DEPLOYMENT_GUIDE.md) 