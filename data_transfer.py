import os
import sys
import json
import pandas as pd
import numpy as np
import pymongo
import certifi
from dotenv import load_dotenv
from networksecurity.logging.logger import logging
from networksecurity.exceptionhandling.exception import CustomException

load_dotenv()  # Load environment variables from .env file

MONGO_BD_URL = os.getenv("MONGO_DB_URL")  # Get the MongoDB URL from environment variable

ca = certifi.where()  # Get the path to the certificate authority bundle provided by certifi. This is used to ensure that the connection to MongoDB is secure and trusted.


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            logging.error(f"Error occurred in NetworkDataExtract class: {e}")
            raise CustomException(e, sys)
        
    def csv_to_dict(self, file_path: str) -> list:
        '''Converts a CSV file to JSON format.
        Args: file_path (str): The path to the CSV file to be converted.
        Returns: list: A list of dictionaries representing the JSON data.
        '''
        try:
            df = pd.read_csv(file_path)
            df = df.reset_index(drop=True)  # Reset the index of the DataFrame to ensure it starts from 0 and is sequential.
            records = df.to_dict(orient="records")  # Convert the DataFrame to a list of dictionaries, where each dictionary represents a row of data with column names as keys and corresponding values.
            logging.info(f"Successfully converted {file_path} to JSON format.")
            return records

        except Exception as e:
            logging.error(f"Error occurred while converting CSV to JSON: {e}")
            raise CustomException(e, sys)


    def insert_to_mongodb(self, records, database, collection):
        '''Inserts a list of records into a MongoDB collection.
        Args: records (list): A list of dictionaries representing the data to be inserted.
              database (str): The name of the MongoDB database where the data will be inserted.
              collection (str): The name of the MongoDB collection where the data will be inserted.
        Returns: None
        '''
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.client = pymongo.MongoClient(MONGO_BD_URL, tlsCAFile=ca)  # Create a MongoDB client using the provided URL and certificate authority file for secure connection.
            self.database = self.client[self.database]  # Access the specified database.
            self.collection = self.database[self.collection]  # Access the specified collection within the database.
            self.collection.insert_many(self.records)  # Insert the list of records into the collection using the insert_many method, which allows for bulk insertion of multiple documents at once.
            logging.info(f"Successfully inserted records into MongoDB collection: {self.collection.name} in database: {self.database.name}.")
            return len(self.records)  # Return the number of records inserted.

        except Exception as e:
            logging.error(f"Error occurred while inserting records into MongoDB: {e}")
            raise CustomException(e, sys)


if __name__ == "__main__":
    file_path = "Network_Data/phisingData.csv"
    database = "NetworkSecurityDB"
    collection = "PhishingData"
    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_dict(file_path)
    inserted_count = network_obj.insert_to_mongodb(records, database, collection)
    print(f"Total records inserted: {inserted_count}")
    logging.info(f"Total records inserted: {inserted_count}")