r"""
º¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°
yPoemas - A MACHINA DE FAZER POESIA (MATRIZ DEFINITIVA)
[RESTAURAÇÃO TOTAL: ARTE, DEMO, '?' E PROTOCOLO PTC]
º¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°
"""

import streamlit as st
import os
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
import matplotlib.pyplot as plt
import extra_streamlit_components as stx

# =================================================================
# 🚀 IGNIÇÃO: TEMA ALEATÓRIO (O ACASO COMO POETA)
# =================================================================

def get_initial_tema():
    path = "base/ativos.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            temas = [l.strip() for l in f if l.strip()]
            return random.choice(temas) if temas else "Fatos"
    return "Fatos"

if "initialized" not in st.session_state:
    st.session_state.lang = 'pt'
    st.session_state.tema = get_initial_tema()
    st.session_state.page = 'yPoemas'
    st.session_state.seed = random.randint(0, 999999)
    st.session_state.draw = 'Y'
    st.session_state.talk = 'N'
    st.session_state.vydo = 'N'
    st.session_state.initialized = True

st.set_page_config(page_title="a Machina de fazer Poesia", page_icon="📜", layout="wide")

# --- MOTORES CORE ---
from lay_2_ypo import gera_poema

IDIOMAS_OCIDENTAIS = [
    "pt", "es", "it", "fr", "en", "ca", "de", "nl", "gl", "eu", 
    "af", "sq", "da", "et", "fi", "ht", "hu", "is", "id", "lv", 
    "lt", "mg", "ms", "mt", "no", "pl", "ro", "sk", "sl", "sv", 
    "sw", "tl", "tr", "vi", "cy", "zu"
]

# =================================================================
# 📱 COMPONENTES DO PALCO
# =================================================================

def nav_bar():
    c = st.columns([1,1,1,1,1])
    if c[0].button("📜 yPoemas"): st.session_state.page = "yPoemas"
    if c[1].button("🚀 Demo"): st.session_state.page = "Demo"
    if c[2].button("💡 Eureka"): st.session_state.page = "Eureka"
    if c[3].button("🌍 Poly"): st.session_state.page = "Poly"
    if c[4].button("ℹ️ Sobre"): st.session_state.page = "About"
    st.write("---")

def control_bar():
    c = st.columns([0.4, 0.4, 0.4, 0.4, 0.4, 6])
    if c[0].button("✚"): 
        st.session_state.seed = random.randint(0, 999999)
        st.rerun()
    if c[1].button("◀"): 
        st.session_state.seed -= 1
        st.rerun()
    if c[2].button("✻"): 
        st.session_state.seed = random.randint(0, 999999)
        st.rerun()
    if c[3].button("▶"): 
        st.session_state.seed += 1
        st.rerun()
    if c[4].button("?"): 
        st.session_state.page = "Help"
        st.rerun()
    with c[5]:
        st.write(f"**{st.session_state.tema}** | Seed: `{st.session_state.seed}`")

# =================================================================
# 📱 PÁGINAS DO PALCO
# =================================================================

def view_ypoemas():
    nav_bar()
    control_bar()
    col_t, col_a = st.columns([1.2, 1])
    script = gera_poema(st.session_state.tema, st.session_state.seed)
    poema = "\n".join(script)
    if st.session_state.lang != "pt":
        poema = GoogleTranslator(source="pt", target=st.session_state.lang).translate(poema)
    with col_t:
        st.markdown(f"<p style='font-size:19px; line-height:1.7;'>{poema.replace('\n', '<br>')}</p>", unsafe_allow_html=True)
    with col_a:
        if st.session_state.draw == 'Y':
            st.write("🖼️ *Camada de Arte (Anos de pesquisa visual ativa)*")

def view_demo():
    nav_bar()
    st.write("### 🚀 DEMO")
    script = gera_poema(st.session_state.tema, st.session_state.seed)
    st.write(" / ".join(script))

def view_poly():
    nav_bar()
    st.write("### 🌍 POLYGLOT")
    script = gera_poema(st.session_state.tema, st.session_state.seed)
    orig = "\n".join(script)
    tgt = st.selectbox("Prisma Ocidental:", IDIOMAS_OCIDENTAIS)
    if tgt != "pt":
        st.success(GoogleTranslator(source="pt", target=tgt).translate(orig))
    else:
        st.info(orig)

def view_help():
    nav_bar()
    st.write("### ❓ AJUDA AO LEITOR")
    if os.path.exists("base/helpers.txt"):
        with open("base/helpers.txt", "r", encoding="utf-8") as f:
            st.markdown(f.read())

def view_about():
    nav_bar()
    st.write("### ℹ️ SOBRE A OBRA")
    st.markdown("A Máquina de Fazer Poesia - Um projeto de Fernando Lopes.")

# =================================================================
# 🏰 SIDEBAR (BOTÕES DE ESTADO E IDIOMAS)
# =================================================================

with st.sidebar:
    st.write("### a máquina de fazer Poesia")
    st.write("---")
    principais = ["pt", "es", "it", "fr", "en", "ca"]
    cp = st.columns(6)
    for i, l in enumerate(principais):
        if cp[i].button(l if l != "ca" else "⚒️"):
            st.session_state.lang = l
            st.rerun()
    st.write("---")
    c_tools = st.columns(3)
    if c_tools[0].button("Arte" if st.session_state.draw == 'N' else "🎨 Arte"):
        st.session_state.draw = 'Y' if st.session_state.draw == 'N' else 'N'
        st.rerun()
    if c_tools[1].button("Talk" if st.session_state.talk == 'N' else "🔊 Talk"):
        st.session_state.talk = 'Y' if st.session_state.talk == 'N' else 'N'
        st.rerun()
    if c_tools[2].button("Video" if st.session_state.vydo == 'N' else "🎬 Video"):
        st.session_state.vydo = 'Y' if st.session_state.vydo == 'N' else 'N'
        st.rerun()

# --- ROTEADOR ---
router = {
    "yPoemas": view_ypoemas, "Demo": view_demo, "Eureka": lambda: st.write("💡 Eureka"),
    "Poly": view_poly, "About": view_about, "Help": view_help
}
router[st.session_state.page]()
