# YouTube-to-MP3-batch-converter

這是一個用於從 YouTube 批量下載音樂並轉換為 MP3 格式的工具。它支援並行下載多首歌曲，並自動嵌入音樂標籤和專輯封面。

## 功能特點

- 🎵 從 YouTube 批量下載音樂
- 🔄 自動轉換為高品質 MP3 格式（256kbps）
- 📝 自動嵌入音樂標籤資訊
- 🖼️ 自動嵌入專輯封面
- 📊 下載進度和狀態追蹤
- 🚀 支援並行下載，提升效率
- 📁 自動整理下載歷史

## 系統需求

- Python 3.12 或更新版本
- FFmpeg（用於音訊處理）
- Poetry（用於依賴管理）

## 安裝步驟

1. 安裝 FFmpeg（如果尚未安裝）

   ```bash
   # macOS（使用 Homebrew）
   brew install ffmpeg

   # Ubuntu/Debian
   sudo apt update
   sudo apt install ffmpeg

   # Windows（使用 Chocolatey）
   choco install ffmpeg
   ```

2. 克隆專案

   ```bash
   git clone https://github.com/KenChen0707/YouTube-to-MP3-batch-converter.git
   cd YouTube-to-MP3-batch-converter
   ```

3. 使用 Poetry 安裝依賴

   ```bash
   poetry install
   ```

## 使用方法

1. 建立歌曲清單檔案

   將 `songs.example.json` 複製為 `songs.json`，並編輯其中的歌曲資訊：

   ```bash
   cp songs.example.json songs.json
   ```

   `songs.json` 格式範例：
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

2. 執行下載程式

   ```bash
   poetry run python main.py
   ```

   下載的音樂檔案將儲存在 `~/Downloads/Music` 目錄下。

## 設定說明

- 下載目錄：預設為 `~/Downloads/Music`，可在 `main.py` 中修改 `download_dir` 變數
- 並行下載數：預設為 10，可在呼叫 `download_songs()` 時透過 `max_workers` 參數調整
- 音訊品質：預設為 256kbps，可在 `download_single_song()` 函式中的 `ydl_opts` 修改

## 日誌記錄

- 程式執行日誌會儲存在 `logs/app.log`
- 使用 Rich 套件提供彩色終端輸出
- 日誌檔案自動輪替，每個檔案最大 1MB，保留最近 5 個備份

## 注意事項

- 請確保有足夠的硬碟空間
- 下載速度取決於網路連線品質
- 部分影片可能因版權限制無法下載
- 請遵守 YouTube 的服務條款和著作權規定

## 授權條款

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 貢獻指南

歡迎提交 Pull Request 或建立 Issue 來改善這個專案！

## 作者

ProMaker <rocker896@gmail.com> 