from src.scenario import Scenario


def test_status():
    scenario = Scenario("state.status")
    repo = scenario.init_local_repo(repo_name="local")
    repo.add_file(file_name="one_line", repo_file_name="status_file")

    response = repo.run("git status")
    assert response.contains("Untracked files:")
    assert response.contains('(use "git add <file>..." to include in what will be committed)')
    assert response.contains("status_file")


def test_diff():
    scenario = Scenario("state.diff")
    repo = scenario.init_local_repo(repo_name="local")
    repo.add_file(file_name="one_line", repo_file_name="diff_file")

    repo.run("git add diff_file")
    repo.run('git commit -m "Add diff_file"')
    repo.get_file("diff_file").append_text("new diff text")

    response = repo.run("git diff")
    assert response.has(on_line=1, text="diff --git a/diff_file b/diff_file")
    assert response.has(on_line=2, text=r"index [0-9a-f]{7}..[0-9a-f]{7} 100644", regex=True)
    assert response.has(on_line=3, text="--- a/diff_file")
    assert response.has(on_line=4, text="+++ b/diff_file")
    assert response.has(on_line=5, text="@@ -1 +1,2 @@")
    assert response.has(on_line=6, text="one line file")
    assert response.has(on_line=7, text="+new diff text")
