# Podcast Project Progress

     ## Project Overview
     This project aims to develop an AI-driven automated investment podcast POC, focusing on data collection and operational automation. The setup includes a cloud-based development environment (Google VM + Windmill + Supabase) and a local Ubuntu 24.04+ environment optimized for AI quantitative trading development. Key tools include core development tools (gcc, FFmpeg), containerization (Docker), code editor (Cursor/VS Code), Python environment (Python 3.12 with `uv`), and version control (Git).

     ## Progress Log

     ### Initial Setup (Rounds 1-4)
     - **Core Tools**: Installed gcc, FFmpeg, and other essentials for compilation and media processing.
     - **Containerization**: Set up Docker and `docker-compose.yml` for Windmill and Postgres services.
     - **Version Control**: Initialized Git repository, fixed GitHub push issues, and set up `progress.md`.
     - **Python Environment**: Installed Python 3.12 with `uv` for fast package management.
     - **Code Editor**: Configured Cursor for AI-assisted coding.
     - **Supabase**: Installed `supabase` (2.20.0) and configured `.env` with `SUPABASE_URL` and `SUPABASE_KEY`.
     - **YouTube API**: Generated and configured YouTube API key.

     ### Database and Windmill Setup (Rounds 9-19)
     - **Windmill Data**: Rebuilt `windmill-data` volume with correct permissions (`windmill:1000`).
     - **Postgres**: Switched to Postgres 16, configured `DATABASE_URL` for Windmill.
     - **Windmill UI**: Fixed `users` table, logged into `http://localhost:8000` as admin.
     - **Environment Variables**: Set up `u/admin` and `u/windmill` variables in Windmill UI, including `YOUTUBE_API_KEY`, `SUPABASE_URL`, and `SUPABASE_KEY`.

     ### Script Development (Rounds 25-43)
     - **youtube_crawler_script**: Created script to fetch YouTube videos (search term: "investment QQQ") and store in Supabase `raw_data` table.
     - **Issues Fixed**:
       - Resolved `PermissionError` by correcting `whoami` to `windmill` user (UID 1000:1000).
       - Fixed environment variable loading issues by mapping `~/podcast-project/.env` to `/app/project/.env`.
       - Corrected script indentation and ensured `load_dotenv('/app/project/.env')` for reliable variable access.
     - **Success (2025-09-29)**: Ran `youtube_crawler_script` successfully, outputting `{"status": "Fetched and stored 5 videos"}`. Confirmed environment variables loaded correctly in container via `python3 -c` test.

### Workflow and Scheduling (Round 48-49, 2025-09-30)
- **data_collection Workflow**: Fixed `DefaultCredentialsError` in `data_collection` by ensuring correct reference to `u/admin/youtube_crawler_script` and proper environment variable loading (`YOUTUBE_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`).
- **Success**: Ran `data_collection` workflow successfully, outputting `{"status": "Fetched and stored 5 videos"}`.
- **Scheduling**: Set daily schedule at 04:00 (Asia/Taipei) for `data_collection`.
- **Next Steps**:
  - Verify Supabase `raw_data` table for correct data storage.
  - Confirm daily schedule execution.
  - Ensure auto-start on laptop reboot (configured in Round 46).

     ## Environment Details
     - **OS**: Ubuntu 24.04+
     - **Project Directory**: `~/podcast-project`
     - **Virtual Environment**: `podcast-env` (Python 3.12, `uv`)
     - **Docker Services**: Windmill (port 8000), Postgres (port 5432)
     - **Supabase**: Project ID `aynwxbozwlftwurmylkv`, `raw_data` table
     - **YouTube API**: Key configured, verified functional
     - **Windmill**: Community Edition v1.392.0, running as `windmill` user

     ## Last Updated
     2025-09-29 20:03 CST