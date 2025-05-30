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
        st.markdown("### Últimas Datas de Faturamento")
        ult_fat = df_fat.sort_values(by='Data Faturamento', ascending=False)
        ult_fat['Data Faturamento'] = ult_fat['Data Faturamento'].dt.strftime('%d/%m/%Y')
        ult_fat_view = ult_fat[['Data Faturamento']].head(10)
        st.dataframe(ult_fat_view, height=table_height)

    with col_ped:
        st.markdown("### Últimas Datas de Inclusão de Pedidos")
        ult_ped = df_ped.sort_values(by='Data Emissao', ascending=False)
        ult_ped['Data Emissao'] = ult_ped['Data Emissao'].dt.strftime('%d/%m/%Y')
        ult_ped_view = ult_ped[['Data Emissao']].head(10)
        st.dataframe(ult_ped_view, height=table_height)
