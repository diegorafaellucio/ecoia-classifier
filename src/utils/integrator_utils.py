import logging
import time
import requests
import traceback


class IntegratorUtils:
    logger = logging.getLogger(__name__)

    @staticmethod
    def integrate_data(integration_endpoint, integration_string):
        integration_start = time.time()
        try:

            return_data = requests.post(integration_endpoint, data=integration_string, timeout=7)
            integration_stop = time.time()
            return_code = return_data.status_code

            elapsed_time = integration_stop - integration_start



        except Exception as ex:
            # traceback.print_exc()
            integration_stop = time.time()
            return_code = '503'
            elapsed_time = integration_stop - integration_start

        return return_code, elapsed_time
