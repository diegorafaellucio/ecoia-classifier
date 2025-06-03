import os
import json
import logging
import shutil
from pathlib import Path
from src.enum.image_state_enum import ImageStateEnum
from django.conf import settings


class FileUtils:
    logger = logging.getLogger(__name__)
    @staticmethod
    def have_files_to_process(data):
        if data is None or len(data) == 0:
            return False
        else:
            return True


    @staticmethod
    def has_file(image_absolute_path, flag_img, state):
        has_image = False

        if os.path.exists(image_absolute_path) and int(flag_img) == 1 and (int(state) == (ImageStateEnum.WAITING_PROCESSING.value)):
            has_image = True
        elif not os.path.exists(image_absolute_path):
            has_image = False

        return has_image

    @staticmethod
    def copy_file(file_absolute_path):
        file_path_elements = os.path.split(file_absolute_path)

        file_base_path = file_path_elements[0]
        file_name = file_path_elements[-1]

        sync_file_base_path = file_base_path.replace('fotos', "sync")

        os.makedirs(sync_file_base_path, exist_ok=True)

        sync_file_absolute_path = os.path.join(sync_file_base_path, file_name)

        shutil.copy(file_absolute_path, sync_file_absolute_path)


    @staticmethod
    def read_model_info(model_weight_path):

        base_dir = settings.BASE_DIR
        model_path = os.path.dirname(model_weight_path)
        model_path_relative = model_path.lstrip('/')
        model_info_path = os.path.join(base_dir, model_path_relative, 'model_info.json')


        try:
            with open(model_info_path, "r") as json_file:
                data = json.load(json_file)

            return data["model_train_approach"]

        except FileNotFoundError:
            raise FileNotFoundError(f"O arquivo model_info não foi encontrado na pasta '{model_info_path}'.")
        except json.JSONDecodeError:
            raise ValueError(f"O arquivo '{model_info_path}' não contém um JSON válido.")