from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig
import sys

if __name__ == "__main__": 
    try:
        logging.info("running data ingestion")
        trainingpipelineconfig = TrainingPipelineConfig()

        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        dataingestion =DataIngestion(dataingestionconfig)
        data_ingestion_artifact = dataingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)

        logging.info("running data validations")

        data_validation_config  = DataValidationConfig(trainingpipelineconfig)
        data_validation_artifact= DataValidation(data_ingestion_artifact, data_validation_config)
        print(data_validation_artifact)


    except Exception as e:
        raise NetworkSecurityException(e, sys) 

