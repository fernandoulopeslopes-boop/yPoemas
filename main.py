import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os
import random

# --- [PROTOCOL] MOTOR SOBERANO ---
from lay_2_ypo import gera_poema

def normalizar_e_traduzir(conteudo, idioma):
    """
    Normaliza a saída (lista ou string), traduz se necessário e limpa 
    a mancha gráfica para garantir a impressão limpa.
    """
    if not conteudo:
        return ""
    
    # Unificação: se for lista (como no Oráculo), transforma em string
    if isinstance(conteudo, list):
        texto_unificado = "\n".join(conteudo)
    else:
        texto_unificado = conteudo
    
    texto_final = texto_unificado
    # Tradução: apenas se o idioma não for Português
    if "Português" not in idioma:
        try:
            codigos = {"ES - Español": "es", "IT - Italiano": "it", "EN - English": "en"}
            target = codigos.get(idioma, 'en')
            texto_final = GoogleTranslator(source='auto', target=target).translate(texto_unificado)
        except Exception:
            pass

    # Limpeza e Normalização: remove resíduos e evita quebras duplas
    return texto_final.replace('\r\n', '\n').replace('\n\n', '\n').strip()

def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { visibility: hidden; }
            footer { visibility: hidden; }
            
            .sb-art-top { margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
            
            /* Botões do Palco: Gap de 12px para evitar colagem */
            div.stButton > button {
                border-radius: 50% !important;
                width: 50px !important;
                height: 50px !important;
                border: 1px solid #333 !important;
                background-color: white !important;
                margin: 0 12px !important; 
            }
        </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES DE PÁGINAS E ATIVOS ---
DIR_MD = "md_files"
PAGINAS = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
MAPA_ATIVOS = {
    "mini": {"img": "img_mini.jpg", "md": "INFO_MINI.md"},
    "ypoemas": {"img": "img_ypoemas.jpg", "md": "INFO_YPOEMAS.md"},
    "eureka": {"img": "img_eureka.jpg", "md": "INFO_EUREKA.md"},
    "off-máquina": {"img": "img_off-machina.jpg", "md": "ABOUT_OFF-MACHINA.md"},
    "books": {"img": "img_books.jpg", "md": "INFO_BOOKS.md"},
    "comments": {"img": "img_poly.jpg", "md": "ABOUT_COMMENTS.md"},
    "about": {"img": "img_about.jpg", "md": "INFO_ABOUT.md"}
}

def main():
    st.set_page_config(layout="wide", page_title="yPoemas")
    aplicar_estetica_machina()

    # Estados de Persistência
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 1
    if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = 0
    if 'tema_selecionado' not in st.session_state: st.session_state.tema_selecionado = "Fatos"

    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    ativos = MAPA_ATIVOS.get(aba_atual)

    # --- SIDEBAR ---
    with st.sidebar:
        idioma = st.selectbox("L", ["PT - Português", "ES - Español", "IT - Italiano", "EN - English"], label_visibility="collapsed")
        
        st.markdown('<div class="sb-art-top">', unsafe_allow_html=True)
        if os.path.exists(ativos["img"]): st.image(ativos["img"], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Seletor de Tema
        st.session_state.tema_selecionado = st.selectbox("Tema", ["Fatos", "Amaré", "Anjos", "Babel"], label_visibility="visible")

        # Texto Informativo (Sidebar)
        path_md = os.path.join(DIR_MD, ativos["md"])
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(normalizar_e_traduzir(f.read(), idioma))

    # --- NAVEGAÇÃO SUPERIOR ---
    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)

    # --- CONTROLES DO PALCO ---
    cl, c1, c2, c3, c4, c5, cr = st.columns([3, 1, 1, 1, 1, 1, 3])
    
    if c1.button("✚"): st.session_state.seed_eureka += 1; st.rerun()
    if c2.button("❰"): st.session_state.seed_eureka -= 1; st.rerun()
    if c3.button("✱"): st.session_state.seed_eureka = random.randint(0, 999999); st.rerun()
    if c4.button("❱"): st.session_state.seed_eureka += 1; st.rerun()
    if c5.button("?"): 
        st.toast("Infinitas variações da Machina.")

    if aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_clicada)
        st.rerun()

    st.markdown("---")
    
    # --- RENDERIZAÇÃO DO PALCO ---
    if aba_atual in ["mini", "ypoemas", "eureka"]:
        # Semente exclusiva da Eureka; demais são ""
        semente = st.session_state.seed_eureka if aba_atual == "eureka" else ""
        
        # Execução do Motor
        poema_bruto = gera_poema(st.session_state.tema_selecionado, semente)
        
        # Impressão Limpa
        poema_final = normalizar_e_traduzir(poema_bruto, idioma)
        st.text(poema_final)
    else:
        st.empty()

if __name__ == "__main__":
    main()
