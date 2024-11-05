from src.scenario import Scenario


def test_create():
    scenario = Scenario(name="branch.create")
    scenario.init()

    response = scenario.run("git branch new-branch")
    print(response.output)
    response = scenario.run("git branch")
    print(response.output)
