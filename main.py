import streamlit as st
import extra_streamlit_components as stx
import os

# --- DEFINIÇÃO DE CAMINHOS ---
PATH_MD = "md_files"
PATH_LOGO = "image_0.png"

# LINHA ZERO: Sigla - Nome
IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    # 1. CONFIGURAÇÃO MANDATÓRIA (BATIMENTO ZERO)
    try: 
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except: 
        pass

    # CSS PARA EXPULSAR OS IDIOMAS DO PALCO E FIXAR SIDEBAR
    st.markdown("""
        <style>
            /* Fixa Sidebar em 300px */
            [data-testid="stSidebar"] { width: 300px !important; min-width: 300px !important; }
            
            /* Remove margens do bloco principal para subir a TabBar */
            .block-container { padding-top: 0rem !important; margin-top: -30px; }
            
            /* Torna o Header invisível mas funcional */
            [data-testid="stHeader"] { background: rgba(0,0,0,0); height: 0px; }
            
            /* Ajuste fino do seletor para que ele flutue fora da linha de conteúdo */
            .stSelectbox { margin-top: -20px; }
        </style>
    """, unsafe_allow_html=True)
    
    # LISTA DE PÁGINAS (Conceito: off-máquina)
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    
    if 'current_tab_idx' not in st.session_state: 
        st.session_state.current_tab_idx = 1

    # --- 2. LINHA ZERO (HEADER SUPERIOR - ISOLADO) ---
    # Usando st.container para tentar isolar o seletor do fluxo do palco central
    with st.container():
        c_vazio, c_idiomas = st.columns([8, 2])
        with c_idiomas:
            st.selectbox("", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # --- 3. PALCO CENTRAL: NAVEGADOR (TAB BAR) ---
    tab_id = stx.tab_bar(data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
                         default=tabs_list[st.session_state.current_tab_idx])
    
    # Sincronização e Rerun imediato
    if st.session_state.current_tab_idx != tabs_list.index(tab_id):
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    active_tab = tabs_list[st.session_state.current_tab_idx]

    # --- 4. SIDEBAR (IDENTIDADE + INFO SINCRONIZADA) ---
    with st.sidebar:
        # Bloco I: Identidade
        if os.path.exists(PATH_LOGO):
            st.image(PATH_LOGO, use_container_width=True)
        
        st.markdown("---")
        
        # Bloco II: INFO (Sincronizado via subpasta md_files)
        # Normalização: "off-máquina" -> "OFF_MÁQUINA"
        file_name = active_tab.replace("-", "_").upper()
        info_path = os.path.join(PATH_MD, f"INFO_{file_name}.md")
        
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

    # --- 5. PALCO CENTRAL: ARTE (RAIZ DO PROJETO) ---
    # As artes residem na Main Page (raiz), conforme seu aviso
    img_name = active_tab.replace("-", "_") + ".jpg"
    
    # Busca direta na raiz
    if os.path.exists(img_name):
        st.image(img_name, use_container_width=True)
    else:
        # Fallback silencioso para não poluir o palco se o arquivo faltar
        st.write(f"", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    
