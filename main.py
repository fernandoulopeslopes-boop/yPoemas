import os
import re
import time
import random
import base64
import socket
import streamlit as st
import extra_streamlit_components as stx

from datetime import datetime
from lay_2_ypo import gera_poema

### 0. AXIOMA ZERO: PROTEÇÃO DE LAYOUT INTEGRADA NO BACKUP
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

st.markdown(
    """
    <style>
    /* Trava a sidebar em 310px para não encavalar */
    [data-testid="stSidebar"] {
        min-width: 310px;
        max-width: 310px;
    }
    /* Centraliza o palco principal e dá respiro nas bordas */
    .main .block-container {
        max-width: 850px;
        padding-top: 1.5rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1.5rem;
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

### 1. FUNÇÕES DE SUPORTE (RESTAURADAS DO SEU BACKUP)

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False

def translate(input_text):
    if st.session_state.lang == "pt" or not have_internet():
        return input_text
    try:
        from deep_translator import GoogleTranslator
        out = GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
        return out.replace("<br>>", "<br>").replace("< br>", "<br>").replace("<br >", "<br>")
    except:
        return input_text

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE=None):
    if LOGO_IMAGE == None:
        st.markdown(f"<div class='container'><p class='logo-text'>{LOGO_TEXTO}</p></div>", unsafe_allow_html=True)
    else:
        with open(LOGO_IMAGE, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode()
        st.markdown(f"<div class='container'><img class='logo-img' src='data:image/jpg;base64,{img_b64}'><p class='logo-text'>{LOGO_TEXTO}</p></div>", unsafe_allow_html=True)

### 2. SESSION STATE (INTEGRAL)

states = {
    "lang": "pt", "last_lang": "pt", "book": "livro vivo", "take": 0, "mini": 0,
    "tema": "Fatos", "off_book": 0, "off_take": 0, "eureka": 0,
    "poly_lang": "ca", "poly_name": "català", "poly_take": 12, "poly_file": "poly_pt.txt",
    "visy": True, "nany_visy": 0, "draw": True, "talk": False, "vydo": False,
    "arts": [], "auto": False, "rand": False
}
for key, val in states.items():
    if key not in st.session_state:
        st.session_state[key] = val

### 3. NAVEGAÇÃO SUPERIOR (stx TabBar)

chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="yPoemas", title="yPoemas", description=""),
    stx.TabBarItemData(id="Mini", title="Mini", description=""),
    stx.TabBarItemData(id="Eureka", title="Eureka", description=""),
    stx.TabBarItemData(id="Off", title="Off-Machina", description=""),
    stx.TabBarItemData(id="About", title="About", description=""),
], default="yPoemas")

### 4. PÁGINA PRINCIPAL (O MOTOR ORIGINAL)

def page_ypoemas():
    # Carregamento de Temas do arquivo rol_
    filename = f"./base/rol_{st.session_state.book.replace(' ', '_')}.txt"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            temas_list = [line.strip() for line in f if line.strip()]
    except:
        temas_list = ["Fatos"]
    
    maxy = len(temas_list) - 1
    st.session_state.take %= (maxy + 1)
    st.session_state.tema = temas_list[st.session_state.take]

    # SIDEBAR COMPLETA
    with st.sidebar:
        st.header("Configurações")
        # Seleção de Idioma (6 colunas)
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        if c1.button("pt"): st.session_state.lang = "pt"
        if c2.button("es"): st.session_state.lang = "es"
        if c3.button("it"): st.session_state.lang = "it"
        if c4.button("fr"): st.session_state.lang = "fr"
        if c5.button("en"): st.session_state.lang = "en"
        if c6.button("⚒️"): st.session_state.lang = st.session_state.poly_lang
        
        st.write("---")
        st.session_state.book = st.selectbox("Livro", ["livro vivo", "linguafiada", "faz de conto", "todos os temas"], 
                                            index=["livro vivo", "linguafiada", "faz de conto", "todos os temas"].index(st.session_state.book))
        
        st.session_state.draw = st.checkbox("imagem", st.session_state.draw)
        st.session_state.talk = st.checkbox("áudio", st.session_state.talk)
        st.session_state.vydo = st.checkbox("vídeo", st.session_state.vydo)

    # OS 5 BOTÕES DO PALCO (ORDEM ORIGINAL)
    f1, b_more, b_last, b_rand, b_next, b_help, f2 = st.columns([3, 1, 1, 1, 1, 1, 3])
    
    act_more = b_more.button("✚")
    if b_last.button("◀"): 
        st.session_state.take = (st.session_state.take - 1) % (maxy + 1)
        st.rerun()
    if b_rand.button("✻"): 
        st.session_state.take = random.randint(0, maxy)
        st.rerun()
    if b_next.button("▶"): 
        st.session_state.take = (st.session_state.take + 1) % (maxy + 1)
        st.rerun()
    act_help = b_help.button("?")

    # EXIBIÇÃO DO YPOEMA
    ypoemas_expander = st.expander(f"⚫ {st.session_state.tema} ({st.session_state.take + 1}/{maxy + 1})", expanded=True)
    with ypoemas_expander:
        script = gera_poema(st.session_state.tema, "")
        poema_html = "<br>".join(script)
        
        if st.session_state.lang != "pt":
            poema_html = translate(poema_html)
            
        img_file = f"./images/matrix/{st.session_state.tema.capitalize()}.jpg"
        write_ypoema(poema_html, img_file if st.session_state.draw else None)

    # CONDICIONAIS (HELP E MORE)
    if act_help:
        st.markdown("---")
        st.info(f"Análise e Gráficos da estrutura: {st.session_state.tema}")
        # Chame sua função load_info aqui
        
    if act_more:
        st.success(f"Mais detalhes do tema: {st.session_state.tema}")

# ROTEADOR DE PÁGINAS
if chosen_id == "yPoemas":
    page_ypoemas()
else:
    st.info(f"Página '{chosen_id}' ativa. Insira o código original desta aba aqui.")
