import streamlit as st
import os
import random

# Tentar importar o seu motor, mas sem travar o app se ele falhar
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(t, s): return f"ERRO: Arquivo lay_2_ypo.py não encontrado no GitHub. Tema: {t}"

# --- CONFIGURAÇÃO CLARA (SAINDO DO PRETO ABSOLUTO) ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide")

st.markdown("""
    <style>
    /* Forçar um fundo cinza escuro, não preto, para ver se o CSS atualiza */
    .stApp {
        background-color: #1a1a1a !important;
    }
    div.stButton > button {
        width: 116px !important;
        height: 42px !important;
        background-color: #333 !important;
        color: #00ff00 !important;
        border: 1px solid #555 !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE ESTADO ---
if 'count' not in st.session_state: st.session_state.count = 0
if 'page' not in st.session_state: st.session_state.page = "POESIA"
if 'last_tema' not in st.session_state: st.session_state.last_tema = ""
if 'output' not in st.session_state: st.session_state.output = ""

# --- CABEÇALHO DE TESTE ---
st.sidebar.write(f"SISTEMA ATIVO: {st.session_state.count}")
if st.sidebar.button("FORÇAR RECARGA"):
    st.session_state.count += 1
    st.rerun()

# --- NAVEGAÇÃO SUPERIOR (EXPLÍCITA) ---
c1 = st.columns(6)
with c1[0]: 
    if st.button("+"): st.session_state.count += 1
with c1[1]: 
    if st.button("<"): st.session_state.count -= 1
with c1[2]: 
    if st.button("*"): 
        st.session_state.output = gera_poema("random", random.randint(1, 999))
        st.rerun()
with c1[3]: 
    if st.button(">"): pass
with c1[4]: 
    if st.button("?"): st.session_state.page = "AJUDA"
with c1[5]: 
    if st.button("@"): st.session_state.page = "CONFIG"

c2 = st.columns(6)
with c2[0]:
    if st.button("POESIA"): st.session_state.page = "POESIA"
with c2[1]:
    if st.button("page_mini"): st.session_state.page = "page_mini"

st.markdown("---")

# --- ÁREA DE TRABALHO ---
if st.session_state.page == "POESIA":
    tema = st.text_input("TEMA", value=st.session_state.last_tema, label_visibility="collapsed")
    if st.button("EXECUTAR"):
        if tema:
            st.session_state.last_tema = tema
            st.session_state.output = gera_poema(tema, 42)
    
    st.text_area("PALCO", value=st.session_state.output, height=500, label_visibility="collapsed")

elif st.session_state.page == "page_mini":
    st.write("### MÓDULO MINI ATIVO")
    if st.button("VOLTAR"):
        st.session_state.page = "POESIA"
        st.rerun()
