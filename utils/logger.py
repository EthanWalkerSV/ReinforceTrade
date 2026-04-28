from loguru import logger
from config.settings import settings

logger.remove()
logger.add("logs/reinforcetrade.log", level=settings.log_level, rotation="1 day", retention="7 days")
logger.add(lambda msg: print(msg), level=settings.log_level)
