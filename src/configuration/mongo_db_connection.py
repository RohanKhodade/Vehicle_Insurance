import os
import sys
import pymongo
import certifi

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGO_URI

ca=certifi.where()

class MongoDBClient:
    "MongoDB client class to connect to MongoDB database"
    client=None
    
    def __init__(self,database_name:str=DATABASE_NAME)->None:
        
        try:
            if MongoDBClient.client is None:
                mongo_db_url=os.getenv("MONGO_URI")
                if mongo_db_url is None:
                    raise Exception(".env file variable MONGO_URI is not set",{MONGO_URI})
                
                #establish new ongo connection
                MongoDBClient.client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
                
            self.client=MongoDBClient.client
            self.database=self.client[database_name]
            self.database_name=database_name
            logging.info("MongoDb connection successfull")
            
        except Exception as e:
            raise MyException(e,sys)