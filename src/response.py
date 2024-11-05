from re import search

from src.exceptions import ResponseMismatchError


class Response:
    """ Class Response
    Contains the response segments from the git command.
    """
    def __init__(self, result):
        self.output = result.stdout
        self.output_list = result.stdout.splitlines()

    def contains(self, text):
        if text in self.output:
            return True

        raise ResponseMismatchError(
            f"Response doesn't contain expected text: '{text}'.\n"
            f"Response:\n\n{self.output}"
        )

    def has(self, on_line, text):
        if len(self.output_list) < on_line or on_line < 0:
            raise IndexError(
                f"Requested line number '{on_line}' "
                f"is out of the response boundaries.\nResponse:\n\n{self.output}"
            )

        line = self.output_list[on_line - 1]
        search_result = search(text, line)
        if search_result:
            return search_result

        raise ResponseMismatchError(
            f"Line number '{on_line}': '{line}' doesn't match expected text: '{text}'.\n"
            f"Full response:\n\n{self.output}"
        )
