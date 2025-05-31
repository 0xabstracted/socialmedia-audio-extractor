# Enhanced Bot Protection Guide 🛡️

## 🎯 Overview

This guide documents the enhanced bot detection bypass strategies implemented for the YouTube Audio Extractor API. The improvements include:

- ✅ **Fresh cookie extraction and validation**
- ✅ **Enhanced yt-dlp configuration with randomization**
- ✅ **Advanced fallback extraction strategies**
- ✅ **Multiple client simulation (Android, iOS, TV, Web)**
- ✅ **Realistic browser headers and behavior**

## 🚀 Quick Fix Steps

### 1. Refresh Your Cookies

```bash
# Run the cookie refresh script
python3 refresh_cookies.py
```

This script will:
- Extract fresh cookies from Chrome, Firefox, or Edge
- Validate cookie content
- Test cookies with YouTube
- Backup old cookies automatically

### 2. Test Your API

```bash
# Update the server URL in the script first
python3 test_enhanced_api.py
```

### 3. Deploy Enhanced Code

The main API (`main.py`) now includes:
- Randomized user agents
- Enhanced HTTP headers
- Multiple retry strategies
- Advanced fallback extraction

## 📋 What's New

### Enhanced yt-dlp Configuration

```python
# Random user agents to avoid detection
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...',
    # ... more variants
]

# Enhanced options
opts = {
    'user_agent': random.choice(user_agents),
    'sleep_interval': random.uniform(1, 3),  # Random delays
    'max_sleep_interval': random.uniform(5, 10),
    'sleep_interval_requests': random.uniform(0.5, 1.5),
    
    # Realistic browser headers
    'http_headers': {
        'Accept': 'text/html,application/xhtml+xml,...',
        'Accept-Language': 'en-US,en;q=0.9',
        'DNT': '1',
        # ... more headers
    },
    
    # YouTube-specific optimizations
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'web'],  # Multiple clients
            'skip': ['dash', 'hls'],
            'max_comments': [0],  # Don't load comments
        }
    }
}
```

### Advanced Fallback System

The API now includes an `AdvancedYouTubeExtractor` that tries multiple strategies:

1. **Web Client** - Standard browser simulation
2. **Android Client** - Mobile app simulation  
3. **iOS Client** - iPhone app simulation
4. **TV Client** - Smart TV simulation
5. **Embedded Client** - Embedded player simulation
6. **Minimal Client** - Bare minimum configuration

### Automatic Fallback Logic

```python
try:
    # Try standard extraction
    info = standard_extract(url)
except BotDetectionError:
    # Automatically fallback to advanced strategies
    info = advanced_extract(url)
```

## 🔧 Manual Cookie Setup

If automatic cookie extraction fails:

### Method 1: Browser Extension (Recommended)

1. **Install Extension**:
   - Chrome: "Get cookies.txt LOCALLY"
   - Firefox: "cookies.txt"

2. **Extract Cookies**:
   - Open incognito/private window
   - Log into YouTube with throwaway account
   - Navigate to `https://www.youtube.com/robots.txt`
   - Export cookies as `cookies.txt`
   - Close private window immediately

3. **Place in Project**:
   ```bash
   # Copy to your project directory
   cp ~/Downloads/cookies.txt /path/to/your/project/
   ```

### Method 2: yt-dlp Command

```bash
# Extract from Chrome
yt-dlp --cookies-from-browser chrome --cookies cookies.txt "https://www.youtube.com"

# Extract from Firefox  
yt-dlp --cookies-from-browser firefox --cookies cookies.txt "https://www.youtube.com"
```

## 🧪 Testing & Validation

### Test Cookie Validity

```bash
# Test cookies work with yt-dlp
yt-dlp --cookies cookies.txt --no-download --get-title "https://www.youtube.com/shorts/dQw4w9WgXcQ"
```

### Test API Endpoints

```bash
# Test info extraction
curl -X POST "http://your-server:8000/extract-audio-info" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/shorts/N8tJFeMXrr8"}'

# Test audio extraction
curl -X POST "http://your-server:8000/extract-audio" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/shorts/N8tJFeMXrr8", "return_url": true}'
```

## 🐳 Docker Deployment

### With Cookies

```yaml
# docker-compose.yml
services:
  audio-extractor:
    build: .
    volumes:
      - ./cookies.txt:/app/cookies.txt:ro
    environment:
      - YOUTUBE_COOKIES_PATH=/app/cookies.txt
    ports:
      - "8000:8000"
```

### Build and Run

```bash
# Copy cookies to container
docker-compose up -d --build

# Or copy after startup
docker cp cookies.txt container_name:/app/cookies.txt
```

## 🚨 Troubleshooting

### Bot Detection Still Occurring

1. **Refresh Cookies**:
   ```bash
   python3 refresh_cookies.py
   ```

2. **Use Different Account**:
   - Create new throwaway YouTube account
   - Export cookies from that account
   - Don't use main personal account

3. **Try Different Browser**:
   - Extract cookies from different browser
   - Clear browser cache before extracting

4. **Check Cookie Age**:
   - Cookies expire after ~7 days of inactivity
   - Export fresh cookies weekly for heavy usage

### "No module named 'advanced_youtube_extractor'"

If running locally without Docker:
```bash
# Ensure the file is in the same directory
ls -la advanced_youtube_extractor.py

# Or copy to your Python path
cp advanced_youtube_extractor.py /path/to/your/python/site-packages/
```

### Rate Limiting Issues

- Current limits: 10 extractions/minute, 20 info requests/minute
- For higher volume, implement your own rate limiting
- Consider multiple throwaway accounts with rotation

### Specific Error Messages

| Error | Solution |
|-------|----------|
| "Sign in to confirm you're not a bot" | Refresh cookies |
| "Video unavailable" | Try different client (Android/iOS) |
| "Private video" | Use account that has access |
| "Age-restricted" | Use logged-in account cookies |
| Timeout errors | Increase timeouts, check server load |

## 📊 Success Metrics

After implementing these enhancements, you should see:

- ✅ **~90%+ success rate** with YouTube Shorts
- ✅ **Reduced bot detection** errors
- ✅ **Faster extraction** times (5-15 seconds)
- ✅ **Higher rate limits** with account cookies

## 🔒 Security Best Practices

1. **Use Dedicated Accounts**:
   - Create separate YouTube accounts for API usage
   - Don't use personal accounts

2. **Rotate Cookies**:
   - Refresh weekly for regular usage
   - Monitor logs for detection patterns

3. **Secure Storage**:
   ```bash
   chmod 600 cookies.txt  # Restrict permissions
   ```

4. **Monitor Usage**:
   - Stay under ~300 requests/hour without cookies
   - ~2000 requests/hour with valid account cookies

## 📈 Performance Optimization

### For High Volume Usage

1. **Cookie Rotation**:
   ```python
   # Implement multiple cookie files
   cookie_files = ['cookies1.txt', 'cookies2.txt', 'cookies3.txt']
   current_cookie = random.choice(cookie_files)
   ```

2. **Request Caching**:
   ```python
   # Cache video info for repeated requests
   @lru_cache(maxsize=1000)
   def get_video_info(url: str):
       return extract_info(url)
   ```

3. **Load Balancing**:
   - Deploy multiple API instances
   - Use different cookie files per instance
   - Implement health checks

## 📞 Support

If you're still experiencing issues:

1. **Check Logs**: Enable debug logging in your server
2. **Test Different URLs**: Try various YouTube Shorts
3. **Update Dependencies**: Ensure latest yt-dlp version
4. **Community**: Check yt-dlp GitHub issues for latest workarounds

---

**Last Updated**: December 2024  
**Next Review**: Check for yt-dlp updates monthly 