import streamlit as st
import pandas as pd
import pyodbc
import os

st.set_page_config(page_title="Dashboard de Faturamento", layout="wide")
st.title("📦 Dashboard de Faturamento - SX Group")

def get_faturamento_data():
    try:
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=sx.gruposps.com.br,14382;"
            "DATABASE=SBO_SX2022;"
            "UID=Sx;"
            "PWD=Sx4dm1n@1234;"
            "TrustServerCertificate=yes;"
        )

        with open('query.sql', 'r', encoding='utf-8') as f:
            query = f.read()

        conn = pyodbc.connect(conn_str)
        df = pd.read_sql(query, conn)
        conn.close()
        return df

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = get_faturamento_data()

    def dedup_columns(columns):
        seen = {}
        new_columns = []
        for col in columns:
            if col in seen:
                seen[col] += 1
                new_columns.append(f"{col}_{seen[col]}")
            else:
                seen[col] = 0
                new_columns.append(col)
        return new_columns  # <-- Corrigido aqui

