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
    def gera_poema(t, p=""): return ["Não precisar é preciso."]

# Inicialização de Estados (Correção 6 e 8: Manter navegação ativa)
for key, val in {
    'page': 'demo', 
    'show_help': False, 
    'idx_tema': 0, 
    'temas_atuais': []
}.items():
    if key not in st.session_state: st.session_state[key] = val

# --- 2. CSS: O RETORNO DA SUTILEZA (BOTÕES CIRCULARES) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}

    /* 1. TÍTULO À ESQUERDA (Ajuste 1) */
    .typo-title {
        font-family: 'Georgia', serif; font-size: 1.35rem; font-weight: bold;
        text-decoration: underline; text-align: left; margin-bottom: 18px;
        color: #333;
    }

    /* TEXTO COMPACTO */
    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.32rem; 
        line-height: 1.35; color: #1a1a1a; margin-bottom: 5px;
    }

    /* 4. BOTÕES DE PÁGINA COM LARGURA FIXA (Ajuste 4) */
    div.stButton > button {
        width: 100% !important; 
        min-width: 100px; /* Tamanho fixo para harmonia */
        height: 40px !important;
    }

    /* 3. BOTÕES CIRCULARES DE NAVEGAÇÃO (Ajuste 3) */
    .nav-container {
        display: flex; justify-content: center; align-items: center; gap: 15px;
    }
    
    /* Seletor específico para os botões redondos de navegação */
    div[data-testid="stColumn"] > div > div > div > div.stButton > button[key^="nav_"] {
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        min-width: 50px !important;
        background-color: #f8f9fa !important;
        border: 1px solid #e0e0e0 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        font-size: 1.2rem !important;
    }

    .star-icon { width: 32px; height: 32px; }
    .palco-wrapper { height: calc(100vh - 300px); overflow-y: auto; padding-right: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & FUNÇÕES (FIDELIDADE) ---
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
c1, _, c2 = st.columns([2.5, 0.4, 7.1])

with c1:
    # 2. BOTÕES DE MÍDIA "AGINDO" (Ajuste 2)
    mc1, mc2, mc3 = st.columns(3)
    if mc1.button("🔊", key="act_som"): st.toast("Som ativado")
    if mc2.button("🎨", key="act_art"): st.toast("Galeria aberta")
    if mc3.button("🎬", key="act_vid"): st.toast("Projeção iniciada")
    st.divider()
    
    livro_sel = st.selectbox("Livros", list(ACERVO.keys()) if ACERVO else ["-"])
    if ACERVO:
        with open(os.path.join("base", ACERVO[livro_sel]), "r", encoding="utf-8") as f:
            temas = [l.strip() for l in f if l.strip()]
            if temas != st.session_state.temas_atuais:
                st.session_state.temas_atuais = temas
                st.session_state.idx_tema = 0
    
    total = len(st.session_state.temas_atuais)
    idx_seg = st.session_state.idx_tema % total if total > 0 else 0
    st.selectbox("Temas", st.session_state.temas_atuais, index=idx_seg, key="st_combo")
    
    idioma_alvo = st.selectbox("Idioma", ["Português", "English", "Español", "Deutsch", "Français", "Italiano", "Latin"], key="lang_sel")

with c2:
    # 5. MENU SUPERIOR (Correção da estrela duplicada e alinhamento)
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    t_cols = st.columns([1, 1, 1, 0.6, 1, 1, 1])
    
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p, key=f"p_{p}"): st.session_state.page = p
    
    with t_cols[3]:
        # Apenas um elemento visual (Ajuste 5)
        if STAR_B64:
            st.markdown(f'<center><img src="data:image/x-icon;base64,{STAR_B64}" class="star-icon" style="margin-top:-10px"></center>', unsafe_allow_html=True)
        else:
            st.markdown('<center style="font-size:24px; margin-top:-10px">★</center>', unsafe_allow_html=True)
        if st.button("H", key="h_btn", help="Help"): st.session_state.show_help = not st.session_state.show_help

    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p, key=f"p_{p}"): st.session_state.page = p

    # 3. NAVEGAÇÃO CIRCULAR AGRUPADA (Ajuste 3 e 6)
    st.write("") 
    n_cols = st.columns([2.5, 0.8, 0.8, 0.8, 0.8, 2.5])
    if n_cols[1].button("❮", key="nav_p"): st.session_state.idx_tema -= 1
    if n_cols[2].button("✚", key="nav_a"): pass 
    if n_cols[3].button("✱", key="nav_r"): st.session_state.idx_tema = random.randint(0, total-1) if total > 0 else 0
    if n_cols[4].button("❯", key="nav_n"): st.session_state.idx_tema += 1
    st.divider()

    # PALCO DE RENDERIZAÇÃO
    palco = st.container()
    with palco:
        if st.session_state.show_help:
            st.info("Ajuda da Machina: Entre a precisão e a 'precisão', escolhemos a harmonia.")
        
        # O palco continua gerando mesmo com o help oculto (Ajuste 6)
        if st.session_state.page == "demo" and total > 0:
            tema_atual = st.session_state.temas_atuais[st.session_state.idx_tema % total]
            st.markdown(f'<div class="typo-title">{tema_atual.upper()}</div>', unsafe_allow_html=True)
            try:
                for v in gera_poema(tema_atual, ""):
                    # Tradução omitida para foco estrutural
                    st.markdown(f'<div class="typo-verse">{v}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Sutileza interrompida: {str(e)}")
        else:
            st.markdown(f"### {st.session_state.page.upper()}")
