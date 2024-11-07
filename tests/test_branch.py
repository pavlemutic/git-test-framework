from src.scenario import Scenario


def test_create():
    scenario = Scenario("branch.create")
    repo = scenario.init_local_repo(repo_name="local")

    repo.run("git branch new-branch")
    response = repo.run("git branch")
    assert response.contains("* main")
    assert response.contains("new-branch")


def test_checkout():
    scenario = Scenario("branch.checkout")
    repo = scenario.init_local_repo(repo_name="local")

    repo.run("git checkout -b checkout-branch")
    response = repo.run("git branch")
    assert response.contains("main")
    assert response.contains("* checkout-branch")

    response = repo.run("git status")
    assert response.contains("On branch checkout-branch")
    assert response.contains("nothing to commit, working tree clean")

    repo.run("git checkout main")
    response = repo.run("git branch")
    assert response.contains("* main")
    assert response.contains("checkout-branch")

    response = repo.run("git status")
    assert response.contains("On branch main")
    assert response.contains("nothing to commit, working tree clean")


def test_merge():
    scenario = Scenario("branch.merge")
    repo = scenario.init_local_repo(repo_name="local")

    merge_file = "merge_file"
    expected_merge_file = "expected_merge_file"
    merge_branch = "branch-to-merge"

    repo.add_file(file_name="five_lines", repo_file_name=merge_file)
    repo.run(f"git add {merge_file}")
    repo.run(f'git commit -m "Add {merge_file}"')
    repo.run(f"git branch {merge_branch}")

    repo.get_file(merge_file).append_text("new, sixth line")
    repo.run(f"git add {merge_file}")
    repo.run('git commit -m "Add sixth line to merge_file"')

    repo.run(f"git checkout {merge_branch}")
    repo.get_file(merge_file).replace_nth_line("new, second line", 2)
    repo.run(f"git add {merge_file}")
    repo.run('git commit -m "Update second line in merge_file"')

    repo.run("git checkout main")
    repo.run(f"git merge {merge_branch}")

    response = repo.run("git status")
    assert response.contains("On branch main")
    assert response.contains("nothing to commit, working tree clean")

    response = repo.run("git log")
    response.echo()
    assert response.has(on_line=1, text=r"commit [0-9a-f]{40}", is_regex=True)
    assert response.has(on_line=2, text=r"Merge: [0-9a-f]{7} [0-9a-f]{7}", is_regex=True)
    assert response.has(on_line=3, text="Author: Pavle <mail@pavlemutic.com>")
    assert response.has(on_line=4, text=r"Date:   \w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4} [+-]\d{4}", is_regex=True)
    assert response.has(on_line=6, text="Merge branch 'branch-to-merge'")

    assert response.has(on_line=8, text=r"commit [0-9a-f]{40}", is_regex=True)
    assert response.has(on_line=9, text="Author: Pavle <mail@pavlemutic.com>")
    assert response.has(
        on_line=10, text=r"Date:   \w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4} [+-]\d{4}", is_regex=True
    )
    assert response.has(on_line=12, text='"Add sixth line to merge_file"')

    assert response.has(on_line=14, text=r"commit [0-9a-f]{40}", is_regex=True)
    assert response.has(on_line=15, text="Author: Pavle <mail@pavlemutic.com>")
    assert response.has(
        on_line=16, text=r"Date:   \w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4} [+-]\d{4}", is_regex=True
    )
    assert response.has(on_line=18, text='"Update second line in merge_file"')

    assert response.has(on_line=20, text=r"commit [0-9a-f]{40}", is_regex=True)
    assert response.has(on_line=21, text="Author: Pavle <mail@pavlemutic.com>")
    assert response.has(
        on_line=22, text=r"Date:   \w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4} [+-]\d{4}", is_regex=True
    )
    assert response.has(on_line=24, text='"Add merge_file"')

    assert response.has(on_line=26, text=r"commit [0-9a-f]{40}", is_regex=True)
    assert response.has(on_line=27, text="Author: Pavle <mail@pavlemutic.com>")
    assert response.has(
        on_line=28, text=r"Date:   \w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4} [+-]\d{4}", is_regex=True
    )

    assert response.has(on_line=30, text="Initial commit")

    assert repo.get_file(merge_file) == repo.get_expected_file(expected_merge_file)


def test_merge_conflict():
    scenario = Scenario("branch.merge_conflict")
    repo = scenario.init_local_repo(repo_name="local")

    file = "conflict_file"
    expected_conflict_file = "expected_conflict_file"
    branch = "conflict_branch"

    repo.add_file(file_name="five_lines", repo_file_name=file)
    repo.run(f"git add {file}")
    repo.run(f'git commit -m "Add {file}"')

    repo.run(f"git branch {branch}")
    repo.get_file(file).replace_nth_line("new fourth line from 'main'", 4)
    repo.run(f"git add {file}")
    repo.run(f'git commit -m "Update {file} on 4th from main"')

    repo.run(f"git checkout {branch}")
    repo.get_file(file).replace_nth_line(f"new fourth line from '{branch}'", 4)
    repo.run(f"git add {file}")
    repo.run(f'git commit -m "Update {file} on 4th from {branch}"')

    repo.run(f"git checkout main")
    response = repo.run(f"git merge {branch}")
    assert response.has(on_line=1, text="Auto-merging conflict_file")
    assert response.has(on_line=2, text="CONFLICT (content): Merge conflict in conflict_file")
    assert response.has(on_line=3, text="Automatic merge failed; fix conflicts and then commit the result.")

    response = repo.run("git status")
    assert response.has(on_line=1, text="On branch main")
    assert response.has(on_line=2, text="You have unmerged paths.")
    assert response.has(on_line=3, text='(fix conflicts and run "git commit")')
    assert response.has(on_line=4, text='(use "git merge --abort" to abort the merge)')
    assert response.has(on_line=6, text="Unmerged paths:")
    assert response.has(on_line=7, text='(use "git add <file>..." to mark resolution)')
    assert response.has(on_line=8, text="both modified:   conflict_file")
    assert response.has(on_line=10, text='no changes added to commit (use "git add" and/or "git commit -a")')

    response = repo.run("git log")
    assert response.has(on_line=1, text=r"commit [0-9a-f]{40}", is_regex=True)
    assert response.has(on_line=2, text="Author: Pavle <mail@pavlemutic.com>")
    assert response.has(on_line=3, text=r"Date:   \w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4} [+-]\d{4}", is_regex=True)
    assert response.has(on_line=5, text='"Update conflict_file on 4th from main"')

    assert response.has(on_line=7, text=r"commit [0-9a-f]{40}", is_regex=True)
    assert response.has(on_line=8, text="Author: Pavle <mail@pavlemutic.com>")
    assert response.has(on_line=9, text=r"Date:   \w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4} [+-]\d{4}", is_regex=True)
    assert response.has(on_line=11, text='"Add conflict_file"')

    assert response.has(on_line=13, text=r"commit [0-9a-f]{40}", is_regex=True)
    assert response.has(on_line=14, text="Author: Pavle <mail@pavlemutic.com>")
    assert response.has(
        on_line=15, text=r"Date:   \w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4} [+-]\d{4}", is_regex=True
    )
    assert response.has(on_line=17, text="Initial commit")

    assert repo.get_file(file) == repo.get_expected_file(expected_conflict_file)
