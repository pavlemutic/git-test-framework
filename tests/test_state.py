from src.scenario import Scenario

def test_status():
    scenario = Scenario(name="state.status")
    scenario.init()
    scenario.add_file(src_file_name="one_line", dest_file_name="status_file")

    response = scenario.run("git status")
    assert response.contains('Untracked files:')
    assert response.contains('(use "git add <file>..." to include in what will be committed)')
    assert response.contains('status_file')

def test_diff():
    scenario = Scenario(name="state.diff")
    scenario.init()
    scenario.add_file(src_file_name="one_line", dest_file_name="diff_file")

    scenario.run("git add diff_file")
    scenario.run('git commit -m "Add diff_file"')
    scenario.get_file("diff_file").append_text("new diff text\n")

    response = scenario.run("git diff")
    assert response.contains("diff --git a/diff_file b/diff_file")
    assert response.contains("--- a/diff_file")
    assert response.contains("+++ b/diff_file")
    assert response.contains("@@ -1 +1,2 @@")
    assert response.contains("one line file")
    assert response.contains("+new diff text")
