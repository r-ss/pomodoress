import sys
from loguru import logger
from config import config

logger.remove(0)
logger.add(
    sys.stderr,
    level=config.LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{message}</level>",
    colorize=True,
    backtrace=True,
    diagnose=True,
)
logger.add(
    config.LOG_FILE_PATH,
    level=config.LOG_LEVEL,
    rotation="3 MB",
    retention="10 days",
    format="{time:YYYY-MM-DD at HH:mm:ss} {level} {message}",
)


def log(message: str, level: str = "info") -> None:
    if level.lower() == "debug":
        logger.debug(message)
    if level.lower() == "info":
        logger.info(message)
    if level.lower().startswith('warn'):
        logger.warning(message)
