import streamlit as st
import os

# --- MOTOR DE BUSCA (v.33.9 - SOLUÇÃO FINAL DE SINTAXE) ---

def load_md_file(file_name):
    """
    Motor de busca que resolve o conflito Windows/Linux e o erro de parêntese.
    """
    # 1. Âncora de Diretório (Cloud)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_cloud = os.path.join(base_dir, "md_files", file_name)
    
    # 2. Âncora Local (Windows) com Raw String fechada corretamente
    path_local_folder = r"C:\ypo\md_files"
    
    # 3. Lógica de Seleção de Alvo (Segura contra SyntaxError)
    if os.path.exists(path_local_folder):
        target = os.path.join(path_local_folder, file_name)
    else:
        target = path_cloud
    
    # 4. TENTATIVA DE LEITURA
    if os.path.exists(target):
        try:
            with open(target, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"⚠️ Erro ao abrir: {str(e)}"
    
    # 5. DIAGNÓSTICO (Caso o arquivo não exista no alvo)
    try:
        itens_raiz = os.listdir(base_dir)
        debug_msg = f"⚠️ ARQUIVO NÃO ENCONTRADO: {file_name}\n\n"
        debug_msg += f"Procurado em: {target}\n"
        if "md_files" in itens_raiz:
            pasta_real = os.path.join(base_dir, "md_files")
            debug_msg += f"Conteúdo da /md_files: {os.listdir(pasta_real)}"
        else:
            debug_msg += f"Estrutura na Raiz: {itens_raiz}"
        return debug_msg
    except:
        return f"⚠️ {file_name} inacessível."

# --- COMPONENTES DE INTERFACE ---

def write_ypoema(texto, imagem):
    """Lateralidade: Texto (2/3) | Imagem (1/3)"""
    col_txt, col_img = st.columns([2, 1])
    with col_txt:
        st.markdown(texto)
    with col_img:
        st.image(imagem, use_container_width=True)

# --- PÁGINA SOBRE (ABOUT) ---

def page_abouts():
    """Lógica de Engenharia Reversa para Documentação"""
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
                
                # Interface Viva (Matriz)
                tema = st.session_state.get('tema', 'default')
                path_img = f"./images/matrix/{tema}.jpg"
                
                # st.markdown("Carregando Matriz...") # Placeholder
                
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
