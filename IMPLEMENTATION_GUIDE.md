# Social Media Audio Extractor - Implementation Guide

## 🎯 Overview
This guide will walk you through implementing a complete Social Media Audio Extractor that processes Telegram messages (text, voice, or mixed), extracts audio from social media URLs, and generates engaging videos using AI.

## 📋 Prerequisites

### Required Services & Accounts
1. **n8n Instance** (Cloud or Self-hosted)
2. **Telegram Bot** (BotFather setup)
3. **OpenAI Account** (GPT & DALL-E access)
4. **Hedra Account** (Video generation API)
5. **Google Drive Account** (File storage)
6. **Audio Extraction API** (Your existing service at `52.0.132.35:8000`)

### Required Credentials
- Telegram Bot Token
- OpenAI API Key
- Hedra API Key
- Google Drive OAuth2 Credentials

## 🔧 Step-by-Step Implementation

### Step 1: Telegram Bot Setup

1. **Create Telegram Bot**
   ```
   1. Message @BotFather on Telegram
   2. Use /newbot command
   3. Follow prompts to create your bot
   4. Save the bot token provided
   ```

2. **Configure Bot Settings**
   ```
   /setcommands - Set bot commands
   /setdescription - Set bot description
   /setabouttext - Set about text
   ```

### Step 2: n8n Credentials Configuration

#### 2.1 Telegram Credentials
```json
{
  "name": "Telegram Bot",
  "type": "telegramApi",
  "data": {
    "accessToken": "YOUR_BOT_TOKEN_HERE"
  }
}
```

#### 2.2 OpenAI Credentials
```json
{
  "name": "OpenAI API",
  "type": "openAiApi", 
  "data": {
    "apiKey": "YOUR_OPENAI_API_KEY_HERE"
  }
}
```

#### 2.3 Hedra Custom Auth
```json
{
  "name": "Hedra API",
  "type": "httpCustomAuth",
  "data": {
    "headers": {
      "X-API-Key": "YOUR_HEDRA_API_KEY_HERE"
    }
  }
}
```

#### 2.4 Google Drive OAuth2
```json
{
  "name": "Google Drive",
  "type": "googleDriveOAuth2Api",
  "data": {
    "clientId": "YOUR_GOOGLE_CLIENT_ID",
    "clientSecret": "YOUR_GOOGLE_CLIENT_SECRET",
    "scope": "https://www.googleapis.com/auth/drive"
  }
}
```

### Step 3: Import Main Workflow

1. **Import Workflow**
   - Copy the `SocialMediaAudioExtractor.json` content
   - Import into your n8n instance
   - Connect all credentials to respective nodes

2. **Update Configuration**
   - Verify Audio Extraction API URL: `http://52.0.132.35:8000/extract-audio`
   - Update Google Drive folder ID for backup storage
   - Adjust video generation parameters as needed

### Step 4: Workflow Node Configuration

#### 4.1 Telegram Trigger Node
```json
{
  "parameters": {
    "updates": ["message", "edited_message"],
    "additionalFields": {
      "download_content": true
    }
  },
  "credentials": {
    "telegramApi": "Telegram Bot"
  }
}
```

#### 4.2 Audio Extractor API Node
```json
{
  "method": "POST",
  "url": "http://52.0.132.35:8000/extract-audio",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "url": "{{ $json.extracted_urls[0] }}",
    "format": "mp3",
    "quality": "192",
    "return_url": false
  },
  "timeout": 120000,
  "responseFormat": "file"
}
```

#### 4.3 Hedra Video Generation Node
```json
{
  "method": "POST",
  "url": "https://api.hedra.com/web-app/public/generations",
  "credentials": "Hedra API",
  "body": {
    "type": "video",
    "ai_model_id": "d1dd37a3-e39a-4854-a298-6510289f9cf2",
    "start_keyframe_id": "{{ $json.image_asset_id }}",
    "audio_id": "{{ $json.audio_asset_id }}",
    "generated_video_inputs": {
      "text_prompt": "{{ $json.visual_prompt }}",
      "resolution": "720p",
      "aspect_ratio": "9:16",
      "duration_ms": 15000
    }
  }
}
```

### Step 5: Testing & Validation

#### 5.1 Test Input Types
1. **Text with URL**: Send a message like `"Extract audio from https://youtube.com/watch?v=xyz"`
2. **Voice + URL**: Send a voice message saying "Create a dancing video" with text containing URL
3. **Voice Only**: Send voice message with URL mentioned in speech

#### 5.2 Expected Flow
```
1. User sends message to Telegram bot
2. Bot classifies input type (text/voice/mixed)
3. Extracts URLs and context from input
4. Downloads audio from social media URL
5. Generates AI-enhanced video prompt
6. Creates video using Hedra API
7. Sends final video back to user
```

## 🛠️ Error Handling & Troubleshooting

### Common Issues

#### 1. ContainerConfig Error (Docker)
**Solution from your original issue:**
```bash
# Clean up containers and images
docker-compose down --volumes --remove-orphans
docker rmi socialmedia-audio-extractor_audio-extractor
docker system prune -f

# Rebuild without cache
docker-compose build --no-cache
docker-compose up -d
```

#### 2. Telegram Webhook Issues
```bash
# Check webhook status
curl -X GET "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"

# Delete webhook if needed
curl -X GET "https://api.telegram.org/bot<TOKEN>/deleteWebhook"
```

#### 3. Audio Extraction Timeouts
- Increase timeout in HTTP Request node to 180000ms (3 minutes)
- Add retry logic for failed extractions
- Validate URL format before processing

#### 4. Hedra API Rate Limits
- Add wait nodes between API calls
- Implement exponential backoff
- Monitor API usage quotas

### Debugging Tips

1. **Enable Workflow Execution Data**
   - Go to Settings > Workflow Settings
   - Enable "Save Execution Progress"
   - Check execution logs for errors

2. **Test Individual Nodes**
   - Use Manual Trigger for testing
   - Test each node separately
   - Verify data format between nodes

3. **Monitor API Responses**
   - Check response codes and messages
   - Validate JSON structure
   - Ensure proper error handling

## 📈 Performance Optimization

### 1. Caching Strategy
- Cache frequently used AI responses
- Store user preferences and settings
- Implement session management for repeated requests

### 2. Resource Management
- Limit concurrent video generations
- Implement queue system for high traffic
- Set appropriate timeouts for each service

### 3. Monitoring Setup
```javascript
// Add to workflow for monitoring
const executionTime = Date.now() - $('Telegram Trigger').item.json.timestamp;
const success = $json.status === 'completed';

// Log metrics
console.log({
  execution_time: executionTime,
  success: success,
  user_id: $json.chat_id,
  url_processed: $json.source_url
});
```

## 🚀 Production Deployment

### 1. Environment Setup
```yaml
# docker-compose.yml updates
services:
  n8n:
    environment:
      - N8N_ENCRYPTION_KEY=your-encryption-key
      - WEBHOOK_URL=https://your-domain.com/
      - GENERIC_TIMEZONE=UTC
      - N8N_SECURE_COOKIE=false
      - N8N_LOG_LEVEL=info
```

### 2. Security Considerations
- Use environment variables for all secrets
- Enable HTTPS for webhook endpoints
- Implement rate limiting
- Set up proper CORS policies

### 3. Backup Strategy
- Regular workflow exports
- Database backups
- Google Drive file retention policies
- Monitoring and alerting setup

## 📋 Maintenance Checklist

### Daily
- [ ] Monitor execution success rates
- [ ] Check API quota usage
- [ ] Review error logs

### Weekly  
- [ ] Update AI prompts based on user feedback
- [ ] Clean up old files from Google Drive
- [ ] Performance optimization review

### Monthly
- [ ] API key rotation
- [ ] Security audit
- [ ] Feature enhancement planning
- [ ] User feedback analysis

## 🎯 Next Steps & Enhancements

### Phase 2 Features
1. **Batch Processing**: Handle multiple URLs in single request
2. **Custom Styles**: User-selectable video styles and themes
3. **Social Sharing**: Direct posting to social platforms
4. **Analytics Dashboard**: Usage stats and performance metrics

### Phase 3 Features
1. **Voice Cloning**: Replicate user's voice for narration
2. **Advanced Editing**: Trim, merge, and enhance videos
3. **Template System**: Pre-built video templates
4. **Collaboration**: Team workspaces and sharing

---

## 🎉 Conclusion

This implementation provides a robust foundation for social media audio extraction and video generation. The system handles multiple input types, provides comprehensive error handling, and delivers high-quality video content directly to users via Telegram.

**Key Benefits:**
- ✅ Multi-modal input support (text, voice, mixed)
- ✅ AI-powered content enhancement
- ✅ Professional video generation
- ✅ Comprehensive error handling
- ✅ Scalable architecture
- ✅ Direct Telegram delivery

Follow this guide step-by-step to implement your Social Media Audio Extractor successfully! 