import json

from django.db import connection
from src.enum.configuration_enum import ConfigurationEnum
from src.utils.configuration_utils import ConfigurationUtils
import re
class ConfigurationStorageController:


    @staticmethod
    def initialize_configs():

        with connection.cursor() as cursor:
            for key, value in ConfigurationUtils.config_dict.items():
                has_config_counter = ConfigurationStorageController.has_config(key)
                if has_config_counter == 0:
                    value = json.dumps(value)
                    default_query = "INSERT INTO configuration_storage (type, value) VALUES ('{}', '{}');".format(key, value)
                    cursor.execute(default_query)
            cursor.close()
            connection.close()

    @staticmethod
    def get_config_data_value(config_type):
        with connection.cursor() as cursor:
            cursor.execute("select value from configuration_storage where type = '{}'".format(config_type))
            results = cursor.fetchall()
            data  = results[0][0]
            cursor.close()
            connection.close()
            return json.loads(data)

    @staticmethod
    def has_config(config_type):
        with connection.cursor() as cursor:
            cursor.execute("select count(*) from configuration_storage where type = '{}'".format(config_type))
            results = cursor.fetchall()
            data = results[0][0]
            cursor.close()
            return data



