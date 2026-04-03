import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime
from lay_2_ypo import gera_poema

### bof: settings

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="wide",
    initial_sidebar_state="auto",
)

if "page" not in st.session_state: 
    st.session_state.page = "mini"

# Regra 0: Look & Feel (Trilho de Scroll do yPo)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .main .block-container {
        max-width: 98% !important;
        padding-top: 1.5rem;
    }
    
    /* Configuração do Trilho de Navegação */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        gap: 10px !important;
        padding-bottom: 25px !important;
    }

    /* Trava de largura para os botões */
    [data-testid="column"] {
        flex: 0 0 auto !important;
        width: 125px !important;
    }

    /* Estilo dos Botões */
    div.stButton > button {
        width: 120px !important; 
        border-radius: 12px;
        height: 3.2em;
        background-color: #f8f9fa;
        border: 1px solid #d1d5db;
        font-family: 'IBM Plex Sans';
        font-size: 13px;
        white-space: nowrap;
    }
    
    div.stButton > button:hover {
        border-color: powderblue;
        color: powderblue;
        background-color: white;
    }

    /* Barra de scroll */
    [data-testid="stHorizontalBlock"]::-webkit-scrollbar {
        height: 6px;
    }
    [data-testid="stHorizontalBlock"]::-webkit-scrollbar-thumb {
        background: powderblue;
        border-radius: 10px;
    }
    </style> """,
    unsafe_allow_html=True,
)

### bof: navigation (O Trilho)

nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
labels = ["ツ mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]

for i in range(6):
    with nav_cols[i]:
        if st.button(labels[i], key=f"btn_nav_{paginas[i]}"):
            st.session_state.page = paginas[i]
            st.rerun()

st.markdown("---")

### bof: sidebar (Bastidores)

st.sidebar.title("Configurações")

mapeamento_artes = {
    "mini": "img_mini.jpg",
    "ypoemas": "img_ypoemas.jpg",
    "eureka": "img_eureka.jpg",
    "off-machina": "img_off-machina.jpg",
    "comments": "img_poly.jpg",
    "sobre": "img_about.jpg"
}

arte_atual = mapeamento_artes.get(st.session_state.page)
if arte_atual and os.path.exists(arte_atual):
    st.sidebar.image(arte_atual, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.selectbox("Idioma", ["Português", "English", "Français"], key="sel_lang")
st.sidebar.checkbox("Talk (Áudio)", value=True)
st.sidebar.checkbox("Draw (Imagem)", value=True)

### bof: pages

def page_mini():
    st.subheader("ツ mini")
    st.info("Trilho de botões com rolagem lateral ativo.")

def page_ypoemas():
    st.subheader("ツ ypoemas")

def page_eureka():
    st.subheader("ツ eureka")

def page_off_machina():
    st.subheader("ツ off-machina")

def page_comments():
    st.subheader("ツ comments")

def page_sobre():
    st.subheader("ツ sobre")

# Router
if st.session_state.page == "mini":
    page_mini()
elif st.session_state.page == "ypoemas":
    page_ypoemas()
elif st.session_state.page == "eureka":
    page_eureka()
elif st.session_state.page == "off-machina":
    page_off_machina()
elif st.session_state.page == "comments":
    page_comments()
elif st.session_state.page == "sobre":
    page_sobre()
