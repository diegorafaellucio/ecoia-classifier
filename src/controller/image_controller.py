from django.db import connection, transaction
from src.enum.image_state_enum import ImageStateEnum
import re


class ImageController:

    @staticmethod
    def get_images_to_classify(limit):
        with connection.cursor() as cursor:
            sql = 'select id, path, sequence_nr, side_nr, aux_grading_id from image where state in  ({}) and flag_img = 1 order by id asc limit {};'.format(
                ImageStateEnum.WAITING_PROCESSING.value, limit)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results

    @staticmethod
    def get_amount_of_images_by_state(state):
        with connection.cursor() as cursor:
            sql = 'select count(*) from image where state = {};'.format(
                state)
            cursor.execute(sql)
            results = cursor.fetchone()
            cursor.close()
            connection.close()
            return results[0]

    @staticmethod
    def get_to_integrate(limit, send_93_error_information=False):
        with transaction.atomic():
            with connection.cursor() as cursor:

                if send_93_error_information:
                    sql = 'select id, path, sequence_nr, side_nr, roulette_id, slaughter_dt, created_at , processed_at, flag_img, state, aux_grading_id from image where state in  ({}) and flag_img = 1 order by id asc limit {}; '.format(
                    ImageStateEnum.WAITING_INTEGRATION.value,
                    limit)

                else:

                    sql = 'select id, path, sequence_nr, side_nr, roulette_id, slaughter_dt, created_at , processed_at, flag_img, state, aux_grading_id from image where state in  ({}) and flag_img = 1 and aux_grading_id != 13 order by id asc limit {}; '.format(
                        ImageStateEnum.WAITING_INTEGRATION.value,
                        limit)

                cursor.execute(sql)
                results = cursor.fetchall()
                cursor.close()
                connection.close()
                return results

    @staticmethod
    def update_status(status, image_id):
        with connection.cursor() as cursor:
            query = "update image set state = '{}', processed_at = now()  where id = '{}'".format(status, image_id)
            cursor.execute(query)
            cursor.close()
            connection.close()

    @staticmethod
    def update_side_information(classification, image_id):
        with connection.cursor() as cursor:
            query = "update image set aux_side_id = '{}'  where id = '{}'".format(classification, image_id)
            cursor.execute(query)
            cursor.close()
            connection.close()

    @staticmethod
    def update_filter_data(filter_label, filter_confidence, image_id):
        with connection.cursor() as cursor:
            query = "update image set filter_label = '{}', filter_confidence = '{}', processed_at = now()  where id = '{}'".format(
                filter_label, filter_confidence, image_id)
            cursor.execute(query)
            cursor.close()
            connection.close()

    @staticmethod
    def update_classification(classification, image_id):
        with connection.cursor() as cursor:
            query = "update image set aux_grading_id = '{}'  where id = '{}'".format(classification, image_id)
            cursor.execute(query)
            cursor.close()
            connection.close()

    @staticmethod
    def update_carcass_detection_confidence(carcass_detection_confidence, image_id):
        with connection.cursor() as cursor:
            query = "update image set update_carcass_detection_confidence = '{}'  where id = '{}'".format(
                carcass_detection_confidence, image_id)
            cursor.execute(query)
            cursor.close()
            connection.close()

    @staticmethod
    def upadte_carcass_intersection(intersection_score, image_id):
        with connection.cursor() as cursor:
            query = "update image set carcass_intersection = '{}'  where id = '{}'".format(
                intersection_score, image_id)
            cursor.execute(query)
            cursor.close()
            connection.close()
