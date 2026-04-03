import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime
from lay_2_ypo import gera_poema

### bof: settings

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# REGRA 0: CSS Corretivo Anti-Gigantismo (Forçando a Harmonia)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .reportview-container .main .block-container{ padding: 0rem; }
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child { width: 310px; }
    
    /* FORÇAR BOTÕES PEQUENOS */
    div.stButton > button {
        width: 60px !important;
        height: 30px !important;
        padding: 0px !important;
        font-size: 14px !important;
        line-height: 1 !important;
        min-width: 60px !important;
    }

    /* Ajuste específico para os botões de navegação do topo (maiores que os de idioma) */
    .nav-container div.stButton > button {
        width: 100px !important;
    }

    mark { background-color: powderblue; color: black; }
    </style> """,
    unsafe_allow_html=True,
)

if "lang" not in st.session_state: st.session_state.lang = "pt"
if "page" not in st.session_state: st.session_state.page = "mini"

### bof: sidebar (Idiomas e Temas - REGRA: TAMANHO CONTROLADO)

with st.sidebar:
    st.write("### idiomas")
    # Usamos muitas colunas vazias para "empurrar" os botões para a esquerda e mantê-los pequenos
    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1])
    if c1.button("pt"): st.session_state.lang = "pt"
    if c2.button("en"): st.session_state.lang = "en"
    # c3, c4, c5 ficam vazios para não deixar os dois primeiros crescerem

    st.markdown("---")
    st.write("### temas")
    t1, t2, t3 = st.columns([1, 1, 1])
    if t1.button("Fatos"): st.session_state.tema = "Fatos"
    if t2.button("Amor"): st.session_state.tema = "Amor"

### bof: navigation (Abas de Navegação no Topo)

st.markdown('<div class="nav-container">', unsafe_allow_html=True)
cols = st.columns([1, 1, 1, 1, 1, 1])

if cols[0].button("mini"): st.session_state.page = "mini"
if cols[1].button("ypo"): st.session_state.page = "ypoemas"
if cols[2].button("eur"): st.session_state.page = "eureka"
if cols[3].button("bib"): st.session_state.page = "biblioteca"
if cols[4].button("ofic"): st.session_state.page = "oficina"
if cols[5].button("sob"): st.session_state.page = "sobre"
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

### bof: pages

if st.session_state.page == "mini":
    st.subheader("ツ mini")
    st.info("Aprovada !!! go'in to next")
elif st.session_state.page == "ypoemas":
    st.subheader("ツ ypoemas")
    st.write("Em estudo...")
else:
    st.subheader(f"ツ {st.session_state.page}")
    st.write("Under Construction")
