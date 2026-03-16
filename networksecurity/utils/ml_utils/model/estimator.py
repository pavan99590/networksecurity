from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def predict(self, x):
        try:
            # Transform input features using the saved preprocessor
            transformed_feature = self.preprocessor.transform(x)
            
            # Generate predictions using the trained model
            y_hat = self.model.predict(transformed_feature)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def __repr__(self):
        return f"NetworkModel(model={self.model})"

    def __str__(self):
        return f"NetworkModel(model={self.model})"