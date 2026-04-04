import streamlit as st
import os
import random
from lay_2_ypo import gera_poema

# --- CONFIGURAÇÃO @fernandoulopeslopes-boop ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide", initial_sidebar_state="expanded")

# CSS: Reset de Interface (Removendo o "Fantasma" do fundo absoluto)
st.markdown("""
    <style>
    .stApp {
        background-color: #111; 
    }
    div.stButton > button {
        width: 116px !important;
        height: 42px !important;
        border-radius: 0px;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        background-color: #222;
        color: #eee;
        border: 1px solid #444;
    }
    div.stButton > button:hover {
        border-color: #00ff00;
        color: #00ff00;
    }
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        background-color: #050505;
        color: #00ff00;
        font-size: 19px;
        border: 1px solid #111;
    }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE ESTADO ---
if 'page' not in st.session_state: st.session_state.page = "POESIA"
if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = 42
if 'last_tema' not in st.session_state: st.session_state.last_tema = ""
if 'output' not in st.session_state: st.session_state.output = ""

# --- PALCO SUPERIOR: COMANDO FIXO ---

# Linha 1: Operadores de Fluxo (Explícitos)
c1 = st.columns(6)
with c1[0]: 
    if st.button("+"): pass
with c1[1]: 
    if st.button("<"): pass
with c1[2]: 
    if st.button("*"): 
        st.session_state.seed_eureka = random.randint(1000, 9999)
        if st.session_state.last_tema:
            st.session_state.output = gera_poema(st.session_state.last_tema, st.session_state.seed_eureka)
        st.rerun()
with c1[3]: 
    if st.button(">"): pass
with c1[4]: 
    if st.button("?"): st.session_state.page = "AJUDA"
with c1[5]: 
    if st.button("@"): st.session_state.page = "CONFIG"

# Linha 2: Navegação de Páginas
c2 = st.columns(6)
with c2[0]:
    if st.button("POESIA"): st.session_state.page = "POESIA"
with c2[1]:
    if st.button("page_mini"): st.session_state.page = "page_mini"
with c2[2]:
    if st.button("SOBRE"): st.session_state.page = "SOBRE"
with c2[3]:
    if st.button("AJUDA"): st.session_state.page = "AJUDA"
with c2[4]:
    if st.button("CONFIG"): st.session_state.page = "CONFIG"

st.markdown("---")

# --- CONTEÚDO DINÂMICO ---

if st.session_state.page == "POESIA":
    c_main, c_var = st.columns([5, 1])
    
    with c_main:
        tema = st.text_input("INPUT", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="DIGITE O TEMA...")
        if st.button("GERAR"):
            if tema:
                st.session_state.last_tema = tema
                st.session_state.output = gera_poema(tema.lower().strip(), st.session_state.seed_eureka)
        
        st.text_area("", value=st.session_state.output, height=650, label_visibility="collapsed")

    with c_var:
        st.write("**VARS**")
        for v in range(1, 11):
            if st.button(f"v{v}"):
                st.session_state.seed_eureka = v
                if st.session_state.last_tema:
                    st.session_state.output = gera_poema(st.session_state.last_tema, st.session_state.seed_eureka)
                st.rerun()

elif st.session_state.page == "page_mini":
    st.subheader("📟 Biblioteca de Ítimos")
    
    # Carregamento da pasta /temas
    try:
        itens = [f.split('.')[0] for f in os.listdir("temas") if f.endswith(('.txt', '.ypo'))]
    except:
        itens = []

    cols = st.columns(4)
    for i, t in enumerate(itens[:16]):
        with cols[i % 4]:
            if st.button(t, key=f"m_{t}"):
                st.session_state.last_tema = t
                st.session_state.output = gera_poema(t, st.session_state.seed_eureka)
                st.session_state.page = "POESIA"
                st.rerun()

st.markdown("---")
st.caption("Machina v2.5 - @fernandoulopeslopes-boop")
