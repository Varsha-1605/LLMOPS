# Correct import of the logger file
from .cutom_logger import CustomLogger

# Create the global logger instance
_global_logger = CustomLogger().get_logger(__name__)

# Wrapper class so the rest of the app can call log.info(), log.error(), etc.
class GlobalLogger:
    @staticmethod
    def info(msg, **kwargs):
        _global_logger.info(msg, **kwargs)

    @staticmethod
    def warning(msg, **kwargs):
        _global_logger.warning(msg, **kwargs)

    @staticmethod
    def error(msg, **kwargs):
        _global_logger.error(msg, **kwargs)

    @staticmethod
    def debug(msg, **kwargs):
        _global_logger.debug(msg, **kwargs)
