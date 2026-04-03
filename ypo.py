import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime
from lay_2_ypo import gera_poema

# Configuração da Página
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# REGRA 0: CSS Anti-Gigantismo (O "Remédio" para o layout)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child { width: 310px; }
    
    /* Forçar botões pequenos e harmônicos */
    button {
        height: 28px !important;
        padding: 0px 8px !important;
        font-size: 14px !important;
        width: auto !important;
        min-width: 40px !important;
    }
    
    /* Impedir que os botões de idioma estiquem */
    [data-testid="stHorizontalBlock"] {
        align-items: center;
    }
    </style> """,
    unsafe_allow_html=True,
)

# Inicialização de Variáveis (Session State)
if "lang" not in st.session_state: st.session_state.lang = "pt"
if "page" not in st.session_state: st.session_state.page = "mini"
if "tema" not in st.session_state: st.session_state.tema = "Fatos"

# --- SIDEBAR: IDIOMAS ---
with st.sidebar:
    st.write("### idiomas")
    # Usando 6 colunas para garantir que os botões fiquem pequenos
    c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 1, 1, 1, 1])
    if c1.button("pt"): st.session_state.lang = "pt"
    if c2.button("es"): st.session_state.lang = "es"
    if c3.button("it"): st.session_state.lang = "it"
    if c4.button("fr"): st.session_state.lang = "fr"
    if c5.button("en"): st.session_state.lang = "en"
    if c6.button("⚒️"): st.session_state.lang = "ca"

    st.markdown("---")
    st.write("### temas")
    # Exemplo de botões de tema também pequenos
    t1, t2 = st.columns(2)
    if t1.button("Amor"): st.session_state.tema = "Amor"
    if t2.button("Fatos"): st.session_state.tema = "Fatos"

# --- NAVEGAÇÃO SUPERIOR (Ordem do Manual) ---
# Criando as "Abas" com botões horizontais
n1, n2, n3, n4, n5, n6 = st.columns(6)
if n1.button("mini"): st.session_state.page = "mini"
if n2.button("ypo"): st.session_state.page = "ypoemas"
if n3.button("eur"): st.session_state.page = "eureka"
if n4.button("bib"): st.session_state.page = "biblioteca"
if n5.button("ofic"): st.session_state.page = "oficina"
if n6.button("sob"): st.session_state.page = "sobre"

st.markdown("---")

# --- LÓGICA DAS PÁGINAS ---
if st.session_state.page == "mini":
    st.subheader(f"ツ mini - {st.session_state.tema}")
    # Aqui chama a sua função de gerar poema
    # texto = gera_poema(st.session_state.tema, "")
    # st.write(texto)
    st.info("Página Mini ativa.")

elif st.session_state.page == "ypoemas":
    st.subheader("ツ ypoemas")
    st.write("Seção de poemas completos.")

else:
    st.subheader(f"ツ {st.session_state.page}")
    st.write("Em desenvolvimento...")
