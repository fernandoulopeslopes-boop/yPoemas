import streamlit as st
import random
import os

# --- CONTADOR INTERNO (MY_TRIES) ---
my_tries = 7

# --- LOG DE CONTROLE E VERSÃO ---
st.error(f"yPoemas: commit # {my_tries} | PROTOCOLLO AXIOMA_ZERO")

try:
    from lay_2_ypo import gera_poema
except Exception as e:
    st.error(f"FALHA NO MOTOR: {e}")
    def gera_poema(t, s): return "MOTOR OFFLINE"

# --- CONFIGURAÇÃO E ESTÉTICA MADRUGADA ---
st.set_page_config(page_title=f"yPoemas #{my_tries}", layout="wide", initial_sidebar_state="collapsed")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&display=swap');

    .stApp {{
        background-color: #000000 !important;
        color: #00ff00 !important;
    }}
    
    /* Botões Operadores */
    div.stButton > button {{
        width: 100% !important;
        height: 45px !important;
        background-color: #000 !important;
        color: #00ff00 !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 0px !important;
        font-family: 'Courier Prime', monospace !important;
        font-size: 20px !important;
    }}
    div.stButton > button:hover {{
        border-color: #00ff00 !important;
    }}

    /* Palco (Terminal) */
    .stTextArea textarea {{
        background-color: #000 !important;
        color: #00ff00 !important;
        font-family: 'Courier Prime', monospace !important;
        font-size: 22px !important;
        border: 1px solid #111 !important;
        border-radius: 0px !important;
        padding: 25px !important;
    }}

    /* Input do Tema */
    input {{
        background-color: #000 !important;
        color: #00ff00 !important;
        font-family: 'Courier Prime', monospace !important;
        text-align: center !important;
        border: none !important;
        border-bottom: 1px solid #222 !important;
    }}

    /* Ocultar Interface Padrão */
    header, footer, .stDeployButton {{ display: none !important; }}
    </style>
""", unsafe_allow_html=True)

# --- ESTADO DA SESSÃO ---
if 'output' not in st.session_state: st.session_state.output = ""
if 'last_tema' not in st.session_state: st.session_state.last_tema = ""
if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = "42"

# --- INTERFACE DE COMANDO ---

# 1. Operadores Superiores (+ < * > ? @)
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

# 2. Palco Central
c_main, c_vars = st.columns([5, 1])

with c_main:
    # Campo para o nome do arquivo (ex: Fatos.ypo)
    tema_input = st.text_input("TEMA", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="DIGITE O NOME EXATO DO ARQUIVO...")
    
    if st.button("PROCESSAR"):
        if tema_input:
            st.session_state.last_tema = tema_input
            try:
                # Motor processa exatamente o input do usuário
                res = gera_poema(tema_input.strip(), st.session_state.seed_eureka)
                st.session_state.output = "\n".join(res) if isinstance(res, list) else res
            except Exception as e:
                st.session_state.output = f"ERRO: '{tema_input}' não encontrado.\nLog: {e}"
            st.rerun()

    # Saída do Terminal
    st.text_area("PALCO", value=st.session_state.output, height=650, label_visibility="collapsed")

with c_vars:
    # Variações v1 a v10
    for v in range(1, 11):
        if st.button(f"v{v}"):
            st.session_state.seed_eureka = str(v)
            if st.session_state.last_tema:
                res = gera_poema(st.session_state.last_tema, str(v))
                st.session_state.output = "\n".join(res) if isinstance(res, list) else res
            st.rerun()

st.markdown("---")
# Identificador visível no rodapé
st.caption(f"yPoemas: commit # {my_tries} | PROTOCOLLO AXIOMA_ZERO")
