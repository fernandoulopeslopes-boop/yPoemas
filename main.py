import os
import io
import re
import time
import random
import base64
import datetime
import streamlit as st
import socket
from gtts import gTTS
from collections import deque

# Project Module
from lay_2_ypo import gera_poema

### bof: settings

st.set_page_config(
    page_title='yPoemas - a "machina" de fazer Poesia',
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# Tenta importar o tradutor de forma segura
try:
    from deep_translator import GoogleTranslator
except ImportError:
    st.warning("Google Translator não conectado.")

# --- INICIALIZAÇÃO DE ESTADO (Crucial para evitar tela branca) ---
def init_state():
    defaults = {
        "lang": "pt", "last_lang": "pt", "book": "livro vivo",
        "take_tema": 0, "poly_lang": "ca", "poly_name": "català",
        "poly_take": 12, "poly_file": "poly_pt.txt", "visy": True,
        "nany_visy": 0, "find_word": "amor", "draw": False,
        "talk": False, "arts": []
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()

# the User IP para LYPO/TYPO
hostname = socket.gethostname()
user_id = socket.gethostbyname(hostname)

# CSS para Sidebar e Estética
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { width: 310px !important; }
    mark { background-color: lightblue; color: black; }
    .logo-text { font-weight: 700; font-size: 18px; font-family: 'IBM Plex Sans'; padding-left: 15px; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True
)

### bof: loaders (Atualizados para st.cache_data)

@st.cache_data
def load_file(file):
    try:
        with open(os.path.join("./md_files/" + file), encoding="utf-8") as f:
            return f.read()
    except:
        return "Erro ao carregar arquivo."

@st.cache_data
def load_temas(book):
    try:
        with open(os.path.join("./base/" + book + ".rol"), "r", encoding="utf-8") as file:
            return [line.strip("\n") for line in file]
    except:
        return ["erro-ao-carregar"]

def load_poema(nome_tema, seed_eureka):
    script = gera_poema(nome_tema, seed_eureka)
    novo_ypoema = ""
    lypo_user = f"LYPO_{user_id}"
    
    # Salva cópia local para persistência na sessão
    with open(os.path.join("./temp/", lypo_user), "w", encoding="utf-8") as save_lypo:
        save_lypo.write(f"{nome_tema}\n")
        for line in script:
            clean_line = line.strip()
            save_lypo.write(f"{clean_line}\n")
            novo_ypoema += f"{clean_line}<br>"
    return novo_ypoema

### bof: functions

def write_ypoema(LOGO_TEXT, LOGO_IMAGE="none"):
    if LOGO_IMAGE == "none":
        st.markdown(f'<p class="logo-text">{LOGO_TEXT}</p>', unsafe_allow_html=True)
    else:
        # Tenta carregar a imagem da Machina
        try:
            with open(LOGO_IMAGE, "rb") as img_file:
                b64 = base64.b64encode(img_file.read()).decode()
            st.markdown(
                f'<div style="display:flex"><img src="data:image/jpg;base64,{b64}" width="150"><p class="logo-text">{LOGO_TEXT}</p></div>',
                unsafe_allow_html=True
            )
        except:
            st.markdown(f'<p class="logo-text">{LOGO_TEXT}</p>', unsafe_allow_html=True)

### bof: pages

def page_ypoemas():
    st.sidebar.info("Gerador de Poemas Únicos")
    
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list) - 1
    
    col1, col2, col3 = st.columns([1,1,1])
    if col2.button("✴ Gerar Novo", help="Cria uma combinação inédita"):
        st.session_state.take_tema = random.randint(0, maxy)
        
    curr_tema = temas_list[st.session_state.take_tema]
    
    with st.expander(f"Poema: {curr_tema}", expanded=True):
        poema = load_poema(curr_tema, "")
        write_ypoema(poema)

def main():
    pages = {
        "yPoemas": page_ypoemas,
        "about": lambda: st.write(load_file("INFO_ABOUT.md")),
    }
    
    page = st.sidebar.selectbox("Menu Principal", tuple(pages.keys()))
    pages[page]()

if __name__ == "__main__":
    main()
