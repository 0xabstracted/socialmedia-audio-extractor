# n8n Integration Guide for YouTube Audio Extractor 🎵

## 🎯 Quick Setup for n8n

This guide shows you exactly how to configure your n8n HTTP nodes to extract YouTube audio using your AWS API.

## 📋 Prerequisites

1. ✅ YouTube Audio Extractor deployed on AWS
2. ✅ API accessible at `http://your-ec2-ip:8000`
3. ✅ n8n instance running

## 🚀 HTTP Node Configurations

### Option 1: Get Audio as Binary Data (Recommended)

**Use this when:** You want the MP3 file directly in n8n for further processing.

```yaml
HTTP Request Node Settings:
├── Method: POST
├── URL: http://your-ec2-ip:8000/extract-audio
├── Response Format: File
├── Request Format: JSON
├── Authentication: None
├── Timeout: 120000 (2 minutes)
└── Body (JSON):
    {
      "url": "{{ $json.youtube_url }}",
      "format": "mp3",
      "quality": "192",
      "return_url": false
    }
```

**Result:** The audio file will be available as binary data in `$binary.data`.

### Option 2: Get Download URL

**Use this when:** You want a URL to download the audio file later.

```yaml
HTTP Request Node Settings:
├── Method: POST
├── URL: http://your-ec2-ip:8000/extract-audio
├── Response Format: JSON
├── Request Format: JSON
├── Authentication: None
├── Timeout: 120000 (2 minutes)
└── Body (JSON):
    {
      "url": "{{ $json.youtube_url }}",
      "format": "mp3",
      "quality": "192",
      "return_url": true
    }
```

**Result:** You'll get a JSON response with `download_url` field.

### Option 3: Get Video Info Only

**Use this when:** You want to check video details before extracting audio.

```yaml
HTTP Request Node Settings:
├── Method: POST
├── URL: http://your-ec2-ip:8000/extract-audio-info
├── Response Format: JSON
├── Request Format: JSON
├── Authentication: None
├── Timeout: 30000 (30 seconds)
└── Body (JSON):
    {
      "url": "{{ $json.youtube_url }}",
      "format": "mp3",
      "quality": "192"
    }
```

## 🎬 Step-by-Step n8n Setup

### Step 1: Create a New Workflow

1. Open n8n
2. Click "New Workflow"
3. Add a "Manual Trigger" node

### Step 2: Add HTTP Request Node

1. Click the "+" button
2. Search for "HTTP Request"
3. Select "HTTP Request" node

### Step 3: Configure HTTP Node for Audio Extraction

**Basic Settings:**
- **Method:** `POST`
- **URL:** `http://your-ec2-ip:8000/extract-audio` (replace with your actual IP)

**Authentication:**
- **Authentication:** `None`

**Body:**
- **Request Format:** `JSON`
- **JSON:** Enable "JSON Parameters"
- **Parameters:**
  ```json
  {
    "url": "https://www.youtube.com/shorts/N8tJFeMXrr8",
    "format": "mp3",
    "quality": "192",
    "return_url": false
  }
  ```

**Options:**
- **Response Format:** `File` (for binary data) or `JSON` (for URL)
- **Timeout:** `120000`

### Step 4: Test the Node

1. Click "Test Step" on the HTTP Request node
2. You should see the audio file in the node output
3. If using binary format, check the "Binary" tab for the MP3 file

## 📊 Example Workflows

### Simple Audio Extraction

```
[Manual Trigger] → [HTTP Request: Extract Audio] → [Output]
```

### With Error Handling

```
[Manual Trigger] 
    ↓
[HTTP Request: Get Info] 
    ↓
[IF: Check Success] 
    ├─ TRUE → [HTTP Request: Extract Audio] → [Output]
    └─ FALSE → [Stop and Error]
```

### Processing Multiple URLs

```
[Manual Trigger] 
    ↓
[Set: YouTube URLs Array] 
    ↓
[Split In Batches] 
    ↓
[HTTP Request: Extract Audio] 
    ↓
[Merge] 
    ↓
[Output]
```

## 🔧 Advanced Configuration

### Dynamic URL from Previous Node

Instead of hardcoding the URL, use data from previous nodes:

```json
{
  "url": "{{ $json.youtube_url }}",
  "format": "mp3",
  "quality": "192"
}
```

### Handle Different Video Qualities

```json
{
  "url": "{{ $json.youtube_url }}",
  "format": "mp3",
  "quality": "{{ $json.audio_quality || '192' }}"
}
```

### Error Handling with IF Node

After the HTTP request, add an IF node:

**Condition:** `{{ $json.success }} is equal to true`
- **TRUE branch:** Continue with success flow
- **FALSE branch:** Handle error (email notification, etc.)

## 🚨 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Connection refused** | Check if your EC2 security group allows port 8000 |
| **Timeout errors** | Increase timeout to 120000ms (2 minutes) |
| **Empty response** | Check server logs: `docker logs youtube-audio-extractor` |
| **Bot detection error** | Refresh cookies on your server |

### Testing Your API

Before configuring n8n, test your API directly:

```bash
# Test health endpoint
curl http://your-ec2-ip:8000/health

# Test video info extraction
curl -X POST http://your-ec2-ip:8000/extract-audio-info \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/shorts/dQw4w9WgXcQ"}'

# Test audio extraction (URL mode)
curl -X POST http://your-ec2-ip:8000/extract-audio \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/shorts/dQw4w9WgXcQ", "return_url": true}'
```

### Debug Mode

Enable debug logging in your n8n workflow:
1. Add a "Set" node after HTTP Request
2. Set `debug_response` to `{{ $json }}`
3. Check the execution log for detailed response

## 🎵 Using the Audio Data

### Save to File System

After getting binary data, use a "Write Binary File" node:
- **File Name:** `{{ $json.title || 'audio' }}.mp3`
- **Data:** `{{ $binary.data }}`

### Upload to Cloud Storage

Use cloud storage nodes (AWS S3, Google Drive, etc.):
- **File Name:** `{{ $json.title }}.mp3`
- **File Data:** `{{ $binary.data }}`

### Send via Email

Use email node with attachment:
- **Attachment:** Binary data from HTTP Request
- **Filename:** `{{ $json.title }}.mp3`

## 📝 Complete Example Workflow

### Import this JSON into n8n:

```json
{
  "name": "YouTube to MP3 Extractor",
  "nodes": [
    {
      "parameters": {
        "values": {
          "string": [
            {
              "name": "youtube_url",
              "value": "https://www.youtube.com/shorts/N8tJFeMXrr8"
            },
            {
              "name": "api_url",
              "value": "http://your-ec2-ip:8000"
            }
          ]
        }
      },
      "name": "Input",
      "type": "n8n-nodes-base.set"
    },
    {
      "parameters": {
        "httpVersion": "v2",
        "method": "POST",
        "url": "={{ $json.api_url }}/extract-audio",
        "requestFormat": "json",
        "responseFormat": "file",
        "jsonParameters": true,
        "parametersJson": {
          "url": "={{ $json.youtube_url }}",
          "format": "mp3",
          "quality": "192"
        },
        "options": {
          "timeout": 120000
        }
      },
      "name": "Extract Audio",
      "type": "n8n-nodes-base.httpRequest"
    }
  ],
  "connections": {
    "Input": {
      "main": [
        [
          {
            "node": "Extract Audio",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

## 🔄 Automation Ideas

### Webhook Trigger

Replace Manual Trigger with Webhook:
1. **URL:** `https://your-n8n-instance/webhook/youtube-extract`
2. **Method:** `POST`
3. **Body:** `{ "youtube_url": "..." }`

### Schedule Processing

Use Cron Trigger to process a list of URLs:
1. **Cron Expression:** `0 */6 * * *` (every 6 hours)
2. **Read URLs from:** Google Sheets, Airtable, or JSON file
3. **Process in batches** to avoid overwhelming the API

### Integration with Other Services

- **Telegram Bot:** Extract audio from YouTube links sent to a bot
- **Discord Bot:** Process YouTube links shared in Discord channels
- **RSS Feed:** Extract audio from YouTube videos in RSS feeds
- **Zapier/Make:** Trigger from other automation platforms

---

**Quick Start Checklist:**
1. ✅ Replace `your-ec2-ip` with your actual EC2 IP address
2. ✅ Test API health endpoint
3. ✅ Import example workflow into n8n
4. ✅ Update URLs in the workflow
5. ✅ Test with a YouTube Shorts URL
6. ✅ Customize for your specific use case

**Support:** Check your server logs if issues occur: `docker logs youtube-audio-extractor` 