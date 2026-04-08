import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os
import random

# --- MOTOR DE TRADUÇÃO ---
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

# --- MANUAL DE OPERAÇÃO ---
def get_help_tips(idioma):
    tips = {
        "plus": "Imprime mais uma cópia do mesmo tema",
        "prev": "Retorna ao tema anterior",
        "random": "Escolhe um tema ao acaso (Random)",
        "next": "Avança para o próximo tema",
        "help": "Manual de Instruções da Machina"
    }
    return {k: traduzir_texto(v, idioma) for k, v in tips.items()}

# --- ARQUITETURA DE ESTILO (PTC-CSS V37 - RIGIDEZ TOTAL) ---
def aplicar_estetica_machina():
    st.markdown("""
        <style>
            /* Bloqueio do Scroll Global da Sidebar */
            [data-testid="stSidebarUserContent"] {
                overflow: hidden !important;
                display: flex;
                flex-direction: column;
                height: 100vh !important;
            }

            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            .block-container { padding-top: 1rem !important; }
            footer { visibility: hidden; }

            /* BLOCO 1 & 2: Cabeçalho Estático */
            .sb-header {
                flex-shrink: 0;
                margin-top: -45px;
                background: white;
                padding-bottom: 10px;
                z-index: 20;
            }

            /* BLOCO 3: Janela de Scroll Rígida */
            .sb-content-scroll {
                flex-grow: 1;
                height: calc(100vh - 450px) !important; /* Altura calculada para nunca empurrar a arte */
                max-height: calc(100vh - 450px) !important;
                overflow-y: auto !important;
                padding-right: 15px;
                margin-bottom: 5px;
                scrollbar-width: thin;
                border-bottom: 1px solid #f0f0f0;
            }

            /* BLOCO 4: Arte Fixada no Rodapé da Sidebar */
            .sb-footer-art {
                position: fixed;
                bottom: 0;
                width: 260px;
                background: white;
                padding: 10px 0;
                z-index: 30;
                border-top: 1px solid #eee;
            }

            /* Estilo dos Botões do Palco */
            div.stButton > button {
                border-radius: 50% !important;
                width: 52px !important;
                height: 52px !important;
                border: 2px solid #222 !important;
                background-color: #ffffff !important;
                color: #000 !important;
                font-size: 24px !important;
                font-weight: 900 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            }
            div.stButton > button:hover {
                border-color: #ff4b4b !important;
                color: #ff4b4b !important;
            }

            [data-testid="column"] { display: flex; justify-content: center; align-items: center; }
        </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES ---
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
    st.set_page_config(layout="wide", page_title="yPoemas", page_icon="🎭")
    aplicar_estetica_machina()

    if 'current_tab_idx' not in st.session_state:
        st.session_state.current_tab_idx = 1
    if 'poema_seed' not in st.session_state:
        st.session_state.poema_seed = 0
    
    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    ativos = MAPA_ATIVOS.get(aba_atual)

    # --- 1. SIDEBAR REESTRUTURADA ---
    with st.sidebar:
        # BLOCO 1 & 2: Topo Fixo
        st.markdown('<div class="sb-header">', unsafe_allow_html=True)
        idioma = st.selectbox("L", [
            "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
            "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
        ], label_visibility="collapsed")
        
        if ativos["desc"]:
            st.markdown(f"**{traduzir_texto(ativos['desc'], idioma)}**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        tips = get_help_tips(idioma)

        # BLOCO 3: O Pulmão com Scroll Controlado
        st.markdown('<div class="sb-content-scroll">', unsafe_allow_html=True)
        path_md = os.path.join(DIR_MD, ativos["md"])
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), idioma))
        st.markdown('</div>', unsafe_allow_html=True)

        # BLOCO 4: Arte Blindada no Rodapé
        st.markdown('<div class="sb-footer-art">', unsafe_allow_html=True)
        if os.path.exists(ativos["img"]):
            st.image(ativos["img"], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 2. PALCO ---
    aba_clicada = stx.tab_bar(
        data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], 
        default=aba_atual, key="machina_v37_rigid"
    )

    cl, c1, c2, c3, c4, c5, cr = st.columns([4, 1, 1, 1, 1, 1, 4])
    
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
    if c5.button("？", help=tips["help"]): pass

    if aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_clicada)
        st.rerun()

    st.markdown("---")
    
    # RENDERIZAÇÃO
    if aba_atual == "comments":
        path_c = os.path.join(DIR_MD, "COMMENTS.md")
        if os.path.exists(path_c):
            with open(path_c, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), idioma))
    elif aba_atual == "ypoemas":
        st.markdown(f"### {aba_atual.upper()} (Semente: {st.session_state.poema_seed})")
    else:
        st.empty()

if __name__ == "__main__":
    main()
