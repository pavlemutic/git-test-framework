# CHANGELOG

## [Unreleased]

## [Version 1.3.0] - 2024-11-06
### Added
- Repo class
- Local and Remote init tests
- Clone test, submodule test, fetch test
### Changed
- Moved the main logic from Scenario to Repo
- Improved readme file with info about framework and test strategy
### Removed
- init_repo folder with preinitialised local and remote repos
- create_init_repo.sh as we don't need preinitialising repos any more

## [Version 1.2.0] - 2024-11-06
### Added
- Parallel execution
- Test for merge conflicts
- Git error codes exceptions
- Black lint
- pyproject.toml for pytest and black config
### Changed
- Response has() now differs from regex strings from non-regex
- Merge and diff test according to the above change
### Removed
- pytest.ini, replaced with pyproject.toml

## [Version 1.1.0] - 2024-11-06
### Added
- Logging

## [Version 1.0.0] - 2024-11-05
### Added
- Introduced versioning
- Added Docker support

## How To
- Added for new features.
- Changed for changes in existing functionality.
- Deprecated for soon-to-be removed features.
- Removed for now removed features.
- Fixed for any bug fixes.
- Security in case of vulnerabilities.
