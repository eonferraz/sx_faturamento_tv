import streamlit as st
import pandas as pd
from utils.db import get_faturamento_data

st.set_page_config(page_title="Dashboard de Faturamento", layout="wide")

st.title("📦 Dashboard de Faturamento - SX Group")

df = get_faturamento_data()

if df.empty:
    st.warning("Nenhum dado encontrado.")
else:
    with st.sidebar:
        st.markdown("## Filtros")
        filiais = st.multiselect("Filial", df["Filial"].unique(), default=df["Filial"].unique())
        tipos = st.multiselect("Tipo Documento", df["Tipo Doc"].unique(), default=df["Tipo Doc"].unique())
        clientes = st.multiselect("Cliente", df["Cliente"].unique(), default=df["Cliente"].unique())

    df_filtered = df[
        (df["Filial"].isin(filiais)) &
        (df["Tipo Doc"].isin(tipos)) &
        (df["Cliente"].isin(clientes))
    ]

    st.metric("Total Faturado", f"R$ {df_filtered['Total Produto'].sum():,.2f}")
    st.metric("CMV Total", f"R$ {df_filtered['CMV'].sum():,.2f}")
    
    st.dataframe(df_filtered)

    st.bar_chart(df_filtered.groupby("Filial")["Total Produto"].sum())

