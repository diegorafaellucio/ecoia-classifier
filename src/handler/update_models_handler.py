import logging
from src.utils.aux_model_utils import AuxModelUtils


class UpdateModelsHandler:
    logger = logging.getLogger(__name__)

    @staticmethod
    def update():
        AuxModelUtils.update_models()



