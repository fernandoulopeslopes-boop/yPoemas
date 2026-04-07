import streamlit as st
import extra_streamlit_components as stx
import os

# --- ARQUITETURA DE DADOS (RAIZ /ypo) ---
PATH_MD = "md_files"
PATH_LOGO = "image_0.png"
IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    # 1. ÂNCORA DE INFRAESTRUTURA (CIMA PARA BAIXO)
    try:
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except:
        pass

    # 2. ESTADO (LÓGICA ANTES DA INTERFACE)
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    if 'current_tab_idx' not in st.session_state:
        st.session_state.current_tab_idx = 1
    
    active_tab = tabs_list[st.session_state.current_tab_idx]

    # 3. INTERFACE: ESQUERDA (SIDEBAR)
    # Declarada primeiro para garantir que o Streamlit reserve o frame lateral.
    with st.sidebar:
        # Identidade Visual (O Desenho/Logo confinado aqui)
        if os.path.exists(PATH_LOGO):
            st.image(PATH_LOGO, use_container_width=True)
        
        st.markdown("---")
        
        # Bloco INFO Sincronizado
        file_name = active_tab.replace("-", "_").upper()
        info_path = os.path.join(PATH_MD, f"INFO_{file_name}.md")
        
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.markdown(f"**{active_tab.upper()}**")

    # 4. INTERFACE: DIREITA (PALCO)
    # CSS de blindagem para evitar que a imagem "suba" ou a sidebar suma.
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { width: 300px !important; min-width: 300px !important; }
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            .main .block-container { padding-top: 1rem !important; }
            /* Prevenção de sobreposição do seletor de idiomas */
            div[data-testid="stVerticalBlock"] > div:first-child { z-index: 100; }
        </style>
    """, unsafe_allow_html=True)

    # PALCO: LINHA ZERO (IDIOMAS)
    # Topo absoluto do palco central.
    _, col_lang = st.columns([7, 3])
    with col_lang:
        st.selectbox("Idioma", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # PALCO: MOTOR DE NAVEGAÇÃO (TABS)
    # Posicionado entre os idiomas e a arte.
    tab_id = stx.tab_bar(
        data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
        default=tabs_list[st.session_state.current_tab_idx],
        key="motor_machina_final"
    )
    
    # Gatilho de Sincronia: Se mudar, recomeça a leitura sequencial.
    if st.session_state.current_tab_idx != tabs_list.index(tab_id):
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    # PALCO: ARTE (BASE)
    # Renderizada por último para nunca cobrir os controles superiores.
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

    # PALCO: CONTEÚDO EXTRA (COMMENTS)
    if active_tab == "comments":
        comm_path = os.path.join(PATH_MD, "COMMENTS.md")
        if os.path.exists(comm_path):
            with open(comm_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

if __name__ == "__main__":
    main()
