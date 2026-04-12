import streamlit as st
import os

# --- MOTOR DE BUSCA (v.33.9 - ANTI-RESÍDUO & CASE INSENSITIVE) ---

def load_md_file(file_name):
    """
    Localiza e lê arquivos na pasta md_files.
    Suporta .md ou .MD e ambientes Local/Cloud.
    """
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
            return f"⚠️ Erro de leitura: {str(e)}"
            
    return f"⚠️ {target_upper} não localizado."

# --- COMPONENTES DE INTERFACE ---

def write_ypoema(texto, imagem):
    """Renderiza a estrutura clássica da Machina: Texto | Imagem"""
    col_txt, col_img = st.columns([2, 1])
    with col_txt:
        st.markdown(texto)
    with col_img:
        if os.path.exists(imagem):
            st.image(imagem, use_container_width=True)

# --- PÁGINA SOBRE (ABOUT) ---

def page_abouts():
    """Navegação da Documentação com Limpeza Síncrona"""
    
    # SEQUÊNCIA ORIGINAL MANTIDA
    abouts_list = [
        "prefácio", "machina", "off-machina", "outros", 
        "traduttore", "bibliografia", "imagens", "samizdát", 
        "comments", "notes", "license", "index"
    ]

    sobrios = "↓  SOBRE" 
    
    # Seletor Principal
    opt_abouts = st.selectbox(
        sobrios,
        abouts_list,
        index=0,
        key="opt_abouts",
    )

    # --- CONTAINER ANTI-RESÍDUO ---
    placeholder = st.empty()

    permitir_exibicao_texto = True 

    if st.session_state.get('vydo', False):
        permitir_exibicao_texto = False 
        st.session_state.vydo = False

    if permitir_exibicao_texto:
        nome_base = opt_abouts.upper()
        
        with placeholder.container():
            with st.expander("", expanded=True):
                if nome_base == "MACHINA":
                    st.markdown(load_md_file("ABOUT_MACHINA_A.MD"))
                    
                    tema_atual = st.session_state.get('tema', 'default')
                    path_img = f"./images/matrix/{tema_atual}.jpg"
                    
                    st.markdown(load_md_file("ABOUT_MACHINA_D.MD"))
                else:
                    arquivo_alvo = f"ABOUT_{nome_base}.MD"
                    st.markdown(load_md_file(arquivo_alvo))

# --- MOTOR PRINCIPAL ---

def main():
    st.set_page_config(
        page_title="yPoemas - A Máquina de Fazer Poesia",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inicialização de Estados (Consolidado)
    if 'tema' not in st.session_state:
        st.session_state.tema = "default"
    if 'vydo' not in st.session_state:
        st.session_state.vydo = False
    if 'lang' not in st.session_state:
        st.session_state.lang = "PT"

    # Sidebar Estrutural
    with st.sidebar:
        st.title("yPoemas")
        st.write("v.33.9")
        st.divider()

    # Início da Execução
    page_abouts()

if __name__ == "__main__":
    main()
