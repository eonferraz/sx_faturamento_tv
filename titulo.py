import streamlit as st

def render_titulo(hoje):
    st.markdown(f"<h2 style='text-align:center;'>Faturamento {hoje.strftime('%B').capitalize()} - SX Lighting</h2>", unsafe_allow_html=True)
