import pytest
from unittest.mock import patch, MagicMock
from src.file import File
from src.response import Response
from src.config import output_path, files_path, expected_files_path
from src.exceptions import GitExecutionError
from src.scenario import Scenario


@pytest.fixture
def scenario():
    return Scenario(name="test.scenario")


@patch("src.scenario.copyfile")
def test_add_file(mock_copyfile, scenario):
    scenario.local_path = output_path / "test_scenario" / "local"
    scenario.add_file("source.txt", "dest.txt")
    mock_copyfile.assert_called_once_with(src=files_path / "source.txt", dst=scenario.local_path / "dest.txt")
    assert "dest.txt" in scenario._files
    assert isinstance(scenario._files["dest.txt"], File)


def test_get_file(scenario):
    file_mock = MagicMock(spec=File)
    scenario._files["test.txt"] = file_mock
    assert scenario.get_file("test.txt") == file_mock
    assert scenario.get_file("nonexistent.txt") is None


def test_get_expected_file():
    file_name = "expected.txt"
    expected_file = ScenarioOld.get_expected_file(file_name)
    assert isinstance(expected_file, File)
    assert expected_file.path == expected_files_path / file_name


@patch("src.scenario.subprocess.run")
def test_run_success(mock_run, scenario):
    mock_run.return_value = MagicMock(returncode=0, stdout="Success output")
    command = "git status"
    response = scenario.run(command)
    mock_run.assert_called_once_with(
        ["git", "status"], cwd=scenario.local_path, capture_output=True, text=True
    )
    assert isinstance(response, Response)


@patch("src.scenario.subprocess.run")
def test_run_failure(mock_run, scenario):
    mock_run.return_value = MagicMock(returncode=2, stderr="Error output")
    command = "git status"
    with pytest.raises(GitExecutionError, match="Git command 'git status' failed with status code '2'"):
        scenario.run(command)


@patch("src.scenario.subprocess.run")
def test_run_failure_exception(mock_run, scenario):
    mock_run.return_value = MagicMock(returncode=1, stderr="Error output")
    command = "git status"
    response = scenario.run(command)
    mock_run.assert_called_once_with(
        ["git", "status"], cwd=scenario.local_path, capture_output=True, text=True
    )
    assert isinstance(response, Response)
