import os
import sys
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
import pandas as pd
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig

from networksecurity.constant.trainingpipeline import TARGET_COLUMN
from networksecurity.constant.trainingpipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.utils.main_utils.utils import save_numpy_array, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact, data_transformation_config:DataTransformationConfig):
        """
        initiates Data transformation on given data 

        params:
        data_validation_artifact: validated data filepaths
         data_transformation_config: transformation config
        """
        logging.info("entered into data transformation stage")

        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    @staticmethod    
    def read_data(filepath:str):
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def get_transformer_object(cls)->Pipeline:
        try:
            logging.info("entered get_data_transformer object ")
            imputer:KNNImputer= KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor = Pipeline([("imputer", imputer)])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self)-> DataTransformationArtifact:
        try:
            logging.info("entered initiate_data_transformation function ")

            #train df
            train_dataframe = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            input_train_feature = train_dataframe.drop(columns=[TARGET_COLUMN], axis=1)
            target_train_feature = train_dataframe[TARGET_COLUMN]
            target_train_feature = target_train_feature.replace(-1, 0)
            logging.info("train feature splitted into inpput / target")

            #test df
            test_dataframe = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            input_test_feature = test_dataframe.drop(columns=[TARGET_COLUMN], axis=1)
            target_test_feature = test_dataframe[TARGET_COLUMN]
            target_test_feature = target_test_feature.replace(-1,0)
            logging.info("test feature splitted into inpput / target")


            preprocessor = self.get_transformer_object()
            logging.info("loaded preprocessor object")

            transformed_train_input_arr = preprocessor.fit_transform(input_train_feature)
            transformed_test_input_arr = preprocessor.transform(input_test_feature)
            logging.info("feauter transformation complete")


            train_arr = np.c_[transformed_train_input_arr, np.array(target_train_feature)]
            test_arr = np.c_[transformed_test_input_arr, np.array(target_test_feature)]
            
            
            save_numpy_array(self.data_transformation_config.transformed_train_path, train_arr)
            save_numpy_array(self.data_transformation_config.transformed_test_path, test_arr)
            save_object(self.data_transformation_config.transformed_object_path, preprocessor)
            logging.info("saved to numpy array")

            save_object( "final_model/preprocessor.pkl", preprocessor,)


            return DataTransformationArtifact(
                transformed_train_path=self.data_transformation_config.transformed_train_path,
                transformed_test_path=self.data_transformation_config.transformed_test_path,
                transformed_object_filepath=self.data_transformation_config.transformed_object_path
            )


        except Exception as e:
            raise NetworkSecurityException(e, sys) 