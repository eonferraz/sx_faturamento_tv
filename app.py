import streamlit as st
import pandas as pd
import pyodbc
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard de Faturamento e Pedidos", layout="wide")

META_MENSAL = 5_800_000

COLOR_REALIZADO = '#2ca02c'  # verde
COLOR_PROMETIDO = '#ff7f0e'  # laranja
COLOR_RESTANTE = '#d62728'   # vermelho
COLOR_META = '#1f77b4'       # azul
COLOR_INFO = '#6c757d'

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

# Função para ler dados dos pedidos
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
        st.error(f"Erro ao carregar pedidos: {e}")
        return pd.DataFrame()

# Carregar dados
df_fat = get_faturamento_data()
df_ped = get_pedidos_data()

if df_fat.empty or df_ped.empty:
    st.warning("Dados incompletos carregados.")
else:
    df_fat['Data Emissão'] = pd.to_datetime(df_fat['Data Emissão'])
    df_ped['Data Emissão'] = pd.to_datetime(df_ped['Data Emissão'])

    hoje = datetime.today()
    mes_atual = hoje.month
    ano_atual = hoje.year

    # Filtrar mês atual
    df_fat_mes = df_fat[(df_fat['Data Emissão'].dt.month == mes_atual) & (df_fat['Data Emissão'].dt.year == ano_atual)]
    df_ped_mes = df_ped[(df_ped['Data Emissão'].dt.month == mes_atual) & (df_ped['Data Emissão'].dt.year == ano_atual)]

    realizado = df_fat_mes['Total Produto'].sum()
    prometido = df_ped_mes['Valor Receita Bruta Pedido'].sum()
    restante = max(META_MENSAL - realizado - prometido, 0)

    perc_realizado = min(realizado / META_MENSAL * 100, 100)
    perc_prometido = min(prometido / META_MENSAL * 100, 100)
    perc_restante = max(100 - perc_realizado - perc_prometido, 0)

    # Indicadores principais
    st.markdown(f"""
        <style>
        .card {{
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 10px;
            color: white;
            text-align: center;
        }}
        .card b {{ font-size: 32px; }}
        .card-title {{ font-size: 16px; display: block; }}
        .meta {{ background-color: {COLOR_META}; }}
        .prometido {{ background-color: {COLOR_PROMETIDO}; }}
        .realizado {{ background-color: {COLOR_REALIZADO}; }}
        .restante {{ background-color: {COLOR_RESTANTE}; }}
        .info {{ background-color: {COLOR_INFO}; }}
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f'<div class="card meta"><span class="card-title">Meta Mensal</span><b>R$ {META_MENSAL:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col2.markdown(f'<div class="card prometido"><span class="card-title">Prometido</span><b>R$ {prometido:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col3.markdown(f'<div class="card realizado"><span class="card-title">Faturado</span><b>R$ {realizado:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col4.markdown(f'<div class="card restante"><span class="card-title">Restante</span><b>R$ {restante:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

    # Gráfico termômetro
    fig_termo = go.Figure()
    fig_termo.add_trace(go.Bar(y=['Meta'], x=[realizado], orientation='h', marker=dict(color=COLOR_REALIZADO), text=[f'{perc_realizado:.1f}%'], textposition='auto'))
    fig_termo.add_trace(go.Bar(y=['Meta'], x=[prometido], orientation='h', marker=dict(color=COLOR_PROMETIDO), text=[f'{perc_prometido:.1f}%'], textposition='auto'))
    fig_termo.add_trace(go.Bar(y=['Meta'], x=[restante], orientation='h', marker=dict(color=COLOR_RESTANTE), text=[f'{perc_restante:.1f}%'], textposition='auto'))
    fig_termo.update_layout(barmode='stack', height=80, margin=dict(t=10, b=10), showlegend=False)
    st.plotly_chart(fig_termo, use_container_width=True)

    # Últimos faturamentos
    st.markdown("### Últimos Faturamentos")
    ult_fat = df_fat_mes.sort_values(by='Data Emissão', ascending=False)
    ult_fat['Data Emissão'] = ult_fat['Data Emissão'].dt.strftime('%d/%m/%Y')
    ult_fat_view = ult_fat[['Data Emissão', 'Cliente', 'Vendedor', 'Total Produto']].head(10)
    ult_fat_view['Total Produto'] = ult_fat_view['Total Produto'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    st.dataframe(ult_fat_view, height=300)

    # Últimos pedidos
    st.markdown("### Últimos Pedidos (Prometidos)")
    ult_ped = df_ped_mes.sort_values(by='Data Emissão', ascending=False)
    ult_ped['Data Emissão'] = ult_ped['Data Emissão'].dt.strftime('%d/%m/%Y')
    ult_ped_view = ult_ped[['Data Emissão', 'Cliente', 'Vendedor', 'Valor Receita Bruta Pedido']].head(10)
    ult_ped_view['Valor Receita Bruta Pedido'] = ult_ped_view['Valor Receita Bruta Pedido'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    st.dataframe(ult_ped_view, height=300)

    # Indicadores rápidos
    df_fat_dia = df_fat[df_fat['Data Emissão'].dt.date == hoje.date()]
    df_fat_semana = df_fat[df_fat['Data Emissão'].dt.isocalendar().week == hoje.isocalendar().week]
    df_ped_dia = df_ped[df_ped['Data Emissão'].dt.date == hoje.date()]
    df_ped_semana = df_ped[df_ped['Data Emissão'].dt.isocalendar().week == hoje.isocalendar().week]

    colx, coly = st.columns(2)
    colx.markdown(f'<div class="card info"><span class="card-title">Faturado Hoje</span><b>R$ {df_fat_dia["Total Produto"].sum():,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    coly.markdown(f'<div class="card info"><span class="card-title">Faturado na Semana</span><b>R$ {df_fat_semana["Total Produto"].sum():,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

    colx, coly = st.columns(2)
    colx.markdown(f'<div class="card info"><span class="card-title">Prometido Hoje</span><b>R$ {df_ped_dia["Valor Receita Bruta Pedido"].sum():,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    coly.markdown(f'<div class="card info"><span class="card-title">Prometido na Semana</span><b>R$ {df_ped_semana["Valor Receita Bruta Pedido"].sum():,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
