from networksecurity.exception.exception import NetworkSecurityException as nsexception
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion

import sys

if __name__ == "__main__":
    try:
        logging.info("running data ingestion")
        dataingestion =DataIngestion()
        data_ingestion_artifact = dataingestion.initiate_data_ingestion()
    except Exception as e:
        raise nsexception(e, sys) 

