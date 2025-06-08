from datetime import datetime
import os
from networksecurity.constant import trainingpipeline


class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%d_%m_%Y_%H_%M_%S")
        self.pipeline_name = trainingpipeline.PIPELINE_NAME  # pipeline name
        self.artifact_name = trainingpipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(
            self.artifact_name, timestamp)  # timestamp + artifact diR
        self.timestamp: str = timestamp


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, trainingpipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_dir_filepath: str = os.path.join(
            self.ingestion_dir, trainingpipeline.DATA_INGESTION_FEATURE_STORE_DIR, trainingpipeline.FILENAME
        )
        self.train_dir_filepath: str = os.path.join(
            self.ingestion_dir, trainingpipeline.DATA_INGESTION_INGESTED_DIR, trainingpipeline.TRAIN_FILE_NAME
        )
        self.test_dir_filepath: str = os.path.join(
            self.ingestion_dir, trainingpipeline.DATA_INGESTION_INGESTED_DIR, trainingpipeline.TEST_FILE_NAME
        )
        self.train_test_split_ratio: float = trainingpipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.data_ingestion_database_name = trainingpipeline.DATA_INGESTION_DATABASE_NAME
        self.data_ingestion_collection_name = trainingpipeline.DATA_INGESTION_COLLECTION_NAME


class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.validation_dir = os.path.join(
            training_pipeline_config.artifact_dir, trainingpipeline.DATA_VALIDATION_DIR
        )
        self.valid_data_dir = os.path.join(
            self.validation_dir, trainingpipeline.DATA_VALIDATION_VALID_DIR
        )
        self.invalid_data_dir = os.path.join(
            self.validation_dir, trainingpipeline.DATA_VALIDATION_INVALID_DIR
        )
        self.valid_train_file_path = os.path.join(
            self.valid_data_dir, trainingpipeline.TRAIN_FILE_NAME
        )
        self.valid_test_file_path = os.path.join(
            self.valid_data_dir, trainingpipeline.TEST_FILE_NAME
        )
        self.invalid_train_file_path = os.path.join(
            self.invalid_data_dir, trainingpipeline.TRAIN_FILE_NAME
        )
        self.invalid_test_file_path = os.path.join(
            self.invalid_data_dir, trainingpipeline.TEST_FILE_NAME
        )
        self.drift_report_file_path = os.path.join(
            self.validation_dir,
            trainingpipeline.DATA_VALIDATION_DRIFT_REPORT_DIR, 
            trainingpipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_PATH
        )
