import streamlit as st
import locale

# Define locale para português
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

def render_titulo(hoje):
    mes_portugues = hoje.strftime('%B').capitalize()
    st.markdown(f"<h2 style='text-align:center;'>Faturamento {mes_portugues} - SX Lighting</h2>", unsafe_allow_html=True)
