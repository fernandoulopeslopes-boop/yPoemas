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

# Inicialização do Estado
if "page" not in st.session_state: 
    st.session_state.page = "mini"

# Regra 0: Look & Feel (Estética Phenix)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .main .block-container { max-width: 98% !important; padding-top: 1.5rem; }
    
    /* Blindagem contra Fullscreen e Toolbar */
    [data-testid="stImage"] button, [data-testid="stElementToolbar"] { display: none !important; }
    [data-testid="stImage"] img { pointer-events: none; }

    /* Estilo da Sidebar */
    [data-testid="stSidebar"] { width: 280px !important; background-color: #fafafa; }
    
    /* Cabeçalhos em minúsculo (estilo ypo) */
    .sidebar-header {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        color: #888;
        margin-top: 20px;
        margin-bottom: 5px;
        text-transform: lowercase;
    }

    /* Botões de Navegação */
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-wrap: nowrap !important; gap: 12px !important; }
    [data-testid="column"] { flex: 0 0 auto !important; width: 125px !important; }
    div.stButton > button {
        width: 120px !important; border-radius: 12px; height: 3.2em;
        background-color: #ffffff; border: 1px solid #d1d5db; font-size: 13px;
    }
    div.stButton > button:hover { border-color: powderblue; color: powderblue; }
    </style> """,
    unsafe_allow_html=True,
)

### bof: navigation (Trilho)

nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
labels = ["ツ mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]

for i in range(6):
    with nav_cols[i]:
        if st.button(labels[i], key=f"btn_nav_{paginas[i]}"):
            st.session_state.page = paginas[i]
            st.rerun()

st.markdown("---")

### bof: sidebar (O Novo Painel Minimalista)

# 1. Definição do Mapeamento (AGORA ANTES DO USO)
mapeamento_artes = {
    "mini": "img_mini.jpg",
    "ypoemas": "img_ypoemas.jpg",
    "eureka": "img_eureka.jpg",
    "off-machina": "img_off-machina.jpg",
    "comments": "img_poly.jpg",
    "sobre": "img_about.jpg"
}

# 2. Imagem Identitária
arte_atual = mapeamento_artes.get(st.session_state.page)
if arte_atual and os.path.exists(arte_atual):
    st.sidebar.image(arte_atual, use_container_width=True)

# 3. Idiomas
st.sidebar.markdown("<div class='sidebar-header'>idiomas</div>", unsafe_allow_html=True)
st.sidebar.selectbox(
    "label_hidden",
    ["Português", "English", "Français", "Español", "Italiano"],
    key="sel_lang",
    label_visibility="collapsed"
)

# 4. Recursos
st.sidebar.markdown("<div class='sidebar-header'>recursos</div>", unsafe_allow_html=True)
st.session_state.audio_on = st.sidebar.checkbox("🎙️ voz (talk)", value=True)
st.session_state.draw_on = st.sidebar.checkbox("🎨 arte (draw)", value=True)

# 5. Conexões (Exemplo de Redes Sociais)
st.sidebar.markdown("<div class='sidebar-header'>conexões</div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="display: flex; gap: 15px; font-size: 18px; padding-left: 5px;">
    <a href="#" style="text-decoration: none;">📸</a>
    <a href="#" style="text-decoration: none;">🐙</a>
    <a href="#" style="text-decoration: none;">✉️</a>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("Phenix Machina 2026")

### bof: pages

if st.session_state.page == "mini":
    st.subheader("ツ mini")
    st.write("O Palco está limpo. Sidebar configurada com drop-down e sem títulos redundantes.")
else:
    st.subheader(f"ツ {st.session_state.page}")
    st.write("Aguardando montagem do cenário...")
