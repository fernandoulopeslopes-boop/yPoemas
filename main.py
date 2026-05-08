import streamlit as st

# 1. CONFIGURAÇÃO INICIAL (NOME DEFINITIVO)
st.set_page_config(
    page_title="yPoemas - a Machina de fazer Poesia", 
    layout="wide"
)

# 2. PROTOCOLO DE ESTILO (PTC - RESET DE INTERAÇÃO)
st.markdown(
    """
    <style>
        /* Reset de cliques para evitar o congelamento */
        html, body, [data-testid="stAppViewContainer"] {
            pointer-events: auto !important;
        }

        /* O PALCO: Largura de 90% sem bloquear o mouse */
        .block-container {
            max-width: 90% !important;
            margin-left: auto;
            margin-right: auto;
            padding-top: 2rem;
            z-index: 1;
        }

        /* SIDEBAR: Garantia de acesso total */
        section[data-testid="stSidebar"] {
            z-index: 10000 !important;
            pointer-events: auto !important;
        }

        /* HEADER */
        header[data-testid="stHeader"] {
            z-index: 9999 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    # --- SIDEBAR: LISTA OFICIAL CONFORME O CPC ---
    st.sidebar.title("Configurações")
    
    # LISTA OFICIAL ESTABELECIDA
    languages = ["Português", "Español", "Italiano", "Français", "English", "Català"]
    
    sel_lang = st.sidebar.selectbox("Idioma", languages)
    
    st.sidebar.divider()
    st.sidebar.write("2026 - a Machina de fazer Poesia")

    # --- O PALCO (ÁREA PRINCIPAL) ---
    st.title("yPoemas - a Machina de fazer Poesia")
    
    st.info(f"Idioma selecionado: {sel_lang}")
    
    # Teste de área clicável
    if st.button("Testar Mouse (Clique Aqui)"):
        st.success("O mouse está operacional no palco!")

if __name__ == "__main__":
    main()
