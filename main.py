import os
import io
import re
import time
import random
import base64
import datetime
import socket
import streamlit as st
from gtts import gTTS
from collections import deque

# Project Module
try:
    from lay_2_ypo import gera_poema
except ImportError:
    st.error("Módulo 'lay_2_ypo' não encontrado. Verifique o arquivo no diretório.")

# --- 1. ENGENHARIA DE ESTADO (BOF) ---
# Garante que todas as variáveis de controle existam antes da renderização
def init_session_state():
    defaults = {
        "lang": "pt", 
        "last_lang": "pt", 
        "book": "livro vivo",
        "take_tema": 0, 
        "poly_lang": "ca", 
        "poly_name": "català",
        "poly_take": 12, 
        "poly_file": "poly_pt.txt", 
        "visy": True,
        "nany_visy": 0, 
        "find_word": "amor",
        "draw": False, 
        "talk": False, 
        "arts": []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()
# --- EOF ENGENHARIA DE ESTADO ---

# --- 2. CONFIGURAÇÕES E ESTILO ---
st.set_page_config(
    page_title='yPoemas - a "machina" de fazer Poesia',
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# Hostname e IP para registros
hostname = socket.gethostname()
user_id = socket.gethostbyname(hostname)

# CSS para Sidebar e Layout
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { width: 310px !important; }
    .logo-text { font-weight: 700; font-size: 18px; font-family: 'IBM Plex Sans'; color: #000000; padding-left: 15px; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. FERRAMENTAS E LOADERS (CORE) ---
@st.cache_data
def load_file(file): 
    try:
        with open(os.path.join("./md_files/" + file), encoding="utf-8") as f:
            return f.read()
    except:
        return f"Erro: {file} não encontrado."

@st.cache_data
def load_temas(book):
    try:
        with open(os.path.join("./base/" + book + ".rol"), "r", encoding="utf-8") as file:
            return [line.strip("\n") for line in file]
    except:
        return ["erro-ao-carregar"]

# --- 4. FUNÇÕES DE PÁGINA (ORIGINAIS) ---
def page_mini():
    # Lógica original da página mini...
    st.subheader("mini")
    # ... (restante do código original)

def page_ypoemas():
    # Lógica original da página yPoemas...
    st.subheader("yPoemas")
    # ... (restante do código original)

def page_eureka():
    st.subheader("eureka")
    # ...

def page_off_machina():
    st.subheader("off-machina")
    # ...

def page_polys():
    st.subheader("poly")
    # ...

def page_books():
    st.subheader("books")
    # ...

def page_abouts():
    st.subheader("about")
    # ...

# --- 5. EXECUÇÃO PRINCIPAL (MAIN) ---
def main():
    # Mapeamento de navegação
    pages = {
        "mini": page_mini,
        "yPoemas": page_ypoemas,
        "eureka": page_eureka,
        "off-machina": page_off_machina,
        "poly": page_polys,
        "books": page_books,
        "about": page_abouts,
    }

    # Sidebar Menu
    with st.sidebar:
        page_choice = st.selectbox("menu", tuple(pages.keys()))
        # Chamada de ferramentas da sidebar[cite: 1]
        # pick_lang()
        # show_icons()

    # Renderização da Página Escolhida
    if page_choice in pages:
        pages[page_choice]()

if __name__ == "__main__":
    main()
