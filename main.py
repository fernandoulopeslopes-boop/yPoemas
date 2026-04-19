#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tools import load_temas_ativos, zay_number
import streamlit as st

IDIOMAS = {
    'Português': 'pt',
    'Espanhol': 'es',
    'Italiano': 'it',
    'Francês': 'fr',
    'Inglês': 'en',
    'Catalão': 'ca',
    'Córsico': 'co',
    'Galego': 'gl',
    'Basco': 'eu',
    'Esperanto': 'eo',
    'Latin': 'la',
    'Galês': 'cy',
    'Sueco': 'sv',
    'Polonês': 'pl',
    'Holandês': 'nl',
    'Norueguês': 'no',
    'Finlandês': 'fi',
    'Dinamarquês': 'da',
    'Irlandês': 'ga',
    'Romeno': 'ro',
    'Russo': 'ru'
}

INFO_AUTOR = "Machina Ypoemas: escultura de texto, som e imagem. Autor: Zay."

def main():
    st.set_page_config(
        page_title="Ypoemas",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    ativos = load_temas_ativos()

    # Estado da Machina
    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = "yPoemas"

    if 'livro_atual' not in st.session_state:
        st.session_state.livro_atual = "Livro_01"

    if 'tema_atual' not in st.session_state:
        st.session_state.tema_atual = list(ativos.keys())[0] if ativos else "tema_vazio"

    # Sidebar = Cockpit do leitor
    with st.sidebar:
        st.title("Cockpit")
        idioma = st.selectbox("Idioma", options=list(IDIOMAS.keys()))
        st.divider()
        st.subheader("Controles do Palco")
        show_arte = st.checkbox("Arte", value=True)
        show_som = st.checkbox("Som", value=True)
        show_video = st.checkbox("Vídeo", value=True)
        st.divider()
        st.subheader("Info")
        st.caption(INFO_AUTOR)
        st.divider()
        st.caption(f"Página: {st.session_state.pagina_atual}")

    # Botões das 6 páginas - sempre no topo
    paginas = ["mini", "yPoemas", "Eureka", "off-mach", "Comments", "About"]
    cols = st.columns(6)
    for i, pagina in enumerate(paginas):
        with cols[i]:
            if st.button(pagina, use_container_width=True, key=f"btn_{pagina}"):
                st.session_state.pagina_atual = pagina
                st.rerun()

    st.divider()

    # Roteamento das páginas
    if st.session_state.pagina_atual == "mini":
        st.title("mini")
        st.write("Conteúdo da página mini.")

    elif st.session_state.pagina_atual == "yPoemas":
        # Botões de navegação centralizados
        _, nav_col, _ = st.columns([2,3,2])
        with nav_col:
            b1,b2,b3,b4,b5 = st.columns(5)
            b1.button("+", help="Mais uma variação do tema", key="btn_mais")
            b2.button("<", help="Tema anterior", key="btn_ant")
            b3.button("*", help="Tema aleatório", key="btn_rand")
            b4.button(">", help="Próximo tema", key="btn_prox")
            b5.button("?", help="Help: O que é isso? Onde estou? Como usar?", key="btn_help")

        # Layout 3 colunas: livros | palco | temas
        col_livros, col_palco, col_temas = st.columns([1,3,1])

        with col_livros:
            st.subheader("Livros")
            livros = ["Livro_01", "Livro_02", "Livro_03"]
            livro_sel = st.radio(" ", livros, index=livros.index(st.session_state.livro_atual), label_visibility="collapsed", key="radio_livros")
            if livro_sel!= st.session_state.livro_atual:
                st.session_state.livro_atual = livro_sel
                st.rerun()

        with col_palco:
            st.subheader(f"Palco: {st.session_state.tema_atual}")
            st.write(f"Idioma: {idioma} | Código: {IDIOMAS[idioma]}")
            st.write(f"Controles: Arte={show_arte} | Som={show_som} | Vídeo={show_video}")
            st.caption(f"Tipo: {ativos.get(st.session_state.tema_atual, 'N/A')}")
            st.caption(f"Zay: {zay_number(st.session_state.tema_atual)}")
            st.divider()
            st.write("Área de apresentação do tema.")

        with col_temas:
            st.subheader("Temas")
            temas_do_livro = list(ativos.keys())
            if temas_do_livro:
                tema_sel = st.radio(" ", temas_do_livro, index=temas_do_livro.index(st.session_state.tema_atual), label_visibility="collapsed", key="radio_temas")
                if tema_sel!= st.session_state.tema_atual:
                    st.session_state.tema_atual = tema_sel
                    st.rerun()
            else:
                st.write("Nenhum tema ativo.")

    elif st.session_state.pagina_atual == "Eureka":
        st.title("Eureka")
        st.write("Conteúdo da página Eureka.")

    elif st.session_state.pagina_atual == "off-mach":
        st.title("off-mach")
        st.write("Conteúdo da página off-mach.")

    elif st.session_state.pagina_atual == "Comments":
        st.title("Comments")
        st.write("Conteúdo da página Comments.")

    elif st.session_state.pagina_atual == "About":
        st.title("About")
        st.write("Conteúdo da página About.")

if __name__ == "__main__":
    main()
