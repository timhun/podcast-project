# Podcast 專案進度

## 2025-09-27
### 已完成
- 配置本地 Ubuntu 環境：
  - 安裝核心工具（gcc 13+, FFmpeg，libopenblas-dev）。
  - 安裝 Docker 和 Docker Compose，驗證容器運行正常。
  - 初始化 Git 儲存庫，創建 `.gitignore` 和 `progress.md`，修復 GitHub 推送身份驗證問題（使用 PAT 或 SSH）。

### 待辦事項
- 設置 Python 3.12 虛擬環境，安裝 Podcast 核心套件（elevenlabs、langchain 等）。
- 安裝 Cursor，配置 Python 和 Docker 擴充。
- 設置 Supabase 資料庫，準備儲存原始資料與 metadata。
- 撰寫簡單爬蟲腳本，測試 YouTube API 資料收集。
- 初始化 Windmill 工作流，模擬每日定時任務。

### 問題與解決
- **問題**：Git 推送失敗（`Invalid username or token`）。
- **解決**：生成 GitHub PAT，更新遠端 URL，或改用 SSH 密鑰。