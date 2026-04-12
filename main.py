import streamlit as st
import os

# --- MOTOR DE BUSCA (v.33.9 - SEGURO & MULTI-AMBIENTE) ---

def load_md_file(file_name):
    """
    Localiza e lê arquivos .md ou .MD na pasta md_files.
    Compatível com ambiente local (C:\\ypo) e Streamlit Cloud.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define a pasta alvo baseada no ambiente
    if os.path.exists(r"C:\ypo"):
        folder = r"C:\ypo\md_files"
    else:
        folder = os.path.join(base_dir, "md_files")

    # Busca ignorando maiúsculas/minúsculas na extensão
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
            
    return f"⚠️ ERRO: {target_upper} não encontrado em {folder}"

# --- COMPONENTES DE INTERFACE ---

def write_ypoema(texto, imagem):
    """Exibe texto e imagem lado a lado (Proporção 2:1)"""
    col_txt, col_img = st.columns([2, 1])
    with col_txt:
        st.markdown(texto)
    with col_img:
        st.image(imagem, use_container_width=True)

# --- PÁGINA SOBRE (ABOUT) ---

def page_abouts():
    """Gerencia a navegação das páginas de documentação"""
    abouts_list = [
        "comments", "prefácio", "machina", "off-machina", 
        "outros", "traduttore", "bibliografia", "imagens", 
        "samizdát", "notes", "license", "index"
    ]

    sobrios = "↓  SOBRE" 
    options = list(range(len(abouts_list)))
    
    # Seletor central de sub-páginas
    opt_abouts = st.selectbox(
        sobrios,
        options,
        format_func=lambda x: abouts_list[x],
        key="opt_abouts",
    )

    permitir_exibicao_texto = True 

    # Lógica para ocultar texto se houver vídeo (vydo) ativo
    if st.session_state.get('vydo', False):
        permitir_exibicao_texto = False 
        st.session_state.vydo = False

    if permitir_exibicao_texto:
        nome_base = abouts_list[opt_abouts].upper()
        arquivo_alvo = f"ABOUT_{nome_base}.MD"
        
        with st.expander("", expanded=True):
            if nome_base == "MACHINA":
                # Layout especial para a página principal da Machina
                st.markdown(load_md_file("ABOUT_MACHINA_A.MD"))
                
                tema_atual = st.session_state.get('tema', 'default')
                path_img = f"./images/matrix/{tema_atual}.jpg"
                # Se houver função de carregamento de info, inserir aqui:
                # write_ypoema(load_info(tema_atual), path_img)
                
                st.markdown(load_md_file("ABOUT_MACHINA_D.MD"))
            else:
                # Carregamento genérico para as demais seções
                conteudo = load_md_file(arquivo_alvo)
                st.markdown(conteudo)

# --- MOTOR PRINCIPAL ---

def main():
    st.set_page_config(layout="wide", page_title="A Máquina de Fazer Poesia")

    # Inicialização de variáveis de estado
    if 'tema' not in st.session_state:
        st.session_state.tema = "default"
    if 'vydo' not in st.session_state:
        st.session_state.vydo = False

    # Renderiza a seção About
    page_abouts()

if __name__ == "__main__":
    main()
