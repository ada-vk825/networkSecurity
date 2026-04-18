import os
import sys
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split    
from networksecurity.exceptionhandling.exception import CustomException
from networksecurity.logging.logger import logging

# Configuration of the Data Ingestion Config
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)

    def export_collection_as_df(self):
        '''Exporting the collection data as a dataframe
        Args: None
        Returns: df: DataFrame: DataFrame containing the collection data
        '''
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns:
                df = df.drop(columns=['_id'])
            df = df.replace('na', np.nan)
            return df
        
        except Exception as e:
            logging.error(f"Error in exporting collection data as dataframe: {e}")
            raise CustomException(e, sys)

    def export_data_as_csv(self, df: pd.DataFrame):
        '''Exporting the dataframe as a csv file
        Args: df: DataFrame: DataFrame containing the collection data
        Returns: None
        '''
        try:
            export_file_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(export_file_path), exist_ok=True)
            df.to_csv(export_file_path, index=False, header=True)
            logging.info(f"Exported dataframe as csv file at {export_file_path}")
            return df
        except Exception as e:
            logging.error(f"Error in exporting dataframe as csv file: {e}")
            raise CustomException(e, sys)

    def split_data_as_train_test(self, df: pd.DataFrame):
        '''Splitting the dataframe as train and test set
        Args: df: DataFrame: DataFrame containing the collection data
        Returns: None
        '''
        try:
            train_set, test_set = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            logging.info(f"Split the dataframe as train and test set with test size {self.data_ingestion_config.train_test_split_ratio}")
            train_file_path = self.data_ingestion_config.training_file_path
            test_file_path = self.data_ingestion_config.testing_file_path
            os.makedirs(os.path.dirname(train_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
            train_set.to_csv(train_file_path, index=False, header=True)
            test_set.to_csv(test_file_path, index=False, header=True)
            logging.info(f"Split the dataframe as train and test set and saved at {train_file_path} and {test_file_path}")
        except Exception as e:
            logging.error(f"Error in splitting the dataframe as train and test set: {e}")
            raise CustomException(e, sys)

    def initiate_data_ingestion(self):
        try:
            df = self.export_collection_as_df()
            df = self.export_data_as_csv(df)
            logging.info("Exported collection data as dataframe")
            self.split_data_as_train_test(df)
            logging.info("Initiated data ingestion process")
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        
        except Exception as e:
            logging.error(f"Error in initiating data ingestion process: {e}")
            raise CustomException(e, sys)




