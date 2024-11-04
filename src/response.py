class Response:
    """ Class Response
    Contains the response segments from the git command.
    """
    def __init__(self, result):
        self.status_ok = result.returncode == 0
        self.output = result.stdout
        # self.error = result.stderr

    def contains(self, text):
        return text in self.output
