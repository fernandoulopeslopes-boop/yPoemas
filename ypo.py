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

# Carregamento de bibliotecas para tradução e áudio
if have_internet():
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        pass
    try:
        from gtts import gTTS
    except ImportError:
        pass

# Identificação de ambiente
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# CSS e Identidade Visual (Estilo Original Preservado)
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
    .logo-img { float:right; max-width: 150px; }
    </style> """,
    unsafe_allow_html=True,
)

# Inicialização do SessionState
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

def talk(text):
    if have_internet() and st.session_state.talk:
        try:
            clean_text = text.replace("<br>", " ").replace("\n", " ")
            tts = gTTS(text=clean_text, lang=st.session_state.lang)
            if not os.path.exists("./temp"): os.makedirs("./temp")
            tts.save("./temp/speech.mp3")
            st.audio("./temp/speech.mp3")
        except:
            pass

def pick_lang():
    cols = st.sidebar.columns([1, 1, 1, 1, 1, 1])
    opts = [("pt", 1), ("es", 2), ("it", 3), ("fr", 4), ("en", 5), ("⚒️", 6)]
    for i, (lab, k) in enumerate(opts):
        if cols[i].button(lab, key=f"btn_lang_{k}"):
            st.session_state.lang = lab if lab != "⚒️" else st.session_state.poly_lang

def draw_check_buttons():
    c1, c2, c3 = st.sidebar.columns([1, 1, 1])
    st.session_state.draw = c1.checkbox("imagem", st.session_state.draw)
    st.session_state.talk = c2.checkbox("áudio", st.session_state.talk)
    st.session_state.vydo = c3.checkbox("vídeo", st.session_state.vydo)

### bof: loaders

def load_temas(book):
    try:
        with open(f"./base/rol_{book}.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["Fatos", "Anjos", "Tempo", "Beaba", "Manifesto"]

def load_poema(nome_tema, seed_eureka):
    script = gera_poema(nome_tema, seed_eureka)
    lypo_user = f"LYPO_{IPAddres}"
    novo = ""
    if not os.path.exists("./temp"): os.makedirs("./temp")
    with open(f"./temp/{lypo_user}", "w", encoding="utf-8") as f:
        f.write(nome_tema + "\n")
        for line in script:
            f.write(line + "\n")
            novo += line + "<br>"
    return novo

def write_ypoema(texto, img_path=None):
    if img_path and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"<div class='container'><img class='logo-img' src='data:image/jpg;base64,{data}'><p class='logo-text'>{texto}</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='container'><p class='logo-text'>{texto}</p></div>", unsafe_allow_html=True)

### Lógica de Navegação Principal

pick_lang()
draw_check_buttons()

# Menu de Navegação via Selectbox (Estável)
menu = st.sidebar.selectbox("Machina Menu", ["Mini", "yPoemas", "Eureka"])

if menu == "Mini":
    st.subheader("LYPO - Mini Machina")
    
    if st.session_state.rand:
        temas_list = load_temas(st.session_state.book)
        st.session_state.tema = random.choice(temas_list)
    
    if st.button("Gerar Novo"):
        with st.spinner("Desafiando as regras..."):
            poema = load_poema(st.session_state.tema, "")
            final = translate(poema)
            write_ypoema(final)
            if st.session_state.talk:
                talk(final)

elif menu == "yPoemas":
    st.subheader("📚 Galeria yPoemas")
    temas_g = load_temas(st.session_state.book)
    tema_sel = st.selectbox("Selecione o tema da trilha:", temas_g)
    
    if st.button("Explorar Tema"):
        with st.spinner(f"Processando {tema_sel}..."):
            st.session_state.tema = tema_sel
            poema = load_poema(tema_sel, "")
            final = translate(poema)
            write_ypoema(final)
            if st.session_state.talk:
                talk(final)

elif menu == "Eureka":
    st.subheader("🔍 Módulo Eureka")
    
    with st.sidebar:
        st.markdown("---")
        eureka_val = st.text_input("Seed/Chave:", value=str(st.session_state.eureka))
        if st.button("Fixar Chave"):
            st.session_state.eureka = eureka_val
            st.success("Sentença Prolatada!")

    temas_e = load_temas(st.session_state.book)
    tema_e = st.selectbox("Garimpar em:", temas_e)

    if st.button("Executar Eureka"):
        with st.spinner("Buscando a semente sem lei..."):
            poema = load_poema(tema_e, st.session_state.eureka)
            final = translate(poema)
            write_ypoema(final)
            if st.session_state.talk:
                talk(final)

# Rodapé de Status
st.sidebar.markdown("---")
st.sidebar.caption(f"📍 Host: {hostname} | Versão: 238-Stable")
