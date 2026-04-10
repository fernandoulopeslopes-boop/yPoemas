r"""
º¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°
yPoemas - PAI ORIGINAL (INTEGRAL & SINTAXE CORRIGIDA)
[ESTRUTURA DE PALCO COMPLETA - PTC]
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

# =================================================================
# 🚀 IGNIÇÃO E ESTADO DO AMBIENTE
# =================================================================

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

# --- ESTILOS ORIGINAIS (READ-ONLY) ---
st.markdown(""" <style>
    footer {visibility: hidden;}
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child { width: 310px; }
    .logo-text { font-weight: 600; font-size: 18px; font-family: 'IBM Plex Sans'; color: #000000; padding-left: 15px; line-height: 1.6; white-space: pre-wrap !important; }
    .logo-img { float: right; max-width: 300px; margin-left: 15px; }
    .stButton > button { width: 100%; text-align: center; border: 1px solid #ddd; background: #fff; padding: 5px; }
    .stButton > button:hover { background-color: #f0f2f6; border-color: #aaa; }
</style> """, unsafe_allow_html=True)

# =================================================================
# 🛠️ MOTORES E FERRAMENTAS
# =================================================================

@st.cache_resource
def load_eureka_database():
    path = os.path.join("base", "lexico.pt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return [l.strip() for l in f if " : " in l]
    return []

def translate(text, target):
    if target == "pt": return text
    try: return GoogleTranslator(source="pt", target=target).translate(text=text)
    except: return text

from lay_2_ypo import gera_poema

# =================================================================
# 📱 AS PÁGINAS DO PALCO (CORREÇÃO SINTÁTICA NA LINHA 86)
# =================================================================

def nav_menu():
    """Menu de navegação integrado ao palco, conforme o PAI."""
    c = st.columns([1,1,1,1,1,1,1])
    if c[0].button("yPoemas"): st.session_state.page = "yPoemas"
    if c[1].button("Mini"): st.session_state.page = "Mini"
    if c[2].button("Eureka"): st.session_state.page = "Eureka"  # <--- LINHA 86 CORRIGIDA
    if c[3].button("Poly"): st.session_state.page = "Poly"
    if c[4].button("Livros"): st.session_state.page = "Books"
    if c[5].button("Ajuda"): st.session_state.page = "Help"
    if c[6].button("Sobre"): st.session_state.page = "About"
    st.write("---")

def page_ypoemas():
    nav_menu()
    st.write(f"⚫ {st.session_state.lang} ( {st.session_state.tema} )")
    script = gera_poema(st.session_state.tema, "")
    poema = "\n".join(script)
    if st.session_state.lang != "pt": poema = translate(poema, st.session_state.lang)
    st.markdown(f"<p class='logo-text'>{poema.replace('\n', '<br>')}</p>", unsafe_allow_html=True)

def page_mini():
    nav_menu()
    st.write("### 🧩 MINI")
    script = gera_poema("Fatos", "")
    st.markdown(f"<p class='logo-text'>{"\n".join(script).replace('\n', '<br>')}</p>", unsafe_allow_html=True)

def page_eureka():
    nav_menu()
    st.write("### 💡 EUREKA")
    lexico = load_eureka_database()
    search = st.text_input("Busca no Léxico:", value=st.session_state.eureka_search)
    if search:
        results = [l for l in lexico if search.lower() in l.lower()]
        st.write(f"Encontrados: {len(results)}")
        for r in results[:50]: st.write(f"• {r}")

def page_poly():
    nav_menu()
    st.write("### 🌍 POLYGLOT")
    script = gera_poema(st.session_state.tema, "")
    base_text = "\n".join(script)
    st.write("**Texto Base (PT):**")
    st.info(base_text)
    target = st.selectbox("Traduzir para:", ["en", "es", "it", "fr", "ca"])
    st.write(f"**Tradução ({target}):**")
    st.success(translate(base_text, target))

def page_books():
    nav_menu()
    st.write("### 📚 BIBLIOTECA / ROLS")
    if os.path.exists("base/ativos.txt"):
        with open("base/ativos.txt", "r") as f:
            for line in f: st.write(f"📖 {line.strip()}")

def page_help():
    nav_menu()
    st.write("### ❓ AJUDA")
    if os.path.exists("base/helpers.txt"):
        with open("base/helpers.txt", "r", encoding="utf-8") as f:
            st.markdown(f.read())

def page_about():
    nav_menu()
    st.write("### ℹ️ ABOUT")
    st.markdown("A Máquina de Fazer Poesia - Fernando Lopes.")

# =================================================================
# 🏰 SIDEBAR (CONTROLES E LINGUAGEM)
# =================================================================

with st.sidebar:
    st.write("### a máquina de fazer Poesia")
    st.write("---")
    
    langs = ["pt", "es", "it", "fr", "en", "ca"]
    c = st.columns(len(langs))
    for i, l in enumerate(langs):
        if c[i].button(l if l != "ca" else "⚒️"): 
            st.session_state.lang = l
    
    st.write("---")
    st.session_state.draw = 'Y' if st.checkbox("Art", value=(st.session_state.draw == 'Y')) else 'N'
    st.session_state.talk = 'Y' if st.checkbox("Talk", value=(st.session_state.talk == 'Y')) else 'N'
    st.session_state.vydo = 'Y' if st.checkbox("Video", value=(st.session_state.vydo == 'Y')) else 'N'
    
    st.write("---")
    st.markdown("<nav><a href='#'>facebook</a> | <a href='#'>instagram</a></nav>", unsafe_allow_html=True)

# =================================================================
# 🏁 ROTEADOR DO AMBIENTE
# =================================================================

router = {
    "yPoemas": page_ypoemas,
    "Mini": page_mini,
    "Eureka": page_eureka,
    "Poly": page_poly,
    "Books": page_books,
    "Help": page_help,
    "About": page_about
}

router[st.session_state.page]()
