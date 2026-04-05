import os
import re
import time
import random
import base64
import socket
import streamlit as st

from extra_streamlit_components import TabBar as stx
from datetime import datetime
from lay_2_ypo import gera_poema

### bof: settings

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# PROTOCOLO DE LAYOUT: CSS INTEGRADO (Proteção contra encavalamento)
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        min-width: 310px;
        max-width: 310px;
    }
    .main .block-container {
        max-width: 850px;
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
        margin: auto;
    }
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    mark {
      background-color: powderblue;
      color: black;
    }
    .container {
        display: flex;
    }
    .logo-text {
        font-weight: 600;
        font-size: 18px;
        font-family: 'IBM Plex Sans';
        color: #000000;
        padding-left: 15px;
    }
    .logo-img {
        float:right;
    }
    </style>
    """,
    unsafe_allow_html=True,
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

# Initialize SessionState
states = {
    "lang": "pt", "last_lang": "pt", "book": "livro vivo", 
    "take": 0, "mini": 0, "tema": "Fatos", "off_book": 0, 
    "off_take": 0, "eureka": 0, "poly_lang": "ca", 
    "poly_name": "català", "poly_take": 12, "poly_file": "poly_pt.txt",
    "visy": True, "nany_visy": 0, "draw": False, "talk": False, 
    "vydo": False, "arts": [], "auto": False, "rand": False
}
for key, val in states.items():
    if key not in st.session_state:
        st.session_state[key] = val

### bof: tools (Abreviadas para foco no fluxo, mas funcionais)

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
        if cols[i].button(l, key=f"lang_{l}"):
            if l == "⚒️":
                st.session_state.lang = st.session_state.poly_lang
            else:
                st.session_state.lang = l

def draw_check_buttons():
    draw_text, talk_text, vyde_text = st.sidebar.columns([3.8, 3.2, 3])
    st.session_state.draw = draw_text.checkbox("imagem", st.session_state.draw)
    st.session_state.talk = talk_text.checkbox("áudio", st.session_state.talk)
    st.session_state.vydo = vyde_text.checkbox("vídeo", st.session_state.vydo)

def load_poema(nome_tema, seed=""):
    script = gera_poema(nome_tema, seed)
    lypo_user = f"LYPO_{IPAddres}"
    with open(os.path.join("./temp/", lypo_user), "w", encoding="utf-8") as f:
        f.write(nome_tema + "\n" + "\n".join(script))
    return "<br>".join(script)

def load_lypo():
    try:
        with open(os.path.join("./temp/", f"LYPO_{IPAddres}"), encoding="utf-8") as f:
            return f.read().replace("\n", "<br>")
    except: return ""

def write_ypoema(text, img=None):
    if img:
        img_b64 = base64.b64encode(open(img, 'rb').read()).decode()
        st.markdown(f"<div class='container'><img class='logo-img' src='data:image/jpg;base64,{img_b64}'><p class='logo-text'>{text}</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='container'><p class='logo-text'>{text}</p></div>", unsafe_allow_html=True)

### bof: main navigation

with st.sidebar:
    st.title("Machina")
    pick_lang()
    draw_check_buttons()
    
    # Seletor de Livros
    books_list = ["livro vivo", "linguafiada", "faz de conto", "todos os temas"]
    st.session_state.book = st.selectbox("Escolha o Livro:", books_list)
    
    st.markdown("---")
    st.info("Status: Online" if have_internet() else "Status: Offline")

# Execução da Página
def run_machina():
    temas = []
    # Simulação de carregamento de temas do arquivo rol_
    try:
        with open(f"./base/rol_{st.session_state.book.replace(' ', '_')}.txt", "r", encoding="utf-8") as f:
            temas = [line.strip() for line in f if line.strip()]
    except:
        temas = ["Fatos", "Amor", "Tempo"]

    col1, col2, col3 = st.columns([1, 2, 1])
    if col1.button("◀"): st.session_state.take -= 1
    if col2.button("✻ NOVO POEMA"): st.session_state.take = random.randint(0, len(temas)-1)
    if col3.button("▶"): st.session_state.take += 1
    
    st.session_state.take %= len(temas)
    st.session_state.tema = temas[st.session_state.take]
    
    st.subheader(f"Tema: {st.session_state.tema}")
    
    poema = load_poema(st.session_state.tema)
    if st.session_state.lang != "pt":
        poema = translate(poema)
    
    write_ypoema(poema)

if __name__ == "__main__":
    run_machina()
