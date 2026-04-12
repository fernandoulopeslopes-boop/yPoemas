import streamlit as st
import os

# --- MOTOR DE BUSCA (v.33.15 - FIDELIDADE ABSOLUTA) ---

def load_md_file(file_name):
    """Localiza e lê arquivos na pasta md_files (Local/Cloud)."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder = r"C:\ypo\md_files" if os.path.exists(r"C:\ypo") else os.path.join(base_dir, "md_files")
    
    target_upper = file_name.upper()
    if os.path.exists(folder):
        try:
            for arquivo in os.listdir(folder):
                if arquivo.upper() == target_upper:
                    with open(os.path.join(folder, arquivo), "r", encoding="utf-8") as f:
                        return f.read()
        except Exception as e:
            return f"⚠️ Erro: {str(e)}"
    return f"⚠️ {target_upper} não localizado."

# --- PÁGINA SOBRE (ABOUT) ---

def page_abouts():
    """Navegação interna da página About."""
    abouts_list = [
        "prefácio", "machina", "off-machina", "outros", 
        "traduttore", "bibliografia", "imagens", "samizdát", 
        "comments", "notes", "license", "index"
    ]
    
    opt_abouts = st.selectbox(
        "↓ DETALHES", 
        abouts_list, 
        index=abouts_list.index(st.session_state.get('sub_page', 'prefácio'))
    )
    st.session_state.sub_page = opt_abouts
    
    with st.expander(f"{opt_abouts.upper()}", expanded=True):
        if opt_abouts.upper() == "MACHINA":
            st.markdown(load_md_file("ABOUT_MACHINA_A.MD"))
            st.markdown(load_md_file("ABOUT_MACHINA_D.MD"))
        else:
            st.markdown(load_md_file(f"ABOUT_{opt_abouts.upper()}.MD"))

# --- MOTOR PRINCIPAL ---

def main():
    st.set_page_config(
        page_title="yPoemas",
        layout="wide"
    )

    # Inicialização de Estados
    if 'tema' not in st.session_state: st.session_state.tema = "default"
    if 'lang' not in st.session_state: st.session_state.lang = "PT"
    if 'sub_page' not in st.session_state: st.session_state.sub_page = "prefácio"

    # --- MENU HORIZONTAL (ORDEM CORRIGIDA: DEMO EM 1º) ---
    tab_demo, tab_ypoemas, tab_eureka, tab_off, tab_comments, tab_about = st.tabs([
        "Demo",
        "yPoemas", 
        "Eureka", 
        "Off-Machina", 
        "Comments", 
        "About"
    ])

    # --- RENDERIZAÇÃO ---
    with tab_demo:
        st.markdown(load_md_file("INFO_DEMO.MD"))

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

    # --- SIDEBAR ORIGINAL ---
    with st.sidebar:
        st.title("yPoemas")
        st.write("v.33.15")
        st.divider()
        st.session_state.lang = st.selectbox("IDIOMA", ["PT", "ES", "EN", "FR", "IT"])
        st.session_state.tema = st.select_slider("TEMA", options=["default", "caos", "matrix"])

if __name__ == "__main__":
    main()
