import csv
import os

from yt_dlp import YoutubeDL

from logger import setup_logger

# 在程式開始時初始化 logger
logger = setup_logger()


def download_songs_from_csv(file_path):
    """
    從CSV檔案讀取歌手和歌名，然後從YouTube下載為MP3格式。
    CSV格式應該是: 歌手,歌名
    """
    if not os.path.exists("下載的音樂"):
        os.makedirs("下載的音樂")

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                artist = row[0].strip()
                song = row[1].strip()
                download_song(artist, song)
            else:
                logger.warning(f"跳過格式不正確的行: {row}")


def download_song(artist, song):
    """
    使用歌手和歌名從YouTube下載歌曲
    """
    search_query = f"{artist} - {song}"
    output_path = os.path.join("下載的音樂", f"{artist} - {song}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": output_path,
        "noplaylist": True,
        "quiet": False,
        "default_search": "ytsearch",
    }

    logger.info(f"正在搜尋並下載: {search_query}")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{search_query}"])
        logger.info(f"成功下載: {search_query}")
    except Exception as e:
        logger.error(f"下載 {search_query} 時發生錯誤: {e}")


if __name__ == "__main__":
    input_file = input("請輸入含有歌手和歌名的CSV檔案路徑: ")
    if os.path.exists(input_file):
        download_songs_from_csv(input_file)
    else:
        logger.error(f"找不到檔案: {input_file}")
        logger.info("請確保您提供了正確的檔案路徑。")
