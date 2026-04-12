import streamlit as st
import os

# --- MOTOR DE BUSCA (ESTÁVEL & LOCALIZADO) ---

def load_md_file(file_name):
    """Lê ficheiros MD da pasta md_files ou da raiz."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Prioridade para md_files conforme indicado
    paths = [os.path.join(base_dir, "md_files"), base_dir]
    
    target_upper = file_name.upper()
    for folder in paths:
        if os.path.exists(folder):
            try:
                for arquivo in os.listdir(folder):
                    if arquivo.upper() == target_upper:
                        with open(os.path.join(folder, arquivo), "r", encoding="utf-8") as f:
                            return f.read()
            except Exception:
                continue
    return f"⚠️ {target_upper} não localizado em /md_files ou na raiz."

# --- MOTOR PRINCIPAL ---

def main():
    st.set_page_config(
        page_title="yPoemas",
        layout="wide"
    )

    # CSS Original: Sidebar 300px e Botões Redondos
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

    # 1. PALCO: NAVEGAÇÃO SUPERIOR (TABS)
    tabs_labels = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
    tab_objs = st.tabs(tabs_labels)

    # Inicialização do estado da aba
    if "current_active" not in st.session_state:
        st.session_state.current_active = "Demo"

    # 2. RENDERIZAÇÃO DO CONTEÚDO
    with tab_objs[0]: # DEMO
        st.session_state.current_active = "Demo"
        video_path = "video_DEMO.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.write("---") # Espaço para a Máquina

    with tab_objs[1]: # YPOEMAS
        st.session_state.current_active = "yPoemas"
        st.markdown(load_md_file("MANUAL_YPOEMAS.MD"))

    with tab_objs[2]: # EUREKA
        st.session_state.current_active = "Eureka"
        st.markdown(load_md_file("MANUAL_EUREKA.MD"))

    with tab_objs[3]: # OFF-MACHINA
        st.session_state.current_active = "Off-Machina"
        st.markdown(load_md_file("MANUAL_OFF-MACHINA.MD"))

    with tab_objs[4]: # COMMENTS
        st.session_state.current_active = "Comments"
        st.markdown(load_md_file("ABOUT_COMMENTS.MD"))

    with tab_objs[5]: # ABOUT
        st.session_state.current_active = "About"
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("Prefácio"): st.session_state.sub = "prefácio"
        if c2.button("Machina"): st.session_state.sub = "machina"
        if c3.button("Imagens"): st.session_state.sub = "imagens"
        if c4.button("Index"): st.session_state.sub = "index"
        sub = st.session_state.get('sub', 'prefácio')
        st.markdown(load_md_file(f"ABOUT_{sub.upper()}.MD"))

    # 3. SIDEBAR (CONFIGURAÇÃO FINAL)
    with st.sidebar:
        # Lista de Idiomas Western ABC no topo
        idiomas_abc = ["Português", "Español", "English", "Français", "Italiano", "Deutsch", "Català", "Galego", "Latin", "Română"]
        st.selectbox("🌐 IDIOMA", options=idiomas_abc)
        st.divider()

        # ARTE DA PÁGINA (Imagens na raiz)
        current = st.session_state.current_active
        img_map = {
            "Demo": "img_demo.jpg",
            "yPoemas": "img_ypoemas.jpg",
            "Eureka": "img_eureka.jpg",
            "Off-Machina": "img_off-machina.jpg",
            "Comments": "img_about.jpg",
            "About": "img_about.jpg"
        }
        
        target_img = img_map.get(current)
        if target_img and os.path.exists(target_img):
            st.image(target_img, use_container_width=True)
        
        st.divider()

        # INFO DA PÁGINA (Ficheiros em /md_files/)
        info_file = f"INFO_{current.upper()}.MD"
        st.markdown(load_md_file(info_file))

        st.divider()

        # CONTATOS
        st.markdown("### Contatos")
        st.markdown("🌐 [GitHub](https://github.com/)")
        st.markdown("✉️ [Email](mailto:contato@exemplo.com)")

if __name__ == "__main__":
    main()
