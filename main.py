import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime

# Se o arquivo lay_2_ypo.py já estiver no seu repositório:
# from lay_2_ypo import gera_poema

### bof: settings

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="wide",
    initial_sidebar_state="auto",
)

# Inicialização de Estados (O Coração da Machina)
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

# Regra 0: Look & Feel (A MANDALA de Estilo)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    
    /* PALCO FLUIDO: Ocupa o espaço quando a sidebar recolhe */
    .main .block-container { 
        max-width: 95% !important; 
        padding-top: 1.5rem; 
        padding-left: 2rem;
        padding-right: 2rem;
        transition: max-width 0.3s ease;
    }
    
    /* BLINDAGEM: Remove Fullscreen e Toolbars de imagens */
    [data-testid="stImage"] button, [data-testid="stElementToolbar"] { display: none !important; }
    [data-testid="stImage"] img { pointer-events: none; }

    /* SIDEBAR: Esguia e Minimalista (240px) */
    [data-testid="stSidebar"] { 
        width: 240px !important; 
        min-width: 240px !important;
        background-color: #fafafa; 
        border-right: 1px solid #eeeeee;
    }
    
    /* CABEÇALHOS: Apenas para Conexões */
    .sidebar-header {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #999;
        margin-top: 20px;
        margin-bottom: 8px;
        text-transform: lowercase;
    }

    /* NAVEGAÇÃO: O Trilho de 116px */
    [data-testid="stHorizontalBlock"] { 
        display: flex !important; 
        flex-wrap: nowrap !important; 
        gap: 8px !important; 
    }
    
    [data-testid="column"] { 
        flex: 0 0 auto !important; 
        width: 120px !important; 
    }
    
    div.stButton > button {
        width: 116px !important; 
        border-radius: 12px; 
        height: 3.2em;
        background-color: #ffffff; 
        border: 1px solid #d1d5db; 
        font-size: 12px;
        transition: 0.2s;
    }
    
    div.stButton > button:hover { 
        border-color: powderblue; 
        color: powderblue; 
        background-color: #f0fbff;
    }
    </style> """,
    unsafe_allow_html=True,
)

### bof: navigation (O Trilho)

nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
labels = ["ツ mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]

for i in range(6):
    with nav_cols[i]:
        if st.button(labels[i], key=f"btn_nav_{paginas[i]}"):
            st.session_state.page = paginas[i]
            st.rerun()

st.markdown("---")

### bof: sidebar (O Cockpit do Piloto)

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

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# 1. Idiomas (O Leitor Descobre)
lista_idiomas = ["Português", "English", "Français", "Español", "Italiano", st.session_state.poly_name]
sel_idioma = st.sidebar.selectbox(
    "idioma_selector",
    lista_idiomas,
    key="sel_lang",
    label_visibility="collapsed"
)

# 2. Recursos (Com Help Tip Dinâmico e Poliglota)
current_help = help_dict.get(sel_idioma, help_dict["Português"])

st.session_state.audio_on = st.sidebar.checkbox("🎙️ voz (talk)", value=True, help=current_help)
st.session_state.draw_on = st.sidebar.checkbox("🎨 arte (draw)", value=True, help=current_help)

# 3. Conexões
st.sidebar.markdown("<div class='sidebar-header'>conexões</div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="display: flex; gap: 18px; font-size: 20px; padding-left: 5px;">
    <a href="#" style="text-decoration: none;">📸</a>
    <a href="#" style="text-decoration: none;">🐙</a>
    <a href="#" style="text-decoration: none;">✉️</a>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption(f"Phenix Machina | {st.session_state.page}")

### bof: pages (O Palco)

if st.session_state.page == "mini":
    st.subheader("ツ mini")
    st.markdown(f"**Modo Poliglota:** {sel_idioma}")
    st.write(f"_{current_help}_")
    
elif st.session_state.page == "ypoemas":
    st.subheader("ツ ypoemas")
    
elif st.session_state.page == "eureka":
    st.subheader("ツ eureka")
    
elif st.session_state.page == "off-machina":
    st.subheader("ツ off-machina")
    
elif st.session_state.page == "comments":
    st.subheader("ツ comments")
    
elif st.session_state.page == "sobre":
    st.subheader("ツ sobre")

st.write("")
