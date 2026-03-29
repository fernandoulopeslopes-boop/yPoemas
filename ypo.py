def page_ypoemas():
    # --- 1. O TETO (A BIBLIOTECA) ---
    # Listamos as pastas de livros (os 13 Rols)
    books_path = "./books"
    books_list = sorted([f for f in os.listdir(books_path) if os.path.isdir(os.path.join(books_path, f)) and not f.startswith('.')])
    
    # Seletor de Livro (Cápsula de topo)
    if st.session_state.book not in books_list:
        st.session_state.book = books_list[0]
        
    book_selection = st.selectbox(
        label="📖 " + translate("BIBLIOTECA"),
        options=books_list,
        index=books_list.index(st.session_state.book),
        key="selector_books_top"
    )

    # Se o usuário trocar o livro, resetamos o 'take' (poema) para o início
    if book_selection != st.session_state.book:
        st.session_state.book = book_selection
        st.session_state.take = 0
        st.rerun()

    # --- 2. O RADAR (OS TEMAS) ---
    temas_list = load_temas(st.session_state.book)
    max_idx = len(temas_list) - 1
    
    # Segurança para o índice
    if st.session_state.take > max_idx:
        st.session_state.take = 0

    # --- 3. O COCKPIT DE COMANDO (BOTÕES + PICK-LIST) ---
    help_tips = load_help(st.session_state.lang)
    
    # 5 colunas para botões e 1 larga para o seletor de temas
    c1, c2, c3, c4, c5, c_sel = st.columns([0.6, 0.6, 0.6, 0.6, 0.6, 4.0])

    with c1: last_btn = st.button("◀", help=help_tips[0], key="btn_prev")
    with c2: rand_btn = st.button("✻", help=help_tips[1], key="btn_rand")
    with c3: next_btn = st.button("▶", help=help_tips[2], key="btn_next")
    with c4: more_btn = st.button("✚", help=help_tips[4], key="btn_more")
    with c5: manu_btn = st.button("?", help="Help / Manual", key="btn_help")

    with c_sel:
        # O seletor de temas agora é um "radar" dentro da linha de comando
        tema_idx = st.selectbox(
            label="Seletor de Temas",
            options=list(range(len(temas_list))),
            index=st.session_state.take,
            format_func=lambda x: temas_list[x].replace("_", " ").title(),
            key="selector_temas",
            label_visibility="collapsed"
        )

    # --- 4. LÓGICA DE NAVEGAÇÃO ---
    if tema_idx != st.session_state.take:
        st.session_state.take = tema_idx
        st.rerun()
    if last_btn:
        st.session_state.take = (st.session_state.take - 1) % len(temas_list)
        st.rerun()
    if next_btn:
        st.session_state.take = (st.session_state.take + 1) % len(temas_list)
        st.rerun()
    if rand_btn:
        st.session_state.take = random.randrange(0, len(temas_list))
        st.rerun()

    # --- 5. A PRENSA (O POEMA) ---
    st.session_state.tema = temas_list[st.session_state.take]
    
    # Carrega o conteúdo e exibe: Texto primeiro, Imagem depois
    raw_text = load_poema(str(st.session_state.tema), "")
    
    # Tradução automática se necessário
    if st.session_state.lang != "pt":
        raw_text = translate(raw_text)

    # Formatação HTML para preservar o desenho das estrofes
    linhas = [l.lstrip().strip() for l in raw_text.split('\n')]
    texto_html = "<br>".join([l if l else "&nbsp;" for l in linhas])

    # Visualização final
    img = load_arts(st.session_state.tema) if st.session_state.draw else None
    write_ypoema(texto_html, img)
