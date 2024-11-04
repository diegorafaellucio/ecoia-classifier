from enum import Enum


class CutAndMeatClassificationCorrelationEnum(Enum):
    POSITIVE = ("POSITIVE", "POSITIVE")
    NEGATIVE = ("NEGATIVE", "POSITIVE")
    IN_COMPLIANCE = ("IN_COMPLIANCE", "IN_COMPLIANCE")

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
