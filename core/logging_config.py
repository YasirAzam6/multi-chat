import logging
import os
from core.config import config


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logging():
    """
    Configures application-wide logging.
    Logs go to both console and a file in the tenant root directory.
    """

    level = logging.DEBUG if config.DEBUG else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(LOG_DIR, "app.log"))
        ]
    )