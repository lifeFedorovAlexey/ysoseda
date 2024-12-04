import logging
from config import LOG_LEVEL

# Настройка логгера
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=getattr(logging, LOG_LEVEL.upper(), "INFO")
)
logger = logging.getLogger(__name__)
