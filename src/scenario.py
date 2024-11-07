from os import listdir

from src.repo import Repo
from src.config import output_path
from src.logger import log


class Scenario:
    def __init__(self, name):
        log.name = name

        self.name = name
        self.path = output_path.joinpath(*(name.split(".")))
        self.path.mkdir(parents=True, exist_ok=False)
        log.info(f"New scenario '{self.name}' created on path: '{self.path}'")

        self.local_repos = {}
        self.remote_repos = {}

    def init_local_repo(self, repo_name):
        repo = Repo(name=repo_name, scenario_name=self.name, scenario_path=self.path)
        repo.run("git init")
        repo.setup()
        self.local_repos[repo.name] = repo
        return repo

    def init_remote_repo(self, repo_name):
        repo = Repo(name=repo_name, scenario_name=self.name, scenario_path=self.path, is_remote=True)
        repo.run("git init --bare")
        repo.setup()
        self.remote_repos[repo.name] = repo
        return repo

    def clone_repo(self, remote_repo_name, local_repo_name):
        remote_repo = self.remote_repos.get(remote_repo_name)
        local_repo = Repo(name=local_repo_name, scenario_name=self.name, scenario_path=self.path)
        local_repo.run(f"git clone {remote_repo.path} {local_repo.path}")
        local_repo.setup()
        self.local_repos[local_repo.name] = local_repo
        return local_repo

    def list_folder_items(self, path=None):
        if not path:
            path = self.path
        if isinstance(path, str):
            path = self.path.joinpath(path)

        folder_items = listdir(path)
        log.debug(f"Folder items on path '{path}': {folder_items}")
        return folder_items
