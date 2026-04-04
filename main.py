import streamlit as st
import os
import random

# --- @fernandoulopeslopes-boop's Machina: STATUS ESTÁVEL ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide", initial_sidebar_state="expanded")

# CSS: Calibragem 116px e Estética de Terminal (Verde no Preto)
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
        background-color: #0e1117;
        color: #00ff00;
        font-size: 16px;
        border: 1px solid #333;
        line-height: 1.5;
    }
    [data-testid="stSidebar"] {
        width: 280px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE ESTADO (PERSISTÊNCIA) ---
if 'page' not in st.session_state:
    st.session_state.page = "POESIA"
if 'last_tema' not in st.session_state:
    st.session_state.last_tema = ""
if 'output' not in st.session_state:
    st.session_state.output = ""

@st.cache_data
def abre(tema_alvo):
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_name = os.path.join(base_path, "temas", f"{tema_alvo}.txt")
    try:
        with open(full_name, encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return None

def processa(conteudo):
    if not conteudo: return ""
    linhas = [l.strip() for l in conteudo.strip().split('\n') if l.strip()]
    random.shuffle(linhas)
    return "\n".join(linhas)

# --- SIDEBAR (CONTROLE) ---
with st.sidebar:
    st.title("🌀 yPoemas")
    st.markdown("### @fernandoulopeslopes-boop's Machina")
    st.markdown("---")
    st.write(f"PÁGINA: {st.session_state.page}")
    st.write(f"TEMA: {st.session_state.last_tema}")
    st.markdown("---")
    if st.button("RELOAD"):
        st.cache_data.clear()
        st.rerun()

# --- NAVEGADORES ---

# Camada 1: Páginas (116px)
p_cols = st.columns(6)
with p_cols[0]:
    if st.button("POESIA"): st.session_state.page = "POESIA"
with p_cols[1]:
    if st.button("page_mini"): st.session_state.page = "page_mini"
with p_cols[2]:
    if st.button("SOBRE"): st.session_state.page = "SOBRE"
with p_cols[3]:
    if st.button("AJUDA"): st.session_state.page = "AJUDA"
with p_cols[4]:
    if st.button("CONFIG"): st.session_state.page = "CONFIG"

# Camada 2: Operações de Tema (+ < * > ? @)
t_cols = st.columns(6)
with t_cols[0]: st.button("+")
with t_cols[1]: st.button("<")
with t_cols[2]: st.button("*")
with t_cols[3]: st.button(">")
with t_cols[4]: st.button("?")
with t_cols[5]: st.button("@")

st.markdown("---")

# --- LÓGICA DE EXECUÇÃO ---

if st.session_state.page == "POESIA":
    c_main, c_var = st.columns([5, 1])
    
    with c_main:
        # Palco Limpo (Input sem label)
        tema = st.text_input("INPUT", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="TEMA...")
        
        if st.button("GERAR POESIA"):
            if tema:
                st.session_state.last_tema = tema
                raw = abre(tema.lower().strip())
                if raw:
                    st.session_state.output = processa(raw)
                else:
                    st.session_state.output = f"ERRO: {tema}.txt NÃO ENCONTRADO"

        st.text_area("", value=st.session_state.output, height=600, label_visibility="collapsed")

    with c_var:
        st.markdown("**VARS**")
        for i in range(1, 11):
            if st.button(f"v{i}", key=f"v_p_{i}"):
                pass

elif st.session_state.page == "page_mini":
    st.subheader("📟 page_mini")
    col_m1, col_m2 = st.columns([1, 2])
    with col_m1:
        m_in = st.text_input("M_TARGET", key="mini_in", label_visibility="collapsed")
        st.button("RAND", key="m_rand")
    with col_m2:
        if m_in:
            res_m = abre(m_in.lower().strip())
            st.text_area("", value=processa(res_m), height=400, label_visibility="collapsed")

# --- MANDALA ---
st.markdown("---")
st.markdown("✨ *Mandala: @fernandoulopeslopes-boop's Machina*")
