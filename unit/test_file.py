import pytest
from hashlib import md5
from src.file import File


@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Initial content\nLine 2\nLine 3\n")
    return File(file_path)


def calculate_md5(content):
    md5_obj = md5()
    md5_obj.update(content.encode())
    return md5_obj.hexdigest()


def test_hash(temp_file):
    expected_hash = calculate_md5("Initial content\nLine 2\nLine 3\n")
    assert temp_file.hash == expected_hash


def test_append_text(temp_file):
    temp_file.append_text("New line")
    assert temp_file.path.read_text().endswith("New line\n")


def test_replace_nth_line(temp_file):
    temp_file.replace_nth_line("Replaced line", 2)
    lines = temp_file.path.read_text().splitlines()
    assert lines[1] == "Replaced line"
    assert lines[0] == "Initial content"
    assert lines[2] == "Line 3"


def test_override_text(temp_file):
    temp_file.override_text("Overwritten content")
    assert temp_file.path.read_text() == "Overwritten content\n"


def test_equality_same_content(tmp_path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_text("Same content")
    file2.write_text("Same content")

    file_obj1 = File(file1)
    file_obj2 = File(file2)

    assert file_obj1 == file_obj2


def test_equality_different_content(tmp_path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_text("Content A")
    file2.write_text("Content B")

    file_obj1 = File(file1)
    file_obj2 = File(file2)

    assert file_obj1 != file_obj2


def test_equality_type_error(temp_file):
    with pytest.raises(TypeError, match="Both sides of equation must be of type File"):
        assert temp_file == "not a File object"


def test_repr(temp_file):
    expected_hash = temp_file.hash
    assert repr(temp_file) == expected_hash
