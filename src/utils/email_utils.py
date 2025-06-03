from httplib2 import Http
from json import dumps
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.enum.configuration_enum import ConfigurationEnum
from src.controller.industry_controller import IndustryController
from src.controller.email_log_controller import EmailLogController


class EmailUtils():
    @staticmethod
    def send_email(email_body, email_title, email_type):
        industry = IndustryController.get_industry_name()
        token = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.CHAT_TOKEN.name)
        space = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.CHAT_SPACE.name)

        url = "https://chat.googleapis.com/v1/spaces/{}/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token={}".format(space, token)

        subject = "*{}* | *{}*".format(industry, email_title)

        try:
            app_message = {"text": subject + '\n \n' + email_body}

            message_headers = {"Content-Type": "application/json; charset=UTF-8"}
            http_obj = Http()

            _, _ = http_obj.request(
                uri=url,
                method="POST",
                headers=message_headers,
                body=dumps(app_message),
            )

            print(EmailLogController.insert(email_type, email_body))
        except Exception as e:
            print('Erro ao enviar e-mail: ', e)
