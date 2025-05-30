import streamlit as st

def render_tabelas(df_fat, df_ped, hoje):
    table_height = 450

    # Aplicar estilo global maior
    st.markdown("""
        <style>
        .css-1d391kg .e1f1d6gn2 {font-size: 18px;} /* Título das tabelas */
        .css-1v0mbdj .e1f1d6gn1 {font-size: 16px;} /* Conteúdo das tabelas */
        </style>
    """, unsafe_allow_html=True)

    col_fat, col_ped = st.columns(2)

    with col_fat:
        st.markdown("### Últimos Faturamentos")
        ult_fat = df_fat.sort_values(by='Data Emissão', ascending=False)
        ult_fat['Data Emissão'] = ult_fat['Data Emissão'].dt.strftime('%d/%m/%Y')
        ult_fat_view = ult_fat[['Data Emissão', 'Cliente', 'Vendedor', 'Total Produto']].head(10)
        ult_fat_view['Total Produto'] = ult_fat_view['Total Produto'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.dataframe(ult_fat_view.style.hide(axis='index'), height=table_height)

    with col_ped:
        st.markdown("### Últimos Pedidos Inclusos")
        ult_ped = df_ped.sort_values(by='Data Emissao', ascending=False)
        ult_ped['Data Emissao'] = ult_ped['Data Emissao'].dt.strftime('%d/%m/%Y')
        ult_ped_view = ult_ped[['Data Emissao', 'Cliente', 'Vendedor', 'Valor Receita Bruta Pedido']].head(10)
        ult_ped_view['Valor Receita Bruta Pedido'] = ult_ped_view['Valor Receita Bruta Pedido'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.dataframe(ult_ped_view.style.hide(axis='index'), height=table_height)
