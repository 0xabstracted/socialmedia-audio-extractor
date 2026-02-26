# Social Media Audio Extractor - Execution Plan

## 🎯 Project Overview
Build a comprehensive Telegram bot that extracts audio from social media URLs, processes mixed input types (text, voice, URLs), and generates engaging videos using Hedra API integration.

## 📋 Core Requirements Analysis

### Input Handling
- **Telegram Trigger**: Handle text messages, voice messages, and mixed inputs
- **URL Processing**: Extract audio from social media platforms (YouTube, TikTok, Instagram, etc.)
- **Voice Transcription**: Convert voice messages to text using OpenAI Whisper
- **Multi-modal Input**: Support combinations of text + voice + URLs in single request

### Processing Pipeline
- **Audio Extraction**: Use existing API at `http://52.0.132.35:8000/extract-audio`
- **Content Generation**: Create engaging content using AI models
- **Video Generation**: Leverage Hedra API for video creation with audio sync
- **Response Delivery**: Send processed videos directly via Telegram

## 🏗️ Architecture Design

### 1. Input Layer (Telegram Integration)
```
Telegram Trigger → Input Classification → Processing Router
```

**Components:**
- Telegram Trigger (handles all message types)
- Input Switch (text/voice/mixed detection)
- Voice File Download & Transcription
- URL Extraction & Validation

### 2. Processing Layer (Audio & Content)
```
URL Input → Audio Extraction → Content Analysis → AI Enhancement
```

**Components:**
- Audio Extractor API integration
- Content analyzer (extract metadata, duration, quality)
- AI content enhancer (generate descriptions, titles)
- Format standardization (MP3, quality optimization)

### 3. Video Generation Layer (Hedra Integration)
```
Audio + Metadata → Asset Creation → Video Generation → Quality Check
```

**Components:**
- Hedra Asset Creation (audio + image assets)
- Video generation with custom prompts
- Progress monitoring and status checks
- Quality validation and retry logic

### 4. Output Layer (Telegram Response)
```
Generated Video → Google Drive Storage → Telegram Delivery
```

**Components:**
- Google Drive upload for backup
- Direct Telegram video sending
- Progress notifications
- Error handling and user feedback

## 🔧 Technical Implementation Plan

### Phase 1: Core Infrastructure Setup
1. **Telegram Bot Configuration**
   - Set up Telegram trigger with webhook
   - Configure message type detection
   - Implement voice file download

2. **Audio Extraction Integration**
   - Connect to existing API endpoint
   - Add error handling and retry logic
   - Implement timeout management

3. **Basic Response System**
   - Simple text responses
   - File upload capabilities
   - Progress notifications

### Phase 2: AI-Powered Processing
1. **Voice Transcription**
   - OpenAI Whisper integration
   - Language detection
   - Quality optimization

2. **Content Analysis**
   - Extract metadata from URLs
   - Generate engaging descriptions
   - Create video prompts

3. **Smart Input Handling**
   - Mixed input processing
   - Context understanding
   - User intent recognition

### Phase 3: Video Generation (Hedra Integration)
1. **Asset Management**
   - Audio asset creation
   - Image asset generation
   - Asset uploading and validation

2. **Video Creation**
   - Custom prompt generation
   - Video parameter optimization
   - Progress monitoring

3. **Quality Control**
   - Output validation
   - Retry mechanisms
   - Error recovery

### Phase 4: Advanced Features
1. **Batch Processing**
   - Multiple URL handling
   - Queue management
   - Priority processing

2. **Customization Options**
   - Video style selection
   - Quality preferences
   - Output format choices

3. **Analytics & Monitoring**
   - Usage tracking
   - Performance metrics
   - Error logging

## 📊 Workflow Structure

### Main Workflow: `SocialMediaAudioExtractor`
```
Telegram Trigger
├── Input Switch (Text/Voice/Mixed)
│   ├── Voice Branch
│   │   ├── Download Voice File
│   │   ├── Transcribe Audio (OpenAI)
│   │   └── Extract URLs from Transcription
│   ├── Text Branch
│   │   ├── Extract URLs from Text
│   │   └── Validate URL Format
│   └── Mixed Branch
│       ├── Process Voice Component
│       ├── Process Text Component
│       └── Merge Context
├── URL Processing
│   ├── Audio Extraction API Call
│   ├── Metadata Analysis
│   └── Quality Optimization
├── AI Content Generation
│   ├── Generate Video Description
│   ├── Create Engaging Title
│   └── Build Hedra Prompt
├── Hedra Video Generation
│   ├── Create Audio Asset
│   ├── Generate/Select Image Asset
│   ├── Upload Assets
│   ├── Create Video Generation Request
│   ├── Monitor Progress (Wait + Check)
│   └── Download Generated Video
├── Output Processing
│   ├── Upload to Google Drive (backup)
│   ├── Send Video to Telegram
│   └── Send Confirmation Message
└── Error Handling
    ├── API Error Recovery
    ├── User Notification
    └── Retry Logic
```

### Supporting Workflows:
1. **AudioExtractionHandler**: Dedicated audio extraction with retry logic
2. **VideoGenerationManager**: Hedra API interaction management
3. **ContentEnhancer**: AI-powered content generation
4. **ErrorHandler**: Centralized error management

## 🛠️ Node Configuration Details

### Telegram Trigger Setup
```json
{
  "parameters": {
    "updates": ["message", "edited_message"],
    "additionalFields": {
      "download_content": true
    }
  }
}
```

### Input Classification Switch
```javascript
// Input type detection logic
const hasVoice = $json.message?.voice?.file_id;
const hasText = $json.message?.text;
const hasUrls = /https?:\/\/[^\s]+/.test($json.message?.text || '');

if (hasVoice && hasText && hasUrls) return "mixed";
if (hasVoice) return "voice";
if (hasText && hasUrls) return "text_with_url";
return "text_only";
```

### Audio Extraction API Call
```json
{
  "method": "POST",
  "url": "http://52.0.132.35:8000/extract-audio",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "url": "={{ $json.extracted_url }}",
    "format": "mp3",
    "quality": "192",
    "return_url": false
  },
  "timeout": 120000,
  "responseFormat": "file"
}
```

### Hedra Asset Creation
```json
{
  "method": "POST",
  "url": "https://api.hedra.com/web-app/public/assets",
  "body": {
    "name": "extracted-audio-{{ $now() }}",
    "type": "audio"
  }
}
```

### Video Generation Request
```json
{
  "method": "POST",
  "url": "https://api.hedra.com/web-app/public/generations",
  "body": {
    "type": "video",
    "ai_model_id": "d1dd37a3-e39a-4854-a298-6510289f9cf2",
    "audio_id": "{{ $json.audio_asset_id }}",
    "generated_video_inputs": {
      "text_prompt": "{{ $json.enhanced_prompt }}",
      "resolution": "720p",
      "aspect_ratio": "9:16",
      "duration_ms": "{{ $json.audio_duration }}"
    }
  }
}
```

## 🔐 Required Credentials & APIs

### Essential Services
1. **Telegram Bot API**
   - Bot token for webhook setup
   - Chat permissions for file handling

2. **OpenAI API**
   - Whisper for audio transcription
   - GPT models for content enhancement

3. **Hedra API**
   - Asset creation and management
   - Video generation services

4. **Google Drive API**
   - File upload and storage
   - Backup and sharing capabilities

### Optional Enhancements
1. **ElevenLabs API**: Voice synthesis for narration
2. **Stability AI**: Image generation for thumbnails
3. **Redis**: Caching and session management

## 📈 Success Metrics & Monitoring

### Performance KPIs
- Audio extraction success rate (target: >95%)
- Video generation completion rate (target: >90%)
- Average processing time (target: <5 minutes)
- User satisfaction score (feedback-based)

### Monitoring Points
- API response times
- Error rates by component
- Resource utilization
- User engagement patterns

## 🚀 Deployment Strategy

### Development Phase
1. Local n8n instance setup
2. Test with sample URLs and audio files
3. Validate Hedra API integration
4. Test Telegram bot functionality

### Staging Phase
1. Deploy to staging environment
2. Load testing with multiple concurrent requests
3. Error handling validation
4. User acceptance testing

### Production Phase
1. Deploy to production n8n instance
2. Configure monitoring and alerting
3. Set up backup and recovery procedures
4. Launch with limited user group

## 📚 Documentation Requirements

### Technical Documentation
1. API integration guides
2. Workflow configuration instructions
3. Troubleshooting guides
4. Performance optimization tips

### User Documentation
1. Bot usage instructions
2. Supported platforms and formats
3. Quality and limitation guidelines
4. FAQ and common issues

## 🔄 Maintenance & Updates

### Regular Maintenance
- API endpoint health checks
- Credential rotation and security updates
- Performance optimization reviews
- User feedback incorporation

### Feature Evolution
- Support for additional platforms
- Enhanced video customization options
- Batch processing capabilities
- Advanced AI integration

---

## Next Steps
1. Review and approve this execution plan
2. Set up development environment
3. Begin Phase 1 implementation
4. Establish testing protocols
5. Create detailed technical specifications

*This plan provides a comprehensive roadmap for building a robust, scalable social media audio extractor with advanced video generation capabilities.* 