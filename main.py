import streamlit as st
import extra_streamlit_components as stx
import os

# --- CONFIGURAÇÃO DE INFRAESTRUTURA ---
PATH_MD = "md_files"
PATH_LOGO = "image_0.png"

IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    # 1. CABEÇA (Configuração inicial)
    try:
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except:
        pass

    # 2. ESTADO (Lógica de Navegação)
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    if 'current_tab_idx' not in st.session_state:
        st.session_state.current_tab_idx = 1
    
    active_tab = tabs_list[st.session_state.current_tab_idx]

    # 3. ESQUERDA (SIDEBAR) - Declarada primeiro para garantir o espaço
    with st.sidebar:
        # Identidade
        if os.path.exists(PATH_LOGO):
            st.image(PATH_LOGO, use_container_width=True)
        
        st.markdown("---")
        
        # INFO Sincronizado (Busca o arquivo MD correspondente)
        file_name = active_tab.replace("-", "_").upper()
        info_path = os.path.join(PATH_MD, f"INFO_{file_name}.md")
        
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.markdown(f"### {active_tab.upper()}")

    # 4. DIREITA (PALCO) - De cima para baixo
    
    # CSS: Limpeza de Header e travamento de Sidebar (300px)
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { width: 300px !important; min-width: 300px !important; }
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            .block-container { padding-top: 1rem !important; }
        </style>
    """, unsafe_allow_html=True)

    # LINHA ZERO: Idiomas (Topo do Palco)
    c_idiomas = st.container()
    with c_idiomas:
        col_espaco, col_sel = st.columns([7, 3])
        with col_sel:
            st.selectbox("Idioma", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # MOTOR: Navegação (Logo abaixo dos idiomas)
    c_navegacao = st.container()
    with c_navegacao:
        tab_id = stx.tab_bar(
            data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
            default=tabs_list[st.session_state.current_tab_idx],
            key="motor_machina_final"
        )
    
    # Sincronia de clique: Se mudar, rerun para atualizar o script de cima para baixo
    if st.session_state.current_tab_idx != tabs_list.index(tab_id):
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    # ARTE: O último elemento (Base do Palco)
    img_map = {
        "mini": "img_mini.jpg",
        "ypoemas": "img_ypoemas.jpg",
        "eureka": "img_eureka.jpg",
        "off-máquina": "img_off-machina.jpg",
        "books": "img_books.jpg",
        "about": "img_about.jpg",
        "comments": "img_poly.jpg"
    }
    
    img_file = img_map.get(active_tab)
    if img_file and os.path.exists(img_file):
        st.image(img_file, use_container_width=True)

    # Conteúdo Específico (Comments)
    if active_tab == "comments":
        comm_path = os.path.join(PATH_MD, "COMMENTS.md")
        if os.path.exists(comm_path):
            with open(comm_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

if __name__ == "__main__":
    main()
