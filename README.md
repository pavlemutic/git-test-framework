# Git Test Framework

Automated test framework for testing Git tool. Written in Python, 
uses PyTest as a test runner. As this is a demo project, test coverage 
is restricted to very few and basic Git functionalities.

Framework is designed to be able to cover most of the Git functionalities. 
It is also created to be easy extendable to support Git functionalities that 
might not be capable now.

Tests can be executed in Docker container, making it suitable for CI/CD integration.

- [Usage](#usage)
  - [Install](#install)
  - [Run tests](#run-tests)
  - [Before PUSH](#before-push)
- [License](#license)

## Usage
### Install
```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run tests
```shell
pytest
```

### Before PUSH
```shell
pytest  # make sure your tests are not failing
pytest unit  # make sure unit tests are not failing
black .  # make sure your code looks consistent 

docker build -t gtf-docker:latest .  # build docker image
docker run --rm gtf-docker:latest pytest  # run tests from docker, making sure they work there, as well
```

## License
[MIT License](LICENSE)

## Development notes
### Challenges 
- how to execute tests in parallel since only one branch can be active at a time
- how to organise and setup scenario, and not to overcomplicate it
- subprocess cannot handle quoted command parts
- nested git conflicts

### Functionalities
- init: git init, git init --bare
- branch management: create, delete, checkout, switch (remote), merge, rebase
- file management: add, restore, restore staged, commit
- remote management: fetch, pull, push, clone, submodule
- state mamagement: ststus, diff, log
- config management: several config options

### Workflow
- global setup: prepare files on local machine for testing
    - remove everything from output directory
    - install git (docker)
- git initiator: creates independent client and/or server, for each test where needed
- scenario creator: before each test, creates a scenario for it (copy files, create branches)
- request runner: function that sends git commands through subprocess
- response parser: function that parses git command output and detemines pass/fail from command perspective
- result analiser: function that verifies the expected result, final pass/fail
    - checks changed files, compare hash values
    - existing branches
    - git tree / log
    - commit history is correct
    - etc
- error reporter: reports the failed result in human-readable mode
