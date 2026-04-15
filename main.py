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

# --- 1. BOOT & ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

# Importação de Material Icons
st.markdown('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">', unsafe_allow_html=True)

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

# --- 2. CSS: PADRONIZAÇÃO TOTAL (WIDTH ÚNICO) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1.5rem !important;}
    
    /* Padronização de botões (Controles e Menu) */
    div.stButton > button {
        width: 100% !important;
        height: 45px !important;
        border-radius: 5px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Scroll Interno do Palco */
    .lypo-scroll-box {
        max-height: 65vh;
        overflow-y: auto !important;
        padding-right: 15px;
    }

    /* Star Mestra */
    .star-mestra-wrapper {
        display: flex; justify-content: center; align-items: center;
    }
    .star-mestra-wrapper button {
        background: transparent !important; border: none !important;
        color: #f1c40f !important; font-size: 2rem !important;
        width: auto !important;
    }

    /* Tipografia */
    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.65rem; 
        line-height: 1.7; color: #1a1a1a; 
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & TRADUÇÃO ---
@st.cache_data
def traduzir(texto, lang_destino):
    mapeamento = {"Português": "pt", "English": "en", "Español": "es", "Deutsch": "de", "Français": "fr"}
    if lang_destino == "Português": return texto
    try:
        return GoogleTranslator(source='auto', target=mapeamento[lang_destino]).translate(texto)
    except:
        return texto

@st.cache_data
def get_help_text(id_clic):
    path = f"docs/help_{id_clic}.txt"
    return open(path, "r", encoding="utf-8").read() if os.path.exists(path) else f"Help: {id_clic}"

@st.cache_data
def get_acervo():
    path = "base"
    if not os.path.exists(path): return {}
    files = sorted([f for f in os.listdir(path) if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = get_acervo()

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.5, 7])

with c1:
    st.markdown("### 🎛️ Controles")
    ic = st.columns(3)
    ic[0].button("volume_up", help="Som") # Simulando material icon via label se necessário
    ic[1].button("palette", help="Arte")
    ic[2].button("movie", help="Vídeo")
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
    # Topo Balanceado
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    t_cols = st.columns([1, 1, 1, 0.6, 1, 1, 1])
    
    if t_cols[0].button(pgs[0]): nav_to(pgs[0])
    if t_cols[1].button(pgs[1]): nav_to(pgs[1])
    if t_cols[2].button(pgs[2]): nav_to(pgs[2])
    with t_cols[3]:
        st.markdown('<div class="star-mestra-wrapper">', unsafe_allow_html=True)
        if st.button("★", key="m_star"): st.session_state.show_help = not st.session_state.show_help
        st.markdown('</div>', unsafe_allow_html=True)
    if t_cols[4].button(pgs[3]): nav_to(pgs[3])
    if t_cols[5].button(pgs[4]): nav_to(pgs[4])
    if t_cols[6].button(pgs[5]): nav_to(pgs[5])

    # Navegação [ < + * > ] (Width igual para todos)
    _, n_box, _ = st.columns([2, 5, 2])
    with n_box:
        nb = st.columns(4)
        if nb[0].button("navigate_before"): ante_tema()
        nb[1].button("add")
        if nb[2].button("casino"): sorteio_tema()
        if nb[3].button("navigate_next"): prox_tema()
    st.divider()

    # PALCO
    if st.session_state.show_help:
        st.info(get_help_text(st.session_state.ID_CLIC))
    else:
        st.markdown('<div class="lypo-scroll-box">', unsafe_allow_html=True)
        if st.session_state.page == "demo" and st.session_state.temas_atuais:
            tema_alvo = st.session_state.temas_atuais[st.session_state.idx_tema]
            poema = gera_poema(tema_alvo, "")
            for v in poema:
                v_trad = traduzir(v, idioma_alvo) if v.strip() else ""
                st.markdown(f'<div class="typo-verse">{v_trad}</div>', unsafe_allow_html=True)
        else:
            st.write(f"Ambiente: {st.session_state.page}")
        st.markdown('</div>', unsafe_allow_html=True)
