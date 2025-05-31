# YouTube Cookies Setup Guide

## 🍪 Why Cookies Are Needed

YouTube is enforcing stricter bot detection measures. Using cookies from your browser helps bypass these restrictions by making requests appear as if they're coming from a real user session.

## 📋 Methods to Provide Cookies

### Method 1: Browser Cookie Extraction (Recommended)

The API will automatically try to use Chrome browser cookies if available. No setup required!

### Method 2: Manual Cookie Export

#### Option A: Using yt-dlp to Export Cookies

1. **Install yt-dlp locally** (if not already installed):
   ```bash
   pip install yt-dlp
   ```

2. **Export cookies from Chrome**:
   ```bash
   # This creates a cookies.txt file with your YouTube session
   yt-dlp --cookies-from-browser chrome --cookies /path/to/cookies.txt "https://www.youtube.com"
   ```

3. **For Firefox users**:
   ```bash
   yt-dlp --cookies-from-browser firefox --cookies /path/to/cookies.txt "https://www.youtube.com"
   ```

#### Option B: Browser Extension Method

1. **Install a cookie export extension**:
   - **Chrome**: "Get cookies.txt LOCALLY" (safe version)
   - **Firefox**: "cookies.txt"

2. **Export YouTube cookies**:
   - Navigate to YouTube.com
   - Click the extension icon
   - Export cookies as `cookies.txt`

#### Option C: Private Browsing Method (Most Secure)

1. **Open incognito/private window**
2. **Log into YouTube** in that window
3. **Navigate to** `https://www.youtube.com/robots.txt` (this prevents cookie rotation)
4. **Export cookies** using browser extension
5. **Close the private window** immediately

## 🐳 Docker Deployment with Cookies

### Method 1: Environment Variable

```bash
# Set the path to your cookies file
export YOUTUBE_COOKIES_PATH=/path/to/your/cookies.txt

# Run with docker-compose
docker-compose -f docker-compose.simple.yml up -d --build
```

### Method 2: Volume Mount

Add this to your `docker-compose.yml`:

```yaml
services:
  audio-extractor:
    volumes:
      - /path/to/your/cookies.txt:/app/cookies.txt:ro
    environment:
      - YOUTUBE_COOKIES_PATH=/app/cookies.txt
```

### Method 3: Copy to Container

```bash
# Copy cookies to running container
docker cp cookies.txt container_name:/app/cookies.txt

# Set environment variable
docker exec container_name sh -c 'export YOUTUBE_COOKIES_PATH=/app/cookies.txt'
```

## 🔧 API Configuration

The API now automatically:
- ✅ **Tries Chrome browser cookies** (if available)
- ✅ **Uses environment variable** `YOUTUBE_COOKIES_PATH`
- ✅ **Adds realistic User-Agent** headers
- ✅ **Implements request delays** to avoid rate limiting
- ✅ **Uses YouTube-optimized** extractor settings

## 🧪 Testing Cookie Setup

### Test Script with Cookie Validation

```python
import requests
import os

# Your server URL
BASE_URL = "http://your-server:8000"

def test_youtube_with_cookies():
    """Test YouTube extraction with cookies"""
    
    # Test URL that often triggers bot detection
    test_url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
    
    payload = {
        "url": test_url,
        "format": "mp3",
        "quality": "192"
    }
    
    print("Testing YouTube Shorts extraction...")
    response = requests.post(f"{BASE_URL}/extract-audio-info", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ SUCCESS! Cookies are working")
        print(f"Title: {data.get('title')}")
        print(f"Duration: {data.get('duration')} seconds")
    else:
        print("❌ FAILED - Cookie setup needed")
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_youtube_with_cookies()
```

## 🔒 Security Best Practices

1. **Use throwaway account**: Create a separate YouTube account for API usage
2. **Monitor usage**: Don't exceed ~300 videos/hour without account cookies
3. **Rotate cookies**: Export fresh cookies periodically (weekly)
4. **Secure storage**: Keep cookies file with restricted permissions:
   ```bash
   chmod 600 cookies.txt
   ```

## 🐛 Troubleshooting

### "Sign in to confirm you're not a bot"
- ✅ **Solution**: Export fresh cookies using private browsing method
- ✅ **Check**: Ensure cookies.txt file format is correct (Netscape format)

### "This content isn't available"
- ✅ **Solution**: Add delays between requests (already implemented)
- ✅ **Check**: Don't exceed rate limits (~300 videos/hour)

### Cookies not working
- ✅ **Check file path**: Ensure `YOUTUBE_COOKIES_PATH` points to correct file
- ✅ **Check permissions**: Make sure Docker can read the cookies file
- ✅ **Re-export**: Cookies may have expired, export fresh ones

## 📊 Expected Results

After proper cookie setup:
- ✅ **YouTube Shorts**: Should extract successfully
- ✅ **Age-restricted content**: Should work with logged-in cookies
- ✅ **Rate limits**: Higher limits with account cookies (~2000/hour vs ~300/hour)

## 🔄 Cookie Maintenance

1. **Monitor logs** for bot detection errors
2. **Re-export cookies** when errors occur
3. **Use different browser profiles** for backup cookies
4. **Consider multiple throwaway accounts** for high-volume usage

---

**Next Steps**: Follow Method 1 (browser extraction) or Method 2A (yt-dlp export) to set up cookies for your server. 