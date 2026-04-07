import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os

# --- MOTOR DE TRADUÇÃO COM CACHE (EFICIÊNCIA) ---
@st.cache_data
def traduzir_texto(texto, destino='pt'):
    if not texto or destino == 'pt': 
        return texto
    try:
        # Mapeamento simples de códigos para o GoogleTranslator
        codigos = {
            "PT - Português": "pt", "ES - Español": "es", "IT - Italiano": "it",
            "FR - Français": "fr", "DE - Deutsch": "de", "EN - English": "en",
            "CA - Català": "ca", "GL - Galego": "gl", "RO - Română": "ro"
        }
        target = codigos.get(destino, 'en')
        return GoogleTranslator(source='auto', target=target).translate(texto)
    except:
        return texto

# --- CONFIGURAÇÕES DE RAIZ ---
PATH_MD = "md_files"
PATH_LOGO = "image_0.png"
ICON_YPO = "icon_ypo.ico"

IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    # 1. ÂNCORA DE IDENTIDADE (O SELO NO TOPO)
    st.set_page_config(
        layout="wide", 
        page_title="yPoemas", 
        page_icon=ICON_YPO if os.path.exists(ICON_YPO) else "🎭"
    )

    # 2. ESTADO E CONCEITOS
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    if 'current_tab_idx' not in st.session_state:
        st.session_state.current_tab_idx = 1
    
    # 3. SIDEBAR (A ESQUERDA - PRIMEIRO FOCO)
    with st.sidebar:
        if os.path.exists(PATH_LOGO):
            st.image(PATH_LOGO, use_container_width=True)
        
        st.markdown("---")
        
        # LINHA ZERO: Seletor de Idiomas (Suporte)
        sel_idioma = st.selectbox("Idioma / Language", IDIOMAS_ABC, key="lang_sel")
        
        st.markdown("---")
        
        # INFO Sincronizado e Traduzido
        active_tab = tabs_list[st.session_state.current_tab_idx]
        file_name = active_tab.replace("-", "_").upper()
        info_path = os.path.join(PATH_MD, f"INFO_{file_name}.md")
        
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                conteudo_info = f.read()
                st.markdown(traduzir_texto(conteudo_info, sel_idioma))

    # 4. PALCO (A DIREITA - HIERARQUIA DE RENDERIZAÇÃO)
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { width: 300px !important; min-width: 300px !important; }
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            .block-container { padding-top: 0rem !important; }
            .stTabs [data-baseweb="tab-list"] { gap: 10px; }
        </style>
    """, unsafe_allow_html=True)

    # MOTOR DE NAVEGAÇÃO (Topo do Palco)
    c_navegacao = st.container()
    with c_navegacao:
        tab_id = stx.tab_bar(
            data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
            default=tabs_list[st.session_state.current_tab_idx],
            key="motor_ypo_v_final"
        )
    
    # Sincronização de Clique
    if st.session_state.current_tab_idx != tabs_list.index(tab_id):
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    # ESPAÇO DA ARTE E CONTEÚDO (Base do Palco)
    c_arte = st.container()
    with c_arte:
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

        # Se for COMMENTS, carrega o texto traduzido abaixo da arte
        if active_tab == "comments":
            comm_path = os.path.join(PATH_MD, "COMMENTS.md")
            if os.path.exists(comm_path):
                with open(comm_path, "r", encoding="utf-8") as f:
                    st.markdown("---")
                    st.markdown(traduzir_texto(f.read(), sel_idioma))

if __name__ == "__main__":
    main()
