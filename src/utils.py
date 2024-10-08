import pandas as pd
import numpy as np
import os
import sys
from src.exception import CustomException
import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from src.logger import logging

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}
        for model_name, model in models.items():
            logging.info(f"Evaluating model: {model_name}")
            if model_name in param:
                para = param[model_name]
                logging.info(f"Using parameters: {para}")
                gs = GridSearchCV(model, para, cv=3)
                gs.fit(X_train, y_train)
                best_params = gs.best_params_
                logging.info(f"Best parameters: {best_params}")
                model.set_params(**best_params)
            else:
                logging.warning(f"No parameters found for model: {model_name}, using default settings.")

            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score
            logging.info(f"Model {model_name}: Train R2: {train_model_score}, Test R2: {test_model_score}")

        return report
    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
        
        try:
            with open (file_path,'rb')as file_obj:
                return dill.load(file_obj)
        except CustomException as e:

            raise CustomException(e,sys)