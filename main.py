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

# --- CONFIGURAÇÕES ---
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

    # 1. ESTADO E MAPA (ABOUT FIXO)
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    if 'current_tab_idx' not in st.session_state:
        st.session_state.current_tab_idx = 1
    
    active_tab = tabs_list[st.session_state.current_tab_idx]

    map_assets = {
        "mini": {"img": "img_mini.jpg", "md": "INFO_MINI.md"},
        "ypoemas": {"img": "img_ypoemas.jpg", "md": "INFO_YPOEMAS.md"},
        "eureka": {"img": "img_eureka.jpg", "md": "INFO_EUREKA.md"},
        "off-máquina": {"img": "img_off-machina.jpg", "md": "ABOUT_OFF-MACHINA.md"},
        "books": {"img": "img_books.jpg", "md": "INFO_BOOKS.md"},
        "comments": {"img": "img_poly.jpg", "md": "ABOUT_COMMENTS.md"},
        "about": {"img": "img_about.jpg", "md": "INFO_ABOUT.md"}
    }

    # 2. SIDEBAR (CONTROLE E IDENTIDADE)
    with st.sidebar:
        st.write("### Idioma")
        sel_idioma = st.selectbox("Selecione", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")
        st.markdown("---")

        # Texto Informativo (MEIO)
        asset = map_assets.get(active_tab)
        info_path = os.path.join(PATH_MD, asset["md"])
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), sel_idioma))
        
        # Logo da Página (BASE - ÚNICO LUGAR)
        st.markdown("<br>" * 10, unsafe_allow_html=True)
        st.markdown("---")
        if os.path.exists(asset["img"]):
            st.image(asset["img"], use_container_width=True)

    # 3. PALCO (LIMPEZA E BOTÕES)
    st.markdown("""
        <style>
            header {visibility: hidden;}
            .block-container {padding-top: 1rem !important;}
            /* Ajuste para botões de navegação não encavalarem */
            div.stButton > button {
                width: 40px !important;
                height: 40px !important;
                padding: 0px !important;
                font-weight: bold !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # MOTOR DE ABAS
    tab_id = stx.tab_bar(
        data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
        default=active_tab,
        key="motor_ypo_v7"
    )

    # NAV BOTÕES (Alinhamento Horizontal Compacto)
    c_nav = st.container()
    col1, col2, col3, col4, col5, _ = c_nav.columns([0.6, 0.6, 0.6, 0.6, 0.6, 12])
    
    with col1:
        if st.button("+"): pass
    with col2:
        if st.button("<"):
            st.session_state.current_tab_idx = (st.session_state.current_tab_idx - 1) % len(tabs_list)
            st.rerun()
    with col3:
        if st.button("*"):
            st.session_state.current_tab_idx = 1
            st.rerun()
    with col4:
        if st.button(">"):
            st.session_state.current_tab_idx = (st.session_state.current_tab_idx + 1) % len(tabs_list)
            st.rerun()
    with col5:
        if st.button("?"): pass

    # Sincronia TabBar -> Estado
    if tab_id != active_tab:
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    # CONTEÚDO DO PALCO (SEM IMAGEM REPETIDA)
    st.markdown("---")
    
    # Se houver conteúdo específico (COMMENTS ou outros MDs de palco), mostra aqui.
    # Caso contrário, o palco permanece limpo/minimalista.
    if active_tab == "comments":
        c_path = os.path.join(PATH_MD, "COMMENTS.md")
        if os.path.exists(c_path):
            with open(c_path, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), sel_idioma))
    elif active_tab == "ypoemas":
        # Espaço reservado para a "Machina" de poemas futura
        st.info("Aguardando motor de poesia...")

if __name__ == "__main__":
    main()
