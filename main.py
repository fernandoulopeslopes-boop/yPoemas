import streamlit as st
import os
import random
from deep_translator import GoogleTranslator

# --- 1. BOOT & ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

try: 
    from lay_2_ypo import gera_poema
except Exception as e: 
    st.error(f"Erro no Motor: {e}")
    def gera_poema(t, p=""): return ["Erro: motor inoperante."]

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

# --- 2. CSS: ATAQUE TOTAL AO ALINHAMENTO ---
st.markdown("""
<style>
    /* TRAVA DE SCROLL GLOBAL */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainViewContainer"], .main {
        overflow: hidden !important;
        height: 100vh !important;
    }
    
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}
    
    /* PALCO: FORÇAR TOPO ABSOLUTO DENTRO DA COLUNA */
    [data-testid="stVerticalBlock"] > div:has(div.palco-wrapper) {
        vertical-align: top !important;
        justify-content: flex-start !important;
    }

    .palco-wrapper {
        display: block !important;
        height: calc(100vh - 270px); 
        width: 100%;
        overflow-y: auto !important;
        position: relative !important;
        background: transparent;
    }
    
    .palco-content {
        position: absolute !important;
        top: 0 !important; /* Âncora no topo */
        left: 0 !important;
        width: 100%;
        padding-bottom: 100px;
        text-align: left;
    }

    div.stButton > button {
        width: 100% !important;
        height: 45px !important;
    }

    .star-mestra-wrapper {
        display: flex; justify-content: center; align-items: center;
    }
    .star-mestra-wrapper button {
        background: transparent !important; border: none !important;
        color: #f1c40f !important; font-size: 2.2rem !important;
        box-shadow: none !important;
    }

    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.65rem; 
        line-height: 1.7; color: #1a1a1a; margin-bottom: 8px;
    }
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
    ic = st.columns(3)
    ic[0].button("🔊", key="b_som")
    ic[1].button("🎨", key="b_arte")
    ic[2].button("📽️", key="b_vid")
    st.divider()
    
    livro_sel = st.selectbox("Livros", list(ACERVO.keys()) if ACERVO else ["-"])
    if ACERVO:
        with open(os.path.join("base", ACERVO[livro_sel]), "r", encoding="utf-8") as f:
            temas_disco = [l.strip() for l in f if l.strip()]
            if temas_disco != st.session_state.temas_atuais:
                st.session_state.temas_atuais = temas_disco
                st.session_state.idx_tema = 0
    
    st.selectbox("Temas", st.session_state.temas_atuais, 
                 index=min(st.session_state.idx_tema, len(st.session_state.temas_atuais)-1) if st.session_state.temas_atuais else 0,
                 key="st_combo", on_change=lambda: st.session_state.update({"idx_tema": st.session_state.temas_atuais.index(st.session_state.st_combo)}))
    
    idioma_alvo = st.selectbox("Idioma", ["Português", "English", "Español", "Deutsch", "Français"], key="si")

with c2:
    # Menu Superior
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    t_cols = st.columns([1, 1, 1, 0.4, 1, 1, 1])
    
    for i in range(3):
        if t_cols[i].button(pgs[i], key=f"btn_{pgs[i]}"): nav_to(pgs[i])
    with t_cols[3]:
        st.markdown('<div class="star-mestra-wrapper">', unsafe_allow_html=True)
        if st.button("★", key="m_star"): st.session_state.show_help = not st.session_state.show_help
        st.markdown('</div>', unsafe_allow_html=True)
    for i in range(3, 6):
        if t_cols[i+1].button(pgs[i], key=f"btn_{pgs[i]}"): nav_to(pgs[i])

    # Navegação [ ❮ ✚ * ❯ ]
    _, n_box, _ = st.columns([2, 6, 2])
    with n_box:
        nb = st.columns(4)
        if nb[0].button("❮", key="prev"): ante_tema()
        nb[1].button("✚", key="add")
        if nb[2].button("*", key="rand"): sorteio_tema()
        if nb[3].button("❯", key="next"): prox_tema()
    st.divider()

    # PALCO DE RENDERIZAÇÃO: Envelopamento de topo
    st.markdown('<div class="palco-wrapper"><div class="palco-content">', unsafe_allow_html=True)
    if st.session_state.show_help:
        st.markdown(f"### ⚡ AJUDA: {st.session_state.ID_CLIC.upper()}")
        st.info(get_help_text(st.session_state.ID_CLIC))
    else:
        p = st.session_state.page
        st.session_state.ID_CLIC = p
        
        if p == "demo" and st.session_state.temas_atuais:
            tema_alvo = st.session_state.temas_atuais[st.session_state.idx_tema]
            try:
                poema = gera_poema(tema_alvo, "")
                for v in poema:
                    v_trad = traduzir(v, idioma_alvo)
                    st.markdown(f'<div class="typo-verse">{v_trad}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erro no tema '{tema_alvo}': {e}")
        else:
            st.write(f"### {p.upper()}")
            st.info("A Machina aguarda o sopro poético.")
    st.markdown('</div></div>', unsafe_allow_html=True)
