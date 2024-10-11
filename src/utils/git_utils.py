from src.controller.model_controller import ModelController
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from git import Repo
import git
import os
from pathlib import Path

class GitUtils:

    @staticmethod
    def get_most_recent_branch_based_into_model_identifier(project_path, plant_models_identifier):
        most_recent_branch_name = 'main'

        project_repo = Repo(project_path)

        project_repo.git.fetch('--all')

        project_repo.remotes.origin.pull()

        available_branches = [branch.split("/")[-1] for branch in project_repo.git.branch('-r').splitlines()]

        # available_branches = project_repo.branches

        selected_branches = []

        for available_branch in available_branches:

            if plant_models_identifier in available_branch:
                selected_branches.append(available_branch)

        if len(selected_branches) != 0:
            most_recent_branch_name = GitUtils.get_most_recent_branch(selected_branches)

        return most_recent_branch_name

    @staticmethod
    def remove_all_not_active_branchs(current_branch, model_path):
        project_repo = Repo(model_path)

        local_branches = project_repo.branches

        for branch in local_branches:
            if branch.name != current_branch:
                try:
                    project_repo.delete_head(branch, force=True)  # force=True se quiser forçar a remoção
                    print(f"Deleted branch: {branch.name}")
                except git.exc.GitCommandError as e:
                    print(f"Could not delete branch {branch.name}: {e}")


    @staticmethod
    def get_current_version(model_path):
        project_repo = Repo(model_path)

        project_version = project_repo.active_branch.name

        return project_version

    @staticmethod
    def get_most_recent_branch(available_branches):
        sorted_available_branches = sorted(available_branches, reverse=True)

        return sorted_available_branches[0]

    @staticmethod
    def perform_checkout(project_path, branch_name):
        project_repo = Repo(project_path)
        project_repo.git.checkout(branch_name)
        project_repo.git.pull('origin', branch_name)

