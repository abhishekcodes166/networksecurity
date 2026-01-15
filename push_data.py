import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_URL = os.getenv("uri")
if not MONGO_URL:
    raise ValueError("MongoDB URI not found in .env file")

print("Mongo URI loaded successfully")


import certifi
import pandas as pd
import pymongo

from networksecurity.exception.exception import NetworkSecurityLoggingException
from networksecurity.logging.logger import logging

CA_FILE = certifi.where()

class NetworkDataExtract:
    def __init__(self):
        try:
            self.client = None
        except Exception as e:
            raise NetworkSecurityLoggingException(e)

    def csv_to_json_converter(self, file_path: str):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = json.loads(data.to_json(orient="records"))
            return records
        except Exception as e:
            raise NetworkSecurityLoggingException(e)

    def connect_mongo(self):
        try:
            self.client = pymongo.MongoClient(
                MONGO_URL,
                tls=True,
                tlsCAFile=CA_FILE,
                serverSelectionTimeoutMS=30000
            )

           
            self.client.admin.command("ping")
            logging.info("MongoDB connection successful")

        except Exception as e:
            raise NetworkSecurityLoggingException(e)

    def insert_data_mongo(self, records, database_name, collection_name):
        try:
            if not self.client:
                self.connect_mongo()

            database = self.client[database_name]
            collection = database[collection_name]

            if records:
                collection.insert_many(records)
                logging.info(
                    f"Inserted {len(records)} records into "
                    f"{database_name}.{collection_name}"
                )
            else:
                logging.warning("No records to insert")

        except Exception as e:
            raise NetworkSecurityLoggingException(e)

if __name__ == "__main__":
    try:
        FILE_PATH = "Network_Data\phisingData.csv"
        DATABASE_NAME = "network_security_db"
        COLLECTION_NAME = "traffic_logs"

        extractor = NetworkDataExtract()

        records = extractor.csv_to_json_converter(FILE_PATH)
        extractor.insert_data_mongo(
            records,
            DATABASE_NAME,
            COLLECTION_NAME
        )

        print("✅ Data ingestion completed successfully")

    except NetworkSecurityLoggingException as ne:
        ne.log_exception()
        sys.exit(1)
