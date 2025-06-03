from django.db import connection
from src.enum.image_state_enum import ImageStateEnum
import re


class ModelController:

    @staticmethod
    def get_models_without_current_version():
        with connection.cursor() as cursor:
            sql = 'select * from aux_model where current_version is null;'

            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results


    @staticmethod
    def is_model_in_database(model):
        with connection.cursor() as cursor:
            sql = "select * from aux_model where name = '{}' and current_version is not null;".format(model)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()

            if len(results) > 0:
                return True
            else:
                return False

    @staticmethod
    def insert(model_name, model_version, model_weight_path, model_approach):
        with connection.cursor() as cursor:
            sql = "INSERT INTO aux_model (name, current_version, path, approach, created_at, updated_at) VALUES ('{}', '{}', '{}', '{}', DEFAULT, DEFAULT)".format(model_name, model_version, model_weight_path, model_approach)

            cursor.execute(sql)
            cursor.close()
            connection.close()

    @staticmethod
    def get_id(model_name):
        with connection.cursor() as cursor:
            sql = "select id, current_version from aux_model where name = '{}'".format(model_name)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()

            return results[0][0]

    @staticmethod
    def update_version( new_version, model):
        with connection.cursor() as cursor:
            sql = "update aux_model set current_version =  '{}', updated_at =  now() where name = '{}'".format(new_version, model)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()

    @staticmethod
    def get_current_version(model):
        with connection.cursor() as cursor:
            sql = "select current_version from aux_model where name = '{}'".format(model)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            connection.close()

            return results[0][0]

