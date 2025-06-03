from django.db import connection
import re
class IntegrationLogController:


    @staticmethod
    def insert(image_id, return_code, elapsed_time, integration_string):
        with connection.cursor() as cursor:
            sql = "insert into integration_log (return_code, elapsed_time, image_id, integration_string, created_at, updated_at) values ({}, {}, {}, '{}', now(), now())".format(
                    return_code, elapsed_time, image_id, integration_string)
            cursor.execute(sql)
            cursor.close()
            connection.close()

    @staticmethod
    def has_integration_to_image(image_id):
        with connection.cursor() as cursor:
            sql = "select count(*) from integration_log where image_id = {}".format(
                image_id)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()

            if results[0][0] == 0:
                return False
            else:
                return True


