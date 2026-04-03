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
    layout="wide",
    initial_sidebar_state="auto",
)

# Estado da página (MANDALA) - Inicialização Crítica
if "page" not in st.session_state: 
    st.session_state.page = "mini"

# Regra 0: Look & Feel (Foco no Palco Central)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .main .block-container {
        max-width: 95% !important;
        padding-top: 1.5rem;
    }
    [data-testid="stSidebar"] { width: 260px !important; }
    
    /* Botões 100px - Simetria de Painel de Controle */
    div.stButton > button {
        width: 100px !important; 
        border-radius: 12px;
        height: 3.2em;
        background-color: #f8f9fa;
        border: 1px solid #d1d5db;
        transition: all 0.2s ease-in-out;
        font-family: 'IBM Plex Sans';
        font-weight: 500;
        font-size: 12px;
    }
    div.stButton > button:hover {
        border-color: powderblue;
        color: powderblue;
        background-color: white;
    }
    [data-testid="column"] {
        padding: 0 8px !important;
        display: flex;
        justify-content: center;
    }
    </style> """,
    unsafe_allow_html=True,
)

### bof: navigation (O Comando do Palco)
# Processamos o clique ANTES de desenhar a sidebar para atualização instantânea

_, center_col, _ = st.columns([1, 8, 1]) 

with center_col:
    nav_cols = st.columns(6)
    if nav_cols[0].button("ツ mini"): 
        st.session_state.page = "mini"
        st.rerun()
    if nav_cols[1].button("ypoemas"): 
        st.session_state.page = "ypoemas"
        st.rerun()
    if nav_cols[2].button("eureka"): 
        st.session_state.page = "eureka"
        st.rerun()
    if nav_cols[3].button("off-machina"): 
        st.session_state.page = "off-machina"
        st.rerun()
    if nav_cols[4].button("comments"): 
        st.session_state.page = "comments"
        st.rerun()
    if nav_cols[5].button("sobre"): 
        st.session_state.page = "sobre"
        st.rerun()

st.markdown("---")

### bof: sidebar (Bastidores / Configurações)

st.sidebar.title("Configurações")

mapeamento_artes = {
    "mini": "img_mini.jpg",
    "ypoemas": "img_ypoemas.jpg",
    "eureka": "img_eureka.jpg",
    "off-machina": "img_off-machina.jpg",
    "comments": "img_poly.jpg",
    "sobre": "img_about.jpg"
}

arte_atual = mapeamento_artes.get(st.session_state.page)
if arte_atual and os.path.exists(arte_atual):
    st.sidebar.image(arte_atual, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.selectbox("Idioma", ["Português", "English", "Français"], key="sel_lang")
st.sidebar.checkbox("Talk (Áudio)", value=True)
st.sidebar.checkbox("Draw (Imagem)", value=True)

### bof: pages (O Espetáculo)

def page_mini():
    st.subheader("ツ mini")
    st.write("Configurações aplicadas. O palco é seu.")

def page_ypoemas():
    st.subheader("ツ ypoemas")

def page_eureka():
    st.subheader("ツ eureka")

def page_off_machina():
    st.subheader("ツ off-machina")

def page_comments():
    st.subheader("ツ comments")

def page_sobre():
    st.subheader("ツ sobre")

# Router final para carregar a página selecionada
if st.session_state.page == "mini":
    page_mini()
elif st.session_state.page == "ypoemas":
    page_ypoemas()
elif st.session_state.page == "eureka":
    page_eureka()
elif st.session_state.page == "off-machina":
    page_off_machina()
elif st.session_state.page == "comments":
    page_comments()
elif st.session_state.page == "sobre":
    page_sobre()
