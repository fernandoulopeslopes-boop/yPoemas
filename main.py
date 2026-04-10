import os
import io
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime
from lay_2_ypo import gera_poema

# --- Settings ---

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

@st.cache_data
def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

# CSS Original: Sidebar 300px e Estética de Leitura
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 300px;
    }
    .poema-container {
        font-family: 'serif';
        font-size: 1.35rem;
        line-height: 1.6;
        color: #1a1a1a;
        padding: 20px;
    }
    </style> """,
    unsafe_allow_html=True,
)

# --- Help System (PAI: Help_Listers) ---

@st.cache_data
def load_helpers():
    """Carrega o dicionário de labels do arquivo helpers.txt."""
    h_dict = {}
    if os.path.exists("./base/helpers.txt"):
        with open("./base/helpers.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split("|")
                if len(parts) > 2:
                    # Chave: pt_1, en_5, etc.
                    h_dict[parts[1].strip()] = parts[2].strip()
    return h_dict

def get_h(key_index):
    """Busca o termo baseado no idioma da sessão e no índice solicitado."""
    h_dict = load_helpers()
    search_key = f"{st.session_state.lang}_{key_index}"
    # Fallback caso a chave não exista no dicionário
    return h_dict.get(search_key, f"Label_{key_index}")

# --- Session State ---

if "lang" not in st.session_state: st.session_state.lang = "pt"
if "book" not in st.session_state: st.session_state.book = "livro vivo"
if "tema" not in st.session_state: st.session_state.tema = "Fatos"
if "take" not in st.session_state: st.session_state.take = 0
if "draw" not in st.session_state: st.session_state.draw = False
if "talk" not in st.session_state: st.session_state.talk = False

# --- Sidebar (Portal à Esquerda) ---

def build_sidebar():
    with st.sidebar:
        st.write("### a máquina de fazer Poesia")
        
        # 1. pick_lang (6 colunas)
        st.write("---")
        c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 1, 1, 1, 1])
        if c1.button("pt"): st.session_state.lang = "pt"
        if c2.button("es"): st.session_state.lang = "es"
        if c3.button("it"): st.session_state.lang = "it"
        if c4.button("fr"): st.session_state.lang = "fr"
        if c5.button("en"): st.session_state.lang = "en"
        if c6.button("⚒️"): st.session_state.lang = "poly"
        
        st.write("---")
        
        # 2. Navegação (Mini, yPoemas, Eureka)
        page = st.radio("", ["Mini", "yPoemas", "Eureka"], 
                        index=1, label_visibility="collapsed")
        
        # 3. Contexto (Apenas para yPoemas)
        if page == "yPoemas":
            st.session_state.book = st.selectbox("", ["livro vivo", "todos os temas"], label_visibility="collapsed")
            st.session_state.tema = st.selectbox("", ["Fatos", "Amor", "Morte"], label_visibility="collapsed")
        
        st.write("---")
        
        # 4. Sentidos (Labels dinâmicos do PAI: 4=Art, 5=Talk)
        st.session_state.draw = st.checkbox(get_h(4), value=st.session_state.draw)
        st.session_state.talk = st.checkbox(get_h(5), value=st.session_state.talk)
        
        st.write("---")
        
        # 5. Rodapé
        st.write("✨ 📚 ✉️ ☕")
        st.checkbox(get_h(6), value=False) # Show Readings
        if st.button(get_h(7)):            # Share
            st.toast("Link copiado!")

        return page

# --- Página yPoemas (Elemento Central) ---

def show_ypoemas():
    # Navegação superior: Anterior(0), Acaso(1), Próximo(2), Ajuda(3)
    n1, n2, n3, n4 = st.columns([1, 1, 1, 1])
    if n1.button(f"⬅️ {get_h(0)}"): st.session_state.take -= 1
    if n2.button(f"🎲 {get_h(1)}"): st.session_state.take = random.randint(0, 999)
    if n3.button(f"➡️ {get_h(2)}"): st.session_state.take += 1
    with n4:
        with st.expander(get_h(3)):
            st.write("Instruções de uso da Machina.")

    st.write("---")

    # Geração via lay_2_ypo
    poema_raw = gera_poema(st.session_state.tema, "")
    poema_html = "<br>".join(poema_raw)

    # Exibição: Texto e Imagem (Western Layout)
    if st.session_state.draw:
        col_t, col_i = st.columns([1.6, 1])
        with col_t:
            st.markdown(f"<div class='poema-container'>{poema_html}</div>", unsafe_allow_html=True)
        with col_i:
            st.image("https://via.placeholder.com/400x600.png?text=Art", use_container_width=True)
    else:
        st.markdown(f"<div class='poema-container'>{poema_html}</div>", unsafe_allow_html=True)

# --- Execução Principal ---

def main():
    current_page = build_sidebar()
    
    if current_page == "yPoemas":
        show_ypoemas()
    elif current_page == "Mini":
        st.info("Página Mini")
    elif current_page == "Eureka":
        st.info("Página Eureka")

if __name__ == "__main__":
    main()
