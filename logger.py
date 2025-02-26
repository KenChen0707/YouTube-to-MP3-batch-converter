import logging
import os
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler


def setup_logger():
    # 建立 logger
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)

    # 設定檔案輸出格式
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s %(module)s %(message)s")

    # 確保 logs 目錄存在
    os.makedirs("logs", exist_ok=True)

    # 設定檔案處理器
    file_handler = RotatingFileHandler(
        "logs/app.log",  # 設定日誌檔案路徑
        maxBytes=1024 * 1024,  # 設定日誌檔案最大大小（1MB）
        backupCount=5,  # 設定備份次數
        encoding="utf-8",  # 設定日誌檔案編碼
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 設定 Rich 控制台處理器
    console_handler = RichHandler(
        rich_tracebacks=True,
        show_time=True,
        show_path=False,
        markup=True,
        log_time_format="[%Y-%m-%d %H:%M:%S]",
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
