from django.db import connection
import re


class CutsGradingController:

    @staticmethod
    def insert(image_id, aux_grading_id, cut_id, meat_and_cut_correlation):
        with connection.cursor() as cursor:
            sql = "insert into cuts_grading (image_id, aux_grading_id, cut_id, carcacass_cut_classification_correlation) values ({}, {}, {}, '{}')".format(
                image_id, aux_grading_id, cut_id, meat_and_cut_correlation)

            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results
