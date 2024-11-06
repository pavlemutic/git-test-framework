import subprocess
from re import findall
from shutil import copytree, copyfile

from src.response import Response
from src.file import File
from src.config import init_repo_path, files_path, expected_files_path, output_path
from src.exceptions import GitExecutionError
from src.logger import log


class Scenario:
    def __init__(self, name, remote=False):
        self.name = name
        self._remote = remote

        self.local_repo_path = init_repo_path / "local"
        self.remote_repo_path = init_repo_path / "repo.git"
        self.scenario_path = None
        self.scenario_local_path = None

        self._files = {}
        self._expected_files = {}

        log.name = name

    def init(self):
        log.info(f"Initialising new scenario, setting 'local' {'and \'remote\' ' if self._remote else ''}git repo")
        self.scenario_path = output_path.joinpath(*(self.name.split(".")))
        self.scenario_path.mkdir(parents=True, exist_ok=False)
        log.debug(f"Scenario path: '{self.scenario_path}'")

        self.scenario_local_path = self.scenario_path / "local"
        copytree(self.local_repo_path, self.scenario_local_path)
        (self.scenario_local_path / ".git-nogit").rename(self.scenario_local_path / ".git")

        if self._remote:
            copytree(self.remote_repo_path, self.scenario_path / "repo.git")

    def add_file(self, file_name, scenario_file_name):
        log.debug(f"Adding '{file_name}' file to the scenario, as '{scenario_file_name}'")
        copyfile(
            src=files_path / file_name,
            dst=self.scenario_local_path / scenario_file_name
        )
        self._files[scenario_file_name] = File(self.scenario_local_path / scenario_file_name)

    def get_file(self, name):
        log.debug(f"Getting file '{name}' from scenario")
        return self._files.get(name)

    @staticmethod
    def get_expected_file(file_name):
        log.debug(f"Getting expected file '{file_name}' from '{expected_files_path / file_name}'")
        return File(expected_files_path / file_name)

    def run(self, command):
        log.info(f"Running command '{command}'")
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

    def get_heads_ref(self, branch, remote=False):
        path = self.scenario_path / "repo.git" / "refs" / "heads" / branch \
            if remote else self.scenario_local_path / ".git" / "refs" / "heads" / branch

        with open(path, "r") as heads_file:
            ref = heads_file.readline().strip()
            log.debug(f"Getting {'remote' if remote else 'local'} heads ref: {ref}")
            return ref
