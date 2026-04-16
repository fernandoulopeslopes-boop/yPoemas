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

AlfaBetaAção == C:\WINDOWS\new.ini
config.toml == C:\Users\dkvece\.streamlit

share : https://share.streamlit.io/
deploy: https://share.streamlit.io/nandoulopes/ypoemas/main/ypo.py
runnin: https://nandoulopes-ypoemas-ypo-gf4z3l.streamlitapp.com/
config: chrome://settings/content/siteDetails?site=https%3A%2F%2Fauth.streamlit.io
github: https://github.com/NandouLopes/yPoemas
instag: https://www.instagram.com/maquina_de_fazer_ypoemas/
youtub: https://youtu.be/uL6T3roTtAs
google: https://console.cloud.google.com/welcome?project=ypoemas&cloudshell=false
prosas: https://prosas.com.br/dashboards/my-proposals
bairro: https://www.superbairro.com.br/joseense-cria-maquina-de-produzir-poemas-2/

para novos temas:
- incluir novo_tema em \ypo\base\ativos.txt
- incluir novo_tema em \ypo\base\images.txt
- incluir novo_tema em \ypo\temp\readings.txt
- incluir novo_tema em \base\rol_*.txt
- atualizar ABOUT_NOTES.md se necessário...

VISY == New Visitor
NANY_VISY == Number of Visitors
LYPO == Last YPOema created from curr_ypoema
TYPO == Translated YPOema from LYPO
POLY == Poliglot Idiom == Changed on Catalán

One more test...
"""

import re
import time
import random
import base64
import socket
import streamlit as st
from pathlib import Path
from random import randrange
from extra_streamlit_components import TabBar as stx
from datetime import datetime

### bof: settings

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- [ PATHS SEGUROS ] ---
BASE_DIR = Path(__file__).parent
BASE = BASE_DIR / "base"
DATA = BASE_DIR / "data"
TEMP = BASE_DIR / "temp"
MD_FILES = BASE_DIR / "md_files"
IMAGES = BASE_DIR / "images"
OFF_MACHINA = BASE_DIR / "off_machina"

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        return False

if have_internet():
    try:
        from deep_translator import GoogleTranslator
    except ImportError as ex:
        st.warning(translate("Google Translator não conectado"))
    try:
        from gtts import gTTS
    except ImportError as ex:
        st.warning(translate("Google TTS não conectado"))
else:
    st.warning("Internet não conectada. Traduções não disponíveis no momento.")

# the User IPAddres for LYPO, TYPO
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# hide Streamlit Menu and Footer
st.markdown(
    """ <style>
    /*#MainMenu {visibility: hidden;}*/
    footer {visibility: hidden;}
    </style> """,
    unsafe_allow_html=True,
)

# change padding between components
st.markdown(
    f""" <style>
  .reportview-container.main.block-container{{
        padding-top: {0}rem;
        padding-right: {0}rem;
        padding-left: {0}rem;
        padding-bottom: {0}rem;
    }} </style> """,
    unsafe_allow_html=True,
)

# change sidebar width
st.markdown(
    """
    <style>
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 310px;
    }
    </style> """,
    unsafe_allow_html=True,
)

# load_poema settings
st.markdown(
    """
    <style>
    mark {
      background-color: powderblue;
      color: black;
    }
  .container {
        display: flex;
        /* justify-content: center; */
    }

  .header {
        text-align:center;
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
    </style> """,
    unsafe_allow_html=True,
)

# Initialize SessionState

if "lang" not in st.session_state:
    st.session_state.lang = "pt"
if "last_lang" not in st.session_state:
    st.session_state.last_lang = "pt"

if "book" not in st.session_state:
    st.session_state.book = "livro vivo"
if "take" not in st.session_state:
    st.session_state.take = 0
if "mini" not in st.session_state:
    st.session_state.mini = 0
if "tema" not in st.session_state:
    st.session_state.tema = "Fatos"

if "off_book" not in st.session_state:
    st.session_state.off_book = 0
if "off_take" not in st.session_state:
    st.session_state.off_take = 0

if "eureka" not in st.session_state:
    st.session_state.eureka = 0

if "poly_lang" not in st.session_state:
    st.session_state.poly_lang = "ca"
if "poly_name" not in st.session_state:
    st.session_state.poly_name = "català"
if "poly_take" not in st.session_state:
    st.session_state.poly_take = 12
if "poly_file" not in st.session_state:
    st.session_state.poly_file = "poly_pt.txt"

if "visy" not in st.session_state:
    st.session_state.visy = True
if "nany_visy" not in st.session_state:
    st.session_state.nany_visy = 0

if "draw" not in st.session_state:
    st.session_state.draw = False
if "talk" not in st.session_state:
    st.session_state.talk = False
if "vydo" not in st.session_state:
    st.session_state.vydo = False
if "arts" not in st.session_state:
    st.session_state.arts = []
if "auto" not in st.session_state:
    st.session_state.auto = False
if "rand" not in st.session_state:
    st.session_state.rand = False

### eof: settings
### bof: MACHINA - GERADOR DE POEMA

@st.cache_data
def abre(nome_do_tema):
