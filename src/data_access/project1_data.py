import sys
import numpy as np
from typing import Optional
import pandas as pd

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException

class Proj1Data:
    """
    A class to export MongoDB records as a pandas DataFrame.
    """
    def __init__(self)->None:
        try:
            self.mongo_client=MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e,sys)
        
    def export_collection_as_dataframe(self,collection_name:str,database_name:Optional[str]=None)->pd.DataFrame:
        """
        Export a MongoDB collection as a pandas DataFrame.
        
        Parameters:
            collection_name (str): The name of the MongoDB collection to export.
            database_name (str, optional): The name of the MongoDB database. Defaults to None.
        
        Returns:
            pd.DataFrame: A pandas DataFrame containing the exported data.
        """
        try:
            if database_name is None:
                collection=self.mongo_client.database[collection_name]
            else:
                collection=self.mongo_client.client[database_name][collection_name]
            print("fetching data from mongo db")
            df=pd.DataFrame(list(collection.find()))
            print(f"DataFetched with length : {len(df)}")
            if "id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            df.replace({"NaN":np.nan},inplace=True)
            df.replace({"nan":np.nan},inplace=True)
            df.replace({"N/A":np.nan},inplace=True)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise MyException(e,sys)
        