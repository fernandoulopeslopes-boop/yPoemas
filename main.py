import streamlit as st
import os

# --- 1. BOOT & ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'show_help' not in st.session_state: st.session_state.show_help = False

# Callback vital para a funcionalidade
def trigger_nav(p, h):
    st.session_state.page = p
    st.session_state.show_help = h

# --- 2. CSS DE FORÇA BRUTA (ESTRELAS OURO) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}
    
    /* Painel Lateral Fixo */
    [data-testid="column"]:nth-child(1) {
        position: fixed !important;
        top: 1rem; left: 1rem; width: 185px !important; z-index: 1001;
    }
    [data-testid="column"]:nth-child(3) { margin-left: 215px !important; }

    /* ESTRELAS OURO (#FFD700) */
    div.bottom-star button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        height: 40px !important;
    }
    
    /* Atacando o elemento de texto do botão diretamente */
    div.bottom-star button div[data-testid="stMarkdownContainer"] p {
        color: #FFD700 !important;
        font-size: 35px !important;
        font-weight: 900 !important;
        -webkit-text-fill-color: #FFD700 !important;
        line-height: 1 !important;
    }

    .scroll-stage {
        height: 75vh;
        overflow-y: auto;
        padding: 10px;
        border-top: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. ACERVO ---
@st.cache_data
def load_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = load_acervo()
IDIOMAS = ["Português", "Español
