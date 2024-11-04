from hashlib import md5


class File:
    def __init__(self, path):
        self.path = path

    @staticmethod
    def _get_file_hash(file_path):
        md5_obj = md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_obj.update(chunk)

        return md5_obj.hexdigest()

    def append_text(self, text):
        with open(self.path, "a") as fp:
            fp.write(text)

    def override_text(self, text):
        with open(self.path, "w") as fp:
            fp.write(text)

    def is_equal(self, comparable_path):
        original_file_hash = self._get_file_hash(self.path)
        comparing_file_hash = self._get_file_hash(comparable_path)
        return original_file_hash == comparing_file_hash
