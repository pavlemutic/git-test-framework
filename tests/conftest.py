import shutil

from src.config import output_path, root_path


def clear_output_dir():
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(exist_ok=True)


def pytest_sessionstart(session):
    clear_output_dir()


def pytest_collection_finish(session):
    with open(root_path / "VERSION") as fp:
        print(f"git-test-framework version: {fp.readline()}")
