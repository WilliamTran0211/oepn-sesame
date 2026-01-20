from datetime import datetime
from app.utils.file_utils import ensure_dir, get_absolute_path

from .filters import SensitiveDataFilter

date_str = datetime.now().strftime("%Y-%m-%d")

LOG_DIR_STR = "./logs"
LOG_DIR = ensure_dir(LOG_DIR_STR)
LOG_FILE = f"{get_absolute_path(LOG_DIR_STR)}/{date_str}-open-sesame.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "[%(levelname)s] - %(asctime)s - %(name)s - %(message)s",
        },
    },
    "filters": {
        "sensitive_data_filter": {
            "()": SensitiveDataFilter,
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
            "filters": ["sensitive_data_filter"],
        },
        "file": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "filename": LOG_FILE,
            "mode": "a",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "open_sesame_logger": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
}
