import streamlit as st

def main():
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = "mini"
    if 'idioma' not in st.session_state:
        st.session_state.idioma = "Português"

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
                padding-top: 2rem !important;
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
            .stButton > button {
                width: 100%;
                font-size: 22px !important;
                padding: 0px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        col_t, col_a = st.columns(2)
        with col_t:
            st.button("Talk")
        with col_a:
            st.button("Arts")
        
        st.divider()

        # LISTA DE IDIOMAS OCIDENTAIS (SORTED ATÉ SV)
        idiomas_base = ["Português", "English", "Español", "Français", "Deutsch", "Italiano"]
        outros = sorted(["Dansk", "Suomi", "Norsk", "Svenska", "Nederlands", "Portuñol"])
        lista_completa = idiomas_base + [i for i in outros if i not in idiomas_base]
        
        st.session_state.idioma = st.selectbox("Translator", lista_completa)
        
        st.divider()

        st.markdown("### a Máquina de Fazer Poesia")
        st.caption("yPoema / Machina")

    # NAVEGAÇÃO: PROPORÇÃO EXATA PELA QUANTIDADE DE LETRAS
    paginas = ["mini", "yPoema", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre"]
    
    # PESO = NÚMERO DE CARACTERES (PROPORÇÃO PURA)
    pesos = [len(pg) for pg in paginas]
    
    cols = st.columns(pesos)
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

    st.divider()

if __name__ == "__main__":
    main()
