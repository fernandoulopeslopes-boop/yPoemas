import streamlit as st
import os
import random

# --- CONEXÃO MODULAR CORRIGIDA ---
try:
    from lay_2_ypo import gera_poema
except ModuleNotFoundError:
    st.error("ERRO: O arquivo 'lay_2_ypo.py' não foi encontrado no repositório.")
    def gera_poema(nome_tema, seed_eureka):
        return "Módulo lay_2_ypo não localizado. Verifique o GitHub."

# --- CONFIGURAÇÃO @fernandoulopeslopes-boop ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide", initial_sidebar_state="expanded")

# CSS: Precisão 116px e Ambiente de Terminal
st.markdown("""
    <style>
    div.stButton > button {
        width: 116px !important;
        height: 42px !important;
        border-radius: 0px;
        font-family: 'Courier New', Courier, monospace;
        border: 1px solid #444;
        font-weight: bold;
    }
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        background-color: #0e1117;
        color: #00ff00;
        font-size: 16px;
    }
    [data-testid="stSidebar"] {
        width: 280px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE ESTADO ---
if 'page' not in st.session_state:
    st.session_state.page = "POESIA"
if 'seed_eureka' not in st.session_state:
    st.session_state.seed_eureka = 42
if 'last_tema' not in st.session_state:
    st.session_state.last_tema = ""
if 'output_machina' not in st.session_state:
    st.session_state.output_machina = ""

# --- SIDEBAR (CONTROLE DE FLUXO) ---
with st.sidebar:
    st.title("🌀 yPoemas")
    st.markdown("### Machina v.2.3.8")
    st.write(f"**SEED:** {st.session_state.seed_eureka}")
    st.write(f"**PAGE:** {st.session_state.page}")
    st.markdown("---")
    if st.button("RELOAD"):
        st.cache_data.clear()
        st.rerun()

# --- NAVEGADORES (PALCO SUPERIOR) ---

# Camada 1: Páginas (116px)
p_cols = st.columns(6)
pages = ["POESIA", "page_mini", "SOBRE", "AJUDA", "CONFIG"]
for i, p in enumerate(pages):
    with p_cols[i]:
        if st.button(p, key=f"pg_{p}"):
            st.session_state.page = p

# Camada 2: Operações (+ < * > ? @)
t_cols = st.columns(6)
ops = ["+", "<", "*", ">", "?", "@"]
for i, op in enumerate(ops):
    with t_cols[i]:
        if st.button(op, key=f"op_{op}"):
            if op == "*": # RANDOM SEED
                st.session_state.seed_eureka = random.randint(1000, 9999)
                st.rerun()

st.markdown("---")

# --- LÓGICA DE EXECUÇÃO ---

if st.session_state.page == "POESIA":
    c_main, c_var = st.columns([5, 1])
    
    with c_main:
        # Input do Tema (nome_tema para a função)
        tema = st.text_input("INPUT", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="TEMA...")
        
        if st.button("GERAR POESIA"):
            if tema:
                st.session_state.last_tema = tema
                # Chamada oficial para lay_2_ypo
                st.session_state.output_machina = gera_poema(tema.lower().strip(), st.session_state.seed_eureka)
        
        st.text_area("", value=st.session_state.output_machina, height=600, label_visibility="collapsed")

    with c_var:
        st.markdown("**VARS**")
        for v in range(1, 11):
            if st.button(f"v{v}", key=f"v_p_{v}"):
                st.session_state.seed_eureka = v
                st.session_state.output_machina = gera_poema(st.session_state.last_tema, st.session_state.seed_eureka)
                st.rerun()

elif st.session_state.page == "page_mini":
    st.subheader("📟 page_mini")
    m_in = st.text_input("M_TARGET", key="mini_in", label_visibility="collapsed")
    if m_in:
        # Mini palco direto
        st.text_area("", value=gera_poema(m_in.lower().strip(), st.session_state.seed_eureka), height=450, label_visibility="collapsed")

# --- MANDALA ---
st.markdown("---")
st.markdown("✨ *Mandala: @fernandoulopeslopes-boop's Machina ativa.*")
