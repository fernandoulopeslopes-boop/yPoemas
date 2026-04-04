import streamlit as st
import random
import os

# --- CONTADOR INTERNO (PROTOCOLLO AXIOMA_ZERO) ---
my_tries = 8

# --- IDENTIFICADOR VISÍVEL NO TOPO ---
st.error(f"yPoemas: commit # {my_tries} | STATUS: RECONSTRUÇÃO BRUTA")

try:
    from lay_2_ypo import gera_poema
except Exception as e:
    st.error(f"ERRO MOTOR: {e}")
    def gera_poema(t, s): return "MOTOR OFFLINE"

# --- ESTÉTICA MADRUGADA (RECALIBRADA) ---
st.set_page_config(page_title=f"yPoemas #{my_tries}", layout="wide")

st.markdown(f"""
    <style>
    /* Reset total para evitar o 'lixo' visual */
    .stApp {{
        background-color: #000000 !important;
        color: #00ff00 !important;
        font-family: 'Courier New', monospace !important;
    }}
    
    /* Botões Operadores Superior (+ < * > ? @) */
    div.stButton > button {{
        width: 100% !important;
        background-color: #000 !important;
        color: #00ff00 !important;
        border: 1px solid #222 !important;
        border-radius: 0px !important;
        font-weight: bold !important;
    }}
    div.stButton > button:hover {{
        border-color: #00ff00 !important;
    }}

    /* O Palco (Área de Texto) */
    .stTextArea textarea {{
        background-color: #050505 !important;
        color: #00ff00 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 20px !important;
        border: 1px solid #111 !important;
        border-radius: 0px !important;
    }}

    /* Input de Tema */
    input {{
        background-color: #000 !important;
        color: #00ff00 !important;
        border: none !important;
        border-bottom: 1px solid #333 !important;
        text-align: center !important;
    }}

    /* Limpeza de UI */
    header, footer, .stDeployButton {{ display: none !important; }}
    </style>
""", unsafe_allow_html=True)

# --- ESTADO DA SESSÃO ---
if 'output' not in st.session_state: st.session_state.output = ""
if 'last_tema' not in st.session_state: st.session_state.last_tema = ""
if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = "42"

# --- INTERFACE ---

# 1. LINHA DE COMANDO (+ < * > ? @)
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

# 2. ÁREA CENTRAL
c_main, c_vars = st.columns([5, 1])

with c_main:
    # Digite o nome exato do arquivo (ex: Fatos.ypo)
    tema_input = st.text_input("INPUT", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="DIGITE O ARQUIVO...")
    
    if st.button("PROCESSAR"):
        if tema_input:
            st.session_state.last_tema = tema_input
            try:
                res = gera_poema(tema_input.strip(), st.session_state.seed_eureka)
                st.session_state.output = "\n".join(res) if isinstance(res, list) else res
            except Exception as e:
                st.session_state.output = f"ERRO: {e}"
            st.rerun()

    st.text_area("PALCO", value=st.session_state.output, height=600, label_visibility="collapsed")

with c_vars:
    # Coluna de Variáveis (v1-v10)
    for v in range(1, 11):
        if st.button(f"v{v}"):
            st.session_state.seed_eureka = str(v)
            if st.session_state.last_tema:
                res = gera_poema(st.session_state.last_tema, str(v))
                st.session_state.output = "\n".join(res) if isinstance(res, list) else res
            st.rerun()

# --- RODAPÉ DE CONTROLE ---
st.markdown("---")
st.caption(f"yPoemas: commit # {my_tries} | PROTOCOLLO AXIOMA_ZERO")
