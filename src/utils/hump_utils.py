from src.enum.hump_enum import HumpEnum
class HumpUtils:

    @staticmethod
    def get_hump_id(hump_result):
        if hump_result:
            return HumpEnum.PRESENTE.value
        return HumpEnum.AUSENTE.value
