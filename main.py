import streamlit as st
import sys
import os
import random
from deep_translator import GoogleTranslator

# =================================================================
# 🧠 CONEXÃO COM O MOTOR (PROTOCOLO DE SEGURANÇA)
# =================================================================

# Força o Python a enxergar a raiz do projeto no Streamlit Cloud
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from lay_2_ypo import gera_poema
except ImportError as e:
    st.error(f"### 🚨 ERRO DE SINCRONIZAÇÃO")
    st.write(f"A Pele (main.py) não conseguiu encontrar o Cérebro (lay_2_ypo.py).")
    st.info(f"Detalhe técnico: {e}")
    st.stop()

# =================================================================
# 🎨 CONFIGURAÇÃO VISUAL & ESTADOS (ESMERO NOS DETALHES)
# =================================================================

st.set_page_config(page_title="yPoemas - Machina", layout="wide")

# Inicialização de Estados (Session State)
if 'tema' not in st.session_state: st.session_state.tema = 'Random'
if 'seed' not in st.session_state: st.session_state.seed = 42
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'draw' not in st.session_state: st.session_state.draw = 'N'

# CSS para limpeza de interface (Sem Matplotlib)
st.markdown("""
    <style>
    .logo-text { font-family: 'Courier New', Courier, monospace; font-size: 1.8rem; color: #333; }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 🛠️ BARRA LATERAL (CONTROL BAR)
# =================================================================

with st.sidebar:
    st.title("Machina")
    st.write("---")
    
    # Botões de Arte e Talk (Substituindo o antigo Video)
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🎨 Arte"): st.session_state.draw = 'Y'
    with col_btn2:
        if st.button("💬 Talk"): st.session_state.draw = 'N'
    
    st.write("---")
    
    # Seletor de Idiomas (Prisma)
    langs = {'Português': 'pt', 'English': 'en', 'Español': 'es', 'Français': 'fr', 'Italiano': 'it'}
    sel_lang = st.selectbox("Idioma do Poema", list(langs.keys()))
    st.session_state.lang = langs[sel_lang]

# =================================================================
# 🎭 PALCO PRINCIPAL (VIEW
