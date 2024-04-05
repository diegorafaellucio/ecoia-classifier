from django.db import connection
import re
class BruiseController:

    @staticmethod
    def get_color_by_bruise_id(bruise_id):
        with connection.cursor() as cursor:
            cursor.execute("select code from color where id = (select color_id from aux_bruise ab where ab.id = {})".format(bruise_id))
            results = cursor.fetchall()
            data = results[0][0]
            cursor.close()
            connection.close()
            return data

    @staticmethod
    def insert_into_bruise(image_id, bruise_id, cut_id, bruise_coordinates):
        with connection.cursor() as cursor:
            sql = "insert into bruise (bruise_id, image_id, cut_id, bruise_coordinates, created_at, updated_at) values ({}, {}, {}, '{}', now(), now())".format(
                    bruise_id, image_id, cut_id, bruise_coordinates)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results