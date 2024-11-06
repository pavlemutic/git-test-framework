from src.scenario import Scenario


def test_create():
    scenario = Scenario("branch.create")
    scenario.init()

    scenario.run("git branch new-branch")
    response = scenario.run("git branch")
    assert response.contains('* main')
    assert response.contains('new-branch')


def test_checkout():
    scenario = Scenario("branch.checkout")
    scenario.init()

    scenario.run("git checkout -b checkout-branch")
    response = scenario.run("git branch")
    assert response.contains('main')
    assert response.contains('* checkout-branch')

    response = scenario.run("git status")
    assert response.contains('On branch checkout-branch')
    assert response.contains('nothing to commit, working tree clean')

    scenario.run("git checkout main")
    response = scenario.run("git branch")
    assert response.contains('* main')
    assert response.contains('checkout-branch')

    response = scenario.run("git status")
    assert response.contains('On branch main')
    assert response.contains('nothing to commit, working tree clean')


def test_merge():
    scenario = Scenario("branch.merge")
    scenario.init()
    scenario.add_file(file_name="five_lines", scenario_file_name="merge_file")
    scenario.run("git add merge_file")
    scenario.run('git commit -m "Add merge_file"')
    scenario.run("git branch branch-to-merge")

    scenario.get_file("merge_file").append_text("new, sixth line")
    scenario.run("git add merge_file")
    scenario.run('git commit -m "Add sixth line to merge_file"')

    scenario.run("git checkout branch-to-merge")
    scenario.get_file("merge_file").replace_nth_line("new, second line", 2)
    scenario.run("git add merge_file")
    scenario.run('git commit -m "Update second line in merge_file"')

    scenario.run("git checkout main")
    scenario.run("git merge branch-to-merge")

    response = scenario.run("git status")
    assert response.contains('On branch main')
    assert response.contains('nothing to commit, working tree clean')

    response = scenario.run("git log")
    assert response.has(on_line=1, text=r'commit [0-9a-f]{40}')
    assert response.has(on_line=2, text=r'Merge: [0-9a-f]{7} [0-9a-f]{7}')
    assert response.has(on_line=3, text='Author: Pavle Mutic <mail@pavlemutic.com>')
    assert response.has(on_line=4, text=r'Date:   \w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4} [+-]\d{4}')
    assert response.has(on_line=6, text="Merge branch 'branch-to-merge'")

    assert response.has(on_line=8, text=r'commit [0-9a-f]{40}')
    assert response.has(on_line=9, text='Author: Pavle Mutic <mail@pavlemutic.com>')
    assert response.has(on_line=10, text=r'Date:   \w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4} [+-]\d{4}')
    assert response.has(on_line=12, text='"Add sixth line to merge_file"')

    assert response.has(on_line=14, text=r'commit [0-9a-f]{40}')
    assert response.has(on_line=15, text='Author: Pavle Mutic <mail@pavlemutic.com>')
    assert response.has(on_line=16, text=r'Date:   \w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4} [+-]\d{4}')
    assert response.has(on_line=18, text='"Update second line in merge_file"')

    assert response.has(on_line=20, text=r'commit [0-9a-f]{40}')
    assert response.has(on_line=21, text='Author: Pavle Mutic <mail@pavlemutic.com>')
    assert response.has(on_line=22, text=r'Date:   \w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4} [+-]\d{4}')
    assert response.has(on_line=24, text='"Add merge_file"')

    assert response.has(on_line=26, text=r'commit [0-9a-f]{40}')
    assert response.has(on_line=27, text='Author: Pavle Mutic <mail@pavlemutic.com>')
    assert response.has(on_line=28, text=r'Date:   \w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4} [+-]\d{4}')

    assert response.has(on_line=30, text='Initial commit')

    assert scenario.get_file("merge_file") == scenario.get_expected_file("expected_merge_file")
