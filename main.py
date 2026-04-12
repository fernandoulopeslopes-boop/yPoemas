import streamlit as st
import os

# --- MOTOR DE BUSCA (v.33.9 - CASE INSENSITIVE) ---

def load_md_file(file_name):
    """Localiza arquivos em md_files independente de extensão .md ou .MD."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(r"C:\ypo"):
        folder = r"C:\ypo\md_files"
    else:
        folder = os.path.join(base_dir, "md_files")

    target_upper = file_name.upper()
    if os.path.exists(folder):
        try:
            arquivos_reais = os.listdir(folder)
            for arquivo in arquivos_reais:
                if arquivo.upper() == target_upper:
                    with open(os.path.join(folder, arquivo), "r", encoding="utf-8") as f:
                        return f.read()
        except Exception as e:
            return f"⚠️ Erro ao acessar pasta: {str(e)}"
    return f"⚠️ ERRO: {target_upper} não encontrado."

# --- PÁGINA SOBRE (ABOUT) ---

def page_abouts():
    # Lista de páginas (Removi o 'index' da lista interna para usá-lo como padrão)
    abouts_list = [
        "INÍCIO", "comments", "prefácio", "machina", "off-machina", 
        "outros", "traduttore", "bibliografia", "imagens", 
        "samizdát", "notes", "license"
    ]

    sobrios = "↓  SOBRE" 
    
    # Seletor de sub-páginas
    opt_abouts = st.selectbox(
        sobrios,
        abouts_list,
        index=0, # Garante que comece no "INÍCIO"
        key="opt_abouts",
    )

    permitir_exibicao_texto = True 
    if st.session_state.get('vydo', False):
        permitir_exibicao_texto = False 
        st.session_state.vydo = False

    if permitir_exibicao_texto:
        nome_base = opt_abouts.upper()
        
        with st.expander("", expanded=True):
            if nome_base == "INÍCIO":
                # Carrega o índice geral ou introdução
                st.markdown(load_md_file("ABOUT_INDEX.MD"))
            
            elif nome_base == "MACHINA":
                st.markdown(load_md_file("ABOUT_MACHINA_A.MD"))
                # Espaço para imagem da matriz
                st.markdown(load_md_file("ABOUT_MACHINA_D.MD"))
            
            else:
                # Carrega a página selecionada (comments, prefácio, etc)
                arquivo_alvo = f"ABOUT_{nome_base}.MD"
                st.markdown(load_md_file(arquivo_alvo))

# --- MOTOR PRINCIPAL ---

def main():
    st.set_page_config(layout="wide", page_title="A Máquina de Fazer Poesia")

    if 'tema' not in st.session_state:
        st.session_state.tema = "default"
    if 'vydo' not in st.session_state:
        st.session_state.vydo = False

    page_abouts()

if __name__ == "__main__":
    main()
