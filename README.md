# Social Media Audio Extractor API

A robust FastAPI application that extracts audio from YouTube Shorts and Instagram Reels, returning MP3 files or binary data optimized for n8n integration and automation workflows.

## Features

- 🎵 Extract audio from YouTube Shorts and Instagram Reels
- 📦 Return binary data suitable for n8n nodes
- ⚡ Async processing with FastAPI
- 🔒 Rate limiting and security features
- 🐳 Docker containerization for easy deployment
- 📊 Health checks and monitoring
- 🛠️ Comprehensive error handling
- 📋 OpenAPI documentation

## Supported Platforms

- YouTube Shorts (`youtube.com/shorts/`, `youtu.be/`)
- Instagram Reels (`instagram.com/reel/`, `instagram.com/p/`, `instagram.com/tv/`)

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SocialMediaAudioExtractor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the API**
   - API: `http://localhost:8000`
   - Documentation: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

## API Endpoints

### 1. Extract Audio
**POST** `/extract-audio`

Extract audio from social media URL and return binary MP3 data.

```json
{
  "url": "https://youtube.com/shorts/EXAMPLE",
  "format": "mp3",
  "quality": "192"
}
```

**Response**: Binary MP3 data with headers:
- `Content-Type`: `audio/mpeg`
- `X-Audio-Duration`: Duration in seconds
- `X-File-Size`: File size in bytes
- `X-Original-Title`: Original video title

### 2. Extract Audio Info
**POST** `/extract-audio-info`

Get audio metadata without downloading (preview/validation).

```json
{
  "url": "https://youtube.com/shorts/EXAMPLE",
  "format": "mp3",
  "quality": "192"
}
```

**Response**:
```json
{
  "success": true,
  "title": "Video Title",
  "duration": 30.5,
  "uploader": "Channel Name",
  "upload_date": "20231201",
  "view_count": 1000000,
  "platform": "Youtube",
  "thumbnail": "https://..."
}
```

### 3. Health Check
**GET** `/health`

Check API health and yt-dlp version.

### 4. Root
**GET** `/`

Basic service information and supported platforms.

## Usage Examples

### Python
```python
import requests

# Extract audio info
response = requests.post("http://localhost:8000/extract-audio-info", json={
    "url": "https://youtube.com/shorts/EXAMPLE"
})
info = response.json()

# Extract audio binary data
response = requests.post("http://localhost:8000/extract-audio", json={
    "url": "https://youtube.com/shorts/EXAMPLE",
    "format": "mp3",
    "quality": "192"
})

# Save audio file
with open("audio.mp3", "wb") as f:
    f.write(response.content)
```

### cURL
```bash
# Get audio info
curl -X POST "http://localhost:8000/extract-audio-info" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://youtube.com/shorts/EXAMPLE"}'

# Extract audio
curl -X POST "http://localhost:8000/extract-audio" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://youtube.com/shorts/EXAMPLE"}' \
     --output audio.mp3
```

## n8n Integration

The API is optimized for n8n workflows. See `n8n_integration_guide.md` for detailed integration instructions, including:

- HTTP Request node configuration
- Binary data handling
- Sample workflows
- Error handling patterns
- Cloud storage integration

## Rate Limiting

- **Audio Extraction**: 10 requests per minute per IP
- **Audio Info**: 20 requests per minute per IP
- Rate limits can be configured via environment variables

## Configuration

### Environment Variables

```bash
# Redis (optional, for distributed rate limiting)
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO

# Rate limiting
RATE_LIMIT_ENABLED=true
EXTRACT_RATE_LIMIT=10
INFO_RATE_LIMIT=20
```

### Audio Quality Options

- **Format**: `mp3`, `m4a`, `aac`, `flac`, `wav`
- **Quality**: `96`, `128`, `192`, `256`, `320` (kbps for MP3)

## AWS Deployment

### 1. EC2 Instance
```bash
# Install Docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start

# Clone and deploy
git clone <repository-url>
cd SocialMediaAudioExtractor
sudo docker-compose up -d
```

### 2. ECS with Fargate
Use the provided `Dockerfile` with ECS task definition.

### 3. Lambda (for light usage)
The application can be adapted for AWS Lambda using Mangum.

## Security Considerations

- Rate limiting prevents abuse
- Input validation for URLs
- No persistent storage of downloaded content
- CORS enabled for web integration
- Health checks for monitoring

## Legal Compliance

⚠️ **Important**: This tool downloads content from third-party platforms. Please ensure compliance with:

- YouTube Terms of Service
- Instagram Terms of Service
- Copyright laws in your jurisdiction
- Platform-specific developer policies

**Recommendations**:
- Use only for personal or legally permitted purposes
- Obtain proper licenses for commercial use
- Respect content creators' rights
- Consider fair use doctrine limitations

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install requests

# Run tests (update test URLs first)
python test_api.py
```

Update the `TEST_URLS` in `test_api.py` with actual URLs before testing.

## Monitoring and Logging

The application provides comprehensive logging:

- Request/response logging
- Error tracking
- Performance metrics
- Health check endpoints

Logs are structured for easy parsing by monitoring tools like CloudWatch, Datadog, or ELK stack.

## Troubleshooting

### Common Issues

1. **FFmpeg not found**
   ```bash
   # Ubuntu/Debian
   sudo apt update && sudo apt install ffmpeg
   
   # macOS
   brew install ffmpeg
   ```

2. **Rate limit errors**
   - Implement delays between requests
   - Use Redis for distributed rate limiting

3. **Large file handling**
   - Monitor memory usage
   - Consider streaming for very large files

4. **Platform restrictions**
   - Some URLs may be geo-restricted
   - Private/age-restricted content may fail

### Debug Mode

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python main.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is provided as-is for educational and personal use. Users are responsible for ensuring compliance with all applicable laws and terms of service.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Test with the provided test script
4. Open an issue with detailed error information

---

**Note**: Always ensure you have the right to download and process audio content from the provided URLs. 