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
        if 'Nº Doc SAP' in df_fat.columns and 'Data Emissão' in df_fat.columns:
            df_fat['Data Emissão'] = pd.to_datetime(df_fat['Data Emissão'], errors='coerce')
            ult_fat = df_fat.sort_values(by=['Data Emissão', 'Nº Doc SAP'], ascending=[False, False])
            ult_fat['Data Emissão'] = ult_fat['Data Emissão'].dt.strftime('%d/%m/%Y')
            ult_fat_view = ult_fat[['Nº Doc SAP', 'Data Emissão', 'Cliente', 'Vendedor', 'Total Produto']]
            ult_fat_view = ult_fat_view.rename(columns={'Nº Doc SAP': 'NF'})
            ult_fat_view['Total Produto'] = ult_fat_view['Total Produto'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            st.dataframe(ult_fat_view, height=table_height, use_container_width=True, hide_index=True)
        else:
            st.warning("Colunas 'Nº Doc SAP' ou 'Data Emissão' não encontradas no DataFrame de faturamento.")

    with col_ped:
        st.markdown("### Últimos Pedidos Inclusos")
        if 'Pedido' in df_ped.columns and 'Data Emissao' in df_ped.columns:
            df_ped['Data Emissao'] = pd.to_datetime(df_ped['Data Emissao'], errors='coerce')
            ult_ped_grouped = df_ped.groupby(['Pedido', 'Data Emissao', 'Cliente', 'Vendedor'], as_index=False)['Valor Receita Bruta Pedido'].first()
            ult_ped_grouped = ult_ped_grouped.sort_values(by=['Data Emissao', 'Pedido'], ascending=[False, False])
            ult_ped_grouped['Data Emissao'] = ult_ped_grouped['Data Emissao'].dt.strftime('%d/%m/%Y')
            ult_ped_view = ult_ped_grouped.rename(columns={'Pedido': 'PV'})[['PV', 'Data Emissao', 'Cliente', 'Vendedor', 'Valor Receita Bruta Pedido']]
            ult_ped_view['Valor Receita Bruta Pedido'] = ult_ped_view['Valor Receita Bruta Pedido'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            st.dataframe(ult_ped_view, height=table_height, use_container_width=True, hide_index=True)
        else:
            st.warning("Colunas 'Pedido' ou 'Data Emissao' não encontradas no DataFrame de pedidos.")
