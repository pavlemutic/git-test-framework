import logging
from logging.handlers import RotatingFileHandler

from src.config import log_level, log_path

log = logging.getLogger("GTF")
log.setLevel(log_level)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s :: %(message)s")

file_handler = RotatingFileHandler(filename=log_path, mode="a", maxBytes=100000, backupCount=1)
file_handler.setFormatter(formatter)
log.addHandler(file_handler)
