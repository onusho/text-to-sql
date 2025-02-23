import pandas as pd
from sqlalchemy import create_engine


class Database:
    def __init__(self):
        self.params = {
            "host": "localhost",
            "port": 5432,
            "database": "postgres",
            "user": "postgres",
            "password": "123456"  
        }
        self.connection = self.connect_to_db()

    def connect_to_db(self):
        return create_engine(f"postgresql://{self.params['user']}:{self.params['password']}@{self.params['host']}:{self.params['port']}/{self.params['database']}")
        
    def get_data(self, query):
        """returns dataframe"""
        try:
            df = pd.read_sql(query, self.connection)
            return df
        except Exception as e:
            print("Error executing query:", e)
            return None
    
    # def close_connection(self):
    #     self.connection.close()

