# Podcast Project Progress

## Project Overview
- Objective: Build an AI-driven automated investment podcast system.
- Components:
  - Local: Ubuntu 24.04+ + Docker + Windmill + PostgreSQL (Supabase alternative) + Python (podcast-env) + Cursor.
  - Cloud: Oracle Cloud Free Tier + GitHub Pages.
- Tools:
  - Core Dev Tools: gcc, FFmpeg, curl.
  - Containerization: Docker for isolated environments.
  - Code Editor: Cursor for AI-assisted coding.
  - Python Env: Python 3.12 with uv package manager.
  - Version Control: Git for code tracking.

## Milestones
1. **Environment Setup** (Completed):
   - Local: Configured Ubuntu 24.04+, podcast-env, Git, Docker, Cursor.
   - Repository: Cloned podcast-project, set up .env with Supabase and YouTube API keys.
   - Basic Postgres: Configured local PostgreSQL for Supabase alternative.

2. **Local First Setup** (Completed 2025-10-15):
   - Installed core dev tools (gcc, FFmpeg).
   - Set up containerization with Docker for Windmill and PostgreSQL.
   - Initialized Git and recorded progress.md.

3. **Python Environment & LLM Content Generation** (Completed 2025-10-16):
   - Installed Python 3.12 and uv, set up podcast-env with dependencies.
   - Developed generate_podcast_script.py for LLM-based script generation.
   - Configured Windmill workflow with notification script.

4. **TTS and RSS Generation** (Completed 2025-10-17):
   - Implemented generate_podcast_audio.py using gTTS for audio generation.
   - Fixed AttributeError in send_notification.py by handling None audio_result.
   - Added generate_rss.py to create Podcast RSS feed.
   - Updated workflow to include TTS, RSS, and notification.

5. **POC Completion** (Completed 2025-10-17):
   - Tested full workflow (script, audio, RSS, notification).
   - Optimized RSS with public URL for cloud deployment.
   - Documented final POC results.

6. **Cloud Deployment** (Completed 2025-10-17):
   - Deployed Windmill and PostgreSQL to Oracle Cloud Free Tier.
   - Published audio and RSS files via GitHub Pages.
   - Automated upload to GitHub Pages with upload_to_docs.py.

## Next Steps
- Monitor cloud performance and optimize costs.
- Expand content with additional data sources (e.g., Twitter sentiment analysis).
- Submit Podcast to platforms (e.g., Spotify, Apple Podcasts).