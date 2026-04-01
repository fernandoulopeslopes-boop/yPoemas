elif menu == "Eureka":
    st.subheader("🔍 Módulo Eureka - Busca por Sementes")
    
    # Campo de entrada para a "Eureka Seed" (A semente da descoberta)
    with st.sidebar:
        st.markdown("---")
        eureka_input = st.text_input("Insira a Seed/Chave:", value=str(st.session_state.eureka), help="Uma chave numérica ou texto para fixar o poema")
        if st.button("Fixar Chave"):
            st.session_state.eureka = eureka_input
            st.success(f"Chave {eureka_input} aplicada!")

    # Seleção de Tema para a busca
    temas_disponiveis = load_temas(st.session_state.book)
    tema_escolhido = st.selectbox("Escolha o Tema para a busca Eureka:", temas_disponiveis, index=temas_disponiveis.index(st.session_state.tema) if st.session_state.tema in temas_disponiveis else 0)

    if st.button("Executar Eureka"):
        with st.spinner(f"Garimpando versos com a chave {st.session_state.eureka}..."):
            # A função gera_poema no lay_2_ypo usa a seed para travar a aleatoriedade
            poema_eureka = load_poema(tema_escolhido, st.session_state.eureka)
            
            # Tradução e Exibição
            poema_final = translate(poema_eureka)
            
            # Exibe o resultado com o estilo da Machina
            write_ypoema(poema_final, None)
            
            # Se o áudio estiver ativo
            if st.session_state.talk:
                talk(poema_final)
                
    st.info("O Módulo Eureka permite que você replique poemas exatos usando a mesma chave e tema.")
