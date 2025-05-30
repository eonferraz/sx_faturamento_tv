import streamlit as st

def render_titulo(hoje):
    meses_pt = {
        'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
        'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
        'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
        'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
    }
    mes_portugues = meses_pt[hoje.strftime('%B')]
    st.markdown(f"<h2 style='text-align:center;'>Faturamento {mes_portugues} - SX Lighting</h2>", unsafe_allow_html=True)
