from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# config
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact 

import os
import sys
from typing import List

import pymongo

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_to_dataframe(self):
        try:
            """
            Reads data from mongo db cleint
            """
            database_name = self.data_ingestion_config.data_ingestion_database_name
            collection_name = self.data_ingestion_config.data_ingestion_collection_name
            mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            logging.info("data from  mongodb transferred to working environment")
            if "_id" in df.columns.tolist():
                df =df.drop(columns=["_id"], axis=1)
            df.replace({"na": np.nan}, inplace=True)
            return df
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe:pd.DataFrame)->pd.DataFrame:
        try:
            feature_store_filepath = self.data_ingestion_config.feature_dir_filepath
            dir_path_name = os.path.dirname(feature_store_filepath)
            os.makedirs(dir_path_name, exist_ok=True)
            dataframe.to_csv(feature_store_filepath, index=False, header=True)

            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_data_to_train_test(self, dataframe:pd.DataFrame) -> pd.DataFrame:
        train_set, test_set = train_test_split(
            dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
        
        logging.info("dataframe splitted into train and test size sucessfully")
        dirpath = os.path.dirname(self.data_ingestion_config.train_dir_filepath)
        os.makedirs(dirpath, exist_ok=True)
        logging.info("saving splitted data") 
        train_set.to_csv(self.data_ingestion_config.train_dir_filepath, header=True, index=False)
        test_set.to_csv(self.data_ingestion_config.test_dir_filepath, header=True, index=False)
        logging.info("saved splitted data") 

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_to_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            logging.info("raw.csv exported to feature store")
            self.split_data_to_train_test(dataframe)
            logging.info("data ingestion completed")
            
            data_ingestion_artifact = DataIngestionArtifact(
                self.data_ingestion_config.train_dir_filepath,
                self.data_ingestion_config.test_dir_filepath)
            
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
