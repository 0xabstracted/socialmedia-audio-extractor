# n8n Integration Guide for Social Media Audio Extractor

This guide explains how to integrate the Social Media Audio Extractor API with n8n workflows.

## API Endpoints

### 1. Extract Audio Info (Preview)
- **URL**: `POST /extract-audio-info`
- **Purpose**: Get metadata without downloading
- **Use**: Validate URLs and preview content

### 2. Extract Audio (Download)
- **URL**: `POST /extract-audio`
- **Purpose**: Extract and download audio as binary data
- **Use**: Get the actual MP3 file for processing

## n8n Node Configuration

### HTTP Request Node Setup

#### For Audio Info (Preview):
```json
{
  "method": "POST",
  "url": "http://your-server:8000/extract-audio-info",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "url": "{{ $json.social_media_url }}",
    "format": "mp3",
    "quality": "192"
  }
}
```

#### For Audio Extraction:
```json
{
  "method": "POST",
  "url": "http://your-server:8000/extract-audio",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "url": "{{ $json.social_media_url }}",
    "format": "mp3",
    "quality": "192"
  },
  "responseFormat": "file"
}
```

## Sample n8n Workflows

### Workflow 1: URL Validation and Audio Extraction

1. **Webhook Node**: Receive social media URL
2. **HTTP Request Node**: Call `/extract-audio-info` for validation
3. **IF Node**: Check if valid
4. **HTTP Request Node**: Call `/extract-audio` if valid
5. **Set Node**: Process response headers and binary data

### Workflow 2: Batch Processing

1. **Trigger**: Read URLs from Google Sheets/Airtable
2. **Split in Batches**: Process multiple URLs
3. **HTTP Request**: Extract audio for each URL
4. **Google Drive/AWS S3**: Save extracted audio files

### Workflow 3: Content Analysis Pipeline

1. **HTTP Request**: Extract audio
2. **OpenAI Whisper**: Transcribe audio to text
3. **OpenAI GPT**: Analyze content sentiment
4. **Database**: Store results

## Working with Binary Data in n8n

### Accessing Audio File
The audio extraction endpoint returns binary data. In n8n:

```javascript
// Get binary data
const audioData = $binary.data;

// Get metadata from headers
const duration = $response.headers['x-audio-duration'];
const fileSize = $response.headers['x-file-size'];
const title = $response.headers['x-original-title'];
```

### Saving to Cloud Storage

#### AWS S3 Node:
- **Input**: Binary data from HTTP Request
- **Bucket**: Your S3 bucket
- **File Name**: `{{ $json.title }}.mp3`

#### Google Drive Node:
- **Input**: Binary data from HTTP Request
- **Name**: `{{ $json.title }}.mp3`
- **MIME Type**: `audio/mpeg`

## Error Handling

### Common Error Codes
- `400`: Invalid URL (not from supported platforms)
- `429`: Rate limit exceeded
- `500`: Extraction failed

### n8n Error Handling:
```javascript
// Check response status
if ($response.statusCode !== 200) {
  throw new Error(`Audio extraction failed: ${$response.statusMessage}`);
}

// Validate binary data
if (!$binary.data) {
  throw new Error('No audio data received');
}
```

## Environment Variables

Set these in your n8n environment:

```bash
AUDIO_EXTRACTOR_API_URL=http://your-server:8000
AUDIO_EXTRACTOR_RATE_LIMIT=10  # requests per minute
```

## Example n8n JSON Workflow

```json
{
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "extract-audio",
        "responseMode": "responseNode"
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "parameters": {
        "url": "={{ $env.AUDIO_EXTRACTOR_API_URL }}/extract-audio",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendBody": true,
        "bodyContentType": "json",
        "jsonBody": "={\n  \"url\": \"{{ $json.body.url }}\",\n  \"format\": \"mp3\",\n  \"quality\": \"192\"\n}",
        "options": {
          "response": {
            "response": {
              "responseFormat": "file"
            }
          }
        }
      },
      "name": "Extract Audio",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300]
    },
    {
      "parameters": {
        "values": {
          "string": [
            {
              "name": "filename",
              "value": "={{ $response.headers['x-original-title'] }}.mp3"
            },
            {
              "name": "duration",
              "value": "={{ $response.headers['x-audio-duration'] }}"
            },
            {
              "name": "fileSize",
              "value": "={{ $response.headers['x-file-size'] }}"
            }
          ]
        }
      },
      "name": "Process Response",
      "type": "n8n-nodes-base.set",
      "position": [650, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [
        [
          {
            "node": "Extract Audio",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Extract Audio": {
      "main": [
        [
          {
            "node": "Process Response",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

## Best Practices

1. **Rate Limiting**: Respect the 10 requests/minute limit
2. **Error Handling**: Always include error handling for failed extractions
3. **Binary Data**: Use `responseFormat: "file"` for audio extraction
4. **Metadata**: Utilize response headers for file information
5. **Validation**: Use the info endpoint before extraction for large batches
6. **Storage**: Consider file size limits when saving to cloud storage

## Troubleshooting

### Common Issues:
1. **No binary data**: Check `responseFormat` is set to "file"
2. **Rate limit errors**: Add delays between requests
3. **Invalid URLs**: Validate URLs match supported platforms
4. **Large files**: Monitor memory usage for long audio files

### Debug Mode:
Enable n8n debug mode to see full HTTP responses and binary data information. 