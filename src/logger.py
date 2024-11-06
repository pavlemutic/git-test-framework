import logging
from logging.handlers import TimedRotatingFileHandler

from src.config import log_level, log_path

log = logging.getLogger("GTF")
log.setLevel(log_level)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s :: %(message)s")

file_handler = TimedRotatingFileHandler(filename=log_path, when="W5", interval=1)
file_handler.setFormatter(formatter)
log.addHandler(file_handler)
