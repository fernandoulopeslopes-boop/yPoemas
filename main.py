import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os

# --- MOTOR DE TRADUÇÃO (ESTABILIDADE E CACHE) ---
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

# --- CONFIGURAÇÕES DE AMBIENTE ---
PATH_MD = "md_files"
ICON_YPO = "icon_ypo.ico"
IDIOMAS_ABC = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]

def main():
    # 1. IDENTIDADE DO NAVEGADOR (SELO)
    st.set_page_config(
        layout="wide", 
        page_title="yPoemas", 
        page_icon=ICON_YPO if os.path.exists(ICON_YPO) else "🎭"
    )

    # 2. GESTÃO DE ESTADO E ATIVOS
    tabs_list = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    if 'current_tab_idx' not in st.session_state:
        st.session_state.current_tab_idx = 1 # Inicia em ypoemas
    
    active_tab = tabs_list[st.session_state.current_tab_idx]

    # Mapeamento Estrito de Arquivos (Conceito -> Físico)
    map_assets = {
        "mini": {"img": "img_mini.jpg", "md": "INFO_MINI.md"},
        "ypoemas": {"img": "img_ypoemas.jpg", "md": "INFO_YPOEMAS.md"},
        "eureka": {"img": "img_eureka.jpg", "md": "INFO_EUREKA.md"},
        "off-máquina": {"img": "img_off-machina.jpg", "md": "ABOUT_OFF-MACHINA.md"},
        "books": {"img": "img_books.jpg", "md": "INFO_BOOKS.md"},
        "comments": {"img": "img_poly.jpg", "md": "ABOUT_COMMENTS.md"},
        "about": {"img": "img_about.jpg", "md": "INFO_ABOUT.md"}
    }

    # --- 3. SIDEBAR (CONTROLE -> INFO -> IDENTIDADE) ---
    with st.sidebar:
        # TOPO: Idiomas (Prioridade Zero)
        st.write("### 🌐 Idioma")
        sel_idioma = st.selectbox("Seletor", IDIOMAS_ABC, label_visibility="collapsed", key="lang_sel")
        st.markdown("---")

        # MEIO: Texto "Sobre a Página" (Tratamento de tradução)
        asset = map_assets.get(active_tab)
        info_path = os.path.join(PATH_MD, asset["md"])
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                conteudo_raw = f.read()
                st.markdown(traduzir_texto(conteudo_raw, sel_idioma))
        
        # BASE: Logo da Seção (Âncora Visual)
        # Espaçador dinâmico para garantir que o logo "caia" para o fundo
        st.markdown("<div style='height: 20vh;'></div>", unsafe_allow_html=True)
        st.markdown("---")
        if os.path.exists(asset["img"]):
            st.image(asset["img"], use_container_width=True)

    # --- 4. PALCO (NAVEGAÇÃO E CONTEÚDO) ---
    st.markdown("""
        <style>
            header {visibility: hidden;}
            .block-container {padding-top: 1rem !important;}
            /* Design dos Botões de Navegação (Circulares e Alinhados) */
            .stButton > button {
                border-radius: 50% !important;
                width: 42px !important;
                height: 42px !important;
                padding: 0px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                font-size: 18px !important;
                border: 1px solid #eee !important;
                background-color: transparent !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # MOTOR DE ABAS (stx)
    tab_id = stx.tab_bar(
        data=[stx.TabBarItemData(id=t, title=t.upper(), description="") for t in tabs_list], 
        default=active_tab,
        key="machina_v9_stable"
    )

    # BARRA DE NAVEGAÇÃO COMPACTA (+ < * > ?)
    c_nav = st.container()
    with c_nav:
        col_buttons = st.columns([0.6, 0.6, 0.6, 0.6, 0.6, 10])
        with col_buttons[0]:
            if st.button("➕"): pass
        with col_buttons[1]:
            if st.button("⬅️"):
                st.session_state.current_tab_idx = (st.session_state.current_tab_idx - 1) % len(tabs_list)
                st.rerun()
        with col_buttons[2]:
            if st.button("🏠"):
                st.session_state.current_tab_idx = 1 # Volta para ypoemas
                st.rerun()
        with col_buttons[3]:
            if st.button("➡️"):
                st.session_state.current_tab_idx = (st.session_state.current_tab_idx + 1) % len(tabs_list)
                st.rerun()
        with col_buttons[4]:
            if st.button("❓"): pass

    # Sincronização entre Clique na Aba e Estado
    if tab_id != active_tab:
        st.session_state.current_tab_idx = tabs_list.index(tab_id)
        st.rerun()

    # ÁREA DE CONTEÚDO (PALCO LIMPO)
    st.markdown("---")
    
    if active_tab == "comments":
        # Conteúdo estendido para a aba Comments
        c_path = os.path.join(PATH_MD, "COMMENTS.md")
        if os.path.exists(c_path):
            with open(c_path, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), sel_idioma))
    
    elif active_tab == "ypoemas":
        # Placeholder para o coração da Machina
        st.markdown(f"### Bem-vindo à {active_tab.upper()}")
    
    else:
        # Para as demais, o palco foca no minimalismo, a info está na sidebar.
        st.empty()

if __name__ == "__main__":
    main()
