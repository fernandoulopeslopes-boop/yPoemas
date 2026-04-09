import streamlit as st
import streamlit.components.v1 as components
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=54 (RESTAURAÇÃO DO PALCO + TEXTO FIEL + ESTÉTICA CIRÚRGICA)
# REGRA_ZERO: Foco na hospitalidade do texto e na eliminação da "tripa" visual.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

DICI_LANG = {
    'Português': 'pt', 'Español': 'es', 'Italiano': 'it', 
    'Français': 'fr', 'English': 'en', 'Català': 'ca',
    'Deutsch': 'de', 'Galego': 'gl', 'Română': 'ro'
}

def aplicar_estetica_v54():
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            
            /* EXTIRPAÇÃO DO BLOCO SUPERIOR */
            .main .block-container {
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
                margin-top: -125px !important; 
            }
            
            [data-testid="stVerticalBlock"] > div { gap: 0rem !important; }

            /* COCKPIT FIXO */
            .fixed-top {
                position: fixed; top: 0; left: 0; width: 100%;
                background-color: white; z-index: 999;
                border-bottom: 1px solid #f2f2f2;
                display: flex; flex-direction: column; align-items: center;
                padding-bottom: 15px;
            }
            
            /* BOTÕES CIRCULARES */
            .stButton > button { 
                border-radius: 50% !important; width: 38px !important; height: 38px !important; 
                background: white !important; border: 1px solid #eee !important;
            }
            
            /* VISOR DE TEMAS (SELECTBOX CUSTOM) */
            div[data-testid="stSelectbox"] {
                margin-top: 10px !important;
                width: 500px !important; 
            }
            div[data-testid="stSelectbox"] label { display: none !important; }
            
            /* Limpeza estética do Selectbox nativo */
            div[data-testid="stSelectbox"] > div[data-baseweb="select"] > div {
                border: none !important;
                background-color: transparent !important;
                box-shadow: none !important;
                font-size: 18px !important;
                color: #555 !important;
                text-align: center !important;
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética")
    aplicar_estetica_v54()

    # --- 1. ESTADOS ---
    if 'seed' not in st.session_state: st.session_state.seed = random.randint(1, 9999)
    if 'current_tab' not in st.session_state: st.session_state.current_tab = "demo"
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = "todos os temas"
    if 'memoria_temas' not in st.session_state: 
        st.session_state.memoria_temas = {"todos os temas": random.randint(0, 10)}
    if 'lang' not in st.session_state: st.session_state.lang = 'Português'
    if 'show_config' not in st.session_state: st.session_state.show_config = False

    # --- 2. CARREGAMENTO ---
    arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_") and f.endswith(".txt")]) if os.path.exists(BASE_PATH) else []
    LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
    book_foco = "todos os temas" if st.session_state.current_tab == "demo" else st.session_state.book_em_foco
    caminho_livro = os.path.join(BASE_PATH, LIVROS.get(book_foco, "rol_todos os temas.txt"))
    
    try:
        with open(caminho_livro, "r", encoding="utf-8") as f:
            lista_temas = [l.strip() for l in f if l.strip() and not l.startswith("[")]
    except:
        lista_temas = ["Rol Indisponível"]

    # --- 3. COCKPIT ---
    st.markdown('<div class="fixed-top">', unsafe_allow_html=True)
    
    _, col_nav, _ = st.columns([1, 2, 1])
    with col_nav:
        b_cols = st.columns(6)
        if b_cols[0].button("✚", key="x54_plus"): 
            st.session_state.seed += 1
            st.rerun()
        if b_cols[1].button("❰", key="x54_prev"): 
            st.session_state.memoria_temas[book_foco] -= 1
            st.rerun()
        if b_cols[2].button("✱", key="x54_rnd"): 
            st.session_state.seed = random.randint(1, 9999)
            st.session_state.memoria_temas[book_foco] = random.randint(0, len(lista_temas)-1)
            st.rerun()
        if b_cols[3].button("❱", key="x54_next"): 
            st.session_state.memoria_temas[book_foco] += 1
            st.rerun()
        b_cols[4].button("?", key="x54_help")
        if b_cols[5].button("@", key="x54_cfg"):
            st.session_state.show_config = not st.session_state.show_config
            st.rerun()

    idx_tema = st.session_state.memoria_temas.get(book_foco, 0) % len(lista_temas)
    st.selectbox("Visor", lista_temas, index=idx_tema, key=f"v54_sel", 
                 on_change=lambda: st.session_state.memoria_temas.update({book_foco: lista_temas.index(st.session_state["v54_sel"])}),
                 label_visibility="collapsed")

    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=st.session_state.current_tab)
    if aba_sel and aba_sel != st.session_state.current_tab:
        st.session_state.current_tab = aba_sel
        st.rerun()

    if st.session_state.show_config:
        st.session_state.lang = st.selectbox("Idioma", list(DICI_LANG.keys()), index=list(DICI_LANG.keys()).index(st.session_state.lang))
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 4. PALCO (RESTORED PRINT) ---
    st.markdown('<div style="margin-top: 170px;"></div>', unsafe_allow_html=True)
    
    if st.session_state.current
