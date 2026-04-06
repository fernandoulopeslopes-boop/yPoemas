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

# =================================================================
# 1. SETTINGS & INTERFACE
# =================================================================

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
    except:
        return False

if have_internet():
    try:
        from deep_translator import GoogleTranslator
        from gtts import gTTS
    except ImportError:
        pass

hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

st.markdown(
    """ <style>
    footer {visibility: hidden;}
    
    .main .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .logo-text {
        font-weight: 400;
        font-size: 20px;
        font-family: 'IBM Plex Sans', serif;
        color: #000000;
        line-height: 1.6;
        padding-top: 10px;
        padding-left: 15px;
    }
    
    .logo-img {
        float: right;
        margin-left: 20px;
        max-width: 280px;
        border-radius: 4px;
    }

    [data-testid="stSidebar"] {
        min-width: 310px;
        max-width: 310px;
    }
    </style> """,
    unsafe_allow_html=True,
)

# =================================================================
# 2. SESSION STATE
# =================================================================

if "lang" not in st.session_state: st.session_state.lang = "pt"
if "last_lang" not in st.session_state: st.session_state.last_lang = "pt"
if "book" not in st.session_state: st.session_state.book = "livro vivo"
if "take" not in st.session_state: st.session_state.take = 0
if "tema" not in st.session_state: st.session_state.tema = "Fatos"
if "visy" not in st.session_state: st.session_state.visy = True
if "draw" not in st.session_state: st.session_state.draw = True
if "talk" not in st.session_state: st.session_state.talk = False
if "vydo" not in st.session_state: st.session_state.vydo = False
if "arts" not in st.session_state: st.session_state.arts = []

# =================================================================
# 3. TOOLS & LOADERS
# =================================================================

def translate(input_text):
    if st.session_state.lang == "pt" or not have_internet():
        return input_text
    try:
        return GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
    except:
        return input_text

def load_temas(book):
    try:
        with open(os.path.join("./base/rol_" + book + ".txt"), "r", encoding="utf-8") as f:
            return [line.strip().replace(" ", "") for line in f if line.strip()]
    except:
        return ["Fatos"]

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    if LOGO_IMAGE == None:
        st.markdown(f"<div class='container'><p class='logo-text'>{LOGO_TEXTO}</p></div>", unsafe_allow_html=True)
    else:
        try:
            with open(LOGO_IMAGE, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode()
            st.markdown(
                f"""<div class='container'>
                    <img class='logo-img' src='data:image/jpg;base64,{img_base64}'>
                    <p class='logo-text'>{LOGO_TEXTO}</p>
                </div>""", 
                unsafe_allow_html=True
            )
        except:
            st.markdown(f"<div class='container'><p class='logo-text'>{LOGO_TEXTO}</p></div>", unsafe_allow_html=True)

# =================================================================
# 4. PAGES
# =================================================================

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    if st.session_state.take >= len(temas_list): st.session_state.take = 0
    st.session_state.tema = temas_list[st.session_state.take]
    
    poema_raw = gera_poema(st.session_state.tema, "")
    poema_formatado = "<br>".join(poema_raw)
    
    if st.session_state.lang != "pt":
        poema_formatado = translate(poema_formatado)

    st.write(f"### {st.session_state.tema}")
    write_ypoema(poema_formatado, None)

# =================================================================
# 5. MAIN
# =================================================================

def main():
    if st.session_state.visy:
        st.session_state.visy = False

    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
