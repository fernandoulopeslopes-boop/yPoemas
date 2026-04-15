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
    def gera_poema(t, p=""): return ["A noite vasta canta em segredo."]

# Inicialização de Estados (Regra de Fidelidade)
if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'show_help' not in st.session_state: st.session_state.show_help = False
if 'idx_tema' not in st.session_state: st.session_state.idx_tema = 0
if 'temas_atuais' not in st.session_state: st.session_state.temas_atuais = []

# --- 2. CSS: REFINAMENTO E BOTÕES REDONDOS (CC: NO_EMPTY) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}

    /* 1. TÍTULO À ESQUERDA */
    .typo-title {
        font-family: 'Georgia', serif; font-size: 1.3rem; font-weight: bold;
        text-decoration: underline; text-align: left; margin-bottom: 15px; color: #333;
    }

    /* TEXTO COMPACTO */
    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.32rem; 
        line-height: 1.35; color: #1a1a1a; margin-bottom: 5px;
    }

    /* 3. REDUÇÃO DE 50% NOS BOTÕES DE MÍDIA */
    .media-btn-container div[data-testid="stColumn"] button {
        width: 50% !important; min-width: 40px !important; margin: 0 auto !important; display: block;
    }

    /* 4. BOTÕES DE PÁGINA (WIDTH FIXO) */
    div.stButton > button { width: 100% !important; min-width: 90px; height: 38px !important; }

    /* 5. BOTÕES REDONDOS DE NAVEGAÇÃO (RESTAURADOS) */
    .st-key-nav_p button, .st-key-nav_a button, .st-key-nav_r button, .st-key-nav_n button {
        border-radius: 50% !important;
        width: 45px !important; height: 45px !important;
        min-width: 45px !important;
        background-color: #f0f2f6 !important;
        border: 1px solid #d1d5db !important;
        color: #374151 !important;
        font-weight: bold !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & CORREÇÃO DE ARQUIVOS (REGRA DE FIDELIDADE) ---
@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    # Correção 6: Garantir que HaiCai seja lido corretamente
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    acervo_dict = {}
    for f in files:
        nome_limpo = f.replace("rol_", "").replace(".txt", "").replace("_", " ").title()
        # Forçar correção de nomes errôneos na origem da lista
        if "Haykay" in nome_limpo: nome_limpo = "HaiCai"
        acervo_dict[nome_limpo] = f
    return acervo_dict

ACERVO = get_acervo()

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.4, 7.1])

with c1:
    # 2 e 3. BOTÕES DE MÍDIA REDUZIDOS E ATIVOS
    st.markdown('<div class="media-btn-container">', unsafe_allow_html=True)
    mc1, mc2, mc3 = st.columns(3)
    if mc1.button("🔊", key="act_som"): st.toast("Som: On")
    if mc2.button("🎨", key="act_art"): st.toast("Arte: On")
    if mc3.button("🎬", key="act_vid"): st.toast("Vídeo: On")
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()
    
    # 1. LIVRO INICIAL: LIVRO VIVO
    livros_disponiveis = list(ACERVO.keys())
    default_livro = "Livro Vivo" if "Livro Vivo" in livros_disponiveis else (livros_disponiveis[0] if livros_disponiveis else "-")
    
    livro_sel = st.selectbox("Livros", livros_disponiveis, index=livros_disponiveis.index(default_livro) if default_livro in livros_disponiveis else 0)
    
    if ACERVO:
        with open(os.path.join("base", ACERVO[livro_sel]), "r", encoding="utf-8") as f:
            st.session_state.temas_atuais = [l.strip() for l in f if l.strip()]
    
    total = len(st.session_state.temas_atuais)
    idx_seg = st.session_state.idx_tema % total if total > 0 else 0
    st.selectbox("Temas", st.session_state.temas_atuais, index=idx_seg, key="st_combo")
    st.selectbox("Idioma", ["Português", "English", "Español", "Deutsch", "Français", "Italiano", "Latin"], key="lang_sel")

with c2:
    # 4. MENU SUPERIOR (ELIMINAÇÃO DA STAR / ÍCONE ?)
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    t_cols = st.columns([1, 1, 1, 0.6, 1, 1, 1])
    
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p, key=f"p_{p}"): st.session_state.page = p
    
    with t_cols[3]:
        # Ícone padrão ? no lugar da star (Ajuste 4)
        if st.button("?", key="help_btn"): st.session_state.show_help = not st.session_state.show_help

    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p, key=f"p_{p}"): st.session_state.page = p

    # 5. NAVEGAÇÃO REDONDA (RESTAURADA)
    st.write("") 
    n_cols = st.columns([2.5, 0.7, 0.7, 0.7, 0.7, 2.5])
    if n_cols[1].button("❮", key="nav_p"): st.session_state.idx_tema -= 1
    if n_cols[2].button("✚", key="nav_a"): st.toast("Adicionado")
    if n_cols[3].button("✱", key="nav_r"): st.session_state.idx_tema = random.randint(0, total-1) if total > 0 else 0
    if n_cols[4].button("❯", key="nav_n"): st.session_state.idx_tema += 1
    st.divider()

    # PALCO
    palco = st.container()
    with palco:
        if st.session_state.show_help:
            st.info("Ajuda da Machina: A liberdade natural requer ordem estrutural.")
        
        if st.session_state.page == "demo" and total > 0:
            tema_atual = st.session_state.temas_atuais[st.session_state.idx_tema % total]
            st.markdown(f'<div class="typo-title">{tema_atual.upper()}</div>', unsafe_allow_html=True)
            try:
                # 6. RESILIENTE A ERROS DE ARQUIVO
                versos = gera_poema(tema_atual, "")
                for v in versos:
                    st.markdown(f'<div class="typo-verse">{v}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Sutileza interrompida em {tema_atual}: {str(e)}")
        else:
            st.markdown(f"### {st.session_state.page.upper()}")
