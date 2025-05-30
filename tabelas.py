import streamlit as st

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
        ult_fat = df_fat.sort_values(by=['Data Emissão', 'Nota Fiscal'], ascending=[False, False])
        ult_fat['Data Emissão'] = ult_fat['Data Emissão'].dt.strftime('%d/%m/%Y')
        if 'Nota Fiscal' in ult_fat.columns:
            ult_fat_view = ult_fat[['Nota Fiscal', 'Data Emissão', 'Cliente', 'Vendedor', 'Total Produto']]
            ult_fat_view = ult_fat_view.rename(columns={'Nota Fiscal': 'NF'})
        else:
            ult_fat_view = ult_fat[['Data Emissão', 'Cliente', 'Vendedor', 'Total Produto']]
        ult_fat_view['Total Produto'] = ult_fat_view['Total Produto'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.dataframe(ult_fat_view, height=table_height, use_container_width=True, hide_index=True)

    with col_ped:
        st.markdown("### Últimos Pedidos Inclusos")
        ult_ped = df_ped.copy()
        if 'Pedido' in ult_ped.columns:
            ult_ped_grouped = ult_ped.groupby(['Pedido', 'Data Emissao', 'Cliente', 'Vendedor'], as_index=False)['Valor Receita Bruta Pedido'].sum()
            ult_ped_grouped = ult_ped_grouped.sort_values(by=['Data Emissao', 'Pedido'], ascending=[False, False])
            ult_ped_grouped['Data Emissao'] = ult_ped_grouped['Data Emissao'].dt.strftime('%d/%m/%Y')
            ult_ped_view = ult_ped_grouped.rename(columns={'Pedido': 'PV'})[['PV', 'Data Emissao', 'Cliente', 'Vendedor', 'Valor Receita Bruta Pedido']]
        else:
            ult_ped_view = ult_ped[['Data Emissao', 'Cliente', 'Vendedor', 'Valor Receita Bruta Pedido']]
        ult_ped_view['Valor Receita Bruta Pedido'] = ult_ped_view['Valor Receita Bruta Pedido'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.dataframe(ult_ped_view, height=table_height, use_container_width=True, hide_index=True)
