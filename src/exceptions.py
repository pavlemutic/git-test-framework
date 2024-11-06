from src.logger import log

class GtfError(Exception):
    def __init__(self, message):
        super().__init__(message)
        log.error(f"{self.__class__.__name__}: {message}")

class GitExecutionError(GtfError):
    pass

class ResponseMismatchError(GtfError):
    pass
