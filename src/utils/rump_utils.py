from src.enum.meat_enum import MeatEnum
from src.enum.rump_error_enum import ClassificationErrorRumpEnum
from src.enum.rump_enum import ClassificationRumpEnum
from src.enum.bruises_enum import BruisesEnum
from src.enum.rump_enum import ClassificationRumpEnum

class RumpUtils:

    @staticmethod
    def get_rump_id(rump_result):
        return MeatEnum[rump_result['label']].value['database_id']
        # return RumpEnum[].value



    @staticmethod
    def get_bruise_deviation(rump_is_bruised):
        bruise_deviation = None
        bruises = list(set(rump_is_bruised))



        has_failure = BruisesEnum.FALHA.value in bruises
        has_bruise_severe = BruisesEnum.GRAVE.value in bruises
        has_bruise_mild = BruisesEnum.LEVE.value in bruises
        has_bruise_moderate = BruisesEnum.MODERADA.value in bruises

        print(bruises)

        if has_failure and not (has_bruise_severe or has_bruise_mild or has_bruise_moderate):
            bruise_deviation = ClassificationErrorRumpEnum.ERRO_105.value
        elif (has_bruise_severe or has_bruise_mild or has_bruise_moderate) and not has_failure:
            bruise_deviation = ClassificationErrorRumpEnum.ERRO_104.value
        elif has_failure:
            bruise_deviation = ClassificationErrorRumpEnum.ERRO_106.value


        return bruise_deviation


    @staticmethod
    def classify_meat_deviation(classification_id, rump_id):

        classification_value = None
        rump_value = None

        for meat in MeatEnum:
            if meat.value['database_id'] == str(classification_id):
                classification_value = meat.value['model_id']

        for rump in ClassificationRumpEnum:
            if rump.value['database_id'] == str(rump_id):
                rump_value = rump.value['model_id']

        print(rump_value, classification_value)

        if rump_value:

            if classification_value == rump_value:
                return ClassificationRumpEnum.IN_COMPLIANCE.value['database_id']
            elif rump_value > classification_value:
                return ClassificationRumpEnum.POSITIVE.value['database_id']
            elif rump_value < classification_value:
                return ClassificationRumpEnum.NEGATIVE.value['database_id']

        else:
            if rump_id == ClassificationErrorRumpEnum.ERRO_104.value:
                return ClassificationRumpEnum.BRUISE.value['database_id']
            elif rump_id == ClassificationErrorRumpEnum.ERRO_105.value:
                return ClassificationRumpEnum.FAILURE.value['database_id']
            else:
                return ClassificationRumpEnum.FAILURE_BRUISE.value['database_id']