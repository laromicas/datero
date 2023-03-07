import logging
from .configuration import config

log_level = config['LOG'].get('LogLevel', logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s - %(levelname)s] - %(message)s", "%Y-%m-%d %H:%M:%S")

class TrimmedFileHandler(logging.FileHandler):
    def emit(self, record):
        # Get the log message
        msg = self.format(record).strip()

        # Write the trimmed message to the file
        if msg:
            try:
                self.stream.write(msg + self.terminator)
                self.flush()
            except Exception:
                self.handleError(record)

# Get root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create a file handler
if config.getboolean('LOG', 'Logging', fallback=False):
    file_handler = TrimmedFileHandler(config['LOG'].get('LogFile', 'datero.log'))
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# Create a stream handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
if config['COMMAND'].get('Verbose', False):
    stream_handler.setLevel(logging.DEBUG)
if config['COMMAND'].get('Quiet', False):
    stream_handler.setLevel(logging.WARNING)
logger.addHandler(stream_handler)
