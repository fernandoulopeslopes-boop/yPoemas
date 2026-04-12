import streamlit as st
import os

# --- MOTOR DE BUSCA (ESTÁVEL) ---

def load_md_file(file_name):
    """Lê ficheiros MD da pasta md_files ou da raiz."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
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
    st.set_page_config(page_title="yPoemas", layout="wide")

    # Estilo: Sidebar 300px e Botões Suaves (Menu e Sub-menus)
    st.markdown("""
        <style>
        div.stButton > button {
            border-radius: 20px;
            background-color: rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.1);
            padding: 5px 15px;
            width: 100%;
        }
        [data-testid="stSidebar"] {
            min-width: 300px;
            max-width: 300px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 1. NAVEGAÇÃO DO PALCO (BOTÕES NO TOPO)
    if "active_page" not in st.session_state:
        st.session_state.active_page = "Demo"

    cols_nav = st.columns(6)
    paginas = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
    
    for idx, pg in enumerate(paginas):
        if cols_nav[idx].button(pg):
            st.session_state.active_page = pg
            st.rerun()

    st.divider()

    # 2. RENDERIZAÇÃO DO CONTEÚDO (PALCO)
    current = st.session_state.active_page

    if current == "Demo":
        video_path = "video_DEMO.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.write(" ") # Área da Máquina

    elif current == "About":
        col1, col2, col3, col4 = st.columns(4)
        if col1.button("Prefácio"): st.session_state.sub = "prefácio"
        if col2.button("Machina"): st.session_state.sub = "machina"
        if col3.button("Imagens"): st.session_state.sub = "imagens"
        if col4.button("Index"): st.session_state.sub = "index"
        
        sub = st.session_state.get('sub', 'prefácio')
        st.markdown(load_md_file(f"ABOUT_{sub.upper()}.MD"))

    elif current == "Comments":
        st.markdown(load_md_file("ABOUT_COMMENTS.MD"))

    else:
        st.markdown(load_md_file(f"MANUAL_{current.upper()}.MD"))

    # 3. SIDEBAR (SINCRONIZADA PELOS BOTÕES)
    with st.sidebar:
        # Idiomas Western ABC
        idiomas_abc = ["Português", "Español", "English", "Français", "Italiano", "Deutsch", "Català", "Galego", "Latin", "Română"]
        st.selectbox("🌐 IDIOMA", options=idiomas_abc)
        st.divider()

        # ARTE DA PÁGINA (Direto da Raiz)
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

        # INFO DA PÁGINA (De /md_files/)
        st.markdown(load_md_file(f"INFO_{current.upper()}.MD"))

        st.divider()

        # CONTATOS
        st.markdown("### Contatos")
        st.markdown("🌐 [GitHub](https://github.com/)")
        st.markdown("✉️ [Email](mailto:contato@exemplo.com)")

if __name__ == "__main__":
    main()
