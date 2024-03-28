from src.enum.configuration_enum import ConfigurationEnum

class ConfigurationUtils:
    config_dict = {
        ConfigurationEnum.DEVICE.name: 'cpu',

        ConfigurationEnum.SKELETON_CLASSIFICATION_WEIGHTS_PATH.name: './data/detector/skeleton/weight.pt',
        ConfigurationEnum.FILTER_CLASSIFICATION_WEIGHTS_PATH.name: './data/detector/filter/weight.pt',
        ConfigurationEnum.MEAT_CLASSIFICATION_WEIGHTS_PATH.name: './data/detector/meat/weight.pt',
        ConfigurationEnum.SIDE_CLASSIFICATION_WEIGHTS_PATH.name: './data/detector/side/weight.pt',
        ConfigurationEnum.BRUISE_CLASSIFICATION_WEIGHTS_PATH.name: './data/detector/bruise/weight.pt',

        ConfigurationEnum.SIDE_A_SHAPE_PREDICTOR_WEIGHTS_FILE_PATH.name: './data/shape_predictor/model_A.dat',
        ConfigurationEnum.SIDE_B_SHAPE_PREDICTOR_WEIGHTS_FILE_PATH.name: './data/shape_predictor/model_B.dat',

        ConfigurationEnum.FILTER_BLACK_LIST.name: ['VIRADA_TOTAL', 'VIRADA_PARCIAL', 'ANGULADA_COSTELA_BANDA_A', 'ANGULADA_COSTELA_BANDA_b'],

        ConfigurationEnum.SYSTEM_VERSION.name: 'PROFESSIONAL',

        ConfigurationEnum.IMAGES_MAIN_PATH.name: '/home/ecotrace/fotos',

        ConfigurationEnum.IMAGES_ENDPOINT.name: 'http://localhost:3333/fotos',

        ConfigurationEnum.INTEGRATION_ENDPOINT.name: '',

        ConfigurationEnum.MAX_PROCESSING_ATTEMPTS.name: '',

        ConfigurationEnum.MAX_WORKERS.name: 5,

        ConfigurationEnum.DETECTION_PADDING.name: 350,

    }
