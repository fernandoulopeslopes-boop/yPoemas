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

# CSS REFINADO: Foco no Poema e na Elegância Bizantina
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .reportview-container .main .block-container{
        padding-top: 2rem; 
    }
    /* Estilo do Texto do Poema */
    .logo-text {
        font-weight: 400; font-size: 22px;
        font-family: 'IBM Plex Sans', sans-serif; 
        color: #1a1a1a;
        line-height: 1.6;
        padding: 25px;
        border-left: 3px solid #f0f2f6;
        background-color: #fafafa;
    }
    .logo-img { float:right; max-width: 150px; opacity: 0.8; }
    /* Ajuste da Sidebar */
    [data-testid="stSidebar"] { background-color: #f8f9fb; }
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
    st.sidebar.write("🌐 Idioma")
    cols = st.sidebar.columns(6)
    opts = [("pt", 1), ("es", 2), ("it", 3), ("fr", 4), ("en", 5), ("⚒️", 6)]
    for i, (lab, k) in enumerate(opts):
        if cols[i].button(lab, key=f"btn_l_{k}"):
            st.session_state.lang = lab if lab != "⚒️" else st.session_state.poly_lang

def draw_check_buttons():
    st.sidebar.write("⚙️ Engrenagens")
    c1, c2, c3 = st.sidebar.columns(3)
    st.session_state.draw = c1.checkbox("🖼️", st.session_state.draw, help="Imagem")
    st.session_state.talk = c2.checkbox("🎙️", st.session_state.talk, help="Áudio")
    st.session_state.vydo = c3.checkbox("🎬", st.session_state.vydo, help="Vídeo")

def load_temas(book):
    try:
        with open(f"./base/rol_{book}.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["Fatos", "Anjos", "Tempo", "Manifesto", "Submundo"]

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
    if img_path and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"<div class='container'><img class='logo-img' src='data:image/jpg;base64,{data}'><p class='logo-text'>{texto}</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='container'><p class='logo-text'>{texto}</p></div>", unsafe_allow_html=True)

### LAYOUT PRINCIPAL: TABS (Abas)

pick_lang()
draw_check_buttons()

# Título da Máquina no topo
st.title("a máquina de fazer Poesia")

# Criação das Abas Originais
tab_mini, tab_gallery, tab_eureka = st.tabs(["📟 Mini", "📚 yPoemas", "🔍 Eureka"])

with tab_mini:
    st.markdown("### LYPO Mini")
    if st.session_state.rand:
        temas_list = load_temas(st.session_state.book)
        st.session_state.tema = random.choice(temas_list)
    
    if st.button("Acionar Engrenagem", key="mini_gen"):
        with st.spinner("Gerando verso..."):
            poema = load_poema(st.session_state.tema, "")
            final = translate(poema)
            write_ypoema(final)
            if st.session_state.talk: talk(final)

with tab_gallery:
    st.markdown("### Galeria de Temas")
    temas_g = load_temas(st.session_state.book)
    col_t1, col_t2 = st.columns([3, 1])
    tema_sel = col_t1.selectbox("Selecione a trilha:", temas_g, label_visibility="collapsed")
    
    if col_t2.button("Explorar", key="gal_gen"):
        with st.spinner("Processando..."):
            st.session_state.tema = tema_sel
            poema = load_poema(tema_sel, "")
            final = translate(poema)
            write_ypoema(final)
            if st.session_state.talk: talk(final)

with tab_eureka:
    st.markdown("### Busca de Sementes")
    c_e1, c_e2 = st.columns([3, 1])
    eureka_val = c_e1.text_input("Seed/Chave:", value=str(st.session_state.eureka))
    if c_e2.button("Fixar", key="fix_seed"):
        st.session_state.eureka = eureka_val
        st.success("Fixada")

    temas_e = load_temas(st.session_state.book)
    tema_e = st.selectbox("Garimpar em:", temas_e, key="eureka_sel")

    if st.button("Executar Busca Eureka", key="eur_gen"):
        with st.spinner("Buscando..."):
            poema = load_poema(tema_e, st.session_state.eureka)
            final = translate(poema)
            write_ypoema(final)
            if st.session_state.talk: talk(final)

# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.caption(f"📍 {hostname} | v.238-Stable")
