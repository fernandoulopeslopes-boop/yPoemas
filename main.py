import streamlit as st
import os
import random
from deep_translator import GoogleTranslator

# --- 1. BOOT & ESTADO (PROTOCOLO PTC) ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

try: 
    from lay_2_ypo import gera_poema
except Exception: 
    def gera_poema(t, p=""): return ["Erro no motor real."]

for key, val in {
    'page': 'demo', 
    'show_help': False, 
    'ID_CLIC': 'demo', 
    'idx_tema': 0, 
    'temas_atuais': []
}.items():
    if key not in st.session_state: st.session_state[key] = val

def sorteio_tema():
    if st.session_state.temas_atuais:
        st.session_state.idx_tema = random.randint(0, len(st.session_state.temas_atuais) - 1)

# --- 2. CSS: RECUPERAÇÃO E ANCORAGEM TOPO ---
st.markdown("""
<style>
    /* Trava de Scroll Global */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainViewContainer"], .main {
        overflow: hidden !important; height: 100vh !important;
    }
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}

    /* PALCO: ANCORAGEM ABSOLUTA AO TOPO */
    .palco-wrapper {
        height: calc(100vh - 280px);
        width: 100%;
        overflow-y: auto !important;
        display: block !important; /* Sai do flexbox que centraliza */
        position: relative;
    }
    
    .palco-content {
        position: absolute;
        top: 0 !important;
        left: 0;
        width: 100%;
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.65rem; 
        line-height: 1.6; color: #1a1a1a; margin-bottom: 5px;
        text-align: left;
    }

    /* Botões e Selectbox (Garantir visibilidade) */
    div.stButton > button { width: 100% !important; height: 42px !important; }
    div[data-testid="stSelectbox"] { margin-bottom: 10px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGICA DE DADOS ---
@st.cache_data
def traduzir(texto, lang_destino):
    mapeamento = {"Português": "pt", "English": "en", "Español": "es", "Deutsch": "de", "Français": "fr"}
    if not texto.strip() or lang_destino == "Português": return texto
    try: return GoogleTranslator(source='auto', target=mapeamento[lang_destino]).translate(texto)
    except: return texto

@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = get_acervo()

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.5, 7])

with c1:
    st.columns(3)[0].button("🔊", key="vol")
    st.divider()
    
    livro_sel = st.selectbox("Livros", list(ACERVO.keys()) if ACERVO else ["-"])
    if ACERVO:
        with open(os.path.join("base", ACERVO[livro_sel]), "r", encoding="utf-8") as f:
            st.session_state.temas_atuais = [l.strip() for l in f if l.strip()]
    
    st.selectbox("Temas", st.session_state.temas_atuais, 
                 index=min(st.session_state.idx_tema, len(st.session_state.temas_atuais)-1) if st.session_state.temas_atuais else 0,
                 key="st_combo")
    
    # RECURSO RECUPERADO: Lista de Idiomas
    idioma_alvo = st.selectbox("Idioma", ["Português", "English", "Español", "Deutsch", "Français"], key="lang_sel")

with c2:
    # Menu Superior
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    t_cols = st.columns([1, 1, 1, 0.4, 1, 1, 1])
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p, key=f"t_{p}"): st.session_state.page = p
    with t_cols[3]:
        if st.button("★", key="m_star"): st.session_state.show_help = not st.session_state.show_help
    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p, key=f"t_{p}"): st.session_state.page = p

    # Navegação
    n_cols = st.columns([2, 1.5, 1.5, 1.5, 1.5, 2])
    if n_cols[1].button("❮", key="prev"): st.session_state.idx_tema -= 1
    n_cols[2].button("✚", key="add")
    if n_cols[3].button("*", key="rand"): sorteio_tema()
    if n_cols[4].button("❯", key="next"): st.session_state.idx_tema += 1
    st.divider()

    # PALCO DE RENDERIZAÇÃO
    st.markdown('<div class="palco-wrapper"><div class="palco-content">', unsafe_allow_html=True)
    if not st.session_state.show_help:
        if st.session_state.page == "demo" and st.session_state.temas_atuais:
            tema = st.session_state.temas_atuais[st.session_state.idx_tema % len(st.session_state.temas_atuais)]
            try:
                for v in gera_poema(tema, ""):
                    v_t = traduzir(v, idioma_alvo)
                    st.markdown(f'<div class="typo-verse">{v_t}</div>', unsafe_allow_html=True)
            except: st.error("Erro na geração.")
        else:
            st.markdown(f"### {st.session_state.page.upper()}")
    else:
        st.info("Modo Ajuda.")
    st.markdown('</div></div>', unsafe_allow_html=True)
