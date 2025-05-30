import streamlit as st
import pandas as pd

def render_tabelas(df_fat, df_ped, hoje):
    table_height = 450

    st.markdown("""
        <style>
        .css-1d391kg .e1f1d6gn2 {font-size: 18px;} /* Título das tabelas */
        .css-1v0mbdj .e1f1d6gn1 {font-size: 16px;} /* Conteúdo das tabelas */
        </style>
    """, unsafe_allow_html=True)

    col_fat, col_ped = st.columns(2)

    with col_fat:
        st.markdown("### Últimos Faturamentos")

        # Padroniza nomes de colunas
        df_fat = df_fat.rename(columns={
            'Doc SAP': 'DocNum',
            'Nº Doc SAP': 'DocNum',
            'Data Emissão': 'DataEmissao',
            'Cliente': 'Cliente',
            'Vendedor': 'Vendedor',
            'Total Produto': 'TotalProduto'
        })

        if 'DocNum' in df_fat.columns and 'DataEmissao' in df_fat.columns:
            df_fat['DataEmissao'] = pd.to_datetime(df_fat['DataEmissao'], errors='coerce')
            ult_fat = df_fat.groupby(['DocNum', 'DataEmissao', 'Cliente', 'Vendedor'], as_index=False)['TotalProduto'].sum()
            ult_fat = ult_fat.sort_values(by=['DataEmissao', 'DocNum'], ascending=[False, False])
            ult_fat['DataEmissao'] = ult_fat['DataEmissao'].dt.strftime('%d/%m/%Y')
            ult_fat_view = ult_fat.rename(columns={'DocNum': 'NF', 'DataEmissao': 'Data Emissão', 'TotalProduto': 'Total Produto'})[['NF', 'Data Emissão', 'Cliente', 'Vendedor', 'Total Produto']]
            ult_fat_view['Total Produto'] = ult_fat_view['Total Produto'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            st.dataframe(ult_fat_view, height=table_height, use_container_width=True, hide_index=True)
        else:
            st.warning(f"Colunas 'DocNum' ou 'DataEmissao' não encontradas no DataFrame de faturamento.")

    with col_ped:
        st.markdown("### Últimos Pedidos Inclusos")

        df_ped = df_ped.rename(columns={
            'Pedido': 'Pedido',
            'Data Emissao': 'DataEmissao',
            'Cliente': 'Cliente',
            'Vendedor': 'Vendedor',
            'Valor Receita Bruta Pedido': 'ValorReceitaBrutaPedido'
        })

        if 'Pedido' in df_ped.columns and 'DataEmissao' in df_ped.columns:
            df_ped['DataEmissao'] = pd.to_datetime(df_ped['DataEmissao'], errors='coerce')
            ult_ped_grouped = df_ped.groupby(['Pedido', 'DataEmissao', 'Cliente', 'Vendedor'], as_index=False)['ValorReceitaBrutaPedido'].sum()
            ult_ped_grouped = ult_ped_grouped.sort_values(by=['DataEmissao', 'Pedido'], ascending=[False, False])
            ult_ped_grouped['DataEmissao'] = ult_ped_grouped['DataEmissao'].dt.strftime('%d/%m/%Y')
            ult_ped_view = ult_ped_grouped.rename(columns={'Pedido': 'PV', 'DataEmissao': 'Data Emissão', 'ValorReceitaBrutaPedido': 'Valor Receita Bruta Pedido'})[['PV', 'Data Emissão', 'Cliente', 'Vendedor', 'Valor Receita Bruta Pedido']]
            ult_ped_view['Valor Receita Bruta Pedido'] = ult_ped_view['Valor Receita Bruta Pedido'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            st.dataframe(ult_ped_view, height=table_height, use_container_width=True, hide_index=True)
        else:
            st.warning("Colunas 'Pedido' ou 'DataEmissao' não encontradas no DataFrame de pedidos.")
