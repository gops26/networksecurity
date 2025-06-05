import os,sys
import pandas as pd
import numpy as np


"""
contains training pipeline related constants starting with data ingestion var name DATA_INGESTION_VAR NAME

"""
TARGET_COLUMN = "Result"
PIPELINE_NAME: str="NetworkSecurity"
ARTIFACT_DIR: str="Artifacts"
FILENAME : str= "phisingdata.csv"

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
