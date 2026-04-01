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
    initial_sidebar_state="expanded", # Sidebar sempre visível conforme orientado
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

hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# --- CSS: O PALCO E A SIDEBAR (VERSÃO REFINADA) ---
st.markdown(
    """ <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,600;1,300&display=swap');

    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar com Visual de Painel */
    [data-testid="stSidebar"] {
        background-color: #000000;
        color: #ffffff;
        padding-top: 0px;
    }
    
    .sidebar-img {
        width: 100%;
        margin-bottom: 20px;
        border-bottom: 1px solid #333;
    }

    /* O PALCO CENTRAL */
    .palco {
        background-color: #ffffff;
        border: 1px solid #1a1a1a;
        padding: 50px;
        margin: 0 auto;
        max-width: 900px;
        min-height: 550px;
        box-shadow: 30px 30px 0px #cfcfcf;
        position: relative;
    }

    .poema-texto {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 300;
        font-size: 28px;
        color: #000;
        line-height: 1.55;
        z-index: 5;
    }

    .arte-palco {
        float: right;
        max-width: 280px;
        margin-left: 35px;
        margin-bottom: 20px;
        border: 1px solid #000;
        filter: grayscale(100%) contrast(105%);
    }

    /* BOTÕES DE COMANDO (+ < * > ⚒️) */
    .stButton>button {
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        font-size: 22px;
        border: 1px solid #000;
        border-radius: 0px;
        width: 100%;
        height: 60px;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #000;
        color: #fff;
    }

    /* Estilo para Inputs */
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
    ("eureka", 0), ("poema_html", ""), ("menu_nav", "Mini"),
    ("draw", True), ("talk", False)
]
for k, v in keys:
    if k not in st.session_state:
        st.session_state[k] = v

# --- CORE FUNCTIONS ---
def get_img_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def render_poema(tema, seed=""):
    script = gera_poema(tema, str(seed))
    corpo = "<br>".join(script)
    
    # Busca arte do tema para o Palco
    img_tag = ""
    img_b64 = get_img_b64(f"./arts/{tema.lower()}.jpg")
    if img_b64:
        img_tag = f'<img src="data:image/jpg;base64,{img_b64}" class="arte-palco">'
    
    st.session_state.poema_html = f'<div class="palco">{img_tag}<div class="poema-texto">{corpo}</div></div>'

def load_temas(book):
    try:
        with open(f"./base/rol_{book}.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["Fatos", "Anjos", "Tempo", "Manifesto"]

# --- SIDEBAR: O PAINEL DE CONTROLE ---
with st.sidebar:
    # Mostra imagem do modo atual (ex: mini.jpg, galeria.jpg)
    modo_img = get_img_b64(f"./assets/{st.session_state.menu_nav.lower()}.jpg")
    if modo_img:
        st.markdown(f'<img src="data:image/jpg;base64,{modo_img}" class="sidebar-img">', unsafe_allow_html=True)
    
    st.markdown("### 🎛️ PARÂMETROS")
    st.session_state.book = st.selectbox("LIVRO", ["livro vivo", "arquivo morto"])
    st.session_state.draw = st.toggle("Artes no Palco", st.session_state.draw)
    st.session_state.talk = st.toggle("Sintetizar Voz", st.session_state.talk)
    
    st.markdown("---")
    st.session_state.lang = st.selectbox("TRADUÇÃO", ["pt", "en", "es", "it", "fr"])
    
    st.markdown("---")
    st.caption(f"📍 {hostname}")
    st.caption(f"Status: Trial 238-Stable")

# --- NAVEGAÇÃO DE FLUXO (+ < * > ⚒️) ---
cols_nav = st.columns(5)
if cols_nav[0].button("+", help="Mini Machina"): st.session_state.menu_nav = "Mini"
if cols_nav[1].button("<", help="Galeria"): st.session_state.menu_nav = "yPoemas"
if cols_nav[2].button("*", help="Aleatório"):
    tema_sorteio = random.choice(load_temas(st.session_state.book))
    render_poema(tema_sorteio)
if cols_nav[3].button(">", help="Eureka"): st.session_state.menu_nav = "Eureka"
if cols_nav[4].button("⚒️", help="Config"): st.session_state.menu_nav = "Config"

st.markdown("---")

# --- INTERFACES ESPECÍFICAS ---
temas_disp = load_temas(st.session_state.book)

if st.session_state.menu_nav == "Mini":
    st.subheader("📟 Modo Mini")
    col_m1, col_m2 = st.columns([3, 1])
    tema_m = col_m1.selectbox("Selecione:", temas_disp, label_visibility="collapsed")
    if col_m2.button("EXECUTAR +"):
        render_poema(tema_m)

elif st.session_state.menu_nav == "yPoemas":
    st.subheader("📚 Galeria yPoemas")
    tema_g = st.selectbox("Escolha a trilha para explorar:", temas_disp)
    if st.button("ABRIR <"):
        render_poema(tema_g)

elif st.session_state.menu_nav == "Eureka":
    st.subheader("🔍 Módulo Eureka")
    col_e1, col_e2 = st.columns([3, 1])
    st.session_state.eureka = col_e1.text_input("Chave Seed:", value=str(st.session_state.eureka))
    tema_e = st.selectbox("Garimpar semente em:", temas_disp)
    if st.button("GERAR >"):
        render_poema(tema_e, st.session_state.eureka)

elif st.session_state.menu_nav == "Config":
    st.subheader("⚒️ Ajustes de Sistema")
    st.write("Configurações avançadas do motor lypo.")
    # Aqui entrariam os campos de IP, Hostname, etc.

# --- EXIBIÇÃO DO PALCO (Onde o texto aparece) ---
if st.session_state.poema_html:
    st.markdown(st.session_state.poema_html, unsafe_allow_html=True)
