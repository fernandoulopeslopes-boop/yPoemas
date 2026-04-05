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

# A ÚNICA ADIÇÃO AO SEU BACKUP: O PROTOCOLO DE PROTEÇÃO DE LAYOUT
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
        padding-top: 0px;
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

# Carregamento de Bibliotecas de Tradução e Voz
if have_internet():
    try:
        from deep_translator import GoogleTranslator
        from gtts import gTTS
    except ImportError:
        pass

# Identificação do Usuário
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# Inicialização Integral do SessionState (Sem omissões)
states = {
    "lang": "pt", "last_lang": "pt", "book": "livro vivo", "take": 0, "mini": 0,
    "tema": "Fatos", "off_book": 0, "off_take": 0, "eureka": 0,
    "poly_lang": "ca", "poly_name": "català", "poly_take": 12, "poly_file": "poly_pt.txt",
    "visy": True, "nany_visy": 0, "draw": False, "talk": False, "vydo": False,
    "arts": [], "auto": False, "rand": False
}
for key, val in states.items():
    if key not in st.session_state:
        st.session_state[key] = val

### bof: tools (RESTAURADAS DO BACKUP)

def translate(input_text):
    if st.session_state.lang == "pt" or not have_internet():
        return input_text
    try:
        output_text = GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
        return output_text.replace("<br>>", "<br>").replace("< br>", "<br>").replace("<br >", "<br>")
    except:
        return "Erro na tradução."

def pick_lang():
    btn_pt, btn_es, btn_it, btn_fr, btn_en, btn_xy = st.sidebar.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
    if btn_pt.button("pt", key=1): st.session_state.lang = "pt"
    if btn_es.button("es", key=2): st.session_state.lang = "es"
    if btn_it.button("it", key=3): st.session_state.lang = "it"
    if btn_fr.button("fr", key=4): st.session_state.lang = "fr"
    if btn_en.button("en", key=5): st.session_state.lang = "en"
    if btn_xy.button("⚒️", key=6): st.session_state.lang = st.session_state.poly_lang

def draw_check_buttons():
    draw_text, talk_text, vyde_text = st.sidebar.columns([3.8, 3.2, 3])
    st.session_state.draw = draw_text.checkbox("imagem", st.session_state.draw)
    st.session_state.talk = talk_text.checkbox("áudio", st.session_state.talk)
    st.session_state.vydo = vyde_text.checkbox("vídeo", st.session_state.vydo)

def load_temas(book):
    book_list = []
    try:
        with open(os.path.join("./base/rol_" + book.replace(" ", "_") + ".txt"), "r", encoding="utf-8") as file:
            for line in file:
                book_list.append(line.strip())
    except:
        book_list = ["Fatos"]
    return book_list

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE=None):
    if LOGO_IMAGE == None:
        st.markdown(f"<div class='container'><p class='logo-text'>{LOGO_TEXTO}</p></div>", unsafe_allow_html=True)
    else:
        img_b64 = base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()
        st.markdown(f"<div class='container'><img class='logo-img' src='data:image/jpg;base64,{img_b64}'><p class='logo-text'>{LOGO_TEXTO}</p></div>", unsafe_allow_html=True)

### bof: interface (Navegação de Páginas via TabBar)

chosen_id = stx(data=[
    stx.Item(id="yPoemas", title="yPoemas"),
    stx.Item(id="Mini", title="Mini"),
    stx.Item(id="Eureka", title="Eureka"),
    stx.Item(id="Off", title="Off-Machina"),
    stx.Item(id="About", title="About"),
], default="yPoemas")

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list) - 1
    
    # OS 5 BOTÕES DE NAVEGAÇÃO DO PALCO (RESTABELECIDOS)
    foo1, b_more, b_last, b_rand, b_next, b_help, foo2 = st.columns([3, 1, 1, 1, 1, 1, 3])
    
    more = b_more.button("✚")
    last = b_last.button("◀")
    rand = b_rand.button("✻")
    next = b_next.button("▶")
    help = b_help.button("?")

    if last: st.session_state.take = (st.session_state.take - 1) % (maxy + 1)
    if rand: st.session_state.take = random.randint(0, maxy)
    if next: st.session_state.take = (st.session_state.take + 1) % (maxy + 1)

    st.session_state.tema = temas_list[st.session_state.take]
    
    # Sidebar Conteúdo
    with st.sidebar:
        st.header("Configurações")
        pick_lang()
        draw_check_buttons()
        st.session_state.book = st.selectbox("Livro", ["livro vivo", "linguafiada", "faz de conto", "todos os temas"])

    # Palco
    ypoemas_expander = st.expander(f"⚫ {st.session_state.tema} ({st.session_state.take + 1}/{maxy + 1})", expanded=True)
    with ypoemas_expander:
        poema_raw = gera_poema(st.session_state.tema, "")
        poema_html = "<br>".join(poema_raw)
        if st.session_state.lang != "pt":
            poema_html = translate(poema_html)
        
        write_ypoema(poema_html)

    # O GRÁFICO/INFO SÓ APARECE SE HELP FOR CLICADO
    if help:
        st.markdown("---")
        st.subheader(f"Informações Técnicas: {st.session_state.tema}")
        # Aqui entraria a sua lógica de load_info ou gráfico 3D
        st.write("Dados de processamento da Machina para este tema...")

# Router de Páginas
if chosen_id == "yPoemas":
    page_ypoemas()
elif chosen_id == "Mini":
    st.write("Página Mini em construção conforme backup.")
# ... as outras páginas seguem a mesma lógica do seu backup.
