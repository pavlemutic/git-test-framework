from src.scenario import Scenario
from src.repo import Repo


def test_init_local():
    scenario = Scenario("init.local")
    assert scenario.list_folder_items() == []

    repo = Repo(name="local", scenario_name=scenario.name, scenario_path=scenario.path)
    response = repo.run("git init")
    assert response.contains(
        "Initialized empty Git repository in /Users/pavlemutic/repos/git-test-framework/output/init/local/local/.git/"
    )

    response = repo.run("git status")
    assert response.has(on_line=1, text="On branch main")
    assert response.has(on_line=3, text="No commits yet")
    assert response.has(on_line=5, text='nothing to commit (create/copy files and use "git add" to track)')

    assert ".git" in repo.list_folder_items(repo.path)
    assert "config" in repo.list_folder_items(repo.path / ".git")
    assert "objects" in repo.list_folder_items(repo.path / ".git")
    assert "HEAD" in repo.list_folder_items(repo.path / ".git")
    assert "info" in repo.list_folder_items(repo.path / ".git")
    assert "description" in repo.list_folder_items(repo.path / ".git")
    assert "hooks" in repo.list_folder_items(repo.path / ".git")
    assert "refs" in repo.list_folder_items(repo.path / ".git")


def test_init_remote():
    scenario = Scenario("init.remote")
    assert scenario.list_folder_items() == []

    repo = Repo(name="repo.git", scenario_name=scenario.name, scenario_path=scenario.path, is_remote=True)
    response = repo.run("git init --bare")
    assert response.contains(
        "Initialized empty Git repository in /Users/pavlemutic/repos/git-test-framework/output/init/remote/repo.git/"
    )

    assert repo.get_config_value("bare") == "true"

    assert ".git" not in repo.list_folder_items()
    assert "config" in repo.list_folder_items()
    assert "objects" in repo.list_folder_items()
    assert "HEAD" in repo.list_folder_items()
    assert "info" in repo.list_folder_items()
    assert "description" in repo.list_folder_items()
    assert "hooks" in repo.list_folder_items()
    assert "refs" in repo.list_folder_items()
