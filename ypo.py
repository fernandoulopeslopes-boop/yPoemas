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

# CSS AVANÇADO: O Retorno da Estética Machina
st.markdown(
    """ <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400&family=IBM+Plex+Sans:wght@300;600&display=swap');

    footer {visibility: hidden;}
    
    /* Container Principal */
    .reportview-container .main .block-container{
        padding-top: 1rem;
    }

    /* O Poema: Papiro Digital */
    .poema-container {
        background-color: #fdfdfd;
        border: 1px solid #e0e0e0;
        padding: 40px;
        border-radius: 2px;
        box-shadow: 10px 10px 0px #eeeeee;
        margin-top: 20px;
        min-height: 200px;
    }

    .logo-text {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 300;
        font-size: 24px;
        color: #2c2c2c;
        line-height: 1.5;
        text-align: left;
    }

    .logo-img { 
        float: right; 
        max-width: 120px; 
        filter: grayscale(100%); 
        opacity: 0.7;
        margin-left: 20px;
    }

    /* Estilização das Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f8f9fb;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #eeeeee !important;
        font-weight: 600;
    }
    
    /* Botões Rústicos */
    .stButton>button {
        width: 100%;
        border-radius: 2px;
        border: 1px solid #000;
        background-color: transparent;
        color: #000;
        font-family: 'IBM Plex Mono', monospace;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #000;
        color: #fff;
    }

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
            path = "./temp/speech.mp3"
            tts.save(path)
            st.audio(path)
        except:
            pass

def pick_lang():
    st.sidebar.markdown("### 🌐 Dialetos")
    cols = st.sidebar.columns(3)
    opts = [("pt", 0), ("es", 1), ("it", 2), ("fr", 3), ("en", 4), ("ca", 5)]
    for i, (lab, idx) in enumerate(opts):
        col_idx = i % 3
        if cols[col_idx].button(lab, key=f"l_{idx}"):
            st.session_state.lang = lab

def draw_check_buttons():
    st.sidebar.markdown("### ⚙️ Sensores")
    c1, c2 = st.sidebar.columns(2)
    st.session_state.draw = c1.checkbox("Imagens", st.session_state.draw)
    st.session_state.talk = c2.checkbox("Voz", st.session_state.talk)

def load_temas(book):
    try:
        with open(f"./base/rol_{book}.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["Fatos", "Anjos", "Tempo", "Manifesto", "Direito"]

def load_poema(nome_tema, seed_eureka):
    seed_limpa = str(seed_eureka) if seed_eureka is not None else ""
    script = gera_poema(nome_tema, seed_limpa)
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
    # O layout do poema agora usa a classe poema-container definida no CSS
    if img_path and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"""<div class='poema-container'>
            <img class='logo-img' src='data:image/jpg;base64,{data}'>
            <p class='logo-text'>{texto}</p>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class='poema-container'>
            <p class='logo-text'>{texto}</p>
            </div>""", unsafe_allow_html=True)

### NAVEGAÇÃO POR ABAS (ESTÉTICA ORIGINAL)

pick_lang()
draw_check_buttons()

st.title("a máquina de fazer Poesia")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["[ MINI ]", "[ yPOEMAS ]", "[ EUREKA ]"])

with tab1:
    col_m1, col_m2 = st.columns([3, 1])
    temas_mini = load_temas(st.session_state.book)
    tema_mini = col_m1.selectbox("Tema do Dia", temas_mini, label_visibility="collapsed")
    
    if col_m2.button("GERAR", key="btn_mini"):
        with st.spinner("Girando engrenagens..."):
            poema = load_poema(tema_mini, "")
            final = translate(poema)
            write_ypoema(final)
            if st.session_state.talk: talk(final)

with tab2:
    temas_g = load_temas(st.session_state.book)
    tema_gal = st.selectbox("Selecione a trilha bizantina:", temas_g)
    
    if st.button("EXPLORAR TRILHA", key="btn_gal"):
        with st.spinner("Garimpando versos..."):
            st.session_state.tema = tema_gal
            poema = load_poema(tema_gal, "")
            final = translate(poema)
            write_ypoema(final)
            if st.session_state.talk: talk(final)

with tab3:
    col_e1, col_e2 = st.columns([2, 1])
    eureka_input = col_e1.text_input("Inserir Semente (Seed):", value=str(st.session_state.eureka))
    if col_e2.button("FIXAR", key="btn_fix"):
        st.session_state.eureka = eureka_input
    
    temas_eureka = load_temas(st.session_state.book)
    tema_eureka = st.selectbox("Tema para Garimpo:", temas_eureka, key="sel_eureka")

    if st.button("EXECUTAR EUREKA", key="btn_eureka"):
        with st.spinner("Recuperando do submundo..."):
            poema = load_poema(tema_eureka, st.session_state.eureka)
            final = translate(poema)
            write_ypoema(final)
            if st.session_state.talk: talk(final)

# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.caption(f"Host: {hostname}")
st.sidebar.caption(f"Status: Trial 238-Stable")
