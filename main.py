import streamlit as st
import os

# --- IMPORTAÇÃO DO MOTOR ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    st.error("Erro: Arquivo 'lay_2_ypo.py' não encontrado.")
except SyntaxError as e:
    st.error(f"Erro de Sintaxe no motor: {e}")

# =================================================================
# ⚙️ CONFIGURAÇÕES & ESTILO
# =================================================================

st.set_page_config(
    page_title="a Máquina de Fazer Poesia",
    page_icon="ツ",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Cache moderno para arquivos auxiliares
@st.cache_data(show_spinner=False)
def load_info(file_name):
    path = os.path.join("./base", file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# CSS para manter o esmero visual
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
    
    # Menu Nativo (Substituindo o TabBar problemático)
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
    
    # Botões de Ação solicitados
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.sidebar.button("Talk"):
            st.session_state.action = "talk"
    with col2:
        if st.sidebar.button("Arte"):
            st.session_state.action = "draw"

    # Exibição automática de informações do tema na Sidebar
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
    
    if st.button(f"Gerar {tema_selecionado}"):
        with st.spinner("Semeando versos..."):
            # Adicionado tratamento para o motor
            try:
                poema = gera_poema(tema_selecionado)
                if poema:
                    st.markdown("---")
                    for linha in poema:
                        st.write(linha)
                    st.markdown("---")
            except Exception as e:
                st.error(f"Erro na geração: {e}")

if __name__ == "__main__":
    main()
