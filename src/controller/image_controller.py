from django.db import connection
from src.enum.image_state_enum import ImageStateEnum
import re


class ImageController:

    @staticmethod
    def get_images_to_classify(limit):
        with connection.cursor() as cursor:
            sql = 'select id, path, sequence_nr, side_nr, roulette_id, slaughter_dt, created_at , processed_at, flag_img, state, aux_grading_id from image where state in  ({}) and flag_img = 1 order by id asc limit {};'.format(
                ImageStateEnum.WAITING_PROCESSING.value, limit)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results

    @staticmethod
    def get_images_to_integrate(limit):
        with connection.cursor() as cursor:
            sql = 'select id, path, sequence_nr, side_nr, roulette_id, slaughter_dt, created_at , processed_at, flag_img, state, aux_grading_id from image where state in  ({}) and flag_img = 1 order by id asc limit {};'.format(
                ImageStateEnum.WAITING_INTEGRATION.value,
                limit)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results

    @staticmethod
    def update_image_status(status, image_id):
        with connection.cursor() as cursor:
            query = "update image set state = '{}'  where id = '{}'".format(status, image_id)
            cursor.execute(query)
            cursor.close()
            connection.close()

    @staticmethod
    def update_side_classification_data(classification, image_id):
        with connection.cursor() as cursor:
            query = "update image set aux_grading_id = '{}'  where id = '{}'".format(classification, image_id)
            cursor.execute(query)
            cursor.close()
            connection.close()

    @staticmethod
    def update_filter_classification_data(filter_label, filter_confidence, image_id):
        with connection.cursor() as cursor:
            query = "update image set filter_label = '{}', filter_confidence = '{}'  where id = '{}'".format(
                filter_label, filter_confidence, image_id)
            cursor.execute(query)
            cursor.close()
            connection.close()

    @staticmethod
    def update_image_classification(classification, image_id):
        with connection.cursor() as cursor:
            query = "update image set aux_grading_id = '{}'  where id = '{}'".format(classification, image_id)
            cursor.execute(query)
            cursor.close()
            connection.close()

    # @staticmethod
    # def get_new_image_data_py():
    #     with connection.cursor() as cursor:
    #         cursor.execute('select func_insert_img_no_id_py()')
    #         results = cursor.fetchall()
    #         new_image_data = results[0][0]
    #         cursor.close()
    #         connection.close()
    #         return new_image_data
    #
    # @staticmethod
    # def get_new_image_data_by_seq_and_side(sequence_number, side):
    #     with connection.cursor() as cursor:
    #
    #         query = "select func_insert_img_seq_side('{}', '{}', 110)".format(sequence_number, side)
    #         cursor.execute(query)
    #         results = cursor.fetchall()
    #         new_image_data  = results[0][0]
    #         cursor.close()
    #         connection.close()
    #         return new_image_data
    #
    #
    # @staticmethod
    # def update_image_set_has_image(image_name):
    #     with connection.cursor() as cursor:
    #         query = "update image set flag_img = 1  where path like '%{}%'".format(image_name)
    #         cursor.execute(query)
    #         cursor.close()
    #         connection.close()
    #
    # @staticmethod
    # def update_image_if_has_error(image_name):
    #     with connection.cursor() as cursor:
    #         regex = r'^(\d{4})(\d{2})(\d{2})-(\d{4})-(\d)-(\d{4})-(\d{4})\.jpg$'
    #         if re.match(regex, image_name):
    #             query = "update image set flag_img = 1, state = 0 where path like '%{}%'".format(image_name)
    #             cursor.execute(query)
    #             cursor.close()
    #             connection.close()
    #
    #
