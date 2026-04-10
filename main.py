### bof: main execution logic


def main():
    # Sidebar: Título e Navegação
    with st.sidebar:
        st.markdown("## a máquina de fazer Poesia")
        
        # Seletor de Idiomas (como definido na sua função pick_lang)
        pick_lang()
        
        st.divider()
        
        # Menu de Navegação (Ajustado para o seu padrão de abas)
        page = st.radio(
            translate("Navegação"),
            ["Mini", "yPoemas", "Eureka"],
            index=0,
            key="main_nav"
        )
        
        st.divider()
        
        # Controles globais (Art, Talk)
        draw_check_buttons()
        
        # Rodapé da sidebar
        show_icons()
        if st.checkbox(translate("Exibir Leituras")):
            list_readings()

    # Roteamento de Páginas
    if page == "Mini":
        page_mini()
    elif page == "yPoemas":
        page_ypoemas()
    elif page == "Eureka":
        page_eureka()

if __name__ == "__main__":
    # Inicialização do estado de áudio se não existir
    if "voice" not in st.session_state:
        st.session_state.voice = "pt-BR-AntonioNeural"
    
    main()
