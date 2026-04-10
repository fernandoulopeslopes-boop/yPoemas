# =================================================================
# 🚀 NAVEGAÇÃO PURIFICADA (SIDEBAR) - SEM INTRUSOS
# =================================================================

def build_sidebar():
    with st.sidebar:
        st.write("### a máquina de fazer Poesia")
        
        st.write("---")
        # 1. pick_lang (Seletor de Idiomas original)
        pick_lang()
        
        st.write("---")
        # 2. Navegação Direta (Substituindo Radio Buttons)
        # Usando botões para mudar a página no session_state
        if st.button("Mini", key="nav_mini"): 
            st.session_state.page = "Mini"
        if st.button("yPoemas", key="nav_ypo"): 
            st.session_state.page = "yPoemas"
        if st.button("Eureka", key="nav_eureka"): 
            st.session_state.page = "Eureka"
        
        st.write("---")
        # 3. Sentidos (Sem selectboxes de tema aqui, apenas controles)
        st.session_state.draw = st.checkbox("Art", value=(st.session_state.draw == 'Y'))
        st.session_state.talk = st.checkbox("Talk", value=(st.session_state.talk == 'Y'))
        
        st.write("---")
        # 4. Rodapé e Ícones
        show_icons()
        st.checkbox("Show Readings", value=False)
        st.button("Share")

# --- EXECUÇÃO DO PAI ---
def main_execution():
    # Define a página atual baseada no botão clicado
    if "page" not in st.session_state:
        st.session_state.page = "yPoemas"
        
    build_sidebar()
    
    if st.session_state.page == "yPoemas":
        page_ypoemas()
    elif st.session_state.page == "Mini":
        page_mini()
    elif st.session_state.page == "Eureka":
        st.write("Página Eureka") # Local para o código da Eureka

if __name__ == "__main__":
    main_execution()
