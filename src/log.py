import sys

from loguru import logger

from config import config

logger.remove(0)
logger.add(sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{message}</level>", colorize=True)
logger.add(
    config.LOG_FILE_PATH,
    level=config.LOG_LEVEL,
    rotation="1 MB",
    retention="10 days",
    format="{time:YYYY-MM-DD at HH:mm:ss} {level} {message}",
)


def log(message: str, level: str = "info") -> None:

    match level.lower():
        case "debug":
            logger.debug(message)
        case "warn":
            logger.warning(message)
        case "warning":
            logger.warning(message)
        case "error":
            logger.error(message)
        case _:
            logger.info(message)
