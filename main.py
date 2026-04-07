import streamlit as st
import extra_streamlit_components as stx
import os

# --- DIRETRIZES TÉCNICAS (ESTRUTURA MACHINA) ---
PATH_MD = r"md_files"
PATH_LOGO = "image_0.png"

# Sigla - Nome (ABC Ocidental)
IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    # Setup inicial
    try: 
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except: 
        pass

    # CSS: Sidebar 300px + Limpeza de Palco
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { width: 300px !important; min-width: 300px !important; }
            .stAppHeader { background-color: transparent; height: 0px; }
            .block-container { padding-top: 1rem !important; }
            [data-testid="stVerticalBlock"] > div:first-child { margin-top: -2.5rem; }
        </style>
    """, unsafe_allow_html=True)
    
    # LISTA DE PÁGINAS (Nome-conceito: off-máquina)
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    
    # Inicialização segura do índice
    if 'current_tab_idx' not in st.session_state: 
        st.session_state.current_tab_idx = 1

    # --- 1. LINHA ZERO (ABSOLUTA NO TOPO DIREITO) ---
    c_topo = st.columns([7, 3])
    with c_topo[1]:
        st.selectbox("Idioma", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # --- 2. MOTOR DE NAVEGAÇÃO (PALCO) ---
    # Capturamos o tab_id imediatamente. 
    # Se ele mudar, forçamos o rerun para que a Sidebar (que vem depois no código) se atualize.
    tab_id = stx.tab_bar(data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
                         default=tabs_list[st.session_state.current_tab_idx])
    
    # Sincronização Crítica
    if st.session_state.current_tab_idx != tabs_list.index(tab_id):
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    # Definimos a página ativa para todo o restante do script
    active_tab = tabs_list[st.session_state.current_tab_idx]

    # --- 3. SIDEBAR (IDENTIDADE + INFO SINCRONIZADA) ---
    with st.sidebar:
        # Bloco I: Identidade
        if os.path.exists(PATH_LOGO):
            st.image(PATH_LOGO, use_container_width=True)
        
        st.markdown("---")
        
        # Bloco II: INFO (Texto explicativo sincronizado)
        # Sincronia garantida pelo st.rerun() acima
        file_name = active_tab.replace("-", "_").upper()
        info_path = os.path.join(PATH_MD, f"INFO_{file_name}.md")
        
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.caption(f"INFO_{file_name}.md aguardando conteúdo.")

    # --- 4. PALCO CENTRAL: ARTE E CONTEÚDO ---
    # A Arte da página (JPG) sincronizada
    img_name = active_tab.replace("-", "_") + ".jpg"
    img_path = os.path.join(PATH_MD, img_name)
    
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)

    # Conteúdo Específico: COMMENTS
    if active_tab == "comments":
        comm_path = os.path.join(PATH_MD, "COMMENTS.md")
        if os.path.exists(comm_path):
            with open(comm_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

if __name__ == "__main__":
    main()
