from loguru import logger

from .config import LOG_DIR
from .tg_bot import App

logger.add(
    LOG_DIR / "info.log",
    level="INFO",
    rotation="10 MB",
    retention="10 days",
    encoding="utf-8",
)
logger.add(
    LOG_DIR / "error.log",
    level="ERROR",
    rotation="10 MB",
    retention="10 days",
    encoding="utf-8",
)


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
