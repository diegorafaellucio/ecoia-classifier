import time

def classification_processor_job():
    # your functionality goes here
    import requests

    url = "http://127.0.0.1:8000/meat-classifier"

    payload = {}
    headers = {}

    counter = 0

    while counter < 15:

        counter += 1

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        time.sleep(4)


def integrator_processor_job():
    # your functionality goes here
    import requests

    url = "http://127.0.0.1:8000/integrator"

    payload = {}
    headers = {}

    counter = 0

    while counter < 15:

        counter += 1

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        time.sleep(4)


