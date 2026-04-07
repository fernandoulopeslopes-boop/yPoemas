import streamlit as st
import extra_streamlit_components as stx
import random
import os

# --- CONFIGURAÇÕES E DIRETRIZES ---
PATH_DATA = r"data"
PATH_MD = r"md_files"
PATH_BASE = r"base"
PATH_LOGO = "image_0.png"
BULB_ICON = "💡"

# LINHA ZERO: IDIOMAS ABC (Consolidados)
IDIOMAS_ABC = ["PT", "ES", "IT", "FR", "DE", "EN", "CA", "GL", "RO"]

def main():
    # Sidebar travada em 300px conforme combinado
    st.markdown("<style>[data-testid='stSidebar'] { width: 300px !important; min-width: 300px !important; }</style>", unsafe_allow_html=True)
    
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 1
    
    tabs_list = ["mini", "ypoemas", "eureka", "off", "books", "comments", "about"]
    active_tab = tabs_list[st.session_state.current_tab_idx]

    try: st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except: pass

    # --- LINHA ZERO: HEADER SUPERIOR ---
    c_zero = st.columns([8, 2])
    with c_zero[1]:
        st.selectbox("Idiomas ABC", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # --- SIDEBAR: FOCO TOTAL (IDENTIDADE + INFO) ---
    with st.sidebar:
        # BLOCO I: IDENTIDADE
        col_id1, col_id2 = st.columns([1, 3])
        col_id1.markdown(f"## {BULB_ICON}") # Lâmpada de Bulbo Amarela
        if os.path.exists(PATH_LOGO):
            col_id2.image(PATH_LOGO, width=120) # Logo image_0.png
        
        st.markdown("---")
        
        # BLOCO II: O ESPAÇO DO INFO (Texto explicativo da página)
        # O texto que explica o quê a página selecionada no palco faz
        info_path = os.path.join(PATH_MD, f"INFO_{active_tab.upper()}.md")
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        
        # Espaçador para empurrar a navegação para a base
        st.markdown("<br>" * 10, unsafe_allow_html=True)
        st.markdown("---")
        
        # BLOCO III: NAVEGAÇÃO CR (NA BASE)
        cn1, cn2 = st.columns(2)
        if cn1.button("« Anterior"): 
            st.session_state.current_tab_idx = (st.session_state.current_tab_idx - 1) % len(tabs_list)
            st.rerun()
        if cn2.button("Próxima »"): 
            st.session_state.current_tab_idx = (st.session_state.current_tab_idx + 1) % len(tabs_list)
            st.rerun()

    # --- PALCO CENTRAL (SEM ALTERAÇÕES DE LÓGICA OU COMPONENTES) ---
    tab_id = stx.tab_bar(data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
                         default=tabs_list[st.session_state.current_tab_idx])
    st.session_state.current_tab_idx = tabs_list.index(tab_id)

    # Conteúdo do palco permanece conforme estava
    img_path = os.path.join(PATH_MD, f"{tab_id}.jpg")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)

if __name__ == "__main__":
    main()
