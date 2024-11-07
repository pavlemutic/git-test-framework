from src.scenario import Scenario
from src.repo import Repo
from src.file import File


def test_clone():
    scenario = Scenario("remote.clone")
    remote_repo = scenario.init_remote_repo(repo_name="repo.git")
    assert scenario.list_folder_items() == ["repo.git"]

    local_repo = Repo(name="local", scenario_name=scenario.name, scenario_path=scenario.path)
    local_repo.run(f"git clone {remote_repo.path} {local_repo.path}")

    assert scenario.list_folder_items() == ["repo.git", "local"]
    assert local_repo.list_folder_items() == [".git"]
    assert local_repo.get_config_value("url") == str(remote_repo.path)


def test_push():
    scenario = Scenario("remote.push")
    remote_repo = scenario.init_remote_repo(repo_name="repo.git")
    local_repo = scenario.clone_repo(remote_repo_name="repo.git", local_repo_name="local")

    local_repo.add_file(file_name="five_lines", repo_file_name="push_file")
    local_repo.run("git add push_file")
    local_repo.run('git commit -m "Add push_file"')

    response = local_repo.run("git push -u origin main")
    assert response.contains("branch 'main' set up to track 'origin/main'.")

    response = local_repo.run("git status")
    assert response.contains("On branch main")
    assert response.contains("nothing to commit, working tree clean")
    assert local_repo.get_heads_ref("main") == remote_repo.get_heads_ref("main")


def test_fetch():
    scenario = Scenario("remote.fetch")
    remote_repo = scenario.init_remote_repo(repo_name="repo.git")
    local_repo = scenario.clone_repo(remote_repo_name="repo.git", local_repo_name="local")

    local_repo.run("git checkout -b fetch-branch")
    local_repo.add_file(file_name="five_lines", repo_file_name="fetch_file")

    local_repo.run("git add fetch_file")
    local_repo.run('git commit -m "Add fetch_file"')
    local_repo.run('git push -u origin fetch-branch')
    assert local_repo.get_heads_ref("fetch-branch") == remote_repo.get_heads_ref("fetch-branch")

    local_repo.run("git checkout main")
    assert local_repo.get_heads_ref("main") != remote_repo.get_heads_ref("fetch-branch")
    local_repo.run("git fetch origin fetch-branch")
    local_repo.run("git merge origin/fetch-branch")
    assert local_repo.get_heads_ref("main") == remote_repo.get_heads_ref("fetch-branch")


def test_pull():
    scenario = Scenario("remote.pull")
    scenario.init_remote_repo(repo_name="repo.git")
    local_repo = scenario.clone_repo(remote_repo_name="repo.git", local_repo_name="local")

    local_repo.run("git checkout -b pull-branch")
    local_repo.add_file(file_name="five_lines", repo_file_name="pull_file")

    local_repo.run("git add pull_file")
    local_repo.run('git commit -m "Add pull_file"')
    local_repo.run("git push -u origin pull-branch")
    local_repo.run("git checkout main")

    folder_items = local_repo.list_folder_items()
    assert "pull_file" not in folder_items

    local_repo.run("git pull origin pull-branch")
    folder_items = local_repo.list_folder_items()
    assert "pull_file" in folder_items

    pulled_file = File(local_repo.path / "pull_file")
    assert local_repo.get_file("pull_file") == pulled_file


def test_submodule():
    scenario = Scenario("remote.submodule")
    scenario.init_remote_repo(repo_name="repo_1.git")
    local_repo_1 = scenario.clone_repo(remote_repo_name="repo_1.git", local_repo_name="local_1")

    remote_repo_2 = scenario.init_remote_repo(repo_name="repo_2.git")
    local_repo_2 = scenario.clone_repo(remote_repo_name="repo_2.git", local_repo_name="local_2")

    local_repo_2.add_file(file_name="one_line", repo_file_name="repo_2_one_line")
    local_repo_2.run("git add repo_2_one_line")
    local_repo_2.run('git commit -m "Add repo_2_one_line file"')
    local_repo_2.run("git push -u origin main")

    local_repo_1.run(f"git -c protocol.file.allow=always submodule add {remote_repo_2.path} submodule")
    local_repo_1.run("git submodule update --init")

    assert "submodule" in local_repo_1.list_folder_items()
    assert ".gitmodules" in local_repo_1.list_folder_items()
    assert "README.md" in local_repo_1.list_folder_items()
    assert "repo_2_one_line" in local_repo_1.list_folder_items("submodule")
    assert "README.md" in local_repo_1.list_folder_items("submodule")

    submodule_one_line_file = File(local_repo_1.path / "submodule" / "repo_2_one_line")
    assert submodule_one_line_file == local_repo_2.get_file("repo_2_one_line")
