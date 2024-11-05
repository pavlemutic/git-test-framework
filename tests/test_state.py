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
    assert response.has(on_line=1, text='diff --git a/diff_file b/diff_file')
    assert response.has(on_line=2, text='index [0-9a-f]{7}..[0-9a-f]{7} 100644')
    assert response.has(on_line=3, text='--- a/diff_file')
    assert response.has(on_line=4, text='\+\+\+ b/diff_file')
    assert response.has(on_line=5, text='@@ -1 \+1,3 @@')
    assert response.has(on_line=6, text='one line file')
    assert response.has(on_line=7, text='\+new diff text')
    assert response.has(on_line=8, text='\+')
