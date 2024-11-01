# Git Test Framework

## Questions
- how to test several branches in parallel, if they share the same physical space?

## Installation
- create venv
- activate
- install requirements

## Structure
- src: helper and other functions and classes
- tests: test case files
- scenarios: prepared files for scenarios, each test one scenario folder
- output: where testing is happening, files from scenarios being copied, analiser checks expected outputs

## Workflow
- global setup: prepare files on local machine for testing
  - remove everything
  - create folder structure (output, client, server)
  - install git (docker)
  - initiate shared git repo (tests are executed on the same branch)
- git initiator: creates independent client and/or server, for each test where needed
- scenario creator: before each test, creates a scenario for it (copy files, create branches)
- request sender: function that sends git commands through subprocess
- response parser: function that parses git command output and detemines pass/fail from command perspective
- result analiser: function that verifies the expected result, final pass/fail
  - checks changed files
  - existing branches
  - git tree / log
  - commit history is correct
  - etc

## Functionalities
- branch management: create, delete, checkout, switch (remote), merge, rebase
- file management: add, restore, restore staged, commit
- remote management: fetch, pull, push, clone, submodule
- state mamagement: ststus, diff, log

## Test Types
- client tests: small independent tests, testing only one functionality
- integration tests: testing bigger scenario (merging several branches, merge conflicts)