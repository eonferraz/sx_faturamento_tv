import streamlit as st
import plotly.graph_objects as go

COLOR_REALIZADO = '#2ca02c'
COLOR_CARTEIRA = '#ff7f0e'
COLOR_RESTANTE = '#d62728'

def render_termometro(realizado, carteira, restante, meta_mensal):
    perc_realizado = min((realizado / meta_mensal) * 100, 100)
    perc_carteira = min((carteira / meta_mensal) * 100, 100)
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
