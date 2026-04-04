import streamlit as st
import os
import random

# --- @fernandoulopeslopes-boop's Machina: AMBIENTE 05:00 AM ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide", initial_sidebar_state="expanded")

# CSS: Calibragem 116px, Mini-Buttons e Terminal de Saída
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
        background-color: #0e1117;
        color: #00ff00;
        font-size: 16px;
        border: 1px solid #333;
    }
    [data-testid="stSidebar"] {
        width: 280px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE ESTADO ---
if 'page' not in st.session_state:
    st.session_state.page = "POESIA"
if 'last_tema' not in st.session_state:
    st.session_state.last_tema = ""
if 'output' not in st.session_state:
    st.session_state.output = ""

@st.cache_data
def abre(tema_alvo):
    base_path = os.path.dirname(os.path.abspath(__file__))
    # Caminho corrigido para o ambiente de deploy
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

# --- SIDEBAR (CONTROLE DE FLUXO) ---
with st.sidebar:
    st.title("🌀 yPoemas")
    st.markdown("### Machina v.2.3.8")
    st.markdown("---")
    st.write(f"INTERFACE: {st.session_state.page}")
    st.write(f"TARGET: {st.session_state.last_tema}")
    st.markdown("---")
    if st.button("RELOAD SYSTEM", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# --- NAVEGADORES DE PALCO ---

# Nível 1: Páginas (116px)
p_cols = st.columns(6)
pages = ["POESIA", "MINI", "VOZ", "SOBRE", "CONFIG", "HELP"]
for i, p in enumerate(pages):
    with p_cols[i]:
        if st.button(p, key=f"pg_{p}"):
            st.session_state.page = p

# Nível 2: Operações
t_cols = st.columns(6)
ops = ["+", "<", "*", ">", "?", "@"]
for i, op in enumerate(ops):
    with t_cols[i]:
        if st.button(op, key=f"op_{op}"):
            st.session_state.last_op = op

st.markdown("---")

# --- LÓGICA DE EXECUÇÃO ---

if st.session_state.page == "POESIA":
    c_main, c_var = st.columns([5, 1])
    
    with c_main:
        tema = st.text_input("INPUT", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="TEMA...")
        
        if st.button("EXECUTAR", use_container_width=True):
            if tema:
                st.session_state.last_tema = tema
                raw = abre(tema.lower().strip())
                if raw:
                    st.session_state.output = processa(raw)
                else:
                    st.session_state.output = f"SYSTEM_ERROR: {tema}.txt NOT FOUND"

        st.text_area("", value=st.session_state.output, height=600, label_visibility="collapsed")

    with c_var:
        st.markdown("**VARS**")
        st.markdown('<div class="min-btn-grid">', unsafe_allow_html=True)
        for i in range(1, 9):
            if st.button(f"v{i}", key=f"v_m_{i}"):
                pass
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "MINI":
    st.subheader("📟 MINI_VIEW")
    col_m1, col_m2 = st.columns([1, 2])
    with col_m1:
        m_in = st.text_input("M_TARGET", key="mini_in", label_visibility="collapsed")
        st.button("RAND", key="m_rand")
    with col_m2:
        if m_in:
            res_m = abre(m_in.lower().strip())
            st.text_area("", value=processa(res_m), height=400, label_visibility="collapsed")

elif st.session_state.page == "VOZ":
    st.title("🎙️ VOICE_MODULE")
    st.write("Aguardando gTTS...")

# --- MANDALA ---
st.markdown("---")
st.markdown("✨ *Mandala: @fernandoulopeslopes-boop's Machina*")
