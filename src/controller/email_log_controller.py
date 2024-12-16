from django.db import connection
import traceback
import re
class EmailLogController:
    @staticmethod
    def insert(email_type, email_message):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO notification_email (email_type, email_message) VALUES (%s, %s);"
                cursor.execute(sql, (email_type, email_message))
                cursor.close()
                connection.close()
                return True
        except:
            exception_info = traceback.format_exc()
            print("An error occurred trying to send email:\n {}".format(exception_info))
            return False