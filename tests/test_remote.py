from src.scenario import Scenario
from src.file import File


def test_push():
    scenario = Scenario(name="remote.push", remote=True)
    scenario.init()

    assert scenario.get_heads_ref("main") == scenario.get_heads_ref("main", remote=True)

    scenario.add_file(file_name="five_lines", scenario_file_name="push_file")
    scenario.run("git add push_file")
    scenario.run('git commit -m "Add push_file"')

    assert scenario.get_heads_ref("main") != scenario.get_heads_ref("main", remote=True)

    response = scenario.run('git push -u ../repo.git main')
    assert response.contains("branch 'main' set up to track '../repo.git/main'.")

    response = scenario.run('git status')
    assert response.contains("On branch main")
    assert response.contains("nothing to commit, working tree clean")

    assert scenario.get_heads_ref("main") == scenario.get_heads_ref("main", remote=True)


# def test_fetch():
#     scenario = Scenario(name="remote.fetch", remote=True)
#     scenario.init()
#
#     scenario.run("git checkout -b fetch-branch")
#     scenario.add_file(src_file_name="five_lines", dest_file_name="fetch_file")
#
#     scenario.run("git add fetch_file")
#     scenario.run('git commit -m "Add fetch_file"')
#     scenario.run('git push -u ../repo.git fetch-branch')
#     # scenario.run('git fetch ../repo.git fetch-branch')


def test_pull():
    scenario = Scenario(name="remote.pull", remote=True)
    scenario.init()

    scenario.run("git checkout -b pull-branch")
    scenario.add_file(file_name="five_lines", scenario_file_name="pull_file")

    scenario.run("git add pull_file")
    scenario.run('git commit -m "Add pull_file"')
    scenario.run('git push -u ../repo.git pull-branch')
    scenario.run('git checkout main')
    response = scenario.run('ls -la')
    assert response.has(on_line=2, text='.')
    assert response.has(on_line=3, text='..')
    assert response.has(on_line=4, text='.git')
    assert response.has(on_line=5, text='README.md')

    scenario.run('git pull ../repo.git pull-branch')
    response = scenario.run('ls -la')
    assert response.has(on_line=2, text='.')
    assert response.has(on_line=3, text='..')
    assert response.has(on_line=4, text='.git')
    assert response.has(on_line=5, text='README.md')
    assert response.has(on_line=6, text='pull_file')

    pulled_file = File(scenario.scenario_local_path / "pull_file")
    assert scenario.get_file("pull_file") == pulled_file

