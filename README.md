# Git Test Framework

Automated test framework for testing Git tool. Written in Python, 
uses PyTest as a test runner. As this is a demo project, test coverage 
is restricted to very few and basic Git functionalities.

Framework is designed to be able to cover most of the Git functionalities. 
It is also created to be easy extendable to support Git functionalities that 
might not be capable now.

Tests can be executed in Docker container, making it suitable for CI/CD integration.

<!-- TOC -->
* [Git Test Framework](#git-test-framework)
  * [Usage](#usage)
    * [Install](#install)
    * [Run tests](#run-tests)
    * [Before PUSH](#before-push)
  * [Framework](#framework)
    * [Structure](#structure)
    * [Workflow](#workflow)
    * [Assertion types](#assertion-types)
  * [Test plan](#test-plan)
    * [Phase I (current state)](#phase-i-current-state)
    * [Phase II](#phase-ii)
    * [System requirements for CI/CD](#system-requirements-for-cicd)
  * [Development notes](#development-notes)
    * [Challenges](#challenges-)
  * [License](#license)
<!-- TOC -->

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

## Framework
### Structure

| Framework structure |                                                                                                                                                                                                                                                                             |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| log                 | Holds `gtf.log` file, the main (and only) log file of the framework. There could be backups as well, as it rotates on 100KB (configurable in `src/config.py`).                                                                                                              |
| output              | Executed scenarios are kept here, as an output of the test execution. Each scenario represents one test case, and each of them holds one or many repos with all files used for testing.                                                                                     |
| results             | JSON file with test execution results (test status, duration, etc)                                                                                                                                                                                                          |
| scenario_artefacts  | Files used within testing scenarios. `scenario_artefacts/files` are files that are being added to repo, modified and then performed Git action on it. `scenario_artefacts/expected_files` are files used to compare complex scenario outputs, as `merge conflict` scenario. |
| scripts             | Helpful scripts, not directly related to the framework.                                                                                                                                                                                                                     |
| src                 | Source files, framework core and complete logic.                                                                                                                                                                                                                            |
| tests               | Test cases for testing Git.                                                                                                                                                                                                                                                 |
| unit                | Unit tests for testing code in `src` folder.                                                                                                                                                                                                                                |

| Source structure |                                                                                                                                                                                                                                                                                                                              |
|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| scenario.py      | Scenario represents one test scenario, for instance 'merge'. It holds necessary repos and files for fulfilling the scenario. It contains methods for repo initialisation, clone, and to list the files.                                                                                                                      |
| repo.py          | Repo is a single repo within a Scenario. It can be local or remote, and there can be many of them, depending of the scenario (for 'submodule' there are four, two local, two remote repos). It contains the main logic of the framework, methods to run git commands, add file to the repo, compare with expected file, etc. |
| file.py          | File abstracts a file in the repo. It is the pointer to the file that is being managed with Git. It contains method for change the file content (append text, replace specific line), and to compare with another File.                                                                                                      |
| response.py      | Response is helping to catch and assert response message from Git command execution.                                                                                                                                                                                                                                         |
| logger.py        | Holds code for logging the actions to 'log/gtf.log' file                                                                                                                                                                                                                                                                     |
| exceptions.py    | Custom framework exceptions                                                                                                                                                                                                                                                                                                  |
| config.py        | Configurable items, mostly paths to the scenario artefacts, scenario outputs, log level and git user config.                                                                                                                                                                                                                 |

### Workflow
One test case tests one Git scenario. Each test case is independent and can be executed isolated or in parallel.
Scenario class abstracts Git scenario and one or more Git repos and files used within scenario. Each time 
scenario is created, new folder structure in `output` folder is created that follows scenario name. It can be 
chosen how many and of which type, repos will be created for single scenario. For this purpose there is Repo class, 
abstracting one code repositorium, local or remote. Main function of the Repo is to be able to execute Git 
console commands, and to manipulate with files. File can be added to the repo, content of the file can be updated, 
and file can be compared with another File. For this, we use File class. Finally, each Git console command 
response is captured in Response class, which helps us to assert the terminal output precisely.

### Assertion types
Specific assertion types are available to cover important aspects of git functionalities.

| Type            | Method                       | Description                                                                                                                                                 |
|-----------------|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Response        | contains(text)               | Verifies that Git command console output contains the text.                                                                                                 |
|                 | has(text, on_line, is_regex) | Verifies that Git command console output has the exact text on the specifi output line. Optionally, regex can be used for matching.                         |
| File comparison | file_1 == file_2             | Generates the hash code for each file and compares it. Useful to check if the final file, after modifications and conflicts resolved, has expected content. |
| Head reference  | get_heads_ref(branch)        | Get the repo head reference for given branch. Useful to check if local and remote branhes are having the same content, after pull/push and similar actions. |
| Folder items    | list_folder_items(path)      | List the content of the folder. Useful to check if repo contains all expected files.                                                                        |
| Config          | get_config_value(key)        | Each repo, local or remote, has it's config. This function helps us to verify the config content, for instance, if local points to expected origin.         |


## Test plan
Task: Describe what the second phase of the test implementation would be.

### Phase I (current state)
Implement tests with Priority 1 (P1) / most commonly used Git functionalities. Test coverage should be focused only on 
positive scenarios, not going into negative or edge cases, makeing sure that very important Git feature works
within it's basic usage.

Example scenario - `git merge`:
- On `main` branch create a `merge_file` file and commit it
- Create `second` branch, and checkout to it
- Update `merge_file` file content, commit it to `second` branch
- Checkout `main` branch and perform `git merge ssecond`
- Assert that `merge_file` is merged correctly

The given example shows basic usage of common and very important Git functionality. Focus was not on the idea 
to break it, but rather to make sure it works as expected. This is the general purpose of Phase I.

Current test coverage:
- init: init local repo, init server repo
- state: status, diff, log
- branch: create, checkout, commit, merge (without conflicts), merge (with conflicts)
- remote: clone, push, fetch, pull, submodule

### Phase II
Implement test with P2 priority, which cover the same functionalities as in Phase I, but this time to cover 
more use cases around single functionality. Speking of `git merge`, scenario with several updated files accross 
remote and local branches, with conflicts.
Test coverage should be also expanded on less important or less frequent functionalities, e.g. 
rebase, tag, stash, undo changes, head reset, cherry-pick, etc. Like in Phase I, only the basic usage of these 
less important functionalities should be covered.
The idea behind Phase II is to verify that important P1 functionalities work with most use case variations, 
and also to widen coverage of P2 functionalities, with basic usage.

### System requirements for CI/CD
Task: Describe the requirements of the system that would run these tests in a continuous integration manner.


## Development notes
### Challenges 
- how to execute tests in parallel since only one branch can be active at a time
- how to organise and setup scenario, and not to overcomplicate it
- subprocess cannot handle quoted command parts
- nested git conflicts
- to have multiple repos per scenario

## License
[MIT License](LICENSE)
