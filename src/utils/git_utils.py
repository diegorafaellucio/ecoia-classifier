from src.controller.aux_model_controller import ModelController
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from git import Repo
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
    def get_project_current_version(project_path):
        model_repo = Repo(project_path)
        current_branch = model_repo.active_branch
        branch_name = current_branch.name
        project_version = GitUtils.get_version_from_branch_name(branch_name)

        return project_version



    @staticmethod
    def get_version_from_branch_name(branch_name):
        branch_name_elements = branch_name.split('-')
        project_version = branch_name_elements[-1]
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

