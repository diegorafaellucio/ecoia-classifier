from src.enum.breed_enum import BreedEnum

class BreedUtils:

    @staticmethod
    def get_breed_id(breed_result):
        if breed_result['label'] == 'CARIMBO_ANGUS':
            return BreedEnum.ANGUS.value
        return 0