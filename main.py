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

# --- 2. CONTEÚDO: DNA ESTÉTICO & COMPRESSÃO ---
st.markdown("""
    <style>
    footer {visibility: hidden;}
    [data-testid='stSidebar'] { overflow-x: hidden; }
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child { width: 310px; }
    
    /* Botões de Idioma */
    div.stButton > button {
        padding: 2px 2px !important;
        font-size: 14px !important;
        width: 100% !important;
        white-space: nowrap !important;
    }
    
    /* Alinhamento das Colunas */
    [data-testid="column"] { padding: 0 2px !important; min-width: 0px !important; }
    
    .reportview-container .main .block-container {
        padding-top: 0rem; padding-right: 0rem; padding-left: 0rem; padding-bottom: 0rem;
    }
    
    .ypo_box {
        font-family: 'Courier New', Courier, monospace;
        background-color: #FAFAFA;
        padding: 25px;
        border: 1px solid #EEE;
        line-height: 1.5;
        font-size: 16px;
        color: #333;
    }

    /* Links Sociais no Topo da Sidebar */
    .nav-links {
        font-family: 'Courier New', Courier, monospace;
        font-size: 14px;
        padding-bottom: 10px;
        text-align: center;
    }
    .nav-links a { color: #555; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONTEÚDO: INITIALIZE SESSIONSTATE ---
states = {
    "lang": "pt", "last_lang": "pt", "book": "livro vivo", "take": 0,
    "mini": 0, "tema": "Mini", "visy": True, "draw": True, "talk": False, 
    "vydo": False, "poly_lang": "ca", "poly_name": "català", "current_ypoema": ""
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
                if pipe[1].strip() == f"{idiom}_help":
                    returns.append(pipe[2].strip())
        return returns if len(returns) > 7 else ["ajuda"] * 10
    except:
        return ["ajuda"] * 10

def get_ypoema(tema):
    f_path = f"./base/rol_{tema.lower().replace(' ', '_')}.txt"
    if os.path.exists(f_path):
        with open(f_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        if not lines: return "ARQUIVO VAZIO."
        content = "\n".join(random.sample(lines, min(len(lines), 6)))
        if st.session_state.lang != "pt" and have_internet():
            try:
                return GoogleTranslator(source='pt', target=st.session_state.lang).translate(content)
            except: return content
        return content
    return f"ERRO: {f_path} NÃO ENCONTRADO."

def pick_lang():
    cols = st.sidebar.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
    langs = ["pt", "es", "it", "fr", "en"]
    for i, l in enumerate(langs):
        if cols[i].button(l): st.session_state.lang = l
    if cols[5].button("⚒️"): st.session_state.lang = st.session_state.poly_lang

def draw_check_buttons():
    draw_text, talk_text, vyde_text = st.sidebar.columns([3.8, 3.2, 3])
    help_tips = load_help(st.session_state.lang)
    st.session_state.draw = draw_text.checkbox(help_tips[5], st.session_state.draw, key="draw_machina")
    st.session_state.talk = talk_text.checkbox(help_tips[6], st.session_state.talk, key="talk_machina")
    st.session_state.vydo = vyde_text.checkbox(help_tips[7], st.session_state.vydo, key="vyde_machina")

# --- 5. EXECUÇÃO DO COCKPIT (SIDEBAR) ---

# Links no topo absoluto da sidebar
st.sidebar.markdown('<div class="nav-links"><a href="https://github.com/NandouLopes/yPoemas">github</a> | <a href="https://youtu.be/uL6T3roTtAs">youtube</a></div>', unsafe_allow_html=True)

# Arte da Sidebar (Logo)
if os.path.exists("./images/logo.jpg"):
    st.sidebar.image("./images/logo.jpg", use_container_width=True)

with st.sidebar:
    pick_lang()
    st.divider()
    draw_check_buttons()

# --- 6. EXIBIÇÃO DAS PÁGINAS ---
paginas = ["Mini", "yPoemas", "Eureka", "Biblioteca", "Livro Vivo", "Ensaios", "Sobre"]
tabs = st.tabs([p.upper() for p in paginas])

for i, (nome, tab) in enumerate(zip(paginas, tabs)):
    with tab:
        col_txt, col_img = st.columns([2, 1])
        
        # Botão para disparar a geração (sempre visível na aba)
        if col_txt.button(f"GERAR {nome.upper()}", key=f"btn_{nome}_{i}"):
            st.session_state.tema = nome
            st.session_state.current_ypoema = get_ypoema(nome)
            st.rerun()
        
        # Conteúdo persistente se o tema atual for esta aba
        if st.session_state.tema == nome:
            if st.session_state.current_ypoema:
                col_txt.markdown(f'<div class="ypo_box">{st.session_state.current_ypoema.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
                
                if st.session_state.talk and have_internet():
                    tts = gTTS(text=st.session_state.current_ypoema, lang=st.session_state.lang)
                    if not os.path.exists("temp"): os.makedirs("temp")
                    tts.save(f"temp/voice.mp3")
                    st.audio(f"temp/voice.mp3")

                if st.session_state.draw:
                    # Tenta carregar a arte específica do tema
                    img_path = f"./images/{nome.lower().replace(' ', '_')}.jpg"
                    if os.path.exists(img_path):
                        col_img.image(img_path, use_container_width=True)
            else:
                col_txt.info("Clique no botão acima para iniciar a Machina.")
