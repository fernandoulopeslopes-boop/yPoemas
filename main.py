import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os

# --- MOTOR DE TRADUÇÃO ---
@st.cache_data
def traduzir_texto(texto, destino_nome):
    if not texto or "Português" in destino_nome: 
        return texto
    try:
        codigos = {
            "PT - Português": "pt", "ES - Español": "es", "IT - Italiano": "it",
            "FR - Français": "fr", "DE - Deutsch": "de", "EN - English": "en",
            "CA - Català": "ca", "GL - Galego": "gl", "RO - Română": "ro"
        }
        target = codigos.get(destino_nome, 'en')
        return GoogleTranslator(source='auto', target=target).translate(texto)
    except:
        return texto

# --- CONFIGURAÇÕES DE DIRETÓRIO ---
PATH_MD = "md_files"
ICON_YPO = "icon_ypo.ico"
IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    st.set_page_config(
        layout="wide", 
        page_title="yPoemas", 
        page_icon=ICON_YPO if os.path.exists(ICON_YPO) else "🎭"
    )

    # ESTADO
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    if 'current_tab_idx' not in st.session_state:
        st.session_state.current_tab_idx = 1
    
    active_tab = tabs_list[st.session_state.current_tab_idx]

    # MAPEAMENTO DE ATIVOS (CORREÇÃO DE NOMES ABOUT)
    map_assets = {
        "mini": {"img": "img_mini.jpg", "md": "INFO_MINI.md"},
        "ypoemas": {"img": "img_ypoemas.jpg", "md": "INFO_YPOEMAS.md"},
        "eureka": {"img": "img_eureka.jpg", "md": "INFO_EUREKA.md"},
        "off-máquina": {"img": "img_off-machina.jpg", "md": "ABOUT_OFF-MACHINA.md"},
        "books": {"img": "img_books.jpg", "md": "INFO_BOOKS.md"},
        "comments": {"img": "img_poly.jpg", "md": "ABOUT_COMMENTS.md"},
        "about": {"img": "img_about.jpg", "md": "INFO_ABOUT.md"}
    }

    # --- 1. SIDEBAR (ESQUERDA) ---
    with st.sidebar:
        # TOPO
        st.write("### Idioma")
        sel_idioma = st.selectbox("Selecione", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")
        st.markdown("---")

        # MEIO
        asset = map_assets.get(active_tab)
        info_path = os.path.join(PATH_MD, asset["md"])
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), sel_idioma))
        
        # BASE (Logo da Seção)
        st.markdown("<br>" * 10, unsafe_allow_html=True)
        st.markdown("---")
        if os.path.exists(asset["img"]):
            st.image(asset["img"], use_container_width=True)

    # --- 2. PALCO (DIREITA) ---
    st.markdown("""<style>header {visibility: hidden;} .block-container {padding-top: 1rem !important;}</style>""", unsafe_allow_html=True)

    # MOTOR DE ABAS
    tab_id = stx.tab_bar(
        data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
        default=active_tab,
        key="motor_ypo_v6"
    )

    # BOTÕES DE NAVEGAÇÃO ESPECÍFICOS: + < * > ?
    col1, col2, col3, col4, col5, _ = st.columns([0.5, 0.5, 0.5, 0.5, 0.5, 8])
    
    with col1:
        if st.button("+"): # Exemplo: Novo/Ação
            pass
    with col2:
        if st.button("<"): # Anterior
            st.session_state.current_tab_idx = (st.session_state.current_tab_idx - 1) % len(tabs_list)
            st.rerun()
    with col3:
        if st.button("*"): # Home/Reset
            st.session_state.current_tab_idx = 1 # ypoemas
            st.rerun()
    with col4:
        if st.button(">"): # Próxima
            st.session_state.current_tab_idx = (st.session_state.current_tab_idx + 1) % len(tabs_list)
            st.rerun()
    with col5:
        if st.button("?"): # Ajuda/Info
            pass

    # Sincronia motor -> estado
    if tab_id != active_tab:
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    # CONTEÚDO DO PALCO
    if active_tab == "comments":
        c_path = os.path.join(PATH_MD, "COMMENTS.md")
        if os.path.exists(c_path):
            with open(c_path, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), sel_idioma))
    else:
        if os.path.exists(asset["img"]):
            st.image(asset["img"], use_container_width=True)

if __name__ == "__main__":
    main()
