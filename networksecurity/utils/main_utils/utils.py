import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import yaml
import numpy as np
from sklearn.metrics import r2_score
import pickle
from sklearn.model_selection import GridSearchCV

def read_yaml_file(filepath)->object:
    try:
        with open(filepath, 'rb') as yaml_content:
            return yaml.safe_load(yaml_content)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def write_yaml_file(savepath:str, content:object, replace:bool=False)-> None:
    """
    writes yaml content to create drift report 
    
    """
    try:
        if replace:
            if os.path.exists(savepath): os.remove(savepath)
        os.makedirs(os.path.dirname(savepath), exist_ok=True)
        with open(savepath, "w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_numpy_array(filepath:str,arr:np.array)->None:
    try:
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path, exist_ok=True)
        with open(filepath, "wb") as f:
            np.save(f,arr)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def load_numpy_array(filepath)->np.array:
    try:
        with open(filepath, "rb") as f:
            arr= np.load(filepath)
        return arr
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_object(filepath:str, obj:object)-> None:
    try:
        with open(filepath, 'wb') as file:
            pickle.dump(obj=obj, file=file)
    except Exception as e:
        NetworkSecurityException(e, sys)

def load_object(filepath)->object:
    try:
        with open(filepath, 'rb') as f:
            obj = pickle.load(f)
        return obj
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    


def evaluate_model(X_train,y_train,X_test,y_test,models:dict, params:dict)->object:
    """
    evaluates the best model from the given dict of models and dict of params

    params:
        models = a dictionary of all models
        params = params of all models for grid search cv 
    
    """
    try:
        report = {}
        for i in range(len(list(models.values()))):
            model_name = list(models.keys())[i]

            model = list(models.values())[i]
            model_param = params[model_name]

            logging.info("entering grid search cv")
            gs = GridSearchCV(estimator=model, param_grid=model_param)
            gs.fit(X_train, y_train)
            logging.info(f"grid search cv completed for model {model_name} best params are {gs.best_params_}")

            model.set_params(**gs.best_params_)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score

        return report

    except Exception as e:
        raise NetworkSecurityException(e, sys)