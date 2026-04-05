import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime

# --- 1. MOTOR: CONFIGURAÇÕES INICIAIS ---
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
        from gtts import gTTS
    except ImportError:
        pass

# --- 2. CONTEÚDO: DNA ESTÉTICO & COMPRESSÃO DE SIDEBAR ---
st.markdown("""
    <style>
    footer {visibility: hidden;}
    
    /* Bloqueio de transbordo e largura rigorosa */
    [data-testid='stSidebar'] {
        overflow-x: hidden;
    }
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 310px;
    }

    /* Previne quebra de linha nas siglas de idioma */
    div.stButton > button {
        padding: 2px 2px !important;
        font-size: 14px !important;
        width: 100% !important;
        white-space: nowrap !important;
        overflow: hidden;
    }

    /* Ajuste de colunas para sensores e botões */
    [data-testid="column"] {
        padding: 0 1px !important;
        min-width: 0px !important;
    }

    .reportview-container .main .block-container {
        padding-top: 0rem; padding-right: 0rem; padding-left: 0rem; padding-bottom: 0rem;
    }
    .logo-text {
        font-weight: 600; font-size: 18px; font-family: 'IBM Plex Sans';
        color: #000000; padding-left: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONTEÚDO: INITIALIZE SESSIONSTATE ---
states = {
    "lang": "pt", "last_lang": "pt", "book": "livro vivo", "take": 0,
    "mini": 0, "tema": "Fatos", "visy": True, "draw": True, "talk": False, 
    "vydo": False, "poly_lang": "ca", "poly_name": "català"
}
for key, val in states.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- 4. MOTOR: TOOLS & LOADERS ---

@st.cache_data
def load_help(idiom):
    returns = []
    try:
        with open("./base/helpers.txt", encoding="utf-8") as file:
            for line in file:
                pipe = line.split("|")
                if pipe[1].startswith(idiom + "_"):
                    returns.append(pipe[2])
    except:
        return ["ajuda"] * 10
    return returns

def pick_lang():
    btn_pt, btn_es, btn_it, btn_fr, btn_en, btn_xy = st.sidebar.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
    if btn_pt.button("pt"): st.session_state.lang = "pt"
    if btn_es.button("es"): st.session_state.lang = "es"
    if btn_it.button("it"): st.session_state.lang = "it"
    if btn_fr.button("fr"): st.session_state.lang = "fr"
    if btn_en.button("en"): st.session_state.lang = "en"
    if btn_xy.button("⚒️"): st.session_state.lang = st.session_state.poly_lang

def draw_check_buttons():
    draw_text, talk_text, vyde_text = st.sidebar.columns([3.8, 3.2, 3])
    help_tips = load_help(st.session_state.lang)
    st.session_state.draw = draw_text.checkbox(help_tips[5], st.session_state.draw, key="draw_machina")
    st.session_state.talk = talk_text.checkbox(help_tips[6], st.session_state.talk, key="talk_machina")
    st.session_state.vydo = vyde_text.checkbox(help_tips[7], st.session_state.vydo, key="vyde_machina")

# --- 5. EXECUÇÃO DO COCKPIT ---

with st.sidebar:
    st.markdown("<nav><a href='https://github.com/NandouLopes/yPoemas'>github</a> | <a href='https://youtu.be/uL6T3roTtAs'>youtube</a></nav>", unsafe_allow_html=True)
    pick_lang()
    st.divider()
    draw_check_buttons()

paginas = ["Mini", "yPoemas", "Eureka", "Biblioteca", "Livro Vivo", "Ensaios", "Sobre"]
tabs = st.tabs([p.upper() for p in paginas])
