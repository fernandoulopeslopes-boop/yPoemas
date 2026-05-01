import streamlit as st
import os

def main():
    # 1. ESTADO DA MACHINA
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = "mini"

    # 2. CSS DE DOMA E ELIMINAÇÃO DE RESÍDUOS
    st.markdown("""
        <style>
            /* Eliminar limitações de largura do container pai */
            [data-testid="stAppViewContainer"] {
                width: 100vw !important;
            }

            /* O PALCO: Definido para ocupar 98% da largura da tela (Viewport Width) */
            /* Isso garante que ele se expanda automaticamente quando a sidebar é recolhida */
            .main .block-container {
                max-width: 98vw !important;
                width: 98vw !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                transition: all 0.3s ease-in-out;
            }

            /* A SIDEBAR: Travada em 300px para o controle ser estável */
            [data-testid="stSidebar"] {
                min-width: 300px !important;
                width: 300px !important;
            }

            /* Eliminar o fundo padrão do header para manter a limpeza visual */
            [data-testid="stHeader"] {
                background: transparent !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # 3. SIDEBAR (Painel de Controle Limpo)
    with st.sidebar:
        st.markdown("### Painel de Controle")
        st.divider()
        # Eliminar informações desnecessárias e focar nos futuros controles
        st.caption("Controle de Expansão Ativo")

    # 4. NAVEGAÇÃO PROPORCIONAL (Regra das Letras)
    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre"]
    big_page_atual = st.session_state.pagina_ativa

    # Pesos baseados no comprimento das palavras (Matemática validada)
    # 4 letras = 1.0 de peso base
    pesos = [len(pg)/4 * (1.25 if pg == big_page_atual else 1.0) for pg in paginas]
    
    cols = st.columns(pesos)
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

    st.divider()
    # O palco agora reage à sidebar: se recolher a lateral, este texto e os botões ocupam a tela toda
    st.write(f"Palco ativo em: **{big_page_atual.upper()}**")

if __name__ == "__main__":
    main()
