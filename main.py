# =================================================================
# 🚀 PAI: MACHINA DE FAZER POESIA (VERSÃO INTEGRAL - PTC)
# =================================================================
import streamlit as st
import os
import re
import random
import time
import socket
import base64
import asyncio
import requests
import json
import glob
import shutil
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from deep_translator import GoogleTranslator
import edge_tts

# --- IGNIÇÃO E INICIALIZAÇÃO BLINDADA ---
if not isinstance(st.session_state, dict) or "initialized" not in st.session_state:
    st.session_state.lang = 'pt'
    st.session_state.last_lang = 'pt'
    st.session_state.tema = 'Fatos'
    st.session_state.book = 'livro vivo'
    st.session_state.take = 0
    st.session_state.mini = 0
    st.session_state.eureka = 0
    st.session_state.talk = 'N'
    st.session_state.vydo = 'N'
    st.session_state.draw = 'Y'
    st.session_state.page = 'yPoemas'
    st.session_state.visy = True
    st.session_state.initialized = 'Y'

# --- CONFIGURAÇÃO DE INTERFACE ---
st.set_page_config(
    page_title="a Machina de fazer Poesia",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- IMPORTAÇÃO DO GERADOR ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(tema, seed): return ["Erro: lay_2_ypo não localizado."]

# --- CACHE E CARREGADORES (UNIVERSO PAI) ---

@st.cache_resource
def load_eureka_database():
    caminho_lexico = os.path.join("base", "lexico_pt.txt")
    if os.path.exists(caminho_lexico):
        try:
            with open(caminho_lexico, "r", encoding="utf-8") as f:
                return [linha.strip() for linha in f if " : " in linha]
        except: return []
    return []

@st.cache_data
def load_help_system(lang):
    help_list = []
    caminho = "./base/helpers.txt"
    if os.path.exists(caminho):
        with open(caminho, encoding="utf-8") as file:
            for line in file: help_list.append(line)
    return help_list

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except: return False

# --- ESTILIZAÇÃO CSS (SIDEBAR 310PX E TEXTO) ---
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child { width: 310px; }
    .logo-text {
        font-weight: 600; font-size: 18px; font-family: 'IBM Plex Sans', sans-serif;
        color: #000000; padding-left: 15px; text-align: left;
        display: block; line-height: 1.6; white-space: pre-wrap !important;
    }
    .logo-img { float: right; max-width: 300px; margin-left: 15px; }
    .stButton > button { width: 100%; text-align: left; border: none; background: transparent; }
    </style> """,
    unsafe_allow_html=True,
)

# --- FERRAMENTAS E FUNÇÕES (PAI ORIGINAL) ---

def translate(input_text):
    if st.session_state.lang == "pt" or not have_internet(): return input_text
    try:
        output = GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
        return output.replace("<br>>", "<br>").replace("< br>", "<br>")
    except: return input_text

def pick_lang():
    cols = st.sidebar.columns([1, 1, 1, 1, 1, 1])
    langs = ["pt", "es", "it", "fr", "en", "⚒️"]
    for i, l in enumerate(langs):
        if cols[i].button(l, key=f"btn_{l}"):
            st.session_state.lang = l if l != "⚒️" else "ca"

def show_icons():
    st.sidebar.markdown(
        "<nav><a href='https://www.facebook.com/nandoulopes' target='_blank'>facebook</a> | "
        "<a href='https://www.instagram.com/maquina_de_fazer_ypoemas/' target='_blank'>instagram</a></nav>",
        unsafe_allow_html=True
    )

def load_poema(nome_tema, seed_eureka):
    script = gera_poema(nome_tema, seed_eureka)
    return "\n".join(script)

def write_ypoema(text, img):
    text_fmt = text.replace("\n", "<br>")
    if img and os.path.exists(img):
        with open(img, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"<div class='container'><img class='logo-img' src='data:image/jpg;base64,{img_b64}'><p class='logo-text'>{text_fmt}</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p class='logo-text'>{text_fmt}</p>", unsafe_allow_html=True)

async def talk_fala_async(text):
    text_clean = text.replace("<br>", " ").replace("\n", " ")
    voices = {"pt": "pt-BR-AntonioNeural", "en": "en-US-GuyNeural", "es": "es-ES-AlvaroNeural", "fr": "fr-FR-RemyNeural", "it": "it-IT-DiegoNeural"}
    voice = voices.get(st.session_state.lang, "pt-BR-AntonioNeural")
    communicate = edge_tts.Communicate(text_clean, voice)
    audio_bytes = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio": audio_bytes += chunk["data"]
    st.audio(audio_bytes, format="audio/mp3")

# --- PÁGINAS ---

def page_ypoemas():
    st.write(f"⚫ {st.session_state.lang} ({st.session_state.book})")
    col1, col2, col3 = st.columns([1, 1, 1])
    if col1.button("◀ Anterior"): st.session_state.take -= 1
    if col2.button("✻ Acaso"): st.session_state.take = random.randint(0, 100)
    if col3.button("Próximo ▶"): st.session_state.take += 1
    
    poema = load_poema(st.session_state.tema, "")
    if st.session_state.lang != "pt": poema = translate(poema)
    write_ypoema(poema, None)
    if st.session_state.talk == 'Y': asyncio.run(talk_fala_async(poema))

def page_mini():
    st.title("Mini Machina")
    if st.button("Gerar Nova"): st.session_state.mini += 1
    poema = load_poema("Fatos", "")
    write_ypoema(poema, None)

def page_eureka():
    st.title("Eureka")
    lexico = load_eureka_database()
    st.write(f"Léxico carregado: {len(lexico)} verbetes.")

# --- SIDEBAR (CONSTRUÇÃO FINAL) ---

with st.sidebar:
    st.write("### a máquina de fazer Poesia")
    st.write("---")
    pick_lang()
    st.write("---")
    
    # NAVEGAÇÃO POR BOTÕES (SUBSTITUINDO OS INTRUSOS)
    if st.button("Mini", key="nav_mini"): st.session_state.page = "Mini"
    if st.button("yPoemas", key="nav_ypo"): st.session_state.page = "yPoemas"
    if st.button("Eureka", key="nav_eureka"): st.session_state.page = "Eureka"
    
    st.write("---")
    st.session_state.draw = 'Y' if st.checkbox("Art", value=(st.session_state.draw == 'Y')) else 'N'
    st.session_state.talk = 'Y' if st.checkbox("Talk", value=(st.session_state.talk == 'Y')) else 'N'
    
    st.write("---")
    show_icons()
    st.write("✨ 📚 ✉️ ☕")

# --- EXECUÇÃO DO UNIVERSO ---

if st.session_state.page == "yPoemas":
    page_ypoemas()
elif st.session_state.page == "Mini":
    page_mini()
elif st.session_state.page == "Eureka":
    page_eureka()
