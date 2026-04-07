import streamlit as st
import extra_streamlit_components as stx
import os

# --- DIRETRIZES TÉCNICAS (ESTRUTURA RAIZ /ypo) ---
PATH_MD = "md_files"
PATH_LOGO = "image_0.png"

IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    # 1. SETUP DE PÁGINA (ESTRITO)
    try:
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except:
        pass

    # CSS: Limpeza e Proteção da Sidebar (300px)
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { width: 300px !important; min-width: 300px !important; }
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            .block-container { padding-top: 0rem !important; }
            /* Ajuste fino para a Linha Zero não empurrar as Tabs */
            div[data-testid="stVerticalBlock"] > div:first-child { margin-top: -3.8rem; }
        </style>
    """, unsafe_allow_html=True)

    # Nomes-conceito das páginas
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    
    if 'current_tab_idx' not in st.session_state:
        st.session_state.current_tab_idx = 1

    # --- 1. LINHA ZERO (HEADER SUPERIOR DIREITO) ---
    c_topo = st.columns([7, 3])
    with c_topo[1]:
        st.selectbox("Idioma", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # --- 2. MOTOR DE NAVEGAÇÃO (ÂNCORA DO PALCO) ---
    # Colocamos as Tabs dentro de um placeholder para garantir precedência
    tab_placeholder = st.empty()
    with tab_placeholder:
        tab_id = stx.tab_bar(data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
                             default=tabs_list[st.session_state.current_tab_idx])
    
    # Sincronização: Se o clique aconteceu, recomeça o script ANTES de desenhar a imagem
    if st.session_state.current_tab_idx != tabs_list.index(tab_id):
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    active_tab = tabs_list[st.session_state.current_tab_idx]

    # --- 3. SIDEBAR (IDENTIDADE + INFO) ---
    with st.sidebar:
        # O LOGOTIPO/DESENHO deve residir apenas aqui
        if os.path.exists(PATH_LOGO):
            st.image(PATH_LOGO, use_container_width=True)
        
        st.markdown("---")
        
        # INFO Sincronizado (Markdown)
        file_name = active_tab.replace("-", "_").upper()
        info_path = os.path.join(PATH_MD, f"INFO_{file_name}.md")
        
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

    # --- 4. PALCO CENTRAL (ARTE SINCRONIZADA) ---
    # Mapeamento para os arquivos JPG na raiz
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
    
    # Renderiza a arte abaixo da TabBar. Se o arquivo não existe, o palco fica limpo para o conteúdo.
    if img_file and os.path.exists(img_file):
        st.image(img_file, use_container_width=True)

    # Conteúdo Específico
    if active_tab == "comments":
        comm_path = os.path.join(PATH_MD, "COMMENTS.md")
        if os.path.exists(comm_path):
            with open(comm_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

if __name__ == "__main__":
    main()
