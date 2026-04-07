import streamlit as st
import extra_streamlit_components as stx
import os

# --- DIRETRIZES TÉCNICAS (ESTRUTURA MACHINA) ---
PATH_MD = r"md_files"
PATH_LOGO = "image_0.png"

# LINHA ZERO: Sigla - Nome (ABC Ocidental)
IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    # Setup de página: Layout Wide para acomodar a Sidebar de 300px
    try: 
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except: 
        pass

    # Estética CSS: Sidebar travada e ajuste de topo para a Linha Zero
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { width: 300px !important; min-width: 300px !important; }
            .stAppHeader { height: 0px; }
            .block-container { padding-top: 0.5rem !important; }
        </style>
    """, unsafe_allow_html=True)
    
    # LISTA DE PÁGINAS (Conceito: off-máquina)
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    
    if 'current_tab_idx' not in st.session_state: 
        st.session_state.current_tab_idx = 1

    # --- 1. LINHA ZERO (ABSOLUTA NO TOPO) ---
    # Posicionada antes da TabBar para garantir que fique FORA do palco
    c_topo = st.columns([7, 3])
    with c_topo[1]:
        st.selectbox("Idioma", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # --- 2. PALCO CENTRAL: TAB BAR (MOTOR) ---
    tab_id = stx.tab_bar(data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
                         default=tabs_list[st.session_state.current_tab_idx])
    
    # Sincronização e Rerun imediato para evitar lag na Sidebar e na Arte
    if st.session_state.current_tab_idx != tabs_list.index(tab_id):
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    active_tab = tabs_list[st.session_state.current_tab_idx]

    # --- 3. SIDEBAR (IDENTIDADE + INFO SINCRONIZADA) ---
    with st.sidebar:
        # Bloco I: Identidade (Apenas o Logotipo)
        if os.path.exists(PATH_LOGO):
            st.image(PATH_LOGO, use_container_width=True)
        
        st.markdown("---")
        
        # Bloco II: INFO (Markdown do Contexto da Página)
        # Nome do arquivo segue o padrão: INFO_OFF_MÁQUINA.md
        file_name = active_tab.replace("-", "_").upper()
        info_path = os.path.join(PATH_MD, f"INFO_{file_name}.md")
        
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

    # --- 4. PALCO CENTRAL: ARTE ---
    # A imagem da página aparece imediatamente abaixo da TabBar
    img_name = active_tab.replace("-", "_") + ".jpg"
    img_path = os.path.join(PATH_MD, img_name)
    
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)

if __name__ == "__main__":
    main()
