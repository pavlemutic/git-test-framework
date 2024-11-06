from re import search

from src.logger import log
from src.exceptions import ResponseMismatchError


class Response:
    """Class Response
    Contains the response segments from the git command.
    """

    def __init__(self, result):
        self.output = result.stdout
        self.output_list = result.stdout.splitlines()

    def contains(self, text):
        log.debug(f"Asserting if response contains text: '{text}'")
        if text in self.output:
            return True

        raise ResponseMismatchError(f"Response doesn't contain expected text: '{text}'.\nResponse:\n\n{self.output}")

    def has(self, on_line, text, regex=False):
        if len(self.output_list) < on_line or on_line < 0:
            raise IndexError(
                f"Requested line number '{on_line}' is out of the response boundaries.\nResponse:\n\n{self.output}"
            )

        line = self.output_list[on_line - 1]
        log.debug(f"Asserting if response on line {on_line} '{line}' has text: '{text}'")

        if regex:
            search_result = search(text, line)
            if search_result:
                return search_result

        elif text in line:
            return True

        raise ResponseMismatchError(
            f"Line number '{on_line}': '{line}' doesn't match expected text: '{text}'.\n"
            f"Full response:\n\n{self.output}"
        )

    def echo(self):
        print(self.output)
