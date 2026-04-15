import streamlit as st
import os
import random
from deep_translator import GoogleTranslator

# MOTOR REAL: Importação mandatória
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(tema, p=""): return ["Erro: lay_2_ypo.py não encontrado."]

# --- 1. BOOT & ESTADO (A CHAVE DA NAVEGAÇÃO) ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'show_help' not in st.session_state: st.session_state.show_help = False
if 'idx_tema' not in st.session_state: st.session_state.idx_tema = 0
if 'temas_atuais' not in st.session_state: st.session_state.temas_atuais = []

def nav_to(p, h):
    st.session_state.page = p
    st.session_state.show_help = h

# --- 2. CSS: ALINHAMENTO E LYPO-TYPO ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}
    
    /* Painel Lateral Fixo */
    [data-testid="column"]:nth-child(1) {
        position: fixed !important; top: 1rem; left: 1rem; width: 210px !important; z-index: 1000;
    }
    
    /* Palco de Conteúdo */
    [data-testid="column"]:nth-child(3) { margin-left: 250px !important; }

    /* LYPO & TYPO: Preservação Estética */
    .lypo-container { margin-top: 20px; }
    .typo-verse { 
        font-family: 'Georgia', serif; 
        font-size: 1.65rem; 
        line-height: 1.7; 
        color: #1a1a1a; 
        min-height: 1.5rem;
    }

    /* Régua de Navegação [ + < * > ? ] */
    .nav-rim-box button {
        background: transparent !important;
        border: none !important;
        font-size: 1.3rem !important;
        color: #777 !important;
    }
    .nav-rim-box button:hover { color: #000 !important; }
    
    .stButton button { width: 100% !important; height: 38px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & TRADUÇÃO ---
@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

def traduzir_poema(lista_versos, destino):
    mapa = {"Português": "pt", "Español": "es", "English": "en", "Deutsch": "de", "Français": "fr", "Italiano": "it"}
    target = mapa.get(destino, "pt")
    if target == "pt": return lista_versos
    try:
        translator = GoogleTranslator(source='auto', target=target)
        return [translator.translate(v) if v.strip() and v != '\n' else v for v in lista_versos]
    except: return lista_versos

ACERVO = get_acervo()
IDIOMAS = ["Português", "Español", "English", "Deutsch", "Français", "Italiano"]

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2, 0.1, 7.9])

with c1:
    st.write("### controles")
    ic = st.columns(3)
    ic[0].button("🔈", key="v_on")
    ic[1].button("🎨", key="a_on")
    ic[2].button("🎬", key="m_on")
    st.divider()
    
    livro_sel = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"], key="sl")
    
    # Gestão da lista de temas por estado
    if ACERVO:
        with open(os.path.join("base", ACERVO[livro_sel]), "r", encoding="utf-8") as f:
            novos_temas = [l.strip() for l in f if l.strip()]
            if novos_temas != st.session_state.temas_atuais:
                st.session_state.temas_atuais = novos_temas
                st.session_state.idx_tema = 0
    
    # Selectbox reflete o estado idx_tema
    tema_atual = st.selectbox("temas", st.session_state.temas_atuais, 
                              index=min(st.session_state.idx_tema, len(st.session_state.temas_atuais)-1),
                              key="st_box")
    st.session_state.idx_tema = st.session_state.temas_atuais.index(tema_atual)
    
    i_sel = st.selectbox("idioma", IDIOMAS, key="si")

with c2:
    pesos = [0.8, 0.9, 0.8, 1.2, 1.0, 0.8]
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    # Navegação Superior
    cn = st.columns(pesos); cs = st.columns(pesos)
    for i, p in enumerate(pgs):
        cn[i].button(p.lower() if p != "yPoemas" else p, key=f"n_{i}", on_click=nav_to, args=(p, False))
        cs[i].button("★", key=f"s_{i}", on_click=nav_to, args=(p, True))

    # RÉGUA [ + < * > ? ] CENTRADA (Sob Eureka/Off-Mach)
    st.markdown('<div class="nav-rim-box">', unsafe_allow_html=True)
    _, col_cent, _ = st.columns([2.5, 5, 2.5])
    with col_cent:
        bn = st.columns(5)
        if bn[0].button("+"): pass
        if bn[1].button("<"): # Voltar
            st.session_state.idx_tema = (st.session_state.idx_tema - 1) % len(st.session_state.temas_atuais)
            st.rerun()
        if bn[2].button("*"): # Random
            st.session_state.idx_tema = random.randint(0, len(st.session_state.temas_atuais)-1)
            st.rerun()
        if bn[3].button(">"): # Próximo
            st.session_state.idx_tema = (st.session_state.idx_tema + 1) % len(st.session_state.temas_atuais)
            st.rerun()
        if bn[4].button("?"): nav_to(st.session_state.page, True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # --- 5. RENDERIZAÇÃO LYPO-TYPO (O LIVRO SEM FIM) ---
    p_atual = st.session_state.page
    h_mode = st.session_state.show_help

    if p_atual == "demo" and not h_mode:
        tema_final = st.session_state.temas_atuais[st.session_state.idx_tema]
        
        # Chamada ao motor
        poema_bruto = gera_poema(tema_final, "")
        versos_exibicao = traduzir_poema(poema_bruto, i_sel)

        st.markdown('<div class="lypo-container">', unsafe_allow_html=True)
        for verso in versos_exibicao:
            if verso == '\n':
                st.write("") 
            else:
                st.markdown(f'<div class="typo-verse">{verso}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
