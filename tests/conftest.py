import shutil

from src.config import output_path

def clear_output_dir():
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(exist_ok=True)

def pytest_sessionstart(session):
    # - install git (docker)
    clear_output_dir()
