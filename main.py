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
    def gera_poema(t, p=""): return ["Erro: Engine não localizada."]

# Estados Iniciais (Regra de Fidelidade)
for key, val in {
    'page': 'demo', 'show_help': False, 'idx_tema': 0, 'temas_atuais': []
}.items():
    if key not in st.session_state: st.session_state[key] = val

# --- 2. CSS: HARMONIA & REDUÇÃO (REGRA NO_EMPTY) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}

    /* 4 e 7. REDUÇÃO DE FONTE E ESPAÇAMENTO */
    .typo-title {
        font-family: 'Georgia', serif; font-size: 1.4rem; font-weight: bold;
        text-decoration: underline; text-align: center; margin-bottom: 15px;
        color: #333;
    }
    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.32rem; /* -20% de 1.65rem */
        line-height: 1.4; /* Redução de entrelinha */
        color: #1a1a1a; margin-bottom: 6px; text-align: left;
    }

    /* 2.1 HARMONIA DOS BOTÕES */
    div.stButton > button {
        width: 100% !important; 
        min-width: 80px; 
        height: 38px !important;
        padding: 0px !important;
    }

    /* 3. NAVEGAÇÃO AGRUPADA */
    .nav-box { display: flex; justify-content: center; gap: 10px; margin-bottom: 10px; }

    .star-icon { width: 30px; height: 30px; }
    
    .palco-wrapper {
        height: calc(100vh - 320px);
        overflow-y: auto;
        padding-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS (FIDELIDADE) ---
@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

def get_base64_bin(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

ACERVO = get_acervo()
STAR_B64 = get_base64_bin("Star_yes.ico")

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.5, 7])

with c1:
    # 1. Botões Som, Arte, Vídeo (Placeholders para futura config)
    sc1, sc2, sc3 = st.columns(3)
    sc1.button("🔊", help="Som")
    sc2.button("🎨", help="Arte")
    sc3.button("🎬", help="Vídeo")
    st.divider()
    
    livro_sel = st.selectbox("Livros", list(ACERVO.keys()) if ACERVO else ["-"])
    if ACERVO:
        with open(os.path.join("base", ACERVO[livro_sel]), "r", encoding="utf-8") as f:
            temas = [l.strip() for l in f if l.strip()]
            if temas != st.session_state.temas_atuais:
                st.session_state.temas_atuais = temas
                st.session_state.idx_tema = 0
    
    total = len(st.session_state.temas_atuais)
    idx_seguro = st.session_state.idx_tema % total if total > 0 else 0
    st.selectbox("Temas", st.session_state.temas_atuais, index=idx_seguro, key="st_combo")
    
    # 5. LISTA DE IDIOMAS COMPLETA
    idiomas_fiei = ["Português", "English", "Español", "Deutsch", "Français", "Italiano", "Latin"]
    idioma_alvo = st.selectbox("Idioma", idiomas_fiei, key="lang_sel")

with c2:
    # 2. MENU SUPERIOR DESALINHADO -> HARMONIZADO
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    t_cols = st.columns([1]*3 + [0.5] + [1]*3) # 2. Proporção ajustada
    
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p): st.session_state.page = p
    
    with t_cols[3]:
        if STAR_B64:
            st.markdown(f'<center><img src="data:image/x-icon;base64,{STAR_B64}" class="star-icon"></center>', unsafe_allow_html=True)
        if st.button("★", key="m_star"): st.session_state.show_help = not st.session_state.show_help

    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p): st.session_state.page = p

    # 3. NAVEGAÇÃO CENTRADA E AGRUPADA
    st.markdown('<div class="nav-box">', unsafe_allow_html=True)
    nb1, nb2, nb3, nb4 = st.columns([1.5, 1, 1, 1.5])[1:3] # Truque de centralização por colunas
    # Aqui usamos colunas Streamlit para manter a funcionalidade do clique (8)
    n_cols = st.columns([3, 1, 1, 1, 1, 3])
    if n_cols[1].button("❮"): st.session_state.idx_tema -= 1
    n_cols[2].button("✚")
    if n_cols[3].button("*"): st.session_state.idx_tema = random.randint(0, total-1) if total > 0 else 0
    if n_cols[4].button("❯"): st.session_state.idx_tema += 1
    st.divider()

    # PALCO (no_empty)
    palco = st.container()
    with palco:
        if st.session_state.show_help:
            st.info("Ajuda da Machina: Navegação restaurada e texto otimizado.")
        elif st.session_state.page == "demo" and total > 0:
            tema_atual = st.session_state.temas_atuais[st.session_state.idx_tema % total]
            # 6. TÍTULO NO TOPO
            st.markdown(f'<div class="typo-title">{tema_atual.upper()}</div>', unsafe_allow_html=True)
            
            try:
                for v in gera_poema(tema_atual, ""):
                    # Tradução (simulação para fidelidade estrutural)
                    st.markdown(f'<div class="typo-verse">{v}</div>', unsafe_allow_html=True)
            except Exception as e:
                # 9. MENSAGEM DE ERRO DETALHADA
                st.error(f"Falha na geração poética. Tema: '{tema_atual}' | Pág: {st.session_state.page} | Erro: {str(e)}")
        else:
            st.markdown(f"### {st.session_state.page.upper()}")
