import streamlit as st

def main():
    # 1. ESTADOS DA MACHINA
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = "mini"

    # 2. CSS DE CONTROLE DE FLUXO (Sidebar vs Palco)
    # Foco: Garantir que o palco ocupe o espaço quando a sidebar recolher
    st.markdown("""
        <style>
            /* Container Total */
            [data-testid="stAppViewContainer"] {
                width: 100vw !important;
            }

            /* O Palco: Ajusta-se dinamicamente ao espaço disponível */
            .main .block-container {
                max-width: 98vw !important;
                width: 98vw !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                transition: all 0.3s ease;
            }

            /* A Sidebar: Travada em 300px quando visível */
            [data-testid="stSidebar"] {
                min-width: 300px !important;
                width: 300px !important;
            }
            
            /* Ajuste para o botão de colapso nativo não gerar lixo visual */
            [data-testid="stSidebarCollapseButton"] {
                right: 0;
            }
        </style>
    """, unsafe_allow_html=True)

    # 3. SIDEBAR (O Painel de Controle)
    with st.sidebar:
        st.write("### Painel de Controle")
        st.divider()
        # Aqui serão inseridos os controles de idioma, arte e som
        st.info("Sidebar Ativa (300px)")

    # 4. O PALCO (Área Central Resolvida)
    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre"]
    big_page_atual = st.session_state.pagina_ativa

    # Regra Matemática de Proporções (Validada)
    pesos = [len(pg)/4 * (1.25 if pg == big_page_atual else 1.0) for pg in paginas]
    
    cols = st.columns(pesos)
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

    st.divider()
    st.write(f"Palco expandido para a página: **{st.session_state.pagina_ativa.upper()}**")

if __name__ == "__main__":
    main()
