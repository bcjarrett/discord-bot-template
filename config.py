import logging
import os

logger = logging.getLogger(__name__)

# Secrets & Config
DISCORD_API_SECRET = os.environ.get("DISCORD_API_SECRET", None)
BOT_STATUS = ["Example Status 1", "Example Status 2", "Example Status 3"]

# Define attached cogs here, add by folder name e.g. ./example/cog.py -> "example"
COGS = [
    "example",
]

# Database
DATABASE = "/data/my-db.db"

# Logging
LOG_PATH = "/data/log.log"

if not os.path.exists(LOG_PATH):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "w", encoding="utf-8"):
        pass

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "stream": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": f"{LOG_PATH}",
        },
    },
    "loggers": {
        "": {"handlers": ["stream", "file"], "level": "INFO", "propagate": False},
    },
}
