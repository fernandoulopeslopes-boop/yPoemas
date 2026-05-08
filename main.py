import streamlit as st

# 1. CONFIGURAÇÃO INICIAL (Obrigatório ser a primeira chamada)
st.set_page_config(page_title="yPoemas - A Machina", layout="wide")

# 2. PROTOCOLO DE ESTILO (PTC - Correção de Interação)
st.markdown(
    """
    <style>
        /* Ajuste do Palco: Largura de 90% e liberação de cliques */
        .block-container {
            max-width: 90% !important;
            margin-left: auto;
            margin-right: auto;
            padding-top: 2rem;
            /* Garante que a área receba eventos de mouse */
            pointer-events: auto !important; 
        }

        /* Sidebar: Prioridade de visualização e clique */
        section[data-testid="stSidebar"] {
            z-index: 10000 !important;
        }

        /* Estilização básica para verificar se o palco está vivo */
        .palco-moldura {
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 10px;
            background-color: #f9f9f9;
        }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    # --- SIDEBAR: LISTA OFICIAL CPC ---
    st.sidebar.title("Configurações")
    languages = ["Português", "Español", "Italiano", "Français", "English", "Català"]
    sel_lang = st.sidebar.selectbox("Idioma de Destino", languages)
    
    st.sidebar.divider()
    st.sidebar.write("Machina de Fazer Poesia - 2026")

    # --- O PALCO (ÁREA PRINCIPAL) ---
    st.title("yPoemas")
    
    # Usando uma div com classe para testar a interatividade
    st.markdown(f"""
        <div class="palco-moldura">
            <h3>Palco Ativo: {sel_lang}</h3>
            <p>Se você consegue selecionar este texto, o mouse não está mais congelado.</p>
        </div>
    """, unsafe_allow_html=True)

    # Espaço para o motor da Machina
    if st.button("Precipitar o Acaso"):
        st.balloons()
        st.success(f"Gerando variações em {sel_lang}...")

if __name__ == "__main__":
    main()
