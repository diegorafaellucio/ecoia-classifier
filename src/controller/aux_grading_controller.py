from django.db import connection
from src.enum.image_state_enum import ImageStateEnum
import re


class AuxGradingController:

    @staticmethod
    def get_score_by_id(id):
        with connection.cursor() as cursor:
            sql = "select score from aux_grading where id = '{}';".format(id)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()

            score = results[0][0]
            return score

    @staticmethod
    def get_name_by_id(id):
        with connection.cursor() as cursor:
            sql = "select name from aux_grading where id = '{}';".format(id)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()

            name = results[0][0]
            return name



