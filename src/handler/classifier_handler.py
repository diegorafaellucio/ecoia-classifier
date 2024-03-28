from src.utils.detector_utils import DetectorUtils
class ClassifierHandler:


    @staticmethod
    def classify(detector, image):

        image_height, image_width = image.shape[:2]
        detection_results = detector.detect(image)
        best_result = DetectorUtils.get_best_detection(detection_results, image_height, image_width)

        return best_result
