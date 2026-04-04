import streamlit as st
import os
import random

# --- @fernandoulopeslopes-boop's Machina: DEPLOY REAL ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide", initial_sidebar_state="expanded")

# CSS: Precisão 116px e Fontes Mono
st.markdown("""
    <style>
    div.stButton > button {
        width: 116px !important;
        height: 42px !important;
        border-radius: 0px;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
    }
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        background-color: #0e1117;
        color: #00ff00;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ESTADO ---
if 'page' not in st.session_state:
    st.session_state.page = "POESIA"
if 'last_tema' not in st.session_state:
    st.session_state.last_tema = ""
if 'output' not in st.session_state:
    st.session_state.output = ""

def carregar_tema(t):
    path = f"temas/{t}.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            linhas = [l.strip() for l in f.readlines() if l.strip()]
            random.shuffle(linhas)
            return "\n".join(linhas)
    return f"SISTEMA: {t}.txt não localizado."

# --- A ESTRUTURA DO PALCO (O QUE ESTAVA ACIMA) ---

# 1. BOTÕES DE NAVEGAÇÃO DE FLUXO (O TOPO)
c_nav = st.columns(6)
ops = ["+", "<", "*", ">", "?", "@"]
for i, op in enumerate(ops):
    with c_nav[i]:
        if st.button(op, key=f"nav_{op}"):
            # Lógica de permutação imediata no '*'
            if op == "*" and st.session_state.last_tema:
                st.session_state.output = carregar_tema(st.session_state.last_tema)

# 2. BOTÕES DE NAVEGAÇÃO PELAS PÁGINAS (LOGO ABAIXO)
c_pg = st.columns(6)
pages = ["POESIA", "page_mini", "SOBRE", "AJUDA", "CONFIG"]
for i, p in enumerate(pages):
    with c_pg[i]:
        if st.button(p, key=f"pg_{p}"):
            st.session_state.page = p

st.markdown("---")

# --- ÁREA DE TRABALHO ---

if st.session_state.page == "POESIA":
    col_main, col_vars = st.columns([5, 1])
    
    with col_main:
        # Input do Tema
        tema = st.text_input("TEMA", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="TEMA...")
        
        if st.button("GERAR"):
            if tema:
                st.session_state.last_tema = tema
                st.session_state.output = carregar_tema(tema.lower().strip())
        
        st.text_area("", value=st.session_state.output, height=600, label_visibility="collapsed")

    with col_vars:
        st.markdown("**VARS**")
        for i in range(1, 11):
            if st.button(f"v{i}"):
                pass

elif st.session_state.page == "page_mini":
    st.subheader("📟 page_mini")
    m_in = st.text_input("MINI_TARGET", key="mini_in", label_visibility="collapsed")
    if m_in:
        st.text_area("", value=carregar_tema(m_in.lower()), height=400, label_visibility="collapsed")

# --- MANDALA ---
st.markdown("---")
st.markdown("✨ *Mandala: @fernandoulopeslopes-boop's Machina*")
