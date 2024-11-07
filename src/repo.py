import subprocess
from shutil import copyfile
from re import search, findall
from os import listdir

from src.file import File
from src.response import Response
from src.config import files_path, expected_files_path
from src.config import git_user_name, git_user_email, error_code_exceptions
from src.logger import log
from src.exceptions import GitExecutionError


class Repo:
    def __init__(self, name, scenario_name, scenario_path, is_remote=False):
        log.name = f"{scenario_name}.{name}"

        self.name = name
        self.path = scenario_path / name
        self.path.mkdir(parents=True, exist_ok=False)
        log.info(f"Setting {'remote' if is_remote else 'local'} repo '{self.name}' on path: '{self.path}'")

        self.is_remote = is_remote
        self._files = {}

    def run(self, command):
        log.info(f"Running command '{command}'")

        command_list = findall(r'"[^"]*"|\S+', command)
        result = subprocess.run(command_list, cwd=self.path, capture_output=True, text=True)

        if result.returncode == 0 or result.returncode in error_code_exceptions.keys():
            return Response(result=result)

        raise GitExecutionError(
            f"Git command '{command}' failed with status code '{result.returncode}'.\n\n"
            f"Git output:\n{result.stderr}"
        )

    def setup(self):
        if self.is_remote:
            self.run("git --git-dir=. symbolic-ref HEAD refs/heads/main")

        else:
            self.run(f"git config user.name '{git_user_name}'")
            self.run(f"git config user.email '{git_user_email}'")

            self.add_file(file_name="README.md", repo_file_name="README.md")
            self.run("git add README.md")
            self.run('git commit -m "Initial commit"')

    def add_file(self, file_name, repo_file_name):
        log.debug(f"Adding '{file_name}' file to the '{self.name}' repo, as '{repo_file_name}'")
        copyfile(src=files_path / file_name, dst=self.path / repo_file_name)
        self._files[repo_file_name] = File(self.path / repo_file_name)

    def get_file(self, name):
        log.debug(f"Getting file '{name}' from '{self.name}' repo")
        return self._files.get(name)

    def get_config_value(self, key):
        path = self.path if self.is_remote else self.path / ".git"
        with open(path / "config") as fp:
            for line in fp.readlines():
                re_sult = search(rf"^\s+{key} = (?P<value>.+)\n?", line)
                if re_sult:
                    return re_sult.group("value")

    @staticmethod
    def get_expected_file(file_name):
        log.debug(f"Getting expected file '{file_name}' from '{expected_files_path / file_name}'")
        return File(expected_files_path / file_name)

    def get_heads_ref(self, branch):
        path = (
            self.path / "refs" / "heads" / branch if self.is_remote else self.path / ".git" / "refs" / "heads" / branch
        )

        with open(path, "r") as heads_file:
            ref = heads_file.readline().strip()
            log.debug(f"Getting '{self.name}' repo heads ref for '{branch}' branch: {ref}")
            return ref

    def list_folder_items(self, path=None):
        if not path:
            path = self.path
        if isinstance(path, str):
            path = self.path.joinpath(path)

        folder_items = listdir(path)
        log.debug(f"Folder items on path '{path}': {folder_items}")
        return folder_items
