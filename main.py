from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityLoggingException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainigPipelineConfig

if __name__ == "__main__":
    try:
        data_ingestion = DataIngestion(DataIngestionConfig(TrainigPipelineConfig()))
        art = data_ingestion.initiate_data_ingestion()
        print(art)
    except Exception as e:
        raise NetworkSecurityLoggingException(e)
    