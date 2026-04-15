import streamlit as st
import os
import random

# MOTOR REAL
try: 
    from lay_2_ypo import gera_poema
except Exception: 
    def gera_poema(t, p=""): 
        return ["Erro: motor não encontrado."]

# --- 1. BOOT & ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

for key, val in {
    'page': 'demo', 
    'show_help': False, 
    'ID_CLIC': 'demo', 
    'idx_tema': 0, 
    'temas_atuais': []
}.items():
    if key not in st.session_state: 
        st.session_state[key] = val

def nav_to(p):
    st.session_state.page = p
    st.session_state.show_help = False
    st.session_state.ID_CLIC = p

def prox_tema():
    if st.session_state.temas_atuais:
        st.session_state.idx_tema = (st.session_state.idx_tema + 1) % len(st.session_state.temas_atuais)

def ante_tema():
    if st.session_state.temas_atuais:
        st.session_state.idx_tema = (st.session_state.idx_tema - 1) % len(st.session_state.temas_atuais)

# --- 2. CSS: RIGOR ABSOLUTO DE POSICIONAMENTO ---
st.markdown("""
<style>
    /* Trava o scroll da página inteira */
    html, body, [data-testid="stAppViewContainer"] { 
        overflow: hidden !important; 
        height: 100vh;
        margin: 0;
    }
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 0rem !important;}

    /* Painel Lateral Esquerdo Fixo */
    .sidebar-fixa {
        position: fixed;
        top: 20px;
        left: 20px;
        width: 240px;
        height: 95vh;
        z-index: 1000;
        background: #f9f9f9;
        padding: 15px;
        border-right: 1px solid #eee;
    }

    /* Topo Fixo */
    .topo-fixo {
        position: fixed;
        top: 0;
        left: 280px;
        right: 0;
        height: 120px;
        z-index: 999;
        background: white;
        padding: 20px;
    }

    /* PALCO COM SCROLL EXCLUSIVO */
    .palco-container {
        position: absolute;
        top: 130px;
        left: 280px;
        right: 20px;
        bottom: 20px;
        overflow-y: auto !important;
        padding: 20px;
        background: transparent;
    }

    /* Alinhamento da Star Mestra */
    .star-mestra-btn button {
        background: transparent !important;
        border: none !important;
        color: #f1c40f !important;
        font-size: 2rem !important;
        line-height: 1;
    }

    /* Estilo dos Versos */
    .typo-verse { 
        font-family: 'Georgia', serif; 
        font-size: 1.65rem; 
        line-height: 1.6; 
        color: #1a1a1a; 
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & HELP ---
@st.cache_data
def get_help_text(id_clic):
    path = f"docs/help_{id_clic}.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f: return f.read()
    return f"Manual aguardando conteúdo: help_{id_clic}.txt"

@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = get_acervo()

# --- 4. RENDERIZAÇÃO DA INTERFACE ---

# COLUNA 1: SIDEBAR FIXA
st.markdown('<div class="sidebar-fixa">', unsafe_allow_html=True)
st.write("### CONTROLES")
c_btns = st.columns(3)
c_btns[0].button("🔈\nSom")
c_btns[1].button("🎨\nArte")
c_btns[2].button("🎬\nVídeo")
st.divider()

livro_sel = st.selectbox("Livros", list(ACERVO.keys()) if ACERVO else ["-"], key="sl")
if ACERVO:
    with open(os.path.join("base", ACERVO[livro_sel]), "r", encoding="utf-8") as f:
        temas_disco = [l.strip() for l in f if l.strip()]
        if temas_disco != st.session_state.temas_atuais:
            st.session_state.temas_atuais = temas_disco
            st.session_state.idx_tema = 0

st.selectbox("Temas", st.session_state.temas_atuais, 
             index=min(st.session_state.idx_tema, len(st.session_state.temas_atuais)-1),
             key="st_combo", on_change=lambda: st.session_state.update({"idx_tema": st.session_state.temas_atuais.index(st.session_state.st_combo)}))
st.selectbox("Idioma", ["Português", "English", "Español", "Deutsch", "Français"], key="si")
st.markdown('</div>', unsafe_allow_html=True)

# COLUNA 2: TOPO E PALCO
# 1. Topo Balanceado
st.markdown('<div class="topo-fixo">', unsafe_allow_html=True)
cols = st.columns([1, 1, 1, 0.5, 1, 1, 1])
pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]

if cols[0].button(pgs[0], key="top_0"): nav_to(pgs[0])
if cols[1].button(pgs[1], key="top_1"): nav_to(pgs[1])
if cols[2].button(pgs[2], key="top_2"): nav_to(pgs[2])

with cols[3]:
    st.markdown('<div class="star-mestra-btn">', unsafe_allow_html=True)
    if st.button("★", key="master_star"):
        st.session_state.show_help = not st.session_state.show_help
    st.markdown('</div>', unsafe_allow_html=True)

if cols[4].button(pgs[3], key="top_3"): nav_to(pgs[3])
if cols[5].button(pgs[4], key="top_4"): nav_to(pgs[4])
if cols[6].button(pgs[5], key="top_5"): nav_to(pgs[5])

# Régua de Navegação [ < * > ]
_, c_nav, _ = st.columns([2, 3, 2])
with c_nav:
    n_btns = st.columns(4)
    n_btns[0].button("➕")
    if n_btns[1].button("◀"): ante_tema()
    n_btns[2].button("🎲")
    if n_btns[3].button("▶"): prox_tema()
st.markdown('</div>', unsafe_allow_html=True)

# 2. Palco de Conteúdo
st.markdown('<div class="palco-container">', unsafe_allow_html=True)
if st.session_state.show_help:
    ctx = st.session_state.ID_CLIC
    st.markdown(f"## AJUDA: {ctx.upper()}")
    st.markdown(get_help_text(ctx))
    if st.button("FECHAR AJUDA"):
        st.session_state.show_help = False
        st.rerun()
else:
    p = st.session_state.page
    st.session_state.ID_CLIC = p
    
    if p == "demo":
        if st.session_state.temas_atuais:
            try:
                tema_alvo = st.session_state.temas_atuais[st.session_state.idx_tema]
                poema = gera_poema(tema_alvo, "")
                for v in poema:
                    if v == '\n': st.write("")
                    else: st.markdown(f'<div class="typo-verse">{v}</div>', unsafe_allow_html=True)
            except Exception as e: 
                st.error(f"Erro no Motor: {e}")
    else:
        st.write(f"### Ambiente {p.upper()}")
        st.info(f"ID_CLIC focado em '{p}'. Clique na estrela para ver as instruções.")
st.markdown('</div>', unsafe_allow_html=True)
