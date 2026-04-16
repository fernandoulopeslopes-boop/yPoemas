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

import re
import time
import random
import base64
import socket
import streamlit as st
from pathlib import Path
from random import randrange
from datetime import datetime

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

BASE_DIR = Path(__file__).parent
BASE = BASE_DIR / "base"
DATA = BASE_DIR / "data"
TEMP = BASE_DIR / "temp"
MD_FILES = BASE_DIR / "md_files"
IMAGES = BASE_DIR / "images"
OFF_MACHINA = BASE_DIR / "off_machina"

# Garante que pastas existem
TEMP.mkdir(exist_ok=True)

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
    except ImportError:
        st.warning("Google Translator não conectado")
    try:
        from gtts import gTTS
    except ImportError:
        st.warning("Google TTS não conectado")
else:
    st.warning("Internet não conectada. Traduções não disponíveis no momento.")

hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

st.markdown(""" <style> footer {visibility: hidden;} </style> """, unsafe_allow_html=True)

# CSS original mantido
st.markdown("""
    <style>
    mark { background-color: powderblue; color: black; }
   .container { display: flex; }
   .header { text-align:center; }
   .logo-text { font-weight: 600; font-size: 18px; font-family: 'IBM Plex Sans'; color: #000000; padding-top: 0px; padding-left: 15px; }
   .logo-img { float:right; }
    </style> """, unsafe_allow_html=True)

# SessionState
for key, default in {
    "lang": "pt", "last_lang": "pt", "book": "livro vivo", "take": 0, "mini": 0, "tema": "Fatos",
    "off_book": 0, "off_take": 0, "eureka": 0, "poly_lang": "ca", "poly_name": "català",
    "poly_take": 12, "poly_file": "poly_pt.txt", "visy": True, "nany_visy": 0,
    "draw": False, "talk": False, "vydo": False, "arts": [], "auto": False, "rand": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

### MACHINA - MOTOR COM FALLBACKS

@st.cache_data
def abre(nome_do_tema):
    full_name = DATA / f"{nome_do_tema}.ypo"
    lista = []
    try:
        with open(full_name, encoding="utf-8") as file:
            for line in file:
                lista.append(line)
    except (FileNotFoundError, UnicodeDecodeError):
        st.error(f"Arquivo {nome_do_tema}.ypo não encontrado em /data/")
        lista = ["*Erro\n", "|01|01|erro|F|1|1|arquivo não encontrado|\n"]
    return lista

@st.cache_data
def load_babel():
    lista = []
    try:
        with open(BASE / "babel.txt", "r", encoding="utf-8") as babel:
            for line in babel:
                lista.append(line.strip())
    except FileNotFoundError:
        lista = ["ba", "be", "bi", "bo", "bu"] # fallback
    return lista

@st.cache_data
def load_cidades():
    cidades = []
    try:
        with open(BASE / "fatos_cidades.txt", encoding="utf8") as file:
            for line in file:
                if line.strip():
                    cidades.append(line.strip())
    except FileNotFoundError:
        cidades = ["São Paulo", "Rio de Janeiro"]
    return cidades

@st.cache_data
def load_abnp():
    lista = []
    try:
        with open(BASE / "abnp.txt", encoding="utf-8") as file:
            for line in file:
                alinhas = line.split("|")
                for item in alinhas:
                    item = item.strip()
                    if item:
                        lista.append(item)
    except FileNotFoundError:
        lista = ["ABNT"]
    return lista

def novo_babel(swap_pala):
    lista_silabas = load_babel()
    sinais_ini = [".", ",", ":", "!", "?", "...", " "]
    sinais_end = [".", "!", "?", "..."]
    min_versos = 5
    max_versos = 15
    qtd_versos = random.randrange(min_versos, max_versos)
    novo_poema = []
    for nQtdLin in range(qtd_versos):
        novo_verso_babel = ""
        if swap_pala == 0:
            qtd_palas = random.randrange(3, 7)
        else:
            qtd_palas = swap_pala
        for nova_frase in range(qtd_palas):
            nova_pala = ""
            qtd_silabas = random.randrange(2, 4)
            for palavra in range(qtd_silabas):
                if lista_silabas:
                    njump = random.randrange(len(lista_silabas))
                    nova_silaba = str(lista_silabas[njump])
                    nova_pala += nova_silaba.strip()
            nova = nova_pala.replace("aa", "a").replace("ee", "e").replace("ii", "i").replace("uu", "u")
            novo_verso_babel += nova.strip() + " "
        if nQtdLin == 0:
            njump = random.randrange(len(sinais_ini))
            sinal = sinais_ini[njump]
            novo_poema.append("")
            novo_poema.append(novo_verso_babel.strip() + sinal)
        else:
            nany = random.randrange(100)
            if nany <= 50:
                njump = random.randrange(len(sinais_ini))
                sinal = sinais_ini[njump]
                novo_verso_babel = novo_verso_babel.rstrip() + sinal
            novo_poema.append(novo_verso_babel.strip())
            if nany <= 50:
                if ","!= sinal:
                    novo_poema.append("")
    if novo_poema:
        last = novo_poema[-1]
        njump = random.randrange(len(sinais_end))
        sinal = sinais_end[njump]
        if len(last) > 1 and not last[-1] in sinais_ini:
            if "," == last or ":" == last:
                novo_poema[-1] += sinal
            else:
                novo_poema[-1] += "."
    return novo_poema
