r"""
yPoemas is an app that randomly collects words and phrases
from specific databases and organizes them
in different new poems or poetic texts.

All texts are unique and will only be repeated
after they are sold out the thourekasands
of combinations possible to each theme.

[Epitaph]
Passei boa parte da minha vida escrevendo a "machina".
A leitura fica para os amanhãs.
Não vivo no meu tempo.

º¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°

ツpoemas
"""

import os
import re
import time
import random
import base64
import socket
import datetime
import streamlit as st
from extra_streamlit_components import TabBar as stx
from random import randrange

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- PATHS ---
BASE_DIR = os.path.dirname(__file__)
BASE = os.path.join(BASE_DIR, "base")
DATA = os.path.join(BASE_DIR, "data")
TEMP = os.path.join(BASE_DIR, "temp")
MD_FILES = os.path.join(BASE_DIR, "md_files")
IMAGES = os.path.join(BASE_DIR, "images")
OFF_MACHINA = os.path.join(BASE_DIR, "off_machina")
os.makedirs(TEMP, exist_ok=True)

IPAddres = socket.gethostbyname(socket.gethostname())
LYPO_FILE = os.path.join(TEMP, f"LYPO_{IPAddres}")
TYPO_FILE = os.path.join(TEMP, f"TYPO_{IPAddres}")

# --- CSS ÚNICO: remove faixa branca + estilo do título ---
st.markdown("""
<style>
footer {visibility: hidden;}
section[data-testid="stSidebar"] {display: block!important;}
header[data-testid="stHeader"] {height: 0rem;}
div[data-testid="stToolbar"] {display: none;}
div[data-testid="stDecoration"] {display: none;}
.reportview-container.main.block-container{
    padding-top: 0rem;
    padding-right: 1rem;
    padding-left: 1rem;
    padding-bottom: 0rem;
}
div[data-testid="stVerticalBlock"] > div:first-child {margin-top: -1rem;}
[data-testid='stSidebar'][aria-expanded='true'] > div:first-child {width: 310px;}
mark {background-color: powderblue; color: black;}
.container {display: flex; align-items: flex-start; gap: 15px;}
.poem-title {
    font-weight: 700; font-size: 22px; font-family: 'IBM Plex Sans';
    color: #000000; margin: 0 0 8px 0; padding-left: 0px; text-align: left;
}
.logo-text {
    font-weight: 400; font-size: 18px; font-family: 'IBM Plex Sans';
    color: #000000; padding-top: 0px; line-height: 1.6;
}
.logo-img {max-width: 200px; height: auto;}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
DEFAULTS = {
    "lang": "pt", "last_lang": "pt", "book": "livro vivo", "take": 0, "mini": 0,
    "tema": "Fatos", "off_book": 0, "off_take": 0, "eureka": 0, "poly_lang": "ca",
    "poly_name": "català", "poly_take": 12, "poly_file": "poly_pt.txt",
    "visy": True, "nany_visy": 0, "draw": False, "talk": False, "vydo": False,
    "arts": [], "auto": False, "rand": False, "internet": None, "translator": None, "gtts": None
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- INTERNET + IMPORTS PESADOS ---
@st.cache_resource
def check_deps():
    def have_net(host="8.8.8.8", port=53, timeout=2):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except:
            return False
    internet = have_net()
    translator = gtts = None
    if internet:
        try:
            from deep_translator import GoogleTranslator
            translator = GoogleTranslator
        except: pass
        try:
            from gtts import gTTS
            gtts = gTTS
        except: pass
    return internet, translator, gtts

st.session_state.internet, st.session_state.translator, st.session_state.gtts = check_deps()
if not st.session_state.internet:
    st.warning("Internet não conectada. Traduções não disponíveis no momento.")

# --- HELPERS ARQUIVO ---
@st.cache_data
def load
