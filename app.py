import streamlit as st
import pandas as pd
import pyodbc
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard de Faturamento e Carteira", layout="wide")

META_MENSAL = 5_800_000

COLOR_REALIZADO = '#2ca02c'
COLOR_CARTEIRA = '#ff7f0e'
COLOR_RESTANTE = '#d62728'
COLOR_META = '#1f77b4'
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

# Carregar dados
df_fat = get_faturamento_data()
df_cart = get_carteira_data()

if df_fat.empty or df_cart.empty:
    st.warning("Dados incompletos carregados.")
else:
    hoje = datetime.today()
    mes_atual = hoje.month
    ano_atual = hoje.year

    data_col_fat = [col for col in df_fat.columns if 'Data' in col][0]
    data_col_cart = 'Data Entrega'

    df_fat[data_col_fat] = pd.to_datetime(df_fat[data_col_fat])
    df_cart[data_col_cart] = pd.to_datetime(df_cart[data_col_cart])

    df_fat_mes = df_fat[(df_fat[data_col_fat].dt.month == mes_atual) & (df_fat[data_col_fat].dt.year == ano_atual)]
    df_cart_mes = df_cart[(df_cart[data_col_cart].dt.month == mes_atual) & (df_cart[data_col_cart].dt.year == ano_atual)]

    realizado = df_fat_mes['Total Produto'].sum()
    carteira = df_cart_mes['Valor Receita Bruta Pedido'].sum()
    restante = max(META_MENSAL - realizado - carteira, 0)

    perc_realizado = min(realizado / META_MENSAL * 100, 100)
    perc_carteira = min(carteira / META_MENSAL * 100, 100)
    perc_restante = max(100 - perc_realizado - perc_carteira, 0)

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
        .realizado {{ background-color: {COLOR_REALIZADO}; }}
        .carteira {{ background-color: {COLOR_CARTEIRA}; }}
        .restante {{ background-color: {COLOR_RESTANTE}; }}
        .info {{ background-color: {COLOR_INFO}; }}
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f'<div class="card meta"><span class="card-title">Meta Mensal</span><b>R$ {META_MENSAL:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col2.markdown(f'<div class="card realizado"><span class="card-title">Faturado</span><b>R$ {realizado:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col3.markdown(f'<div class="card carteira"><span class="card-title">Carteira</span><b>R$ {carteira:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col4.markdown(f'<div class="card restante"><span class="card-title">Restante</span><b>R$ {restante:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

    fig_termo = go.Figure()
    fig_termo.add_trace(go.Bar(y=['Meta'], x=[realizado], orientation='h', marker=dict(color=COLOR_REALIZADO), text=[f'{perc_realizado:.1f}%'], textposition='auto'))
    fig_termo.add_trace(go.Bar(y=['Meta'], x=[carteira], orientation='h', marker=dict(color=COLOR_CARTEIRA), text=[f'{perc_carteira:.1f}%'], textposition='auto'))
    fig_termo.add_trace(go.Bar(y=['Meta'], x=[restante], orientation='h', marker=dict(color=COLOR_RESTANTE), text=[f'{perc_restante:.1f}%'], textposition='auto'))
    fig_termo.update_layout(barmode='stack', height=80, margin=dict(t=10, b=10), showlegend=False)
    st.plotly_chart(fig_termo, use_container_width=True)

    # Tabelas com altura aumentada em 50%
    table_height = 450

    col_fat, col_cart = st.columns(2)

    with col_fat:
        st.markdown("### Últimos Faturamentos")
        ult_fat = df_fat_mes.sort_values(by=data_col_fat, ascending=False)
        ult_fat[data_col_fat] = ult_fat[data_col_fat].dt.strftime('%d/%m/%Y')
        ult_fat_view = ult_fat[[data_col_fat, 'Cliente', 'Vendedor', 'Total Produto']].head(10)
        ult_fat_view['Total Produto'] = ult_fat_view['Total Produto'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.dataframe(ult_fat_view, height=table_height)

        df_fat_dia = df_fat[df_fat[data_col_fat].dt.date == hoje.date()]
        df_fat_semana = df_fat[df_fat[data_col_fat].dt.isocalendar().week == hoje.isocalendar().week]

        colx, coly = st.columns(2)
        colx.markdown(f'<div class="card info"><span class="card-title">Faturado Hoje</span><b>R$ {df_fat_dia["Total Produto"].sum():,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
        coly.markdown(f'<div class="card info"><span class="card-title">Faturado na Semana</span><b>R$ {df_fat_semana["Total Produto"].sum():,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

    with col_cart:
        st.markdown("### Última Carteira")
        ult_cart = df_cart_mes.sort_values(by=data_col_cart, ascending=False)
        ult_cart[data_col_cart] = ult_cart[data_col_cart].dt.strftime('%d/%m/%Y')
        ult_cart_view = ult_cart[[data_col_cart, 'Cliente', 'Vendedor', 'Valor Receita Bruta Pedido']].head(10)
        ult_cart_view['Valor Receita Bruta Pedido'] = ult_cart_view['Valor Receita Bruta Pedido'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.dataframe(ult_cart_view, height=table_height)

        df_cart_dia = df_cart[df_cart[data_col_cart].dt.date == hoje.date()]
        df_cart_semana = df_cart[df_cart[data_col_cart].dt.isocalendar().week == hoje.isocalendar().week]

        colx, coly = st.columns(2)
        colx.markdown(f'<div class="card info"><span class="card-title">Carteira Hoje</span><b>R$ {df_cart_dia["Valor Receita Bruta Pedido"].sum():,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
        coly.markdown(f'<div class="card info"><span class="card-title">Carteira na Semana</span><b>R$ {df_cart_semana["Valor Receita Bruta Pedido"].sum():,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
