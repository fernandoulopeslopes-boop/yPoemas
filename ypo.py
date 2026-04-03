import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime
from lay_2_ypo import gera_poema

# Configurações de Página
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# CSS Corretivo (Botões e Layout)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .reportview-container .main .block-container{ padding: 0rem; }
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child { width: 310px; }
    
    /* Forçar botões pequenos */
    div.stButton > button {
        width: auto !important;
        min-width: 45px !important;
        height: 28px !important;
        padding: 0px 8px !important;
        font-size: 13px !important;
    }
    
    mark { background-color: powderblue; color: black; }
    .logo-text {
        font-weight: 600; font-size: 18px;
        font-family: 'IBM Plex Sans'; color: #000000;
        padding-left: 15px;
    }
    </style> """,
    unsafe_allow_html=True,
)

# Inicialização de SessionState
if "lang" not in st.session_state: st.session_state.lang = "pt"
if "page" not in st.session_state: st.session_state.page = "mini"
if "tema" not in st.session_state: st.session_state.tema = "Fatos"
if "visy" not in st.session_state: st.session_state.visy = True

# --- SIDEBAR: Idiomas ---
with st.sidebar:
    st.write("### idiomas")
    c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 1, 1, 1, 1])
    if c1.button("pt"): st.session_state.lang = "pt"
    if c2.button("es"): st.session_state.lang = "es"
    if c3.button("it"): st.session_state.lang = "it"
    if c4.button("fr"): st.session_state.lang = "fr"
    if c5.button("en"): st.session_state.lang = "en"
    if c6.button("⚒️"): st.session_state.lang = "ca"
    st.markdown("---")

# --- NAVEGAÇÃO: Menu Superior ---
n1, n2, n3, n4, n5, n6 = st.columns(6)
if n1.button("mini"): st.session_state.page = "mini"
if n2.button("ypoemas"): st.session_state.page = "ypoemas"
if n3.button("eureka"): st.session_state.page = "eureka"
if n4.button("biblioteca"): st.session_state.page = "biblioteca"
if n5.button("oficina"): st.session_state.page = "oficina"
if n6.button("sobre"): st.session_state.page = "sobre"
st.markdown("---")

# --- LÓGICA DE PÁGINAS ---
if st.session_state.page == "mini":
    st.subheader(f"ツ mini - {st.session_state.tema}")
    # Gerar Poema
    curr_ypoema = gera_poema(st.session_state.tema, "")
    st.write(curr_ypoema)

elif st.session_state.page == "ypoemas":
    st.subheader("ツ ypoemas")
    st.write("Conteúdo da página ypoemas...")

else:
    st.subheader(f"ツ {st.session_state.page}")
    st.write("Página em desenvolvimento.")
