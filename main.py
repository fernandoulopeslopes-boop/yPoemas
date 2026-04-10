r"""
º¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°
yPoemas - PAI CONSOLIDADO (VERSÃO INTEGRAL SEM CORTES)
º¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°
"""
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
# import matplotlib.pyplot as plt 
import extra_streamlit_components as stx
from PIL import Image, ImageDraw, ImageFont

# --- 🚀 IGNIÇÃO E ESTADO ---
if not isinstance(st.session_state, dict) or "initialized" not in st.session_state:
    st.session_state.lang = 'pt'
    st.session_state.tema = 'Fatos'
    st.session_state.page = 'yPoemas'
    st.session_state.draw = 'Y'
    st.session_state.talk = 'N'
    st.session_state.vydo = 'N'
    st.session_state.eureka_search = ""
    st.session_state.initialized = 'Y'

st.set_page_config(page_title="a Machina de fazer Poesia", page_icon="📜", layout="wide")

# --- 🎨 ESTILOS CSS ---
st.markdown(""" <style>
    footer {visibility: hidden;}
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child { width: 310px; }
    .logo-text { font-weight: 600; font-size: 18px; font-family: 'IBM Plex Sans'; color: #000000; padding-left: 15px; line-height: 1.6; white-space: pre-wrap !important; }
    .logo-img { float: right; max-width: 300px; margin-left: 15px; }
    .stButton > button { width: 100%; text-align: left; border: none; background: transparent; }
    .stButton > button:hover { background-color: #f0f2f6; }
</style> """, unsafe_allow_html=True)

# --- 🛠️ FERRAMENTAS CORE ---
@st.cache_resource
def load_eureka_database():
    path = os.path.join("base", "lexico.pt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return [l.strip() for l in f if " : " in l]
    return []

def translate(text, target_lang):
    if target_lang == "pt": return text
    try: return GoogleTranslator(source="pt", target=target_lang).translate(text=text)
    except: return text

from lay_2_ypo import gera_poema

# =================================================================
# 📱 AS PÁGINAS REAIS (FUNCIONAMENTO INTEGRAL PAI)
# =================================================================

def page_ypoemas():
    st.write(f"⚫ {st.session_state.lang} ( {st.session_state.tema} )")
    script = gera_poema(st.session_state.tema, "")
    poema = "\n".join(script)
    if st.session_state.lang != "pt": poema = translate(poema, st.session_state.lang)
    st.markdown(f"<p class='logo-text'>{poema.replace('\n', '<br>')}</p>", unsafe_allow_html=True)

def page_mini():
    st.write("### 🧩 MINI")
    script = gera_poema("Fatos", "")
    poema = "\n".join(script)
    st.markdown(f"<p class='logo-text'>{poema.replace('\n', '<br>')}</p>", unsafe_allow_html=True)

def page_eureka():
    st.write("### 💡 EUREKA")
    lexico = load_eureka_database()
    search = st.text_input("Busca no Léxico:", value=st.session_state.eureka_search)
    if search:
        results = [l for l in lexico if search.lower() in l.lower()]
        st.write(f"Encontrados: {len(results)}")
        for r in results[:100]: st.write(f"• {r}")

def page_poly():
    st.write("### 🌍 POLYGLOT")
    script = gera_poema(st.session_state.tema, "")
    base_text = "\n".join(script)
    langs = ['en', 'es', 'fr', 'it', 'ca']
    cols = st.columns(len(langs))
    for i, l in enumerate(langs):
        with cols[i]:
            st.write(f"**{l}**")
            st.write(translate(base_text, l))

def page_books():
    st.write("### 📚 BOOKS / ROLS")
    if os.path.exists("base/ativos.txt"):
        with open("base/ativos.txt", "r") as f:
            ativos = f.readlines()
            for a in ativos: st.write(f"📖 {a.strip()}")

def page_help():
    st.write("### ❓ AJUDA")
    if os.path.exists("base/helpers.txt"):
        with open("base/helpers.txt", "r", encoding="utf-8") as f:
            st.markdown(f.read())

def page_about():
    st.write("### ℹ️ ABOUT")
    st.markdown("""
    **A Máquina de Fazer Poesia** Projeto de Fernando Lopes.  
    *Linguística Generativa e Arte Digital.*
    """)

# =================================================================
# 🏰 SIDEBAR PORTAL
# =================================================================

with st.sidebar:
    st.write("### a máquina de fazer Poesia")
    st.write("---")
    
    # pick_lang
    c = st.columns([1,1,1,1,1,1])
    for i, l in enumerate(["pt", "es", "it", "fr", "en", "ca"]):
        if c[i].button(l): st.session_state.lang = l
    
    st.write("---")
    if st.button("yPoemas"): st.session_state.page = "yPoemas"
    if st.button("Mini"): st.session_state.page = "Mini"
    if st.button("Eureka"): st.session_state.page = "Eureka"
    if st.button("Poly"): st.session_state.page = "Poly"
    if st.button("Livros"): st.session_state.page = "Books"
    if st.button("Ajuda"): st.session_state.page = "Help"
    if st.button("Sobre"): st.session_state.page = "About"
    
    st.write("---")
    st.session_state.draw = 'Y' if st.checkbox("Art", value=(st.session_state.draw == 'Y')) else 'N'
    st.session_state.talk = 'Y' if st.checkbox("Talk", value=(st.session_state.talk == 'Y')) else 'N'
    st.session_state.vydo = 'Y' if st.checkbox("Video", value=(st.session_state.vydo == 'Y')) else 'N'

# =================================================================
# 🏁 ROTEADOR
# =================================================================
pages = {
    "yPoemas": page_ypoemas,
    "Mini": page_mini,
    "Eureka": page_eureka,
    "Poly": page_poly,
    "Books": page_books,
    "Help": page_help,
    "About": page_about
}
pages[st.session_state.page]()
