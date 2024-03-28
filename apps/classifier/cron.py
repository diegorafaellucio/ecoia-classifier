import time

def classification_processor_job():
    # your functionality goes here
    with open("/home/diego/Dropbox/Projects/PycharmProjects/Eco/novo_classificador/output_cron.txt", 'a') as file1:
        file1.write('teste')
        execution_counter = 120
        # while True:
        #     # TODO face algo
        #     pass
        # time.sleep(0.5)