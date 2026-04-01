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
    except ImportError:
        st.warning("Google Translator não conectado")
    try:
        from gtts import gTTS
    except ImportError:
        st.warning("Google TTS não conectado")
else:
    st.warning("Internet não conectada. Traduções não disponíveis no momento.")

# Identificação do IP para LYPO e TYPO
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# Ocultar Menu e Footer do Streamlit
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    </style> """,
    unsafe_allow_html=True,
)

# Ajuste de Padding (Espaçamento)
st.markdown(
    """ <style>
    .reportview-container .main .block-container{
        padding-top: 0rem;
        padding-right: 0rem;
        padding-left: 0rem;
        padding-bottom: 0rem;
    } </style> """,
    unsafe_allow_html=True,
)

# Largura da Sidebar
st.markdown(
    """ 
    <style>
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 310px;
    }
    </style> """,
    unsafe_allow_html=True,
)

# Estilos de Layout (Defs para st.markdown)
st.markdown(
    """
    <style>
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
        padding-top: 0px;
        padding-left: 15px;
    }
    .logo-img {
        float:right;
        max-width: 150px;
    }
    </style> """,
    unsafe_allow_html=True,
)

# Inicialização do SessionState
states = {
    "lang": "pt", "last_lang": "pt", "book": "livro vivo", 
    "take": 0, "mini": 0, "tema": "Fatos", "off_book": 0, 
    "off_take": 0, "eureka": 0, "poly_lang": "ca", 
    "poly_name": "català", "poly_take": 12, "poly_file": "poly_pt.txt",
    "visy": True, "nany_visy": 0, "draw": False, "talk": False, 
    "vydo": False, "arts": [], "auto": False, "rand": False
}

for key, value in states.items():
    if key not in st.session_state:
        st.session_state[key] = value

### eof: settings
### bof: tools

def translate(input_text):
    if st.session_state.lang == "pt" or not have_internet():
        return input_text
    try:
        output_text = GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
        return output_text.replace("<br>>", "<br>").replace("< br>", "<br>")
    except:
        return "Erro na tradução."

def pick_lang():
    cols = st.sidebar.columns([1, 1, 1, 1, 1, 1])
    langs = [("pt", 1), ("es", 2), ("it", 3), ("fr", 4), ("en", 5), ("⚒️", 6)]
    for i, (label, key) in enumerate(langs):
        if cols[i].button(label, key=key):
            st.session_state.lang = label if label != "⚒️" else st.session_state.poly_lang

def draw_check_buttons():
    c1, c2, c3 = st.sidebar.columns([1, 1, 1])
    st.session_state.draw = c1.checkbox("imagem", st.session_state.draw)
    st.session_state.talk = c2.checkbox("áudio", st.session_state.talk)
    st.session_state.vydo = c3.checkbox("vídeo", st.session_state.vydo)

### bof: loaders (Lógica de arquivos)

def load_lypo():
    lypo_user = f"LYPO_{IPAddres}"
    try:
        with open(f"./temp/{lypo_user}", encoding="utf-8") as f:
            return "<br>".join([line.strip() for line in f])
    except:
        return ""

def load_poema(nome_tema, seed_eureka):
    script = gera_poema(nome_tema, seed_eureka)
    lypo_user = f"LYPO_{IPAddres}"
    novo_ypoema = ""
    with open(f"./temp/{lypo_user}", "w", encoding="utf-8") as f:
        f.write(nome_tema + "\n")
        for line in script:
            f.write(line + "\n")
            novo_ypoema += line + "<br>"
    return novo_ypoema

### bof: functions

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    if LOGO_IMAGE is None:
        st.markdown(f"<div class='container'><p class='logo-text'>{LOGO_TEXTO}</p></div>", unsafe_allow_html=True)
    else:
        with open(LOGO_IMAGE, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        st.markdown(
            f"<div class='container'><img class='logo-img' src='data:image/jpg;base64,{img_data}'><p class='logo-text'>{LOGO_TEXTO}</p></div>",
            unsafe_allow_html=True
        )

def talk(text):
    if have_internet() and st.session_state.talk:
        clean_text = text.replace("<br>", "\n")
        tts = gTTS(text=clean_text, lang=st.session_state.lang)
        tts.save("./temp/speech.mp3")
        st.audio("./temp/speech.mp3")

### Interface e Navegação

pick_lang()
draw_check_buttons()

# Substituição da TabBar por Selectbox (Evita erro de pacote)
pagina = st.sidebar.selectbox("Machina Menu", ["Mini", "yPoemas", "Eureka"])

if pagina == "Mini":
    st.subheader("LYPO - Mini Machina")
    if st.button("Gerar Novo"):
        poema = load_poema(st.session_state.tema, "")
        write_ypoema(poema, None)
        talk(poema)
elif pagina == "yPoemas":
    st.write("Módulo yPoemas Ativo")
    # Insira aqui a lógica da page_ypoemas()
else:
    st.write("Módulo Eureka Ativo")
