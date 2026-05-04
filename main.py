import os
import re
import time
import random
import base64
import socket
import streamlit as st

from extra_streamlit_components import TabBar as stx
from datetime import datetime
from lay_2_ypo import gera_poema

### bof: settings

# the User IPAddress for LYPO, TYPO
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

def have_internet():
    try:
        # Tenta conectar ao IP da Cloudflare na porta 80 (HTTP)
        socket.create_connection(("1.1.1.1", 80), timeout=3)
        return True
    except OSError:
        return False
        
st.set_page_config(
    page_title="a Machina de fazer Poesia - yPoemas",
    page_icon="★",
    layout="centered",
    initial_sidebar_state="expanded",
)

if have_internet():
    try:
        from deep_translator import GoogleTranslator
        from gtts import gTTS
    except ImportError:
        st.warning("Dependências ausentes no requirements.txt")
else:
    st.warning("Internet não conectada. Traduções não disponíveis no momento.")

# --- BLOCO ÚNICO DE CSS (Otimizado) ---
st.markdown(
    """
    <style>
    /* 1. Respiro no topo: Ajustado para o ponto ideal */
    .block-container {
        padding-top: 2rem !important; 
        margin-top: 0px !important;
    }

    /* 2. Sidebar e Botão de Colapso (>>) */
    [data-testid="stSidebar"] {
        width: 310px !important;
        min-width: 310px !important;
    }

    [data-testid="stSidebarCollapseButton"] {
        left: 310px !important;
        z-index: 999999;
    }

    /* 3. Estética do Poema */
    mark { background-color: powderblue; color: black; }
    .logo-text {
        font-weight: 600;
        font-size: 16px;
        font-family: 'IBM Plex Sans';
        color: #000000;
        padding-left: 5px;
    }
    header { visibility: hidden; height: 0px; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)
### eof: settings

# ... [Mantenha os SessionState como estão no seu original] ...

### bof: tools

def pick_lang():  # define idioma de forma horizontal na sidebar
    with st.sidebar:
        cols = st.columns([1, 1, 1, 1, 1, 1])
        
        btn_pt = cols[0].button("pt", help="Português")
        btn_es = cols[1].button("es", help="Español")
        btn_it = cols[2].button("it", help="Italiano")
        btn_fr = cols[3].button("fr", help="Français")
        btn_en = cols[4].button("en", help="English")
        btn_xy = cols[5].button("⚒️", help=st.session_state.poly_name)

        if btn_pt:
            st.session_state.lang = "pt"
            st.session_state.poly_file = "poly_pt.txt"
        elif btn_es:
            st.session_state.lang = "es"
            st.session_state.poly_file = "poly_es.txt"
        elif btn_it:
            st.session_state.lang = "it"
            st.session_state.poly_file = "poly_it.txt"
        elif btn_fr:
            st.session_state.lang = "fr"
            st.session_state.poly_file = "poly_fr.txt"
        elif btn_en:
            st.session_state.lang = "en"
            st.session_state.poly_file = "poly_en.txt"
        elif btn_xy:
            st.session_state.last_lang = st.session_state.lang
            st.session_state.lang = st.session_state.poly_lang

# ... [Mantenha as funções translate, load_help, etc.] ...

def main():
    chosen_id = stx.tab_bar(
        data=[
            stx.TabBarItemData(id=1, title="mini", description=""),
            stx.TabBarItemData(id=2, title="yPoemas", description=""),
            stx.TabBarItemData(id=3, title="eureka", description=""),
            stx.TabBarItemData(id=4, title="off-machina", description=""),
            stx.TabBarItemData(id=5, title="books", description=""),
            stx.TabBarItemData(id=6, title="poly", description=""),
            stx.TabBarItemData(id=7, title="about", description=""),
        ],
        default=2,
    )

    pick_lang()
    draw_check_buttons()

    # Correção das vírgulas nas atribuições de magy
    if chosen_id == "1":
        st.sidebar.info(load_md_file("INFO_MINI.md"))
        magy = "./images/img_mini.jpg"
        page_mini()
    elif chosen_id == "2":
        st.sidebar.info(load_md_file("INFO_YPOEMAS.md"))
        magy = "./images/img_ypoemas.jpg"
        page_ypoemas()
    elif chosen_id == "3":
        st.sidebar.info(load_md_file("INFO_EUREKA.md"))
        magy = "./images/img_eureka.jpg"
        page_eureka()
    elif chosen_id == "4":
        st.sidebar.info(load_md_file("INFO_OFF-MACHINA.md"))
        magy = "./images/img_off-machina.jpg"
        page_off_machina()
    elif chosen_id == "5":
        st.sidebar.info(load_md_file("INFO_BOOKS.md"))
        magy = "./images/img_books.jpg"
        page_books()
    elif chosen_id == "6":
        st.sidebar.info(load_md_file("INFO_POLY.md"))
        magy = "./images/img_poly.jpg"
        page_polys()
    elif chosen_id == "7":
        st.sidebar.info(load_md_file("INFO_ABOUT.md"))
        magy = "./images/img_about.jpg"
        page_abouts()

    with st.sidebar:
        # Só tenta carregar se magy for uma string válida
        if 'magy' in locals() and isinstance(magy, str):
            st.image(magy)

    show_icons()

if __name__ == "__main__":
    main()
