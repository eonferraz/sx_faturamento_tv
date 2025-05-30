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

    # Garantir que estamos usando os nomes corretos das colunas das queries fornecidas
    with col_fat:
        st.markdown("### Últimas Datas de Faturamento")
        if 'DocDate' in df_fat.columns:
            ult_fat = df_fat.sort_values(by='DocDate', ascending=False)
            ult_fat['DocDate'] = ult_fat['DocDate'].dt.strftime('%d/%m/%Y')
            ult_fat_view = ult_fat[['DocDate']].head(10)
            ult_fat_view = ult_fat_view.rename(columns={'DocDate': 'Data Faturamento'})
            st.dataframe(ult_fat_view, height=table_height)
        else:
            st.warning("Coluna 'DocDate' não encontrada no DataFrame de faturamento.")

    with col_ped:
        st.markdown("### Últimas Datas de Inclusão de Pedidos")
        if 'DocDate' in df_ped.columns:
            ult_ped = df_ped.sort_values(by='DocDate', ascending=False)
            ult_ped['DocDate'] = ult_ped['DocDate'].dt.strftime('%d/%m/%Y')
            ult_ped_view = ult_ped[['DocDate']].head(10)
            ult_ped_view = ult_ped_view.rename(columns={'DocDate': 'Data Inclusão Pedido'})
            st.dataframe(ult_ped_view, height=table_height)
        else:
            st.warning("Coluna 'DocDate' não encontrada no DataFrame de pedidos.")
