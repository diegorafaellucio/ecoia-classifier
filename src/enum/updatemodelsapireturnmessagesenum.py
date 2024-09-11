from enum import Enum


class UpdateModelsApiReturnMessagesEnum(Enum):
    SUCCESS = 'All the models with new available versions were successfully updated!'
    FAILURE = 'An error occurred when trying update the models with new available versions!'
