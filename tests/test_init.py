from src.scenario import Scenario


def test_init():
    scenario = Scenario("init.init")
    scenario.init()

    response = scenario.run("git init")
    response.echo()
    response = scenario.run("git status")
    response.echo()
