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

def sorteio_tema():
    if st.session_state.temas_atuais:
        st.session_state.idx_tema = random.randint(0, len(st.session_state.temas_atuais) - 1)

# --- 2. CSS: ESTABILIDADE E SCROLL NO PALCO ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1.5rem !important;}
    
    /* Scroll apenas no conteúdo do poema */
    .lypo-scroll-box {
        max-height: 70vh;
        overflow-y: auto !important;
        padding-right: 15px;
        margin-top: 10px;
    }

    /* Star Mestra */
    .star-mestra-wrapper {
        display: flex; justify-content: center; align-items: center;
    }
    .star-mestra-wrapper button {
        background: transparent !important; border: none !important;
        color: #f1c40f !important; font-size: 1.5rem !important;
        margin-top: 5px !important;
    }

    /* Régua de Navegação [ + < * > ] */
    .nav-rim-box button { 
        background: transparent !important; border: none !important; 
        font-size: 1.4rem !important; color: #777 !important; 
    }

    /* Tipografia */
    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.65rem; 
        line-height: 1.7; color: #1a1a1a; 
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & HELP ---
@st.cache_data
def get_help_text(id_clic):
    path = f"docs/help_{id_clic}.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f: return f.read()
    return f"Manual aguardando redação: help_{id_clic}.txt"

@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = get_acervo()

# --- 4. INTERFACE: COLUNAS NATIVAS (ESTÁVEIS) ---
c1, _, c2 = st.columns([2, 0.2, 7.8])

with c1:
    st.write("### CONTROLES")
    ic = st.columns(3)
    if ic[0].button("🔈 Som"): pass
    if ic[1].button("🎨 Arte"): pass
    if ic[2].button("🎬 Vídeo"): pass
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

with c2:
    # TOPO: Navegação balanceada com Star Mestra
    cols = st.columns([1, 1, 1, 0.4, 1, 1, 1])
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    cols[0].button(pgs[0], on_click=nav_to, args=(pgs[0],))
    cols[1].button(pgs[1], on_click=nav_to, args=(pgs[1],))
    cols[2].button(pgs[2], on_click=nav_to, args=(pgs[2],))
    
    with cols[3]:
        st.markdown('<div class="star-mestra-wrapper">', unsafe_allow_html=True)
        if st.button("★", key="master_star"):
            st.session_state.show_help = not st.session_state.show_help
        st.markdown('</div>', unsafe_allow_html=True)
        
    cols[4].button(pgs[3], on_click=nav_to, args=(pgs[3],))
    cols[5].button(pgs[4], on_click=nav_to, args=(pgs[4],))
    cols[6].button(pgs[5], on_click=nav_to, args=(pgs[5],))

    # Régua Centralizada [ + < * > ]
    st.markdown('<div class="nav-rim-box">', unsafe_allow_html=True)
    _, col_cent, _ = st.columns([3, 4, 3])
    with col_cent:
        bn = st.columns(4)
        bn[0].button("➕")
        bn[1].button("◀", on_click=ante_tema)
        bn[2].button("🎲", on_click=sorteio_tema)
        bn[3].button("▶", on_click=prox_tema)
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

    # PALCO DE CONTEÚDO
    if st.session_state.show_help:
        ctx = st.session_state.ID_CLIC
        st.markdown(f"### AJUDA: {ctx.upper()}")
        st.markdown(get_help_text(ctx))
        if st.button("Fechar Ajuda"):
            st.session_state.show_help = False
            st.rerun()
    else:
        p = st.session_state.page
        st.session_state.ID_CLIC = p
        
        st.markdown('<div class="lypo-scroll-box">', unsafe_allow_html=True)
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
            st.write(f"### Ambiente {p.upper()}")
            st.info(f"O ID_CLIC está mapeado para '{p}'.")
        st.markdown('</div>', unsafe_allow_html=True)
