import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os
import random

# --- MOTOR DE TRADUÇÃO (ESTABILIDADE) ---
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

# --- MANUAL DE OPERAÇÃO (HELP_LISTER) ---
def get_help_tips(idioma):
    tips = {
        "plus": "Imprime mais uma cópia do mesmo tema",
        "prev": "Retorna ao tema anterior",
        "random": "Escolhe um tema ao acaso (Random)",
        "next": "Avança para o próximo tema",
        "help": "Manual de Instruções da Machina"
    }
    return {k: traduzir_texto(v, idioma) for k, v in tips.items()}

# --- ARQUITETURA DE ESTILO (PTC-CSS) ---
def aplicar_estetica_machina():
    st.markdown("""
        <style>
            /* Reset e Ocultação de Elementos Nativos */
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            .block-container { padding-top: 1rem !important; }
            footer { visibility: hidden; }

            /* Sidebar: Estrutura em 4 Containers */
            section[data-testid="stSidebar"] {
                width: 300px !important;
                min-width: 300px !important;
                max-width: 300px !important;
            }
            
            /* Bloco 2 & 3: Container de Scroll Independente */
            .sidebar-content-scroll {
                height: calc(100vh - 300px);
                overflow-y: auto;
                padding-right: 8px;
                margin-bottom: 10px;
            }
            
            /* Bloco 4: Arte Ancorada na Base */
            .sidebar-footer-fixed {
                position: absolute;
                bottom: 15px;
                width: 260px;
                background: white;
                z-index: 100;
            }

            /* Botões de Navegação: Glifos de Alta Densidade */
            div.stButton > button {
                border-radius: 50% !important;
                width: 54px !important;
                height: 54px !important;
                border: 2px solid #222 !important;
                background-color: #ffffff !important;
                color: #000 !important;
                font-size: 26px !important;
                font-weight: 900 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                transition: all 0.2s ease;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                margin: 0 auto !important;
                padding: 0px !important;
            }
            div.stButton > button:hover {
                border-color: #ff4b4b !important;
                color: #ff4b4b !important;
                transform: scale(1.1);
            }

            /* Palco: Centralização das Colunas */
            [data-testid="column"] {
                display: flex;
                justify-content: center;
                align-items: center;
            }
        </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES E MAPEAMENTO ---
DIR_MD = "md_files"
PAGINAS = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
MAPA_ATIVOS = {
    "mini": {"img": "img_mini.jpg", "md": "INFO_MINI.md", "desc": "Sobre a Mini-Machina"},
    "ypoemas": {"img": "img_ypoemas.jpg", "md": "INFO_YPOEMAS.md", "desc": ""},
    "eureka": {"img": "img_eureka.jpg", "md": "INFO_EUREKA.md", "desc": "O momento da descoberta"},
    "off-máquina": {"img": "img_off-machina.jpg", "md": "ABOUT_OFF-MACHINA.md", "desc": "Sobre os livros off-machina"},
    "books": {"img": "img_books.jpg", "md": "INFO_BOOKS.md", "desc": "A biblioteca da Machina"},
    "comments": {"img": "img_poly.jpg", "md": "ABOUT_COMMENTS.md", "desc": ""},
    "about": {"img": "img_about.jpg", "md": "INFO_ABOUT.md", "desc": "A alma do projeto"}
}

def main():
    # Inicialização do Ambiente
    st.set_page_config(layout="wide", page_title="yPoemas", page_icon="🎭")
    aplicar_estetica_machina()

    # Gestão de Estado (Navegação e Motor)
    if 'current_tab_idx' not in st.session_state:
        st.session_state.current_tab_idx = 1
    if 'poema_seed' not in st.session_state:
        st.session_state.poema_seed = 0
    
    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    ativos = MAPA_ATIVOS.get(aba_atual)

    # --- 1. SIDEBAR (TRIPÉ DE INTERFACE) ---
    with st.sidebar:
        # BLOCO 1: Seletor de Idioma (Topo Absoluto)
        idioma = st.selectbox("L", [
            "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
            "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
        ], label_visibility="collapsed")
        
        st.markdown("---")
        tips = get_help_tips(idioma)

        # BLOCO 2 & 3: Descrição + Conteúdo (Área de Scroll Independente)
        st.markdown('<div class="sidebar-content-scroll">', unsafe_allow_html=True)
        if ativos["desc"]:
            st.markdown(f"**{traduzir_texto(ativos['desc'], idioma)}**")
        
        path_md = os.path.join(DIR_MD, ativos["md"])
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), idioma))
        st.markdown('</div>', unsafe_allow_html=True)

        # BLOCO 4: Arte Ancorada (Rodapé Fixo)
        st.markdown('<div class="sidebar-footer-fixed">', unsafe_allow_html=True)
        st.markdown("---")
        if os.path.exists(ativos["img"]):
            st.image(ativos["img"], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 2. PALCO (SIMETRIA E NAVEGAÇÃO ICÔNICA) ---
    aba_clicada = stx.tab_bar(
        data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], 
        default=aba_atual, key="machina_v33_final"
    )

    # Grelha de Navegação Centrada (✚ ❰ ✱ ❱ ？)
    c_puffer_l, c1, c2, c3, c4, c5, c_puffer_r = st.columns([4, 1, 1, 1, 1, 1, 4])
    
    if c1.button("✚", help=tips["plus"]):
        st.session_state.poema_seed += 1
        st.rerun()
    
    if c2.button("❰", help=tips["prev"]):
        st.session_state.current_tab_idx = (st.session_state.current_tab_idx - 1) % len(PAGINAS)
        st.rerun()
        
    if c3.button("✱", help=tips["random"]):
        opcoes = [i for i in range(len(PAGINAS)) if i != st.session_state.current_tab_idx]
        st.session_state.current_tab_idx = random.choice(opcoes)
        st.rerun()
        
    if c4.button("❱", help=tips["next"]):
        st.session_state.current_tab_idx = (st.session_state.current_tab_idx + 1) % len(PAGINAS)
        st.rerun()
        
    if c5.button("？", help=tips["help"]): 
        pass

    # Sincronia entre Tab Bar e Botões
    if aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_clicada)
        st.rerun()

    st.markdown("---")
    
    # RENDERIZAÇÃO DE CONTEÚDO
    if aba_atual == "comments":
        path_c = os.path.join(DIR_MD, "COMMENTS.md")
        if os.path.exists(path_c):
            with open(path_c, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), idioma))
    elif aba_atual == "ypoemas":
        # Placeholder para o Motor de Poesia
        st.markdown(f"### {aba_atual.upper()}")
        st.write(f"Versão de Impressão: {st.session_state.poema_seed}")
    else:
        st.empty()

if __name__ == "__main__":
    main()
