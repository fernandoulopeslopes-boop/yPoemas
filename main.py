r"""

º¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°

yPoemas - PAI ORIGINAL (INTEGRAL & FUNCIONAL)
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
# 📱 AS PÁGINAS DO PALCO (O TODO)
# =================================================================

def nav_menu():
    """Menu de navegação integrado ao palco, conforme o PAI."""
    c = st.columns([1,1,1,1,1,1,1])
    if c[0].button("yPoemas"): st.session_state.page = "yPoemas"
    if c[1].button("Mini"): st.session_state.page = "Mini"
    if c[2].button("Eureka
