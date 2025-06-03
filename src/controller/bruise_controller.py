from django.db import connection
import re


class BruiseController:

    @staticmethod
    def insert(image_id, bruise_id, cut_id, bruise_coordinates, width, height, diameter):
        with connection.cursor() as cursor:
            sql = "insert into bruise (bruise_id, image_id, cut_id, bruise_coordinates, created_at, updated_at, height, width, diameter) values ({}, {}, {}, '{}', now(), now(), {}, {}, {})".format(
                bruise_id, image_id, cut_id, bruise_coordinates, height, width, diameter)

            cursor.execute(sql)
            cursor.close()
            connection.close()

    @staticmethod
    def get_color_by_bruise_id(bruise_id):
        with connection.cursor() as cursor:
            cursor.execute(
                "select code from color where id = (select color_id from aux_bruise ab where ab.id = {})".format(
                    bruise_id))
            results = cursor.fetchall()
            data = results[0][0]
            cursor.close()
            connection.close()
            return data

    @staticmethod
    def insert_into_bruise(image_id, bruise_id, cut_id, cut_intersection_score, bruise_coordinates, region_code_bruise,
                           width=None, height=None, diameter=None, bruise_level_id=None):
        with connection.cursor() as cursor:

            if width == None and height == None and diameter == None and bruise_level_id == None:
                sql = "insert into bruise (bruise_id, image_id, cut_id, cut_intersection_score, bruise_coordinates, created_at, updated_at, region_bruise_code) values ({}, {}, {}, '{}', '{}', now(), now(),'{}')".format(
                    bruise_id, image_id, cut_id, cut_intersection_score, bruise_coordinates, region_code_bruise)
            else:
                sql = "insert into bruise (bruise_id, image_id, cut_id, cut_intersection_score, bruise_coordinates, created_at, updated_at, height, width, diameter, bruise_level_id, region_bruise_code) values ({}, {}, {},'{}', '{}', now(), now(), {}, {}, {}, {},'{}')".format(
                    bruise_id, image_id, cut_id, cut_intersection_score, bruise_coordinates, height, width, diameter,
                    bruise_level_id, region_code_bruise)

            print(sql)
            cursor.execute(sql)
            cursor.close()
            connection.close()

    @staticmethod
    def get_by_image_id(image_id):
        with connection.cursor() as cursor:
            sql = "select * from bruise where image_id =  '{}';".format(image_id)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results

    def get_only_greatest_intersection_bruises_by_image_id(image_id):
        with connection.cursor() as cursor:
            sql = """
                SELECT b.*
                FROM bruise b
                JOIN (
                    SELECT image_id, bruise_coordinates, MAX(cut_intersection_score) AS max_score
                    FROM bruise
                    WHERE image_id = '{}'
                    GROUP BY image_id, bruise_coordinates
                ) AS sub
                ON b.image_id = sub.image_id
                AND b.bruise_coordinates = sub.bruise_coordinates
                AND b.cut_intersection_score = sub.max_score
                WHERE b.image_id = '{}';
            """.format(image_id, image_id)

            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results

    @staticmethod
    def get_cuts_affectd_by_image_id_and_region_code(image_id, region_code_id):
        with connection.cursor() as cursor:
            sql = "select * from bruise where image_id =  '{}' and region_bruise_code = '{}';".format(image_id,
                                                                                                      region_code_id)

            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results
