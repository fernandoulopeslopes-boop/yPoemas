import streamlit as st
import random
import os

# --- 1. IDENTIFICAÇÃO DE VERSÃO ---
st.error("MANDALA ATIVA | PROTOCOLLO AXIOMA_ZERO | 04-ABRIL")

try:
    from lay_2_ypo import gera_poema
except Exception as e:
    st.error(f"FALHA NO MOTOR: {e}")
    def gera_poema(t, s): return "MOTOR OFFLINE"

# --- 2. ESTÉTICA DA MADRUGADA (BLACK & GREEN) ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&display=swap');

    /* Fundo e Texto Base */
    .stApp {
        background-color: #000000 !important;
        color: #00ff00 !important;
    }
    
    /* Botões Operadores (Superior) */
    div.stButton > button {
        width: 100% !important;
        height: 45px !important;
        background-color: #000 !important;
        color: #00ff00 !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 0px !important;
        font-family: 'Courier Prime', monospace !important;
        font-size: 20px !important;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        border-color: #00ff00 !important;
        background-color: #050505 !important;
    }

    /* O Palco (Terminal de Saída) */
    .stTextArea textarea {
        background-color: #000 !important;
        color: #00ff00 !important;
        font-family: 'Courier Prime', monospace !important;
        font-size: 22px !important;
        line-height: 1.5 !important;
        border: 1px solid #111 !important;
        border-radius: 0px !important;
        padding: 25px !important;
    }

    /* Campo de Input (Tema) */
    input {
        background-color: #000 !important;
        color: #00ff00 !important;
        font-family: 'Courier Prime', monospace !important;
        text-align: center !important;
        font-size: 18px !important;
        border: none !important;
        border-bottom: 1px solid #222 !important;
    }

    /* Interface Clean */
    header, footer, .stDeployButton { display: none !important; }
    .stMarkdown hr { border-top: 1px solid #111 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. ESTADO DA SESSÃO ---
if 'output' not in st.session_state: st.session_state.output = ""
if 'last_tema' not in st.session_state: st.session_state.last_tema = ""
if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = "42"

# --- 4. COMANDOS SUPERIORES (+ < * > ? @) ---
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

# --- 5. PALCO CENTRAL E VARIÁVEIS ---
c_main, c_vars = st.columns([5, 1])

with c_main:
    # O usuário insere o nome exato do arquivo (ex: Fatos.ypo)
    tema_input = st.text_input("TEMA", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="DIGITE O NOME EXATO DO ARQUIVO...")
    
    if st.button("PROCESSAR"):
        if tema_input:
            st.session_state.last_tema = tema_input
            try:
                # Motor processa o nome exato sem adivinhações
                res = gera_poema(tema_input.strip(), st.session_state.seed_eureka)
                st.session_state.output = "\n".join(res) if isinstance(res, list) else res
            except Exception as e:
                st.session_state.output = f"ERRO NA BUSCA: '{tema_input}'\nVerifique a extensão e o local do arquivo."
            st.rerun()

    # Saída de Texto (O Poema)
    st.text_area("PALCO", value=st.session_state.output, height=650, label_visibility="collapsed")

with c_vars:
    # Botões de Variação (v1 a v10)
    for v in range(1, 11):
        if st.button(f"v{v}"):
            st.session_state.seed_eureka = str(v)
            if st.session_state.last_tema:
                res = gera_poema(st.session_state.last_tema, str(v))
                st.session_state.output = "\n".join(res) if isinstance(res, list) else res
            st.rerun()

st.markdown("---")
st.caption("Machina v5.0 - PROTOCOLLO AXIOMA_ZERO")
