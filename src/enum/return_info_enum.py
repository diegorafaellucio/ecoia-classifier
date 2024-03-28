from enum import Enum
# from modules.enum.system_status import SystemStatus
# from modules.enum.return_type import ReturnType

class ReturnInfo(Enum):

    # @classmethod
    # def get_all_info(cls):
    #     return list(map(lambda c: c.value, cls))
    #
    # @classmethod
    # def get_all_error_info_codes(cls):
    #     all_info = cls.get_all_info()
    #
    #     error_codes = [info[0] for info in all_info if info[2] == SystemStatus.FAILURE.value]
    #
    #     return error_codes
    #
    # @classmethod
    # def get_all_success_info_codes(cls):
    #     all_info = cls.get_all_info()
    #
    #     error_codes = [info[0] for info in all_info if info[2] == SystemStatus.SUCCESS.value]
    #
    #     return error_codes


    FILE_NOT_FOUND = 91, 'Arquivo não encontrado.'
    IS_NOT_POSSIBLE_TO_OBTAIN_A_PRE_FILTER_RESULT = 95, 'Não foi possivel identificar a orientação da carcaça.'
    IS_NOT_POSSIBLE_TO_CLASSIFY_THE_INPUT_IMAGE = 96, 'Não foi possivel classificar a carcaça.'
    ROTATED_SKELETON_IS_FOUND = 97, 'A carcaça detectada apresenta rotação.'





if __name__ == '__main__':
    print(ReturnInfo.FILE_NOT_FOUND.value)