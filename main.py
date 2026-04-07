import streamlit as st
import extra_streamlit_components as stx
import os

# --- CONFIGURAÇÕES DE DIRETÓRIO (BASE SALVADOR) ---
PATH_MD = r"md_files"
PATH_LOGO = "image_0.png"

# LINHA ZERO: Sigla - Nome (ABC Ocidental)
IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    # Setup de página e largura da Sidebar
    try: 
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except: 
        pass

    st.markdown("""
        <style>
            [data-testid="stSidebar"] { width: 300px !important; min-width: 300px !important; }
            .stAppHeader { height: 0px; }
            .block-container { padding-top: 0rem !important; }
        </style>
    """, unsafe_allow_html=True)
    
    # LISTA DE PÁGINAS (Conceito: off-máquina)
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    
    if 'current_tab_idx' not in st.session_state: 
        st.session_state.current_tab_idx = 1

    # --- 1. LINHA ZERO (TOPO ABSOLUTO) ---
    with st.container():
        _, c_lang = st.columns([7, 3])
        with c_lang:
            st.selectbox("", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # --- 2. PALCO CENTRAL: TAB BAR ---
    # Capturamos o ID da aba ANTES da sidebar para sincronizar o INFO
    tab_id = stx.tab_bar(data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
                         default=tabs_list[st.session_state.current_tab_idx])
    
    # Sincronização de Estado
    if st.session_state.current_tab_idx != tabs_list.index(tab_id):
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    active_tab = tabs_list[st.session_state.current_tab_idx]

    # --- 3. SIDEBAR (IDENTIDADE + INFO) ---
    with st.sidebar:
        # Bloco I: Identidade
        if os.path.exists(PATH_LOGO):
            st.image(PATH_LOGO, use_container_width=True)
        
        st.markdown("---")
        
        # Bloco II: INFO (Markdown Sincronizado)
        # Converte "off-máquina" para "OFF_MÁQUINA" para o arquivo MD
        file_name = active_tab.replace("-", "_").upper()
        info_path = os.path.join(PATH_MD, f"INFO_{file_name}.md")
        
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

    # --- 4. PALCO CENTRAL: ARTE ---
    # A imagem deve aparecer logo abaixo da TabBar
    img_file = active_tab.replace("-", "_") + ".jpg"
    img_path = os.path.join(PATH_MD, img_file)
    
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)

if __name__ == "__main__":
    main()
