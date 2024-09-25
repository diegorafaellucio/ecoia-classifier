import requests
import time

def routine_classifier():
    url= "http://classifier:8000/meat-classifier"
    payload = {}
    headers = {}

    counter = 0

    while counter < 15:

        counter += 1

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        time.sleep(4)

def routine_imtegrator():
    url = "http://classifier:8000/integrator"

    payload = {}
    headers = {}

    counter = 0

    while counter < 1:

        counter += 1

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        # time.sleep(4)

while(True):
    routine_classifier()
    routine_imtegrator()