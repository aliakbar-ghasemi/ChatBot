import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from app.core.config import settings

# Ensure the logs directory exists
log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")  # ✅ Relative path
os.makedirs(log_dir, exist_ok=True)  # ✅ This ensures the directory is created

log_file = os.path.join(log_dir, "app.log")

# Define log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Console handler (for development)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# File handler (for persistent logging)
file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
file_handler.setLevel(logging.INFO)  # Only log INFO level and above to file
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Configure root logger
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format=LOG_FORMAT,
    handlers=[console_handler, file_handler]
)

# Get a logger instance
logger = logging.getLogger("app")
