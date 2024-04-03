from src.enum.configuration_enum import ConfigurationEnum
from src.enum.detection_approach_enum import DetectionApproachEnum

class ConfigurationUtils:
    detection_approach_default = DetectionApproachEnum.ULTRALYTICS.value

    config_dict = {
        ConfigurationEnum.DEVICE.name: 'cpu',

        ConfigurationEnum.SKELETON_CLASSIFICATION_WEIGHTS_PATH.name: './data/models/skeleton/weight.pt',
        ConfigurationEnum.SKELETON_CLASSIFICATION_APPROACH.name: detection_approach_default,

        ConfigurationEnum.FILTER_CLASSIFICATION_WEIGHTS_PATH.name: './data/models/filter/weight.pt',
        ConfigurationEnum.FILTER_CLASSIFICATION_APPROACH.name: detection_approach_default,

        ConfigurationEnum.MEAT_CLASSIFICATION_WEIGHTS_PATH.name: './data/models/meat/weight.pt',
        ConfigurationEnum.MEAT_CLASSIFICATION_APPROACH.name: detection_approach_default,

        ConfigurationEnum.SIDE_CLASSIFICATION_WEIGHTS_PATH.name: './data/models/side/weight.pt',
        ConfigurationEnum.SIDE_CLASSIFICATION_APPROACH.name: detection_approach_default,

        ConfigurationEnum.BRUISE_CLASSIFICATION_WEIGHTS_PATH.name: './data/models/bruise/weight.pt',
        ConfigurationEnum.BRUISE_CLASSIFICATION_APPROACH.name: detection_approach_default,

        ConfigurationEnum.STAMP_CLASSIFICATION_WEIGHTS_PATH.name: './data/models/stamp/weight.pt',
        ConfigurationEnum.STAMP_CLASSIFICATION_APPROACH.name: detection_approach_default,

        ConfigurationEnum.SIDE_A_SHAPE_PREDICTOR_WEIGHTS_FILE_PATH.name: './data/modes/cuts/model_A.dat',
        ConfigurationEnum.SIDE_B_SHAPE_PREDICTOR_WEIGHTS_FILE_PATH.name: './data/modes/cuts/model_B.dat',

        ConfigurationEnum.FILTER_BLACK_LIST.name: ['VIRADA_TOTAL', 'VIRADA_PARCIAL', 'ANGULADA_COSTELA_BANDA_A', 'ANGULADA_COSTELA_BANDA_B'],

        ConfigurationEnum.SYSTEM_VERSION.name: 'PROFESSIONAL',

        ConfigurationEnum.IMAGES_MAIN_PATH.name: '/home/ecotrace/fotos',

        ConfigurationEnum.IMAGES_ENDPOINT.name: 'http://localhost:3333/fotos',

        ConfigurationEnum.INTEGRATION_ENDPOINT.name: '',

        ConfigurationEnum.MAX_PROCESSING_ATTEMPTS.name: '',

        ConfigurationEnum.MAX_WORKERS.name: 5,

        ConfigurationEnum.DETECTION_PADDING.name: 350,

    }
