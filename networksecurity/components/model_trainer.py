from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

import os
import sys
import pandas as pd
import numpy as np

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.utils.main_utils.utils import load_numpy_array, load_object, save_object, evaluate_model
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_metric
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier 
)
import mlflow
# import dagshub
# dagshub.init(repo_owner='gops26', repo_name='networksecurity', mlflow=True)

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact, model_trainer_config:ModelTrainerConfig):
        try:
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_config=model_trainer_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def track_mlflow(self,best_model,classification_metric):
        try:
            with mlflow.start_run():
                f1_score = classification_metric.f1_score
                precision_score = classification_metric.precision_score
                recall_score = classification_metric.recall_score

                mlflow.log_metric("f1_score", f1_score)
                mlflow.log_metric("precision_score", precision_score)
                mlflow.log_metric("recall_score", recall_score)
                mlflow.sklearn.log_model(best_model,"model" )



        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def train_model(self, X_train, X_test,y_train, y_test):
        try:
            models = {
                "Random Forest":RandomForestClassifier(verbose=1),
                "AdaBoost":AdaBoostClassifier(),
                "Gradient Boosting":GradientBoostingClassifier(verbose=1),
                "LogisticRegression":LogisticRegression(verbose=1),
                "Decision Tree":DecisionTreeClassifier()
            }
        
            params = {
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                # 'learning_rate':[.1,.01,.05,.001],
                # 'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                # 'n_estimators': [8,16,32,64,128,256]
            },
            "LogisticRegression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
            model_report:dict= evaluate_model( X_train, X_test,y_train, y_test, models=models, params=params)

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]

             #training evaluation
            y_train_pred = best_model.predict(X_train)    
            classification_train_metric = get_classification_metric(y_train, y_train_pred)
            # self.track_mlflow(best_model, classification_train_metric)
            #test evaluation
            y_test_pred = best_model.predict(X_test)    
            classification_test_metric = get_classification_metric(y_test, y_test_pred)
            self.track_mlflow(best_model, classification_train_metric)
            preprocessor =load_object(self.data_transformation_artifact.transformed_object_filepath)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_filepath)
            os.makedirs(model_dir_path, exist_ok=True)

            Network_Model = NetworkModel(preprocessor=preprocessor, model=best_model)
            save_object(self.model_trainer_config.trained_model_filepath, obj=NetworkModel)
            save_object("final_model/model.pkl", best_model)
            save_object("final_model/preprocessor.pkl", preprocessor)



            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_filepath=self.model_trainer_config.trained_model_filepath,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
                )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_model_trainer(self):
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_path
            test_file_path = self.data_transformation_artifact.transformed_test_path

            train_arr = load_numpy_array(train_file_path)
            test_arr = load_numpy_array(test_file_path)

            x_train, y_train, x_test, y_test =(
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],


            )
            model_trainer_artifact = self.train_model(x_train, x_test, y_train, y_test)
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
    

