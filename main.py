import streamlit as st
import os
import random

# --- AMBIENTE @fernandoulopeslopes-boop's Machina ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide", initial_sidebar_state="expanded")

# CSS: Precisão de 116px, Mini-Buttons e Ambiente Industrial/Poético
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
    /* Estilo para os min_buttons da page_mini */
    .min-btn-container div.stButton > button {
        width: 56px !important;
        height: 32px !important;
        font-size: 11px !important;
        margin: 1px !important;
    }
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        background-color: #0e1117;
        color: #00ff00;
        font-size: 15px;
        border: 1px solid #333;
    }
    [data-testid="stSidebar"] {
        width: 260px !important;
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
    """Mecânica de busca no diretório de temas."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_name = os.path.join(base_path, "temas", f"{tema_alvo.txt}")
    try:
        with open(full_name, encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return None

def permuta(conteudo):
    """Mecânica de permutação das variações."""
    if not conteudo: return ""
    linhas = [l.strip() for l in conteudo.strip().split('\n') if l.strip()]
    random.shuffle(linhas)
    return "\n".join(linhas)

# --- SIDEBAR (PAINEL DE CONTROLE) ---
with st.sidebar:
    st.title("🌀 yPoemas")
    st.markdown("### Machina v.238")
    st.markdown("---")
    st.write(f"**STATUS:** {st.session_state.page}")
    st.write(f"**TARGET:** {st.session_state.last_tema}")
    st.markdown("---")
    if st.button("RELOAD / CLEAR"):
        st.cache_data.clear()
        st.rerun()
    st.markdown("---")
    st.info("NEXT: gTTS Integration (VOZ)")

# --- NAVEGADORES (PALCO SUPERIOR) ---

# Linha 1: Navegador de Páginas (Botões de 116px)
p_cols = st.columns(6)
pages = ["POESIA", "MINI", "VOZ", "SOBRE", "CONFIG", "HELP"]
for i, p in enumerate(pages):
    with p_cols[i]:
        if st.button(p, key=f"btn_pg_{p}"):
            st.session_state.page = p

# Linha 2: Navegador de Operação (More / Last / Rand / Nest / Help / Love)
t_cols = st.columns(6)
ops = ["+", "<", "*", ">", "?", "@"]
for i, op in enumerate(ops):
    with t_cols[i]:
        if st.button(op, key=f"btn_op_{op}"):
            st.session_state.last_op = op

st.markdown("---")

# --- LÓGICA DE INTERFACE ---

if st.session_state.page == "POESIA":
    # Palco Principal: Temas e Execução
    c_main, c_var = st.columns([5, 1])
    
    with c_main:
        tema = st.text_input("INPUT", value=st.session_state.last_tema, label_visibility="collapsed", placeholder="TEMA...")
        
        if st.button("EXECUTAR PERMUTAÇÃO", use_container_width=True):
            if tema:
                st.session_state.last_tema = tema
                raw = abre(tema.lower().strip())
                if raw:
                    st.session_state.output = permuta(raw)
                else:
                    st.session_state.output = f"ERROR: {tema}.txt NOT FOUND"

        st.text_area("", value=st.session_state.output, height=580, label_visibility="collapsed")

    with c_var:
        st.markdown("**VAR**")
        st.markdown('<div class="min-btn-container">', unsafe_allow_html=True)
        for v in range(1, 9):
            if st.button(f"v{v}", key=f"v_main_{v}"):
                pass
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "MINI":
    # Estrutura page_mini (Mini View)
    st.subheader("📟 PAGE_MINI")
    col_m1, col_m2 = st.columns([3, 1])
    with col_m1:
        m_in = st.text_input("MINI_IN", key="mini_in", label_visibility="collapsed", placeholder="MINI TEMA...")
        if m_in:
            res = abre(m_in.lower().strip())
            st.text_area("", value=permuta(res), height=350, label_visibility="collapsed")
    with col_m2:
        st.markdown("**MINI CTRL**")
        st.button("v1", key="m_v1")
        st.button("v2", key="m_v2")

elif st.session_state.page == "VOZ":
    st.title("🎙️ Módulo de Voz")
    st.write("Aguardando implementação gTTS...")

# --- MANDALA ---
st.markdown("---")
st.markdown("✨ *A máquina de fazer poesia está ativa. @fernandoulopeslopes-boop*")
