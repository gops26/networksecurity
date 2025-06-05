import os, sys, json
from dotenv import load_dotenv
import pymongo.mongo_client
import ssl
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi  
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging import logger
from networksecurity.exception import exception

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise exception.NetworkSecurityException(e, sys)
        
    def csv_to_json(self, filepath):
        try:
            data = pd.read_csv(filepath)
            data.reset_index(drop=True, inplace=True)
            # making list of values of the dict of json
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise exception.NetworkSecurityException(e,sys)
        
    def push_to_mongo(self,records,database,collection):
        try:
            # init
            self.database = database
            self.records =records
            self.collection = collection

            #load mongoclient 
            self.mongoclient = pymongo.MongoClient(MONGO_DB_URL, ssl=True)
            # find data base
            self.database = self.mongoclient[database]
            self.collection = self.database[collection]

            # insert data
            self.collection.insert_many(records)
            return len(self.records)
        except Exception as e:
            raise exception.NetworkSecurityException(e, sys)



if __name__ == "__main__":
    FILE_PATH = 'Network_Data\phisingData.csv'
    DATABASE = "GOPINATHAI"
    Collection = "NetworkData"
    networkdata = NetworkDataExtract()
    records  = networkdata.csv_to_json(FILE_PATH)
    # print(records)
    n_records = networkdata.push_to_mongo(records,DATABASE, Collection)
    print(n_records)
