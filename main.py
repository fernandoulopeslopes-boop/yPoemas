import streamlit as st
import os

# --- 1. CONFIGURAÇÃO E ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

# Inicialização forçada
if 'page' not in st.session_state:
    st.session_state.page = 'demo'
if 'show_help' not in st.session_state:
    st.session_state.show_help = False

# --- 2. CSS: OURO E PALCO ISOLADO ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important; overflow: hidden !important;}
    
    /* Painel Lateral Fixo */
    [data-testid="column"]:nth-child(1) {
        position: fixed !important;
        top: 1rem;
        left: 1rem;
        width: 200px !important;
        z-index: 1000;
    }
    [data-testid="column"]:nth-child(3) { margin-left: 230px !important; }

    /* Botões de Navegação */
    .stButton button { height: 38px !important; width: 100% !important; }
    
    /* ESTRELAS OURO REAL (#FFD700) */
    div.bottom-star button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        height: 30px !important;
        margin-top: -10px !important;
    }
    div.bottom-star button p { 
        color: #FFD700 !important; 
        font-size: 30px !important; 
        font-weight: bold !important;
        line-height: 1 !important;
    }
    div.bottom-star button:hover p { color: #FFEA00 !important; }

    /* Palco com Scroll Independente */
    .scroll-stage { height: 78vh; overflow-y: auto; padding-right: 15px; }
    .md-render { font-family: 'Georgia', serif; line-height: 1.7; color: #1a1a1a; }
    .md-render blockquote { border-left: 4px solid #FFD700; padding-left: 20px; font-style: italic; color: #444; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS ---
@st.cache_data
def get_acervo():
    p = "base"
    if not os.path.exists(p): return {}
    files = sorted([f for f in os.listdir(p) if f.startswith("rol_") and f.endswith(".txt")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = get_acervo()
IDIOMAS = ["Português", "Español", "English", "Deutsch", "Nederlands", "Français", "Italiano", "Català", "Ελληνικά", "Türkçe", "العربية", "ע Hebrew", "हिन्दी"]

# --- 4. INTERFACE ---
c_painel, _, c_palco = st.columns([2, 0.1, 7.9])

with c_painel:
    st.write("### controles")
    ic1, ic2, ic3 = st.columns(3)
    ic1.button("🔈", key="s_on")
    ic2.button("🎨", key="a_on")
    ic3.button("💬", key="t_on")
    st.divider()
    
    livro_sel = st
