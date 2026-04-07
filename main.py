import streamlit as st
import extra_streamlit_components as stx
import os

# --- DIRETRIZES TÉCNICAS (BACKUP SALVADOR) ---
PATH_MD = r"md_files"
PATH_LOGO = "image_0.png"

# LINHA ZERO: Sigla - Nome (ABC Ocidental)
IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    # 1. ORDEM SAGRADA: Configuração de página antes de qualquer widget
    try: 
        st.set_page_config(layout="wide", page_title="yPoemas", page_icon="icon_ypo.ico")
    except: 
        pass

    # CSS PARA FORÇAR POSICIONAMENTO E CORREÇÃO DO PALCO:
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { width: 300px !important; min-width: 300px !important; }
            
            /* Remove o espaço em branco superior e margens do bloco principal */
            .block-container { padding-top: 0rem !important; margin-top: -20px; }
            
            /* Tenta injetar o seletor no header do Streamlit via seletor de classe */
            [data-testid="stHeader"] { 
                background: rgba(0,0,0,0); 
                display: flex; 
                justify-content: flex-end;
                padding-right: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # LISTA DE PÁGINAS (Conceito: off-máquina)
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    
    if 'current_tab_idx' not in st.session_state: 
        st.session_state.current_tab_idx = 1

    # --- 2. LINHA ZERO (SELECTOR DE IDIOMAS) ---
    # Usando st.sidebar para retirar o seletor do palco, mas no topo da sidebar
    # Se o seletor for para o palco, ele rouba o foco da arte.
    with st.container():
        _, c_idiomas = st.columns([8, 2])
        with c_idiomas:
            st.selectbox("", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")

    # --- 3. PALCO CENTRAL: MOTOR DE NAVEGAÇÃO ---
    tab_id = stx.tab_bar(data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
                         default=tabs_list[st.session_state.current_tab_idx])
    
    # Sincronização imediata para atualizar o contexto (INFO e ARTE)
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
        
        # Bloco II: INFO (Markdown sincronizado)
        # Normalização rigorosa: "off-máquina" vira "OFF_MÁQUINA"
        file_name = active_tab.replace("-", "_").upper()
        info_path = os.path.join(PATH_MD, f"INFO_{file_name}.md")
        
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

    # --- 5. PALCO CENTRAL: ARTE DA PÁGINA ---
    # A imagem deve aparecer IMEDIATAMENTE abaixo da TabBar.
    # Verificação de nome de arquivo: off-máquina -> off_máquina.jpg
    img_name = active_tab.replace("-", "_") + ".jpg"
    img_path = os.path.join(PATH_MD, img_name)
    
    # Forçar a exibição da arte
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        # Fallback de busca caso o nome no OS use outra codificação
        st.warning(f"Arte não encontrada: {img_name}")

if __name__ == "__main__":
    main()
