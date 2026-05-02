import streamlit as st
import os

# --- 0. MOTORES DA MACHINA (SUPORTE) ---
def load_md_file(filename):
    """Busca o arquivo no diretório com lógica case-insensitive."""
    folder = "md_files"
    search_name = filename if filename.upper().endswith(".MD") else f"{filename}.MD"
    if os.path.exists(folder):
        for arq in os.listdir(folder):
            if arq.upper() == search_name.upper():
                with open(os.path.join(folder, arq), "r", encoding="utf-8") as f:
                    return f.read()
    return f"<!-- {search_name} não encontrado -->"

def set_full_width():
    """Injeta CSS para expansão total do palco principal."""
    st.markdown(
        """
        <style>
        [data-testid="stMainInternal"] {
            max-width: 98% !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        .stExpander { border: none !important; box-shadow: none !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 1. BOOTSTRAP (FIX: INICIALIZAÇÃO PRECOCE) ---
# Definido no topo para evitar AttributeError[cite: 1]
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = "sobre"
if 'sub_sobre' not in st.session_state:
    st.session_state.sub_sobre = "ypoemas"
if 'tema' not in st.session_state:
    st.session_state.tema = "default"

# Configuração de layout dinâmica
sb_state = "collapsed" if st.session_state.pagina_ativa == "sobre" else "expanded"
st.set_page_config(layout="wide", initial_sidebar_state=sb_state)

# --- 2. O FAROL (SOBRE) ---
def page_sobre():
    set_full_width()
    sobre_list = ["comments", "prefácio", "machina", "off-machina", "notes", "license"]
    
    _, col_menu, _ = st.columns([1, 2, 1])
    with col_menu:
        try:
            curr_idx = sobre_list.index(st.session_state.sub_sobre.lower())
        except ValueError:
            curr_idx = 0
        choice = st.selectbox("↓ SOBRE", sobre_list, index=curr_idx).upper()
        st.session_state.sub_sobre = choice.lower()

    st.divider()

    # PALCO EXPANDIDO: Uso total da área da tela[cite: 1]
    with st.container():
        with st.expander("", expanded=True):
            if choice == "MACHINA":
                st.markdown(load_md_file("ABOUT_MACHINA_A.MD"))
                
                # Bloco Visual Matrix
                img_matrix = f"./images/matrix/{st.session_state.tema.upper()}.JPG"
                st.divider()
                if os.path.exists(img_matrix):
                    st.image(img_matrix, use_container_width=True)
                st.markdown(f"### METADADOS DA MATRIX: {st.session_state.tema.upper()}")
                st.divider()
                
                st.markdown(load_md_file("ABOUT_MACHINA_D.MD"))
            else:
                # Tratamento para nomes como OFF_MACHINA
                file_name = choice.replace("-", "_")
                st.markdown(load_md_file(f"ABOUT_{file_name}.MD"))

# --- 3. EXECUÇÃO ---
if __name__ == "__main__":
    if st.session_state.pagina_ativa == "sobre":
        page_sobre()
    else:
        # Espaço reservado para o palco principal da Machina
        st.write("Retorne ao Farol (Sobre) para documentação expandida.")
