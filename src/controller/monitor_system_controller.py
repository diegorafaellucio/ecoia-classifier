from django.db import connection

class MonitorSystem:
    @staticmethod
    def insert_data_restart_system(application_name):
        with connection.cursor() as cursor:
            sql = "insert into monitor_restart_system (application) values ('{}');".format(application_name)

            cursor.execute(sql)
            cursor.close()
            connection.close()