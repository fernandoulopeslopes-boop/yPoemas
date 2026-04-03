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

# Inicialização de Estados
if "page" not in st.session_state: st.session_state.page = "mini"
if "poly_lang" not in st.session_state: st.session_state.poly_lang = "ca"
if "poly_name" not in st.session_state: st.session_state.poly_name = "català"

# Dicionário de Help Tips (Cockpit Sensível ao Idioma)
help_dict = {
    "Português": "escolha como a machina deve atuar",
    "English": "choose how the machine should act",
    "Français": "choisissez comment la machine deve agir",
    "Español": "elige cómo deve actuar la máquina",
    "Italiano": "scegli come deve agire la macchina",
    st.session_state.poly_name: "tria com ha d'actuar la màquina"
}

# Regra 0: Look & Feel (Ajuste de 112px)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .main .block-container { max-width: 98% !important; padding-top: 1.5rem; }
    
    /* Blindagem e Limpeza */
    [data-testid="stImage"] button, [data-testid="stElementToolbar"] { display: none !important; }
    [data-testid="stImage"] img { pointer-events: none; }

    /* Estilo da Sidebar */
    [data-testid="stSidebar"] { width: 280px !important; background-color: #fafafa; }
    
    .sidebar-header {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        color: #888;
        margin-top: 15px;
        margin-bottom: 5px;
        text-transform: lowercase;
    }

    /* Navegação - Ajuste para 112px (O Equilíbrio) */
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-wrap: nowrap !important; gap: 8px !important; }
    [data-testid="column"] { flex: 0 0 auto !important; width: 115px !important; }
    
    div.stButton > button {
        width: 112px !important; 
        border-radius: 12px; 
        height: 3.2em;
        background-color: #ffffff; 
        border: 1px solid #d1d5db; 
        font-size: 12px; /* Redução leve na fonte para ajudar no encaixe */
    }
    div.stButton > button:hover { border-color: powderblue; color: powderblue; }
    </style> """,
    unsafe_allow_html=True,
)

### bof: navigation (O Trilho de 112px)

nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
labels = ["ツ mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]

for i in range(6):
    with nav_cols[i]:
        if st.button(labels[i], key=f"btn_nav_{paginas[i]}"):
            st.session_state.page = paginas[i]
            st.rerun()

st.markdown("---")

### bof: sidebar (O Cockpit Limpo)

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

# 1. Idiomas (Sem título, apenas o seletor)
lista_idiomas = ["Português", "English", "Français", "Español", "Italiano", st.session_state.poly_name]
sel_idioma = st.sidebar.selectbox(
    "idioma_selector",
    lista_idiomas,
    key="sel_lang",
    label_visibility="collapsed"
)

# 2. Recursos (Com Help Tip dinâmico)
current_help = help_dict.get(sel_idioma, help_dict["Português"])

st.sidebar.markdown("<div class='sidebar-header'>recursos</div>", unsafe_allow_html=True)
st.session_state.audio_on = st.sidebar.checkbox("🎙️ voz (talk)", value=True, help=current_help)
st.session_state.draw_on = st.sidebar.checkbox("🎨 arte (draw)", value=True, help=current_help)

# 3. Conexões
st.sidebar.markdown("<div class='sidebar-header'>conexões</div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="display: flex; gap: 15px; font-size: 18px; padding-left: 5px;">
    <a href="#" style="text-decoration: none;">📸</a>
    <a href="#" style="text-decoration: none;">🐙</a>
    <a href="#" style="text-decoration: none;">✉️</a>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption(f"Phenix Machina | {st.session_state.page}")

### bof: pages

if st.session_state.page == "mini":
    st.subheader("ツ mini")
    st.write(f"Cockpit configurado. {current_help.capitalize()}.")
else:
    st.subheader(f"ツ {st.session_state.page}")
    st.write("Cenário em espera.")
