from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
import os
from networksecurity.entity.config_entity import (
    DataTransformationConfig,
    DataIngestionConfig,
    DataValidationConfig,
    ModelTrainerConfig,
    TrainingPipelineConfig
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ClassificationMetricArtifact
)

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.constant.trainingpipeline import TRAINING_BUCKET_NAME

from networksecurity.cloud.s3_syncer import S3_sync


class TrainingPipeline:
    def __init__(self):
        try:
            self.training_pipeline_config = TrainingPipelineConfig()
            self.s3_sync = S3_sync()
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            
            logging.info("entering data_ingestion")
            ingestion_config = DataIngestionConfig(
                training_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("completed data_ingestion")

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info("entering data_validation")

            validation_config = DataValidationConfig(
                self.training_pipeline_config)
            data_validation = DataValidation(
                data_ingestion_artifact, validation_config)

            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("completed data_validation")

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def sync_artifact_dir_to_s3(self):
        try:
            aws_s3_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifacts/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.artifact_dir,aws_s3_bucket_url=aws_s3_bucket_url) 
        except Exception as e:
            pass

    def sync_final_model_dir_to_s3(self):
        try:
            aws_s3_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder="final_model",aws_s3_bucket_url=aws_s3_bucket_url) 
        except Exception as e:
            pass

    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            logging.info("entering data_transformation")

            transformation_config = DataTransformationConfig(
                self.training_pipeline_config)

            data_transformation = DataTransformation(
                data_validation_artifact, data_transformation_config=transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("completed data_transformation")

            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            logging.info("entering model trainer")

            model_trainer_config = ModelTrainerConfig(
                self.training_pipeline_config)

            model_trainer = ModelTrainer(
                data_transformation_artifact, model_trainer_config=model_trainer_config)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            
            logging.info("model trainer completed")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact= self.start_data_ingestion()

            data_validation_artifact= self.start_data_validation(data_ingestion_artifact= data_ingestion_artifact)

            data_transformation_artifact = self.start_data_transformation(data_validation_artifact= data_validation_artifact)

            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact= data_transformation_artifact)
            
            self.sync_artifact_dir_to_s3()
            self.sync_final_model_dir_to_s3()

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    pipeline = TrainingPipeline()
    model_artifact=pipeline.run_pipeline()
    print(model_artifact)