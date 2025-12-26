import logging
from datetime import datetime
import os

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/app_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('chaalak')

def log_error(error_type: str, message: str, user_id: str = None):
    context = f"[User: {user_id}] " if user_id else ""
    logger.error(f"{context}{error_type}: {message}")

def log_info(message: str, user_id: str = None):
    context = f"[User: {user_id}] " if user_id else ""
    logger.info(f"{context}{message}")

def log_warning(message: str, user_id: str = None):
    context = f"[User: {user_id}] " if user_id else ""
    logger.warning(f"{context}{message}")

def log_login_attempt(username: str, success: bool, ip: str = None):
    status = "SUCCESS" if success else "FAILED"
    ip_info = f" from {ip}" if ip else ""
    logger.info(f"Login {status}: {username}{ip_info}")
