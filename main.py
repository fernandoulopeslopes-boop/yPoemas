import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os

# --- MOTOR DE TRADUÇÃO ---
@st.cache_data
def traduzir_texto(texto, destino_nome):
    if not texto or "Português" in destino_nome: 
        return texto
    try:
        codigos = {
            "PT - Português": "pt", "ES - Español": "es", "IT - Italiano": "it",
            "FR - Français": "fr", "DE - Deutsch": "de", "EN - English": "en",
            "CA - Català": "ca", "GL - Galego": "gl", "RO - Română": "ro"
        }
        target = codigos.get(destino_nome, 'en')
        return GoogleTranslator(source='auto', target=target).translate(texto)
    except:
        return texto

# --- CONFIGURAÇÕES DE AMBIENTE ---
PATH_MD = "md_files"
ICON_YPO = "icon_ypo.ico"
IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    st.set_page_config(
        layout="wide", 
        page_title="yPoemas", 
        page_icon=ICON_YPO if os.path.exists(ICON_YPO) else "🎭"
    )

    # --- CSS DE PRECISÃO: LARGURA 300PX E DESIGN DOS BOTÕES ---
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            .block-container { padding-top: 1rem !important; }

            /* Sidebar: LARGURA RIGOROSA 300PX */
            section[data-testid="stSidebar"] {
                width: 300px !important;
                min-width: 300px !important;
                max-width: 300px !important;
            }
            
            /* Topo Absoluto na Sidebar (Zerar padding) */
            [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
                padding-top: 0rem !important;
            }

            /* Botões de Navegação: Padrão Glifos Pesados */
            div.stButton > button {
                border-radius: 50% !important;
                width: 52px !important;
                height: 52px !important;
                border: 1px solid #333 !important;
                background-color: #ffffff !important;
                color: #111 !important;
                font-size: 26px !important;
                font-weight: bold !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                transition: all 0.2s ease-in-out;
                box-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                margin: 0 auto !important;
            }
            div.stButton > button:hover {
                border-color: #ff4b4b !important;
                color: #ff4b4b !important;
                transform: translateY(-1px);
                box-shadow: 2px 4px 8px rgba(0,0,0,0.15);
            }
        </style>
    """, unsafe_allow_html=True)

    # ESTADO E ATIVOS
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    if 'current_tab_idx' not in st.session_state:
        st.session_state.current_tab_idx = 1
    
    active_tab = tabs_list[st.session_state.current_tab_idx]

    map_assets = {
        "mini": {"img": "img_mini.jpg", "md": "INFO_MINI.md"},
        "ypoemas": {"img": "img_ypoemas.jpg", "md": "INFO_YPOEMAS.md"},
        "eureka": {"img": "img_eureka.jpg", "md": "INFO_EUREKA.md"},
        "off-máquina": {"img": "img_off-machina.jpg", "md": "ABOUT_OFF-MACHINA.md"},
        "books": {"img": "img_books.jpg", "md": "INFO_BOOKS.md"},
        "comments": {"img": "img_poly.jpg", "md": "ABOUT_COMMENTS.md"},
        "about": {"img": "img_about.jpg", "md": "INFO_ABOUT.md"}
    }
    asset = map_assets.get(active_tab)

    # --- 1. SIDEBAR (CONTROLE, INFORMAÇÃO E IDENTIDADE) ---
    with st.sidebar:
        st.markdown("### 🌐 Idioma")
        sel_idioma = st.selectbox("Seletor", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")
        st.markdown("---")

        # Texto Informativo (Parte Central)
        info_path = os.path.join(PATH_MD, asset["md"])
        if os.
