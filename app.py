import streamlit as st
import pandas as pd
import pyodbc
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard de Faturamento", layout="wide")

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
    df['Data Emissão'] = pd.to_datetime(df['Data Emissão'])
    df = df[df['Receita'] == 'SIM']

    hoje = datetime.today()
    mes_atual = hoje.month
    ano_atual = hoje.year
    dias_mes = (datetime(ano_atual, mes_atual % 12 + 1, 1) - timedelta(days=1)).day

    df_mes = df[(df['Data Emissão'].dt.month == mes_atual) & (df['Data Emissão'].dt.year == ano_atual)]
    df_dia = df[df['Data Emissão'].dt.date == hoje.date()]
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    df_semana = df[df['Data Emissão'].dt.date >= inicio_semana.date()]

    realizado = df_mes['Total Produto'].sum()
    pendente = max(META_MENSAL - realizado, 0)
    perc_realizado = min(realizado / META_MENSAL * 100, 100)
    valor_dia = df_dia['Total Produto'].sum()
    valor_semana = df_semana['Total Produto'].sum()

    st.markdown("""
        <style>
        .card {
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 10px;
            color: white;
            text-align: center;
            font-size: 18px;
        }
        .meta { background-color: #1f77b4; }
        .realizado { background-color: #2ca02c; }
        .pendente { background-color: #d62728; }
        .info { background-color: #6c757d; }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.markdown(f'<div class="card meta">Meta Mensal<br><b>R$ {META_MENSAL:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col2.markdown(f'<div class="card realizado">Faturado no Mês<br><b>R$ {realizado:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col3.markdown(f'<div class="card pendente">Pendente<br><b>R$ {pendente:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col4.markdown(f'<div class="card info">Faturado no Dia<br><b>R$ {valor_dia:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col5.markdown(f'<div class="card info">Faturado na Semana<br><b>R$ {valor_semana:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

    fig_termo = go.Figure()
    fig_termo.add_trace(go.Bar(
        y=['Meta'],
        x=[realizado],
        name='Realizado',
        orientation='h',
        marker=dict(color='green'),
        text=f'{perc_realizado:.1f}%',
        textposition='inside'
    ))
    fig_termo.add_trace(go.Bar(
        y=['Meta'],
        x=[pendente],
        name='Pendente',
        orientation='h',
        marker=dict(color='lightgray')
    ))
    fig_termo.update_layout(barmode='stack', height=125, margin=dict(t=20, b=20), showlegend=True)
    st.plotly_chart(fig_termo, use_container_width=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Últimos faturamentos")
        ultimos = df_mes.sort_values(by='Data Emissão', ascending=False).head(10)
        ultimos['Data Emissão'] = ultimos['Data Emissão'].dt.strftime('%d/%m/%Y')
        ultimos_view = ultimos[['Data Emissão', 'Cliente', 'Vendedor', 'Total Produto']]
        ultimos_view['Total Produto'] = ultimos_view['Total Produto'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.dataframe(ultimos_view, height=550)

    with col2:
        st.markdown("### Ranking de Vendedores")
        ranking = df_mes.groupby('Vendedor')['Total Produto'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_ranking = px.bar(
            ranking,
            y='Vendedor',
            x='Total Produto',
            orientation='h',
            text=ranking['Total Produto'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        )
        fig_ranking.update_traces(textposition='outside')
        fig_ranking.update_layout(
            height=550,
            margin=dict(t=20),
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_ranking, use_container_width=True)

    df_mes['Dia'] = df_mes['Data Emissão'].dt.day
    acumulado = df_mes.groupby('Dia')['Total Produto'].sum().cumsum().reset_index()
    acumulado['Meta Linear'] = (META_MENSAL / dias_mes) * acumulado['Dia']
    fig_acum = px.line(
        acumulado,
        x='Dia',
        y=['Total Produto', 'Meta Linear'],
        labels={'value': 'R$', 'variable': 'Legenda'}
    )
    fig_acum.update_layout(height=350, margin=dict(t=20))
    fig_acum.update_yaxes(tickformat=".2f")
    st.plotly_chart(fig_acum, use_container_width=True)
