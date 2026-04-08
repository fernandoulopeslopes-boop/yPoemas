import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os
import random

# --- IMPORTAÇÃO DO MOTOR ---
from lay_2_ypo import gera_poema

# --- MOTOR DE TRADUÇÃO ---
@st.cache_data(show_spinner=False)
def traduzir_texto(texto, destino_nome):
    if not texto or "Português" in destino_nome: 
        return texto
    try:
        codigos = {"PT - Português": "pt", "ES - Español": "es", "IT - Italiano": "it", "EN - English": "en"}
        target = codigos.get(destino_nome, 'en')
        return GoogleTranslator(source='auto', target=target).translate(texto)
    except Exception:
        return texto

# --- ESTÉTICA DO BACKUP ---
def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { visibility: hidden; }
            footer { visibility: hidden; }
            .sb-art-top { margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
            div.stButton > button {
                border-radius: 50% !important;
                width: 50px !important;
                height: 50px !important;
                border: 1px solid #333 !important;
            }
        </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES ---
DIR_MD = "md_files"
PAGINAS = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
MAPA_ATIVOS = {
    "mini": {"img": "img_mini.jpg", "md": "INFO_MINI.md", "tema_motor": "mini"},
    "ypoemas": {"img": "img_ypoemas.jpg", "md": "INFO_YPOEMAS.md", "tema_motor": "fatos"},
    "eureka": {"img": "img_eureka.jpg", "md": "INFO_EUREKA.md", "tema_motor": "eureka"},
    "off-máquina": {"img": "img_off-machina.jpg", "md": "ABOUT_OFF-MACHINA.md", "tema_motor": None},
    "books": {"img": "img_books.jpg", "md": "INFO_BOOKS.md", "tema_motor": None},
    "comments": {"img": "img_poly.jpg", "md": "ABOUT_COMMENTS.md", "tema_motor": None},
    "about": {"img": "img_about.jpg", "md": "INFO_ABOUT.md", "tema_motor": None}
}

def main():
    st.set_page_config(layout="wide", page_title="yPoemas")
    aplicar_estetica_machina()

    # Inicialização de Estados
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 1
    if 'poema_seed' not in st.session_state: st.session_state.poema_seed = 0

    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    ativos = MAPA_ATIVOS.get(aba_atual)

    # --- SIDEBAR (INFORMATIVA) ---
    with st.sidebar:
        idioma = st.selectbox("L", ["PT - Português", "ES - Español", "IT - Italiano", "EN - English"], label_visibility="collapsed")
        
        st.markdown('<div class="sb-art-top">', unsafe_allow_html=True)
        if os.path.exists(ativos["img"]): st.image(ativos["img"], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Conteúdo textual da sidebar
        path_md = os.path.join(DIR_MD, ativos["md"])
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), idioma))

    # --- NAVEGAÇÃO DE PÁGINAS (SUPERIOR) ---
    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)

    # --- CONTROLES DO PALCO ---
    cl, c1, c2, c3, c4, cr = st.columns([4, 1, 1, 1, 1, 4])
    
    if c1.button("✚"): 
        st.session_state.poema_seed += 1
        st.rerun()
    
    if c2.button("❰"): 
        st.session_state.poema_seed -= 1
        st.rerun()
    
    if c3.button("✱"): 
        st.session_state.poema_seed = random.randint(0, 999999)
        st.rerun()
    
    if c4.button("❱"): 
        st.session_state.poema_seed += 1
        st.rerun()

    # Sincronia das Abas
    if aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_clicada)
        st.rerun()

    st.markdown("---")
    
    # --- RENDERIZAÇÃO DO CONTEÚDO ---
    # Só aciona o motor se a página atual tiver um 'tema_motor' definido
    tema_para_o_motor = ativos.get("tema_motor")
    
    if tema_para_o_motor:
        # O motor recebe o tema específico da página e a semente atual
        resultado = gera_poema(tema_para_o_motor, st.session_state.poema_seed)
        st.text(traduzir_texto(resultado, idioma))
    else:
        # Para as outras páginas (off-máquina, books, etc), o palco fica limpo 
        # ou exibe o conteúdo MD já processado na sidebar.
        st.empty()

if __name__ == "__main__":
    main()
