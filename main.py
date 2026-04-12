import streamlit as st
import os

# --- MOTOR DE BUSCA (ESTÁVEL) ---

def load_md_file(file_name):
    """Localiza e lê arquivos na pasta md_files."""
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

# --- MOTOR PRINCIPAL ---

def main():
    st.set_page_config(
        page_title="yPoemas",
        layout="wide"
    )

    # Injeção de CSS para os botões redondos com fundo suave
    st.markdown("""
        <style>
        div.stButton > button {
            border-radius: 20px;
            background-color: rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.1);
            padding: 5px 15px;
            transition: all 0.3s;
        }
        div.stButton > button:hover {
            background-color: rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(0, 0, 0, 0.2);
        }
        </style>
    """, unsafe_allow_html=True)

    # 1. SIDEBAR: APENAS FUNÇÕES TÉCNICAS (Idioma no Topo)
    with st.sidebar:
        st.title("yPoemas")
        st.write("v.33.19")
        st.divider()

        # Lista expandida Western ABC
        idiomas_abc = [
            "Português", "Español", "English", "Français", "Italiano", "Deutsch",
            "Català", "Galego", "Latin", "Română"
        ]
        st.session_state.lang = st.selectbox("🌐 IDIOMA", options=idiomas_abc)
        
        st.divider()
        st.session_state.tema = st.select_slider("🎨 MATRIZ", options=["default", "caos", "matrix"])

    # 2. TOPO DO PALCO: NAVEGAÇÃO DE PÁGINAS (Tabs Limpas)
    tab_demo, tab_ypoemas, tab_eureka, tab_off, tab_comments, tab_about = st.tabs([
        "Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"
    ])

    # 3. CONTEÚDO E BOTÕES DE SUB-NAVEGAÇÃO
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
        # Botões redondos para navegar nos temas de About
        col1, col2, col3, col4 = st.columns(4)
        if col1.button("Prefácio"): st.session_state.sub = "prefácio"
        if col2.button("Machina"): st.session_state.sub = "machina"
        if col3.button("Imagens"): st.session_state.sub = "imagens"
        if col4.button("Index"): st.session_state.sub = "index"
        
        st.divider()
        sub = st.session_state.get('sub', 'prefácio')
        st.markdown(load_md_file(f"ABOUT_{sub.upper()}.MD"))

if __name__ == "__main__":
    main()
