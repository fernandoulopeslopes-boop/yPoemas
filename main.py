import streamlit as st
import os

# --- MOTOR DE BUSCA (v.33.9 - ANTI-RESÍDUO & CASE INSENSITIVE) ---

def load_md_file(file_name):
    """Localiza e lê arquivos na pasta md_files (Local/Cloud)."""
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
            return f"⚠️ Erro: {str(e)}"
    return f"⚠️ {target_upper} não localizado."

# --- PÁGINAS DE MODO (PLACEHOLDERS) ---

def page_eureka():
    st.title("💡 Modo Eureka")
    st.markdown(load_md_file("MANUAL_EUREKA.MD"))

def page_ypoemas():
    st.title("📜 Modo yPoemas")
    st.markdown(load_md_file("MANUAL_YPOEMAS.MD"))

def page_off_machina():
    st.title("🔌 Off-Machina")
    st.markdown(load_md_file("MANUAL_OFF-MACHINA.MD"))

# --- PÁGINA SOBRE (ABOUT) ---

def page_abouts():
    """Navegação da Documentação"""
    abouts_list = [
        "prefácio", "machina", "off-machina", "outros", 
        "traduttore", "bibliografia", "imagens", "samizdát", 
        "comments", "notes", "license", "index"
    ]
    
    # Seletor secundário para a documentação
    opt_abouts = st.selectbox("↓ DETALHES", abouts_list, index=0)
    
    placeholder = st.empty()
    with placeholder.container():
        nome_base = opt_abouts.upper()
        with st.expander(f"EXIBINDO: {nome_base}", expanded=True):
            if nome_base == "MACHINA":
                st.markdown(load_md_file("ABOUT_MACHINA_A.MD"))
                st.markdown(load_md_file("ABOUT_MACHINA_D.MD"))
            else:
                st.markdown(load_md_file(f"ABOUT_{nome_base}.MD"))

# --- MOTOR PRINCIPAL (MENU COMPLETO) ---

def main():
    st.set_page_config(layout="wide", page_title="A Máquina de Fazer Poesia")

    # Inicialização de Estados
    if 'tema' not in st.session_state: st.session_state.tema = "default"
    if 'vydo' not in st.session_state: st.session_state.vydo = False

    # --- SIDEBAR: MENU DE NAVEGAÇÃO COMPLETO ---
    with st.sidebar:
        st.title("yPoemas")
        st.write("v.33.9")
        st.divider()
        
        # O Coração da Navegação
        menu_principal = [
            "Modo yPoemas", 
            "Modo Eureka", 
            "Off-Machina", 
            "Comments", 
            "About"
        ]
        
        escolha = st.radio("NAVEGAÇÃO", menu_principal)
        st.divider()

    # --- LÓGICA DE EXIBIÇÃO (ANTI-LIXO) ---
    main_container = st.empty()
    
    with main_container.container():
        if escolha == "Modo yPoemas":
            page_ypoemas()
        
        elif escolha == "Modo Eureka":
            page_eureka()
            
        elif escolha == "Off-Machina":
            page_off_machina()
            
        elif escolha == "Comments":
            # Exibe diretamente o arquivo de comentários
            st.markdown(load_md_file("ABOUT_COMMENTS.MD"))
            
        elif escolha == "About":
            page_abouts()

if __name__ == "__main__":
    main()
