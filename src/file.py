from hashlib import md5


class File:
    def __init__(self, path):
        self.path = path

    @property
    def hash(self):
        md5_obj = md5()
        with open(self.path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_obj.update(chunk)

        return md5_obj.hexdigest()

    def append_text(self, text):
        with open(self.path, "a") as fp:
            fp.write(text + "\n")

    def replace_nth_line(self, text, line_num):
        old_file = self.path.parent / f"{self.path.name}.old"
        self.path.rename(old_file)

        with open(self.path, "w") as out_file:
            with open(old_file, "r") as in_file:
                for index, line in enumerate(in_file.readlines()):
                    if index + 1 == line_num:
                        out_file.write(text + "\n")
                        continue
                    out_file.write(line)
        old_file.unlink()

    def override_text(self, text):
        with open(self.path, "w") as fp:
            fp.write(text + "\n")

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.hash == other.hash

        raise TypeError("Both sides of equation must be of type File")

    def __repr__(self):
        return self.hash