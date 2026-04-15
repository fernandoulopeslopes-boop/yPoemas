import streamlit as st
import os
import random
import base64
from deep_translator import GoogleTranslator

# MOTOR REAL
try: 
    from lay_2_ypo import gera_poema
except Exception: 
    def gera_poema(t, p=""): 
        return ["Erro: motor não encontrado."]

# --- 1. BOOT & ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

for key, val in {
    'page': 'demo', 
    'show_help': False, 
    'ID_CLIC': 'demo', 
    'idx_tema': 0, 
    'temas_atuais': []
}.items():
    if key not in st.session_state: st.session_state[key] = val

def nav_to(p):
    st.session_state.page = p
    st.session_state.show_help = False
    st.session_state.ID_CLIC = p

def prox_tema():
    if st.session_state.temas_atuais:
        st.session_state.idx_tema = (st.session_state.idx_tema + 1) % len(st.session_state.temas_atuais)

def ante_tema():
    if st.session_state.temas_atuais:
        st.session_state.idx_tema = (st.session_state.idx_tema - 1) % len(st.session_state.temas_atuais)

def sorteio_tema():
    if st.session_state.temas_atuais:
        st.session_state.idx_tema = random.randint(0, len(st.session_state.temas_atuais) - 1)

# Função para converter ícone em Base64 para exibição no HTML
def get_base64_bin(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- 2. CSS: ISOLAMENTO TOTAL DE SCROLL E POSICIONAMENTO ---
st.markdown(f"""
<style>
    /* DESATIVA SCROLL DA PÁGINA INTEIRA - ATAQUE DIRETO */
    [data-testid="stAppViewContainer"], [data-testid="stMainViewContainer"], .main {{
        overflow: hidden !important;
        height: 100vh !important;
    }}
    [data-testid="stHeader"], [data-testid="stSidebar"] {{display: none
