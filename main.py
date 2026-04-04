import streamlit as st
import os
# A IMPORTAÇÃO CRUCIAL QUE EU ESTAVA IGNORANDO:
from lay_2_ipo import gera_poema

# --- @fernandoulopeslopes-boop's Machina: AMBIENTE MODULAR ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide", initial_sidebar_state="expanded")

# CSS: Calibragem 116px e Estética Industrial
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
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÃO DE CARREGAMENTO (CONFORME EXPLICADO) ---
def load_poema(tema, seed):
    """
    Busca o arquivo e utiliza a seed para a geração 
    via módulo externo lay_2_ipo.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_name = os.path.join(base_path, "temas", f"{tema}.txt")
    try:
        with open(full_name, encoding="utf-8") as file:
            conteudo = file.read()
            # Aqui entra a lógica que você mencionou:
            return gera_poema(conteudo, seed)
    except FileNotFoundError:
        return f"SISTEMA: {tema}.txt não localizado."

# --- SISTEMA DE ESTADO ---
if 'page' not in st.session_state:
    st.session_state.page = "POESIA"
if 'last_tema' not in st.session_state:
    st.session_state.last_tema = ""
if 'seed' not in st.session_state:
    st.session_state.seed = 42

# --- SIDEBAR ---
with st.sidebar:
    st.title("🌀 yPoemas")
    st.write(f"**MODO:** {st.session_state.page}")
    st.markdown("---")
    if st.button("RELOAD"):
        st.cache_data.clear()
        st.rerun()

# --- NAVEGADORES (O PALCO SUPERIOR) ---
p_cols = st.columns(6)
pages = ["POESIA", "page_mini", "SOBRE", "AJUDA", "CONFIG"]
for i, p in enumerate(pages):
    with p_cols[i]:
        if st.button(p, key=f"pg_{p}"):
            st.session_state.page = p

t_cols = st.columns(6)
ops = ["+", "<", "*", ">", "?", "@"]
for i, op in enumerate(ops):
    with t_cols[i]:
        if st.button(op, key=f"op_{op}"):
            # Lógica de operação (More, Last, Rand...)
            if op == "*": st.session_state.seed = random.randint(0, 9999)

st.markdown("---")

# --- LÓGICA DAS PÁGINAS ---

if st.session_state.page == "POESIA":
    c_main, c_var = st.columns([5, 1])
    with c_main:
        tema = st.text_input("INPUT", value=st.session_state.last_tema, label_visibility="collapsed")
        if st.button("GERAR POESIA"):
            if tema:
                st.session_state.last_tema = tema
                st.session_state.output = load_poema(tema.lower().strip(), st.session_state.seed)
        
        if 'output' in st.session_state:
            st.text_area("", value=st.session_state.output, height=600, label_visibility="collapsed")

    with c_var:
        st.markdown("**VARS**")
        for i in range(1, 11):
            if st.button(f"v{i}", key=f"v_main_{i}"):
                st.session_state.seed = i
                st.rerun()

elif st.session_state.page == "page_mini":
    # A página Mini com temas aparecendo no palco
    st.subheader("📟 page_mini")
    # Grid de temas ou seleção rápida
    m_tema = st.text_input("M_TARGET", key="mini_in", label_visibility="collapsed")
    if m_tema:
        output_mini = load_poema(m_tema.lower().strip(), st.session_state.seed)
        st.text_area("", value=output_mini, height=400, label_visibility="collapsed")

# --- MANDALA ---
st.markdown("---")
st.markdown("✨ *Mandala: @fernandoulopeslopes-boop's Machina*")
