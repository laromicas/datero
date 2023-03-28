import logging

from datero.helpers import Bcolors
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
                self.stream.write(Bcolors.remove_color(msg) + self.terminator)
                self.flush()
            except Exception:
                self.handleError(record)



class TrimmedStreamHandler(logging.StreamHandler):
    def emit(self, record):
        """
        Emit a record.

        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        try:
            msg = self.format(record)
            stream = self.stream
            # issue 35046: merged two stream.writes into one.
            stream.write(msg)
            self.flush()
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)

# Get root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def enable_logging():
    global logger
    file_handler = TrimmedFileHandler(config['LOG'].get('LogFile', 'datero.log'))
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# Create a file handler
if config.getboolean('LOG', 'Logging', fallback=False):
    enable_logging()

# Create a stream handler
stream_handler = TrimmedStreamHandler()
stream_handler.setLevel(logging.INFO)
if config.getboolean('COMMAND', 'Verbose', fallback=False):
    stream_handler.setLevel(logging.DEBUG)
if config.getboolean('COMMAND', 'Quiet', fallback=False):
    stream_handler.setLevel(logging.WARNING)
logger.addHandler(stream_handler)

def set_verbosity(verbosity):
    stream_handler.setLevel(verbosity)

def set_quiet():
    stream_handler.setLevel(logging.WARNING)

def set_verbose():
    stream_handler.setLevel(logging.DEBUG)

def get_verbosity():
    return stream_handler.level

def get_file_level():
    for handler in logger.handlers:
        if isinstance(handler, TrimmedFileHandler):
            return handler.level

# for handler in logger.handlers:
#     print(get_file_level())
#     print(get_stream_level())
