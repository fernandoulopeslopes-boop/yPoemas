import streamlit as st
import extra_streamlit_components as stx
import os

# --- DIRETRIZES TÉCNICAS (CONSOLIDADAS) ---
PATH_MD = r"md_files"
PATH_LOGO = "image_0.png"

# LINHA ZERO: Sigla - Nome
IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    # 1. SETUP DE PÁGINA (Sempre o primeiro comando)
    try:
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except:
        pass

    # 2. CSS PARA DESTRAVAR INTERFACE
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { width: 300px !important; min-width: 300px !important; }
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            .block-container { padding-top: 1rem !important; }
            [data-testid="stVerticalBlock"] > div:first-child { margin-top: -2.5rem; }
        </style>
    """, unsafe_allow_html=True)

    # 3. GESTÃO DE ESTADO (NAVEGAÇÃO)
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    
    if 'current_tab_idx' not in st.session_state:
        st.session_state.current_tab_idx = 1

    # --- 4. LINHA ZERO (HEADER) ---
    c_topo = st.columns([7, 3])
    with c_topo[1]:
        st.selectbox("Idioma", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # --- 5. MOTOR DO PALCO (TAB BAR) ---
    # Capturamos a aba selecionada
    tab_id = stx.tab_bar(data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
                         default=tabs_list[st.session_state.current_tab_idx])
    
    # Sincronização obrigatória
    if st.session_state.current_tab_idx != tabs_list.index(tab_id):
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    active_tab = tabs_list[st.session_state.current_tab_idx]

    # --- 6. SIDEBAR (IDENTIDADE + INFO) ---
    # Injetando conteúdo explicitamente para evitar "Sidebar Vazia"
    with st.sidebar:
        if os.path.exists(PATH_LOGO):
            st.image(PATH_LOGO, use_container_width=True)
        else:
            st.warning("Logo não encontrado.")
        
        st.markdown("---")
        
        # Carregamento de INFO (Tratando hífen e acento)
        # Tenta INFO_OFF_MÁQUINA.md ou INFO_OFF_MAQUINA.md
        file_name = active_tab.replace("-", "_").upper()
        info_path = os.path.join(PATH_MD, f"INFO_{file_name}.md")
        
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.info(f"Aguardando conteúdo: INFO_{file_name}.md")

    # --- 7. PALCO CENTRAL (ARTE + CONTEÚDO) ---
    # Arte da página
    img_base = active_tab.replace("-", "_")
    img_path = os.path.join(PATH_MD, f"{img_base}.jpg")
    
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.caption(f"Arte não encontrada: {img_base}.jpg")

    # Conteúdo Específico: COMMENTS
    if active_tab == "comments":
        comm_path = os.path.join(PATH_MD, "COMMENTS.md")
        if os.path.exists(comm_path):
            with open(comm_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.markdown("### Comentários\n*Nenhum registro encontrado em COMMENTS.md*")

    # Conteúdo Específico: OFF-MÁQUINA
    if active_tab == "off-máquina":
        off_path = os.path.join(PATH_MD, "OFF_MAQUINA_CONTENT.md")
        if os.path.exists(off_path):
            with open(off_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

if __name__ == "__main__":
    main()
