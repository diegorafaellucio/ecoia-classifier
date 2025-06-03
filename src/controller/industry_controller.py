from django.db import connection
import re
class IndustryController:

    @staticmethod
    def get_industry_name():
        with connection.cursor() as cursor:
            cursor.execute("select concat(name, ' - ', surname) from industry")
            results = cursor.fetchall()
            industry_name = results[0][0]
            cursor.close()
            connection.close()
            return industry_name