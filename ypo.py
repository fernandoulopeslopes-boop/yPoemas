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

# REGRA 0: Resgate da Harmonia e Tamanhos Originais
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    /* Ajuste de Padding Geral */
    .reportview-container .main .block-container{ padding: 0rem; }
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child { width: 310px; }
    
    /* Botões menores e harmônicos */
    .stButton>button {
        width: auto;
        padding: 2px 10px;
        height: 28px;
        font-size: 14px;
    }
    
    /* Customização dos botões de navegação no topo */
    .nav-btn {
        margin-top: -20px;
    }
    
    mark { background-color: powderblue; color: black; }
    .container { display: flex; }
    .logo-text {
        font-weight: 600; font-size: 18px;
        font-family: 'IBM Plex Sans'; color: #000000;
        padding-left: 15px;
    }
    </style> """,
    unsafe_allow_html=True,
)

if "lang" not in st.session_state: st.session_state.lang = "pt"
if "page" not in st.session_state: st.session_state.page = "mini"

### bof: sidebar (Idiomas e Temas com tamanho controlado)

with st.sidebar:
    st.markdown("### idiomas")
    # Colunas estreitas para evitar botões gigantes
    c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 1, 1, 1, 1])
    if c1.button("pt"): st.session_state.lang = "pt"
    if c2.button("es"): st.session_state.lang = "es"
    if c3.button("it"): st.session_state.lang = "it"
    if c4.button("fr"): st.session_state.lang = "fr"
    if c5.button("en"): st.session_state.lang = "en"
    if c6.button("⚒️"): st.session_state.lang = "poly"

    st.markdown("---")
    st.markdown("### temas")
    # Simulação dos temas (que também devem ser pequenos)
    t_col1, t_col2 = st.columns(2)
    if t_col1.button("Fatos"): st.session_state.tema = "Fatos"
    if t_col2.button("Amor"): st.session_state.tema = "Amor"

### bof: navigation (Abas de Navegação no Topo - Regras 1 e 2)

# Proporções exatas para os botões não ficarem "invisíveis" ou espalhados
cols = st.columns([1, 1.2, 1, 1.3, 1, 1])

if cols[0].button("mini"): st.session_state.page = "mini"
if cols[1].button("ypoemas"): st.session_state.page = "ypoemas"
if cols[2].button("eureka"): st.session_state.page = "eureka"
if cols[3].button("biblioteca"): st.session_state.page = "biblioteca"
if cols[4].button("oficina"): st.session_state.page = "oficina"
if cols[5].button("sobre"): st.session_state.page = "sobre"

st.markdown("---")

### bof: pages (Regra 3)

if st.session_state.page == "mini":
    st.subheader("ツ mini")
    st.info("Aprovada !!! go'in to next")
elif st.session_state.page == "ypoemas":
    st.subheader("ツ ypoemas")
    st.write("Em estudo...")
else:
    st.subheader(f"ツ {st.session_state.page}")
    st.warning("Under Construction")
