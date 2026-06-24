import logging
from core.config import config

def setup_logging():
    """
    Configures application-wide logging.
    Logs stream to the console (captured automatically by Vercel).
    """

    level = logging.DEBUG if config.DEBUG else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )