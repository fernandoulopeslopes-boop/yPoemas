import streamlit as st
import os

# --- MOTOR DE BUSCA (ESTÁVEL & COERENTE) ---
def load_md_file(file_name):
    """Localiza arquivos MD priorizando /md_files e depois a raiz."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    search_paths = [os.path.join(base_dir, "md_files"), base_dir]
    
    target = file_name.upper()
    for folder in search_paths:
        if os.path.exists(folder):
            try:
                for arquivo in os.listdir(folder):
                    if arquivo.upper() == target:
                        with open(os.path.join(folder, arquivo), "r", encoding="utf-8") as f:
                            return f.read()
            except Exception: continue
    return f"⚠️ {target} não localizado."

# --- INTERFACE PRINCIPAL ---
def main():
    st.set_page_config(page_title="yPoemas", layout="wide")

    # CSS: Limpeza, Largura da Sidebar e Botões Suaves
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { min-width: 300px; max-width: 300px; }
        div.stButton > button { 
            border-radius: 20px; 
            background-color: rgba(0, 0, 0, 0.05); 
            border: 1px solid rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # 1. NAVEGAÇÃO DO PALCO (TABS NO TOPO)
    # A ordem que você definiu como original e funcional
    tabs_labels = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
    tab_demo, tab_ypo, tab_eur, tab_off, tab_com, tab_abt = st.tabs(tabs_labels)

    # Dicionário de Imagens (Arquivos na raiz confirmados por você)
    img_map = {
        "Demo": "img_demo.jpg",
        "yPoemas": "img_ypoemas.jpg",
        "Eureka": "img_eureka.jpg",
        "Off-Machina": "img_off-machina.jpg",
        "Comments": "img_about.jpg",
        "About": "img_about.jpg"
    }

    # 2. RENDERIZAÇÃO DO CONTEÚDO (PALCO)
    # Usamos o contexto de cada aba para setar o que a Sidebar deve mostrar
    with tab_demo:
        st.session_state.active = "Demo"
        video_path = "video_DEMO.mp4"
        if os.path.exists(video_path): st.video(video_path)
        else: st.write(" ") # Espaço da Máquina

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

    # 3. SIDEBAR (A VERSÃO PRONTA)
    with st.sidebar:
        # Idiomas (Western ABC)
        idiomas = ["Português", "Español", "English", "Français", "Italiano", "Deutsch", "Català", "Galego", "Latin", "Română"]
        st.selectbox("🌐 IDIOMA", options=idiomas)
        st.divider()

        # ARTE (Sincronizada com o Palco)
        current = st.session_state.get("active", "Demo")
        target_img = img_map.get(current)
        if target_img and os.path.exists(target_img):
            st.image(target_img, use_container_width=True)
        
        st.divider()

        # INFO (Sincronizado via /md_files/)
        st.markdown(load_md_file(f"INFO_{current.upper()}.MD"))
        
        st.divider()
        
        # CONTATOS
        st.markdown("### Contatos")
        st.markdown("🌐 [GitHub](https://github.com/)")
        st.markdown("✉️ [Email](mailto:contato@exemplo.com)")

if __name__ == "__main__":
    main()
