import streamlit as st

def main():
    # 1. ESTADO DA MACHINA
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = "mini"
    if 'idioma' not in st.session_state:
        st.session_state.idioma = "Português"

    # 2. CSS: DOMA DA SIDEBAR E ELASTICIDADE DO PALCO
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
            /* Eliminar decorações desnecessárias nos botões da sidebar */
            .stButton > button {
                width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)

    # 3. SIDEBAR: PAINEL DE CONTROLE (CONTEÚDO E FUNCIONALIDADE)
    with st.sidebar:
        # Topo: Talk e Arts
        col_t, col_a = st.columns(2)
        with col_t:
            st.button("Talk")
        with col_a:
            st.button("Arts")
        
        st.divider()

        # Translator: Restrito ao alfabeto ocidental
        idiomas_ocidentais = ["Português", "English", "Español", "Français", "Deutsch", "Italiano"]
        st.session_state.idioma = st.selectbox("Translator", idiomas_ocidentais)
        
        st.divider()

        # Identificação e Status
        st.markdown("### a Máquina de Fazer Poesia")
        st.caption("yPoemas / Machina")

    # 4. PALCO: NAVEGAÇÃO PROPORCIONAL (EXTREMOS 'm' E 'e' ALINHADOS)
    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre"]
    big_page_atual = st.session_state.pagina_ativa

    # Pesos baseados no comprimento (4 letras = 1.0)
    pesos = [len(pg)/4 * (1.25 if pg == big_page_atual else 1.0) for pg in paginas]
    
    cols = st.columns(pesos)
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

    st.divider()

if __name__ == "__main__":
    main()
