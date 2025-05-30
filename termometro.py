import streamlit as st
import plotly.graph_objects as go

COLOR_REALIZADO = '#2ca02c'
COLOR_CARTEIRA = '#ff7f0e'
COLOR_RESTANTE = '#d62728'

def render_termometro(df_fat, df_cart, meta_mensal):
    try:
        realizado = df_fat['Total Produto'].sum() if 'Total Produto' in df_fat.columns else 0
        carteira = df_cart['Valor Receita Bruta Pedido'].sum() if 'Valor Receita Bruta Pedido' in df_cart.columns else 0
        restante = max(meta_mensal - realizado - carteira, 0)

        perc_realizado = min((realizado / meta_mensal) * 100, 100) if meta_mensal > 0 else 0
        perc_carteira = min((carteira / meta_mensal) * 100, 100) if meta_mensal > 0 else 0
        perc_restante = max(100 - perc_realizado - perc_carteira, 0)

        fig_termo = go.Figure()
        fig_termo.add_trace(go.Bar(
            y=['Meta'],
            x=[realizado],
            orientation='h',
            marker=dict(color=COLOR_REALIZADO),
            text=[f'{perc_realizado:.1f}%'],
            textposition='inside',
            textfont=dict(size=18)
        ))
        fig_termo.add_trace(go.Bar(
            y=['Meta'],
            x=[carteira],
            orientation='h',
            marker=dict(color=COLOR_CARTEIRA),
            text=[f'{perc_carteira:.1f}%'],
            textposition='inside',
            textfont=dict(size=18)
        ))
        fig_termo.add_trace(go.Bar(
            y=['Meta'],
            x=[restante],
            orientation='h',
            marker=dict(color=COLOR_RESTANTE),
            text=[f'{perc_restante:.1f}%'],
            textposition='inside',
            textfont=dict(size=18)
        ))

        fig_termo.update_layout(
            barmode='stack',
            height=100,
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False)
        )

        st.plotly_chart(fig_termo, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar termômetro: {e}")
