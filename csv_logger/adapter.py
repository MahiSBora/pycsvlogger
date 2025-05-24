import logging
from logging import LoggerAdapter
from .handler import CsvLogHandler

# central logger instance
_logger = logging.getLogger("csv_logger")
_logger.setLevel(logging.INFO)

def init_csv_logger(log_file="events.csv", fieldnames=None):
    """
    Attach a CsvLogHandler with your chosen columns:
      init_csv_logger(
        log_file="logs/my_events.csv",
        fieldnames=["timestamp","script","user","status","message"]
      )
    """
    handler = CsvLogHandler(log_file, fieldnames)
    _logger.handlers.clear()
    _logger.addHandler(handler)

def get_record_logger(**defaults):
    """
    Returns a LoggerAdapter pre-loaded with defaults.
    e.g. logger = get_record_logger(record_id="1234", action="download")
    Then logger.info("…") only needs the message.
    """
    return LoggerAdapter(_logger, defaults)
