# =================================================================
# 🚀 PAI: MACHINA DE FAZER POESIA (CONSOLIDADO & LIMPO)
# =================================================================
import streamlit as st
import os
import re
import random
import time
import socket
import base64
import asyncio
from datetime import datetime
from PIL import Image
from deep_translator import GoogleTranslator
import edge_tts
from lay_2_ypo import gera_poema

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(
    page_title="a Machina de fazer Poesia",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INICIALIZAÇÃO BLINDADA
if "initialized" not in st.session_state:
    st.session_state.lang = 'pt'
    st.session_state.last_lang = 'pt'
    st.session_state.tema = 'Fatos'
    st.session_state.book = 'livro vivo'
    st.session_state.take = 0
    st.session_state.talk = 'N'
    st.session_state.draw = 'Y'
    st.session_state.page = 'yPoemas'
    st.session_state.initialized = 'Y'

# 3. ESTILIZAÇÃO (CSS)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 310px;
    }
    .logo-text {
        font-weight: 600;
        font-size: 18px;
        font-family: 'IBM Plex Sans', sans-serif;
        color: #000000;
        padding-left: 15px;
        text-align: left;
        display: block;
        line-height: 1.6;
        white-space: pre-wrap !important;
    }
    .logo-img {
        float: right;
        max-width: 300px;
        margin-left: 15px;
    }
    .stButton > button {
        width: 100%;
        text-align: left;
        border: none;
        background: transparent;
        padding: 5px 15px;
    }
    </style> """,
    unsafe_allow_html=True,
)

# --- FUNÇÕES DE SUPORTE (ORIGINAIS) ---

def pick_lang():
    btn_pt, btn_es, btn_it, btn_fr, btn_en, btn_xy = st.sidebar.columns([1, 1, 1, 1, 1, 1])
    if btn_pt.button("pt"): st.session_state.lang = "pt"
    if btn_es.button("es"): st.session_state.lang = "es"
    if btn_it.button("it"): st.session_state.lang = "it"
    if btn_fr.button("fr"): st.session_state.lang = "fr"
    if btn_en.button("en"): st.session_state.lang = "en"
    if btn_xy.button("⚒️"): st.session_state.lang = "ca"

def show_icons():
    st.sidebar.markdown(
        "<nav><a href='https://www.facebook.com/nandoulopes' target='_blank'>• facebook</a> | "
        "<a href='mailto:lopes.fernando@hotmail.com' target='_blank'>e-mail</a> | "
        "<a href='https://www.instagram.com/fernando.lopes.942/' target='_blank'>instagram</a></nav>",
        unsafe_allow_html=True
    )

def talk_fala(text):
    text_clean = text.replace("<br>", " ")
    voices = {"pt": "pt-BR-AntonioNeural", "en": "en-US-GuyNeural", "es": "es-ES-AlvaroNeural"}
    selected_voice = voices.get(st.session_state.lang, "pt-BR-AntonioNeural")
    async def generate_audio():
        communicate = edge_tts.Communicate(text_clean, selected_voice)
        audio_bytes = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio": audio_bytes += chunk["data"]
        return audio_bytes
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_output = loop.run_until_complete(generate_audio())
        st.audio(audio_output, format="audio/mp3")
    except: pass

def write_ypoema(text, img):
    if img and os.path.exists(img):
        with open(img, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"<div class='container'><img class='logo-img' src='data:image/jpg;base64,{img_b64}'><p class='logo-text'>{text}</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p class='logo-text'>{text}</p>", unsafe_allow_html=True)

# --- PÁGINAS ---

def page_ypoemas():
    st.write(f"### {st.session_state.tema}")
    poema = gera_poema(st.session_state.tema, "")
    text_html = "<br>".join(poema)
    write_ypoema(text_html, None)
    if st.session_state.talk == 'Y': talk_fala(text_html)

def page_mini():
    st.write("### Modo Mini")
    st.write("Variações rápidas e automáticas.")

# --- SIDEBAR (O PORTAL) ---

with st.sidebar:
    st.write("### a máquina de fazer Poesia")
    st.write("---")
    pick_lang()
    st.write("---")
    
    # NAVEGAÇÃO LIMPA (Sem radio buttons)
    if st.button("Mini"): st.session_state.page = "Mini"
    if st.button("yPoemas"): st.session_state.page = "yPoemas"
    if st.button("Eureka"): st.session_state.page = "Eureka"
    
    st.write("---")
    # CONTROLES (Sem selectboxes de temas)
    st.session_state.draw = 'Y' if st.checkbox("Art", value=(st.session_state.draw == 'Y')) else 'N'
    st.session_state.talk = 'Y' if st.checkbox("Talk", value=(st.session_state.talk == 'Y')) else 'N'
    
    st.write("---")
    show_icons()

# --- EXECUÇÃO PRINCIPAL ---
if st.session_state.page == "yPoemas":
    page_ypoemas()
elif st.session_state.page == "Mini":
    page_mini()
elif st.session_state.page == "Eureka":
    st.info("Eureka em construção.")
