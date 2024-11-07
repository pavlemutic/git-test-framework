import logging
from logging.handlers import RotatingFileHandler

from src.config import log_level, log_path, rotation_file_size, backup_count

log = logging.getLogger("GTF")
log.setLevel(log_level)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s :: %(message)s")

file_handler = RotatingFileHandler(filename=log_path, mode="a", maxBytes=rotation_file_size, backupCount=backup_count)
file_handler.setFormatter(formatter)
log.addHandler(file_handler)
