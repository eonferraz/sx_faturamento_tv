import streamlit as st
import pandas as pd
import pyodbc
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard de Faturamento", layout="wide")
st.title("📦 Dashboard de Faturamento - SX Group")

META_MENSAL = 5_000_000

# Função de conexão
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

# Obter dados
df = get_faturamento_data()

if df.empty:
    st.warning("Nenhum dado retornado.")
else:
    # Corrigir colunas duplicadas automaticamente
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
        return new_columns

    df.columns = dedup_columns(df.columns)

    # Filtros de data e receita
    df['Data Emissão'] = pd.to_datetime(df['Data Emissão'])
    df = df[df['Receita'] == 'SIM']

    hoje = datetime.today()
    mes_atual = hoje.month
    ano_atual = hoje.year
    dias_mes = (datetime(ano_atual, mes_atual % 12 + 1, 1) - timedelta(days=1)).day

    df_mes = df[(df['Data Emissão'].dt.month == mes_atual) & (df['Data Emissão'].dt.year == ano_atual)]

    # Linha 1 - Termômetro (barra empilhada horizontal)
    realizado = df_mes['Total Produto'].sum()
    pendente = max(META_MENSAL - realizado, 0)

    st.subheader(f"Meta Mensal: R$ {META_MENSAL:,.2f} | Realizado: R$ {realizado:,.2f}")

    fig_termo = go.Figure()
    fig_termo.add_trace(go.Bar(
        y=['Meta'],
        x=[realizado],
        name='Realizado',
        orientation='h',
        marker=dict(color='green')
    ))
    fig_termo.add_trace(go.Bar(
        y=['Meta'],
        x=[pendente],
        name='Pendente',
        orientation='h',
        marker=dict(color='lightgray')
    ))
    fig_termo.update_layout(barmode='stack', height=100, showlegend=True)
    st.plotly_chart(fig_termo, use_container_width=True)

    # Linha 2 - Duas colunas
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧾 Últimos 10 faturamentos")
        ultimos = df_mes.sort_values(by='Data Emissão', ascending=False).head(10)
        ultimos['Data Emissão'] = ultimos['Data Emissão'].dt.strftime('%d/%m/%Y')
        ultimos_view = ultimos[['Data Emissão', 'Cliente', 'Vendedor', 'Total Produto']]
        ultimos_view['Total Produto'] = ultimos_view['Total Produto'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.dataframe(ultimos_view)

    with col2:
        st.markdown("### 🏅 Top 5 Vendedores no mês")
        ranking = df_mes.groupby('Vendedor')['Total Produto'].sum().sort_values(ascending=False).head(5).reset_index()
        ranking['Total Produto'] = ranking['Total Produto'].round(2)
        fig_ranking = px.bar(
            ranking,
            y='Vendedor',
            x='Total Produto',
            orientation='h',
            text='Total Produto',
            title='Top Vendedores'
        )
        fig_ranking.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig_ranking.update_layout(xaxis_tickformat=",.2f", yaxis=dict(autorange="reversed"))
        fig_ranking.update_layout(height=300)
        st.plotly_chart(fig_ranking, use_container_width=True)

    # Linha 3 - Faturamento acumulado x Meta
    st.markdown("### 📈 Evolução do Faturamento no Mês")
    df_mes['Dia'] = df_mes['Data Emissão'].dt.day
    acumulado = df_mes.groupby('Dia')['Total Produto'].sum().cumsum().reset_index()
    acumulado['Meta Linear'] = (META_MENSAL / dias_mes) * acumulado['Dia']
    fig_acum = px.line(
        acumulado,
        x='Dia',
        y=['Total Produto', 'Meta Linear'],
        labels={'value': 'R$', 'variable': 'Legenda'},
        title='Faturamento Acumulado vs. Meta Linear'
    )
    fig_acum.update_layout(height=350)
    fig_acum.update_yaxes(tickformat=".2f")
    st.plotly_chart(fig_acum, use_container_width=True)
