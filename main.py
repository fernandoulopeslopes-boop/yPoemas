import streamlit as st
import os
import random
from deep_translator import GoogleTranslator

# MOTOR REAL
try: 
    from lay_2_ypo import gera_poema
except Exception: 
    def gera_poema(t, p=""): 
        return ["Erro: motor não encontrado."]

# --- 1. BOOT & ESTADO (LIMPEZA TOTAL) ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

for key, val in {
    'page': 'demo', 
    'show_help': False, 
    'ID_CLIC': 'demo', 
    'idx_tema': 0, 
    'temas_atuais': []
}.items():
    if key not in st.session_state: st.session_state[key] = val

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

# --- 2. CSS: ESTÉTICA E SCROLL ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1.5rem !important;}
    
    /* Scroll Interno do Palco */
    .lypo-scroll-box {
        max-height: 60vh;
        overflow-y: auto !important;
        padding-right: 20px;
    }

    /* Star Mestra centralizada e sem bordas */
    .star-mestra-wrapper {
        display: flex; justify-content: center; align-items: center; height: 100%;
    }
    .star-mestra-wrapper button {
        background: transparent !important; border: none !important;
        color: #f1c40f !important; font-size: 2rem !important;
        padding: 0 !important;
    }

    /* Versos */
    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.65rem; 
        line-height: 1.7; color: #1a1a1a; margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & TRADUÇÃO ---
@st.cache_data
def traduzir(texto, lang_destino):
    mapeamento = {"Português": "pt", "English": "en", "Español": "es", "Deutsch": "de", "Français": "fr"}
    if not texto.strip() or lang_destino == "Português": return texto
    try:
        return GoogleTranslator(source='auto', target=mapeamento[lang_destino]).translate(texto)
    except:
        return texto

@st.cache_data
def get_help_text(id_clic):
    path = f"docs/help_{id_clic}.txt"
    return open(path, "r", encoding="utf-8").read() if os.path.exists(path) else f"Contexto: {id_clic}"

@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = get_acervo()

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.5, 7])

with c1:
    st.write("### 🎛️ CONTROLES")
    ic = st.columns(3)
    ic[0].button("🔊", help="Som", use_container_width=True)
    ic[1].button("🎨", help="Arte", use_container_width=True)
    ic[2].button("🎬", help="Vídeo", use_container_width=True)
    st.divider()
    
    livro_sel = st.selectbox("Livros", list(ACERVO.keys()) if ACERVO else ["-"])
    if ACERVO:
        with open(os.path.join("base", ACERVO[livro_sel]), "r", encoding="utf-8") as f:
            temas_disco = [l.strip() for l in f if l.strip()]
            if temas_disco != st.session_state.temas_atuais:
                st.session_state.temas_atuais = temas_disco
                st.session_state.idx_tema = 0
    
    st.selectbox("Temas", st.session_state.temas_atuais, 
                 index=min(st.session_state.idx_tema, len(st.session_state.temas_atuais)-1),
                 key="st_combo", on_change=lambda: st.session_state.update({"idx_tema": st.session_state.temas_atuais.index(st.session_state.st_combo)}))
    
    idioma_alvo = st.selectbox("Tradução", ["Português", "English", "Español", "Deutsch", "Français"], key="si")

with c2:
    # TOPO BALANCEADO (3 + Star + 3)
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    t_cols = st.columns([1, 1, 1, 0.5, 1, 1, 1])
    
    if t_cols[0].button(pgs[0], use_container_width=True): nav_to(pgs[0])
    if t_cols[1].button(pgs[1], use_container_width=True): nav_to(pgs[1])
    if t_cols[2].button(pgs[2], use_container_width=True): nav_to(pgs[2])
    
    with t_cols[3]:
        st.markdown('<div class="star-mestra-wrapper">', unsafe_allow_html=True)
        if st.button("★", key="m_star"): st.session_state.show_help = not st.session_state.show_help
        st.markdown('</div>', unsafe_allow_html=True)
        
    if t_cols[4].button(pgs[3], use_container_width=True): nav_to(pgs[3])
    if t_cols[5].button(pgs[4], use_container_width=True): nav_to(pgs[4])
    if t_cols[6].button(pgs[5], use_container_width=True): nav_to(pgs[5])

    # NAVEGAÇÃO [ < + * > ]
    _, n_box, _ = st.columns([2.5, 5, 2.5])
    with n_box:
        nb = st.columns(4)
        if nb[0].button("◀", help="Anterior", use_container_width=True): ante_tema()
        if nb[1].button("➕", help="Mais", use_container_width=True): pass
        if nb[2].button("🎲", help="Sorteio", use_container_width=True): sorteio_tema()
        if nb[3].button("▶", help="Próximo", use_container_width=True): prox_tema()
    st.divider()

    # PALCO DE RENDERIZAÇÃO
    if st.session_state.show_help:
        st.markdown(f"### ℹ️ AJUDA: {st.session_state.ID_CLIC.upper()}")
        st.info(get_help_text(st.session_state.ID_CLIC))
        if st.button("Fechar"): 
            st.session_state.show_help = False
            st.rerun()
    else:
        st.markdown('<div class="lypo-scroll-box">', unsafe_allow_html=True)
        if st.session_state.page == "demo" and st.session_state.temas_atuais:
            try:
                tema_alvo = st.session_state.temas_atuais[st.session_state.idx_tema]
                poema = gera_poema(tema_alvo, "")
                for v in poema:
                    v_trad = traduzir(v, idioma_alvo)
                    st.markdown(f'<div class="typo-verse">{v_trad}</div>', unsafe_allow_html=True)
            except Exception as e: st.error(f"Erro no Motor: {e}")
        else:
            st.write(f"### AMBIENTE: {st.session_state.page.upper()}")
            st.info(f"O ID_CLIC está capturando o contexto '{st.session_state.page}'. Clique na Estrela para detalhes.")
        st.markdown('</div>', unsafe_allow_html=True)
