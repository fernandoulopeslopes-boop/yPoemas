import streamlit as st
import os

# --- MOTOR DE BUSCA (v.33.9 - CASE INSENSITIVE & ANTI-RESÍDUO) ---

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

# --- PÁGINA SOBRE (ABOUT) ---

def page_abouts():
    """Navegação da Documentação Detalhada"""
    abouts_list = [
        "prefácio", "machina", "off-machina", "outros", 
        "traduttore", "bibliografia", "imagens", "samizdát", 
        "comments", "notes", "license", "index"
    ]
    
    # Seletor secundário para a documentação técnica
    opt_abouts = st.selectbox("↓ DETALHES", abouts_list, index=0)
    
    nome_base = opt_abouts.upper()
    with st.expander(f"DOCUMENTAÇÃO: {nome_base}", expanded=True):
        if nome_base == "MACHINA":
            st.markdown(load_md_file("ABOUT_MACHINA_A.MD"))
            st.markdown(load_md_file("ABOUT_MACHINA_D.MD"))
        else:
            st.markdown(load_md_file(f"ABOUT_{nome_base}.MD"))

# --- MOTOR PRINCIPAL (LAYOUT HORIZONTAL COMPLETO) ---

def main():
    st.set_page_config(
        page_title="yPoemas - A Máquina de Fazer Poesia",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inicialização de Estados
    if 'tema' not in st.session_state: st.session_state.tema = "default"
    if 'vydo' not in st.session_state: st.session_state.vydo = False

    # --- MENU HORIZONTAL (ABAS) ---
    tab_ypoemas, tab_eureka, tab_off, tab_comments, tab_about = st.tabs([
        "📜 Modo yPoemas", 
        "💡 Modo Eureka", 
        "🔌 Off-Machina", 
        "💬 Comments", 
        "ℹ️ About"
    ])

    # --- RENDERIZAÇÃO POR TAB ---
    with tab_ypoemas:
        st.markdown(load_md_file("MANUAL_YPOEMAS.MD"))

    with tab_eureka:
        st.markdown(load_md_file("MANUAL_EUREKA.MD"))

    with tab_off:
        st.markdown(load_md_file("MANUAL_OFF-MACHINA.MD"))

    with tab_comments:
        st.markdown(load_md_file("ABOUT_COMMENTS.MD"))

    with tab_about:
        page_abouts()

    # --- SIDEBAR (IDENTIDADE E CONTROLE) ---
    with st.sidebar:
        st.title("yPoemas")
        st.write("v.33.9")
        st.divider()

if __name__ == "__main__":
    main()
