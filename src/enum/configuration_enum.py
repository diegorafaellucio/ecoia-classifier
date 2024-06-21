from enum import Enum


from src.enum.detection_approach_enum import DetectionApproachEnum

class ConfigurationEnum(Enum):
    DEVICE = 'cpu'

    SKELETON_CLASSIFICATION_WEIGHTS_PATH = 'data/models/skeleton/weight.pt'
    SKELETON_CLASSIFICATION_APPROACH = DetectionApproachEnum.ULTRALYTICS.value

    FILTER_CLASSIFICATION_WEIGHTS_PATH = 'data/models/filter/weight.pt'
    FILTER_CLASSIFICATION_APPROACH = DetectionApproachEnum.ULTRALYTICS.value

    MEAT_CLASSIFICATION_WEIGHTS_PATH = 'data/models/meat/weight.pt'
    MEAT_CLASSIFICATION_APPROACH = DetectionApproachEnum.ULTRALYTICS.value

    SIDE_CLASSIFICATION_WEIGHTS_PATH = 'data/models/side/weight.pt'
    SIDE_CLASSIFICATION_APPROACH = DetectionApproachEnum.ULTRALYTICS.value

    BRUISE_CLASSIFICATION_WEIGHTS_PATH = 'data/models/bruise/weight.pt'
    BRUISE_CLASSIFICATION_APPROACH = DetectionApproachEnum.ULTRALYTICS.value

    STAMP_CLASSIFICATION_WEIGHTS_PATH = 'data/models/stamp/weight.pt'
    STAMP_CLASSIFICATION_APPROACH = DetectionApproachEnum.ULTRALYTICS.value

    SIDE_A_SHAPE_PREDICTOR_WEIGHTS_FILE_PATH = 'data/models/cuts/model_A.dat'
    SIDE_B_SHAPE_PREDICTOR_WEIGHTS_FILE_PATH = 'data/models/cuts/model_B.dat'

    FILTER_BLACK_LIST = ['VIRADA_TOTAL', 'VIRADA_PARCIAL', 'ANGULADA_COSTELA_BANDA_A', 'ANGULADA_COSTELA_BANDA_B']

    SYSTEM_VERSION = 'PROFESSIONAL'

    IMAGES_MAIN_PATH = '/home/ecotrace/fotos'

    IMAGES_ENDPOINT = 'http://localhost:3333/fotos'

    INTEGRATION_ENDPOINT = ''

    MAX_PROCESSING_ATTEMPTS = ''

    MAX_WORKERS = 5

    DETECTION_PADDING = 350

    BRUISE_CONFIDENCE_THRESHOLD = 0.20

    BRUISE_PLOT_RADIUS = 0.80

    WATERMARK_LOGO_PATH = 'data/images/watermark_logo.png'

    GENERATE_WATERMARK = 0

