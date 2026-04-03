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
    layout="centered",
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

# Regra 0: Look & Feel (Botões Arredondados e Palco Limpo)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .reportview-container .main .block-container{ padding-top: 1rem; }
    
    [data-testid="stSidebar"] { width: 260px !important; }
    
    /* Design dos Botões Originais */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
        transition: all 0.3s;
        font-family: 'IBM Plex Sans';
        font-weight: 500;
    }
    div.stButton > button:hover {
        border-color: powderblue;
        color: powderblue;
        background-color: white;
    }
    
    mark { background-color: powderblue; color: black; }
    .container { display: flex; }
    .logo-text {
        font-weight: 600; font-size: 18px;
        font-family: 'IBM Plex Sans'; color: #000000;
        padding-top: 0px; padding-left: 15px;
    }
    </style> """,
    unsafe_allow_html=True,
)

# Estado da página (MANDALA)
if "page" not in st.session_state: st.session_state.page = "mini"
if "lang" not in st.session_state: st.session_state.lang = "pt"

### bof: sidebar (Configurações)

st.sidebar.title("Configurações")

mapeamento_artes = {
    "mini": "img_mini.jpg",
    "ypoemas": "img_ypoemas.jpg",
    "eureka": "img_eureka.jpg",
    "off-machina": "img_off-machina.jpg",
    "sobre": "img_about.jpg"
}

# Exibição da arte na sidebar (atualiza conforme o clique nos botões)
arte_atual = mapeamento_artes.get(st.session_state.page)
if arte_atual and os.path.exists(arte_atual):
    st.sidebar.image(arte_atual, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.selectbox("Idioma", ["Português", "English", "Français"], key="sel_lang")
st.sidebar.checkbox("Talk (Voz)", value=True)
st.sidebar.checkbox("Draw (Desenho)", value=True)

### bof: navigation (Os Botões Originais no Topo)

# Criamos colunas para o deslocamento horizontal
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("ツ mini"): st.session_state.page = "mini"
with col2:
    if st.button("ypoemas"): st.session_state.page = "ypoemas"
with col3:
    if st.button("eureka"): st.session_state.page = "eureka"
with col4:
    if st.button("off-machina"): st.session_state.page = "off-machina"
with col5:
    if st.button("sobre"): st.session_state.page = "sobre"

st.markdown("---")

### bof: pages

def page_mini():
    st.subheader("ツ mini")
    st.write("Aprovada !!! goi'n to next")

def page_ypoemas():
    st.subheader("ツ ypoemas")
    st.write("Em estudo...")

def page_eureka():
    st.subheader("ツ eureka")
    st.write("Em estudo...")

def page_off_machina():
    st.subheader("ツ off-machina")
    st.info("Cópias digitais de livros impressos.")

def page_sobre():
    st.subheader("ツ sobre")
    st.write("Under Construction")

# Router baseado no clique do botão
if st.session_state.page == "mini":
    page_mini()
elif st.session_state.page == "ypoemas":
    page_ypoemas()
elif st.session_state.page == "eureka":
    page_eureka()
elif st.session_state.page == "off-machina":
    page_off_machina()
elif st.session_state.page == "sobre":
    page_sobre()

### bof: tools
def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    pass
