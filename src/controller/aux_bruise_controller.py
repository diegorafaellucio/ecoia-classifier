from django.db import connection
from src.enum.image_state_enum import ImageStateEnum
import re


class AuxBruiseController:

    @staticmethod
    def get_name_by_id(id):
        with connection.cursor() as cursor:
            sql = "select description from aux_bruise where id = '{}';".format(id)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            name = results[0][0]
            return name



