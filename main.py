import streamlit as st
import os
from deep_translator import GoogleTranslator

# Motor Real da Machina
from lay_2_ypo import gera_poema

# --- 1. BOOT & ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'show_help' not in st.session_state: st.session_state.show_help = False

def nav_to(p, h):
    st.session_state.page = p
    st.session_state.show_help = h

# --- 2. CSS: LYPO-TYPO & ESTRUTURA ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}
    
    /* Painel Fixo */
    [data-testid="column"]:nth-child(1) {position: fixed !important; top: 1rem; left: 1rem; width: 200px !important; z-index: 1000;}
    [data-testid="column"]:nth-child(3) {margin-left: 240px !important;}

    /* LYPO & TYPO */
    .lypo-container { margin-top: 10px; }
    .typo-verse { 
        font-family: 'Georgia', serif; 
        font-size: 1.65rem; 
        line-height: 1.5; 
        color: #1a1a1a; 
        min-height: 1.2rem;
    }

    /* Navegação Inferior [ + < * > ? ] */
    .nav-rim button {
        background: transparent !important;
        border: none !important;
        font-size: 1.2rem !important;
        color: #888 !important;
    }
    .nav-rim button:hover { color: #000 !important; }
    
    .stButton button { width: 100% !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & TRADUÇÃO ---
@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

def traduzir_poema(lista_versos, destino):
    mapa = {"Português": "pt", "Español": "es", "English": "en", "Deutsch": "de", "Nederlands": "nl", "Français": "fr", "Italiano": "it", "Català": "ca", "Ελληνικά": "el", "Türkçe": "tr", "العربية": "ar", "ע Hebrew": "he", "हिन्दी": "hi"}
    target = mapa.get(destino, "pt")
    if target == "pt": return lista_versos
    try:
        translator = GoogleTranslator(source='auto', target=target)
        return [translator.translate(v) if v.strip() and v != '\n' else v for v in lista_versos]
    except: return lista_versos

ACERVO = get_acervo()
IDIOMAS = ["Português", "Español", "English", "Deutsch", "Nederlands", "Français", "Italiano", "Català", "Ελληνικά", "Türkçe", "العربية", "ע Hebrew", "हिन्दी"]

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2, 0.1, 7.9])

with c1:
    ic = st.columns(3)
    som = ic[0].button("🔈", key="v_on")
    art = ic[1].button("🎨", key="a_on")
    vid = ic[2].button("🎬", key="m_on")
    st.divider()
    l_sel = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"], key="sl")
    tema_sel = "-"
    if ACERVO:
        with open(os.path.join("base", ACERVO[l_sel]), "r", encoding="utf-8") as f:
            ts = [l.strip() for l in f if l.strip()]
        tema_sel = st.selectbox("temas", ts, key="st")
    i_sel = st.selectbox
