import os
import re
import time
import random
import base64
import socket
import streamlit as st

# AJUSTE NA IMPORTAÇÃO PARA EVITAR ATTRIBUTE ERROR
import extra_streamlit_components as stx
from datetime import datetime
from lay_2_ypo import gera_poema

### 0. PROTOCOLO DE LAYOUT (Estabilização de Interface)
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { min-width: 310px; max-width: 310px; }
    .main .block-container { max-width: 850px; padding: 2rem 1rem; margin: auto; }
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    mark { background-color: powderblue; color: black; }
    .container { display: flex; flex-direction: column; }
    .logo-text { font-weight: 600; font-size: 19px; font-family: 'IBM Plex Sans', sans-serif; color: #1E1E1E; line-height: 1.5; }
    .logo-img { float: right; margin-bottom: 15px; border-radius: 4px; }
    </style>
    """,
    unsafe_allow_html=True,
)

### 1. NÚCLEO E SESSION STATE
if "lang" not in st.session_state: st.session_state.lang = "pt"
if "book" not in st.session_state: st.session_state.book = "livro vivo"
if "take" not in st.session_state: st.session_state.take = 0
if "draw" not in st.session_state: st.session_state.draw = True

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except: return False

def write_ypoema(text, img=None):
    if img and os.path.exists(img):
        with open(img, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"<div class='container'><img class='logo-img' src='data:image/jpg;base64,{data}'><p class='logo-text'>{text}</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='container'><p class='logo-text'>{text}</p></div>", unsafe_allow_html=True)

### 2. NAVEGAÇÃO DE PÁGINAS (Correção do TabBar)
# O padrão estável é usar stx.tab_bar com uma lista de dicionários ou a classe correta
chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="yPoemas", title="yPoemas", description=""),
    stx.TabBarItemData(id="Mini", title="Mini", description=""),
    stx.TabBarItemData(id="Eureka", title="Eureka", description=""),
    stx.TabBarItemData(id="About", title="About", description=""),
], default="yPoemas")

### 3. PÁGINA PRINCIPAL
def page_ypoemas():
    # Sidebar
    with st.sidebar:
        st.title("Machina")
        st.session_state.book = st.selectbox("Acervo", ["livro vivo", "linguafiada", "faz de conto", "todos os temas"])
        st.session_state.draw = st.checkbox("Imagem", st.session_state.draw)
        st.write("---")
        # Seleção de Idioma simples
        lang_choice = st.radio("Idioma", ["pt", "es", "it", "fr", "en"], horizontal=True)
        st.session_state.lang = lang_choice

    # Carregamento de Temas
    filename = f"./base/rol_{st.session_state.book.replace(' ', '_')}.txt"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            temas = [line.strip() for line in f if line.strip()]
    except:
        temas = ["Fatos"]
    
    maxy = len(temas) - 1
    st.session_state.take %= (maxy + 1)

    # OS 5 BOTÕES DO PALCO
    f1, b_more, b_back, b_rand, b_next, b_help, f2 = st.columns([2, 1, 1, 1, 1, 1, 2])
    
    if b_back.button("◀"): 
        st.session_state.take = (st.session_state.take - 1) % (maxy + 1)
        st.rerun()
    if b_rand.button("✻"): 
        st.session_state.take = random.randint(0, maxy)
        st.rerun()
    if b_next.button("▶"): 
        st.session_state.take = (st.session_state.take + 1) % (maxy + 1)
        st.rerun()
    
    show_more = b_more.button("✚")
    show_help = b_help.button("?")

    st.session_state.tema = temas[st.session_state.take]

    # Renderização
    with st.expander(f"⚫ {st.session_state.tema.upper()} ({st.session_state.take + 1}/{maxy + 1})", expanded=True):
        script = gera_poema(st.session_state.tema, "")
        poema_txt = "<br>".join(script)
        
        img_path = f"./images/matrix/{st.session_state.tema.capitalize()}.jpg"
        write_ypoema(poema_txt, img_path if st.session_state.draw else None)

    if show_help:
        st.info(f"Análise técnica do tema: {st.session_state.tema}")
    if show_more:
        st.success("Mais variações disponíveis no banco de dados.")

if chosen_id == "yPoemas":
    page_ypoemas()
else:
    st.info(f"Página {chosen_id} em desenvolvimento.")
