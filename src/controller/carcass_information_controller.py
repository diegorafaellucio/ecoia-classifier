from django.db import connection
import re
class CarcassInformationController:

    @staticmethod
    def carcass_information_already_exists(image_id):
        with connection.cursor() as cursor:
            cursor.execute("select * from carcass_information where image_id = '{}'".format(image_id))
            results = cursor.fetchall()

            if len(results) > 0:
                return True
            else:
                return False

    @staticmethod
    def initialize_carcass_information(image_id):
        with connection.cursor() as cursor:
            sql = "INSERT INTO carcass_information (image_id, height, width, aux_fat_color_id, aux_conformation_id, color_id, size, created_at, updated_at, aux_maturity_id, aux_ox_termite_id, aux_race_id) VALUES ({}, null, null, null, null, null, null, DEFAULT, DEFAULT, null, null, null)".format(
                image_id)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results
    @staticmethod
    def update_grease_color(image_id, grease_color_id):
        with connection.cursor() as cursor:
            sql = "UPDATE carcass_information t SET t.aux_fat_color_id = '{}' WHERE t.image_id = '{}'".format(
                    grease_color_id, image_id)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results

    @staticmethod
    def update_conformation(image_id, conformation_id):
        with connection.cursor() as cursor:
            sql = "UPDATE carcass_information t SET t.aux_conformation_id = '{}' WHERE t.image_id = '{}'".format(
                conformation_id, image_id)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results

    @staticmethod
    def update_width(image_id, width):
        with connection.cursor() as cursor:
            sql = "UPDATE carcass_information t SET t.width = '{}' WHERE t.image_id = '{}'".format(
                width, image_id)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results

    @staticmethod
    def update_height(image_id, height):
        with connection.cursor() as cursor:
            sql = "UPDATE carcass_information t SET t.height = '{}' WHERE t.image_id = '{}'".format(
                height, image_id)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results

    @staticmethod
    def update_size_descriptor(image_id, size_descriptor):
        with connection.cursor() as cursor:
            sql = "UPDATE carcass_information t SET t.size = '{}' WHERE t.image_id = '{}'".format(
                size_descriptor, image_id)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results