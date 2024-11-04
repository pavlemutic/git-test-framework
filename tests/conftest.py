import shutil

from src.config import output_path


def pytest_sessionstart(session):
    # - install git (docker)
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(exist_ok=True)
