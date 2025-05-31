# API Reference 📡

## Base URL

```
http://your-server:8000
```

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check API health status and dependencies.

**Response:**
```json
{
  "status": "healthy",
  "yt_dlp_version": "2024.8.6"
}
```

**Status Codes:**
- `200` - Service is healthy
- `503` - Service unavailable

---

### 2. Root Information

**Endpoint:** `GET /`

**Description:** Get basic service information and supported platforms.

**Response:**
```json
{
  "service": "Social Media Audio Extractor",
  "status": "healthy",
  "version": "1.0.0",
  "supported_platforms": ["YouTube Shorts", "Instagram Reels"]
}
```

---

### 3. Extract Audio Info

**Endpoint:** `POST /extract-audio-info`

**Description:** Get video metadata without downloading the audio file.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/shorts/dQw4w9WgXcQ",
  "format": "mp3",
  "quality": "192"
}
```

**Parameters:**
- `url` (string, required) - YouTube Shorts URL
- `format` (string, optional) - Audio format (default: "mp3")
- `quality` (string, optional) - Audio quality (default: "192")

**Response (Success):**
```json
{
  "success": true,
  "title": "Rick Astley - Never Gonna Give You Up",
  "duration": 30.5,
  "uploader": "Rick Astley",
  "upload_date": "20231201",
  "view_count": 1000000,
  "platform": "Youtube",
  "thumbnail": "https://...",
  "extraction_method": "standard"
}
```

**Response (Error):**
```json
{
  "detail": "Failed to get audio info: ERROR: [youtube] N8tJFeMXrr8: Sign in to confirm you're not a bot"
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid URL format
- `429` - Rate limit exceeded (20/minute)
- `500` - Extraction failed

---

### 4. Extract Audio

**Endpoint:** `POST /extract-audio`

**Description:** Extract audio from video and return binary data or download URL.

**Request Body (Binary Response):**
```json
{
  "url": "https://www.youtube.com/shorts/dQw4w9WgXcQ",
  "format": "mp3",
  "quality": "192",
  "return_url": false
}
```

**Request Body (URL Response):**
```json
{
  "url": "https://www.youtube.com/shorts/dQw4w9WgXcQ",
  "format": "mp3",
  "quality": "192",
  "return_url": true
}
```

**Parameters:**
- `url` (string, required) - YouTube Shorts URL
- `format` (string, optional) - Audio format: "mp3", "wav", "m4a" (default: "mp3")
- `quality` (string, optional) - Audio quality: "64", "128", "192", "256", "320" (default: "192")
- `return_url` (boolean, optional) - If true, returns download URL instead of binary (default: false)

**Response (Binary):**
- **Content-Type:** `audio/mpeg`
- **Headers:**
  - `X-Audio-Duration`: Duration in seconds
  - `X-File-Size`: File size in bytes
  - `X-Original-Title`: Original video title
- **Body:** Binary MP3 data

**Response (URL):**
```json
{
  "success": true,
  "download_url": "/files/Rick_Astley_Never_Gonna_Give_You_Up.mp3",
  "filename": "Rick_Astley_Never_Gonna_Give_You_Up.mp3",
  "title": "Rick Astley - Never Gonna Give You Up",
  "duration": 30.5,
  "file_size": 491520,
  "message": "Audio extracted successfully. Download at: /files/Rick_Astley_Never_Gonna_Give_You_Up.mp3"
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid URL format
- `429` - Rate limit exceeded (10/minute)
- `500` - Extraction failed

---

### 5. Serve Files

**Endpoint:** `GET /files/{filename}`

**Description:** Download extracted audio files.

**Parameters:**
- `filename` (string, required) - Filename returned from extract-audio with return_url=true

**Response:**
- **Content-Type:** `audio/mpeg`, `audio/wav`, or `audio/mp4`
- **Body:** Binary audio file

**Status Codes:**
- `200` - File found and served
- `400` - Invalid file type
- `404` - File not found

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| `/extract-audio` | 10 requests/minute per IP |
| `/extract-audio-info` | 20 requests/minute per IP |
| All other endpoints | No limit |

## Supported URLs

### YouTube Shorts
- `https://youtube.com/shorts/{video_id}`
- `https://www.youtube.com/shorts/{video_id}`
- `https://youtu.be/{video_id}`

### URL Validation
URLs must contain one of the following patterns:
- `youtube.com/shorts/`
- `youtu.be/`

## Audio Formats

| Format | Extension | MIME Type |
|--------|-----------|-----------|
| MP3 | .mp3 | audio/mpeg |
| WAV | .wav | audio/wav |
| M4A | .m4a | audio/mp4 |

## Quality Options

| Quality | Bitrate | File Size (approx.) |
|---------|---------|-------------------|
| 64 | 64 kbps | ~240 KB/minute |
| 128 | 128 kbps | ~480 KB/minute |
| 192 | 192 kbps | ~720 KB/minute |
| 256 | 256 kbps | ~960 KB/minute |
| 320 | 320 kbps | ~1.2 MB/minute |

## Error Handling

### Common Error Types

#### Bot Detection
```json
{
  "detail": "Failed to get audio info: ERROR: [youtube] ID: Sign in to confirm you're not a bot"
}
```
**Solution:** Refresh cookies using `scripts/cookies/refresh_cookies.py`

#### Invalid URL
```json
{
  "detail": "URL must be from YouTube Shorts or Instagram Reels"
}
```
**Solution:** Ensure URL matches supported patterns

#### Rate Limit
```json
{
  "detail": "Rate limit exceeded: 10 per 1 minute"
}
```
**Solution:** Wait before making another request

#### Video Unavailable
```json
{
  "detail": "Audio extraction failed: ERROR: [youtube] ID: Video unavailable"
}
```
**Solution:** Check if video is private, deleted, or geo-restricted

## Headers

### Request Headers
```http
Content-Type: application/json
Accept: application/json, audio/mpeg
```

### Response Headers (Binary)
```http
Content-Type: audio/mpeg
Content-Disposition: attachment; filename="title.mp3"
X-Audio-Duration: 30.5
X-File-Size: 491520
X-Original-Title: Video Title
```

## Examples

### cURL Examples

#### Get Video Info
```bash
curl -X POST "http://localhost:8000/extract-audio-info" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/shorts/dQw4w9WgXcQ",
    "format": "mp3",
    "quality": "192"
  }'
```

#### Extract Audio (Binary)
```bash
curl -X POST "http://localhost:8000/extract-audio" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/shorts/dQw4w9WgXcQ",
    "format": "mp3",
    "quality": "192",
    "return_url": false
  }' \
  --output audio.mp3
```

#### Extract Audio (URL)
```bash
curl -X POST "http://localhost:8000/extract-audio" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/shorts/dQw4w9WgXcQ",
    "format": "mp3",
    "quality": "192",
    "return_url": true
  }'
```

### Python Examples

```python
import requests

# Base URL
API_BASE = "http://localhost:8000"

# Get video info
info_response = requests.post(f"{API_BASE}/extract-audio-info", json={
    "url": "https://www.youtube.com/shorts/dQw4w9WgXcQ"
})
print(info_response.json())

# Extract audio (binary)
audio_response = requests.post(f"{API_BASE}/extract-audio", json={
    "url": "https://www.youtube.com/shorts/dQw4w9WgXcQ",
    "format": "mp3",
    "quality": "192",
    "return_url": False
})

# Save audio file
with open("audio.mp3", "wb") as f:
    f.write(audio_response.content)

# Extract audio (URL)
url_response = requests.post(f"{API_BASE}/extract-audio", json={
    "url": "https://www.youtube.com/shorts/dQw4w9WgXcQ",
    "return_url": True
})
download_url = url_response.json()["download_url"]

# Download from URL
file_response = requests.get(f"{API_BASE}{download_url}")
with open("audio.mp3", "wb") as f:
    f.write(file_response.content)
```

## OpenAPI Documentation

Interactive API documentation is available at:
- **Swagger UI:** `http://your-server:8000/docs`
- **ReDoc:** `http://your-server:8000/redoc`

## Status Monitoring

Monitor API health and performance:
- **Health Check:** `GET /health`
- **Application Logs:** Available via Docker logs
- **Metrics:** Built-in request/response timing and error tracking 