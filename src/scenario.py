import subprocess
from re import findall
from shutil import copytree, copyfile

from src.response import Response
from src.file import File
from src.config import scenario_artefacts_path, output_path
from src.exceptions import GitExecutionError


class Scenario:
    def __init__(self, name, remote=False):
        self.name = name
        self._remote = remote

        self.local_repo_path = scenario_artefacts_path / "init_repo" / "local"
        self.remote_repo_path = scenario_artefacts_path / "init_repo" / "repo.git"
        self.scenario_path = output_path
        self.scenario_local_path = None

        self.files = {}

    def init(self):
        self.scenario_path = self.scenario_path.joinpath(*(self.name.split(".")))
        self.scenario_path.mkdir(parents=True, exist_ok=False)

        self.scenario_local_path = self.scenario_path / "local"
        copytree(self.local_repo_path, self.scenario_local_path)

        if self._remote:
            copytree(self.remote_repo_path, self.scenario_path / "repo.git")

    def add_file(self, src_file_name, dest_file_name):
        copyfile(
            src=scenario_artefacts_path / "files" / src_file_name,
            dst=self.scenario_local_path / dest_file_name
        )
        self.files[dest_file_name] = File(self.scenario_local_path / dest_file_name)

    def run(self, command):
        command_list = findall(r'"[^"]*"|\S+', command)
        result = subprocess.run(
            command_list,
            cwd=self.scenario_local_path,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return Response(result=result)

        raise GitExecutionError(
            f"Git command '{command}' failed with status code '{result.returncode}'.\n\n"
            f"Git output:\n{result.stderr}"
        )
