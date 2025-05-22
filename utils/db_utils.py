import pyodbc
import pandas as pd
import os

def get_faturamento_data():
    try:
        conn_str = f"""
            DRIVER={{ODBC Driver 17 for SQL Server}};
            SERVER={os.getenv('DB_SERVER')};
            DATABASE={os.getenv('DB_NAME')};
            UID={os.getenv('DB_USER')};
            PWD={os.getenv('DB_PASS')};
            TrustServerCertificate=yes;
        """
        with open('query.sql', 'r', encoding='utf-8') as f:
            query = f.read()
        
        conn = pyodbc.connect(conn_str)
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Erro ao consultar dados: {e}")
        return pd.DataFrame()
