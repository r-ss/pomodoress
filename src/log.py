import sys
from loguru import logger
from config import config

logger.remove(0)
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{message}</level>",
    colorize=True,
    backtrace=True,
    diagnose=True,
)
logger.add(
    config.LOG_FILE_PATH,
    rotation="3 MB",
    retention="10 days",
    format="{time} {level} {message}",
)


def log(message: str, level: str = "info") -> None:
    if level == "debug":
        logger.debug(message)
    if level == "info":
        logger.info(message)
