import streamlit as st
import extra_streamlit_components as stx
import os

# --- DIRETRIZES TÉCNICAS (BACKUP SALVADOR) ---
PATH_MD = r"md_files"
PATH_LOGO = "image_0.png"

# LINHA ZERO: Sigla - Nome (ABC Ocidental)
IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    # 1. O PRIMEIRO BATIMENTO: set_page_config deve ser a primeira instrução Streamlit.
    try: 
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except: 
        pass

    # Estética: Sidebar 300px e limpeza de margens para subir a Linha Zero
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { width: 300px !important; min-width: 300px !important; }
            .block-container { padding-top: 0.5rem !important; }
            [data-testid="stHeader"] { background: rgba(0,0,0,0); height: 0px; }
            .stSelectbox { margin-top: -15px; }
        </style>
    """, unsafe_allow_html=True)
    
    # LISTA DE PÁGINAS (Conceito: off-máquina)
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    
    if 'current_tab_idx' not in st.session_state: 
        st.session_state.current_tab_idx = 1

    # --- 2. LINHA ZERO (SELECTOR DE IDIOMAS) ---
    # Para tirar do palco, ele deve ser renderizado ANTES da TabBar e em coluna isolada.
    c_topo_l, c_topo_r = st.columns([8, 2])
    with c_topo_r:
        st.selectbox("", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # --- 3. PALCO: MOTOR DE NAVEGAÇÃO ---
    tab_id = stx.tab_bar(data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
                         default=tabs_list[st.session_state.current_tab_idx])
    
    # Sincronização de Estado (Prevenção de Lag)
    if st.session_state.current_tab_idx != tabs_list.index(tab_id):
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    active_tab = tabs_list[st.session_state.current_tab_idx]

    # --- 4. SIDEBAR (IDENTIDADE + INFO) ---
    with st.sidebar:
        # Bloco I: Identidade
        if os.path.exists(PATH_LOGO):
            st.image(PATH_LOGO, use_container_width=True)
        
        st.markdown("---")
        
        # Bloco II: INFO (Markdown sincronizado)
        # Normalização de nomes para arquivos: "off-máquina" -> "OFF_MÁQUINA"
        file_name = active_tab.replace("-", "_").upper()
        info_path = os.path.join(PATH_MD, f"INFO_{file_name}.md")
        
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

    # --- 5. PALCO: ARTE DA PÁGINA ---
    # A imagem deve aparecer imediatamente abaixo da TabBar no palco.
    img_file = active_tab.replace("-", "_") + ".jpg"
    img_path = os.path.join(PATH_MD, img_file)
    
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)

if __name__ == "__main__":
    main()
