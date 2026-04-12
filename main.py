import streamlit as st
import os

# --- FUNÇÕES DE SUPORTE (O Motor) ---

def load_md_file(file_name):
    """Carregador Universal: Busca na pasta \md_files"""
    base_path = "./md_files/"
    full_path = os.path.join(base_path, file_name)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"⚠️ Arquivo {file_name} não encontrado."

def write_ypoema(texto, imagem):
    """Renderiza a Matriz respeitando a lateralidade da v.33.9"""
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(texto)
    with col2:
        st.image(imagem, use_container_width=True)

# --- PÁGINAS DE CONTEÚDO ---

def page_abouts():
    """Interface de Suporte: Engenharia Reversa (Finais -> Iniciais)"""
    abouts_list = [
        "comments", "prefácio", "machina", "off-machina", 
        "outros", "traduttore", "bibliografia", "imagens", 
        "samizdát", "notes", "license", "index"
    ]

    options = list(range(len(abouts_list)))
    sobrios = "↓  " + "SOBRE" # Aqui entraria sua função translate("sobre")
    
    opt_abouts = st.selectbox(
        sobrios,
        options,
        format_func=lambda x: abouts_list[x],
        key="opt_abouts",
    )

    # BATISMO FUNCIONAL
    permitir_exibicao_texto = True 

    if st.session_state.get('vydo', False):
        permitir_exibicao_texto = False 
        # show_video("about") -> Chamar sua função de vídeo aqui
        st.session_state.vydo = False

    if permitir_exibicao_texto:
        nome_arquivo = abouts_list[opt_abouts].upper()
        with st.expander("", expanded=True):
            if nome_arquivo == "MACHINA":
                st.markdown(load_md_file("ABOUT_MACHINA_A.MD"))
                
                # Dados da Matriz Viva
                tema = st.session_state.get('tema', 'default')
                # LOGO_TEXTO = load_info(tema) -> Chamar sua função load_info aqui
                LOGO_IMAGE = f"./images/matrix/{tema}.jpg"
                
                # write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
                
                st.markdown(load_md_file("ABOUT_MACHINA_D.MD"))
            else:
                st.markdown(load_md_file(f"ABOUT_{nome_arquivo}.MD"))

# --- MOTOR PRINCIPAL ---

def main():
    st.set_page_config(layout="wide", page_title="Machina de Fazer Poesia v.33.9")

    # Inicialização de Estados
    if 'tema' not in st.session_state:
        st.session_state.tema = "default"
    if 'vydo' not in st.session_state:
        st.session_state.vydo = False

    # Sidebar / Navegação
    with st.sidebar:
        st.title("A MÁCHINA")
        # Aqui entram seus seletores de língua e navegação principal
    
    # Execução da página selecionada (Exemplo: About)
    page_abouts()

if __name__ == "__main__":
    main()
