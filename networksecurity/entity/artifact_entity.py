from dataclasses import dataclass
@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str
@dataclass
class DataValidationArtifact:
    validation_status : bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str

@dataclass
class DataTransformationArtifact:
    transformed_object_filepath:str
    transformed_train_path:str
    transformed_test_path:str
@dataclass
class ClassificationMetricArtifact:
    f1_score:str
    precision_score:str
    recall_score:str


@dataclass
class ModelTrainerArtifact:
    trained_model_filepath:str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact

