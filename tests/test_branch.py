from src.scenario import Scenario


def test_create():
    scenario = Scenario(name="branch.create")
    scenario.init()

    scenario.run("git branch new-branch")
    response = scenario.run("git branch")
    assert response.contains('* main')
    assert response.contains('new-branch')


def test_checkout():
    scenario = Scenario(name="branch.checkout")
    scenario.init()

    scenario.run("git checkout -b checkout-branch")
    response = scenario.run("git branch")
    assert response.contains('main')
    assert response.contains('* checkout-branch')

    response = scenario.run("git status")
    assert response.contains('On branch checkout-branch')
    assert response.contains('nothing to commit, working tree clean')
