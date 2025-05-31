# YouTube Audio Extractor 🎵

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A professional-grade API service for extracting audio from YouTube Shorts with advanced bot detection bypass capabilities. Built for seamless integration with n8n workflows and enterprise automation systems.

## 🚀 Features

- ✅ **YouTube Shorts Support** - Extract audio from YouTube Shorts URLs
- 🛡️ **Advanced Bot Detection Bypass** - Multi-strategy approach to avoid YouTube restrictions
- 🔄 **Multiple Client Simulation** - Android, iOS, TV, and Web client modes
- 🍪 **Smart Cookie Management** - Automated cookie refresh and validation
- 📡 **n8n Integration Ready** - Optimized for workflow automation
- 🐳 **Docker Deployment** - Production-ready containerization
- ⚡ **High Performance** - Async processing with rate limiting
- 🔒 **Security Focused** - Built-in security measures and monitoring

## 📁 Project Structure

```
📦 YouTube Audio Extractor
├── 📂 src/                          # Source Code
│   ├── main.py                      # FastAPI application
│   ├── advanced_youtube_extractor.py # Advanced extraction logic
│   └── requirements.txt             # Python dependencies
├── 📂 scripts/                      # Utility Scripts
│   ├── 📂 deployment/
│   │   └── deploy_to_aws.sh        # AWS deployment automation
│   ├── 📂 cookies/
│   │   └── refresh_cookies.py      # Cookie management
│   ├── 📂 testing/
│   │   ├── test_enhanced_api.py    # API testing
│   │   └── debug_cookies.py        # Cookie debugging
│   └── 📂 utils/                   # Additional utilities
├── 📂 docs/                        # Documentation
│   ├── 📂 deployment/
│   │   └── AWS_DEPLOYMENT_GUIDE.md # AWS deployment guide
│   ├── 📂 integration/
│   │   ├── N8N_INTEGRATION_GUIDE.md # n8n setup guide
│   │   └── 📂 templates/
│   │       └── n8n_workflow_template.json
│   ├── 📂 guides/
│   │   ├── ENHANCED_BOT_PROTECTION_GUIDE.md
│   │   └── YOUTUBE_COOKIES_GUIDE.md
│   └── 📂 api/                     # API documentation
└── README.md                       # This file
```

## 🎯 Quick Start

### Option 1: AWS Deployment (Recommended)

```bash
# 1. Upload project to your AWS EC2 instance
scp -r . ubuntu@your-ec2-ip:~/youtube-audio-extractor/

# 2. Run the automated deployment script
ssh ubuntu@your-ec2-ip
cd ~/youtube-audio-extractor
chmod +x scripts/deployment/deploy_to_aws.sh
./scripts/deployment/deploy_to_aws.sh
```

### Option 2: Local Development

```bash
# 1. Clone and setup
git clone <repository-url>
cd youtube-audio-extractor

# 2. Install dependencies
cd src
pip install -r requirements.txt

# 3. Setup cookies (required for bot detection bypass)
cd ../scripts/cookies
python refresh_cookies.py

# 4. Run the application
cd ../../src
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📊 API Endpoints

Once deployed, your API provides these endpoints:

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/health` | GET | Health check | JSON status |
| `/extract-audio-info` | POST | Get video metadata | JSON info |
| `/extract-audio` | POST | Extract audio file | Binary MP3 or JSON URL |

### Example Usage

```bash
# Check API health
curl http://your-server:8000/health

# Get video information
curl -X POST http://your-server:8000/extract-audio-info \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/shorts/dQw4w9WgXcQ"}'

# Extract audio (binary format)
curl -X POST http://your-server:8000/extract-audio \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/shorts/dQw4w9WgXcQ", "return_url": false}' \
  --output audio.mp3
```

## 🔧 n8n Integration

Perfect for workflow automation! Configure your n8n HTTP node:

**Settings:**
- **URL:** `http://your-server:8000/extract-audio`
- **Method:** `POST`
- **Response Format:** `File` (for binary) or `JSON` (for URL)
- **Timeout:** `120000ms`

**Body:**
```json
{
  "url": "{{ $json.youtube_url }}",
  "format": "mp3",
  "quality": "192",
  "return_url": false
}
```

**Result:** MP3 audio file available as `$binary.data` in your workflow.

## 📚 Documentation

- **🚀 [AWS Deployment Guide](docs/deployment/AWS_DEPLOYMENT_GUIDE.md)** - Complete AWS setup
- **🔗 [n8n Integration Guide](docs/integration/N8N_INTEGRATION_GUIDE.md)** - Workflow setup
- **🛡️ [Bot Protection Guide](docs/guides/ENHANCED_BOT_PROTECTION_GUIDE.md)** - Advanced bypass techniques
- **🍪 [Cookie Setup Guide](docs/guides/YOUTUBE_COOKIES_GUIDE.md)** - Cookie management

## 🛠️ Scripts

- **`scripts/deployment/deploy_to_aws.sh`** - Automated AWS deployment
- **`scripts/cookies/refresh_cookies.py`** - Cookie refresh and validation
- **`scripts/testing/test_enhanced_api.py`** - API testing suite
- **`scripts/testing/debug_cookies.py`** - Cookie debugging tools

## 🔒 Security Features

- **Rate Limiting:** 10 extractions/minute, 20 info requests/minute
- **Input Validation:** URL validation and sanitization
- **Cookie Security:** Secure cookie storage and rotation
- **Error Handling:** Comprehensive error responses
- **Health Monitoring:** Built-in health checks

## 🐳 Docker Support

```yaml
# docker-compose.yml example
version: '3.8'
services:
  youtube-audio-extractor:
    build: ./src
    ports:
      - "8000:8000"
    volumes:
      - ./cookies.txt:/app/cookies.txt:ro
    environment:
      - YOUTUBE_COOKIES_PATH=/app/cookies.txt
```

## 🚨 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Bot detection errors | Run `scripts/cookies/refresh_cookies.py` |
| Connection timeouts | Check firewall settings (port 8000) |
| Empty responses | Verify cookies and check logs |
| Rate limiting | Implement delays between requests |

### Getting Help

1. **Check Logs:** `docker logs youtube-audio-extractor`
2. **Test API:** Use `scripts/testing/test_enhanced_api.py`
3. **Debug Cookies:** Run `scripts/testing/debug_cookies.py`
4. **Documentation:** See `docs/` folder for detailed guides

## 📈 Performance

- **Extraction Time:** 5-15 seconds per video
- **Success Rate:** 90%+ with fresh cookies
- **Supported Formats:** MP3, WAV, M4A
- **Quality Options:** 64k, 128k, 192k, 256k, 320k

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Please respect YouTube's Terms of Service and copyright laws. Always ensure you have permission to download content.

---

**🎉 Ready to get started?** Check out the [AWS Deployment Guide](docs/deployment/AWS_DEPLOYMENT_GUIDE.md) for step-by-step setup instructions! 