# Podcast Project Progress

## Project Overview
- Objective: Build an AI-driven automated investment podcast system.
- Components:
  - Local: Ubuntu 24.04+ + Docker + Windmill + PostgreSQL (Supabase alternative) + Python (supabase-test-env) + Cursor.
  - Cloud: Google Cloud VM (bbm-ai-2330, IP: 35.212.255.243) + Windmill + Supabase.
- Tools:
  - Core Dev Tools: gcc, FFmpeg, curl.
  - Containerization: Docker for isolated environments.
  - Code Editor: Cursor for AI-assisted coding.
  - Python Env: Python 3.12 with uv package manager.
  - Version Control: Git for code tracking.

## Milestones
1. **Environment Setup** (Completed):
   - Local: Configured Ubuntu 24.04+, supabase-test-env, Git, Docker, Cursor.
   - Repository: Cloned podcast-project, set up .env with Supabase and YouTube API keys.
   - Basic Postgres: Configured local PostgreSQL for Supabase alternative.

2. **Local First Setup** (Completed 2025-10-15):
   - Installed core dev tools (gcc, FFmpeg).
   - Set up containerization with Docker for Windmill and PostgreSQL.
   - Initialized Git and recorded progress.md.

3. **Python Environment & LLM Content Generation** (Completed 2025-10-16):
   - Installed Python 3.12 and uv, set up supabase-test-env with dependencies.
   - Developed llm_content_generator.py for LLM-based script generation.
   - Configured Windmill workflow with notification script.

4. **TTS and RSS Generation** (Completed 2025-10-17):
   - Implemented generate_podcast_audio.py using gTTS for audio generation.
   - Fixed AttributeError in send_notification.py by handling None audio_result.
   - Added rss_generator.py to create Podcast RSS feed.
   - Updated workflow to include TTS, RSS, and notification.

5. **POC Completion** (Completed 2025-10-17):
   - Tested full workflow (script, audio, RSS, notification).
   - Optimized RSS with public URL for cloud deployment.
   - Documented final POC results.

6. **Cloud Deployment with Supabase** (Completed 2025-10-19):
   - Deployed Windmill to Google Cloud VM (bbm-ai-2330, IP: 35.212.255.243).
   - Migrated minimal dataset to Supabase free tier using Python client to avoid SQL Editor limits.
   - Fixed Google Cloud authentication scopes issue for SSH and firewall configuration.
   - Resolved SSH host key and scp permission issues for file transfer.
   - Configured local and Google Cloud firewalls for SSH (tcp:22) and Windmill (tcp:8000).
   - Cleaned up unnecessary files (e.g., node_modules, *.js) using .gitignore and rsync.
   - Configured Windmill DATABASE_URL to use Supabase PostgreSQL (aynxwbozwlftwurmylkv).
   - Switched to local PostgreSQL due to persistent Supabase connection issues (IPv6 or firewall).
   - Fixed "wmill: executable file not found" error by correcting command to "windmill".
   - Resolved "invalid input value for enum job_kind: singlescriptflow" by clearing PostgreSQL data volume.
   - Fixed "Address already in use (os error 98)" by terminating conflicting processes and ensuring port 8000 availability.
   - Verified Supabase connection for data queries using Python client.
   - Deployed scripts and workflow, verified full workflow on cloud environment with local PostgreSQL and Supabase for data queries.

## Next Steps
- Resolve Supabase connection for Windmill by addressing IPv6 or firewall issues.
- Publish audio and RSS files via GitHub Pages.
- Test cloud workflow stability and monitor Supabase limits.
- Submit Podcast to platforms (e.g., Spotify, Apple Podcasts).