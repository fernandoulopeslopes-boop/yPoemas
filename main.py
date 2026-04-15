import streamlit as st
import os
import random
import base64
from deep_translator import GoogleTranslator

# --- 1. BOOT & ESTADO (PTC) ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

try: 
    from lay_2_ypo import gera_poema
except Exception: 
    def gera_poema(t, p=""): return ["A imprecisão é de berço.", "O motor aguarda."]

# Inicialização de Estados (CC: Fidelidade)
for key, val in {
    'page': 'demo', 'show_help': False, 'idx_tema': 0, 'temas_atuais': []
}.items():
    if key not in st.session_state: st.session_state[key] = val

# --- 2. CSS: A ESTÉTICA DO INSTINTO (CC: NO_EMPTY) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}

    /* TÍTULO À ESQUERDA (Ajuste Final) */
    .typo-title {
        font-family: 'Georgia', serif; font-size: 1.25rem; font-weight: bold;
        text-decoration: underline; text-align: left; margin-bottom: 12px; color: #444;
    }

    /* TEXTO COMPACTO (-20% e entrelinha curta) */
    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.3rem; 
        line-height: 1.3; color: #1a1a1a; margin-bottom: 4px;
    }

    /* BOTÕES DE MÍDIA QUADRADOS E PEQUENOS */
    .media-box div[data-testid="stColumn"] button {
        width: 38px !important; height: 38px !important;
        min-width: 38px !important; padding: 0px !important;
        margin: 0 auto !important; display: block;
    }

    /* BOTÕES DE PÁGINA: HARMONIA FIXA */
    div.stButton > button { width: 100% !important; min-width: 95px; height: 38px !important; }

    /* HELP QUADRADO (Ajuste 2) */
    .st-key-h_btn button { width: 38px !important; min-width: 38px !important; }

    /* NAVEGAÇÃO CIRCULAR SUAVE (Ajuste 3) */
    .st-key-n_p button, .st-key-n_a button, .st-key-n_r button, .st-key-n_n button {
        border-radius: 50% !important;
        width: 48px !important; height: 48px !important;
        min-width: 48px !important;
        background-color: #f9f9f9 !important;
        border: 1px solid #ddd !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & ACERVO (CC: FIDELIDADE) ---
@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    acervo = {}
    for f in files:
        nome = f.replace("rol_", "").replace(".txt", "").replace("_", " ").title()
        if "Haykay" in nome: nome = "HaiCai"
        acervo[nome] = f
    return acervo

ACERVO = get_acervo()

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.4, 7.1])

with c1:
    # MÍDIA (Ajuste 1: Pequenos e funcionais)
    st.markdown('<div class="media-box">', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    if m1.button("🔊", key="m_s"): st.toast("Som: On")
    if m2.button("🎨", key="m_a"): st.toast("Arte: On")
    if m3.button("🎬", key="m_v"): st.toast("Vídeo: On")
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()
    
    # LIVRO INICIAL (Ajuste 1 da sessão anterior)
    lista_l = list(ACERVO.keys())
    ini_l = "Livro Vivo" if "Livro Vivo" in lista_l else (lista_l[0] if lista_l else "-")
    sel_l = st.selectbox("Livros", lista_l, index=lista_l.index(ini_l) if ini_l in lista_l else 0)
    
    if ACERVO:
        with open(os.path.join("base", ACERVO[sel_l]), "r", encoding="utf-8") as f:
            st.session_state.temas_atuais = [l.strip() for l in f if l.strip()]
    
    tot = len(st.session_state.temas_atuais)
    idx = st.session_state.idx_tema % tot if tot > 0 else 0
    st.selectbox("Temas", st.session_state.temas_atuais, index=idx, key="st_combo")
    st.selectbox("Idioma", ["Português", "English", "Español", "Deutsch", "Français", "Italiano", "Latin"], key="l_sel")

with c2:
    # MENU SUPERIOR (Ajuste 2: Help Quadrado e sintonizado)
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    t_cols = st.columns([1, 1, 1, 0.5, 1, 1, 1])
    
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p, key=f"btn_{p}"): st.session_state.page = p
    
    with t_cols[3]:
        if st.button("?", key="h_btn"): st.session_state.show_help = not st.session_state.show_help

    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p, key=f"btn_{p}"): st.session_state.page = p

    # NAVEGAÇÃO CIRCULAR (Ajuste 5)
    st.write("") 
    n_cols = st.columns([2.5, 0.7, 0.7, 0.7, 0.7, 2.5])
    if n_cols[1].button("❮", key="nav_p"): st.session_state.idx_tema -= 1
    if n_cols[2].button("✚", key="nav_a"): st.toast("Semente guardada")
    if n_cols[3].button("✱", key="nav_r"): st.session_state.idx_tema = random.randint(0, tot-1) if tot > 0 else 0
    if n_cols[4].button("❯", key="nav_n"): st.session_state.idx_tema += 1
    st.divider()

    # PALCO (no_empty)
    palco = st.container()
    with palco:
        if st.session_state.show_help:
            st.info("Ajuda da Machina: A precisão agora dança conforme o instinto.")
        
        if st.session_state.page == "demo" and tot > 0:
            tema = st.session_state.temas_atuais[st.session_state.idx_tema % tot]
            st.markdown(f'<div class="typo-title">{tema.upper()}</div>', unsafe_allow_html=True)
            try:
                for v in gera_poema(tema, ""):
                    st.markdown(f'<div class="typo-verse">{v}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Instinto falhou em {tema}: {str(e)}")
        else:
            st.markdown(f"### {st.session_state.page.upper()}")
            
