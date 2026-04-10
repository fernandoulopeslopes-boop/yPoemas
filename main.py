r"""
º¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°
yPoemas - PAI ORIGINAL (INTEGRAL, FUNCIONAL E DENSO)
[CONTEÚDO INTERNO RESTAURADO - PTC]
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
</style> """, unsafe_allow_html=True)

# =================================================================
# 🛠️ MOTORES E FERRAMENTAS (O RECHEIO DAS PÁGINAS)
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

def nav_menu():
    c = st.columns([1,1,1,1,1,1,1])
    if c[0].button("yPoemas"): st.session_state.page = "yPoemas"
    if c[1].button("Mini"): st.session_state.page = "Mini"
    if c[2].button("Eureka"): st.session_state.page = "Eureka"
    if c[3].button("Poly"): st.session_state.page = "Poly"
    if c[4].button("Livros"): st.session_state.page = "Books"
    if c[5].button("Ajuda"): st.session_state.page = "Help"
    if c[6].button("Sobre"): st.session_state.page = "About"
    st.write("---")

# =================================================================
# 📱 AS PÁGINAS DO PALCO (SEM "CASCAS" VAZIAS)
# =================================================================

def page_ypoemas():
    nav_menu()
    st.write(f"⚫ {st.session_state.lang} ( {st.session_state.tema} )")
    script = gera_poema(st.session_state.tema, "")
    poema = "\n".join(script)
    if st.session_state.lang != "pt": poema = translate(poema, st.session_state.lang)
    st.markdown(f"<p class='logo-text'>{poema.replace('\n', '<br>')}</p>", unsafe_allow_html=True)

def page_mini():
    nav_menu()
    st.write("### 🧩 MINI-MACHINA")
    # Lógica Mini: Geração compacta e instantânea
    script = gera_poema(st.session_state.tema, "mini")
    txt_mini = " / ".join([l.strip() for l in script if l.strip()])
    st.markdown(f"<p class='logo-text' style='font-style: italic;'>{txt_mini}</p>", unsafe_allow_html=True)

def page_eureka():
    nav_menu()
    st.write("### 💡 EUREKA (LÉXICO)")
    lexico = load_eureka_database()
    col_e1, col_e2 = st.columns([2,1])
    with col_e1:
        search = st.text_input("Localizar radical ou palavra:", key="e_search")
    if search:
        results = [l for l in lexico if search.lower() in l.lower()]
        st.write(f"**{len(results)} ocorrências encontradas no léxico.**")
        for r in results[:100]:
            st.text(f"  › {r}")

def page_poly():
    nav_menu()
    st.write("### 🌍 POLYGLOT (LABORATÓRIO)")
    script = gera_poema(st.session_state.tema, "")
    orig = "\n".join(script)
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown(f"**Original (PT):**\n\n{orig.replace('\n', '<br>')}", unsafe_allow_html=True)
    with col_p2:
        t_lang = st.selectbox("Selecione o prisma de tradução:", ["en", "es", "it", "fr", "ca", "de"])
        res = translate(orig, t_lang)
        st.markdown(f"**Versão ({t_lang}):**\n\n{res.replace('\n', '<br>')}", unsafe_allow_html=True)

def page_books():
    nav_menu()
    st.write("### 📚 BOOKS (SISTEMA DE ROLS)")
    # Listagem real dos arquivos de base ativos
    if os.path.exists("base/ativos.txt"):
        with open("base/ativos.txt", "r", encoding="utf-8") as f:
            ativos = [a.strip() for a in f.readlines() if a.strip()]
            for i, a in enumerate(ativos):
                st.write(f"{i+1:02d}. 📖 **{a}**")

def page_help():
    nav_menu()
    st.write("### ❓ MANUAL DE OPERAÇÃO")
    if os.path.exists("base/helpers.txt"):
        with open("base/helpers.txt", "r", encoding="utf-8") as f:
            st.markdown(f.read())
    else:
        st.warning("Arquivo helpers.txt não localizado na pasta base.")

def page_about():
    nav_menu()
    st.write("### ℹ️ ABOUT")
    st.markdown("""
    **A Máquina de Fazer Poesia** Uma arquitetura de Fernando Lopes fundamentada em trilhões de variações linguísticas.  
    *O esmero está no detalhe.*
    """)

# =================================================================
# 🏰 SIDEBAR (PORTAL DE CONTROLES)
# =================================================================

with st.sidebar:
    st.write("### a máquina de fazer Poesia")
    st.write("---")
    langs = ["pt", "es", "it", "fr", "en", "ca"]
    c = st.columns(len(langs))
    for i, l in enumerate(langs):
        if c[i].button(l if l != "ca" else "⚒️"): st.session_state.lang = l
    st.write("---")
    st.session_state.draw = 'Y' if st.checkbox("Art", value=(st.session_state.draw == 'Y')) else 'N'
    st.session_state.talk = 'Y' if st.checkbox("Talk", value=(st.session_state.talk == 'Y')) else 'N'
    st.session_state.vydo = 'Y' if st.checkbox("Video", value=(st.session_state.vydo == 'Y')) else 'N'
    st.write("---")
    st.markdown("<nav><a href='#'>facebook</a> | <a href='#'>instagram</a></nav>", unsafe_allow_html=True)

# =================================================================
# 🏁 ROTEADOR INTEGRAL
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
