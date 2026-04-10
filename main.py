def build_sidebar():
    with st.sidebar:
        # Título Original
        st.markdown("## a máquina de fazer Poesia")
        
        # 1. pick_lang() - Apenas botões, sem labels
        st.divider()
        c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 1, 1, 1, 1])
        if c1.button("pt"): st.session_state.lang = "pt"
        if c2.button("es"): st.session_state.lang = "es"
        if c3.button("it"): st.session_state.lang = "it"
        if c4.button("fr"): st.session_state.lang = "fr"
        if c5.button("en"): st.session_state.lang = "en"
        if c6.button("⚒️"): st.session_state.lang = "poly"
        
        st.divider()
        
        # 2. Navegação de Páginas (Radio limpo)
        page = st.radio("", ["Mini", "yPoemas", "Eureka"], 
                        index=1, label_visibility="collapsed")
        
        st.divider()
        
        # 3. Seletores de Contexto (Aparecem conforme a página)
        if page == "yPoemas":
            # Livros e Temas (Sem labels explicativos)
            st.selectbox("", ["livro vivo", "todos os temas"], 
                         key="book_sel", label_visibility="collapsed")
            st.selectbox("", ["Fatos", "Amor", "Morte"], 
                         key="tema_sel", label_visibility="collapsed")
        
        st.divider()
        
        # 4. draw_check_buttons() - Checkboxes de Sentidos
        col_draw, col_talk = st.columns(2)
        st.session_state.draw = col_draw.checkbox("Imagem", value=st.session_state.draw)
        st.session_state.talk = col_talk.checkbox("Áudio", value=st.session_state.talk)
        
        st.divider()
        
        # 5. Rodapé: show_icons() e Leituras (O que faltava do PAI)
        # Ícones sociais/links rápidos
        st.write("✨ 📚 ✉️ ☕") 
        
        # Checkbox de Leituras (list_readings)
        if st.checkbox("Leituras", value=False):
            st.caption("Últimas sementes: amar, vida, destino...")

        return page
