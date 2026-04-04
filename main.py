import streamlit as st
import os
import random
from lay_2_ypo import gera_poema

# --- @fernandoulopeslopes-boop's Machina: AMBIENTE AVANÇADO ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide", initial_sidebar_state="expanded")

# CSS: Calibragem 116px, Mini-Buttons e Estética Industrial
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
    .min-btn-grid div.stButton > button {
        width: 52px !important;
        height: 32px !important;
        font-size: 10px !important;
        margin: 1px !important;
    }
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        background-color: #000;
        color: #00ff00;
        font-size: 18px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE ESTADO ---
if 'page' not in st.session_state: st.session_state.page = "POESIA"
if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = 42
if 'last_tema' not in st.session_state: st.session_state.last_tema = ""
if 'output' not in st.session_state: st.session_state.output = ""

# --- O PALCO SUPERIOR (ESTRUTURA REAL) ---

# 1. NAVEGAÇÃO DE FLUXO (+ < * > ? @) - NO TOPO
c_nav = st.columns(6)
ops = ["+", "<", "*", ">", "?", "@"]
for i, op in enumerate(ops):
    with c_nav[i]:
        if st.button(op, key=f"nav_{op}"):
            if op == "*" and st.session_state.last_tema:
                st.session_state.seed_eureka = random.randint(1000, 9999)
                st.session_state.output = gera_poema(st.session_state.last_tema, st.session_state.seed_eureka)
                st.rerun()

# 2. NAVEGAÇÃO DE PÁGINAS - ABAIXO DO FLUXO
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
        tema = st.text_input("INPUT", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="TEMA...")
        if st.button("GERAR POESIA"):
            if tema:
                st.session_state.last_tema = tema
                st.session_state.output = gera_poema(tema.lower().strip(), st.session_state.seed_eureka)
        
        st.text_area("", value=st.session_state.output, height=600, label_visibility="collapsed")

    with c_var:
        st.markdown("**VARS**")
        for v in range(1, 11):
            if st.button(f"v{v}", key=f"v_p_{v}"):
                st.session_state.seed_eureka = v
                if st.session_state.last_tema:
                    st.session_state.output = gera_poema(st.session_state.last_tema, st.session_state.seed_eureka)
                    st.rerun()

elif st.session_state.page == "page_mini":
    # A PÁGINA MINI JÁ ESTRUTURADA
    st.subheader("📟 page_mini: TEMAS NO PALCO")
    
    # Listagem automática de temas para facilitar a navegação
    try:
        lista_temas = [f.replace(".txt", "").replace(".ypo", "") for f in os.listdir("temas") if f.endswith((".txt", ".ypo"))]
    except:
        lista_temas = []

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("**BIBLIOTECA**")
        for t in lista_temas[:15]: # Limite para não poluir
            if st.button(t, key=f"mini_t_{t}"):
                st.session_state.last_tema = t
                st.rerun()
    
    with c2:
        if st.session_state.last_tema:
            res_mini = gera_poema(st.session_state.last_tema, st.session_state.seed_eureka)
            st.text_area("MINI_OUTPUT", value=res_mini, height=500, label_visibility="collapsed")

# --- MANDALA ---
st.markdown("---")
st.markdown("✨ *Mandala: @fernandoulopeslopes-boop's Machina ativa e estruturada.*")
