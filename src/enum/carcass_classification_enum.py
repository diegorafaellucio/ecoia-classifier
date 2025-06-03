from enum import Enum

class CarcassClassificationEnum(Enum):
    WITH_CARCASS = ('1', 'WITH_CARCASS')
    WITHOUT_CARCASS = ('2', 'WITHOUT_CARCASS')

    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @classmethod
    def get_value(cls, key):
        for item in cls:
            if item.key == key:
                return item.value
        raise KeyError(f'Key {key} not found in ConfigurationEnum.')
