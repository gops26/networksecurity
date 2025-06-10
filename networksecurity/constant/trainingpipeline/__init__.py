import os,sys
import pandas as pd
import numpy as np


"""
contains COMMON training pipeline related constants starting with data ingestion var name DATA_INGESTION_VAR NAME

"""
TARGET_COLUMN = "Result" #target
PIPELINE_NAME: str="NetworkSecurity"
ARTIFACT_DIR: str="Artifacts"#artifac
FILENAME : str= "phisingdata.csv"
SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yaml")
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME = "test.csv"
"""
contains data ingestion constants starting with data ingestion var name DATA_INGESTION_VAR NAME

"""

DATA_INGESTION_COLLECTION_NAME: str="NetworkData" 
DATA_INGESTION_DATABASE_NAME:str="GOPINATHAI"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION:float = 0.2

"""
Contains data validation constants starting with data validation var name DATA_VALIDATION_VAR_NAME

"""

DATA_VALIDATION_DIR="data_validation"
DATA_VALIDATION_VALID_DIR="valid"
DATA_VALIDATION_INVALID_DIR = 'invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR = 'drift-report'
DATA_VALIDATION_DRIFT_REPORT_FILE_PATH ='report.yaml' 
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"


"""
Contains data transformation constants starting with data validation var name DATA_TRANSFORMATION_VAR_NAME

"""
DATA_TRANSFORMATION_DIR:str = 'data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str='transformed'
DATA_TRANSFORMATION_OBJECT_DIR:str ='transformed_object' 

DATA_TRANSFORMATION_IMPUTER_PARAMS:dict = {
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform",
    }

DATA_TRANSFORMATION_TRAIN_FILE_PATH:str = 'train.npy'
DATA_TRANSFORMATION_TEST_FILE_PATH:str = 'test.npy'

"""
Contains  model training constants starting with model` training var name model_training
"""

MODEL_TRAINER_DIR_NAME = "model_trianer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_ACCURACY_SCORE:float =0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD:float = 0.05