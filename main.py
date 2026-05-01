import streamlit as st

def main():
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = "mini"

    # CSS DE ELIMINAÇÃO DE OBSTÁCULOS
    st.markdown("""
        <style>
            /* Eliminar o travamento horizontal do container pai */
            [data-testid="stAppViewContainer"] {
                display: flex;
                flex-direction: row;
                width: 100vw !important;
            }

            /* O PALCO: Eliminar margens fixas. 
               O segredo é o flex-grow e a largura dinâmica */
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

            /* A SIDEBAR: Eliminamos a flutuação. 
               Ela agora ocupa seu espaço físico de 300px ou zero. */
            [data-testid="stSidebar"] {
                min-width: 300px !important;
                width: 300px !important;
            }
            
            /* Ajuste técnico para o modo recolhido não deixar 'lixo' de 0px ou sombras */
            [data-testid="stSidebar"][aria-expanded="false"] {
                min-width: 0px !important;
                width: 0px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### Painel de Controle")
        st.divider()

    # NAVEGAÇÃO PROPORCIONAL (A Regra Perfeita)
    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre"]
    big_page_atual = st.session_state.pagina_ativa

    # Pesos matemáticos baseados nas letras
    pesos = [len(pg)/4 * (1.25 if pg == big_page_atual else 1.0) for pg in paginas]
    
    cols = st.columns(pesos)
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

    st.divider()
    st.write(f"Estado do Palco: **{big_page_atual.upper()}**")

if __name__ == "__main__":
    main()
