import streamlit as st

def main():
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = "mini"

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
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.divider()

    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre"]
    big_page_atual = st.session_state.pagina_ativa

    pesos = [len(pg)/4 * (1.25 if pg == big_page_atual else 1.0) for pg in paginas]
    
    cols = st.columns(pesos)
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

if __name__ == "__main__":
    main()
