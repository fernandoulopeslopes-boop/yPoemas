import streamlit as st
import os

# --- MOTOR DE BUSCA (v.33.9 - CASE INSENSITIVE) ---

def load_md_file(file_name):
    """Localiza arquivos em md_files independente de extensão .md ou .MD."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Verifica ambiente: Local (C:\ypo) vs Cloud
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

# --- COMPONENTES DE INTERFACE ---

def write_ypoema(texto, imagem):
    """Layout Lateralidade: Texto (2/3) | Imagem (1/3)"""
    col_txt, col_img = st.columns([2, 1])
    with col_txt:
        st.markdown(texto)
    with col_img:
        if os.path.exists(imagem):
            st.image(imagem, use_container_width=True)

# --- PÁGINA SOBRE (ABOUT) ---

def page_abouts():
    """Lógica de Navegação da Documentação Completa"""
    # Lista completa baseada no que o servidor revelou
    abouts_list = [
        "index", "comments", "prefácio", "machina", "off-machina", 
        "outros", "traduttore", "bibliografia", "imagens", 
        "samizdát", "notes", "license"
    ]

    sobrios = "↓  SOBRE" 
    
    # Sidebar ou Main Selectbox (Mantendo no Main por enquanto)
    opt_abouts = st.selectbox(
        sobrios,
        abouts_list,
        index=0,
        key="opt_abouts",
    )

    permitir_exibicao_texto = True 
    if st.session_state.get('vydo', False):
        permitir_exibicao_texto = False 
        st.session_state.vydo = False

    if permitir_exibicao_texto:
        nome_base = opt_abouts.upper()
        
        with st.expander("", expanded=True):
            if nome_base == "MACHINA":
                # Renderização Bipartida da Machina
                st.markdown(load_md_file("ABOUT_MACHINA_A.MD"))
                
                # Interface Viva: Matriz Visual
                tema_atual = st.session_state.get('tema', 'default')
                path_img = f"./images/matrix/{tema_atual}.jpg"
                # Aqui o código renderizaria o load_info(tema_atual)
                
                st.markdown(load_md_file("ABOUT_MACHINA_D.MD"))
            
            else:
                # Carregamento Dinâmico para as demais páginas
                arquivo_alvo = f"ABOUT_{nome_base}.MD"
                st.markdown(load_md_file(arquivo_alvo))

# --- MOTOR PRINCIPAL ---

def main():
    # 1. Configuração de Página (Wide)
    st.set_page_config(
        page_title="yPoemas - A Máquina de Fazer Poesia",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 2. Inicialização de Estados do Sistema
    if 'tema' not in st.session_state:
        st.session_state.tema = "default"
    if 'vydo' not in st.session
