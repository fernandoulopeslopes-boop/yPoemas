import streamlit as st
import random
import os

# --- LOG DE CONTROLE ---
st.error("VERSÃO 04-ABRIL | RECONSTRUÇÃO DE INTERFACE")

try:
    from lay_2_ypo import gera_poema
except Exception as e:
    st.error(f"Erro Motor: {e}")
    def gera_poema(t, s): return "OFFLINE"

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide")

# --- INJEÇÃO DE ESTILO (A CARA DA MADRUGADA) ---
st.markdown("""
    <style>
    /* Reset Geral */
    .stApp { background-color: #000000 !important; }
    
    /* Área de Texto (O Palco) */
    .stTextArea textarea {
        background-color: #000 !important;
        color: #00ff00 !important;
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 20px !important;
        border: 1px solid #1a1a1a !important;
        height: 600px !important;
    }

    /* Botões Operadores (Quadrados) */
    div.stButton > button {
        background-color: #000 !important;
        color: #00ff00 !important;
        border: 1px solid #333 !important;
        border-radius: 0px !important;
        width: 100% !important;
        font-family: 'Courier New', monospace !important;
    }
    div.stButton > button:hover { border-color: #00ff00 !important; }

    /* Input do Tema */
    input {
        background-color: #000 !important;
        color: #00ff00 !important;
        border: none !important;
        border-bottom: 1px solid #333 !important;
        text-align: center !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Esconder Lixo Visual */
    header, footer, .stDeployButton { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- ESTADO ---
if 'output' not in st.session_state: st.session_state.output = ""
if 'last_tema' not in st.session_state: st.session_state.last_tema = ""
if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = "42"

# --- LAYOUT ---

# Operadores Superior (+ < * > ? @)
cols_nav = st.columns(6)
ops = ["+", "<", "*", ">", "?", "@"]
for i, op in enumerate(ops):
    if cols_nav[i].button(op):
        if op == "*":
            st.session_state.seed_eureka = str(random.randint(1000, 9999))
            if st.session_state.last_tema:
                res = gera_poema(st.session_state.last_tema, st.session_state.seed_eureka)
                st.session_state.output = "\n".join(res) if isinstance(res, list) else res
            st.rerun()

st.markdown("---")

# Corpo Principal
c_main, c_vars = st.columns([5, 1])

with c_main:
    tema = st.text_input("TEMA", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="SUSSURRE O TEMA...")
    
    if st.button("PROCESSAR"):
        if tema:
            st.session_state.last_tema = tema
            res = gera_poema(tema.lower().strip(), st.session_state.seed_eureka)
            st.session_state.output = "\n".join(res) if isinstance(res, list) else res
            st.rerun()

    st.text_area("PALCO", value=st.session_state.output, label_visibility="collapsed")

with c_vars:
    for v in range(1, 11):
        if st.button(f"v{v}"):
            st.session_state.seed_eureka = str(v)
            if st.session_state.last_tema:
                res = gera_poema(st.session_state.last_tema, str(v))
                st.session_state.output = "\n".join(res) if isinstance(res, list) else res
            st.rerun()

st.markdown("---")
st.caption("Machina v4.0 - @fernandoulopeslopes-boop")
