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
    
    # 1. TRATAMENTO DE NAVEGAÇÃO
    tabs_list = ["mini", "ypoemas", "eureka", "off", "books", "comments", "about"]
    
    if 'current_tab_idx' not in st.session_state: 
        st.session_state.current_tab_idx = 1

    try: 
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except: 
        pass

    # --- 2. LINHA ZERO (LIMPA - SEM TEXTO/LABEL) ---
    c_topo = st.columns([8, 2])
    with c_topo[1]:
        st.selectbox("", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # --- 3. PALCO CENTRAL: TAB BAR ---
    tab_id = stx.tab_bar(data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
                         default=tabs_list[st.session_state.current_tab_idx])
    
    # Sincronização imediata para garantir que INFO e ARTE correspondam à TAB clicada
    if st.session_state.current_tab_idx != tabs_list.index(tab_id):
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    active_tab = tabs_list[st.session_state.current_tab_idx]

    # --- 4. SIDEBAR (IDENTIDADE + INFO SINCRONIZADA) ---
    with st.sidebar:
        # Bloco I: Identidade
        col_id1, col_id2 = st.columns([1, 3])
        col_id1.markdown(f"## {BULB_ICON}")
        if os.path.exists(PATH_LOGO):
            col_id2.image(PATH_LOGO, width=120)
        
        st.markdown("---")
        
        # Bloco II: INFO (O texto que explica a página selecionada no palco)
        info_path = os.path.join(PATH_MD, f"INFO_{active_tab.upper()}.md")
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

    # --- 5. PALCO CENTRAL: ARTE ---
    img_path = os.path.join(PATH_MD, f"{active_tab}.jpg")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)

if __name__ == "__main__":
    main()
