import streamlit as st
import os

# --- MOTOR DE BUSCA DE ARQUIVOS (Blindagem v.33.9) ---

def load_md_file(file_name):
    """
    Busca absoluta na pasta /md_files. 
    Lógica: Raiz do Projeto -> md_files -> ARQUIVO.MD
    """
    # Define o caminho absoluto para evitar erros de servidor Linux
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, "md_files", file_name)
    
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # Se falhar, o erro imprimirá o caminho exato que o sistema tentou ler
        return f"⚠️ ERRO DE PATH: {file_name} não encontrado em {full_path}"

# --- COMPONENTE DE INTERFACE ---

def write_ypoema(texto, imagem):
    """Layout Lateralidade: Texto(2) | Imagem(1)"""
    col_txt, col_img = st.columns([2, 1])
    with col_txt:
        st.markdown(texto)
    with col_img:
        st.image(imagem, use_container_width=True)

# --- PÁGINA SOBRE (ABOUT) ---

def page_abouts():
    # Lista com grafia exata para o .upper()
    abouts_list = [
        "comments", "prefácio", "machina", "off-machina", 
        "outros", "traduttore", "bibliografia", "imagens", 
        "samizdát", "notes", "license", "index"
    ]

    # Label do Seletor
    sobrios = "↓  SOBRE" 
    options = list(range(len(abouts_list)))
    
    opt_abouts = st.selectbox(
        sobrios,
        options,
        format_func=lambda x: abouts_list[x],
        key="opt_abouts",
    )

    # Batismo funcional: lnew foi substituído
    permitir_exibicao_texto = True 

    if st.session_state.get('vydo', False):
        permitir_exibicao_texto = False 
        # show_video("about")
        st.session_state.vydo = False

    if permitir_exibicao_texto:
        # Construção da query de busca
        nome_upper = abouts_list[opt_abouts].upper()
        arquivo_alvo = f"ABOUT_{nome_upper}.MD"
        
        with st.expander("", expanded=True):
            if nome_upper == "MACHINA":
                # Renderização da Página Coração
                st.markdown(load_md_file("ABOUT_MACHINA_A.MD"))
                
                # Interface Viva (Matriz)
                tema_ativo = st.session_state.get('tema', 'default')
                path_imagem = f"./images/matrix/{tema_ativo}.jpg"
                # write_ypoema(load_info(tema_ativo), path_imagem)
                
                st.markdown(load_md_file("ABOUT_MACHINA_D.MD"))
            else:
                # Renderização das demais páginas .MD
                st.markdown(load_md_file(arquivo_alvo))

# --- MOTOR PRINCIPAL ---

def main():
    st.set_page_config(layout="wide", page_title="Machina v.33.9")

    # Inicialização de Session State
    if 'tema' not in st.session_state:
        st.session_state.tema = "default"
    if 'vydo' not in st.session_state:
        st.session_state.vydo = False

    # Execução do módulo ABOUT
    page_abouts()

if __name__ == "__main__":
    main()
