import streamlit as st
import os

# --- 0. MOTORES DA MACHINA (SUPORTE) ---
def load_md_file(filename):
    folder = "md_files"
    search_name = filename if filename.upper().endswith(".MD") else f"{filename}.MD"
    if os.path.exists(folder):
        for arq in os.listdir(folder):
            if arq.upper() == search_name.upper():
                with open(os.path.join(folder, arq), "r", encoding="utf-8") as f:
                    return f.read()
    return f"<!-- {search_name} não encontrado -->"

def set_full_width():
    """Injeta CSS para expandir o palco principal da Machina."""
    st.markdown(
        """
        <style>
        /* Remove o limite de largura do container interno do Streamlit */
        [data-testid="stMainInternal"] {
            max-width: 98% !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        /* Ajusta o expander para não ter margens laterais excessivas */
        .stExpander {
            border: none !important;
            box-shadow: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. O FAROL (SOBRE) - PALCO EXPANDIDO ---
def page_sobre():
    # Ativa a largura total para a documentação
    set_full_width()
    
    sobre_list = ["comments", "prefácio", "machina", "off-machina", "outros", "traduttore", "notes", "license"]
    
    # Menu centralizado apenas para navegação
    _, col_menu, _ = st.columns([1, 2, 1])
    with col_menu:
        try:
            curr_idx = sobre_list.index(st.session_state.sub_sobre.lower())
        except ValueError:
            curr_idx = 0
        choice = st.selectbox("↓ SOBRE", sobre_list, index=curr_idx).upper()
        st.session_state.sub_sobre = choice.lower()

    st.divider()

    # ÁREA DE EXPOSIÇÃO (Sem colunas de respiro laterais)
    container_md = st.container()
    with container_md:
        with st.expander("", expanded=True):
            if choice == "MACHINA":
                # Carregamento sequencial dos metadados e arquivos A/D
                st.markdown(load_md_file("ABOUT_MACHINA_A.MD"))
                
                # Bloco visual da Matrix
                img_path = f"./images/matrix/{st.session_state.tema.upper()}.JPG"
                st.divider()
                if os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
                st.markdown(f"### METADADOS DA MATRIX: {st.session_state.tema.upper()}")
                st.divider()
                
                st.markdown(load_md_file("ABOUT_MACHINA_D.MD"))
                
            elif choice == "OFF-MACHINA":
                st.markdown(load_md_file("ABOUT_OFF_MACHINA.MD"))
                
            else:
                # Fallback para os demais arquivos (COMMENTS, NOTES, etc.)
                st.markdown(load_md_file(f"ABOUT_{choice}.MD"))

# --- 4. EXECUÇÃO ---
if __name__ == "__main__":
    # Sidebar renderizada normalmente (se necessário)
    # render_sidebar() 
    
    if st.session_state.pagina_ativa == "sobre":
        page_sobre()
    else:
        # Se for para outra página, o Streamlit resetará o CSS no próximo rerun
        # ou você pode injetar um CSS de 'reset' aqui.
        pass
