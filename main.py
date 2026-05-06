import streamlit as st
import random
import os
import time

# --- PROTOCOLO DE CONFIGURAÇÃO DA SIDEBAR ---

def init_sidebar_styles():
    """Aplica o esmero visual: largura fixa de 300px na sidebar"""
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            min-width: 300px;
            max-width: 300px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def pick_lang():
    """
    Gerencia a seleção global de idiomas na sidebar.
    Utiliza estritamente a lista oficial definida.
    """
    languages = ["Português", "Español", "Italiano", "Français", "English", "Català"]
    codes = ["pt", "es", "it", "fr", "en", "ca"]
    
    if "lang" not in st.session_state:
        st.session_state.lang = "pt"
    st.session_state.last_lang = st.session_state.lang

    with st.sidebar:
        st.markdown(f"### {translate('Idioma')}")
        idx = codes.index(st.session_state.lang) if st.session_state.lang in codes else 0
        sel = st.selectbox("↓", languages, index=idx, label_visibility="collapsed")
        st.session_state.lang = codes[languages.index(sel)]

def draw_check_buttons():
    """Controles globais de renderização gráfica e áudio na sidebar"""
    with st.sidebar:
        st.markdown("---")
        if "draw" not in st.session_state:
            st.session_state.draw = True
        st.session_state.draw = st.checkbox(translate("exibir artes visuais"), value=st.session_state.draw)
        
        if "talk" not in st.session_state:
            st.session_state.talk = False
        st.session_state.talk = st.checkbox(translate("ativar leitura (talk)"), value=st.session_state.talk)
        st.markdown("---")


# --- BLOCO PRINCIPAL DA APLICAÇÃO ---

def main():
    init_sidebar_styles()
    
    # Renderização da barra de abas principal
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

    # Fluxo de roteamento das páginas conforme a aba selecionada
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

    # Renderização da imagem contextual na base da sidebar
    with st.sidebar:
        st.image(magy)

    show_icons()
    st.sidebar.state = True


if __name__ == "__main__":
    main()
