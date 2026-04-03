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

if "page" not in st.session_state: st.session_state.page = "mini"

# Regra 0: Look & Feel (Extermínio do Fullscreen e Limpeza Total)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .main .block-container {
        max-width: 98% !important;
        padding-top: 1.5rem;
    }
    
    /* BLOQUEIO TOTAL DO BOTÃO FULLSCREEN E INTERAÇÕES NA IMAGEM */
    [data-testid="stImage"] button, 
    [data-testid="stElementToolbar"],
    .st-emotion-cache-15z78ca button,
    button[title="View fullscreen"] {
        display: none !important;
    }
    
    /* Impede que a imagem mude o cursor ou pareça clicável */
    [data-testid="stImage"] img {
        pointer-events: none;
    }

    /* Ajuste da Sidebar */
    [data-testid="stSidebar"] { 
        width: 280px !important; 
        background-color: #fafafa;
    }
    
    .sidebar-title {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #444;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    /* Navegação */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        gap: 12px !important;
    }

    [data-testid="column"] {
        flex: 0 0 auto !important;
        width: 125px !important;
    }

    div.stButton > button {
        width: 120px !important; 
        border-radius: 12px;
        height: 3.2em;
        background-color: #ffffff;
        border: 1px solid #d1d5db;
        font-size: 13px;
    }
    
    div.stButton > button:hover {
        border-color: powderblue;
        color: powderblue;
    }
    </style> """,
    unsafe_allow_html=True,
)

### bof: navigation

nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
labels = ["ツ mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]

for i in range(6):
    with nav_cols[i]:
        if st.button(labels[i], key=f"btn_nav_{paginas[i]}"):
            st.session_state.page = paginas[i]
            st.rerun()

st.markdown("---")

### bof: sidebar (Painel 100% Estático)

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
    # A imagem agora é puramente visual, sem botões de controle
    st.sidebar.image(arte_atual, use_container_width=True)

st.sidebar.markdown("<div class='sidebar-title'>⚙️ Configurações</div>", unsafe_allow_html=True)

with st.sidebar.expander("🌍 Idioma e Tradução", expanded=True):
    st.selectbox("Selecione o idioma:", ["Português", "English", "Français", "Español", "Italiano"], key="sel_lang")

with st.sidebar.expander("🛠️ Modo de Execução", expanded=True):
    st.session_state.audio_on = st.checkbox("🎙️ Talk (Voz/Áudio)", value=True)
    st.session_state.draw_on = st.checkbox("🎨 Draw (Visual/Arte)", value=True)

st.sidebar.markdown("---")
st.sidebar.caption(f"Fênix Machina | Status: Online")

### bof: pages

if st.session_state.page == "mini":
    st.subheader("ツ mini")
    st.info("A imagem lateral agora deve estar 'blindada' contra o fullscreen.")
else:
    st.subheader(f"ツ {st.session_state.page}")
    st.write("Configurações da sidebar prontas.")
