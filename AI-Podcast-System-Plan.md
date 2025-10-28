# AI 投資 Podcast 系統企畫書 v1.0  
（POC → 試營運 → 正式營運）

作者：Tim  
狀態：v1.0  
日期：2025-10-28  
定位：此文件是本專案的「唯一事實來源 (single source of truth)」。後續所有調整、需求變更、基礎架構改動，一律回寫本文件。


---

## 1. 任務宣言（Mission Statement）

打造一個可持續運作、低成本、高可信度的 AI 投資資訊系統，  
能夠**每日自動**產生一集「清晰、具邏輯、能被一般投資人採用」的投資內容，並同步發布為：

- Podcast (Apple / Spotify)
- Markdown 報告（策略重點、風險、績效數據）
- 未來短影音 / YouTube 長版內容

重點是「每日可以上架」，而不是「偶爾產出一次漂亮 Demo」。


---

## 2. 產品定位（Positioning）

### 2.1 我們是什麼
> 「AI 財經研究團隊的每日投研員。」

系統每天做三件事：
1. 從公開來源擷取投資策略（YouTube、網站、宏觀報告）
2. 轉成可執行的投資邏輯，並用歷史 QQQ / SPY 做風險驗證
3. 產生一則投資摘要，用人話說明誰適合、何時適用、風險在哪裡

### 2.2 使用者價值主張
- 對「年輕想成長型報酬」的投資人：  
  提供高波動策略，但清楚給出止損、資金配置上限。
- 對「退休或保守」投資人：  
  提供風險可控、下跌分批加碼、長抱 ETF 的配置邏輯。

### 2.3 更新頻率
- 每天產 1 集
- 內容長度依階段：
  - POC：文字／講稿即可
  - 試營運：3 分鐘音檔（低製作）
  - 正式營運：7 分鐘完整節目 + 圖表/截圖視覺化


---

## 3. 階段性目標

### 3.1 POC 階段（驗證階段）
**目標**
- Pipeline 走得完（資料 → PK → 講稿 → mp3 → 報告 .md）
- 不追求聲音情緒、不追求品牌視覺
- 產出一個「我願意公開給朋友聽」的 demo 級內容

**成功條件**
- 每日自動跑出：
  - `episode_YYYY-MM-DD.md`
  - `episode_YYYY-MM-DD_script.txt`
  - （可選）`episode_YYYY-MM-DD.mp3`
- `progress.md` 每天自動 append 一段日誌（收集了什麼、PK 結果、產出什麼）

### 3.2 試營運階段（內測）
**目標**
- 內容穩定上架 Apple Podcast / Spotify
- 片長約 3 分鐘
- 逐漸有「聲音人格」與節目風格
- Telegram / Slack 自動推播每日主題

**成功條件**
- 可以穩定對外發佈（私密 RSS or 封閉頻道）
- Token 成本 / API 成本固定在允許範圍（Groq / Gemini / GPT 分攤）
- Supabase / 雲端 Postgres 成為唯一交易資料庫（筆電 & 桌機可共同維運）

### 3.3 正式營運階段（公開頻道 / 對外）
**目標**
- 7 分鐘完整節目
- 回測績效指標、風險敘述、投資人適用情境全都規格化
- 每週自動產出「策略勝率報告」（勝率、回撤、報酬）

**成功條件**
- 可以對外宣稱「這檔節目每天更新，基於透明量化流程，不販賣明牌，只提供風險-報酬邏輯」
- 有明確的節目分段（開場 → 短線策略 → 長線策略 → 風險聲明 → 結語）
- 可擴展到台股/ETF/退休資產配置等新市場


---

## 4. 系統架構總覽（高層圖）

流程每天跑一輪：

1. **Source Registry (資料來源名單)**
   - 我們允許哪些來源餵進來？
   - 例如：特定 YouTube 頻道、ETF 策略部落格、基金經理人訪談、FRED 宏觀數據

2. **Data Collector (蒐集器)**
   - 抓到標題 / 內文 / 時間戳記
   - 存進 Postgres: `raw_content`
   - 不需要 LLM

3. **Pre-Filter & Tagging (預篩 / 標記)**
   - 用本地 Ollama 模型清洗文本，抽出策略重點
   - 判斷是否為「具體可執行策略」
   - 標成短線 or 長線
   - 寫進 `candidate_strategy`

4. **Strategy PK Engine (PK / 簡易回測)**
   - 用 QQQ / SPY 過去一年做模擬
   - 計算 total_return%、max_drawdown%、win_rate%
   - 選出短線冠軍 / 長線冠軍
   - 寫進 `pk_result`

5. **Strategist Agent（策略顧問解釋）**
   - 用雲端 LLM（GPT / Gemini / Groq）把數據翻成人話
   - 說明誰適用、風險在哪、保守 vs 激進版本
   - 回寫 `summary_for_host`（pk_result 欄位）

6. **Narrator Agent（播客講稿生成）**
   - 生成口語化逐字稿 + Markdown 報告
   - 產出：
     - `episode_YYYY-MM-DD_script.txt`
     - `episode_YYYY-MM-DD.md`

7. **TTS & Publish**
   - 用開源 TTS (Piper / Coqui XTTS) 生 mp3
   - 上傳到 Apple Podcast / Spotify feed
   - 推播到 Slack / Telegram

8. **進度記錄**
   - 這一輪發生了什麼，自動 append 到 `logs/progress.md`，並 `git push`


---

## 5. 模組拆解與資料流（POC 定義版）

### 5.1 Stage 0. Source Registry（資料來源登記表）

**任務**  
定義「合法輸入來源」，避免垃圾資訊。

**格式**  
`sources.json` （版本控在 GitHub）：
```json
{
  "source_id": "ryan_trading_channel",
  "title": "Ryan - Day Trading QQQ",
  "type": "youtube",
  "priority": 0.9,
  "category_hint": "短線/動能",
  "url": "https://youtube.com/..."
}
```

**為什麼這層重要**  
- 將來擴充到 50 個來源時，我們可以快速停用一個來源（priority=0）而不用改 code。
- 也作為合規證據：「節目內容都來自公開來源」。

---

### 5.2 Stage 1. Data Collector（資料蒐集器）

**任務**  
每天抓來源內容（標題/描述/逐字稿/發布時間），寫入 DB。

**做法（POC）**
- YouTube: yt-dlp / Transcript API 取得標題、描述、(字幕可得則拿字幕)、發布時間
- 網站/文章: requests + BeautifulSoup / RSS 抓正文
- FRED / 宏觀：API 抓最新指標摘要（之後可進一步用於長線策略情境）

**資料寫入 `raw_content` 表**
欄位：
- `id` (uuid)
- `source_id`
- `published_at`
- `title`
- `raw_text` (原始逐字稿或文章內文)
- `url`
- `collected_at`
- `status` = "new"

**LLM？**
- 不需要 LLM，純抓資料。

**其他**
- 一旦 collector 成功跑完，會自動在 `logs/progress.md` append 當天「Data Collector」段落，並 `git commit`。

---

### 5.3 Stage 2. Pre-Filter & Tagging（預篩＋分類）

**目的**  
不是每個影片/文章都值得分析。我們要選出「今天可能真的有交易價值」的前 5 策略。

**分析目標**
1. 這是不是一個可執行策略？  
   - 還是只是主播在發牢騷、喊盤或講大盤情緒？
2. 這是短線？還是長線？  
   - 短線 = 0DTE / 槓桿 / 幾天內進出 / 明確進出場
   - 長線 = 資產配置 / 分批加碼 / 再平衡 / 抗回撤
3. 熱度 + 新鮮度評分  
   - 熱度（標題情緒、觀看數/按讚比）
   - 新鮮度（發布時間距今天的天數）

**技術**
- 使用本地 Ollama (gpt-oss 類模型) 解析 `raw_text`，回傳 JSON：
  - `is_strategy`: true/false  
  - `style`: "short_term" | "long_term" | "unclear"  
  - `core_claim`: 策略主張一句話  
  - `entry_rule` / `exit_rule`: 進出條件（如有）  
  - `risk_control`: 止損/資金控管（如有）
- 手刻分數：
  - `score_heat`
  - `score_recency`
  - `score_final = 0.6*heat + 0.4*recency`

**寫入 `candidate_strategy`**
欄位：
- `id`
- `raw_content_id`
- `is_strategy`
- `style`
- `core_claim`
- `entry_rule`
- `exit_rule`
- `risk_control`
- `score_heat`
- `score_recency`
- `score_final`
- `status` ("selected" / "dropped")

**產出**
- 依 `score_final` 排序，選出 Top 5，標為 `selected`。

**progress.md**
- Append 本日入選的策略摘要，像：
  - stg_202 長線: "逢10%下跌就分批加碼SPY 20%資金"

---

### 5.4 Stage 3. Strategy PK Engine（策略 PK & 簡易回測）

**目標**
決定「今天誰登場」。  
不是全 PK，而是「短線組互打出一個王」、「長線組互打出一個王」。

**步驟**
1. 將當天的短線候選互相比  
2. 將當天的長線候選互相比  
3. 各組挑出冠軍  
4. 如果短線冠軍太糟（或風險太高不適合講），那只講長線；反之亦然

**回測（POC 簡化）**
- 使用 QQQ / SPY 過去一年 OHLCV，本地用 yfinance 取得並快取為 CSV
- 支援策略型態：
  - 均線交叉（例：5EMA > 20EMA 進場）
  - RSI 反轉（RSI<30 買、RSI>50 出）
  - 逢低加碼 / 分批佈局（長線）
  - 固定資產配置（60% QQQ + 40% 現金，跌到 X% 再加碼 Y%）
- 回測產出三個指標：
  - `total_return_pct`
  - `max_drawdown_pct`
  - `win_rate_pct`（短線才計算，長線可為空）

**寫入 `pk_result`**
欄位：
- `id`
- `candidate_strategy_id`
- `symbol_tested` ("QQQ" / "SPY")
- `period` ("1y")
- `total_return_pct`
- `max_drawdown_pct`
- `win_rate_pct` (nullable)
- `style`
- `summary_for_host`（暫時空，下一階段由 Strategist Agent 補）
- `rank_in_style` (1=冠軍)
- `status` ("winner" / "loser")

**progress.md**
- Append 當天冠軍與它的指標。

---

### 5.5 Strategist Agent（策略顧問敘事層）

**角色**
- 把冷冰冰的回測數據變成人話
- 告訴觀眾/聽眾「這策略適合誰？它在什麼市況下穩？你最大的風險是什麼？」

**由誰執行**
- 使用雲端 LLM（GPT / Gemini / Groq 任一可用額度）
  - 這層屬於「高智商、要合規語氣」的敘事
  - token 花費屬於比較貴的那種 → 我們只跑在冠軍策略上，而不是所有候選

**產出**
- 補上 `pk_result.summary_for_host`，內容包含：
  - 適合族群（年輕進攻 / 退休防禦）
  - 假設前提（例如「假設市場維持區間震盪」）
  - 保守版操作建議（20%倉位嘗試）
  - 激進版操作建議（高風險）

---

### 5.6 Narrator Agent（節目講稿／Markdown 報告）

**角色**
把冠軍策略（含 summary_for_host）拼出兩份成品：

1. `episode_YYYY-MM-DD.md`
   - 標題（今日主題）
   - 短線 or 長線標記
   - 策略邏輯（entry/exit/risk_control）
   - 回測指標表格：total_return%、max_drawdown%、win_rate%
   - 投資人適配族群
   - 免責聲明

2. `episode_YYYY-MM-DD_script.txt`
   - 主持人逐字稿（口語、可直接丟進 TTS）
   - 長度：
     - POC：可以是 2~3 分鐘
     - 試營運：3 分鐘穩定
     - 正式營運：7 分鐘，有開場/收尾/CTA

**由誰執行**
- Narrator Agent 可以使用雲端 LLM（GPT / Gemini）來寫口語化腳本，直到本地模型表現夠好為止。
- 未來可以嘗試在本地 fine-tune（可考慮 QLoRA 等技術）。

---

### 5.7 TTS & Publish（語音合成與發佈）

**POC**
- 使用開源 TTS (Piper / Coqui XTTS) 直接產生一段中文語音
- 檔名：`episode_YYYY-MM-DD.mp3`
- 不強求聲線完美，只要聽得清楚

**試營運**
- 用較穩定音色（可在 Windows 主機上產生正式音檔）
- 自動發布到現有 Apple Podcast / Spotify feed
- 自動把當日主題、風險摘要貼到 Slack / Telegram 通知群

**正式營運**
- 7 分鐘內容
- 自動產封面 PNG（雲端 LLM 文字 + image model），上傳 YouTube 變成長版影音
- 每週整理「策略勝率週報」


---

## 6. 短線 vs 長線 的分類規則（供 LLM 使用）

**短線 (short_term) 判定標準（命中任一就算短線）**
- 有明確進場 / 出場點，持倉週期 ≤ 5 個交易日  
  範例：「當天跌破開盤價 1% 就空，反彈 0.5% 回補」
- 講到 0DTE、槓桿 ETF、當沖、快速止損

**長線 (long_term) 判定標準（命中任一就算長線）**
- 資產配置 / 分批加碼 / 再平衡
- 週期 ≥ 1 個月
- 對象是退休金、長抱 ETF、降低波動
- 強調「抗回撤」、「下跌攤平」、「配息再投入」

**同時出現短線跟長線？**
- 同一段來源可能講日內 0DTE，又講退休長抱配置  
- 我們允許切成兩個獨立策略來記錄（兩筆 candidate_strategy）


---

## 7. 執行/發佈環境與基礎建設（Infra / DevOps）

### 7.1 跨裝置開發模型
- Windows PC（家裡）：高算力、TTS 正式產線、發布 Podcast
- Ubuntu 筆電（外出）：可跑完整 pipeline、但 mp3 可以是草稿級語音

### 7.2 程式碼儲存
- 全部程式碼放在 GitHub repo
- 每次 daily run 之後，程式自動：
  - append 到 `logs/progress.md`
  - `git add`, `git commit -m "daily run <date>"`, `git push`
- 代表 `progress.md` 是營運日誌 + 研發日誌的混合紀錄，也是將來募資/對內稽核用素材

### 7.3 資料庫
- 使用雲端 PostgreSQL / Supabase 免費額度  
  - 儲存 `raw_content`, `candidate_strategy`, `pk_result`
  - 兩台機器都連同一個 DB，狀態永遠一致
- 未來正式營運：
  - 可以把敏感欄位（尚未播出的策略細節）搬回自架 Postgres（或 NAS）

### 7.4 模型推理層
- **本地 Ollama (gpt-oss)**：  
  - Analyst Agent：抓 entry/exit/risk_control，分類短線/長線
- **雲端 LLM (Groq / Gemini / GPT)**：  
  - Strategist Agent：專業投顧式解釋，風險揭露
  - Narrator Agent：人聲口吻腳本
- Token 成本控管策略：  
  - 把重推理（Narrator / Strategist）只跑在「今日勝出策略」，而不是所有候選

### 7.5 大檔案 / 成品儲存
- 使用 Google Drive（1TB 空間）同步：
  - `/marketdata/`：QQQ / SPY 歷史資料 CSV（回測用）
  - `/episodes/`：每日 mp3、封面 PNG、稿件快照
  - `/clips/`：未來短影音切片
- Windows 與 Ubuntu 都 mount 這個 Drive → 兩邊都拿得到最新音檔 / 歷史行情

### 7.6 Secrets / API Keys
- Repo 內會提供 `.env.example`
- 真正的 `.env`（含 Supabase、Postgres、Groq、Gemini、GPT、FRED、Gmail App Password、Slack Bot Token、Telegram Bot Token）只存在在各裝置本地，不進 Git
- Python 用 `python-dotenv` 載入

---

## 8. 日誌與監控

### 8.1 `progress.md`（營運 & 開發日誌）
每天跑完 pipeline，系統自動 append 一個 block，格式如下：

#### 樣例：2025-10-28
1. Data Collector  
   - [OK] 抓到 3 個來源（ryan_trading_channel, macro_fund_talk, etf_retirement_show）  
   - raw_content 新增 3 筆 (rc_101, rc_102, rc_103)

2. Pre-Filter & Tagging  
   - Analyst Agent (Ollama) 解析完成，產出 candidate_strategy 2 筆  
   - stg_201 短線: "RSI<30買進QQQ，反彈出場"  
   - stg_202 長線: "逢10%下跌就分批加碼SPY 20%資金"

3. Strategy PK Engine  
   - stg_201 on QQQ 1y:  
     - total_return: +14.2%  
     - max_drawdown: -18.5%  
     - win_rate: 61%  
   - stg_202 on SPY 1y:  
     - total_return: +9.1%  
     - max_drawdown: -7.4%  
     - win_rate: n/a (長線)  
   - 今日主打策略: stg_202 長線防禦型配置

4. Narrator Agent  
   - 產生 podcast script: `episode_2025-10-28_script.txt`  
   - 產生報告: `episode_2025-10-28.md`

5. TODO / Blockers  
   - Piper TTS 中文音色仍然偏機械  
   - Backtest 模組目前只支援 均線 / RSI / 分批加碼 三種策略  
   - 尚未整合 Telegram 推播

---

### 8.2 Slack / Telegram 通知
- 試營運階段開始：  
  - 每天自動貼一則摘要：「今日策略主題、適合族群、最大風險」  
  - 讓核心聽眾（或內部測試成員）可以用聊天工具感受內容價值

---

## 9. Roadmap（POC → 試營運 → 正式營運）

### 9.1 POC（現在～近期）
- 完成以下腳本的最小可行版本：
  1. `collector.py`  
     - 抓來源 → 寫 `raw_content` → append progress.md
  2. `analyze_strategy_ollama.py`  
     - 本地 Ollama 萃取策略、短/長線分類 → 寫 `candidate_strategy`
  3. `pk_engine.py`  
     - 做回測、算績效 → 寫 `pk_result`
  4. `generate_script.py`  
     - Strategist Agent（雲）+ Narrator Agent（雲）  
     - 產 `.md` + `.txt`
  5. `tts.py` (可選)  
     - Piper / Coqui XTTS 產出 `.mp3`

- 所有步驟都 append 進 `logs/progress.md`，並自動 `git push`

- DB: 先用 Supabase / 雲 Postgres，兩台機器共用  
- 成品檔案(mp3/CSV等): 放 Google Drive，同步兩台機器  
- LLM:  
  - 本地：Analyst Agent  
  - 雲端：Strategist / Narrator Agent

**POC 交付物**
- `episode_YYYY-MM-DD.md`  
- `episode_YYYY-MM-DD_script.txt`  
- (選配) `episode_YYYY-MM-DD.mp3`  
- 最新版 `logs/progress.md`

---

### 9.2 試營運（內測 / 小規模聽眾）
- 每天自動生成 3 分鐘音檔
- 自動上傳到 Apple Podcast / Spotify（你已經有節目管道，可以直接覆用名稱與 feed）
- Slack / Telegram 自動推播「今日策略摘要 + 風險提醒」
- 封面 PNG 簡單自動化（標題 + 日期），並開始嘗試上傳 YouTube 當作音頻版（靜態圖+音檔）

**額外重點**
- 多雲 LLM 成本分攤（Groq / Gemini / GPT），避免單一 API 被用爆
- 保留所有生成內容（稿、音檔、回測紀錄）到 Google Drive 歸檔
- 擴充 PK Engine 指標（Sharpe-like風格 / 最大連虧天數 等）

---

### 9.3 正式營運（公開上架 / 日更品牌）
- 節目長度提升至 7 分鐘，包含：
  - 短線策略一則
  - 長線策略一則
  - 「誰適合／誰不適合」清楚講白
  - 市場情緒／風險總結
- 每週輸出「策略勝率報告」（Markdown + 試算表 + 視覺圖表 .png）
- 自動切片成 Shorts / Reels：
  - 「今天 1 分鐘重點」or「本週最大風險提醒」
- 建立「免責聲明模板」並固定附在口播與摘要文稿末段

---

## 10. 風險與後續要解的問題

1. **合規/風險聲明**
   - 我們不是提供個別投資建議，而是「策略邏輯 + 風險教育」。
   - 在 Narrator Agent 的稿尾固定加上免責聲明。

2. **聲音一致性**
   - Piper / Coqui XTTS 的音色在 Windows 與 Ubuntu 可能略有不同。
   - 試營運階段建議「正式成品音檔只在 Windows 產生」，筆電版本供內部檢聽。

3. **資料來源版權**
   - 系統只能引用公開資訊，不可逐字重播他人付費內容。
   - Pre-Filter / Analyst Agent 必須做「摘要」而不是「抄錄全文」。

4. **DB 存在雲端**
   - 現階段（POC / 試營運）OK，因為內容都是公開策略衍生品。
   - 正式營運可將「未播出的策略明細」遷回自管 DB 或移除敏感細節。

5. **Token 成本控制**
   - Strategist / Narrator Agent 僅運行在「今日最終上節目的冠軍策略」，而非全部候選，避免爆成本。

---

## 11. 行動項目總表（下一步）

1. 建 GitHub repo：  
   - `/src/collector.py`  
   - `/src/analyze_strategy_ollama.py`  
   - `/src/pk_engine.py`  
   - `/src/generate_script.py`  
   - `/src/tts.py`  
   - `/logs/progress.md`  
   - `/sources.json`

2. 建 Supabase / 雲端 Postgres：  
   - 建立三張表：`raw_content`, `candidate_strategy`, `pk_result`

3. 設定 `.env.example`（不含真 Key）  
   - SUPABASE_URL  
   - SUPABASE_KEY  
   - GROQ_API_KEY / GEMINI_API_KEY / OPENAI_API_KEY  
   - FRED_API_KEY  
   - GMAIL_APP_PASSWORD  
   - TELEGRAM_BOT_TOKEN / SLACK_BOT_TOKEN

4. 把 QQQ / SPY 歷史資料 CSV 放到 Google Drive `/marketdata/`

5. 設定 progress.md 自動 append + git push，在每日 pipeline 結束時執行

6. 先跑一輪 POC，產出第一個 episode_YYYY-MM-DD.md。


---

## 12. 最後一句話

本系統不是一個「影音生成器」，
而是一個「每日自動跑研究、驗證風險、消化給一般人聽」的投資研究助理。

POC 階段的唯一 KPI：  
**每天確實能產出一集有邏輯的投資說明，並留下完整稽核紀錄（progress.md）。**

之後的一切（音質、封面、情緒、品牌）都可以慢慢加。