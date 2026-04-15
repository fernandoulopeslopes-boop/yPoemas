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
    def gera_poema(t, p=""): return ["Não há fuga do labirinto.", "O motor aguarda."]

# Inicialização de Estados
for key, val in {
    'page': 'demo', 'show_help': False, 'idx_tema': 0, 'temas_atuais': []
}.items():
    if key not in st.session_state: st.session_state[key] = val

# --- 2. CSS: HARMONIA INTEGRAL (CC: NO_EMPTY) ---
st.markdown("""
<style>
    /* 1. SCROLL DE TELA INTEIRA */
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .main { overflow: auto !important; }
    .block-container { padding: 1.5rem !important; max-width: 95%; }

    /* ESTÉTICA DO TEXTO */
    .typo-title {
        font-family: 'Georgia', serif; font-size: 1.3rem; font-weight: bold;
        text-decoration: underline; text-align: left; margin-bottom: 15px; color: #333;
    }
    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.32rem; 
        line-height: 1.35; color: #1a1a1a; margin-bottom: 5px;
    }

    /* 3. BOTÕES DE MÍDIA E 5. ALINHAMENTO DE FIOS */
    .media-box div[data-testid="stColumn"] button {
        width: 42px !important; height: 42px !important;
        min-width: 42px !important; padding: 0px !important;
        margin: 0 auto !important; display: block;
    }
    hr { margin: 1rem 0 !important; border: 0; border-top: 1px solid #ddd !important; }

    /* 4. BOTÕES DE PÁGINA */
    div.stButton > button { width: 100% !important; min-width: 95px; height: 40px !important; }

    /* 2. ARREDONDAR NAVEGAÇÃO (ROUND BUTTONS) */
    .st-key-nav_p button, .st-key-nav_a button, .st-key-nav_r button, .st-key-nav_n button {
        border-radius: 50% !important;
        width: 50px !important; height: 50px !important;
        min-width: 50px !important;
        background-color: #f8f9fa !important;
        border: 1px solid #e0e0e0 !important;
        font-size: 1.2rem !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }

    /* HELP QUADRADO */
    .st-key-h_btn button { width: 40px !important; min-width: 40px !important; border-radius: 4px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & AJUDA (Ajuste 3) ---
def exibe_ajuda():
    st.markdown("""
    ### Ajuda da Machina
    * **Navegação:** Use os botões redondos para perambular pelos temas.
    * **Acervo:** O 'Livro Vivo' é o seu ponto de partida onírico.
    * **Mídia:** Habilite Som, Arte ou Vídeo para interferir na identidade da obra.
    * **Fuga:** Não há. Aproveite a estadia.
    """)

@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    acervo = {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}
    if "Haykay" in str(acervo): acervo = {k.replace("Haykay", "HaiCai"): v for k,v in acervo.items()}
    return acervo

ACERVO = get_acervo()

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.4, 7.1])

with c1:
    # 6. BLOCO SOM/ARTE/VÍDEO (FUNCIONAL)
    st.markdown('<div class="media-box">', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    if m1.button("🔊", key="m_s"): st.session_state.som = not st.session_state.get('som', False)
    if m2.button("🎨", key="m_a"): st.session_state.arte = not st.session_state.get('arte', False)
    if m3.button("🎬", key="m_v"): st.session_state.video = not st.session_state.get('video', False)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider() # Fio alinhado (5)
    
    # LIVRO INICIAL
    lista_l = list(ACERVO.keys())
    ini_l = "Livro Vivo" if "Livro Vivo" in lista_l else (lista_l[0] if lista_l else "-")
    sel_l = st.selectbox("Livros", lista_l, index=lista_l.index(ini_l) if ini_l in lista_l else 0)
    
    if ACERVO:
        with open(os.path.join("base", ACERVO[sel_l]), "r", encoding="utf-8") as f:
            st.session_state.temas_atuais = [l.strip() for l in f if l.strip()]
    
    tot = len(st.session_state.temas_atuais)
    idx = st.session_state.idx_tema % tot if tot > 0 else 0
    st.selectbox("Temas", st.session_state.temas_atuais, index=idx, key="st_combo")
    st.selectbox("Idioma", ["Português", "English", "Español", "Deutsch", "Français", "Italiano", "Latin"], key="l_sel")

with c2:
    # MENU SUPERIOR (4. Habilitando Opinião/Sobre)
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    t_cols = st.columns([1, 1, 1, 0.5, 1, 1, 1])
    
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p, key=f"btn_{p}"): st.session_state.page = p
    
    with t_cols[3]:
        if st.button("?", key="h_btn"): st.session_state.show_help = not st.session_state.show_help

    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p, key=f"btn_{p}"): st.session_state.page = p

    # 2. NAVEGAÇÃO ARREDONDADA (ROUND)
    st.write("") 
    n_cols = st.columns([2.5, 0.7, 0.7, 0.7, 0.7, 2.5])
    if n_cols[1].button("❮", key="nav_p"): st.session_state.idx_tema -= 1
    if n_cols[2].button("✚", key="nav_a"): st.toast("Elemento capturado")
    if n_cols[3].button("✱", key="nav_r"): st.session_state.idx_tema = random.randint(0, tot-1) if tot > 0 else 0
    if n_cols[4].button("❯", key="nav_n"): st.session_state.idx_tema += 1
    
    st.divider() # Fio alinhado (5)

    # PALCO INTEGRAL (1. Scroll de tela inteira)
    if st.session_state.show_help:
        exibe_ajuda()
    elif st.session_state.page == "demo" and tot > 0:
        tema = st.session_state.temas_atuais[st.session_state.idx_tema % tot]
        st.markdown(f'<div class="typo-title">{tema.upper()}</div>', unsafe_allow_html=True)
        try:
            for v in gera_poema(tema, ""):
                st.markdown(f'<div class="typo-verse">{v}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erro no instinto: {str(e)}")
    elif st.session_state.page == "opinião":
        st.markdown("### OPINIÃO\n*Espaço reservado para o eco do incauto.*")
    elif st.session_state.page == "sobre":
        st.markdown("### SOBRE\n*A Machina é um labirinto de sentenças e liberdade.*")
    else:
        st.markdown(f"### {st.session_state.page.upper()}")
