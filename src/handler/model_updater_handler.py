import logging
from src.utils.model_utils import ModelUtils


class ModelUpdaterHandler:
    logger = logging.getLogger(__name__)

    @staticmethod
    def update():
        ModelUtils.update_models()



