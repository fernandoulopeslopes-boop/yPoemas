import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os
import random

# --- [PROTOCOL] MOTOR SOBERANO ---
from lay_2_ypo import gera_poema

def normalizar_e_traduzir(conteudo, idioma):
    if not conteudo: return ""
    texto_unificado = "\n".join(conteudo) if isinstance(conteudo, list) else conteudo
    texto_final = texto_unificado
    if "Português" not in idioma:
        try:
            codigos = {"ES - Español": "es", "IT - Italiano": "it", "EN - English": "en"}
            target = codigos.get(idioma, 'en')
            texto_final = GoogleTranslator(source='auto', target=target).translate(texto_unificado)
        except Exception: pass
    return texto_final.replace('\r\n', '\n').replace('\n\n', '\n').strip()

def aplicar_estetica_machina():
    st.markdown("""
        <style>
            /* Elimina a altura perdida no topo */
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            footer { visibility: hidden; }
            .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
            
            .sb-art-top { margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
            
            /* Botões no TOP: Ordem + < * > ? */
            div.stButton > button {
                border-radius: 50% !important;
                width: 50px !important;
                height: 50px !important;
                border: 1px solid #333 !important;
                background-color: white !important;
                margin: 0 10px !important;
            }
            
            /* Estilo do Cabeçalho dos Books na Sidebar */
            .book-header {
                font-size: 0.9em;
                font-weight: bold;
                color: #555;
                margin-bottom: 5px;
                text-transform: uppercase;
            }
        </style>
    """, unsafe_allow_html=True)

# LISTA DE TEMAS (Garantia de Existência)
LISTA_TEMAS = ["Fatos", "Amaré", "Anjos", "Babel"] 
PAGINAS_APP = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]

def main():
    st.set_page_config(layout="wide", page_title="yPoemas")
    aplicar_estetica_machina()

    # --- ESTADOS ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 1
    if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = 0
    if 'tema_idx' not in st.session_state: st.session_state.tema_idx = 0
    if 'show_help' not in st.session_state: st.session_state.show_help = False

    aba_atual = PAGINAS_APP[st.session_state.current_tab_idx]
    
    # Cálculos dos Books
    total_paginas = len(LISTA_TEMAS)
    pagina_atual = st.session_state.tema_idx + 1
    nome_do_book = aba_atual.upper()
    
    # --- 1. CONTROLES NO TOP ( + < * > ? ) ---
    cl, c_plus, c_prev, c_rand, c_next, c_help, cr = st.columns([3, 1, 1, 1, 1, 1, 3])
    
    if c_plus.button("✚"):
        st.session_state.show_help = False
        st.session_state.seed_eureka += 1
        st.rerun()

    if c_prev.button("❰"):
        st.session_state.show_help = False
        if aba_atual == "eureka": st.session_state.seed_eureka -= 1
        else: st.session_state.tema_idx = (st.session_state.tema_idx - 1) % total_paginas
        st.rerun()

    if c_rand.button("✱"):
        st.session_state.show_help = False
        if aba_atual == "eureka": st.session_state.seed_eureka = random.randint(0, 999999)
        else: st.session_state.tema_idx = random.randint(0, total_paginas - 1)
        st.rerun()

    if c_next.button("❱"):
        st.session_state.show_help = False
        if aba_atual == "eureka": st.session_state.seed_eureka += 1
        else: st.session_state.tema_idx = (st.session_state.tema_idx + 1) % total_paginas
        st.rerun()

    if c_help.button("?"):
        st.session_state.show_help = not st.session_state.show_help

    # --- 2. NAVEGAÇÃO DE PÁGINAS ---
    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS_APP], default=aba_atual)

    # --- SIDEBAR (O Cockpit dos Books) ---
    with st.sidebar:
        idioma = st.selectbox("L", ["PT - Português", "ES - Español", "IT - Italiano", "EN - English"], label_visibility="collapsed")
        
        # Ativos de Imagem/MD
        ativos = {
            "mini": {"img": "img_mini.jpg", "md": "INFO_MINI.md"},
            "ypoemas": {"img": "img_ypoemas.jpg", "md": "INFO_YPOEMAS.md"},
            "eureka": {"img": "img_eureka.jpg", "md": "INFO_EUREKA.md"},
            "off-máquina": {"img": "img_off-machina.jpg", "md": "ABOUT_OFF-MACHINA.md"},
            "books": {"img": "img_books.jpg", "md": "INFO_BOOKS.md"},
            "comments": {"img": "img_poly.jpg", "md": "ABOUT_COMMENTS.md"},
            "about": {"img": "img_about.jpg", "md": "INFO_ABOUT.md"}
        }.get(aba_atual)

        if os.path.exists(ativos["img"]): st.image(ativos["img"], use_container_width=True)
        
        # CABEÇALHO DO BOOK (A regra do Oráculo)
        header_text = f"{nome_do_book}: {pagina_atual} / {total_paginas}"
        st.markdown(f'<div class="book-header">{header_text}</div>', unsafe_allow_html=True)
        
        tema_sel = st.selectbox("Escolha o Tema", LISTA_TEMAS, index=st.session_state.tema_idx, label_visibility="collapsed")
        if tema_sel != LISTA_TEMAS[st.session_state.tema_idx]:
            st.session_state.tema_idx = LISTA_TEMAS.index(tema_sel)
            st.rerun()

        # MD Informativo
        path_md = os.path.join("md_files", ativos["md"])
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(normalizar_e_traduzir(f.read(), idioma))

    if aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS_APP.index(aba_clicada)
        st.session_state.show_help = False
        st.rerun()

    st.markdown("---")
    
    # --- 3. PALCO CENTRAL ---
    if st.session_state.show_help:
        st.info("A Machina produz poesia infinita. Use + para variar a semente, < > para navegar nos temas e * para o acaso.")
    elif aba_atual in ["mini", "ypoemas", "eureka"]:
        tema_atual = LISTA_TEMAS[st.session_state.tema_idx]
        semente = st.session_state.seed_eureka if aba_atual == "eureka" else ""
        poema_bruto = gera_poema(tema_atual, semente)
        st.text(normalizar_e_traduzir(poema_bruto, idioma))

if __name__ == "__main__":
    main()
