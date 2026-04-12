import streamlit as st
import os

# --- MOTOR DE BUSCA (v.33.9 - CASE INSENSITIVE & MULTI-AMBIENTE) ---

def load_md_file(file_name):
    """
    Motor v.33.9 - Busca Inteligente.
    Localiza arquivos em md_files independente de extensão .md ou .MD.
    Compatível com C:\ypo\md_files e Streamlit Cloud.
    """
    # 1. Âncora de Diretório (Cloud)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Definição da Pasta Alvo (Local vs Cloud)
    if os.path.exists(r"C:\ypo"):
        folder = r"C:\ypo\md_files"
    else:
        folder = os.path.join(base_dir, "md_files")

    # 3. Busca por Match de Nome (Ignorando Case da Extensão)
    target_upper = file_name.upper()
    
    if os.path.exists(folder):
        try:
            arquivos_reais = os.listdir(folder)
            for arquivo in arquivos_reais:
                if arquivo.upper() == target_upper:
                    # Se houver match (ex: 'ABOUT_COMMENTS.md' == 'ABOUT_COMMENTS.MD')
                    with open(os.path.join(folder, arquivo), "r", encoding="utf-8") as f:
                        return f.read()
        except Exception as e:
            return f"⚠️ Erro ao acessar pasta: {str(e)}"
            
    return f"⚠️ ERRO: {target_upper} não encontrado em {folder}"

# --- COMPONENTES DE INTERFACE ---

def write_ypoema(texto, imagem):
    """Layout Lateralidade: Texto (2/3) | Imagem (1/3)"""
    col_txt, col_img = st.columns([2, 1])
    with col_txt:
        st.markdown(texto)
    with col_img:
        st.image(imagem, use_container_width=True)

# --- PÁGINA SOBRE (ABOUT) ---

def page_abouts():
    """Lógica de Engenharia Reversa para Documentação da Machina"""
    abouts_list = [
        "comments", "prefácio", "machina", "off-machina", 
        "outros", "traduttore", "bibliografia", "imagens", 
        "samizdát", "notes", "license", "index"
    ]

    # Interface Visual do Seletor
    sobrios = "↓  SOBRE" 
    options = list(range(len(abouts_list)))
    
    opt_abouts = st.selectbox(
        sobrios,
        options,
        format_func=lambda x: abouts_list[x],
        key="opt_abouts",
    )

    # Batismo Funcional: lnew -> permitir_exibicao_texto
    permitir_exibicao_texto = True 

    if st.session_state.get('vydo', False):
        permitir_exibicao_texto = False 
        # Aqui entra sua função de vídeo: show_video("about")
        st.session_state.vydo = False

    if permitir_exibicao_texto:
        # Prepara a query de busca padrão UPPER
        nome_base = abouts_list[opt_abouts].upper()
        arquivo_alvo = f"ABOUT_{nome_base}.MD"
        
        with st.expander("", expanded=True):
            if nome_base == "MACHINA":
                # Renderização da Página Coração
                st.markdown(load_md_file("ABOUT_MACHINA_A.MD"))
                
                # Interface Viva (Dados da Matriz)
                tema_atual = st.session_state.get('tema', 'default')
                path_img = f"./images/matrix/{tema_atual}.jpg"
                
                # write_ypoema(load_info(tema_atual), path_img)
                
                st.markdown(load_md_file("ABOUT_MACHINA_D.MD"))
            else:
                # Renderização das demais páginas .MD
                st.markdown(load_md_file(arquivo_alvo))

# --- MOTOR PRINCIPAL ---

def main():
    st.set_page_config(layout="wide", page_title="A Máquina de Fazer Poesia")

    # Inicialização de Estados Necessários
    if 'tema' not in st.session_state:
        st.session_state.tema = "default"
    if 'vydo' not in st.session_state:
        st.session_state.vydo = False

    # Execução do Módulo Central
    page_abouts()

if __name__ == "__main__":
    main()
