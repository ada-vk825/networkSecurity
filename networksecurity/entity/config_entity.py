from datetime import datetime
import os
from networksecurity.constant import training_pipeline

print(training_pipeline)


class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        self.timestamp = timestamp.strftime("%m-%d-%Y %H-%M-%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, self.timestamp)


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        '''Data Ingestion Config is the configuration for the data ingestion process
        Args: training_pipeline_config: TrainingPipelineConfig: The configuration for the training pipeline
        Returns: None
        '''
        self.data_ingestion_file_path: str = os.path.join(training_pipeline_config.artifact_dir, 
                                                          training_pipeline.DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path: str = os.path.join(self.data_ingestion_file_path,
                                                         training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME)
        self.training_file_path: str = os.path.join(self.data_ingestion_file_path, training_pipeline.DATA_INGESTION_INGESTED_DIR,
                                                    training_pipeline.TRAIN_FILE_NAME)
        self.testing_file_path: str = os.path.join(self.data_ingestion_file_path, training_pipeline.DATA_INGESTION_INGESTED_DIR,
                                                   training_pipeline.TEST_FILE_NAME)
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME
