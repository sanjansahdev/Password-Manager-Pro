import logging
from pathlib import Path

from config import LOG_FOLDER, LOG_FILE


# ==========================================
# Create Log Folder
# ==========================================

Path(LOG_FOLDER).mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# Configure Logger
# ==========================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==========================================
# Log Functions
# ==========================================

def log_info(message):

    logging.info(message)


def log_error(message):

    logging.error(message)


def log_warning(message):

    logging.warning(message)