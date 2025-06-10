import logging
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import traceback

import imutils

from src.controller.image_controller import ImageController
from src.controller.carcass_information_controller import CarcassInformationController
from src.controller.configuration_storage_controller import ConfigurationStorageController
from src.controller.cuts_grading_controller import CutsGradingController
from src.enum.conformation_enum import ConformationEnum
from src.enum.configuration_enum import ConfigurationEnum
from src.utils.file_utils import FileUtils
from src.utils.classifier_utils import ClassifierUtils
from src.utils.skeleton_size_utils import SkeletonSizeUtils
from src.utils.bruise_utils import BruiseUtils
from src.utils.cuts_utils import CutsUtils
from src.utils.watermark_utils import WatermarkUtils
from src.utils.grease_color_utils import GreaseColorUtils
from src.enum.image_state_enum import ImageStateEnum
from src.enum.system_version_enum import SystemVersionEnum
from src.enum.classification_error_enum import ClassificationErrorEnum
from src.enum.hump_enum import HumpEnum
from src.enum.cuts_enum import CutsEnum
from src.utils.hump_utils import HumpUtils
from src.utils.breed_utils import BreedUtils
import cv2



class UseModelHandler:
    logger = logging.getLogger(__name__)


    @staticmethod
    def predict(image, model_name, classifier_suite):
        """
        Process an image using the specified model from the classifier suite.
        
        Args:
            image: The image to process (OpenCV format)
            model_name: The name of the model to use for prediction
            classifier_suite: Dictionary containing all available models
            
        Returns:
            Dictionary with prediction results
        """
        UseModelHandler.logger.info(f'Processing image with model: {model_name}')
        
        # Check if the model exists in the classifier suite
        if model_name not in classifier_suite:
            UseModelHandler.logger.error(f'Model {model_name} not found in classifier suite')
            raise ValueError(f"Model '{model_name}' not found. Available models: {list(classifier_suite.keys())}")
        
        # Get the model from the classifier suite
        model = classifier_suite[model_name]
        
        # Handle special cases for different model types
        if model_name == 'cuts_classification_models':
            # For cuts models, we need to specify which cut model to use
            raise ValueError("For cuts classification, please specify the cut type in the format: 'cuts_classification_models.CUT_TYPE'")
        
        elif '.' in model_name:
            # Handle nested models like cuts_classification_models.PICANHA
            parts = model_name.split('.')
            if len(parts) != 2:
                raise ValueError(f"Invalid model name format: {model_name}")
            
            parent_model = classifier_suite.get(parts[0])
            if not parent_model:
                raise ValueError(f"Parent model '{parts[0]}' not found")
            
            if parts[0] == 'cuts_classification_models':
                # Get the specific cut model
                cut_type = parts[1]
                if cut_type not in parent_model:
                    raise ValueError(f"Cut type '{cut_type}' not found. Available cuts: {list(parent_model.keys())}")
                
                model = parent_model[cut_type]
            else:
                raise ValueError(f"Nested model access not supported for '{parts[0]}'")
        
        # Process the image based on the model type
        try:

            if 'classifier' in model_name:
                result = model.predict(image, image_classification=True)
            else:
                result = model.predict(image)
            
            return {
                'model_name': model_name,
                'result': result
            }
            
        except Exception as e:
            UseModelHandler.logger.error(f'Error processing image with model {model_name}: {str(e)}')
            raise Exception(f"Error processing image with model {model_name}: {str(e)}")
