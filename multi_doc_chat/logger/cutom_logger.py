import os                           # For filesystem path handling
import logging                      # Python's built-in logging system
from datetime import datetime       # To generate timestamped log filenames
import structlog                    # For structured (JSON) logging


class CustomLogger:
    def __init__(self, log_dir="logs"):
        # Create absolute path to logs directory
        self.logs_dir = os.path.join(os.getcwd(), log_dir)

        # Ensure the directory exists (create if not)
        os.makedirs(self.logs_dir, exist_ok=True)

        # Generate timestamped log filename, e.g., "02_14_2025_19_22_33.log"
        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

        # Full file path where logs will be written
        self.log_file_path = os.path.join(self.logs_dir, log_file)

    def get_logger(self, name=__file__):
        # Extract only the filename for logger identification
        logger_name = os.path.basename(name)

        # File handler → writes logs to the log file
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)                    # Log only INFO+
        file_handler.setFormatter(logging.Formatter("%(message)s"))  # Raw message format

        # Console handler → prints logs to terminal
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        # Configure Python logging system globally
        logging.basicConfig(
            level=logging.INFO,          # Default logging level
            format="%(message)s",        # Don't add metadata—structlog adds it
            handlers=[console_handler, file_handler]
        )

        # Configure structlog to output structured JSON logs
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),  # Add ISO timestamp
                structlog.processors.add_log_level,                                      # Include log level
                structlog.processors.EventRenamer(to="event"),                           # Rename message → event
                structlog.processors.JSONRenderer()                                       # Render final log as JSON
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),  # Use stdlib logger underneath
            cache_logger_on_first_use=True,                   # Faster repeated calls
        )

        # Return a structlog logger instance with the chosen name
        return structlog.get_logger(logger_name)