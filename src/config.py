from pathlib import Path


root_path = Path(__file__).parents[1]

# SCENARIO
scenario_artefacts_path = root_path / "scenario_artefacts"
files_path = scenario_artefacts_path / "files"
expected_files_path = scenario_artefacts_path / "expected_files"
init_repo_path = scenario_artefacts_path / "init_repo"


# OUTPUT
output_path = root_path / "output"


# LOG
log_level = "DEBUG"
log_folder_path = root_path / "log"
log_path = root_path / "log" / "gtf.log"

log_folder_path.mkdir(exist_ok=True)


# GIT
error_code_exceptions = {
    1: "merge conflict"
}