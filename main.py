#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from tools import load_temas_ativos, zay_number

IDIOMAS = {
    'Português': 'pt', 'Espanhol': 'es', 'Italiano': 'it',
    'Francês': 'fr', 'Inglês': 'en', 'Catalão': 'ca'
}

INFO_AUTOR = "Machina Ypoemas: escultura de texto, som e imagem. Autor: Zay."

def main():
    st.set_page_config(
        page_title="Ypoemas",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # CSS pra deszonear o palco
    st.markdown("""
    <style>
    /* 1. Botões de página: evita quebra do título */
   .stButton button {
        white-space: nowrap;
        padding: 0.25rem 0.75rem;
        font-size: 14px;
    }

    /* 2. Radio buttons em linha, não coluna */
    div[data-testid="stRadio"] > div {
        flex-direction: row;
        flex-wrap: wrap;
        gap: 1rem;
    }

    /* 3. Remove espaço extra do topo */
   .block-container {
        padding-top: 1rem;
    }

    /* Ajusta colunas do palco */
    div[data-testid="column"] {
        padding: 0 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = "yPoemas"
    if 'temas_ativos' not in st.session_state:
        st.session_state.temas_ativos = load_temas_ativos()

    temas = list(st.session_state.temas_ativos.keys())

    # Sidebar = Cockpit
    with st.sidebar:
        st.title("Cockpit")
        st.selectbox("Idioma", options=list(IDIOMAS.keys()), key="sel_idioma")
        st.divider()
        st.subheader("Controles do Palco")

        # 3. Controles na horizontal com texto curto
        c1, c2, c3 = st.columns(3)
        with c1:
            st.checkbox("Art", value=True, key="chk_arte")
        with c2:
            st.checkbox("Som", value=True, key="chk_som")
        with c3:
            st.checkbox("Wyd", value=True, key="chk_video")

        st.divider()
        st.subheader("Info")
        st.caption(INFO_AUTOR)
        st.divider()
        st.caption(f"Página: {st.session_state.pagina_atual}")

    # Botões das 6 páginas
    paginas = ["mini", "yPoemas", "Eureka", "off-mach", "Comments", "About"]
    cols = st.columns(6)
    for i, pagina in enumerate(paginas):
        with cols[i]:
            if st.button(pagina, use_container_width=True, key=f"btn_{pagina}"):
                st.session_state.pagina_atual = pagina
                st.rerun()

    st.divider()

    if st.session_state.pagina_atual == "mini":
        st.title("mini")

    elif st.session_state.pagina_atual == "yPoemas":
        _, nav_col, _ = st.columns([2,3,2])
        with nav_col:
            b1,b2,b3,b4,b5 = st.columns(5)
            b1.button("+", key="btn_mais")
            b2.button("<", key="btn_ant")
            b3.button("*", key="btn_rand")
            b4.button(">", key="btn_prox")
            b5.button("?", key="btn_help")

        col_livros, col_palco, col_temas = st.columns([1,3,1])
        with col_livros:
            st.subheader("Livros")
            st.radio(" ", ["Livro_01"], key="radio_livros", label_visibility="collapsed")
        with col_palco:
            st.subheader("Palco")
            st.write(f"Zay: {zay_number(temas[0]) if temas else '---'}")
        with col_temas:
            st.subheader("Temas")
            st.radio(" ", temas, key="radio_temas", label_visibility="collapsed")

    elif st.session_state.pagina_atual == "Eureka":
        st.title("Eureka")
    elif st.session_state.pagina_atual == "off-mach":
        st.title("off-mach")
    elif st.session_state.pagina_atual == "Comments":
        st.title("Comments")
    elif st.session_state.pagina_atual == "About":
        st.title("About")

if __name__ == "__main__":
    main()
