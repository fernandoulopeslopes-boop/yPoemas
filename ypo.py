import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime
from lay_2_ypo import gera_poema

# Tenta importar ferramentas de tradução e voz
try:
    from deep_translator import GoogleTranslator
    from gtts import gTTS
    HAS_TOOLS = True
except ImportError:
    HAS_TOOLS = False

### bof: settings
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="wide", # Layout wide para o palco avançado
    initial_sidebar_state="expanded",
)

# --- ESTÉTICA AVANÇADA (CSS BIZANTINO) ---
st.markdown(
    """ <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,600;1,300&display=swap');
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* SIDEBAR: Painel de Controle Preto */
    [data-testid="stSidebar"] {
        background-color: #000;
        color: #fff;
        min-width: 280px !important;
    }
    .sidebar-header-img { width: 100%; border-bottom: 3px solid #333; margin-bottom: 20px; filter: grayscale(100%); }

    /* O PALCO: Sombra profunda e tipografia de 30px */
    .palco {
        background-color: #ffffff;
        border: 1px solid #000;
        padding: 60px 80px;
        margin: 20px auto;
        max-width: 1000px;
        min-height: 600px;
        box-shadow: 40px 40px 0px #d0d0d0;
        position: relative;
    }
    .poema-texto {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 300;
        font-size: 30px;
        color: #111;
        line-height: 1.5;
        white-space: pre-wrap;
    }
    .arte-tema-palco {
        float: right;
        max-width: 350px;
        margin-left: 40px;
        margin-bottom: 30px;
        border: 1px solid #000;
        filter: grayscale(100%) contrast(110%);
    }

    /* BOTÕES DE NAVEGAÇÃO (+ < * > ⚒️) */
    .stButton>button {
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        font-size: 26px;
        border: 2px solid #000;
        background-color: #fff;
        color: #000;
        border-radius: 0px;
        width: 100%;
        height: 60px;
        transition: 0.2s;
    }
    .stButton>button:hover { background-color: #000; color: #fff; box-shadow: 5px 5px 0px #888; }
    </style> """,
    unsafe_allow_html=True,
)

# --- LÓGICA DE ESTADO (SESSION STATE) ---
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

if "visy" not in st.session_state:
    st.session_state.update({
        "visy": True, "lang": "pt", "menu_nav": "Mini",
        "tema": "Fatos", "book": "livro vivo", "poema_html": "",
        "draw": True, "talk": False, "eureka_seed": ""
    })

# --- CORE FUNCTIONS ---
def get_img_as_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def traduzir_poema(texto, destino):
    if destino == "pt" or not HAS_TOOLS: return texto
    try:
        return GoogleTranslator(source='pt', target=destino).translate(texto)
    except: return texto

def processar_machina(tema, seed=""):
    # Geração
    corpo_lista = gera_poema(tema, str(seed))
    texto_original = "\n".join(corpo_lista)
    
    # Tradução
    texto_final = traduzir_poema(texto_original, st.session_state.lang)
    texto_html = texto_final.replace("\n", "<br>")
    
    # Arte
    img_tag = ""
    if st.session_state.draw:
        img_b64 = get_img_as_base64(f"./arts/{tema.lower()}.jpg")
        if img_b64:
            img_tag = f'<img src="data:image/jpg;base64,{img_b64}" class="arte-tema-palco">'
    
    st.session_state.poema_html = f'<div class="palco">{img_tag}<div class="poema-texto">{texto_html}</div></div>'
    
    # Audio
    if st.session_state.talk and HAS_TOOLS:
        tts = gTTS(text=texto_final, lang=st.session_state.lang)
        tts.save("temp_audio.mp3")
        st.audio("temp_audio.mp3")

def load_temas(book):
    try:
        with open(f"./base/rol_{book.replace(' ', '_')}.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except: return ["Fatos", "Anjos", "Tempo", "Manifesto"]

# --- SIDEBAR DINÂMICO ---
with st.sidebar:
    # Cabeçalho baseado no modo
    h_b64 = get_img_as_base64(f"./assets/head_{st.session_state.menu_nav.lower()}.jpg")
    if h_b64:
        st.markdown(f'<img src="data:image/jpg;base64,{h_b64}" class="sidebar-header-img">', unsafe_allow_html=True)
    
    st.session_state.book = st.selectbox("LIVRO", ["livro vivo", "arquivo morto"])
    st.session_state.draw = st.toggle("Artes", st.session_state.draw)
    st.session_state.talk = st.toggle("Voz", st.session_state.talk)
    
    st.markdown("---")
    langs = {"Português": "pt", "English": "en", "Español": "es", "Italiano": "it", "Français": "fr"}
    st.session_state.lang = langs[st.selectbox("IDIOMA", list(langs.keys()))]
    
    st.caption(f"IP: {IPAddres} | HOST: {hostname}")

# --- NAVEGAÇÃO (+ < * > ⚒️) ---
cols = st.columns([1, 1, 1, 1, 1, 4])
if cols[0].button("+"): st.session_state.menu_nav = "Mini"
if cols[1].button("<"): st.session_state.menu_nav = "yPoemas"
if cols[2].button("*"): 
    t_rand = random.choice(load_temas(st.session_state.book))
    processar_machina(t_rand)
if cols[3].button(">"): st.session_state.menu_nav = "Eureka"
if cols[4].button("⚒️"): st.session_state.menu_nav = "Config"

st.markdown("---")

# --- INTERFACES ---
temas_list = load_temas(st.session_state.book)

if st.session_state.menu_nav == "Mini":
    cm1, cm2 = st.columns([4, 1])
    tema_m = cm1.selectbox("Gatilho:", temas_list, label_visibility="collapsed")
    if cm2.button("OK"): processar_machina(tema_m)

elif st.session_state.menu_nav == "yPoemas":
    tema_g = st.selectbox("Galeria:", temas_list)
    if st.button("ABRIR"): processar_machina(tema_g)

elif st.session_state.menu_nav == "Eureka":
    ce1, ce2 = st.columns([4, 1])
    st.session_state.eureka_seed = ce1.text_input("Seed:", value=st.session_state.eureka_seed)
    tema_e = st.selectbox("Base:", temas_list)
    if st.button("BUSCAR"): processar_machina(tema_e, st.session_state.eureka_seed)

# --- RENDERIZAÇÃO FINAL ---
if st.session_state.poema_html:
    st.markdown(st.session_state.poema_html, unsafe_allow_html=True)
