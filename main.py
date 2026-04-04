import streamlit as st
import os
import random
from lay_2_ypo import gera_poema

# --- @fernandoulopeslopes-boop's Machina: STATUS 05:15 AM ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide", initial_sidebar_state="expanded")

# CSS: Calibragem 116px e Estética de Terminal Industrial
st.markdown("""
    <style>
    div.stButton > button {
        width: 116px !important;
        height: 42px !important;
        border-radius: 0px;
        font-family: 'Courier New', Courier, monospace;
        border: 1px solid #444;
        font-weight: bold;
        background-color: #1e1e1e;
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
        border: 1px solid #333;
        line-height: 1.6;
    }
    [data-testid="stSidebar"] {
        width: 280px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE ESTADO CRÍTICO ---
if 'page' not in st.session_state: st.session_state.page = "POESIA"
if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = 42
if 'last_tema' not in st.session_state: st.session_state.last_tema = ""
if 'output' not in st.session_state: st.session_state.output = ""

# --- SIDEBAR (STATUS DO SISTEMA) ---
with st.sidebar:
    st.title("🌀 yPoemas")
    st.markdown("### Machina v.2.3.8")
    st.markdown("---")
    st.write(f"**INTERFACE:** {st.session_state.page}")
    st.write(f"**SEED:** {st.session_state.seed_eureka}")
    st.write(f"**FILE:** {st.session_state.last_tema}.ypo")
    st.markdown("---")
    if st.button("RELOAD SYSTEM"):
        st.cache_data.clear()
        st.rerun()

# --- NAVEGADORES (PALCO SUPERIOR) ---

# Camada 1: Operações de Ítimos (O TOPO DO PALCO)
c_nav = st.columns(6)
ops = ["+", "<", "*", ">", "?", "@"]
for i, op in enumerate(ops):
    with c_nav[i]:
        if st.button(op, key=f"nav_{op}"):
            if op == "*": # RAND: Nova semente e regeneração
                st.session_state.seed_eureka = random.randint(1000, 9999)
                if st.session_state.last_tema:
                    st.session_state.output = gera_poema(st.session_state.last_tema, st.session_state.seed_eureka)
                st.rerun()

# Camada 2: Páginas de Navegação
c_pg = st.columns(6)
pages = ["POESIA", "page_mini", "SOBRE", "AJUDA", "CONFIG"]
for i, p in enumerate(pages):
    with c_pg[i]:
        if st.button(p, key=f"pg_{p}"):
            st.session_state.page = p

st.markdown("---")

# --- EXECUÇÃO POR PÁGINA ---

if st.session_state.page == "POESIA":
    c_main, c_var = st.columns([5, 1])
    
    with c_main:
        # Palco Limpo: Input direto para gera_poema
        tema = st.text_input("INPUT", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="TEMA...")
        
        if st.button("GERAR POESIA"):
            if tema:
                st.session_state.last_tema = tema
                st.session_state.output = gera_poema(tema.lower().strip(), st.session_state.seed_eureka)
        
        st.text_area("", value=st.session_state.output, height=650, label_visibility="collapsed")

    with c_var:
        st.markdown("**VARS**")
        # Variações rápidas (Sementes fixas 1-10)
        for v in range(1, 11):
            if st.button(f"v{v}", key=f"v_p_{v}"):
                st.session_state.seed_eureka = v
                if st.session_state.last_tema:
                    st.session_state.output = gera_poema(st.session_state.last_tema, st.session_state.seed_eureka)
                st.rerun()

elif st.session_state.page == "page_mini":
    # A PÁGINA MINI AVANÇADA
    st.subheader("📟 page_mini: GERENCIADOR DE ÍTIMOS")
    
    col_m1, col_m2 = st.columns([1, 2])
    with col_m1:
        st.markdown("**DATABASE**")
        m_in = st.text_input("M_TARGET", key="mini_in", label_visibility="collapsed", placeholder="TEMA...")
        if st.button("RAND_MINI"):
            st.session_state.seed_eureka = random.randint(0, 999)
            st.rerun()
    with col_m2:
        if m_in:
            res_mini = gera_poema(m_in.lower().strip(), st.session_state.seed_eureka)
            st.text_area("", value=res_mini, height=500, label_visibility="collapsed")

# --- MANDALA ---
st.markdown("---")
st.markdown("✨ *Mandala: @fernandoulopeslopes-boop's Machina em seu estado pleno.*")
