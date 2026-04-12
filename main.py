import streamlit as st
import os

# --- MOTOR DE BUSCA (ESTÁVEL) ---

def load_md_file(file_name):
    """Localiza e lê arquivos na pasta md_files ou na raiz."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Verifica primeiro em md_files, depois na raiz
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

    # Estilização dos botões (Redondos e Suaves)
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
    tabs = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
    tab_objs = st.tabs(tabs)

    # Lógica para identificar a aba ativa e carregar o contexto
    # Como o Streamlit executa o script todo, usamos uma variável de estado
    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "Demo"

    # 2. RENDERIZAÇÃO DO CONTEÚDO DO PALCO
    for i, tab in enumerate(tab_objs):
        with tab:
            nome_aba = tabs[i]
            # Atualiza o estado da aba atual para a Sidebar
            # (O Streamlit atualiza isso conforme o clique do usuário)
            
            if nome_aba == "About":
                col1, col2, col3, col4 = st.columns(4)
                if col1.button("Prefácio"): st.session_state.sub = "prefácio"
                if col2.button("Machina"): st.session_state.sub = "machina"
                if col3.button("Imagens"): st.session_state.sub = "imagens"
                if col4.button("Index"): st.session_state.sub = "index"
                sub = st.session_state.get('sub', 'prefácio')
                st.markdown(load_md_file(f"ABOUT_{sub.upper()}.MD"))
                # Quando clica na tab, define o contexto para a Sidebar
                st.session_state.current_tab = "About"
            
            elif nome_aba == "Demo":
                # Vídeo Central da Demo (conforme sua nota)
                video_path = "video_DEMO.mp4" # ou .mov, conforme estiver na raiz
                if os.path.exists(video_path):
                    st.video(video_path)
                else:
                    st.info("Vídeo DEMO não localizado na raiz.")
                st.session_state.current_tab = "Demo"
            
            else:
                st.markdown(load_md_file(f"MANUAL_{nome_aba.upper()}.MD"))
                st.session_state.current_tab = nome_aba

    # 3. SIDEBAR (CONTEÚDO DINÂMICO)
    with st.sidebar:
        # LISTA DE IDIOMAS NO TOPO
        idiomas_abc = [
            "Português", "Español", "English", "Français", "Italiano", "Deutsch",
            "Català", "Galego", "Latin", "Română"
        ]
        st.selectbox("🌐 IDIOMA", options=idiomas_abc)
        st.divider()

        # ARTE DA PÁGINA (Ex: logo_demo.jpg para a aba Demo)
        current = st.session_state.current_tab
        if current == "Demo":
            if os.path.exists("logo_demo.jpg"):
                st.image("logo_demo.jpg", use_container_width=True)
        else:
            # Placeholder para artes das outras páginas
            st.write(f"🎨 [ARTE: {current.upper()}]")
        
        st.divider()

        # INFO_PAGINA (INFO_DEMO.MD, INFO_YPOEMAS.MD, etc.)
        info_text = load_md_file(f"INFO_{current.upper()}.MD")
        st.markdown(info_text)

        st.divider()

        # CONTATOS
        st.markdown("### Contatos")
        st.markdown("🌐 [GitHub](https://github.com/)")
        st.markdown("✉️ [Email](mailto:contato@exemplo.com)")

if __name__ == "__main__":
    main()
