import streamlit as st
import random
import os

# --- CONTADOR INTERNO ---
my_tries = 11

# --- CABEÇALHO DE CONTROLE ---
st.error(f"yPoemas: commit # {my_tries} | PROTOCOLLO AXIOMA_ZERO")

try:
    from lay_2_ypo import gera_poema
except Exception as e:
    st.error(f"MOTOR ERROR: {e}")
    def gera_poema(t, s): return "OFFLINE"

# --- CONFIGURAÇÃO E CSS (A CARA DA MADRUGADA) ---
st.set_page_config(page_title=f"yPoemas #{my_tries}", layout="wide")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&display=swap');

    /* Fundo Absoluto */
    .stApp {{
        background-color: #000000 !important;
        color: #00ff00 !important;
    }}
    
    /* Botões Operadores (Superior) */
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
        background-color: #050505 !important;
    }}

    /* O Palco (Terminal de Saída) */
    .stTextArea textarea {{
        background-color: #000 !important;
        color: #00ff00 !important;
        font-family: 'Courier Prime', monospace !important;
        font-size: 22px !important;
        line-height: 1.5 !important;
        border: 1px solid #111 !important;
        border-radius: 0px !important;
        padding: 25px !important;
    }}

    /* Campo de Input (Tema) */
    input {{
        background-color: #000 !important;
        color: #00ff00 !important;
        font-family: 'Courier Prime', monospace !important;
        text-align: center !important;
        font-size: 20px !important;
        border: none !important;
        border-bottom: 2px solid #1a1a1a !important;
    }}

    /* UI Minimalista */
    header, footer, .stDeployButton {{ display: none !important; }}
    .stMarkdown hr {{ border-top: 1px solid #111 !important; }}
    </style>
""", unsafe_allow_html=True)

# --- ESTADO DA SESSÃO ---
if 'output' not in st.session_state: st.session_state.output = ""
if 'last_tema' not in st.session_state: st.session_state.last_tema = ""
if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = "42"

# --- ESTRUTURA DE COMANDO ---

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

# 2. Palco Principal e Variáveis
c_main, c_vars = st.columns([5, 1])

with c_main:
    # PRECISÃO ABSOLUTA: O input vai direto para o motor.
    tema = st.text_input("INPUT", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="DIGITE O ARQUIVO (ex: Fatos.ypo)")
    
    if st.button("PROCESSAR"):
        if tema:
            st.session_state.last_tema = tema.strip()
            try:
                # Motor recebe o tema limpo. 
                # Se o erro './data/...' persistir, o ajuste deve ser feito na lay_2_ypo.py
                res = gera_poema(st.session_state.last_tema, st.session_state.seed_eureka)
                st.session_state.output = "\n".join(res) if isinstance(res, list) else res
            except Exception as e:
                st.session_state.output = f"FALHA NO CAMINHO: {e}\n\nO motor buscou por este nome. Verifique se o arquivo está na pasta correta no GitHub."
            st.rerun()

    # Saída do Terminal
    st.text_area("PALCO", value=st.session_state.output, height=650, label_visibility="collapsed")

with c_vars:
    # Botões de Variação
    for v in range(1, 11):
        if st.button(f"v{v}"):
            st.session_state.seed_eureka = str(v)
            if st.session_state.last_tema:
                res = gera_poema(st.session_state.last_tema, str(v))
                st.session_state.output = "\n".join(res) if isinstance(res, list) else res
            st.rerun()

st.markdown("---")
st.caption(f"yPoemas: commit # {my_tries} | PROTOCOLLO AXIOMA_ZERO")
