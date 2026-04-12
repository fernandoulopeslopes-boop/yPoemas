import streamlit as st
import os

# --- MOTOR DE BUSCA (ESTÁVEL) ---

def load_md_file(file_name):
    """Lê arquivos MD da raiz ou de md_files com prioridade para a raiz."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    paths = [base_dir, os.path.join(base_dir, "md_files")]
    
    for folder in paths:
        path = os.path.join(folder, file_name)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    return f"⚠️ {file_name} não localizado."

# --- MOTOR PRINCIPAL ---

def main():
    st.set_page_config(
        page_title="yPoemas",
        layout="wide"
    )

    # CSS Original (300px e Botões Suaves)
    st.markdown("""
        <style>
        div.stButton > button {
            border-radius: 20px;
            background-color: rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.1);
            padding: 5px 15px;
        }
        [data-testid="stSidebar"] {
            min-width: 300px;
            max-width: 300px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 1. PALCO (NAVEGAÇÃO SUPERIOR)
    tabs = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
    tab_objs = st.tabs(tabs)

    # 2. RENDERIZAÇÃO E LOGICA DE CONTEXTO
    # Identifica a aba para a sidebar não "se perder"
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Demo"

    with tab_objs[0]: # Demo
        st.session_state.active_tab = "Demo"
        if os.path.exists("video_DEMO.mp4"):
            st.video("video_DEMO.mp4")

    with tab_objs[1]: # yPoemas
        st.session_state.active_tab = "yPoemas"
        st.markdown(load_md_file("MANUAL_YPOEMAS.MD"))

    with tab_objs[2]: # Eureka
        st.session_state.active_tab = "Eureka"
        st.markdown(load_md_file("MANUAL_EUREKA.MD"))

    with tab_objs[3]: # Off-Machina
        st.session_state.active_tab = "Off-Machina"
        st.markdown(load_md_file("MANUAL_OFF-MACHINA.MD"))

    with tab_objs[4]: # Comments
        st.session_state.active_tab = "Comments"
        st.markdown(load_md_file("ABOUT_COMMENTS.MD"))

    with tab_objs[5]: # About
        st.session_state.active_tab = "About"
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("Prefácio"): st.session_state.sub = "prefácio"
        if c2.button("Machina"): st.session_state.sub = "machina"
        if c3.button("Imagens"): st.session_state.sub = "imagens"
        if c4.button("Index"): st.session_state.sub = "index"
        sub = st.session_state.get('sub', 'prefácio')
        st.markdown(load_md_file(f"ABOUT_{sub.upper()}.MD"))

    # 3. SIDEBAR (A VERSÃO PRONTA)
    with st.sidebar:
        # Lista de Idiomas (Western ABC)
        idiomas_abc = ["Português", "Español", "English", "Français", "Italiano", "Deutsch", "Català", "Galego", "Latin", "Română"]
        st.selectbox("🌐 IDIOMA", options=idiomas_abc)
        st.divider()

        # ARTE DINÂMICA (Fixa por página)
        tab_ref = st.session_state.active_tab
        img_file = f"img_{tab_ref.lower()}.jpg"
        
        if os.path.exists(img_file):
            st.image(img_file, use_container_width=True)
        elif os.path.exists(f"images/{img_file}"):
            st.image(f"images/{img_file}", use_container_width=True)
        
        st.divider()

        # INFO DA PÁGINA
        info_file = f"INFO_{tab_ref.upper()}.MD"
        st.markdown(load_md_file(info_file))

        st.divider()

        # CONTATOS
        st.markdown("### Contatos")
        st.markdown("🌐 [GitHub](https://github.com/)")
        st.markdown("✉️ [Email](mailto:contato@exemplo.com)")

if __name__ == "__main__":
    main()
