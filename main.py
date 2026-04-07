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
    # 1. PRIMEIRA INSTRUÇÃO: Configuração de Página
    try: 
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except: 
        pass

    # 2. LIMPEZA RADICAL (CSS): Remove Botão Share e destrava o Palco
    st.markdown("""
        <style>
            /* Esconde o Header do Streamlit/Google que contém o Share */
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            
            /* Trava a Sidebar em 300px e remove margens internas */
            [data-testid="stSidebar"] { width: 300px !important; min-width: 300px !important; }
            
            /* Garante que o palco central seja clicável e não tenha sobreposição */
            .main .block-container { 
                padding-top: 1rem !important; 
                max-width: 100% !important; 
            }
            
            /* Remove espaços fantasmas no topo */
            #root > div:nth-child(1) > div > div > div > div > section > div { padding-top: 0rem; }
        </style>
    """, unsafe_allow_html=True)
    
    # LISTA DE PÁGINAS (Nome-conceito: off-máquina)
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    
    if 'current_tab_idx' not in st.session_state: 
        st.session_state.current_tab_idx = 1

    # --- 1. LINHA ZERO (ABSOLUTA NO TOPO DIREITO) ---
    c_topo = st.columns([7, 3])
    with c_topo[1]:
        st.selectbox("Idioma", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # --- 2. MOTOR DE NAVEGAÇÃO (TAB BAR) ---
    # Captura imediata para forçar a atualização da Sidebar
    tab_id = stx.tab_bar(data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
                         default=tabs_list[st.session_state.current_tab_idx])
    
    # Se houve troca de aba, reinicia para atualizar INFO e ARTE
    if st.session_state.current_tab_idx != tabs_list.index(tab_id):
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    active_tab = tabs_list[st.session_state.current_tab_idx]

    # --- 3. SIDEBAR (IDENTIDADE + INFO SINCRONIZADA) ---
    with st.sidebar:
        if os.path.exists(PATH_LOGO):
            st.image(PATH_LOGO, use_container_width=True)
        
        st.markdown("---")
        
        # INFO Sincronizado
        file_name = active_tab.replace("-", "_").upper()
        info_path = os.path.join(PATH_MD, f"INFO_{file_name}.md")
        
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

    # --- 4. PALCO CENTRAL: ARTE ---
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
