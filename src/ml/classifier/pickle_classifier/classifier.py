import pickle

class Classifier():

    def __init__(self, weights_path):
        with open(weights_path,'rb') as file:
            self.model = pickle.load(file)


    def predict(self, image_features):

        results = self.model.predict(image_features)

        return results