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
    def gera_poema(t, p=""): return ["Erro: Engine Machina não encontrada."]

# Inicialização de Estados
if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'show_help' not in st.session_state: st.session_state.show_help = False
if 'idx_tema' not in st.session_state: st.session_state.idx_tema = 0
if 'temas_atuais' not in st.session_state: st.session_state.temas_atuais = []

# --- 2. CSS: HARMONIA E REDUÇÃO VISUAL ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}

    /* TÍTULO DO POEMA (Ajuste 6) */
    .typo-title {
        font-family: 'Georgia', serif; font-size: 1.3rem; font-weight: bold;
        text-decoration: underline; text-align: center; margin-bottom: 20px;
        color: #444; letter-spacing: 1px;
    }

    /* TEXTO GERADO (Ajustes 4 e 7) */
    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.35rem; 
        line-height: 1.35; color: #1a1a1a; margin-bottom: 5px; text-align: left;
    }

    /* HARMONIA DOS BOTÕES (Ajuste 2.1) */
    div.stButton > button {
        width: 100% !important; height: 38px !important;
        padding: 0px !important; font-size: 0.9rem !important;
    }

    .star-icon { width: 30px; height: 30px; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & TRADUÇÃO (FIDELIDADE) ---
@st.cache_data
def traduzir(texto, lang_destino):
    mapeamento = {
        "Português": "pt", "English": "en", "Español": "es", 
        "Deutsch": "de", "Français": "fr", "Italiano": "it", "Latin": "la"
    }
    if not texto or lang_destino == "Português": return texto
    try: 
        return GoogleTranslator(source='auto', target=mapeamento.get(lang_destino, 'en')).translate(texto)
    except: 
        return texto

@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = get_acervo()

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.4, 7.1])

with c1:
    # 1. BOTÕES DE MÍDIA (CONFIGURAÇÃO INICIAL)
    m_cols = st.columns(3)
    m_cols[0].button("🔊", key="b_som")
    m_cols[1].button("🎨", key="b_arte")
    m_cols[2].button("🎬", key="b_video")
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
    
    # 5. LISTA DE IDIOMAS (FIDELIDADE)
    idiomas = ["Português", "English", "Español", "Deutsch", "Français", "Italiano", "Latin"]
    idioma_alvo = st.selectbox("Idioma", idiomas, key="lang_sel")

with c2:
    # 2. MENU SUPERIOR HARMONIZADO
    t_cols = st.columns([1, 1, 1, 0.5, 1, 1, 1])
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p, key=f"btn_{p}"): st.session_state.page = p
    
    with t_cols[3]:
        # Estrela Mestra centralizada
        st.markdown('<div style="text-align:center; margin-top:-5px;">★</div>', unsafe_allow_html=True)
        if st.button("?", key="m_star"): st.session_state.show_help = not st.session_state.show_help

    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p, key=f"btn_{p}"): st.session_state.page = p

    # 3. NAVEGAÇÃO AGRUPADA E CENTRADA (Ajuste Corrigido)
    st.write("") # Espaçador funcional
    n_cols = st.columns([2.5, 1, 1, 1, 1, 2.5])
    if n_cols[1].button("❮", key="nav_prev"): st.session_state.idx_tema -= 1
    n_cols[2].button("✚", key="nav_add")
    if n_cols[3].button("*", key="nav_rand"): 
        st.session_state.idx_tema = random.randint(0, total-1) if total > 0 else 0
    if n_cols[4].button("❯", key="nav_next"): st.session_state.idx_tema += 1
    st.divider()

    # 4, 6, 7 e 9. PALCO DE RENDERIZAÇÃO
    palco = st.container()
    with palco:
        if st.session_state.show_help:
            st.info("Ajuda da Machina: Navegação restaurada. O texto agora é mais denso e o título é obrigatório.")
        elif st.session_state.page == "demo" and total > 0:
            tema_atual = st.session_state.temas_atuais[st.session_state.idx_tema % total]
            
            # Título Centrado e Underlined (6)
            st.markdown(f'<div class="typo-title">{tema_atual.upper()}</div>', unsafe_allow_html=True)
            
            try:
                for v in gera_poema(tema_atual, ""):
                    v_t = traduzir(v, idioma_alvo)
                    st.markdown(f'<div class="typo-verse">{v_t}</div>', unsafe_allow_html=True)
            except Exception as e:
                # Mensagem detalhada de falha (9)
                st.error(f"Falha na geração poética. | Tema: {tema_atual} | Erro: {str(e)}")
        else:
            st.markdown(f"### {st.session_state.page.upper()}")
