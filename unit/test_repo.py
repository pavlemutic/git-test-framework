import pytest
from unittest.mock import patch, MagicMock, mock_open
from src.exceptions import GitExecutionError
from src.repo import Repo
from src.response import Response
from src.file import File
from src.config import output_path, files_path, expected_files_path
from src.config import git_user_name, git_user_email


@pytest.fixture
def repo_path(tmp_path):
    return tmp_path / "test_repo"


@pytest.fixture
def repo(repo_path):
    return Repo(name="test_repo", scenario_name="test_scenario", scenario_path=repo_path)


@patch("src.repo.log")
def test_repo_initialization(mock_log, repo_path):
    repo = Repo(name="test_repo", scenario_name="test_scenario", scenario_path=repo_path)

    assert repo.name == "test_repo"
    assert repo.path == repo_path / "test_repo"
    assert repo.is_remote is False
    mock_log.info.assert_called_with(f"Setting local repo 'test_repo' on path: '{repo.path}'")


@patch("subprocess.run")
@patch("src.repo.log")
def test_run_success(mock_log, mock_run, repo):
    mock_result = MagicMock(returncode=0, stdout="Success", stderr="")
    mock_run.return_value = mock_result

    response = repo.run('git status')
    assert isinstance(response, Response)
    mock_log.info.assert_called_with("Running command 'git status'")


@patch("subprocess.run")
def test_run_git_execution_error(mock_run, repo):
    mock_result = MagicMock(returncode=2, stderr="Some error")
    mock_run.return_value = mock_result

    with pytest.raises(GitExecutionError) as exc:
        repo.run('git status')
    assert "Git command 'git status' failed" in str(exc.value)


@patch("src.repo.Repo.run")
@patch("src.repo.log")
def test_setup_local_repo(mock_log, mock_run, repo):
    repo.setup()
    mock_run.assert_any_call(f"git config user.name '{git_user_name}'")
    mock_run.assert_any_call(f"git config user.email '{git_user_email}'")
    mock_run.assert_any_call("git add README.md")
    mock_run.assert_any_call('git commit -m "Initial commit"')


@patch("src.repo.Repo.run")
@patch("src.repo.log")
def test_setup_remote_repo(mock_log, mock_run, repo):
    repo.is_remote = True
    repo.setup()
    mock_run.assert_called_once_with("git --git-dir=. symbolic-ref HEAD refs/heads/main")


@patch("src.repo.copyfile")
def test_add_file(mock_copyfile, repo):
    repo.path = output_path / "test_repo" / "local"
    repo.add_file("source.txt", "dest.txt")
    mock_copyfile.assert_called_once_with(src=files_path / "source.txt", dst=repo.path / "dest.txt")
    assert "dest.txt" in repo._files
    assert isinstance(repo._files["dest.txt"], File)


def test_get_file(repo):
    repo._files["file.txt"] = File(repo.path / "file.txt")
    file = repo.get_file("file.txt")
    assert file is not None
    assert isinstance(file, File)


@patch("builtins.open", new_callable=mock_open, read_data="    key = value\n")
def test_get_config_value(mock_open, repo):
    value = repo.get_config_value("key")
    mock_open.assert_called_once_with(repo.path / ".git" / "config")
    assert value == "value"


def test_get_expected_file():
    file_name = "expected.txt"
    expected_file = Repo.get_expected_file(file_name)
    assert isinstance(expected_file, File)
    assert expected_file.path == expected_files_path / file_name


@patch("builtins.open", new_callable=mock_open, read_data="1234567890abcdef")
def test_get_heads_ref(mock_open, repo):
    ref = repo.get_heads_ref("main")
    mock_open.assert_called_once_with(repo.path / ".git" / "refs" / "heads" / "main", "r")
    assert ref == "1234567890abcdef"


@patch("src.repo.listdir")
def test_list_folder_items(mock_listdir, repo):
    mock_listdir.return_value = ["file1.txt", "file2.txt"]
    folder_items = repo.list_folder_items()
    mock_listdir.assert_called_once_with(repo.path)
    assert folder_items == ["file1.txt", "file2.txt"]
