from networksecurity.exception.exception import NetworkSecurityLoggingException
from networksecurity.logging.logger import logging


##configuration file 
from networksecurity.entity.config_entity import DataIngestionConfig
import os
import sys
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
import pandas as pd
from networksecurity.entity.artifact_entity import Artifact


from dotenv import load_dotenv
load_dotenv()
mongo_url = os.getenv("uri")
if not mongo_url:
    raise ValueError("MongoDB URI not found in .env file")
logging.info("Mongo URI loaded successfully")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise NetworkSecurityLoggingException(e)
        
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(mongo_url)
            logging.info("MongoDB connection successful")
            database = self.mongo_client[database_name]
            collection = database[collection_name]
            data = pd.DataFrame(list(collection.find()))
            logging.info(
                f"Dataframe shape: {data.shape} and columns: {data.columns}"
            )
            if "_id" in data.columns.to_list():
                data = data.drop(columns=["_id"], axis=1)

            data.replace(to_replace="na", value=np.nan, inplace=True)
            return data
        

        except Exception as e:
            raise NetworkSecurityLoggingException(e)    

    def export_data_into_feature_store(self, data:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            data.to_csv(feature_store_file_path, index=False)
            logging.info(
                f"Exported data to feature store at: {feature_store_file_path}"
            )
            return data

        except Exception as e:
            raise NetworkSecurityLoggingException(e)   

    def split_data_as_train_test(self, data:pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                data,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )

            train_file_path = self.data_ingestion_config.train_file_path
            test_file_path = self.data_ingestion_config.test_file_path

            dir_path = os.path.dirname(train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dir_path = os.path.dirname(test_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(train_file_path, index=False)
            test_set.to_csv(test_file_path, index=False)

            logging.info(
                f"Train and test data split and saved at: {train_file_path} and {test_file_path}"
            )

        except Exception as e:
            raise NetworkSecurityLoggingException(e)    

    def initiate_data_ingestion(self):
        try:
            data = self.export_collection_as_dataframe()
            data = self.export_data_into_feature_store(data)
            self.split_data_as_train_test(data)
            data_ingestion_artifact = Artifact(
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityLoggingException(e)