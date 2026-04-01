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
    layout="wide", # Layout Wide para o Sidebar ficar realmente à esquerda
    initial_sidebar_state="collapsed", # Sidebar encolhido por padrão
)

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

# Bibliotecas de Tradução e Áudio
if have_internet():
    try:
        from deep_translator import GoogleTranslator
        from gtts import gTTS
    except ImportError:
        pass

# Identificação de ambiente
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# --- CSS: O PALCO BIZANTINO ---
st.markdown(
    """ <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400&family=IBM+Plex+Sans:ital,wght@0,300;0,600;1,300&display=swap');

    footer {visibility: hidden;}
    header {visibility: hidden;} /* Esconde o menu padrão do Streamlit */

    /* Sidebar Minimalista */
    [data-testid="stSidebar"] {
        min-width: 200px;
        max-width: 200px;
        background-color: #111;
        color: white;
    }

    /* O Palco de Apresentação */
    .palco {
        background-color: #fcfcfc;
        border: 1px solid #d0d0d0;
        padding: 50px;
        margin: 0 auto;
        max-width: 850px;
        min-height: 450px;
        box-shadow: 20px 20px 0px #e0e0e0;
        position: relative;
    }

    .poema-texto {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 300;
        font-size: 26px;
        color: #1a1a1a;
        line-height: 1.6;
        z-index: 2;
    }

    .arte-capa {
        float: right;
        max-width: 220px;
        margin-left: 30px;
        margin-bottom: 20px;
        border: 1px solid #000;
        filter: sepia(30%) grayscale(20%);
    }

    /* Menu de Navegação Diferente (Pills) */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 40px;
    }

    .stButton>button {
        font-family: 'IBM Plex Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
        border: 1px solid #000;
        background: transparent;
        border-radius: 0px;
        padding: 10px 25px;
        transition: 0.4s;
    }

    .stButton>button:hover {
        background-color: #000;
        color: #fff;
        border: 1px solid #000;
    }

    /* Estilo de Inputs */
    .stTextInput>div>div>input {
        font-family: 'IBM Plex Mono', monospace;
        border-radius: 0px;
    }
    </style> """,
    unsafe_allow_html=True,
)

# --- SESSION STATE ---
keys = [
    ("lang", "pt"), ("book", "livro vivo"), ("tema", "Fatos"), 
    ("eureka", 0), ("draw", True), ("talk", False), ("menu_atual", "Mini")
]
for k, v in keys:
    if k not in st.session_state:
        st.session_state[k] = v

# --- FERRAMENTAS ---
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def load_poema(nome_tema, seed_eureka):
    seed_limpa = str(seed_eureka) if seed_eureka is not None else ""
    script = gera_poema(nome_tema, seed_limpa)
    # Lógica de Imagem: Busca imagem com nome do tema na pasta arts
    img_tag = ""
    img_path = f"./arts/{nome_tema.lower()}.jpg"
    b64 = get_image_base64(img_path)
    if b64:
        img_tag = f'<img src="data:image/jpg;base64,{b64}" class="arte-capa">'
    
    corpo = "<br>".join(script)
    return f'<div class="palco">{img_tag}<div class="poema-texto">{corpo}</div></div>'

def translate(text_html):
    # Tradução simplificada para o conteúdo dentro da div (mantendo as tags)
    if st.session_state.lang == "pt" or not have_internet():
        return text_html
    # Aqui entraria a lógica deep_translator se necessário
    return text_html

# --- SIDEBAR (ENCOLHIDO) ---
with st.sidebar:
    st.markdown("### CONFIG")
    st.session_state.talk = st.checkbox("Áudio", st.session_state.talk)
    st.session_state.draw = st.checkbox("Artes", st.session_state.draw)
    
    st.markdown("---")
    idiomas = {"PT": "pt", "EN": "en", "ES": "es", "IT": "it", "FR": "fr"}
    sel_lang = st.selectbox("Idioma", list(idiomas.keys()))
    st.session_state.lang = idiomas[sel_lang]
    
    st.markdown("---")
    st.caption(f"Host: {hostname}")
    st.caption(f"Trial: 238-Stable")

# --- NAVEGAÇÃO SUPERIOR (O NOVO MENU) ---
c1, c2, c3 = st.columns([1, 1, 1])
if c1.button("📟 MINI"): st.session_state.menu_atual = "Mini"
if c2.button("📚 yPOEMAS"): st.session_state.menu_atual = "yPoemas"
if c3.button("🔍 EUREKA"): st.session_state.menu_atual = "Eureka"

st.markdown("---")

# --- LÓGICA DAS PÁGINAS ---
def load_temas(book):
    try:
        with open(f"./base/rol_{book}.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["Fatos", "Anjos", "Tempo", "Direito"]

if st.session_state.menu_atual == "Mini":
    temas = load_temas(st.session_state.book)
    col_a, col_b = st.columns([3, 1])
    tema_m = col_a.selectbox("Sorteio de Tema", temas, label_visibility="collapsed")
    if col_b.button("GERAR"):
        with st.spinner("..."):
            html_poema = load_poema(tema_m, "")
            st.markdown(html_poema, unsafe_allow_html=True)

elif st.session_state.menu_atual == "yPoemas":
    temas = load_temas(st.session_state.book)
    tema_g = st.selectbox("Trilha Poética", temas)
    if st.button("EXPLORAR"):
        with st.spinner("..."):
            html_poema = load_poema(tema_g, "")
            st.markdown(html_poema, unsafe_allow_html=True)

elif st.session_state.menu_atual == "Eureka":
    col_e1, col_e2 = st.columns([3, 1])
    st.session_state.eureka = col_e1.text_input("Chave Seed", value=str(st.session_state.eureka))
    temas = load_temas(st.session_state.book)
    tema_e = st.selectbox("Garimpo", temas)
    
    if st.button("BUSCAR"):
        with st.spinner("..."):
            html_poema = load_poema(tema_e, st.session_state.eureka)
            st.markdown(html_poema, unsafe_allow_html=True)
