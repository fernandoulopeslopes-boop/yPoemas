import streamlit as st
import os

# --- MOTOR DE BUSCA (v.33.9 - CASE INSENSITIVE & MULTI-AMBIENTE) ---

def load_md_file(file_name):
    """
    Motor v.33.9 - Busca Inteligente.
    Resolve o conflito entre .MD (HD) e .md (GitHub).
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
            
    return f"⚠️ {target_upper} não localizado em {folder}"

# --- COMPONENTES DE INTERFACE ---

def page_abouts():
    """Navegação da Documentação Técnica"""
    abouts_list = [
        "prefácio", "machina", "off-machina", "outros", 
        "traduttore", "bibliografia", "imagens", "samizdát", 
        "comments", "notes", "license", "index"
    ]
    
    # Seletor com persistência de estado
    opt_abouts = st.selectbox(
        "↓ DETALHES", 
        abouts_list, 
        index=abouts_list.index(st.session_state.get('sub_page', 'prefácio'))
    )
    st.session_state.sub_page = opt_abouts
    
    nome_base = opt_abouts.upper()
    
    # Container limpo para exibição
    with st.expander(f"DOCUMENTAÇÃO: {nome_base}", expanded=True):
        if nome_base == "MACHINA":
            st.markdown(load_md_file("ABOUT_MACHINA_A.MD"))
            st.markdown(load_md_file("ABOUT_MACHINA_D.MD"))
        else:
            st.markdown(load_md_file(f"ABOUT_{nome_base}.MD"))

# --- ESTRUTURA MESTRE (LAYOUT HORIZONTAL) ---

def main():
    st.set_page_config(
        page_title="yPoemas - A Máquina de Fazer Poesia",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed" # Foco total no conteúdo central
    )

    # Inicialização de Estados (Consolidado)
    if 'sub_page' not in st.session_state: st.session_state.sub_page = "prefácio"

    # --- MENU HORIZONTAL DE ALTO NÍVEL ---
    tab_ypoemas, tab_eureka, tab_off, tab_comments, tab_about = st.tabs([
        "📜 Modo yPoemas", 
        "💡 Modo Eureka", 
        "🔌 Off-Machina", 
        "💬 Comments", 
        "ℹ️ About"
    ])

    # --- DISTRIBUIÇÃO DE CONTEÚDO ---
    
    with tab_ypoemas:
        st.markdown(load_md_file("MANUAL_YPOEMAS.MD"))

    with tab_eureka:
        st.markdown(load_md_file("MANUAL_EUREKA.MD"))

    with tab_off:
        st.markdown(load_md_file("MANUAL_OFF-MACHINA.MD"))

    with tab_comments:
        # Exibição direta dos comentários (sequência preservada nos MDs)
        st.markdown(load_md_file("ABOUT_COMMENTS.MD"))

    with tab_about:
        page_abouts()

    # --- SIDEBAR (MÍNIMA) ---
    with st.sidebar:
        st.title("yPoemas")
        st.caption("v.33.9 | Linha Zero")
        st.divider()
        st.markdown("Cura e algoritmos poéticos em Western ABC.")

if __name__ == "__main__":
    main()
