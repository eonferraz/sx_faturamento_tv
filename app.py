--- app.py ---
import streamlit as st
import pandas as pd
import pyodbc
from datetime import datetime
from titulo import render_titulo
from cards import render_cards
from termometro import render_termometro
from tabelas import render_tabelas

st.set_page_config(page_title="Dashboard de Faturamento e Carteira", layout="wide")

META_MENSAL = 5_800_000

# Função para ler dados do faturamento
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

# Função para ler dados da carteira
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

# Função para ler dados dos pedidos inclusos
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

# Carregar dados
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


--- titulo.py ---
import streamlit as st

def render_titulo(hoje):
    st.markdown(f"<h2 style='text-align:center;'>Faturamento {hoje.strftime('%B').capitalize()} - SX Lighting</h2>", unsafe_allow_html=True)


--- cards.py ---
import streamlit as st

def render_cards(df_fat, df_cart, df_ped, META_MENSAL, hoje):
    data_col_fat = 'Data Emissão'
    data_col_cart = 'Data Entrega'
    data_col_ped = 'Data Emissao'

    mes_atual = hoje.month
    ano_atual = hoje.year

    df_fat_mes = df_fat[(df_fat[data_col_fat].dt.month == mes_atual) & (df_fat[data_col_fat].dt.year == ano_atual)]
    df_cart_mes = df_cart[(df_cart[data_col_cart].dt.month == mes_atual) & (df_cart[data_col_cart].dt.year == ano_atual)]
    df_ped_mes = df_ped[(df_ped[data_col_ped].dt.month == mes_atual) & (df_ped[data_col_ped].dt.year == ano_atual)]

    realizado = df_fat_mes['Total Produto'].sum()
    carteira = df_cart_mes['Valor Receita Bruta Pedido'].sum()
    restante = max(META_MENSAL - realizado - carteira, 0)

    st.markdown("""
        <style>
        .card { border-radius: 10px; padding: 12px; margin-bottom: 10px; color: white; text-align: center; }
        .card b { font-size: 32px; }
        .card-title { font-size: 16px; display: block; }
        .meta { background-color: #1f77b4; }
        .realizado { background-color: #2ca02c; }
        .carteira { background-color: #ff7f0e; }
        .restante { background-color: #d62728; }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f'<div class="card meta"><span class="card-title">Meta Mensal</span><b>R$ {META_MENSAL:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col2.markdown(f'<div class="card realizado"><span class="card-title">Faturado</span><b>R$ {realizado:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col3.markdown(f'<div class="card carteira"><span class="card-title">Carteira</span><b>R$ {carteira:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col4.markdown(f'<div class="card restante"><span class="card-title">Restante</span><b>R$ {restante:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)


--- termometro.py ---
import streamlit as st
import plotly.graph_objects as go

def render_termometro(df_fat, df_cart, META_MENSAL, hoje):
    data_col_fat = 'Data Emissão'
    mes_atual = hoje.month
    ano_atual = hoje.year

    df_fat_mes = df_fat[(df_fat[data_col_fat].dt.month == mes_atual) & (df_fat[data_col_fat].dt.year == ano_atual)]
    realizado = df_fat_mes['Total Produto'].sum()
    carteira = df_cart['Valor Receita Bruta Pedido'].sum()
    restante = max(META_MENSAL - realizado - carteira, 0)

    perc_realizado = min(realizado / META_MENSAL * 100, 100)
    perc_carteira = min(carteira / META_MENSAL * 100, 100)
    perc_restante = max(100 - perc_realizado - perc_carteira, 0)

    fig_termo = go.Figure()
    fig_termo.add_trace(go.Bar(y=['Meta'], x=[realizado], orientation='h', marker=dict(color='#2ca02c'), text=[f'{perc_realizado:.1f}%'], textposition='auto', textfont=dict(size=18)))
    fig_termo.add_trace(go.Bar(y=['Meta'], x=[carteira], orientation='h', marker=dict(color='#ff7f0e'), text=[f'{perc_carteira:.1f}%'], textposition='auto', textfont=dict(size=18)))
    fig_termo.add_trace(go.Bar(y=['Meta'], x=[restante], orientation='h', marker=dict(color='#d62728'), text=[f'{perc_restante:.1f}%'], textposition='auto', textfont=dict(size=18)))
    fig_termo.update_layout(barmode='stack', height=80, margin=dict(t=10, b=10), showlegend=False)
    st.plotly_chart(fig_termo, use_container_width=True)


--- tabelas.py ---
import streamlit as st

def render_tabelas(df_fat, df_ped, hoje):
    table_height = 450

    col_fat, col_ped = st.columns(2)

    with col_fat:
        st.markdown("### Últimos Faturamentos")
        ult_fat = df_fat.sort_values(by='Data Emissão', ascending=False)
        ult_fat['Data Emissão'] = ult_fat['Data Emissão'].dt.strftime('%d/%m/%Y')
        ult_fat_view = ult_fat[['Data Emissão', 'Cliente', 'Vendedor', 'Total Produto']].head(10)
        ult_fat_view['Total Produto'] = ult_fat_view['Total Produto'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.dataframe(ult_fat_view, height=table_height)

    with col_ped:
        st.markdown("### Últimos Pedidos Inclusos")
        ult_ped = df_ped.sort_values(by='Data Emissao', ascending=False)
        ult_ped['Data Emissao'] = ult_ped['Data Emissao'].dt.strftime('%d/%m/%Y')
        ult_ped_view = ult_ped[['Data Emissao', 'Cliente', 'Vendedor', 'Valor Receita Bruta Pedido']].head(10)
        ult_ped_view['Valor Receita Bruta Pedido'] = ult_ped_view['Valor Receita Bruta Pedido'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.dataframe(ult_ped_view, height=table_height)
