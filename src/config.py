from pathlib import Path


root_path = Path(__file__).parents[1]

scenario_artefacts_path = root_path / "scenario_artefacts"
files_path = scenario_artefacts_path / "files"
expected_files_path = scenario_artefacts_path / "expected_files"
init_repo_path = scenario_artefacts_path / "init_repo"

output_path = root_path / "output"
