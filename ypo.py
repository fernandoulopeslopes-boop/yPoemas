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
    initial_sidebar_state="expanded",
)

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

# Carregamento de bibliotecas para tradução e áudio (Silent Fail)
if have_internet():
    try:
        from deep_translator import GoogleTranslator
        from gtts import gTTS
    except ImportError:
        pass

# Identificação de ambiente
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# --- CSS: O GUETO BIZANTINO (ESTÉTICA COMPLETA) ---
st.markdown(
    """ <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,600;1,300&display=swap');

    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar Permanente com Imagem de Identidade */
    [data-testid="stSidebar"] {
        background-color: #000;
        color: #fff;
        min-width: 250px !important;
    }
    
    .sidebar-header-img {
        width: 100%;
        border-bottom: 2px solid #333;
        margin-bottom: 20px;
    }

    /* O PALCO CENTRAL (O "CORAÇÃO" DA MACHINA) */
    .palco {
        background-color: #ffffff;
        border: 1px solid #111;
        padding: 50px 70px;
        margin: 0 auto;
        max-width: 950px;
        min-height: 600px;
        box-shadow: 35px 35px 0px #dcdcdc;
        position: relative;
        transition: 0.5s;
    }

    .poema-texto {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 300;
        font-size: 28px;
        color: #111;
        line-height: 1.6;
        white-space: pre-wrap;
    }

    .arte-tema-palco {
        float: right;
        max-width: 300px;
        margin-left: 40px;
        margin-bottom: 25px;
        border: 1px solid #000;
        filter: grayscale(100%) contrast(105%) sepia(10%);
    }

    /* NAVEGAÇÃO POR SÍMBOLOS (+ < * > ⚒️) */
    .nav-bar {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 30px;
    }

    .stButton>button {
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        font-size: 24px;
        border: 2px solid #000;
        background-color: #fff;
        color: #000;
        border-radius: 0px;
        padding: 10px 30px;
        transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stButton>button:hover {
        background-color: #000;
        color: #fff;
        transform: translate(-4px, -4px);
        box-shadow: 4px 4px 0px #555;
    }

    /* Customização de Selectbox e Inputs */
    .stSelectbox label, .stTextInput label { font-family: 'IBM Plex Mono', monospace; color: #555; }
    input { border-radius: 0px !important; border: 1px solid #000 !important; }
    </style> """,
    unsafe_allow_html=True,
)

# --- SESSION STATE (PERSISTÊNCIA DE CEM ORIENTAÇÕES) ---
keys = [
    ("lang", "pt"), ("book", "livro vivo"), ("tema", "Fatos"), 
    ("eureka", 0), ("poema_html", ""), ("menu_nav", "Mini"),
    ("draw", True), ("talk", False), ("history", [])
]
for k, v in keys:
    if k not in st.session_state:
        st.session_state[k] = v

# --- CORE FUNCTIONS ---
def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def processar_e_renderizar(tema, seed=""):
    # Chamada ao motor de poesia (lay_2_ypo)
    script = gera_poema(tema, str(seed))
    corpo = "<br>".join(script)
    
    # Busca Arte do Tema para o Palco
    img_tag = ""
    if st.session_state.draw:
        img_b64 = get_base64_img(f"./arts/{tema.lower()}.jpg")
        if img_b64:
            img_tag = f'<img src="data:image/jpg;base64,{img_b64}" class="arte-tema-palco">'
    
    st.session_state.poema_html = f'<div class="palco">{img_tag}<div class="poema-texto">{corpo}</div></div>'

def load_temas(book):
    try:
        with open(f"./base/rol_{book}.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["Fatos", "Anjos", "Tempo", "Manifesto", "Submundo"]

# --- SIDEBAR: O PAINEL DE CONTROLE FIXO ---
with st.sidebar:
    # Mostra a imagem de cabeçalho baseada no modo (Mini, yPoemas, Eureka)
    header_img_b64 = get_base64_img(f"./assets/head_{st.session_state.menu_nav.lower()}.jpg")
    if header_img_b64:
        st.markdown(f'<img src="data:image/jpg;base64,{header_img_b64}" class="sidebar-header-img">', unsafe_allow_html=True)
    
    st.markdown("### 🎛️ COMANDOS")
    st.session_state.book = st.selectbox("LIVRO DE BASE", ["livro vivo", "arquivo morto"])
    
    st.markdown("---")
    st.session_state.draw = st.checkbox("MOSTRAR ARTES", st.session_state.draw)
    st.session_state.talk = st.checkbox("SINTETIZAR VOZ", st.session_state.talk)
    
    st.markdown("---")
    langs = {"Português": "pt", "English": "en", "Español": "es", "Italiano": "it"}
    sel_lang = st.selectbox("IDIOMA", list(langs.keys()))
    st.session_state.lang = langs[sel_lang]
    
    st.markdown("---")
    st.caption(f"📍 HOST: {hostname}")
    st.caption(f"📍 IP: {IPAddres}")
    st.caption(f"TRIAL: 238-Stable")

# --- NAVEGAÇÃO DE FLUXO SUPERIOR (+ < * > ⚒️) ---
cols = st.columns([1, 1, 1, 1, 1, 5]) # Deixamos espaço à direita
if cols[0].button("+"): st.session_state.menu_nav = "Mini"
if cols[1].button("<"): st.session_state.menu_nav = "yPoemas"
if cols[2].button("*"): 
    t_rand = random.choice(load_temas(st.session_state.book))
    processar_e_renderizar(t_rand)
if cols[3].button(">"): st.session_state.menu_nav = "Eureka"
if cols[4].button("⚒️"): st.session_state.menu_nav = "Config"

st.markdown("---")

# --- INTERFACES DE CADA MÓDULO ---
temas_disp = load_temas(st.session_state.book)

if st.session_state.menu_nav == "Mini":
    st.subheader("📟 MINI MACHINA")
    c_m1, c_m2 = st.columns([4, 1])
    tema_m = c_m1.selectbox("Selecione o Gatilho:", temas_disp, label_visibility="collapsed")
    if c_m2.button("ACIONAR +"):
        processar_e_renderizar(tema_m)

elif st.session_state.menu_nav == "yPoemas":
    st.subheader("📚 GALERIA YPOEMAS")
    tema_g = st.selectbox("Selecione a trilha bizantina:", temas_disp)
    if st.button("EXPLORAR <"):
        processar_e_renderizar(tema_g)

elif st.session_state.menu_nav == "Eureka":
    st.subheader("🔍 MÓDULO EUREKA")
    col_e1, col_e2 = st.columns([4, 1])
    st.session_state.eureka = col_e1.text_input("Semente de Busca (Seed):", value=str(st.session_state.eureka))
    tema_e = st.selectbox("Garimpar em:", temas_disp)
    if st.button("GERAR >"):
        processar_e_renderizar(tema_e, st.session_state.eureka)

elif st.session_state.menu_nav == "Config":
    st.subheader("⚒️ CONFIGURAÇÕES DE SISTEMA")
    st.info("Ajustes finos de rede e ambiente de deploy.")
    st.write(f"Diretório Base: `{os.getcwd()}`")

# --- RENDERIZAÇÃO DO PALCO ---
if st.session_state.poema_html:
    st.markdown(st.session_state.poema_html, unsafe_allow_html=True)
