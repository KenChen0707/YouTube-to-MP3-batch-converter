import concurrent.futures
import json
import os

from yt_dlp import YoutubeDL

from logger import setup_logger

# 在程式開始時初始化 logger
logger = setup_logger()

# 設定歌曲清單的檔案路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
songs_file = os.path.join(current_dir, "songs.json")

# 設定歌曲下載的資料夾路徑
download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "Music")


def load_songs_from_json() -> list:
    """從 JSON 檔案載入待處理的歌曲清單。

    Returns:
        list: 歌曲清單，格式為 [ { "artist": "歌手", "name": "歌名" }, ... ]。

    Raises:
        Exception: 當檔案讀取或解析失敗時拋出異常。
    """
    song_list = []

    try:
        with open(songs_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)["Pending"]
            # 將 JSON 結構轉換為程式所需的格式
            for artist, songs in json_data.items():
                for song in songs:
                    song_list.append({"artist": artist, "name": song})
    except Exception as e:
        logger.error(f"載入歌曲清單時發生錯誤: {str(e)}")
    finally:
        return song_list


def download_single_song(song: dict):
    """使用歌手和歌名從YouTube下載單首歌曲。

    Args:
        song (dict): 包含歌曲資訊的字典，必須包含 "artist" 和 "name" 兩個鍵值，
            例如: {"artist": "周杰倫", "name": "稻香"}

    Raises:
        Exception: 當下載或轉換過程發生錯誤時拋出。
            可能的錯誤包含：網路連線問題、YouTube影片不存在、轉換格式失敗等。
    """
    # 組合搜尋關鍵字，格式為 "歌手 - 歌名"
    search_query = f"{song["artist"]} - {song["name"]}"
    # 設定輸出檔案路徑，%(ext)s 會被實際的檔案副檔名取代
    output_path = os.path.join(download_dir, f"{search_query}.%(ext)s")

    # 設定 youtube-dl 的下載選項
    ydl_opts = {
        "format": "bestaudio/best",  # 下載最好的音訊格式
        "outtmpl": output_path,  # 輸出的檔案名稱格式
        "noplaylist": True,  # 確保不下載整個播放清單（如果提供的是單個影片）
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",  # 轉換為音訊格式
                "preferredcodec": "mp3",  # 設定音訊格式為 mp3
                "preferredquality": "256",  # 設定音質（256kbps）
            },
            {"key": "FFmpegMetadata"},  # 嵌入影片資訊（標題、藝術家等）
            {"key": "EmbedThumbnail"},  # 嵌入封面圖
        ],
        "writethumbnail": True,  # 下載影片縮圖用於嵌入
    }

    try:
        # 使用 with 語句確保資源正確釋放
        with YoutubeDL(ydl_opts) as ydl:
            # 使用 ytsearch1 限制只搜尋第一個結果
            ydl.download([f"ytsearch1:{search_query}"])
        logger.info(f"成功下載: {search_query}")
    except Exception as e:
        # 記錄下載失敗的錯誤訊息
        logger.error(f"下載 {search_query} 時發生錯誤: {e}")


def download_songs(song_list: list, max_workers: int = 10):
    """並行下載多首歌曲。

    使用 ThreadPool 進行並行下載，可以同時處理多首歌曲的下載任務。
    下載完成的歌曲會自動進行格式轉換和中繼資料嵌入。

    Args:
        song_list (list): 歌曲清單，格式為 [ { "artist": "歌手", "name": "歌名" }, ... ]。
        max_workers (int, optional): 最大同時下載數量。預設為 10。
    """
    # 確保下載資料夾存在
    os.makedirs(download_dir, exist_ok=True)

    total_songs = len(song_list)
    logger.info(f"開始下載 {total_songs} 首歌曲，同時下載數量: {max_workers}")

    # 使用 ThreadPool 進行並行下載
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(download_single_song, song_list)


def move_songs_to_downloaded():
    """將已下載的歌曲從 "Pending" 移動到 "Downloaded" 分類。

    此函式會更新 songs.json 檔案，將所有 "Pending" 中的歌曲
    移動到 "Downloaded" 中，並清空 "Pending" 清單。

    Raises:
        Exception: 當檔案讀取、寫入或 JSON 解析失敗時拋出。
    """
    try:
        # 讀取現有的 JSON 檔案
        with open(songs_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # 取得待處理和已下載的歌曲清單
        pending_songs = json_data["Pending"]
        downloaded_songs = json_data["Downloaded"]

        # 更新下載狀態
        for artist, songs in pending_songs.items():
            if artist not in downloaded_songs:
                downloaded_songs[artist] = []
            for song in songs:
                if song not in downloaded_songs[artist]:
                    downloaded_songs[artist].append(song)

        # 建立新的 JSON 資料結構
        new_json_data = {"Pending": {}, "Downloaded": downloaded_songs}

        # 寫入更新後的資料
        with open(songs_file, "w", encoding="utf-8") as f:
            json.dump(new_json_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"更新歌曲狀態時發生錯誤: {str(e)}")


if __name__ == "__main__":
    # 載入歌曲清單
    song_list = load_songs_from_json()
    if song_list:
        # 下載全部歌曲
        download_songs(song_list)
        # 將已下載的歌曲從 "Pending" 移動到 "Downloaded" 分類
        move_songs_to_downloaded()

        # 顯示完成訊息
        logger.info(f"下載作業已完成，請至 {download_dir} 檢查下載的檔案")
    else:
        logger.error("沒有找到要下載的歌曲，請確認 songs.json 檔案內容是否正確")
