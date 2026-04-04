import streamlit as st
import os
import random
import time

# --- @fernandoulopeslopes-boop's Machina: AMBIENTE 05:12 AM ---
from lay_2_ypo import gera_poema

st.set_page_config(page_title="yPoemas - Machina", layout="wide", initial_sidebar_state="expanded")

# CSS: Calibragem 116px e Terminal de Alta Precisão
st.markdown("""
    <style>
    div.stButton > button {
        width: 116px !important;
        height: 42px !important;
        border-radius: 0px;
        font-family: 'Courier New', Courier, monospace;
        border: 1px solid #444;
        font-weight: bold;
        background-color: #0e1117;
        color: #fff;
    }
    div.stButton > button:hover {
        border-color: #00ff00;
        color: #00ff00;
    }
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        background-color: #000;
        color: #00ff00;
        font-size: 18px;
        border: 1px solid #222;
        line-height: 1.6;
    }
    [data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #222;
    }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE ESTADO CRÍTICO ---
if 'seed_eureka' not in st.session_state:
    st.session_state.seed_eureka = 42
if 'page' not in st.session_state:
    st.session_state.page = "POESIA"
if 'last_tema' not in st.session_state:
    st.session_state.last_tema = ""
if 'output' not in st.session_state:
    st.session_state.output = ""

# --- SIDEBAR (STATUS DO SISTEMA) ---
with st.sidebar:
    st.title("🌀 yPoemas")
    st.markdown("---")
    st.write(f"SYSTEM_TIME: {time.strftime('%H:%M:%S')}")
    st.write(f"SEED_ACTIVE: {st.session_state.seed_eureka}")
    st.write(f"TARGET_FILE: {st.session_state.last_tema}.ypo")
    st.markdown("---")
    if st.button("RESET_CACHE"):
        st.cache_data.clear()
        st.rerun()

# --- NAVEGADORES (PALCO SUPERIOR) ---

# Linha 1: Páginas (POESIA / MINI / SOBRE / AJUDA / CONFIG)
p_cols = st.columns(6)
pages = ["POESIA", "page_mini", "SOBRE", "AJUDA", "CONFIG"]
for i, p in enumerate(pages):
    with p_cols[i]:
        if st.button(p, key=f"pg_{p}"):
            st.session_state.page = p

# Linha 2: Operações de Ítimos (+ < * > ? @)
t_cols = st.columns(6)
ops = ["+", "<", "*", ">", "?", "@"]
for i, op in enumerate(ops):
    with t_cols[i]:
        if st.button(op, key=f"op_{op}"):
            if op == "*": # RAND SEED
                st.session_state.seed_eureka = random.randint(1000, 9999)
                st.rerun()

st.markdown("---")

# --- EXECUÇÃO POR PÁGINA ---

if st.session_state.page == "POESIA":
    c_main, c_var = st.columns([5, 1])
    
    with c_main:
        # Input Seco (sem label)
        tema = st.text_input("INPUT", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="TEMA...")
        
        if st.button("GERAR POESIA"):
            if tema:
                st.session_state.last_tema = tema
                # Chamada oficial para o script lay_2_ypo
                st.session_state.output = gera_poema(tema.lower().strip(), st.session_state.seed_eureka)
        
        st.text_area("", value=st.session_state.output, height=650, label_visibility="collapsed")

    with c_var:
        st.markdown("**VARS**")
        # Seleção de Sementes Fixas (Variações de Ítimos)
        for v in range(1, 11):
            if st.button(f"v{v}", key=f"v_p_{v}"):
                st.session_state.seed_eureka = v
                if st.session_state.last_tema:
                    st.session_state.output = gera_poema(st.session_state.last_tema, st.session_state.seed_eureka)
                st.rerun()

elif st.session_state.page == "page_mini":
    st.subheader("📟 MINI_MODULE")
    col_m1, col_m2 = st.columns([1, 2])
    with col_m1:
        m_in = st.text_input("M_TARGET", key="mini_in", label_visibility="collapsed", placeholder="TEMA...")
    with col_m2:
        if m_in:
            # Geração imediata no mini palco
            res_mini = gera_poema(m_in.lower().strip(), st.session_state.seed_eureka)
            st.text_area("", value=res_mini, height=450, label_visibility="collapsed")

# --- MANDALA ---
st.markdown("---")
st.markdown("✨ *Mandala: @fernandoulopeslopes-boop's Machina ativa.*")
