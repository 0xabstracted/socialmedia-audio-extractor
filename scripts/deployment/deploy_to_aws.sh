#!/bin/bash

# YouTube Audio Extractor - AWS Deployment Script
# Run this script on your AWS EC2 instance

set -e

echo "🚀 YouTube Audio Extractor - AWS Deployment"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    print_error "This script should not be run as root"
    exit 1
fi

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker if not already installed
if ! command -v docker &> /dev/null; then
    print_status "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    print_success "Docker installed successfully"
else
    print_success "Docker already installed"
fi

# Install Docker Compose if not already installed
if ! command -v docker-compose &> /dev/null; then
    print_status "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    print_success "Docker Compose installed successfully"
else
    print_success "Docker Compose already installed"
fi

# Create project directory
PROJECT_DIR="$HOME/youtube-audio-extractor"
print_status "Creating project directory: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Create production Docker Compose file
print_status "Creating production Docker Compose configuration..."
cat > docker-compose.prod.yml << 'EOF'
version: '3.8'

services:
  youtube-audio-extractor:
    build: .
    container_name: youtube-audio-extractor
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - ./cookies.txt:/app/cookies.txt:rw
      - ./logs:/app/logs
      - /tmp:/tmp
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
EOF

# Create production Dockerfile
print_status "Creating production Dockerfile..."
cat > Dockerfile << 'EOF'
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

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
EOF

# Create enhanced requirements.txt
print_status "Creating requirements.txt..."
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
yt-dlp==2024.8.6
aiofiles==23.2.1
pydantic==2.5.0
slowapi==0.1.9
requests==2.31.0
EOF

# Create logs directory
mkdir -p logs

print_success "Configuration files created successfully!"

# Check if main application files exist
if [[ ! -f "src/main.py" ]]; then
    print_warning "src/main.py not found in current directory"
    print_status "Please upload your application files to: $PROJECT_DIR"
    echo "Required files:"
    echo "  - src/main.py"
    echo "  - src/advanced_youtube_extractor.py"
    echo "  - scripts/cookies/refresh_cookies.py"
    echo ""
    echo "You can upload the entire project using:"
    echo "scp -r . ubuntu@your-ec2-ip:$PROJECT_DIR/"
fi

# Cookie setup
print_status "Setting up cookies..."
if [[ ! -f "cookies.txt" ]]; then
    print_warning "cookies.txt not found"
    
    # Try to install yt-dlp for cookie extraction
    if ! command -v yt-dlp &> /dev/null; then
        print_status "Installing yt-dlp for cookie extraction..."
        pip3 install yt-dlp
    fi
    
    print_status "Attempting to extract cookies from Chrome..."
    if python3 -c "import sys; sys.path.append('scripts/cookies'); from refresh_cookies import extract_cookies_chrome; extract_cookies_chrome()" 2>/dev/null; then
        print_success "Cookies extracted successfully!"
    else
        print_warning "Automatic cookie extraction failed"
        print_status "Please manually create cookies.txt or run: python3 scripts/cookies/refresh_cookies.py"
        print_status "See docs/guides/ENHANCED_BOT_PROTECTION_GUIDE.md for manual cookie setup"
    fi
else
    print_success "cookies.txt already exists"
fi

# Configure firewall
print_status "Configuring firewall..."
if command -v ufw &> /dev/null; then
    sudo ufw allow 22    # SSH
    sudo ufw allow 80    # HTTP
    sudo ufw allow 443   # HTTPS
    sudo ufw allow 8000  # API
    sudo ufw --force enable
    print_success "Firewall configured"
else
    print_warning "UFW not available, please configure security group manually"
fi

# Check if we need to reload Docker group
if ! groups | grep -q docker; then
    print_warning "User not in docker group. Please logout and login again, then run:"
    echo "cd $PROJECT_DIR && docker-compose -f docker-compose.prod.yml up -d --build"
    exit 0
fi

# Ask user if they want to deploy now
echo ""
echo "🎯 Ready to deploy!"
echo "Current directory: $(pwd)"
echo "Files needed:"
echo "  - src/main.py $(test -f src/main.py && echo '✅' || echo '❌')"
echo "  - src/advanced_youtube_extractor.py $(test -f src/advanced_youtube_extractor.py && echo '✅' || echo '❌')"
echo "  - scripts/cookies/refresh_cookies.py $(test -f scripts/cookies/refresh_cookies.py && echo '✅' || echo '❌')"
echo "  - cookies.txt $(test -f cookies.txt && echo '✅' || echo '❌')"
echo ""

read -p "Do you want to build and start the application now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Building and starting the application..."
    
    # Build and start
    docker-compose -f docker-compose.prod.yml up -d --build
    
    # Wait a moment for the service to start
    sleep 10
    
    # Test the deployment
    print_status "Testing the deployment..."
    if curl -f http://localhost:8000/health &> /dev/null; then
        print_success "✅ Application is running successfully!"
        
        # Get the public IP
        PUBLIC_IP=$(curl -s http://checkip.amazonaws.com/ || echo "your-ec2-ip")
        
        echo ""
        echo "🎉 Deployment Complete!"
        echo "================================"
        echo "API Base URL: http://$PUBLIC_IP:8000"
        echo ""
        echo "Available endpoints:"
        echo "  - Health: http://$PUBLIC_IP:8000/health"
        echo "  - Info: http://$PUBLIC_IP:8000/extract-audio-info"
        echo "  - Audio: http://$PUBLIC_IP:8000/extract-audio"
        echo ""
        echo "For n8n HTTP node configuration:"
        echo "  - URL: http://$PUBLIC_IP:8000/extract-audio"
        echo "  - Method: POST"
        echo "  - Response Format: File (for binary) or JSON (for URL)"
        echo "  - Timeout: 120000ms"
        echo ""
        echo "Test with:"
        echo "curl -X POST http://$PUBLIC_IP:8000/extract-audio-info \\"
        echo "  -H 'Content-Type: application/json' \\"
        echo "  -d '{\"url\": \"https://www.youtube.com/shorts/dQw4w9WgXcQ\"}'"
        
    else
        print_error "❌ Application failed to start"
        echo "Check logs with: docker-compose -f docker-compose.prod.yml logs -f"
    fi
else
    echo ""
    echo "To start the application later, run:"
    echo "cd $PROJECT_DIR"
    echo "docker-compose -f docker-compose.prod.yml up -d --build"
fi

echo ""
echo "📚 Documentation:"
echo "  - AWS Deployment Guide: docs/deployment/AWS_DEPLOYMENT_GUIDE.md"
echo "  - Bot Protection Guide: docs/guides/ENHANCED_BOT_PROTECTION_GUIDE.md"
echo "  - n8n Integration Guide: docs/integration/N8N_INTEGRATION_GUIDE.md"
echo "  - n8n Workflow Template: docs/integration/templates/n8n_workflow_template.json"

print_success "Deployment script completed!" 