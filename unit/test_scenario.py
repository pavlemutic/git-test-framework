import pytest
from unittest.mock import patch, MagicMock
from src.scenario import Scenario
from src.repo import Repo


@pytest.fixture
@patch("pathlib.Path.mkdir")
def scenario(mock_mkdir):
    return Scenario(name="test_scenario")


@patch("pathlib.Path.mkdir")
@patch("src.repo.Repo.run")
@patch("src.repo.Repo.setup")
def test_init_local_repo(mock_setup, mock_run, mock_mkdir):
    scenario = Scenario(name="test_scenario")
    repo = scenario.init_local_repo(repo_name="local_repo_name")
    mock_run.assert_called_once_with("git init --initial-branch=main")
    mock_setup.assert_called_once()

    assert scenario.local_repos["local_repo_name"] == repo
    assert isinstance(repo, Repo)


@patch("pathlib.Path.mkdir")
@patch("src.repo.Repo.run")
@patch("src.repo.Repo.setup")
def test_init_remote_repo(mock_setup, mock_run, mock_mkdir):
    scenario = Scenario(name="test_scenario")
    repo = scenario.init_remote_repo("remote_repo")
    mock_run.assert_called_once_with("git init --bare")
    mock_setup.assert_called_once()

    assert scenario.remote_repos["remote_repo"] == repo
    assert isinstance(repo, Repo)


@patch("pathlib.Path.mkdir")
@patch("src.repo.Repo.run")
@patch("src.repo.Repo.setup")
def test_clone_repo(mock_setup, mock_run, mock_mkdir):
    scenario = Scenario(name="test_scenario")
    mock_remote_repo = MagicMock(spec=Repo)
    mock_remote_repo.path = "/fake/remote/repo/path"
    scenario.remote_repos["remote_repo"] = mock_remote_repo

    local_repo = scenario.clone_repo("remote_repo", "local_clone_repo")

    expected_clone_command = f"git clone {mock_remote_repo.path} {local_repo.path}"
    mock_run.assert_any_call(expected_clone_command)
    mock_setup.assert_called_once()

    assert "local_clone_repo" in scenario.local_repos
    assert scenario.local_repos["local_clone_repo"] == local_repo
    assert isinstance(local_repo, Repo)


@patch("src.scenario.listdir")
def test_list_folder_items(mock_listdir, scenario):
    mock_listdir.return_value = ["file1.txt", "file2.txt"]
    folder_items = scenario.list_folder_items()
    mock_listdir.assert_called_once_with(scenario.path)
    assert folder_items == ["file1.txt", "file2.txt"]
