import streamlit as st
from PIL import Image
import os

# Configuração Inicial da Página
st.set_page_config(page_title="yPoemas - A Machina", layout="wide")

# PROTOCOLO DE ESTILO (PTC - Camadas e Interface)
st.markdown(
    """
    <style>
        /* 1. O PALCO: Centralização e Largura de 90% */
        .block-container {
            max-width: 90% !important;
            margin-left: auto;
            margin-right: auto;
            padding-top: 1rem;
            z-index: 1;
        }

        /* 2. A SIDEBAR: Recuperação de autoridade para o Mouse */
        section[data-testid="stSidebar"] {
            z-index: 10000 !important;
        }

        /* 3. O HEADER: Liberação dos menus superiores */
        header[data-testid="stHeader"] {
            z-index: 9999 !important;
            background: transparent;
        }

        /* Ajuste fino dos ícones na sidebar (20x20) */
        .sidebar-icon {
            width: 20px;
            height: 20px;
            vertical-align: middle;
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
    
    # Placeholder para a Arte (Exemplo de carregamento da pasta \ypo)
    # Aqui o código busca as matrizes no C:\ypo\artes conforme a estrutura
    st.write(f"### Palco Ativo: {sel_lang}")
    
    c1, c2, c3 = st.columns([1, 10, 1])
    with c2:
        st.info("Aguardando precipitação do acaso...")
        # Espaço reservado para o output das quindecilhões de variações
        
if __name__ == "__main__":
    main()
