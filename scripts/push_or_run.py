from pathlib import Path

NESTED_REPO_PATH = Path(__file__).parents[1] / "scenario_artefacts" / "init_repo" / "local"

def prepare_for_push():
    dot_git_dir = NESTED_REPO_PATH / ".git"
    dot_git_dir.rename(NESTED_REPO_PATH / ".git.tmp")

def prepare_for_run():
    dot_git__tmp_dir = NESTED_REPO_PATH / ".git.tmp"
    dot_git__tmp_dir.rename(NESTED_REPO_PATH / ".git")


if __name__ == '__main__':
    prepare_for_push()
    # prepare_for_run()