from django.db import connection
import re


class CutsGradingController:

    @staticmethod
    def insert(image_id, aux_grading_id, cut_id):
        with connection.cursor() as cursor:
            sql = "insert into cuts_grading (image_id, aux_grading_id, cut_id) values ({}, {}, {})".format(
                image_id, aux_grading_id, cut_id)

            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results

    @staticmethod
    def update_correlation_information(image_id, meat_and_cut_correlation):
        with connection.cursor() as cursor:
            sql = "update cuts_grading set carcacass_cut_classification_correlation = '{}'  where image_id =  {};".format(
                meat_and_cut_correlation, image_id)

            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results