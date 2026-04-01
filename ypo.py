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
    initial_sidebar_state="collapsed",
)

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

# Carregamento de bibliotecas para tradução e áudio
if have_internet():
    try:
        from deep_translator import GoogleTranslator
        from gtts import gTTS
    except ImportError:
        pass

# Identificação de ambiente
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# --- CSS: ESTÉTICA BIZANTINA / GUETO UNDERGROUND ---
st.markdown(
    """ <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar minimalista à esquerda */
    [data-testid="stSidebar"] {
        min-width: 180px;
        max-width: 180px;
        background-color: #0e0e0e;
    }

    /* O PALCO: Onde a poesia se manifesta */
    .palco {
        background-color: #ffffff;
        border: 1px solid #1a1a1a;
        padding: 60px;
        margin: 0 auto;
        max-width: 800px;
        min-height: 500px;
        box-shadow: 25px 25px 0px #d1d1d1;
        position: relative;
    }

    .poema-texto {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 300;
        font-size: 28px;
        color: #000000;
        line-height: 1.5;
        text-align: left;
    }

    .arte-tema {
        float: right;
        max-width: 250px;
        border: 1px solid #333;
        margin-left: 30px;
        margin-bottom: 20px;
        filter: grayscale(100%) contrast(110%);
    }

    /* NAVEGAÇÃO POR SÍMBOLOS (+ < * >) */
    .nav-symbols {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 30px;
        margin-bottom: 30px;
    }

    .stButton>button {
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        font-size: 20px;
        border: 1px solid #000;
        background-color: #fff;
        color: #000;
        border-radius: 0px;
        padding: 5px 20px;
        transition: 0.2s ease-in-out;
    }

    .stButton>button:hover {
        background-color: #000;
        color: #fff;
    }

    /* Ajuste para inputs */
    input { font-family: 'IBM Plex Mono', monospace !important; }
    </style> """,
    unsafe_allow_html=True,
)

# --- SESSION STATE ---
keys = [
    ("lang", "pt"), ("book", "livro vivo"), ("tema", "Fatos"), 
    ("eureka", 0), ("poema_html", ""), ("menu_naveg", "Mini")
]
for k, v in keys:
    if k not in st.session_state:
        st.session_state[k] = v

# --- FUNÇÕES CORE ---
def get_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def processar_poema(tema, seed=""):
    script = gera_poema(tema, str(seed))
    corpo = "<br>".join(script)
    
    # Busca arte correspondente
    img_tag = ""
    img_b64 = get_b64(f"./arts/{tema.lower()}.jpg")
    if img_b64:
        img_tag = f'<img src="data:image/jpg;base64,{img_b64}" class="arte-tema">'
    
    st.session_state.poema_html = f'<div class="palco">{img_tag}<div class="poema-texto">{corpo}</div></div>'

def load_temas(book):
    try:
        with open(f"./base/rol_{book}.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["Fatos", "Anjos", "Tempo", "Manifesto", "Submundo"]

# --- SIDEBAR (CONFIGURAÇÕES) ---
with st.sidebar:
    st.markdown("<h2 style='color:white; font-family:monospace;'>MACHINA</h2>", unsafe_allow_html=True)
    st.session_state.book = st.selectbox("LIVRO", ["livro vivo", "arquivo morto"], label_visibility="collapsed")
    st.markdown("---")
    st.caption(f"Host: {hostname}")
    st.caption("v.238-Stable")

# --- MENU DE NAVEGAÇÃO SUPERIOR (SÍMBOLOS) ---
st.markdown("<div class='nav-symbols'>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1])

# Símbolos de Comando
if c1.button("+"): # Novo/Mini
    st.session_state.menu_naveg = "Mini"
if c2.button("<"): # Voltar/Galeria
    st.session_state.menu_naveg = "yPoemas"
if c3.button("*"): # Aleatório
    temas = load_temas(st.session_state.book)
    tema_rand = random.choice(temas)
    processar_poema(tema_rand)
if c4.button(">"): # Próximo/Avançar
    st.session_state.menu_naveg = "Eureka"
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# --- INTERFACE DAS PÁGINAS ---
if st.session_state.menu_naveg == "Mini":
    temas = load_temas(st.session_state.book)
    sel_tema = st.selectbox("Selecione o Tema para Acionamento (+):", temas)
    if st.button("GERAR POESIA"):
        processar_poema(sel_tema)

elif st.session_state.menu_naveg == "yPoemas":
    temas = load_temas(st.session_state.book)
    sel_galeria = st.selectbox("Navegar na Galeria (<):", temas)
    if st.button("ABRIR ARQUIVO"):
        processar_poema(sel_galeria)

elif st.session_state.menu_naveg == "Eureka":
    col_in, col_fix = st.columns([3, 1])
    seed_input = col_in.text_input("Chave Seed (>):", value=str(st.session_state.eureka))
    if col_fix.button("FIXAR"):
        st.session_state.eureka = seed_input
    
    temas = load_temas(st.session_state.book)
    tema_eureka = st.selectbox("Garimpar em:", temas)
    if st.button("EXECUTAR EUREKA"):
        processar_poema(tema_eureka, st.session_state.eureka)

# EXIBIÇÃO DO PALCO
if st.session_state.poema_html:
    st.markdown(st.session_state.poema_html, unsafe_allow_html=True)
