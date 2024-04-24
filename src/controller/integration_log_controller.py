from django.db import connection
import re
class IntegrationLogController:


    @staticmethod
    def insert_into_integration_log(image_id, return_code, elapsed_time, integration_string):
        with connection.cursor() as cursor:
            sql = "insert into integration_log (return_code, elapsed_time, image_id, integration_string, created_at, updated_at) values ({}, {}, {}, '{}', now(), now())".format(
                    return_code, elapsed_time, image_id, integration_string)
            cursor.execute(sql)
            cursor.close()
            connection.close()
