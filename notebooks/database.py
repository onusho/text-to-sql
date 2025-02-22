import pandas as pd
from sqlalchemy import create_engine


connection_parameters = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "123456"  
}

def connect_to_db(params):
    return create_engine(f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}")

    
def fetch_query_as_df(conn, query):
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print("Error executing query:", e)
        return None
    

