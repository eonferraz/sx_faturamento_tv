import streamlit as st
import plotly.graph_objects as go

def render_termometro(df_fat, df_cart, META_MENSAL, hoje):
    data_col_fat = 'Data Emissão'
    data_col_cart = 'Data Entrega'
    mes_atual = hoje.month
    ano_atual = hoje.year

    df_fat_mes = df_fat[(df_fat[data_col_fat].dt.month == mes_atual) & (df_fat[data_col_fat].dt.year == ano_atual)]
    realizado = df_fat_mes['Total Produto'].sum()

    df_cart_mes = df_cart[(df_cart[data_col_cart].dt.month == mes_atual) & (df_cart[data_col_cart].dt.year == ano_atual)]
    carteira = df_cart_mes['Valor Receita Bruta Pedido'].sum()

    restante = max(META_MENSAL - realizado - carteira, 0)

    perc_realizado = min(realizado / META_MENSAL * 100, 100)
    perc_carteira = min(carteira / META_MENSAL * 100, 100)
    perc_restante = max(100 - perc_realizado - perc_carteira, 0)

    fig_termo = go.Figure()
    fig_termo.add_trace(go.Bar(x=[realizado], orientation='h', marker=dict(color='#2ca02c'), text=[f'{perc_realizado:.1f}%'], textposition='auto', textfont=dict(size=18)))
    fig_termo.add_trace(go.Bar(x=[carteira], orientation='h', marker=dict(color='#ff7f0e'), text=[f'{perc_carteira:.1f}%'], textposition='auto', textfont=dict(size=18)))
    fig_termo.add_trace(go.Bar(x=[restante], orientation='h', marker=dict(color='#d62728'), text=[f'{perc_restante:.1f}%'], textposition='auto', textfont=dict(size=18)))

    fig_termo.update_layout(barmode='stack', height=80, margin=dict(t=10, b=10), showlegend=False, yaxis=dict(showticklabels=False))
    st.plotly_chart(fig_termo, use_container_width=True)
