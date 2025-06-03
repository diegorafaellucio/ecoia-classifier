from django.db import connection
import re
class CutController:

    @staticmethod
    def insert(cut_id, image_id, coordinates):
        with connection.cursor() as cursor:
            sql = "insert into cut (cut_id, image_id, coordinates, created_at, updated_at) values ({}, {}, '{}', now(), now())".format(
                    cut_id, image_id, coordinates)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results

