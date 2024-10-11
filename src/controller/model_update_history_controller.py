from django.db import connection
from src.enum.image_state_enum import ImageStateEnum
import re


class ModelUpdateHistoryController:

    @staticmethod
    def insert_into_model_update_history(model_id, current_version, update_version):
        with connection.cursor() as cursor:
            sql = "INSERT INTO model_update_history (model_id, current_version, update_version) VALUES ('{}', '{}', '{}')".format(model_id, current_version, update_version)

            cursor.execute(sql)
            cursor.close()
            connection.close()