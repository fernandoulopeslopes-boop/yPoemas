def main():
    # --- 1. BOF: INICIALIZAÇÃO DE SEGURANÇA ---
    # Garante que todas as chaves existam antes de qualquer função chamá-las
    keys_to_init = {
        "talk": False, 
        "arts": False, 
        "lang": "pt", 
        "poly_name": "Custom",
        "poly_lang": "en"
    }
    
    for key, value in keys_to_init.items():
        if key not in st.session_state:
            st.session_state[key] = value
    # --- EOF: INICIALIZAÇÃO DE SEGURANÇA ---

    # 2. Renderização da TabBar
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

    # 3. Chamada das funções da Sidebar (Cockpit)
    pick_lang()          # Agora com as variáveis de idioma seguras
    draw_check_buttons() # Agora com 'talk' e 'arts' inicializados

    # 4. Lógica de navegação e carregamento de imagens
    # Removidas as vírgulas extras para evitar o MediaFileStorageError
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

    # 5. Renderização final da imagem na sidebar
    with st.sidebar:
        if 'magy' in locals() and isinstance(magy, str):
            st.image(magy)

    show_icons()
