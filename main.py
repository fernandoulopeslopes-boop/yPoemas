import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime
from lay_2_ypo import gera_poema
import extra_stylable_components as stx

# 1. CONFIGURAÇÃO (Respeitando a Regra 0)
st.set_page_config(page_title="a máquina de fazer Poesia", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { min-width: 310px !important; max-width: 310px !important; }
    [data-testid="stAppViewBlockContainer"] { max-width: 100% !important; padding: 1rem 2rem !important; }
    footer {visibility: hidden;} #MainMenu {visibility: hidden;} header {visibility: hidden;}
    .poesia-viva {
        font-family: 'Georgia', serif !important;
        font-size: 32px !important; 
        line-height: 1.6 !important;
        padding: 40px;
        background-color: #fdfdfd;
        border-radius: 8px;
        border: 1px solid #eee;
        color: #1a1a1a;
    }
    </style>
""", unsafe_allow_html=True)

# 2. ESTADOS & FERRAMENTAS
if 'take' not in st.session_state: st.session_state.take = random.randint(1000, 9999)
if 'lang' not in st.session_state: st.session_state.lang = "pt"
if 'tema' not in st.session_state: st.session_state.tema = "Fatos"

def carregar_poesia_real(tema, id_seed):
    # Chama a sua engine original
    script = gera_poema(tema, id_seed)
    # Transforma a lista do script em HTML com quebras de linha
    return "<br>".join([line.strip() for line in script if line.strip() != ""])

# 3. NAVEGAÇÃO (TABS - Ordem Original)
chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="1", title="mini", description=""),
    stx.TabBarItemData(id="2", title="yPoemas", description=""),
    stx.TabBarItemData(id="3", title="eureka", description=""),
    stx.TabBarItemData(id="4", title="oficina", description=""),
    stx.TabBarItemData(id="5", title="biblioteca", description=""),
    stx.TabBarItemData(id="6", title="poly", description=""),
    stx.TabBarItemData(id="7", title="sobre", description=""),
], default="2")

mapa = {"1":"mini", "2":"yPoemas", "3":"eureka", "4":"oficina", "5":"biblioteca", "6":"poly", "7":"sobre"}
sala = mapa.get(chosen_id, "yPoemas")

# 4. PALCO (Controles)
st.write("")
c1, c2, c3, c4, c_id = st.columns([1, 1, 1, 1, 4])
if c1.button("✚"): 
    st.session_state.take = random.randint(1000, 9999)
    st.rerun()
if c2.button("◀"): 
    st.session_state.take -= 1
    st.rerun()
if c3.button("✻"): 
    st.session_state.take = random.randint(1000, 9999)
    st.rerun()
if c4.button("▶"): 
    st.session_state.take += 1
    st.rerun()

c_id.code(f"SALA: {sala.upper()} | ID: {st.session_state.take} | TEMA: {st.session_state.tema}")

st.divider()

# EXIBIÇÃO DA POESIA
if sala == "yPoemas":
    conteudo = carregar_poesia_real(st.session_state.tema, st.session_state.take)
    st.markdown(f'<div class="poesia-viva">{conteudo}</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="poesia-viva">SALA: {sala.upper()}<br>[ Em estudo... ]</div>', unsafe_allow_html=True)

# 5. SIDEBAR
with st.sidebar:
    st.title("A Machina")
    st.divider()
    st.write("🌍 **IDIOMA**")
    col1, col2, col3 = st.columns(3)
    if col1.button("pt"): st.session_state.lang = "pt"; st.rerun()
    if col2.button("es"): st.session_state.lang = "es"; st.rerun()
    if col3.button("en"): st.session_state.lang = "en"; st.rerun()
    
    st.divider()
    # Seletor de Tema (Exemplo para a Sala yPoemas)
    st.session_state.tema = st.selectbox("Escolha o Tema", ["Fatos", "Amor", "Tempo", "Espaço"])

