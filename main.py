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

# --- 2. CSS: LIMPEZA E RIGOR VISUAL ---
st.markdown("""
<style>
    /* Bloqueia scroll na página inteira */
    html, body, [data-testid="stAppViewContainer"] { 
        overflow: hidden !important; 
        height: 100vh;
    }
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}
    
    /* Painel Lateral Estático */
    [data-testid="column"]:nth-child(1) { 
        position: fixed !important; top: 1.5rem; left: 1.5rem; width: 220px !important; z-index: 1000; 
    }
    
    /* PALCO COM SCROLL EXCLUSIVO */
    .palco-scroll {
        margin-left: 260px !important; 
        height: calc(100vh - 160px); 
        overflow-y: auto !important;
        padding-right: 20px;
        scrollbar-width: thin;
    }

    /* Alinhamento da Star Mestra */
    .star-mestra-box {
        display: flex; justify-content: center; align-items: center; 
        height: 100%; padding-top: 5px;
    }
    .star-mestra-box button {
        background: transparent !important; border: none !important;
        color: #f1c40f !important; font-size: 1.5rem !important;
    }

    /* Tipografia do Poema */
    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.65rem; 
        line-height: 1.7; color: #1a1a1a; margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & HELP ---
@st.cache_data
def get_help_text(id_clic):
    path = f"docs/help_{id_clic}.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f: return f.read()
    return f"Manual em construção para: {id_clic}"

@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = get_acervo()

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2, 0.1, 7.9])

with c1:
    st.write("### controles")
    ic = st.columns(3)
    ic[0].button("🔈"); ic[1].button("🎨"); ic[2].button("🎬")
    st.divider()
    
    livro_sel = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"], key="sl")
    if ACERVO:
        with open(os.path.join("base", ACERVO[livro_sel]), "r", encoding="utf-8") as f:
            temas_disco = [l.strip() for l in f if l.strip()]
            if temas_disco != st.session_state.temas_atuais:
                st.session_state.temas_atuais = temas_disco
                st.session_state.idx_tema = 0
    
    st.selectbox("temas", st.session_state.temas_atuais, 
                 index=min(st.session_state.idx_tema, len(st.session_state.temas_atuais)-1),
                 key="st_combo", on_change=lambda: st.session_state.update({"idx_tema": st.session_state.temas_atuais.index(st.session_state.st_combo)}))
    st.selectbox("idioma", ["Português", "English", "Español", "Deutsch", "Français"], key="si")

with c2:
    # TOPO: Alinhamento da Star entre Eureka e Off-Mach
    cols = st.columns([1, 1, 1, 0.4, 1, 1, 1])
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    cols[0].button(pgs[0], key="b1", on_click=nav_to, args=(pgs[0],))
    cols[1].button(pgs[1], key="b2", on_click=nav_to, args=(pgs[1],))
    cols[2].button(pgs[2], key="b3", on_click=nav_to, args=(pgs[2],))
    
    with cols[3]: # A Estrela no centro exato
        st.markdown('<div class="star-mestra-box">', unsafe_allow_html=True)
        if st.button("★", key="master_star"):
            st.session_state.show_help = not st.session_state.show_help
        st.markdown('</div>', unsafe_allow_html=True)
        
    cols[4].button(pgs[3], key="b4", on_click=nav_to, args=(pgs[3],))
    cols[5].button(pgs[4], key="b5", on_click=nav_to, args=(pgs[4],))
    cols[6].button(pgs[5], key="b6", on_click=nav_to, args=(pgs[5],))

    st.divider()

    # --- 5. PALCO DE RENDERIZAÇÃO (SCROLL ISOLADO) ---
    st.markdown('<div class="palco-scroll">', unsafe_allow_html=True)
    
    if st.session_state.show_help:
        ctx = st.session_state.ID_CLIC
        st.markdown(f"### Ajuda: {ctx.upper()}")
        st.markdown(get_help_text(ctx))
        if st.button("Fechar"): 
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
                except Exception as e: st.error(f"Erro: {e}")
        else:
            st.write(f"### {p.lower()}")
            st.info(f"Ambiente ativo. O ID_CLIC registra '{p}'.")
            
    st.markdown('</div>', unsafe_allow_html=True)
