import streamlit as st
import extra_streamlit_components as stx
import os

# --- PARADIGMA DE INTERFACE (ESTRUTURA RAIZ /ypo) ---
PATH_MD = "md_files"
PATH_LOGO = "image_0.png"

IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    # 1. ÂNCORA INICIAL: Configuração de Página
    try:
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except:
        pass

    # 2. INJEÇÃO DE CSS: Blindagem da Sidebar e Limpeza de Palco
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { width: 300px !important; min-width: 300px !important; }
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            .block-container { padding-top: 1rem !important; }
            /* Garante que o seletor de idiomas (Linha Zero) não bloqueie o menu */
            [data-testid="stVerticalBlock"] > div:first-child { z-index: 99; }
        </style>
    """, unsafe_allow_html=True)

    # 3. DEFINIÇÃO DE CONCEITOS
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    
    if 'current_tab_idx' not in st.session_state:
        st.session_state.current_tab_idx = 1

    # --- 4. INTERFACE: LINHA ZERO (HEADER) ---
    c_topo = st.columns([7, 3])
    with c_topo[1]:
        st.selectbox("Idioma", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # --- 5. INTERFACE: MOTOR DE NAVEGAÇÃO (PALCO) ---
    # Usando st.container para garantir que o iframe do stx tenha seu próprio espaço
    with st.container():
        tab_id = stx.tab_bar(
            data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
            default=tabs_list[st.session_state.current_tab_idx],
            key="motor_machina"
        )
    
    # Sincronização de Estado (Coração do Paradigma)
    if st.session_state.current_tab_idx != tabs_list.index(tab_id):
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    active_tab = tabs_list[st.session_state.current_tab_idx]

    # --- 6. INTERFACE: SIDEBAR (IDENTIDADE + INFO) ---
    with st.sidebar:
        # Identidade Visual (Logo fixo na raiz)
        if os.path.exists(PATH_LOGO):
            st.image(PATH_LOGO, use_container_width=True)
        
        st.markdown("---")
        
        # Bloco INFO Sincronizado
        file_name = active_tab.replace("-", "_").upper()
        info_path = os.path.join(PATH_MD, f"INFO_{file_name}.md")
        
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

    # --- 7. INTERFACE: PALCO CENTRAL (ARTE E CONTEÚDO) ---
    # Mapeamento estrito para os arquivos na raiz /ypo
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
    
    # Renderização da Arte: Só acontece DEPOIS de processar o estado da aba
    if img_file and os.path.exists(img_file):
        st.image(img_file, use_container_width=True)

    # Conteúdo de Comments
    if active_tab == "comments":
        comm_path = os.path.join(PATH_MD, "COMMENTS.md")
        if os.path.exists(comm_path):
            with open(comm_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

if __name__ == "__main__":
    main()
