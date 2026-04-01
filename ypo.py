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
        pass
    try:
        from gtts import gTTS
    except ImportError:
        pass
else:
    st.warning("Internet não conectada. Traduções/Áudio desativados.")

# Identificação
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# CSS e Layout Original
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .reportview-container .main .block-container{
        padding-top: 0rem; padding-right: 0rem;
        padding-left: 0rem; padding-bottom: 0rem;
    }
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 310px;
    }
    mark { background-color: powderblue; color: black; }
    .container { display: flex; }
    .logo-text {
        font-weight: 600; font-size: 18px;
        font-family: 'IBM Plex Sans'; color: #000000;
        padding-top: 0px; padding-left: 15px;
    }
    .logo-img { float:right; }
    </style> """,
    unsafe_allow_html=True,
)

# Inicialização do SessionState (Seu padrão)
keys = [
    ("lang", "pt"), ("last_lang", "pt"), ("book", "livro vivo"),
    ("take", 0), ("mini", 0), ("tema", "Fatos"), ("off_book", 0),
    ("off_take", 0), ("eureka", 0), ("poly_lang", "ca"),
    ("poly_name", "català"), ("poly_take", 12), ("poly_file", "poly_pt.txt"),
    ("visy", True), ("nany_visy", 0), ("draw", False), ("talk", False),
    ("vydo", False), ("arts", []), ("auto", False), ("rand", False)
]
for k, v in keys:
    if k not in st.session_state:
        st.session_state[k] = v

### bof: tools

def translate(input_text):
    if st.session_state.lang == "pt" or not have_internet():
        return input_text
    try:
        return GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
    except:
        return input_text

def pick_lang():
    cols = st.sidebar.columns([1, 1, 1, 1, 1, 1])
    opts = [("pt", 1), ("es", 2), ("it", 3), ("fr", 4), ("en", 5), ("⚒️", 6)]
    for i, (lab, k) in enumerate(opts):
        if cols[i].button(lab, key=k):
            st.session_state.lang = lab if lab != "⚒️" else st.session_state.poly_lang

def draw_check_buttons():
    c1, c2, c3 = st.sidebar.columns([3.8, 3.2, 3])
    st.session_state.draw = c1.checkbox("imagem", st.session_state.draw)
    st.session_state.talk = c2.checkbox("áudio", st.session_state.talk)
    st.session_state.vydo = c3.checkbox("vídeo", st.session_state.vydo)

### bof: stats & readings (Sua lógica de contadores)

def update_visy():
    try:
        with open("./temp/visitors.txt", "r+") as f:
            tots = int(f.read()) + 1
            f.seek(0)
            f.write(str(tots))
            st.session_state.nany_visy = tots
    except: pass

def update_readings(tema):
    try:
        lines = []
        with open("./temp/read_list.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open("./temp/read_list.txt", "w", encoding="utf-8") as f:
            for line in lines:
                parts = line.split("|")
                if len(parts) > 2 and parts[1] == tema:
                    f.write(f"|{tema}|{int(parts[2])+1}|\n")
                else: f.write(line)
    except: pass

### bof: loaders

def load_temas(book):
    try:
        with open(f"./base/rol_{book}.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except: return ["Fatos"]

def load_poema(nome_tema, seed_eureka):
    script = gera_poema(nome_tema, seed_eureka)
    lypo_user = f"LYPO_{IPAddres}"
    novo = ""
    with open(f"./temp/{lypo_user}", "w", encoding="utf-8") as f:
        f.write(nome_tema + "\n")
        for line in script:
            f.write(line + "\n")
            novo += line + "<br>"
    update_readings(nome_tema)
    return novo

def write_ypoema(texto, img_path):
    if img_path and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"<div class='container'><img class='logo-img' src='data:image/jpg;base64,{data}'><p class='logo-text'>{texto}</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='container'><p class='logo-text'>{texto}</p></div>", unsafe_allow_html=True)

### Main Interface

pick_lang()
draw_check_buttons()

# Navegação (Substituindo o TabBar problemático por Selectbox)
menu = st.sidebar.selectbox("Machina Menu", ["Mini", "yPoemas", "Eureka"])

if menu == "Mini":
    st.subheader("LYPO - Mini Machina")
    
    if st.session_state.rand:
        temas = load_temas(st.session_state.book)
        st.session_state.tema = random.choice(temas)
        
    if st.button("Gerar Novo"):
        poema = load_poema(st.session_state.tema, "")
        txt_tradu = translate(poema)
        write_ypoema(txt_tradu, None)
        if st.session_state.talk:
            clean = txt_tradu.replace("<br>", "\n")
            tts = gTTS(text=clean, lang=st.session_state.lang)
            tts.save("./temp/speech.mp3")
            st.audio("./temp/speech.mp3")

elif menu == "yPoemas":
    st.write("### Módulo yPoemas")
    # Aqui entra sua lógica de carrossel de temas
    
else:
    st.write("### Módulo Eureka")
    # Aqui entra sua lógica de busca por sementes


