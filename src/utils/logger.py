import sys
from loguru import logger

# 移除默认的 handler
logger.remove()

# 添加控制台输出，带有颜色和特定的格式
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# 添加文件输出，每天轮转一次，保留7天
logger.add(
    "logs/dsa_core_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="7 days",
    level="DEBUG",
    encoding="utf-8"
)

# 导出一个全局可用的 logger
__all__ = ["logger"]