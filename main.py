import streamlit as st
import random
import os

# --- CONTADOR INTERNO ---
my_tries = 9

# --- CABEÇALHO DE SINCRONIA ---
st.error(f"yPoemas: commit # {my_tries} | PROTOCOLLO AXIOMA_ZERO")

try:
    from lay_2_ypo import gera_poema
except Exception as e:
    st.error(f"MOTOR ERROR: {e}")
    def gera_poema(t, s): return "OFFLINE"

# --- CONFIGURAÇÃO E INJEÇÃO CSS ---
st.set_page_config(page_title=f"yPoemas #{my_tries}", layout="wide")

st.markdown(f"""
    <style>
    /* Forçar Fundo Preto no Body e no App */
    .stApp, body, [data-testid="stAppViewContainer"] {{
        background-color: #000000 !important;
        color: #00ff00 !important;
    }}
    
    /* Botões Operadores Superior */
    div.stButton > button {{
        width: 100% !important;
        background-color: #000 !important;
        color: #00ff00 !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 0px !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
    }}
    div.stButton > button:hover {{
        border-color: #00ff00 !important;
        box-shadow: 0 0 5px #00ff00;
    }}

    /* O Palco (Terminal) */
    .stTextArea textarea {{
        background-color: #000 !important;
        color: #00ff00 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 22px !important;
        border: 1px solid #111 !important;
        padding: 20px !important;
    }}

    /* Input do Tema */
    input {{
        background-color: #000 !important;
        color: #00ff00 !important;
        border: none !important;
        border-bottom: 2px solid #1a1a1a !important;
        text-align: center !important;
        font-size: 20px !important;
    }}

    /* Esconder elementos de lixo */
    header, footer, .stDeployButton, [data-testid="stToolbar"] {{
        display: none !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- ESTADO ---
if 'output' not in st.session_state: st.session_state.output = ""
if 'last_tema' not in st.session_state: st.session_state.last_tema = ""
if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = "42"

# --- ESTRUTURA DA MACHINA ---

# Bloco 1: Operadores (+ < * > ? @)
with st.container():
    c_nav = st.columns(6)
    ops = ["+", "<", "*", ">", "?", "@"]
    for i, op in enumerate(ops):
        if c_nav[i].button(op):
            if op == "*":
                st.session_state.seed_eureka = str(random.randint(1000, 9999))
                if st.session_state.last_tema:
                    res = gera_poema(st.session_state.last_tema, st.session_state.seed_eureka)
                    st.session_state.output = "\n".join(res) if isinstance(res, list) else res
                st.rerun()

st.markdown("---")

# Bloco 2: Palco e Variáveis
with st.container():
    c_main, c_vars = st.columns([5, 1])

    with c_main:
        tema = st.text_input("INPUT", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="SUSSURRE O NOME DO ARQUIVO...")
        
        if st.button("PROCESSAR"):
            if tema:
                st.session_state.last_tema = tema
                try:
                    res = gera_poema(tema.strip(), st.session_state.seed_eureka)
                    st.session_state.output = "\n".join(res) if isinstance(res, list) else res
                except Exception as e:
                    st.session_state.output = f"FALHA: {e}"
                st.rerun()

        st.text_area("PALCO", value=st.session_state.output, height=600, label_visibility="collapsed")

    with c_vars:
        for v in range(1, 11):
            if st.button(f"v{v}"):
                st.session_state.seed_eureka = str(v)
                if st.session_state.last_tema:
                    res = gera_poema(st.session_state.last_tema, str(v))
                    st.session_state.output = "\n".join(res) if isinstance(res, list) else res
                st.rerun()

# --- RODAPÉ ---
st.markdown("---")
st.caption(f"yPoemas: commit # {my_tries} | PROTOCOLLO AXIOMA_ZERO")
