from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exceptionhandling.exception import CustomException
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from networksecurity.logging.logger import logging
import sys


if __name__ == "__main__":
    try:
        logging.info("Starting the training pipeline")
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
        print(data_ingestion_artifact)

    except Exception as e:
        logging.error(f"Error in the training pipeline: {e}")
        raise CustomException(e, sys)
