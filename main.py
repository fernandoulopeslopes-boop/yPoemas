import streamlit as st
import extra_streamlit_components as stx
import os

# --- DIRETRIZES TÉCNICAS (BACKUP SALVADOR) ---
PATH_MD = r"md_files"
PATH_LOGO = "image_0.png"

IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    # 1. CONFIGURAÇÃO INICIAL (Obrigatória no topo)
    try: 
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except: 
        pass

    # 2. LIMPEZA DE INTERFACE (CSS)
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { width: 300px !important; min-width: 300px !important; }
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            .block-container { padding-top: 0rem !important; }
            /* Remove o espaço que a lista de idiomas ocuparia se estivesse no palco */
            [data-testid="stVerticalBlock"] > div:first-child { margin-top: -3rem; }
        </style>
    """, unsafe_allow_html=True)
    
    # Nome-conceito: off-máquina
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    
    if 'current_tab_idx' not in st.session_state: 
        st.session_state.current_tab_idx = 1

    # --- 3. LINHA ZERO (HEADER) ---
    # Renderizamos o seletor em colunas para forçar o posicionamento no topo
    c_topo = st.columns([7, 3])
    with c_topo[1]:
        st.selectbox("Idioma", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # --- 4. MOTOR DE NAVEGAÇÃO ---
    # Captura a tab ANTES de desenhar a Sidebar
    tab_id = stx.tab_bar(data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
                         default=tabs_list[st.session_state.current_tab_idx])
    
    # Gatilho de Sincronia
    if st.session_state.current_tab_idx != tabs_list.index(tab_id):
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    active_tab = tabs_list[st.session_state.current_tab_idx]

    # --- 5. SIDEBAR (PREENCHIMENTO OBRIGATÓRIO) ---
    with st.sidebar:
        # Bloco I: Identidade
        if os.path.exists(PATH_LOGO):
            st.image(PATH_LOGO, use_container_width=True)
        
        st.markdown("---")
        
        # Bloco II: INFO (Markdown do Contexto)
        file_name = active_tab.replace("-", "_").upper()
        info_path = os.path.join(PATH_MD, f"INFO_{file_name}.md")
        
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

    # --- 6. PALCO CENTRAL: ARTE ---
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
