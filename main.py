import streamlit as st
import extra_streamlit_components as stx
import os

# --- DIRETRIZES TÉCNICAS (BACKUP SALVADOR) ---
PATH_MD = r"md_files"
PATH_LOGO = "image_0.png"
BULB_ICON = "💡"
IDIOMAS_ABC = ["PT", "ES", "IT", "FR", "DE", "EN", "CA", "GL", "RO"]

def main():
    # Estética: Sidebar fixa em 300px
    st.markdown("<style>[data-testid='stSidebar'] { width: 300px !important; min-width: 300px !important; }</style>", unsafe_allow_html=True)
    
    # Controle de Estado de Navegação
    if 'current_tab_idx' not in st.session_state: 
        st.session_state.current_tab_idx = 1
    
    tabs_list = ["mini", "ypoemas", "eureka", "off", "books", "comments", "about"]
    
    try: 
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except: 
        pass

    # --- 1. LINHA ZERO (HEADER SUPERIOR EXTERNO) ---
    c_topo = st.columns([8, 2])
    with c_topo[1]:
        st.selectbox("Idiomas ABC", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # --- 2. SIDEBAR (FOCO: IDENTIDADE + TEXTO DE CONTEXTO) ---
    active_tab = tabs_list[st.session_state.current_tab_idx]
    
    with st.sidebar:
        # Bloco I: Identidade
        col_id1, col_id2 = st.columns([1, 3])
        col_id1.markdown(f"## {BULB_ICON}")
        if os.path.exists(PATH_LOGO):
            col_id2.image(PATH_LOGO, width=120)
        
        st.markdown("---")
        
        # Bloco II: O Texto da Página (INFO)
        # Este é o texto que explica o que a página faz
        info_path = os.path.join(PATH_MD, f"INFO_{active_tab.upper()}.md")
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

    # --- 3. PALCO CENTRAL (ESTÉTICA & ARTE) ---
    # TabBar para navegação entre módulos
    tab_id = stx.tab_bar(data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
                         default=tabs_list[st.session_state.current_tab_idx])
    
    # Sincronização de índice
    st.session_state.current_tab_idx = tabs_list.index(tab_id)

    # A ARTE DA PÁGINA (Aparece no topo do palco)
    img_path = os.path.join(PATH_MD, f"{tab_id}.jpg")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)

if __name__ == "__main__":
    main()
