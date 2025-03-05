# YouTube-to-MP3-batch-converter

一個強大的 YouTube 音樂下載工具，支援批量下載並自動轉換為高品質 MP3。特別適合想要建立本地音樂庫的使用者。

## ✨ 核心功能

- 🎵 批量下載 YouTube 音樂
- 🔄 自動轉換為 MP3（256kbps 高品質）
- 🏷️ 自動嵌入音樂標籤
- 🖼️ 自動嵌入專輯封面
- ⚡ 支援並行下載（預設 10 個同時下載）
- 📝 自動記錄下載歷史
- 📊 即時顯示下載進度
- 📅 依日期自動整理下載檔案

## 🚀 快速開始

### 系統需求
- Python 3.12+
- Poetry（Python 套件管理工具）
- FFmpeg

### 安裝步驟

1. **安裝 Python**
   - 從 [Python 官網](https://www.python.org/downloads/) 下載並安裝

2. **安裝 Poetry**
   ```bash
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
   ```

3. **安裝 FFmpeg**
   - 使用 Chocolatey：
   ```bash
     choco install ffmpeg
     ```
   - 或從 [FFmpeg 官網](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z) 下載

4. **下載並設置專案**
   1. 下載專案
   ```bash
   git clone https://github.com/KenChen0707/YouTube-to-MP3-batch-converter.git
   ```

   2. 移動至專案資料夾
   ```bash
   cd YouTube-to-MP3-batch-converter
   ```

   3. 安裝依賴
   ```bash
   poetry install
   ```

## 💡 使用方法

1. **設定下載清單**
   - 複製範例檔案：
      ```bash
      cp songs.example.json songs.json
      ```
   - 編輯 `songs.json`：
     ```json
     {
         "Pending": {
             "周杰倫": [
                 "稻香",
                 "告白氣球"
             ]
         },
         "Downloaded": {}
     }
     ```

2. **執行下載**
   - 雙擊 `run.bat`
   - 或在終端機執行：
     ```bash
     poetry run python main.py
     ```

3. **查看結果**
   - 下載的音樂會自動存放在 `~/Downloads/Music_YYYYMMDD/` 目錄
   - 程式執行日誌儲存在 `logs/app.log`

## ⚙️ 進階設定

- **下載目錄**：預設為 `~/Downloads/Music_YYYYMMDD/`，可在 `main.py` 中修改 `download_dir` 變數
- **並行下載數**：預設為 10，可在呼叫 `download_songs()` 時透過 `max_workers` 參數調整
- **音訊品質**：預設 256kbps，可在 `download_single_song()` 函式中的 `ydl_opts` 修改

## 📝 注意事項

- 確保網路連線穩定
- 預留足夠硬碟空間
- 遵守 YouTube 服務條款
- 尊重著作權規定

## 🤝 貢獻指南

歡迎提交 Issue 或 Pull Request 來改善專案！

## 📄 授權條款

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 檔案

## 👤 作者

ProMaker <rocker896@gmail.com>