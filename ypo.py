def page_ypoemas():
    # 1. GARANTIA DE DADOS (Executa antes de desenhar qualquer botão)
    if not os.path.exists("./data"):
        st.error("Pasta /data não encontrada.")
        return

    books_list = sorted([f for f in os.listdir("./data") if os.path.isdir(os.path.join("./data", f)) and not f.startswith('.')])
    
    # Inicialização forçada para evitar telas vazias no primeiro carregamento
    if 'book' not in st.session_state: st.session_state.book = books_list[0]
    
    # Carregamos a lista de temas IMEDIATAMENTE
    temas_list = load_temas(st.session_state.book)
    
    if 'take' not in st.session_state: st.session_state.take = 0
    if 'draw' not in st.session_state: st.session_state.draw = True

    # --- TETO: SELETOR DE LIVROS ---
    # Usamos o on_change para forçar o sistema a "acordar" na troca de livro
    def change_book():
        st.session_state.take = 0

    st.selectbox("BIBLIOTECA", books_list, 
                 index=books_list.index(st.session_state.book), 
                 key="book", 
                 on_change=change_book,
                 label_visibility="collapsed")

    # --- COCKPIT: COMANDOS ---
    c1, c2, c3, c4, c5, c_sel = st.columns([0.5, 0.5, 0.5, 0.5, 0.5, 4.5])
    
    # Definimos as funções de navegação para evitar o "atraso" do clique
    with c1: 
        if st.button("◀", key="b_prev"):
            st.session_state.take = (st.session_state.take - 1) % len(temas_list)
            st.rerun()
    with c2: 
        if st.button("✻", key="b_rand"):
            st.session_state.take = random.randrange(len(temas_list))
            st.rerun()
    with c3: 
        if st.button("▶", key="b_next"):
            st.session_state.take = (st.session_state.take + 1) % len(temas_list)
            st.rerun()
    with c4: 
        if st.button("✚", key="b_draw"):
            st.session_state.draw = not st.session_state.draw
            st.rerun()
    with c5: 
        st.button("?", key="b_help")

    with c_sel:
        # Seletor de Temas (Radar)
        st.selectbox("Radar", range(len(temas_list)), 
                     index=st.session_state.take,
                     format_func=lambda x: temas_list[x].replace("_", " ").title(),
                     label_visibility="collapsed", 
                     key="take") # O próprio selectbox altera o session_state.take

    # --- EXECUÇÃO DE EXIBIÇÃO (FORA DE QUALQUER IF) ---
    # Isso garante que, se a página carregar, o conteúdo TEM que ser desenhado
    try:
        tema_atual = temas_list[st.session_state.take]
        texto = load_poema(tema_atual, st.session_state.book)
        imagem = load_arts(tema_atual) if st.session_state.draw else None
        
        # O "Container" vazio que força a limpeza da tela antes de escrever
        placeholder = st.empty()
        with placeholder.container():
            write_ypoema(texto, imagem)
    except Exception as e:
        st.info("Navegando entre as águas da Samizdát... clique em um tema.")
