from enum import Enum


class ClassifierApiReturnMessagesEnum(Enum):
    SUCCESS = 'The image was processed successfully!'
    FAILURE = 'An error occurred when trying to process the waiting images!'
