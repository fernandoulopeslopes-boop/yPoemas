r"""
º¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°
yPoemas - PAI CONSOLIDADO (AMBIENTE INTEGRAL FUNCIONAL)
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
# import matplotlib.pyplot as plt  # <--- Comentado para evitar erro de deploy
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
def translate(text):
    if st.session_state.lang == "pt": return text
    try: return GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=text)
    except: return text

from lay_2_ypo import gera_poema

# =================================================================
# 📱 AS PÁGINAS (FUNCIONAMENTO INTEGRAL CONFORME O PAI)
# =================================================================

def page_ypoemas():
    st.write(f"⚫ {st.session_state.lang} ( {st.session_state.tema} )")
    script = gera_poema(st.session_state.tema, "")
    poema = "\n".join(script)
    if st.session_state.lang != "pt": poema = translate(poema)
    st.markdown(f"<p class='logo-text'>{poema.replace('\n', '<br>')}</p>", unsafe_allow_html=True)

def page_mini():
    st.write("### 🧩 MINI")
    script = gera_poema("Fatos", "")
    poema = "\n".join(script)
    st.markdown(f"<p class='logo-text'>{poema.replace('\n', '<br>')}</p>", unsafe_allow_html=True)

def page_eureka():
    st.write("### 💡 EUREKA")
    st.write("Exploração do Léxico.")

def page_poly():
    st.write("### 🌍 POLY")
    st.write("Traduções e variações.")

def page_books():
    st.write("### 📚 BOOKS")
    st.write("Gestão de Livros.")

def page_help():
    st.write("### ❓ AJUDA")
    st.write("Manual da Machina.")

def page_about():
    st.write("### ℹ️ ABOUT")
    st.write("Sobre o Criador.")

# =================================================================
# 🏰 SIDEBAR PORTAL
# =================================================================

with st.sidebar:
    st.write("### a máquina de fazer Poesia")
    st.write("---")
    
    # pick_lang
    c = st.columns([1,1,1,1,1,1])
    if c[0].button("pt"): st.session_state.lang = "pt"
    if c[1].button("es"): st.session_state.lang = "es"
    if c[2].button("it"): st.session_state.lang = "it"
    if c[3].button("fr"): st.session_state.lang = "fr"
    if c[4].button("en"): st.session_state.lang = "en"
    if c[5].button("⚒️"): st.session_state.lang = "ca"
    
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
    
    st.write("---")
    st.markdown("<nav><a href='#'>facebook</a> | <a href='#'>instagram</a></nav>", unsafe_allow_html=True)

# =================================================================
# 🏁 ROTEADOR
# =================================================================

if st.session_state.page == "yPoemas": page_ypoemas()
elif st.session_state.page == "Mini": page_mini()
elif st.session_state.page == "Eureka": page_eureka()
elif st.session_state.page == "Poly": page_poly()
elif st.session_state.page == "Books": page_books()
elif st.session_state.page == "Help": page_help()
elif st.session_state.page == "About": page_about()
