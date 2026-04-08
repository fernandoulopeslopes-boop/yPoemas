import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os

# --- NÚCLEO DE TRADUÇÃO (SINTONIA FINA) ---
@st.cache_data(show_spinner=False)
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
    except Exception:
        return texto

# --- ESTÉTICA E GEOMETRIA (CSS) ---
def aplicar_estilo_ypoemas():
    st.markdown("""
        <style>
            /* Limpeza de Interface */
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            .block-container { padding-top: 1.5rem !important; }
            footer { visibility: hidden; }

            /* Sidebar: Rigor de 300px e Topo Zero */
            section[data-testid="stSidebar"] {
                width: 300px !important;
                min-width: 300px !important;
                max-width: 300px !important;
            }
            [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
                padding-top: 0rem !important;
                gap: 0.5rem !important;
            }

            /* Botões de Navegação: Glifos Circulares Pesados */
            div.stButton > button {
                border-radius: 50% !important;
                width: 52px !important;
                height: 52px !important;
                border: 1px solid #333 !important;
                background-color: #ffffff !important;
                color: #111 !important;
                font-size: 24px !important;
                font-weight: bold !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                transition: all 0.2s ease-in-out;
                box-shadow: 1px 2px 4px rgba(0,0,0,0.1);
                margin: 0 auto !important;
                padding: 0px !important;
            }
            div.stButton > button:hover {
                border-color: #ff4b4b !important;
                color: #ff4b4b !important;
                transform: translateY(-2px);
                box-shadow: 2px 4px 8px rgba(0,0,0,0.15);
            }

            /* Centralização de Colunas */
            [data-testid="column"] {
                display: flex;
                justify-content: center;
                align-items: center;
            }
        </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES E ATIVOS ---
DIR_MD = "md_files"
ARQUIVO_ICONE = "icon_ypo.ico"
IDIOMAS = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
    "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
]
PAGINAS = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]

ATRIBUTOS = {
    "mini": {"img": "img_mini.jpg", "md": "INFO_MINI.md"},
    "ypoemas": {"img": "img_ypoemas.jpg", "md": "INFO_YPOEMAS.md"},
    "eureka": {"img": "img_eureka.jpg", "md": "INFO_EUREKA.md"},
    "off-máquina": {"img": "img_off-machina.jpg", "md": "ABOUT_OFF-MACHINA.md"},
    "books": {"img": "img_books.jpg", "md": "INFO_BOOKS.md"},
    "comments": {"img": "img_poly.jpg", "md": "ABOUT_COMMENTS.md"},
    "about": {"img": "img_about.jpg", "md": "INFO_ABOUT.md"}
}

def main():
    st.set_page_config(
        layout="wide", 
        page_title="yPoemas", 
        page_icon=ARQUIVO_ICONE if os.path.exists(ARQUIVO_ICONE) else "🎭"
    )
    aplicar_estilo_ypoemas()

    # Controle Robusto de Navegação
    if 'current_tab_idx' not in st.session_state:
        st.session_state.current_tab_idx = 1
    
    pagina_ativa = PAGINAS[st.session_state.current_tab_idx]
    ativo = ATRIBUTOS.get(pagina_ativa)

    # --- 1. SIDEBAR (TRADUÇÃO E IDENTIDADE) ---
    with st.sidebar:
        # Seletor no Topo
        st.markdown("<div style='margin-top: -10px;'></div>", unsafe_allow_html=True)
        idioma_sel = st.selectbox("Lang", IDIOMAS, label_visibility="collapsed", key="lang_ypo")
        st.markdown("---")

        # Texto de Apoio
        path_md = os.path.join(DIR_MD, ativo["md"])
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), idioma_sel))
        
        # Arte Ancorada (Resgate Visual)
        st.markdown("<div style='height: 20vh;'></div>", unsafe_allow_html=True)
        st.markdown("---")
        if os.path.exists(ativo["img"]):
            st.image(ativo["img"], use_container_width=True)

    # --- 2. PALCO (NAVEGAÇÃO E CONTEÚDO) ---
    aba_clicada = stx.tab_bar(
        data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], 
        default=pagina_ativa,
        key="machina_v28_final"
    )

    # Botões Glifo (✚ ❰ ✱ ❱ ❓)
    c1, c2, c3, c4, c5, c_void = st.columns([1, 1, 1, 1, 1, 8])
    
    if c1.button("✚"): pass
    
    if c2.button("❰"):
        st.session_state.current_tab_idx = (st.session_state.current_tab_idx - 1) % len(PAGINAS)
        st.rerun()
        
    if c3.button("✱"):
        st.session_state.current_tab_idx = 1 # Home
        st.rerun()
        
    if c4.button("❱"):
        st.session_state.current_tab_idx = (st.session_state.current_tab_idx + 1) % len(PAGINAS)
        st.rerun()
        
    if c5.button("❓"): pass

    # Sincronização Tab -> Estado
    if aba_clicada != pagina_ativa:
        st.session_state.current_tab_idx = PAGINAS.index(aba_clicada)
        st.rerun()

    st.markdown("---")
    
    # Conteúdo Principal
    if pagina_ativa == "comments":
        path_c = os.path.join(DIR_MD, "COMMENTS.md")
        if os.path.exists(path_c):
            with open(path_c, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), idioma_sel))
    elif pagina_ativa == "ypoemas":
        st.markdown(f"### {pagina_ativa.upper()}")
    else:
        st.empty()

if __name__ == "__main__":
    main()
