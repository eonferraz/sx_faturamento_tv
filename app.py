import streamlit as st
import pandas as pd
import pyodbc
from datetime import datetime
from titulo import render_titulo
from cards import render_cards
from termometro import render_termometro
from tabelas import render_tabelas

st.set_page_config(page_title="Dashboard de Faturamento e Carteira", layout="wide")

META_MENSAL = 5_310_000

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
        st.error(f"Erro ao carregar faturamento: {e}")
        return pd.DataFrame()

def get_carteira_data():
    try:
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=sx.gruposps.com.br,14382;"
            "DATABASE=SBO_SX2022;"
            "UID=Sx;"
            "PWD=Sx4dm1n@1234;"
            "TrustServerCertificate=yes;"
        )
        with open('carteira.sql', 'r', encoding='utf-8') as f:
            query = f.read()
        conn = pyodbc.connect(conn_str)
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar carteira: {e}")
        return pd.DataFrame()

def get_pedidos_data():
    try:
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=sx.gruposps.com.br,14382;"
            "DATABASE=SBO_SX2022;"
            "UID=Sx;"
            "PWD=Sx4dm1n@1234;"
            "TrustServerCertificate=yes;"
        )
        with open('pedidos.sql', 'r', encoding='utf-8') as f:
            query = f.read()
        conn = pyodbc.connect(conn_str)
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar pedidos inclusos: {e}")
        return pd.DataFrame()

df_fat = get_faturamento_data()
df_cart = get_carteira_data()
df_ped = get_pedidos_data()

if df_fat.empty or df_cart.empty or df_ped.empty:
    st.warning("Dados incompletos carregados.")
else:
    hoje = datetime.today()
    render_titulo(hoje)
    render_cards(df_fat, df_cart, df_ped, META_MENSAL, hoje)
    render_termometro(df_fat, df_cart, META_MENSAL, hoje)
    render_tabelas(df_fat, df_ped, hoje)
