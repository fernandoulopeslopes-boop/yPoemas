import os
import socket
import streamlit as st
from datetime import datetime
from lay_2_ypo import gera_poema

# Configurações de Página
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# CSS para domar o layout e os botões (Just do it)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    
    /* Botões pequenos e alinhados */
    div.stButton > button {
        width: auto !important;
        min-width: 45px !important;
        height: 28px !important;
        padding: 0px 8px !important;
        font-size: 13px !important;
    }
    
    /* Largura da Sidebar */
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child { 
        width: 310px; 
    }
    
    mark { background-color: powderblue; color: black; }
    </style> """,
    unsafe_allow_html=True,
)

# Inicialização de Variáveis
if "lang" not in st.session_state: st.session_state.lang = "pt"
if "page" not in st.session_state: st.session_state.page = "mini"
if "tema" not in st.session_state: st.session_state.tema = "Fatos"

# --- SIDEBAR: IDIOMAS ---
with st.sidebar:
    st.write("### idiomas")
    c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 1, 1, 1, 1])
    if c1.button("pt"): st.session_state.lang = "pt"
    if c2.button("es"): st.session_state.lang = "es"
    if c3.button("it"): st.session_state.lang = "it"
    if c4.button("fr"): st.session_state.lang = "fr"
    if c5.button("en"): st.session_state.lang = "en"
    if c6.button("⚒️"): st.session_state.lang = "ca"
    st.markdown("---")

# --- NAVEGAÇÃO SUPERIOR (6 Colunas) ---
n1, n2, n3, n4, n5, n6 = st.columns(6)
if n1.button("mini"): st.session_state.page = "mini"
if n2.button("ypo"): st.session_state.page = "ypoemas"
if n3.button("eur"): st.session_state.page = "eureka"
if n4.button("bib"): st.session_state.page = "biblioteca"
if n5.button("ofic"): st.session_state.page = "oficina"
if n6.button("sob"): st.session_state.page = "sobre"
st.markdown("---")

# --- LÓGICA DE EXIBIÇÃO ---
if st.session_state.page == "mini":
    st.subheader(f"ツ mini - {st.session_state.tema} ({st.session_state.lang})")
    
    if st.button("✻ gera novo"):
        # Chama sua função externa
        texto_poema = gera_poema(st.session_state.tema, "")
        st.write(texto_poema)
    else:
        st.info("Clique no botão acima para gerar um poema.")

elif st.session_state.page == "ypoemas":
    st.subheader("ツ ypoemas")
    st.write("Seção de poemas completos em desenvolvimento.")

elif st.session_state.page == "eureka":
    st.subheader("ツ eureka")
    find_what = st.text_input("digite algo para buscar...")

else:
    st.subheader(f"ツ {st.session_state.page}")
    st.write(f"Página {st.session_state.page} ativa.")
