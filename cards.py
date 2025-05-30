import streamlit as st

def render_cards(df_fat, df_cart, df_ped, META_MENSAL, hoje):
    data_col_fat = 'Data Emissão'
    data_col_cart = 'Data Entrega'
    data_col_ped = 'Data Emissao'

    mes_atual = hoje.month
    ano_atual = hoje.year

    df_fat_mes = df_fat[(df_fat[data_col_fat].dt.month == mes_atual) & (df_fat[data_col_fat].dt.year == ano_atual)]
    df_cart_mes = df_cart[(df_cart[data_col_cart].dt.month == mes_atual) & (df_cart[data_col_cart].dt.year == ano_atual)]
    df_ped_mes = df_ped[(df_ped[data_col_ped].dt.month == mes_atual) & (df_ped[data_col_ped].dt.year == ano_atual)]

    realizado = df_fat_mes['Total Produto'].sum()
    carteira = df_cart_mes['Valor Receita Bruta Pedido'].sum()
    restante = max(META_MENSAL - realizado - carteira, 0)

    st.markdown("""
        <style>
        .card { border-radius: 2px; padding: 12px; margin-bottom: 10px; color: white; text-align: center; }
        .card b { font-size: 44px; }
        .card-title { font-size: 20px; display: block; }
        .meta { background-color: #0160A2; }
        .realizado { background-color: #A0C63F; }
        .carteira { background-color: #FFC000; }
        .restante { background-color: #d62728; }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f'<div class="card meta"><span class="card-title">Meta Mensal</span><b>R$ {META_MENSAL:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col2.markdown(f'<div class="card realizado"><span class="card-title">Faturado</span><b>R$ {realizado:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col3.markdown(f'<div class="card carteira"><span class="card-title">Carteira</span><b>R$ {carteira:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    col4.markdown(f'<div class="card restante"><span class="card-title">Restante</span><b>R$ {restante:,.2f}</b></div>'.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
