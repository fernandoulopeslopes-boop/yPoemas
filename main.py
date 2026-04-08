import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os
import random

# --- [PROTOCOL] IMPORTAÇÃO DO MOTOR ---
from lay_2_ypo import gera_poema

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

# --- ARQUITETURA DE ESTILO (PTC-CSS V45) ---
def aplicar_estetica_machina():
    st.markdown("""
        <style>
            /* Reset e Ocultação */
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            .block-container { padding-top: 1rem !important; }
            footer { visibility: hidden; }

            /* Espaçamento Sidebar */
            [data-testid="stSidebarUserContent"] { padding-top: 20px !important; }
            
            /* Bloco 4 (Arte) - Ancorado no Topo */
            .sb-art-top {
                margin: 10px 0 20px 0;
                border-bottom: 1px solid #f0f0f0;
                padding-bottom: 15px;
            }

            /* Bloco 3 (Texto) - Fluidez abaixo da Arte */
            .sb-text-content { font-size: 0.95rem; line-height: 1.5; color: #444; }

            /* PALCO CENTRAL (MANCHA GRÁFICA) */
            .palco-poetico {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 400px;
                padding: 40px;
                background-color: #fdfdfd;
                margin-top: 30px;
                text-align: center;
            }

            .poema-texto {
                font-family: 'Courier New', Courier, monospace; 
                font-size: 1.6rem;
                color: #1a1a1a;
                white-space: pre-wrap;
                line-height: 1.8;
                letter-spacing: 1px;
            }

            /* Botões Circulares do Palco */
            div.stButton > button {
                border-radius: 50% !important;
                width: 52px !important;
                height: 52px !important;
                border: 2px solid #222 !important;
                background-color: #ffffff !important;
                font-size: 24px !important;
                font-weight: 900 !important;
                margin: 0 auto !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }
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

    # Controle de Sessão
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 1
    if 'poema_seed' not in st.session_state: st.session_state.poema_seed = 0
    
    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    ativos = MAPA_ATIVOS.get(aba_atual)

    # --- 1. SIDEBAR (HARMONIA INVERTIDA) ---
    with st.sidebar:
        # Bloco 1: Idioma
        idioma = st.selectbox("L", [
            "PT - Português", "ES - Español", "IT - Italiano", "FR - Français", 
            "DE - Deutsch", "EN - English", "CA - Català", "GL - Galego", "RO - Română"
        ], label_visibility="collapsed")
        
        # Bloco 2: Conceito
        if ativos["desc"]:
            st.markdown(f"**{traduzir_texto(ativos['desc'], idioma)}**")
        
        # Bloco 4: ARTE (Topo)
        st.markdown('<div class="sb-art-top">', unsafe_allow_html=True)
        if os.path.exists(ativos["img"]):
            st.image(ativos["img"], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        tips = get_help_tips(idioma)

        # Bloco 3: TEXTO (Base)
        st.markdown('<div class="sb-text-content">', unsafe_allow_html=True)
        path_md = os.path.join(DIR_MD, ativos["md"])
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), idioma))
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 2. PALCO E NAVEGAÇÃO ---
    aba_clicada = stx.tab_bar(
        data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], 
        default=aba_atual, key="machina_v45_stable"
    )

    # Controles Físicos
    cl, c1, c2, c3, c4, c5, cr = st.columns([4, 1, 1, 1, 1, 1, 4])
    if c1.button("✚", help=tips["plus"]):
        st.session_state.poema_seed += 1
        st.rerun()
    if c2.button("❰", help=tips["prev"]):
        st.session_state.current_tab_idx = (st.session_state.current_tab_idx - 1) % len(PAGINAS)
        st.rerun()
    if c3.button("✱", help=tips["random"]):
        st.session_state.current_tab_idx = random.choice([i for i in range(len(PAGINAS)) if i != st.session_state.current_tab_idx])
        st.rerun()
    if c4.button("❱", help=tips["next"]):
        st.session_state.current_tab_idx = (st.session_state.current_tab_idx + 1) % len(PAGINAS)
        st.rerun()
    if c5.button("？", help=tips["help"]): pass

    # Sincronia
    if aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_clicada)
        st.rerun()

    st.markdown("---")
    
    # --- 3. EXECUÇÃO DO MOTOR (TRÍADE) ---
    if aba_atual in ["mini", "ypoemas", "eureka"]:
        # Chamada definitiva: motor original + semente da sessão
        poema_bruto = gera_poema(aba_atual, st.session_state.poema_seed)
        
        st.markdown(f"""
            <div class="palco-poetico">
                <div class="poema-texto">{traduzir_texto(poema_bruto, idioma)}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Páginas Estáticas do Palco
        if aba_atual == "comments":
            path_c = os.path.join(DIR_MD, "COMMENTS.md")
            if os.path.exists(path_c):
                with open(path_c, "r", encoding="utf-8") as f:
                    st.markdown(traduzir_texto(f.read(), idioma))
        else:
            st.empty()

if __name__ == "__main__":
    main()
