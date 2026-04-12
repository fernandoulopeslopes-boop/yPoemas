import streamlit as st
import os

# --- MOTOR DE BUSCA (ESTÁVEL) ---

def load_md_file(file_name):
    """Lê ficheiros MD da pasta md_files ou da raiz."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Prioridade absoluta para md_files conforme sua organização
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
    return f"⚠️ {target_upper} não localizado."

# --- MOTOR PRINCIPAL ---

def main():
    st.set_page_config(
        page_title="yPoemas",
        layout="wide"
    )

    # CSS: Sidebar 300px, Botões Redondos e Estilo das Tabs
    st.markdown("""
        <style>
        /* Botões redondos e suaves */
        div.stButton > button {
            border-radius: 20px;
            background-color: rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.1);
            padding: 5px 15px;
        }
        /* Fixar largura da Sidebar */
        [data-testid="stSidebar"] {
            min-width: 300px;
            max-width: 300px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- CONTROLE DE NAVEGAÇÃO (SINCRONIA PALCO/SIDEBAR) ---
    # Usamos Tabs, mas forçamos a atualização do estado para a Sidebar
    tabs_labels = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
    
    # IMPORTANTE: No Streamlit, st.tabs não guarda estado nativo facilmente para a sidebar.
    # Vamos usar um rádio horizontal ou capturar a mudança via session_state.
    
    tab_demo, tab_ypo, tab_eur, tab_off, tab_com, tab_abt = st.tabs(tabs_labels)

    # Mapeamento de Imagens (Raiz)
    img_map = {
        "Demo": "img_demo.jpg",
        "yPoemas": "img_ypoemas.jpg",
        "Eureka": "img_eureka.jpg",
        "Off-Machina": "img_off-machina.jpg",
        "Comments": "img_about.jpg",
        "About": "img_about.jpg"
    }

    # 1. RENDERIZAÇÃO DO PALCO & CAPTURA DE ESTADO
    
    with tab_demo:
        st.session_state.active = "Demo"
        video_path = "video_DEMO.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.write(" ") # Espaço para a Máquina

    with tab_ypo:
        st.session_state.active = "yPoemas"
        st.markdown(load_md_file("MANUAL_YPOEMAS.MD"))

    with tab_eur:
        st.session_state.active = "Eureka"
        st.markdown(load_md_file("MANUAL_EUREKA.MD"))

    with tab_off:
        st.session_state.active = "Off-Machina"
        st.markdown(load_md_file("MANUAL_OFF-MACHINA.MD"))

    with tab_com:
        st.session_state.active = "Comments"
        st.markdown(load_md_file("ABOUT_COMMENTS.MD"))

    with tab_abt:
        st.session_state.active = "About"
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("Prefácio"): st.session_state.sub = "prefácio"
        if c2.button("Machina"): st.session_state.sub = "machina"
        if c3.button("Imagens"): st.session_state.sub = "imagens"
        if c4.button("Index"): st.session_state.sub = "index"
        sub = st.session_state.get('sub', 'prefácio')
        st.markdown(load_md_file(f"ABOUT_{sub.upper()}.MD"))

    # 2. SIDEBAR (CONTEÚDO DINÂMICO BASEADO NO PALCO)
    with st.sidebar:
        # Idiomas no topo
        idiomas_abc = ["Português", "Español", "English", "Français", "Italiano", "Deutsch", "Català", "Galego", "Latin", "Română"]
        st.selectbox("🌐 IDIOMA", options=idiomas_abc)
        st.divider()

        # ARTE DA PÁGINA
        # Se o st.tabs não atualizar o estado a tempo, usamos um seletor auxiliar ou o estado atual
        current = st.session_state.get("active", "Demo")
        
        target_img = img_map.get(current, "img_demo.jpg")
        if os.path.exists(target_img):
            st.image(target_img, use_container_width=True)
        
        st.divider()

        # INFO DA PÁGINA (Sempre de /md_files/)
        info_file = f"INFO_{current.upper()}.MD"
        st.markdown(load_md_file(info_file))

        st.divider()

        # CONTATOS
        st.markdown("### Contatos")
        st.markdown("🌐 [GitHub](https://github.com/)")
        st.markdown("✉️ [Email](mailto:contato@exemplo.com)")

if __name__ == "__main__":
    main()
