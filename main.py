import streamlit as st

def main():
    # 1. ESTADO INTERNO
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = "mini"
    if 'idioma' not in st.session_state:
        st.session_state.idioma = "Português"

    # 2. CSS: DOMA DA SIDEBAR E EXPANSÃO DO PALCO
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {
                display: flex;
                flex-direction: row;
                width: 100vw !important;
            }
            .main {
                flex-grow: 1;
                width: auto !important;
            }
            .main .block-container {
                max-width: 98vw !important;
                width: 98vw !important;
                margin-left: auto !important;
                margin-right: auto !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                transition: width 0.3s ease-in-out;
            }
            [data-testid="stSidebar"] {
                min-width: 300px !important;
                width: 300px !important;
            }
            [data-testid="stSidebar"][aria-expanded="false"] {
                min-width: 0px !important;
                width: 0px !important;
            }
            [data-testid="stHeader"] {
                background: transparent !important;
            }
            /* Estilização dos Botões de Topo na Sidebar */
            .sidebar-top-btns {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # 3. SIDEBAR: PAINEL DE CONTROLE POPULADO
    with st.sidebar:
        # Botões de Topo: Talk e Arts
        col_t, col_a = st.columns(2)
        with col_t:
            if st.button("💬 Talk", use_container_width=True):
                st.toast("Talk Mode Ativado")
        with col_a:
            if st.button("🎨 Arts", use_container_width=True):
                st.toast("Arts Mode Ativado")
        
        st.divider()

        # Seletor de Idiomas (Alfabeto Ocidental apenas)
        idiomas = ["Português", "English", "Español", "Français", "Deutsch", "Italiano"]
        st.session_state.idioma = st.selectbox("Tradução (Machina)", idiomas)
        
        st.divider()

        # Informações da Máquina
        st.markdown("### a Máquina")
        st.caption("Versão: yPoemas / Machina")
        st.info(f"Idioma ativo: {st.session_state.idioma}")
        
        # Espaço para futuros controles de som/permutações
        st.slider("Intensidade das Permutações", 0, 100, 50)

    # 4. PALCO: NAVEGAÇÃO PROPORCIONAL
    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre"]
    big_page_atual = st.session_state.pagina_ativa

    # Regra baseada nas letras: 'm' de mini e 'e' de sobre alinhados à moldura
    pesos = [len(pg)/4 * (1.25 if pg == big_page_atual else 1.0) for pg in paginas]
    
    cols = st.columns(pesos)
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"btn_{pg}", use_container_width=True):
                st.session_state.pagina_ativa = pg
                st.rerun()

    st.divider()

if __name__ == "__main__":
    main()
