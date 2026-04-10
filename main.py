import os
import random
import base64
import streamlit as st
from lay_2_ypo import gera_poema

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="yPoemas", layout="centered")

st.markdown("""
    <style>
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 300px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR COMPLETA (Fiel ao ypo.py) ---

def build_sidebar():
    with st.sidebar:
        # 1. Título/Logo
        st.write("### a máquina de fazer Poesia")
        
        # 2. Seletor de Idiomas (pick_lang)
        st.write("---")
        c1, c2, c3, c4, c5, c6 = st.columns([1,1,1,1,1,1])
        if c1.button("pt"): st.session_state.lang = "pt"
        if c2.button("es"): st.session_state.lang = "es"
        if c3.button("it"): st.session_state.lang = "it"
        if c4.button("fr"): st.session_state.lang = "fr"
        if c5.button("en"): st.session_state.lang = "en"
        if c6.button("⚒️"): st.session_state.lang = "poly" # Seletor de expansão
        
        st.write("---")
        
        # 3. Navegação de Páginas (Radio como no original)
        page = st.radio("Menu", ["Mini", "yPoemas", "Eureka"], index=1)
        
        st.write("---")
        
        # 4. Seleção de Livro e Temas (Essencial para o funcionamento da página)
        # No original, isso muda conforme a página, mas reside na sidebar
        if page == "yPoemas":
            st.session_state.book = st.selectbox("Livro:", ["livro vivo", "todos os temas"])
            # Aqui entraria a carga de temas dinâmica do PAI
            st.session_state.tema = st.selectbox("Tema:", ["Fatos", "Amor", "Morte"]) 

        st.write("---")
        
        # 5. Checkboxes de Sentidos (draw_check_buttons)
        col_draw, col_talk = st.columns(2)
        st.session_state.draw = col_draw.checkbox("Imagem", st.session_state.draw)
        st.session_state.talk = col_talk.checkbox("Áudio", st.session_state.talk)
        
        return page

# --- EXECUÇÃO ---

# Inicialização de estados básicos do PAI
if "lang" not in st.session_state: st.session_state.lang = "pt"
if "draw" not in st.session_state: st.session_state.draw = False
if "talk" not in st.session_state: st.session_state.talk = False
if "book" not in st.session_state: st.session_state.book = "livro vivo"

current_page = build_sidebar()

# Exibição da página conforme seleção
if current_page == "yPoemas":
    st.write(f"### Página yPoemas (Lógica do PAI)")
    # Próxima etapa será montar o corpo desta página completo.
