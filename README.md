# Git Test Framework

## Challenges 
- how to execute tests in parallel since only one branch can be active at a time
- how to organise and setup scenarion, and not to overcomplicate it
- subprocess cannot handle quoted command parts
- nested git conflicts

## Installation

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Structure
- output: where testing is happening, files from scenarios being copied, analiser checks expected outputs
- results: results JSON file
- scenario artefacts: prepared files for scenarios, init git repos
- scripts: helper independent scripts
- src: framework source code
- tests: test case files

## Workflow
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

## Functionalities
- init: git init, git init --bare
- branch management: create, delete, checkout, switch (remote), merge, rebase
- file management: add, restore, restore staged, commit
- remote management: fetch, pull, push, clone, submodule
- state mamagement: ststus, diff, log
- config management: several config options

## Test Types
- client tests: small independent tests, testing only one functionality
- integration tests: testing bigger scenario (merging several branches, merge conflicts)

## Classes
- Response: parses response from the command line
    - status (0: success, 1+: error)
    - output text (parsed console text)
    - function contains (if response text contains string)
    - function get branch name (git helper class?)
    - function get last n commits (git helper class?)
    - function get status (git helper class?)

- Scenario: holds test scenario data
    - scenario folder path
    - expected result files path

- File: functions to work with files
    - init: path to file
    - function append_text
    - function rewrite_text
    - function is_equal - path to another file (output file as expected)
