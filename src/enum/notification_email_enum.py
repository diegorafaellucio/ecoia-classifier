from enum import Enum

class NotificationEmailEnum(Enum):
    IS_NOT_POSSIBLE_TO_CONNECT_ON_PLC = 'Não foi possível conectar ao PLC'
    LAST_CAPTURED_IMAGES_DO_NOT_HAVE_ANY_ANIMAL = 'LAST_CAPTURED_IMAGES_DO_NOT_HAVE_ANY_ANIMAL'
    IS_NOT_POSSIBLE_TO_GET_IMAGE_FROM_CAMERA = 'Não foi possível pegar imagens da câmera'
    IS_NOT_POSSIBLE_TO_CONNECT_WITH_CAMERA = 'Não foi possível conectar com a câmera'
