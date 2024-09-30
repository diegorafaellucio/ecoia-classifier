from enum import Enum
# from modules.enum.system_status import SystemStatus
# from modules.enum.return_type import ReturnType

class ReturnInfo(Enum):

    FILE_NOT_FOUND = 91, 'Arquivo não encontrado.'
    IS_NOT_POSSIBLE_TO_OBTAIN_A_PRE_FILTER_RESULT = 95, 'Não foi possivel identificar a orientação da carcaça.'
    IS_NOT_POSSIBLE_TO_CLASSIFY_THE_INPUT_IMAGE = 96, 'Não foi possivel classificar a carcaça.'
    ROTATED_SKELETON_IS_FOUND = 97, 'A carcaça detectada apresenta rotação.'



