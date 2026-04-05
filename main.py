import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime

# Import da sua lógica de motor
try:
    from lay_2_ypo import gera_poema
except ImportError:
    st.error("Erro: arquivo 'lay_2_ypo.py' não encontrado.")

# 1. CONFIGURAÇÕES DE PÁGINA E INTERFACE (CSS)
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered"
)

# Funções de suporte (Internet e Tradução)
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

# Estilos CSS (Exatamente como os seus originais)
st.markdown("""
    <style>
    footer {visibility: hidden;}
    .logo-text {font-weight: 600; font-size: 18px; font-family: 'IBM Plex Sans'; color: #000000; padding-left: 15px;}
    .container {display: flex;}
    [data-testid='stSidebar'] > div:first-child {width: 310px;}
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DO SESSION STATE (ESTADOS DA MÁQUINA)
if "lang" not in st.session_state: st.session_state.lang = "pt"
if "last_lang" not in st.session_state: st.session_state.last_lang = "pt"
if "book" not in st.session_state: st.session_state.book = "livro vivo"
if "take" not in st.session_state: st.session_state.take = 0
if "mini" not in st.session_state: st.session_state.mini = 0
if "tema" not in st.session_state: st.session_state.tema = "Fatos"
if "visy" not in st.session_state: st.session_state.visy = True
if "draw" not in st.session_state: st.session_state.draw = False
if "talk" not in st.session_state: st.session_state.talk = False
if "vydo" not in st.session_state: st.session_state.vydo = False
if "arts" not in st.session_state: st.session_state.arts = []
if "auto" not in st.session_state: st.session_state.auto = False
if "nany_visy" not in st.session_state: st.session_state.nany_visy = 0

IPAddres = socket.gethostbyname(socket.gethostname())

# 3. DEFINIÇÃO DE FUNÇÕES (MECANISMOS)

def translate(input_text):
    if st.session_state.lang == "pt" or not have_internet():
        return input_text
    try:
        return GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
    except:
        return input_text

def pick_lang():
    cols = st.sidebar.columns([1, 1, 1, 1, 1, 1])
    langs = ["pt", "es", "it", "fr", "en", "⚒️"]
    for i, l in enumerate(langs):
        if cols[i].button(l):
            st.session_state.lang = l if l != "⚒️" else "ca" # Exemplo para poly_lang

def draw_check_buttons():
    st.sidebar.markdown("---")
    st.session_state.draw = st.sidebar.checkbox("Imagem", st.session_state.draw)
    st.session_state.talk = st.sidebar.checkbox("Áudio", st.session_state.talk)
    st.session_state.vydo = st.sidebar.checkbox("Vídeo", st.session_state.vydo)

@st.cache_data
def load_temas(book):
    try:
        with open(f"./base/rol_{book}.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["Fatos"]

def load_poema_local(nome_tema):
    script = gera_poema(nome_tema, "")
    novo_poema = "<br>".join(script)
    # Salva histórico local
    lypo_user = f"LYPO_{IPAddres}"
    if not os.path.exists("./temp"): os.makedirs("./temp")
    with open(f"./temp/{lypo_user}", "w", encoding="utf-8") as f:
        f.write(novo_poema)
    return novo_poema

def write_ypoema(texto, img_path=None):
    if img_path and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"<div class='container'><img src='data:image/jpg;base64,{data}' width='100'><p class='logo-text'>{texto}</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='container'><p class='logo-text'>{texto}</p></div>", unsafe_allow_html=True)

# 4. PÁGINAS DA INTERFACE

def page_ypoemas():
    temas = load_temas(st.session_state.book)
    st.session_state.tema = st.selectbox("Escolha o Tema", temas, index=st.session_state.take)
    
    if st.button("Gerar Poema"):
        poema = load_poema_local(st.session_state.tema)
        write_ypoema(poema)

# 5. MAESTRO (O BLOCO QUE RODA TUDO)

def main():
    # Primeiro as ferramentas de borda
    pick_lang()
    draw_check_buttons()
    
    # Navegação central
    menu = ["Poemas", "Mini", "Eureka"]
    escolha = st.sidebar.radio("Navegar", menu)
    
    if escolha == "Poemas":
        page_ypoemas()
    elif escolha == "Mini":
        st.write("Página Mini em construção...")
    elif escolha == "Eureka":
        st.write("Página Eureka em construção...")

if __name__ == "__main__":
    main()
