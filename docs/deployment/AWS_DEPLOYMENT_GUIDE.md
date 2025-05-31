# AWS Deployment Guide for YouTube Audio Extractor 🚀

## 🎯 Overview

This guide covers deploying the enhanced YouTube Audio Extractor to AWS for n8n integration.

## 📋 Prerequisites

- AWS EC2 instance (Ubuntu 20.04+ recommended)
- Docker and Docker Compose installed
- Domain name or public IP
- SSL certificate (optional but recommended)

## 🔧 AWS EC2 Setup

### 1. Launch EC2 Instance

**Recommended specs:**
- Instance type: `t3.medium` or larger
- Storage: 20GB+ SSD
- Security Group: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS), 8000 (API)

### 2. Connect and Install Dependencies

```bash
# Connect to your EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again for docker group to take effect
exit
```

## 📁 Project Deployment

### 1. Upload Project Files

```bash
# Create project directory
mkdir ~/youtube-audio-extractor
cd ~/youtube-audio-extractor

# Upload your files (use scp, git, or any method you prefer)
# You need to upload:
# - main.py
# - advanced_youtube_extractor.py
# - refresh_cookies.py
# - requirements.txt
# - Dockerfile
# - docker-compose.yml
# - cookies.txt (after generating)
```

### 2. Create Production Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  youtube-audio-extractor:
    build: .
    container_name: youtube-audio-extractor
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - ./cookies.txt:/app/cookies.txt:ro
      - ./logs:/app/logs
      - /tmp:/tmp  # Shared temp directory for audio files
    environment:
      - YOUTUBE_COOKIES_PATH=/app/cookies.txt
      - PYTHONUNBUFFERED=1
      - LOG_LEVEL=INFO
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Nginx reverse proxy
  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro  # If using SSL
    depends_on:
      - youtube-audio-extractor
    profiles:
      - proxy  # Use: docker-compose --profile proxy up
```

### 3. Create Production Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY advanced_youtube_extractor.py .
COPY refresh_cookies.py .

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### 4. Enhanced Requirements for Production

```txt
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
yt-dlp==2024.8.6
aiofiles==23.2.1
pydantic==2.5.0
slowapi==0.1.9
redis==5.0.1  # For caching if needed
requests==2.31.0
```

## 🍪 Cookie Setup on AWS

### 1. Generate Cookies on AWS

```bash
# On your AWS instance
cd ~/youtube-audio-extractor

# Install yt-dlp first
pip3 install yt-dlp

# Run the cookie refresh script
python3 refresh_cookies.py
```

### 2. Manual Cookie Transfer (if needed)

```bash
# From your local machine, upload cookies to AWS
scp -i your-key.pem cookies.txt ubuntu@your-ec2-ip:~/youtube-audio-extractor/

# Or create cookies directly on AWS using browser extension method
# See ENHANCED_BOT_PROTECTION_GUIDE.md for manual methods
```

## 🚀 Deploy the Application

```bash
# Navigate to project directory
cd ~/youtube-audio-extractor

# Build and start the application
docker-compose -f docker-compose.prod.yml up -d --build

# Check logs
docker-compose -f docker-compose.prod.yml logs -f

# Test the deployment
curl http://localhost:8000/health
```

## 🌐 Configure Public Access

### Option 1: Direct Access (Simple)

```bash
# Make sure port 8000 is open in security group
# Access via: http://your-ec2-ip:8000
```

### Option 2: Nginx Reverse Proxy (Recommended)

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream youtube_api {
        server youtube-audio-extractor:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;  # Replace with your domain

        client_max_body_size 100M;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;

        location / {
            proxy_pass http://youtube_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

```bash
# Deploy with Nginx
docker-compose -f docker-compose.prod.yml --profile proxy up -d --build
```

## 📊 n8n Integration Configurations

### 1. HTTP Node Configuration for Info Extraction

```json
{
  "httpVersion": "v2",
  "method": "POST",
  "url": "http://your-ec2-ip:8000/extract-audio-info",
  "authentication": "none",
  "requestFormat": "json",
  "jsonParameters": true,
  "options": {
    "timeout": 30000,
    "redirect": {
      "redirect": {
        "followRedirects": true,
        "maxRedirects": 5
      }
    }
  },
  "parametersJson": {
    "url": "{{ $json.youtube_url }}",
    "format": "mp3",
    "quality": "192"
  }
}
```

### 2. HTTP Node Configuration for Audio Download (Binary)

```json
{
  "httpVersion": "v2",
  "method": "POST",
  "url": "http://your-ec2-ip:8000/extract-audio",
  "authentication": "none",
  "requestFormat": "json",
  "responseFormat": "file",
  "jsonParameters": true,
  "options": {
    "timeout": 120000,
    "redirect": {
      "redirect": {
        "followRedirects": true,
        "maxRedirects": 5
      }
    }
  },
  "parametersJson": {
    "url": "{{ $json.youtube_url }}",
    "format": "mp3",
    "quality": "192",
    "return_url": false
  }
}
```

### 3. HTTP Node Configuration for Audio Download (URL)

```json
{
  "httpVersion": "v2",
  "method": "POST",
  "url": "http://your-ec2-ip:8000/extract-audio",
  "authentication": "none",
  "requestFormat": "json",
  "jsonParameters": true,
  "options": {
    "timeout": 120000
  },
  "parametersJson": {
    "url": "{{ $json.youtube_url }}",
    "format": "mp3",
    "quality": "192",
    "return_url": true
  }
}
```

## 🔧 n8n Workflow Examples

### Example 1: Simple Audio Extraction

```json
{
  "name": "YouTube Audio Extractor",
  "nodes": [
    {
      "parameters": {
        "httpVersion": "v2",
        "method": "POST",
        "url": "http://your-ec2-ip:8000/extract-audio",
        "requestFormat": "json",
        "responseFormat": "file",
        "jsonParameters": true,
        "parametersJson": {
          "url": "https://www.youtube.com/shorts/N8tJFeMXrr8",
          "format": "mp3",
          "quality": "192"
        },
        "options": {
          "timeout": 120000
        }
      },
      "name": "Extract YouTube Audio",
      "type": "n8n-nodes-base.httpRequest",
      "position": [860, 240]
    }
  ]
}
```

### Example 2: Workflow with Error Handling

```json
{
  "name": "YouTube Audio with Error Handling",
  "nodes": [
    {
      "parameters": {
        "httpVersion": "v2",
        "method": "POST",
        "url": "http://your-ec2-ip:8000/extract-audio-info",
        "requestFormat": "json",
        "jsonParameters": true,
        "parametersJson": {
          "url": "{{ $json.youtube_url }}"
        }
      },
      "name": "Get Video Info",
      "type": "n8n-nodes-base.httpRequest"
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "{{ $json.success }}",
              "value2": "true"
            }
          ]
        }
      },
      "name": "Check Success",
      "type": "n8n-nodes-base.if"
    },
    {
      "parameters": {
        "httpVersion": "v2",
        "method": "POST",
        "url": "http://your-ec2-ip:8000/extract-audio",
        "requestFormat": "json",
        "responseFormat": "file",
        "jsonParameters": true,
        "parametersJson": {
          "url": "{{ $json.youtube_url }}",
          "format": "mp3",
          "quality": "192"
        }
      },
      "name": "Extract Audio",
      "type": "n8n-nodes-base.httpRequest"
    }
  ]
}
```

## 🚨 Monitoring and Troubleshooting

### 1. Monitor Application

```bash
# Check container status
docker ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f youtube-audio-extractor

# Check resource usage
docker stats

# Test endpoints
curl http://your-ec2-ip:8000/health
curl -X POST http://your-ec2-ip:8000/extract-audio-info \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/shorts/dQw4w9WgXcQ"}'
```

### 2. Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Connection timeout in n8n | Increase timeout in HTTP node |
| Large file handling | Use `return_url: true` for large files |
| Rate limiting | Implement delays between requests |
| Bot detection | Refresh cookies with `python3 refresh_cookies.py` |
| Out of disk space | Clean temp files: `docker exec container_name find /tmp -name "*.mp3" -delete` |

### 3. Automated Cookie Refresh

```bash
# Create cron job to refresh cookies weekly
crontab -e

# Add this line (runs every Sunday at 2 AM)
0 2 * * 0 cd /home/ubuntu/youtube-audio-extractor && python3 refresh_cookies.py && docker-compose -f docker-compose.prod.yml restart youtube-audio-extractor
```

## 🔒 Security Considerations

1. **Firewall Configuration**:
   ```bash
   # Only allow necessary ports
   sudo ufw allow 22    # SSH
   sudo ufw allow 80    # HTTP
   sudo ufw allow 443   # HTTPS
   sudo ufw allow 8000  # API (if not using proxy)
   sudo ufw enable
   ```

2. **Environment Variables**:
   ```bash
   # Set secure environment variables
   echo "YOUTUBE_COOKIES_PATH=/app/cookies.txt" > .env
   echo "LOG_LEVEL=INFO" >> .env
   ```

3. **SSL Certificate** (if using domain):
   ```bash
   # Use Let's Encrypt
   sudo apt install certbot
   sudo certbot certonly --standalone -d your-domain.com
   ```

## 📈 Performance Optimization

1. **Increase worker processes** for high volume:
   ```yaml
   # In docker-compose.prod.yml
   command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
   ```

2. **Add Redis caching** (optional):
   ```yaml
   redis:
     image: redis:alpine
     restart: unless-stopped
   ```

3. **Monitor disk usage**:
   ```bash
   # Auto-cleanup script
   echo "0 */6 * * * find /tmp -name '*.mp3' -mtime +1 -delete" | crontab -
   ```

---

**Your API Endpoints:**
- Health Check: `http://your-ec2-ip:8000/health`
- Info Extraction: `http://your-ec2-ip:8000/extract-audio-info`
- Audio Extraction: `http://your-ec2-ip:8000/extract-audio`

**For n8n HTTP Node:**
- URL: `http://your-ec2-ip:8000/extract-audio`
- Method: POST
- Response Format: File (for binary) or JSON (for URL)
- Timeout: 120000ms (2 minutes) 