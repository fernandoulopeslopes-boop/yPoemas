import streamlit as st
import os

# --- MOTOR DE BUSCA (Blindagem v.33.9 - Solução Definitiva) ---

def load_md_file(file_name):
    """
    Busca absoluta usando caminhos brutos (raw strings) para evitar
    erros de escape como '\m'.
    """
    # Caminho no Servidor (Linux)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Usamos o join para o Python decidir a barra correta (/ ou \)
    path_cloud = os.path.join(base_dir, "md_files", file_name)
    
    # Caminho no seu ambiente local (Windows) - Usando Raw String r""
    path_local = r"C:\ypo\md_files\\" + file_name
    
    # Prioridade de busca
    if os.path.exists(path_local):
        target = path_local
    else:
        target = path_cloud
    
    try:
        with open(target, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # Se falhar, o erro mostra exatamente o que o Python tentou ler
        return f"⚠️ ERRO: {file_name} não encontrado em {target}"

# --- COMPONENTE DE INTERFACE ---

def write_ypoema(texto, imagem):
    col_txt, col_img = st.columns([2, 1])
    with col_txt:
        st.markdown(texto)
    with col_img:
        st.image(imagem, use_container_width=True)

# --- PÁGINA SOBRE (ABOUT) ---

def page_abouts():
    abouts_list = [
        "comments", "prefácio", "machina", "off-machina", 
        "outros", "traduttore", "bibliografia", "imagens", 
        "samizdát", "notes", "license", "index"
    ]

    sobrios = "↓  SOBRE" 
    options = list(range(len(abouts_list)))
    
    opt_abouts = st.selectbox(
        sobrios,
        options,
        format_func=lambda x: abouts_list[x],
        key="opt_abouts",
    )

    # Batismo funcional (antigo lNew)
    permitir_exibicao_texto = True 

    if st.session_state.get('vydo', False):
        permitir_exibicao_texto = False 
        st.session_state.vydo = False

    if permitir_exibicao_texto:
        nome_upper = abouts_list[opt_abouts].upper()
        arquivo_alvo = f"ABOUT_{nome_upper}.MD"
        
        with st.expander("", expanded=True):
            if nome_upper == "MACHINA":
                st.markdown(load_md_file("ABOUT_MACHINA_A.MD"))
                
                # Interface Viva
                tema_ativo = st.session_state.get('tema', 'default')
                # LOGO_IMAGE será buscada na pasta de imagens do projeto
                path_imagem = f"./images/matrix/{tema_ativo}.jpg"
                
                st.markdown(load_md_file("ABOUT_MACHINA_D.MD"))
            else:
                st.markdown(load_md_file(arquivo_alvo))

# --- MOTOR PRINCIPAL ---

def main():
    st.set_page_config(layout="wide")

    if 'tema' not in st.session_state:
        st.session_state.tema = "default"
    if 'vydo' not in st.session_state:
        st.session_state.vydo = False

    page_abouts()

if __name__ == "__main__":
    main()
