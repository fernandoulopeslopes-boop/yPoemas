import streamlit as st
import random
import os

# --- LOG DE SINCRONIA ---
st.error("VERSÃO 04-ABRIL | ESTÉTICA MADRUGADA")

try:
    from lay_2_ypo import gera_poema
except Exception as e:
    st.error(f"Erro: {e}")
    def gera_poema(t, s): return "OFFLINE"

# --- CONFIGURAÇÃO E CSS (A CARA DA MADRUGADA) ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&display=swap');

    .stApp {
        background-color: #000000;
        color: #00ff00;
    }
    
    /* Botões Operadores Superior */
    div.stButton > button {
        width: 100% !important;
        height: 40px !important;
        background-color: #000 !important;
        color: #00ff00 !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 0px !important;
        font-family: 'Courier Prime', monospace !important;
        font-weight: bold !important;
        font-size: 18px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #00ff00 !important;
        color: #fff !important;
        background-color: #050505 !important;
    }

    /* O Terminal de Texto */
    .stTextArea textarea {
        background-color: #000 !important;
        color: #00ff00 !important;
        font-family: 'Courier Prime', monospace !important;
        font-size: 21px !important;
        line-height: 1.4 !important;
        border: 1px solid #111 !important;
        border-radius: 0px !important;
        padding: 20px !important;
    }

    /* Input do Tema */
    div[data-baseweb="input"] {
        background-color: #000 !important;
        border-bottom: 1px solid #222 !important;
    }
    input {
        color: #00ff00 !important;
        font-family: 'Courier Prime', monospace !important;
        text-align: center !important;
        font-size: 18px !important;
    }

    /* Ajustes de Layout */
    .stMarkdown hr { border-top: 1px solid #111 !important; }
    .stCaption { color: #333 !important; font-family: 'Courier Prime', monospace; }
    
    /* Esconder elementos padrão Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- ESTADO ---
if 'output' not in st.session_state: st.session_state.output = ""
if 'last_tema' not in st.session_state: st.session_state.last_tema = ""
if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = "42"

# --- OPERADORES SUPERIORES ---
c_nav = st.columns(6)
ops = ["+", "<", "*", ">", "?", "@"]
for i, op in enumerate(ops):
    with c_nav[i]:
        if st.button(op):
            if op == "*":
                st.session_state.seed_eureka = str(random.randint(1000, 9999))
                if st.session_state.last_tema:
                    res = gera_poema(st.session_state.last_tema, st.session_state.seed_eureka)
                    st.session_state.output = "\n".join(res) if isinstance(res, list) else res
                st.rerun()

st.markdown("---")

# --- PALCO CENTRAL ---
c_main, c_vars = st.columns([5, 1])

with c_main:
    tema = st.text_input("TEMA", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="SUSSURRE O TEMA...")
    
    if st.button("PROCESSAR"):
        if tema:
            st.session_state.last_tema = tema
            res = gera_poema(tema.lower().strip(), st.session_state.seed_eureka)
            st.session_state.output = "\n".join(res) if isinstance(res, list) else res
            st.rerun()

    st.text_area("PALCO", value=st.session_state.output, height=650, label_visibility="collapsed")

with c_vars:
    for v in range(1, 11):
        if st.button(f"v{v}"):
            st.session_state.seed_eureka = str(v)
            if st.session_state.last_tema:
                res = gera_poema(st.session_state.last_tema, str(v))
                st.session_state.output = "\n".join(res) if isinstance(res, list) else res
            st.rerun()

st.markdown("---")
st.caption("Machina v3.5 - @fernandoulopeslopes-boop")
