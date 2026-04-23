import streamlit as st
import os

# --- Configurações de UI ---
st.set_page_config(layout="wide", page_title="Machina de Fazer Poesia")

# CSS Fixo: Sidebar 300px e arredondamento de artes
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] { width: 300px; max-width: 300px; }
        .stImage img { border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

def main():
    # --- Sidebar (O Cockpit de Navegação) ---
    with st.sidebar:
        st.title("a Máquina")
        
        # Aqui você mantém apenas o que já funcionava:
        # Seleção de Temas, Idiomas e Filtros.
        st.write("Navegação Poética")
        
        st.divider()
        # O Módulo Admin 'go' fica aqui apenas como placeholder, 
        # sem disparar os builds pesados que travam o boot.
        with st.expander(" ", expanded=False):
            st.write("Engenharia em pausa.")

    # --- Área Principal (Onde a Poesia acontece) ---
    # Aqui entra o seu código original de exibição:
    # 1. Carregamento do Poema via lay_2_ypo
    # 2. Exibição das artes da pasta /images/matrix/
    st.markdown("### Bem-vindo à Cobertura")
    st.info("A Machina está operando em modo de estabilidade.")

if __name__ == "__main__":
    main()
