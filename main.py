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

# Regra 0: Look & Feel (Sidebar 260px)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .reportview-container .main .block-container{ padding: 0rem; }
    
    [data-testid="stSidebar"] {
        width: 260px !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        width: 260px !important;
    }
    
    mark { background-color: powderblue; color: black; }
    .container { display: flex; }
    .logo-text {
        font-weight: 600; font-size: 18px;
        font-family: 'IBM Plex Sans'; color: #000000;
        padding-top: 0px; padding-left: 15px;
    }
    .logo-img { float:right; }
    </style> """,
    unsafe_allow_html=True,
)

if "lang" not in st.session_state: st.session_state.lang = "pt"
if "tema" not in st.session_state: st.session_state.tema = "Fatos"

### bof: navigation

# Menu Principal Atualizado (Regra 1, 2 e 3)
menu_opcoes = ["mini", "ypoemas", "eureka", "off-machina", "sobre"]
pagina_selecionada = st.sidebar.selectbox("MANDALA / Menu Principal", menu_opcoes)

# Mapeamento de Artes (Regra 0 & 3)
mapeamento_artes = {
    "mini": "img_mini.jpg",
    "ypoemas": "img_ypoemas.jpg",
    "eureka": "img_eureka.jpg",
    "off-machina": "img_off-machina.jpg",
    "sobre": "img_about.jpg"
}

arte_atual = mapeamento_artes.get(pagina_selecionada)

if arte_atual and os.path.exists(arte_atual):
    st.sidebar.image(arte_atual, use_container_width=True)
else:
    st.sidebar.warning(f"🖼️ [Arquivo {arte_atual} não localizado]")

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
    st.info("Fora da máquina: cópias digitais de livros impressos.")
    st.write("Under Construction")

def page_sobre():
    st.subheader("ツ sobre")
    st.write("Under Construction")

# Execução da Navegação
if pagina_selecionada == "mini":
    page_mini()
elif pagina_selecionada == "ypoemas":
    page_ypoemas()
elif pagina_selecionada == "eureka":
    page_eureka()
elif pagina_selecionada == "off-machina":
    page_off_machina()
elif pagina_selecionada == "sobre":
    page_sobre()

### bof: tools

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    if LOGO_IMAGE == None:
        st.markdown(f"<div class='container'><p class='logo-text'>{LOGO_TEXTO}</p></div>", unsafe_allow_html=True)
    else:
        with open(LOGO_IMAGE, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        st.markdown(
            f"<div class='container'><img class='logo-img' src='data:image/jpg;base64,{img_data}'><p class='logo-text'>{LOGO_TEXTO}</p></div>",
            unsafe_allow_html=True
        )
        
