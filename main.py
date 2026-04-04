import streamlit as st
import random
import os

# --- 1. O AVISO QUE VOCÊ VAI LER (ESTÁ NO TOPO ABSOLUTO) ---
st.error("LOG DE SINCRONIA: [ VERSÃO 04-ABRIL-15H ] ATIVA")
st.sidebar.info("MANDALA ATIVA: Verificando Versão do GitHub")

# --- 2. IMPORTAÇÃO DO MOTOR ---
try:
    from lay_2_ypo import gera_poema
except Exception as e:
    st.error(f"ERRO CRÍTICO NO MOTOR: {e}")
    def gera_poema(t, s): return "MOTOR OFFLINE"

# --- 3. CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide")

# CSS para garantir que a interface apareça mesmo com fundo escuro
st.markdown("""
    <style>
    .stApp { background-color: #111; }
    div.stButton > button {
        width: 116px !important;
        height: 42px !important;
        background-color: #333;
        color: #00ff00;
        border: 1px solid #444;
        font-weight: bold;
    }
    .stTextArea textarea {
        background-color: #050505;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. SISTEMA DE ESTADO ---
if 'output' not in st.session_state: st.session_state.output = ""
if 'last_tema' not in st.session_state: st.session_state.last_tema = ""
if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = "42"

# --- 5. O PALCO DE COMANDO ---

# Linha de Navegação (+ < * > ? @)
c_nav = st.columns(6)
with c_nav[0]: st.button("+")
with c_nav[1]: st.button("<")
with c_nav[2]: 
    if st.button("*"): 
        # BLINDAGEM: Transformando o número em STRING antes de enviar
        nova_seed = str(random.randint(1000, 9999))
        st.session_state.seed_eureka = nova_seed
        if st.session_state.last_tema:
            st.session_state.output = gera_poema(st.session_state.last_tema, nova_seed)
        st.rerun()
with c_nav[3]: st.button(">")
with c_nav[4]: st.button("?")
with c_nav[5]: st.button("@")

st.markdown("---")

# Área de Input e Palco Principal
c_main, c_vars = st.columns([5, 1])

with c_main:
    tema = st.text_input("INPUT", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="TEMA...")
    if st.button("GERAR POESIA"):
        if tema:
            st.session_state.last_tema = tema
            # BLINDAGEM: Garantindo que a semente saia como string
            st.session_state.output = gera_poema(tema.lower().strip(), str(st.session_state.seed_eureka))
    
    st.text_area("PALCO", value=st.session_state.output, height=600, label_visibility="collapsed")

with c_vars:
    st.write("**VARS**")
    for v in range(1, 11):
        if st.button(f"v{v}"):
            st.session_state.seed_eureka = str(v)
            if st.session_state.last_tema:
                st.session_state.output = gera_poema(st.session_state.last_tema, str(v))
            st.rerun()

# --- MANDALA FINAL ---
st.markdown("---")
st.caption("Machina Recalibrada - @fernandoulopeslopes-boop")
