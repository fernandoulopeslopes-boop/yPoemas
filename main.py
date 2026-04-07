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

    # ESTADO
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    if 'current_tab_idx' not in st.session_state:
        st.session_state.current_tab_idx = 1
    
    active_tab = tabs_list[st.session_state.current_tab_idx]

    # Mapeamento de Ativos (Garante que off-máquina aponte para os arquivos certos)
    map_assets = {
        "mini": {"img": "img_mini.jpg", "md": "INFO_MINI.md"},
        "ypoemas": {"img": "img_ypoemas.jpg", "md": "INFO_YPOEMAS.md"},
        "eureka": {"img": "img_eureka.jpg", "md": "INFO_EUREKA.md"},
        "off-máquina": {"img": "img_off-machina.jpg", "md": "INFO_OFF_MACHINA.md"},
        "books": {"img": "img_books.jpg", "md": "INFO_BOOKS.md"},
        "comments": {"img": "img_poly.jpg", "md": "INFO_COMMENTS.md"},
        "about": {"img": "img_about.jpg", "md": "INFO_ABOUT.md"}
    }

    # --- 1. SIDEBAR (ESQUERDA) ---
    with st.sidebar:
        # A - TOPO: Idiomas
        st.write("### Idioma")
        sel_idioma = st.selectbox("Selecione", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")
        st.markdown("---")

        # B - MEIO: Texto Informativo (Tratamento para nomes com hífen)
        info_file = map_assets[active_tab]["md"]
        info_path = os.path.join(PATH_MD, info_file)
        
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), sel_idioma))
        else:
            st.caption(f"(Arquivo {info_file} não detectado)")

        # C - BASE: Logo da Página Selecionada
        st.markdown("<br>" * 10, unsafe_allow_html=True) # Empurra para o final
        st.markdown("---")
        logo_path = map_assets[active_tab]["img"]
        if os.path.exists(logo_path):
            st.image(logo_path, caption=f"Identidade: {active_tab}", use_container_width=True)

    # --- 2. PALCO (DIREITA) ---
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { visibility: hidden; }
            .block-container { padding-top: 1rem !important; }
        </style>
    """, unsafe_allow_html=True)

    # MOTOR DE ABAS
    tab_id = stx.tab_bar(
        data=[stx.TabBarItemData(id=t, title=t, description="") for t in tabs_list], 
        default=active_tab,
        key="motor_ypo_v4"
    )
    
    # BOTÕES DE NAVEGAÇÃO (Logo abaixo das abas)
    col_prev, col_next, _ = st.columns([1, 1, 8])
    with col_prev:
        if st.button("← Anterior"):
            st.session_state.current_tab_idx = (st.session_state.current_tab_idx - 1) % len(tabs_list)
            st.rerun()
    with col_next:
        if st.button("Próxima →"):
            st.session_state.current_tab_idx = (st.session_state.current_tab_idx + 1) % len(tabs_list)
            st.rerun()

    # Sincronização do Motor stx com o Estado
    if tab_id != active_tab:
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    # ARTE DO PALCO (Centro das Atenções)
    arte_path = map_assets[active_tab]["img"]
    if os.path.exists(arte_path):
        st.image(arte_path, use_container_width=True)

    # CONTEÚDO EXTRA (Exclusivo para Comments ou Books se houver MD adicional)
    if active_tab == "comments":
        extra_path = os.path.join(PATH_MD, "COMMENTS.md")
        if os.path.exists(extra_path):
            with open(extra_path, "r", encoding="utf-8") as f:
                st.markdown("---")
                st.markdown(traduzir_texto(f.read(), sel_idioma))

if __name__ == "__main__":
    main()
