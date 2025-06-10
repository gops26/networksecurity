from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
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
        data_validation= DataValidation(data_ingestion_artifact, data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)

        logging.info("running data transfromaion")
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact, data_transformation_config=data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact.transformed_object_filepath)
        
        logging.info("running model trainer")
        model_trainer_config = ModelTrainerConfig(training_pipeline_config=trainingpipelineconfig)
        model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact, model_trainer_config=model_trainer_config)
        model_trainer_artifact= model_trainer.initiate_model_trainer() 
        print(model_trainer_artifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys) 

