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

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

if have_internet():
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        pass
    try:
        from gtts import gTTS
    except ImportError:
        pass

# Regra 0: Look & Feel (Botões Compactos e Centralizados)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    
    /* Centraliza e limita a largura da barra de navegação */
    .nav-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    
    [data-testid="stSidebar"] { width: 260px !important; }
    
    /* Botões com largura fixa menor para simetria total */
    div.stButton > button {
        width: 110px !important; 
        border-radius: 12px;
        height: 3.2em;
        background-color: #f8f9fa;
        border: 1px solid #d1d5db;
        transition: all 0.3s ease-in-out;
        font-family: 'IBM Plex Sans';
        font-weight: 500;
        font-size: 13px;
        white-space: nowrap;
        margin: 0 auto;
    }
    
    div.stButton > button:hover {
        border-color: powderblue;
        color: powderblue;
        background-color: white;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
    }

    [data-testid="column"] {
        padding: 0 4px !important;
        display: flex;
        justify-content: center;
    }

    mark { background-color: powderblue; color: black; }
    </style> """,
    unsafe_allow_html=True,
)

if "page" not in st.session_state: st.session_state.page = "mini"

### bof: sidebar (Configurações)

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
st.sidebar.checkbox("Talk (Voz)", value=True)
st.sidebar.checkbox("Draw (Desenho)", value=True)

### bof: navigation (Botões Compactos no Topo)

# Criamos um container centralizado para os botões
_, center_col, _ = st.columns([1, 4, 1]) # Colunas laterais vazias para "espremer" o centro

with center_col:
    nav_cols = st.columns(6)
    with nav_cols[0]:
        if st.button("ツ mini"): st.session_state.page = "mini"
    with nav_cols[1]:
        if st.button("ypoemas"): st.session_state.page = "ypoemas"
    with nav_cols[2]:
        if st.button("eureka"): st.session_state.page = "eureka"
    with nav_cols[3]:
        if st.button("off-machina"): st.session_state.page = "off-machina"
    with nav_cols[4]:
        if st.button("comments"): st.session_state.page = "comments"
    with nav_cols[5]:
        if st.button("sobre"): st.session_state.page = "sobre"

st.markdown("---")

### bof: pages (Abaixo dos Botões)

def page_mini():
    st.subheader("ツ mini")
    st.info("O palco está pronto para a mini-poesia.")

def page_ypoemas():
    st.subheader("ツ ypoemas")
    st.write("Aguardando as definições da máquina.")

def page_eureka():
    st.subheader("ツ eureka")
    st.write("Laboratório de descobertas.")

def page_off_machina():
    st.subheader("ツ off-machina")
    st.write("Galeria de livros impressos.")

def page_comments():
    st.subheader("ツ comments")
    st.write("Notas e interações.")

def page_sobre():
    st.subheader("ツ sobre")
    st.write("A jornada da Machina.")

# Router de exibição centralizada
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

### bof: tools
def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    pass
