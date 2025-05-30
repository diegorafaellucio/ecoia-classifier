from enum import Enum


class ClassifierApiReturnMessagesEnum(Enum):
    SUCCESS = 'The waiting images was processed successfully!'
    FAILURE = 'An error occurred when trying to process the waiting images!'
