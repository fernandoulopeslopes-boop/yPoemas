r"""

º¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°

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
config.toml  == C:\Users\dkvece\.streamlit

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

"""
# =================================================================
# 🚀 BLOCO DE IGNIÇÃO: MACHINA DE FAZER POESIA (ABNP)
# =================================================================
import streamlit as st
import os
import re
import random
import time
from datetime import datetime
from PIL import Image
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import edge_tts         
import asyncio          
import requests         
import json             
import glob             
import shutil           
import socket           
import matplotlib.pyplot as plt 
import extra_streamlit_components as stx 
from PIL import Image, ImageDraw, ImageFont 

# --INICIALIZAÇÃO BLINDADA ---
if not isinstance(st.session_state, dict) or "initialized" not in st.session_state:
    st.session_state.lang = 'pt'
    st.session_state.last_lang = 'pt'
    st.session_state.tema = 'Fatos'
    st.session_state.talk = 'N'
    st.session_state.vydo = 'N'
    st.session_state.draw = 'Y'
    st.session_state.show_eureka = 'Y'
    st.session_state['eureka'] = 0
    st.session_state.page = 'yPoemas'
    st.session_state.initialized = 'Y'

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(
    page_title="a Machina de fazer Poesia",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. CARREGAMENTO DO LÉXICO (41.291 VERBETES EM CACHE)
@st.cache_resource
def load_eureka_database():
    caminho_lexico = os.path.join("base", "lexico.pt")
    if os.path.exists(caminho_lexico):
        try:
            with open(caminho_lexico, "r", encoding="utf-8") as f:
                return [linha.strip() for linha in f if " : " in linha]
        except Exception:
            return []
    return []

# 4. CARREGAMENTO DE TRADUÇÕES E AJUDA
@st.cache_data
def load_help_system(lang):
    help_list = []
    with open(os.path.join("./base/helpers.txt"), encoding="utf-8") as file:
        for line in file:
            help_list.append(line)
    return help_list

# --- TRATAMENTO DE ÁUDIO E MULTIMÍDIA ---
def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

# --- CSS E PADRONIZAÇÃO ---
st.markdown(""" <style>
    footer {visibility: hidden;}
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child { width: 310px; }
    .logo-text { font-weight: 600; font-size: 18px; font-family: 'IBM Plex Sans', sans-serif; color: #000000; padding-left: 15px; text-align: left; display: block; line-height: 1.6; white-space: pre-wrap !important; }
    .logo-img { float: right; max-width: 300px; margin-left: 15px; }
    .stButton > button { width: 100%; text-align: left; border: none; background: transparent; padding: 0.5rem 1rem; }
    .stButton > button:hover { background-color: #f0f2f6; }
</style> """, unsafe_allow_html=True)

# --- FUNÇÕES CORE ---
def translate(input_text):
    if st.session_state.lang == "pt" or not have_internet(): return input_text
    try:
        output_text = GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
        return output_text.replace("<br>>", "<br>")
    except: return input_text

def pick_lang():
    btn_pt, btn_es, btn_it, btn_fr, btn_en, btn_xy = st.sidebar.columns([1,1,1,1,1,1])
    if btn_pt.button("pt", key=1): st.session_state.lang = "pt"
    if btn_es.button("es", key=2): st.session_state.lang = "es"
    if btn_it.button("it", key=3): st.session_state.lang = "it"
    if btn_fr.button("fr", key=4): st.session_state.lang = "fr"
    if btn_en.button("en", key=5): st.session_state.lang = "en"
    if btn_xy.button("⚒️", key=6): st.session_state.lang = "ca"

def show_icons():
    with st.sidebar:
        st.markdown("""<nav>
            <a href='https://www.facebook.com/nandoulopes' target='_blank'>• facebook</a> |
            <a href='mailto:lopes.fernando@hotmail.com' target='_blank'>e-mail</a> |
            <a href='https://www.instagram.com/fernando.lopes.942/' target='_blank'>instagram</a>
            </nav>""", unsafe_allow_html=True)

def draw_check_buttons():
    st.sidebar.write("---")
    st.session_state.draw = 'Y' if st.sidebar.checkbox("Imagem", value=(st.session_state.draw == 'Y')) else 'N'
    st.session_state.talk = 'Y' if st.sidebar.checkbox("Áudio", value=(st.session_state.talk == 'Y')) else 'N'
    st.session_state.vydo = 'Y' if st.sidebar.checkbox("Vídeo", value=(st.session_state.vydo == 'Y')) else 'N'

# --- PÁGINAS ---
from lay_2_ypo import gera_poema

def page_ypoemas():
    st.write(f"⚫ {st.session_state.lang} ( {st.session_state.tema} )")
    script = gera_poema(st.session_state.tema, "")
    txt = "\n".join(script)
    if st.session_state.lang != "pt": txt = translate(txt)
    st.markdown(f"<p class='logo-text'>{txt.replace('\n', '<br>')}</p>", unsafe_allow_html=True)

def page_mini(): st.title("Mini")
def page_eureka(): st.title("Eureka!")
def page_poly(): st.title("Poly")
def page_books(): st.title("Books")
def page_help(): st.title("Help")

# --- SIDEBAR PORTAL ---
with st.sidebar:
    st.write("### a máquina de fazer Poesia")
    pick_lang()
    st.write("---")
    if st.button("yPoemas"): st.session_state.page = "yPoemas"
    if st.button("Mini"): st.session_state.page = "Mini"
    if st.button("Eureka"): st.session_state.page = "Eureka"
    if st.button("Poly"): st.session_state.page = "Poly"
    if st.button("Books"): st.session_state.page = "Books"
    if st.button("Help"): st.session_state.page = "Help"
    draw_check_buttons()
    st.write("---")
    show_icons()

# --- EXECUÇÃO FINAL ---
if st.session_state.page == "yPoemas":
    page_ypoemas()
elif st.session_state.page == "Mini":
    page_mini()
elif st.session_state.page == "Eureka":
    page_eureka()
elif st.session_state.page == "Poly":
    page_poly()
elif st.session_state.page == "Books":
    page_books()
elif st.session_state.page == "Help":
    page_help()
