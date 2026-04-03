import streamlit as st
import random
import time
import os

# --- MURO DE ARRIMO (Gênese Obrigatória) ---
# Se estas chaves não existirem, o Streamlit morre na linha 44.
# Este bloco PRECISA vir antes de qualquer 'if st.session_state.page'
if 'page' not in st.session_state:
    st.session_state.page = "mini"
if 'mini' not in st.session_state:
    st.session_state.mini = 0
if 'auto' not in st.session_state:
    st.session_state.auto = False
if 'rand' not in st.session_state:
    st.session_state.rand = True
if 'lang' not in st.session_state:
    st.session_state.lang = "pt"
if 'tema' not in st.session_state:
    st.session_state.tema = ""
if 'talk' not in st.session_state:
    st.session_state.talk = True
if 'draw' not in st.session_state:
    st.session_state.draw = True
if 'vydo' not in st.session_state:
    st.session_state.vydo = False

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="yPoemas", layout="wide")

# --- NAVEGAÇÃO ---
nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
labels = ["ツ mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]

for i, pag in enumerate(paginas):
    if nav_cols[i].button(labels[i], key=f"nav_{pag}"):
        st.session_state.page = pag
        st.rerun()

st.markdown("---")

# --- LINHA 44 (AGORA PROTEGIDA) ---
if st.session_state.page == "mini":
    # Aqui entra o seu código da página Mini que você resgatou
    st.write("Māchina Mini pronta.")
