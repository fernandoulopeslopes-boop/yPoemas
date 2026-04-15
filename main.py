import streamlit as st
import os
import random
import base64
from deep_translator import GoogleTranslator

# --- 1. BOOT & ESTADO (PROTOCOLO PTC) ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

try: 
    from lay_2_ypo import gera_poema
except Exception: 
    def gera_poema(t, p=""): return ["Erro no motor: Judia dele!"]

# Inicialização de Estados
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

def get_base64_bin(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

STAR_B64 = get_base64_bin("Star_yes.ico")

# --- 2. CSS: O MARTELO NO RODAPÉ & ESTILO ---
st.markdown("""
<style>
    /* Trava de Scroll e Header */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainViewContainer"], .main {
        overflow: hidden !important; height: 100vh !important;
    }
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}

    /* FORÇAR ALINHAMENTO AO TOPO */
    [data-testid="stVerticalBlock"] {
        justify-content: flex-start !important;
    }

    /* PALCO: O ESPAÇO DA POESIA */
    .palco-wrapper {
        height: calc(100vh - 280px);
        width: 100%;
        overflow-y: auto !important;
        display: block !important;
        padding-top: 5px !important;
    }
    
    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.65rem; 
        line-height: 1.6; color: #1a1a1a; margin-bottom: 8px;
        text-align: left;
    }

    .star-icon { width: 32px; height: 32px; }

    div.stButton > button { width: 100% !important; height: 42px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & TRADUÇÃO ---
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
            temas = [l.strip() for l in f if l.strip()]
            if temas != st.session_state.temas_atuais:
                st.session_state.temas_atuais = temas
                st.session_state.idx_tema = 0
    
    # PROTEÇÃO CONTRA ÍNDICE NEGATIVO (O FIM DA JUDIARIA)
    total_temas = len(st.session_state.temas_atuais)
    safe_index = st.session_state.idx_tema % total_temas if total_temas > 0 else 0
    
    st.selectbox("Temas", st.session_state.temas_atuais, 
                 index=safe_index,
                 key="st_combo")
    
    idioma_alvo = st.selectbox("Idioma", ["Português", "English", "Español", "Deutsch", "Français"], key="lang_sel")

with c2:
    # Menu Superior
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    t_cols = st.columns([1, 1, 1, 0.4, 1, 1, 1])
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p, key=f"t_{p}"): st.session_state.page = p
    
    with t_cols[3]:
        if STAR_B64:
            st.markdown(f'<center><img src="data:image/x-icon;base64,{STAR_B64}" class="star-icon"></center>', unsafe_allow_html=True)
        if st.button("★", key="m_star"): st.session_state.show_help = not st.session_state.show_help

    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p, key=f"t_{p}"): st.session_state.page = p

    # Navegação [ ❮ ✚ * ❯ ]
    n_cols = st.columns([2, 1.5, 1.5, 1.5, 1.5, 2])
    if n_cols[1].button("❮", key="prev"): st.session_state.idx_tema -= 1
    n_cols[2].button("✚", key="add")
    if n_cols[3].button("*", key="rand"): sorteio_tema()
    if n_cols[4].button("❯", key="next"): st.session_state.idx_tema += 1
    st.divider()

    # PALCO DE RENDERIZAÇÃO
    st.markdown('<div class="palco-wrapper">', unsafe_allow_html=True)
    if not st.session_state.show_help:
        if st.session_state.page == "demo" and st.session_state.temas_atuais:
            tema_atual = st.session_state.temas_atuais[st.session_state.idx_tema % total_temas]
            try:
                for v in gera_poema(tema_atual, ""):
                    v_t = traduzir(v, idioma_alvo)
                    st.markdown(f'<div class="typo-verse">{v_t}</div>', unsafe_allow_html=True)
            except: st.error("Erro na geração poética.")
        else:
            st.markdown(f"### {st.session_state.page.upper()}")
    else:
        st.info("Ajuda da Machina: Aqui Agora Absoluta.")
    st.markdown('</div>', unsafe_allow_html=True)
