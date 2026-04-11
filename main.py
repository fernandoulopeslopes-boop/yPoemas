import streamlit as st
import os

# Importação direta e obrigatória
from lay_2_ypo import gera_poema

# =================================================================
# ⚙️ CONFIGURAÇÕES & ESTILO
# =================================================================

st.set_page_config(
    page_title="a Máquina de Fazer Poesia",
    page_icon="ツ",
    layout="centered",
    initial_sidebar_state="expanded",
)

@st.cache_data(show_spinner=False)
def load_info(file_name):
    path = os.path.join("./base", file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

st.markdown("""
    <style>
    [data-testid="stSidebar"] { width: 310px; }
    .main .block-container { padding-top: 1.5rem; }
    div.stButton > button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 🧭 NAVEGAÇÃO & SIDEBAR
# =================================================================

def main():
    st.sidebar.title("ツ Machina")
    
    menu = {
        "1": "Mini",
        "2": "yPoemas",
        "3": "Eureka",
        "4": "Off-Machina",
        "5": "Books",
        "6": "Poly",
        "7": "About"
    }
    
    chosen_id = st.sidebar.radio(
        "Navegação", 
        options=list(menu.keys()), 
        format_func=lambda x: menu[x].upper(),
        index=1
    )

    st.sidebar.markdown("---")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.sidebar.button("Talk"):
            st.session_state.action = "talk"
    with col2:
        if st.sidebar.button("Arte"):
            st.session_state.action = "draw"

    # Carregamento de infos da pasta /base
    info_files = {
        "1": "INFO_MINI.md", "2": "INFO_YPOEMAS.md", "3": "INFO_EUREKA.md",
        "4": "INFO_OFF-MACHINA.md", "5": "INFO_BOOKS.md", "6": "INFO_POLY.md",
        "7": "INFO_ABOUT.md"
    }
    
    info_content = load_info(info_files.get(chosen_id, ""))
    if info_content:
        st.sidebar.info(info_content)

    # --- RENDERIZAÇÃO PRINCIPAL ---
    tema_selecionado = menu[chosen_id]
    st.title(f"Modo: {tema_selecionado}")
    
    # Parâmetro Eureka
    seed_eureka = ""
    if tema_selecionado == "Eureka":
        seed_eureka = st.text_input("Semente ➪ Coords:", value="")
    
    if st.button(f"Gerar {tema_selecionado}"):
        with st.spinner("Semeando versos..."):
            try:
                # Chamada com os 2 parâmetros conforme exigido pelo motor
                resultado = gera_poema(tema_selecionado, seed_eureka)
                
                if resultado:
                    st.markdown("---")
                    if isinstance(resultado, list):
                        for linha in resultado:
                            st.write(linha)
                    else:
                        st.write(resultado)
                    st.markdown("---")
            except Exception as e:
                st.error(f"Erro na execução do motor: {e}")

if __name__ == "__main__":
    main()
