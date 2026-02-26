# Enhanced Aniton Workflow - Comprehensive Plan

## 🎯 Project Overview
**Objective**: Create an advanced n8n workflow that takes three user inputs (Instagram Reel URL, custom image, and transformation prompt) to generate an animated video where the custom image is transformed and animated according to the user's specifications, synchronized with the audio from the Instagram Reel.

## 📋 Step-by-Step Workflow Plan

### **Phase 1: Input Collection & Validation**

#### Step 1: Telegram Trigger
- Listen for incoming messages from users
- Support multiple input types (URLs, images, text)

#### Step 2: Input Type Detection
- **Instagram Reel URL Detection**: Identify Instagram URLs using regex patterns
- **Image File Detection**: Detect uploaded image files (JPG, PNG, etc.)
- **Text Prompt Detection**: Identify transformation and behavior prompts

#### Step 3: Input Collection State Management
- Store all three required inputs in session memory:
  - Instagram Reel URL
  - User-uploaded image
  - Combined transformation prompt
- Track completion status of each input type

#### Step 4: Validation Check
- Ensure all three inputs are collected before proceeding
- Provide clear feedback to user about missing inputs
- Guide user through the input process

---

### **Phase 2: Audio Extraction**

#### Step 5: Audio Extraction API Call
- Use existing social media audio extractor API
- Extract high-quality audio from Instagram Reel URL
- Handle various Instagram URL formats

#### Step 6: Audio Processing
- Convert extracted audio to Hedra-compatible format
- Optimize audio quality and duration
- Prepare for Hedra upload

---

### **Phase 3: Prompt Intelligence & Separation**

#### Step 7: AI Prompt Analyzer Agent
**Purpose**: Intelligently analyze user's single prompt and extract two distinct components

**Input**: Combined user prompt (e.g., "Convert this image to a cute baby who is dancing happily to the music")

**AI Processing**: Use GPT model to separate into:
- **Image Transformation Prompt**: How to transform the original image
  - Examples: "convert to baby", "make it look like an old man", "transform into anime character"
- **Video Behavior Prompt**: What actions/movements the image should perform
  - Examples: "nodding head", "dancing", "talking expressively", "laughing"

#### Step 8: Structured Output Parser
- Ensure clean JSON output with separated prompts
- Validate prompt quality and completeness
- Handle edge cases and ambiguous inputs

---

### **Phase 4: Image Generation & Processing**

#### Step 9: Enhanced Image Prompt Creation
- Combine user's transformation prompt with uploaded image
- Create detailed, high-quality image generation prompt
- Include style, lighting, and quality specifications

#### Step 10: ChatGPT Image Generation
- Generate transformed image using OpenAI DALL-E
- Apply transformation based on separated image prompt
- Ensure high resolution and quality

#### Step 11: Hedra Image Asset Creation
- Create image asset in Hedra system
- Prepare for image upload

#### Step 12: Image Upload to Hedra
- Upload generated image to Hedra
- Handle upload confirmation and asset ID retrieval

---

### **Phase 5: Audio Processing for Hedra**

#### Step 13: Hedra Audio Asset Creation
- Create audio asset in Hedra system
- Set appropriate audio parameters

#### Step 14: Audio Upload to Hedra
- Upload extracted audio to Hedra
- Ensure proper format and quality
- Retrieve audio asset ID

---

### **Phase 6: Video Generation**

#### Step 15: Video Prompt Enhancement
- Refine video behavior prompt for Hedra's specific requirements
- Add technical specifications (resolution, duration, style)
- Optimize for best animation results

#### Step 16: Hedra Video Creation
**Inputs**:
- Transformed image asset ID
- Extracted audio asset ID
- Enhanced video behavior prompt

**Configuration**:
- Resolution: 720p or higher
- Aspect ratio: 9:16 (mobile-optimized)
- Duration: Based on audio length

#### Step 17: Video Processing Wait
- Implement intelligent waiting system
- Monitor Hedra processing status
- Provide progress updates to user

#### Step 18: Video Retrieval
- Download completed video from Hedra
- Verify video quality and completeness

---

### **Phase 7: Delivery & Optional Distribution**

#### Step 19: Video Delivery
- Send final animated video to user via Telegram
- Include completion message and optional details

#### Step 20: Optional: Cloud Storage
- Upload to Google Drive for backup
- Generate shareable links

#### Step 21: Optional: Social Media Distribution
- Auto-post to configured platforms (Instagram, TikTok, YouTube)
- Apply appropriate captions and hashtags

---

## 🔧 Key Components Required

### **🤖 AI Agents**

1. **Input Validator Agent**
   - Ensures all required inputs are present
   - Provides clear user guidance
   - Handles error states gracefully

2. **Prompt Separator Agent**
   - Intelligently splits combined prompt
   - Uses advanced NLP to understand context
   - Outputs structured, usable prompts

3. **Image Enhancement Agent**
   - Creates detailed image generation prompts
   - Incorporates best practices for AI image generation
   - Ensures consistency with user intent

4. **Video Prompt Optimizer Agent**
   - Optimizes video prompts for Hedra API
   - Includes technical specifications
   - Maximizes animation quality

### **🔧 Technical Integrations**

1. **Existing APIs**:
   - Social Media Audio Extractor API (from flow1.json)
   - OpenAI Image Generation API
   - Hedra Video Generation API
   - Telegram Bot API

2. **Optional Integrations**:
   - Google Drive API
   - Social Media Platform APIs

### **💾 State Management**

1. **Session Storage**:
   - User input tracking
   - Progress state management
   - Error handling states

2. **Data Flow**:
   - Input → Processing → Output pipeline
   - Async operation handling
   - Status monitoring

### **🎯 User Experience Features**

1. **Input Guidance**:
   - Clear instructions for each input type
   - Examples and templates
   - Progress indicators

2. **Processing Updates**:
   - Real-time status updates
   - Estimated completion times
   - Error notifications

3. **Quality Assurance**:
   - Input validation
   - Output verification
   - Retry mechanisms

---

## 📊 Expected User Flow

1. **User sends Instagram Reel URL** → System acknowledges and requests image
2. **User uploads image** → System acknowledges and requests transformation prompt
3. **User provides prompt** → System confirms all inputs and starts processing
4. **Audio extraction** → "Extracting audio from your reel..."
5. **Prompt analysis** → "Analyzing your transformation request..."
6. **Image generation** → "Creating your transformed image..."
7. **Video creation** → "Generating your animated video..."
8. **Final delivery** → "Your animated video is ready!"

---

## 🔍 Technical Considerations

### **Performance Optimization**:
- Parallel processing where possible
- Efficient error handling
- Resource management

### **Quality Assurance**:
- Input validation at each step
- Output quality checks
- Fallback mechanisms

### **Scalability**:
- Session management for multiple users
- Queue management for processing
- Resource allocation optimization

### **Security**:
- Input sanitization
- API key protection
- User data privacy

---

## 📈 Success Metrics

1. **Functionality**: All three inputs processed correctly
2. **Quality**: Generated videos meet user expectations
3. **Performance**: Processing completed within reasonable time
4. **User Experience**: Clear communication and guidance throughout
5. **Reliability**: Consistent results with minimal errors

---

## 🚀 Implementation Priority

### **Phase 1 (Core Functionality)**:
- Input collection and validation
- Audio extraction
- Basic prompt separation
- Image generation
- Video creation

### **Phase 2 (Enhancement)**:
- Advanced prompt intelligence
- Quality optimization
- Error handling improvements

### **Phase 3 (Distribution)**:
- Cloud storage integration
- Social media posting
- Analytics and monitoring

---

*Document created for Enhanced Aniton Workflow development*
*Last updated: [Current Date]* 