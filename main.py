import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime

# --- 1. MOTOR: SETTINGS & CONEXÃO ---
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

# Carregamento do Motor de Tradução e Voz
if have_internet():
    try:
        from deep_translator import GoogleTranslator
        from gtts import gTTS
    except ImportError:
        pass

# Identificação de Telemetria (Backup)
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# --- 2. CONTEÚDO: DNA ESTÉTICO (CSS RIGOROSO) ---
st.markdown("""
    <style>
    footer {visibility: hidden;}
    .reportview-container .main .block-container {
        padding-top: 0rem; padding-right: 0rem; padding-left: 0rem; padding-bottom: 0rem;
    }
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 310px;
    }
    mark { background-color: powderblue; color: black; }
    .container { display: flex; }
    .logo-text {
        font-weight: 600; font-size: 18px; font-family: 'IBM Plex Sans';
        color: #000000; padding-top: 0px; padding-left: 15px;
    }
    .logo-img { float:right; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONTEÚDO: INITIALIZE SESSIONSTATE ---
if "lang" not in st.session_state: st.session_state.lang = "pt"
if "last_lang" not in st.session_state: st.session_state.last_lang = "pt"
if "book" not in st.session_state: st.session_state.book = "livro vivo"
if "take" not in st.session_state: st.session_state.take = 0
if "mini" not in st.session_state: st.session_state.mini = 0
if "tema" not in st.session_state: st.session_state.tema = "Fatos"
if "visy" not in st.session_state: st.session_state.visy = True
if "draw" not in st.session_state: st.session_state.draw = True
if "talk" not in st.session_state: st.session_state.talk = False
if "vydo" not in st.session_state: st.session_state.vydo = False
if "poly_lang" not in st.session_state: st.session_state.poly_lang = "ca"
if "poly_name" not in st.session_state: st.session_state.poly_name = "català"

# --- 4. MOTOR: TOOLS & LOADERS (OTIMIZADOS) ---

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
    # Pesos decimais exatos do seu backup para alinhamento
    btn_pt, btn_es, btn_it, btn_fr, btn_en, btn_xy = st.sidebar.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
    if btn_pt.button("pt"): st.session_state.lang = "pt"
    elif btn_es.button("es"): st.session_state.lang = "es"
    elif btn_it.button("it"): st.session_state.lang = "it"
    elif btn_fr.button("fr"): st.session_state.lang = "fr"
    elif btn_en.button("en"): st.session_state.lang = "en"
    elif btn_xy.button("⚒️"): st.session_state.lang = st.session_state.poly_lang

def draw_check_buttons():
    # Colunas de sensores do backup [3.8, 3.2, 3]
    draw_text, talk_text, vyde_text = st.sidebar.columns([3.8, 3.2, 3])
    help_tips = load_help(st.session_state.lang)
    
    st.session_state.draw = draw_text.checkbox(help_tips[5], st.session_state.draw, key="draw_machina")
    st.session_state.talk = talk_text.checkbox(help_tips[6], st.session_state.talk, key="talk_machina")
    st.session_state.vydo = vyde_text.checkbox(help_tips[7], st.session_state.vydo, key="vyde_machina")

# --- 5. EXECUÇÃO DO COCKPIT ---

with st.sidebar:
    st.markdown("""<nav>
        <a href='https://github.com/NandouLopes/yPoemas' target='_blank'>• github</a> | 
        <a href='https://youtu.be/uL6T3roTtAs' target='_blank'>youtube</a>
        </nav>""", unsafe_allow_html=True)
    pick_lang()
    st.divider()
    draw_check_buttons()

# ABAS EM MAIÚSCULAS
paginas = ["Mini", "yPoemas", "Eureka", "Biblioteca", "Livro Vivo", "Ensaios", "Sobre"]
tabs = st.tabs([p.upper() for p in paginas])

# O motor aguarda o conteúdo das páginas (gera_poema)
for nome, tab in zip(paginas, tabs):
    with tab:
        # Espaço reservado para a alma da Machina (Conteúdo)
        pass
