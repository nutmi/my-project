import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")


# Logging configuration
def setup_logging(name):
    logger = logging.getLogger(name)

    # Check if handlers are already added (to prevent duplicate logging)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        # Create formatters
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")

        # File handler (rotating file handler to manage log size)
        file_handler = RotatingFileHandler(
            f"logs/{name}.log",
            maxBytes=10485760,
            backupCount=5,
            encoding="utf-8",  # 10MB
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
