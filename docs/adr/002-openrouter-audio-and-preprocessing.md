# ADR 002: OpenRouter Audio API and FFmpeg Preprocessing

## Status
Accepted

## Context

MeetMind needs to convert audio from meeting recordings into transcriptions for further processing. Meeting files come in various formats (MP3, MP4, WebM, etc.) with different audio configurations (stereo, variable bitrates, sample rates). We need a reliable, cost-effective speech-to-text (STT) solution that can handle this variability while maintaining consistent output quality.

Initial research identified several STT providers:
- **AWS Transcribe**: High cost per minute, vendor lock-in
- **Google Speech-to-Text**: Requires quota management, per-request billing
- **OpenRouter**: Offers multiple audio models through unified API, competitive pricing, flexible rate limiting

OpenRouter provides access to multiple audio models (including Deepgram, Whisper, etc.) through a single API, simplifying integration and allowing model switching without code changes.

Additionally, video files require preprocessing before STT processing. Raw video/audio files may have incompatible formats (stereo audio, high sample rates, compressed codecs). Audio preprocessing standardizes input to ensure consistent processing downstream.

## Decision

1. **STT Provider**: Use OpenRouter Audio API for speech-to-text transcription
   - Provides unified access to multiple audio models
   - Competitive pricing with transparent rate limiting
   - API key stored securely in `.env` file
   - Flexible model selection without code changes

2. **Audio Preprocessing**: Implement FFmpeg-based preprocessing layer
   - Convert video/audio files to standardized WAV format
   - Enforce mono channel output (reduces processing overhead)
   - Standardize sample rate to 16kHz (optimal for most STT models)
   - Remove silence and normalize audio levels
   - Asynchronous processing via Celery task queue

3. **Processing Pipeline**: Updated flow from upload to insights
   ```
   Upload → MinIO Storage → Celery Task → FFmpeg Preprocessing → OpenRouter STT → OpenRouter LLM → PostgreSQL
   ```

4. **Temporary File Handling**
   - FFmpeg processes files in `/tmp` directory
   - Automatic cleanup after successful STT submission
   - Cleanup on error to prevent disk space leaks

## Consequences

### Positive
- **Standardized Input**: FFmpeg preprocessing ensures consistent audio format, reducing STT failures
- **Cost Efficiency**: OpenRouter's unified API reduces operational complexity; competitive pricing per-minute
- **Model Flexibility**: Can switch STT models without backend changes (OpenRouter API abstraction)
- **Async Processing**: Celery integration prevents blocking uploads; supports concurrent transcription
- **Scalability**: Horizontal scaling via Celery worker pool; MinIO handles large file storage

### Negative
- **FFmpeg Dependency**: Requires FFmpeg installation on all worker nodes; adds system-level dependency
- **Processing Overhead**: Audio preprocessing adds latency (~10-30s for typical meeting) before STT begins
- **Temporary Storage**: Requires disk space on worker nodes; must monitor cleanup to prevent leaks
- **OpenRouter Rate Limits**: Subject to OpenRouter's rate limiting; may require quota escalation for high volume
- **API Key Security**: Requires secure `.env` management; compromise exposes rate-limited quota

### Security Considerations
- **API Key Management**: Store OpenRouter API key in `.env`; never commit to version control; rotate periodically
- **File Type Validation**: Restrict uploads to known audio/video MIME types (audio/*, video/mp4, video/webm, etc.)
- **File Size Limits**: Enforce maximum 1GB upload limit; prevents disk exhaustion and excessive API costs
- **Temp File Cleanup**: Celery tasks clean up preprocessed files after submission; errors trigger cleanup via finally blocks
- **Access Control**: MinIO buckets configured with least-privilege policies; STT results stored with row-level security

### Migration Path
1. Deploy FFmpeg to worker nodes
2. Update backend requirements.txt with FFmpeg Python bindings (pydub, moviepy, or ffmpeg-python)
3. Implement Celery task for FFmpeg preprocessing
4. Add OpenRouter API client and STT integration
5. Update upload endpoint to trigger preprocessing task
6. Add monitoring/alerting for STT failures and processing latency

## Alternatives Considered

### 1. Direct Upload to STT without Preprocessing
- **Rejected**: Many providers require standardized formats; raw files often fail or produce poor transcriptions
- **Risk**: Higher failure rate, unpredictable quality, increased support burden

### 2. Client-Side Preprocessing (Browser FFmpeg.wasm)
- **Rejected**: FFmpeg.wasm adds ~50MB to bundle; browser-based processing unreliable for large files
- **Risk**: Poor UX for slow networks, inconsistent results across browsers

### 3. AWS Transcribe
- **Rejected**: Higher cost (~$0.02/min vs OpenRouter's $0.01-0.015/min); vendor lock-in
- **Risk**: Increased operational costs, migration difficulty

### 4. Google Cloud Speech-to-Text
- **Rejected**: Quota complexity, credential management overhead
- **Risk**: Rate limiting surprises, additional operational burden

## Next Steps
1. Document OpenRouter API integration in backend README
2. Add FFmpeg installation instructions to deployment guide
3. Create monitoring dashboard for STT latency and error rates
4. Set up alerts for API quota exhaustion
5. Plan quarterly review of STT model performance and cost
