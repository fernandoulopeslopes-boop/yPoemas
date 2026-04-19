import streamlit as st
import os
from lay_2_ypo import gera_poema

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(
    page_title="a Máquina de Fazer Poesia",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS: Fixar largura da sidebar (300px) e customização técnica
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            min-width: 300px;
            max-width: 300px;
        }
        .stMarkdown p {
            text-align: justify;
        }
        .stButton button {
            width: 100%;
