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

# --- ESTÉTICA DO BACKUP (SIMPLES) ---
def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { visibility: hidden; }
            footer { visibility: hidden; }
            
            /* Sidebar: Arte no Topo conforme acordado */
            .sb-art-top { margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
            
            /* Botões de Navegação */
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

    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 1
    if 'poema_seed' not in st.session_state: st.session_state.poema_seed = 0
    if 'tema_atual' not in st.session_state: st.session_state.tema_atual = "Fatos"

    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    ativos = MAPA_ATIVOS.get(aba_atual)

    # --- SIDEBAR (ART NO TOPO) ---
    with st.sidebar:
        idioma = st.selectbox("L", ["PT - Português", "ES - Español", "IT - Italiano", "EN - English"], label_visibility="collapsed")
        
        st.markdown('<div class="sb-art-top">', unsafe_allow_html=True)
        if os.path.exists(ativos["img"]): st.image(ativos["img"], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.session_state.tema_atual = st.selectbox("Tema", ["Fatos", "Amaré", "Anjos", "Babel"], label_visibility="visible")

        path_md = os.path.join(DIR_MD, ativos["md"])
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), idioma))

    # --- NAVEGAÇÃO ---
    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)

    cl, c1, c2, c3, c4, cr = st.columns([4, 1, 1, 1, 1, 4])
    if c1.button("✚"): st.session_state.poema_seed += 1; st.rerun()
    if c2.button("❰"): st.session_state.current_tab_idx = (st.session_state.current_tab_idx - 1) % len(PAGINAS); st.rerun()
    if c3.button("✱"): st.session_state.current_tab_idx = random.choice([i for i in range(len(PAGINAS))]); st.rerun()
    if c4.button("❱"): st.session_state.current_tab_idx = (st.session_state.current_tab_idx + 1) % len(PAGINAS); st.rerun()

    if aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_clicada)
        st.rerun()

    st.markdown("---")
    
    # --- RENDERIZAÇÃO SEM COMPLICAÇÃO ---
    if aba_atual in ["mini", "ypoemas", "eureka"]:
        # Motor original entrega o texto limpo
        poema_bruto = gera_poema(st.session_state.tema_atual, st.session_state.poema_seed)
        
        # Se for lista, unifica; se não, imprime o objeto direto (st.write ou st.markdown limpo)
        texto_final = traduzir_texto(poema_bruto, idioma)
        
        if isinstance(texto_final, list):
            for linha in texto_final:
                st.text(linha)
        else:
            st.text(texto_final)
    else:
        st.empty()

if __name__ == "__main__":
    main()
