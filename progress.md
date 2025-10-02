# Podcast 專案進度

## 2025-09-27
### 已完成
- 配置本地 Ubuntu 環境：
  - 安裝核心工具（gcc 13+, FFmpeg，libopenblas-dev）。
  - 安裝 Docker 和 Docker Compose，驗證容器運行正常。
  - 初始化 Git 儲存庫，創建 `.gitignore` 和 `progress.md`，修復 GitHub 推送身份驗證問題（使用 PAT 或 SSH）。

## 2025-09-30
### 已完成
- 設置 Supabase 資料庫，創建 `raw_data`、`processed_data`、`metadata` 表，驗證連線正常。
- 撰寫 `youtube_crawler.py`，成功抓取 5 筆 YouTube 投資影片資料並存入 Supabase。
- 初始化 Windmill，運行簡單工作流，模擬每日定時任務。

### 待辦事項
- 撰寫 TTS 腳本，使用 ElevenLabs 或 Edge-TTS 生成 Podcast 音檔。
- 配置 Google Cloud VM，部署爬蟲與工作流。
- 測試 RSS Feed 生成，驗證 Podcast 發佈流程。
- 撰寫內容生成腳本（LLM 稿件生成與審查）。
- 設置 Grafana 或 Telegram 監控。

### 問題與解決
- **問題**：Git 推送失敗（`Invalid username or token`）。
- **解決**：生成 GitHub PAT，更新遠端 URL，或改用 SSH 密鑰。