import streamlit as st
import plotly.graph_objects as go

def render_termometro(df_fat, df_cart, META_MENSAL, hoje):
    data_col_fat = 'Data Emissão'
    mes_atual = hoje.month
    ano_atual = hoje.year

    df_fat_mes = df_fat[(df_fat[data_col_fat].dt.month == mes_atual) & (df_fat[data_col_fat].dt.year == ano_atual)]
    realizado = df_fat_mes['Total Produto'].sum()
    carteira = df_cart['Valor Receita Bruta Pedido'].sum()
    restante = max(META_MENSAL - realizado - carteira, 0)

    perc_realizado = min(realizado / META_MENSAL * 100, 100)
    perc_carteira = min(carteira / META_MENSAL * 100, 100)
    perc_restante = max(100 - perc_realizado - perc_carteira, 0)

    # Exibir os valores calculados no Streamlit
    st.write(f"✅ **Realizado:** R$ {realizado:,.2f}")
    st.write(f"📦 **Carteira:** R$ {carteira:,.2f}")
    st.write(f"⏳ **Restante:** R$ {restante:,.2f}")
    st.write(f"🎯 **Meta Mensal:** R$ {META_MENSAL:,.2f}")

    fig_termo = go.Figure()
    fig_termo.add_trace(go.Bar(y=['Meta'], x=[realizado], orientation='h', marker=dict(color='#2ca02c'), text=[f'{perc_realizado:.1f}%'], textposition='auto', textfont=dict(size=18)))
    fig_termo.add_trace(go.Bar(y=['Meta'], x=[carteira], orientation='h', marker=dict(color='#ff7f0e'), text=[f'{perc_carteira:.1f}%'], textposition='auto', textfont=dict(size=18)))
    fig_termo.add_trace(go.Bar(y=['Meta'], x=[restante], orientation='h', marker=dict(color='#d62728'), text=[f'{perc_restante:.1f}%'], textposition='auto', textfont=dict(size=18)))
    fig_termo.update_layout(barmode='stack', height=80, margin=dict(t=10, b=10), showlegend=False)
    st.plotly_chart(fig_termo, use_container_width=True)
