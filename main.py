import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os
import random

# --- [PROTOCOL] MOTOR SOBERANO ---
from lay_2_ypo import gera_poema

# --- TRADUTOR (CONDICIONAL) ---
@st.cache_data(show_spinner=False)
def traduzir_texto(texto, destino_nome):
    if not texto or "Português" in destino_nome: 
        return texto
    try:
        codigos = {
            "PT - Português": "pt", "ES - Español": "es", 
            "IT - Italiano": "it", "EN - English": "en"
        }
        target = codigos.get(destino_nome, 'en')
        return GoogleTranslator(source='auto', target=target).translate(texto)
    except Exception:
        return texto

# --- ESTÉTICA IDENTITÁRIA ---
def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { visibility: hidden; }
            footer { visibility: hidden; }
            
            /* Sidebar: Arte e Limpeza */
            .sb-art-top { margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
            
            /* Botões Circulares do Palco */
            div.stButton > button {
                border-radius: 50% !important;
                width: 50px !important;
                height: 50px !important;
                border: 1px solid #333 !important;
                background-color: white !important;
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

    # --- ESTADOS DE SESSÃO ---
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
        
        # Seletor de Tema (Motor)
        st.session_state.tema_selecionado = st.selectbox("Tema", ["Fatos", "Amaré", "Anjos", "Babel"], label_visibility="visible")

        # Texto Informativo MD
        path_md = os.path.join(DIR_MD, ativos["md"])
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(traduzir_texto(f.read(), idioma))

    # --- NAVEGAÇÃO SUPERIOR (STX) ---
    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)

    # --- CONTROLES DO PALCO ---
    cl, c1, c2, c3, c4, cr = st.columns([4, 1, 1, 1, 1, 4])
    
    # ✚ e ❱ : Incremento da seed_eureka
    if c1.button("✚"): st.session_state.seed_eureka += 1; st.rerun()
    # ❰ : Decremento da seed_eureka
    if c2.button("❰"): st.session_state.seed_eureka -= 1; st.rerun()
    # ✱ : Random seed_eureka
    if c3.button("✱"): st.session_state.seed_eureka = random.randint(0, 999999); st.rerun()
    # ❱ : Incremento (Próximo)
    if c4.button("❱"): st.session_state.seed_eureka += 1; st.rerun()

    # Sincronia de Abas
    if aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_clicada)
        st.rerun()

    st.markdown("---")
    
    # --- RENDERIZAÇÃO DO PALCO ---
    if aba_atual in ["mini", "ypoemas", "eureka"]:
        
        # A SEMENTE SÓ É NECESSÁRIA NA PÁGINA EUREKA
        # Para mini e ypoemas, passamos "" (conforme o Oráculo)
        semente_final = st.session_state.seed_eureka if aba_atual == "eureka" else ""
            
        # O motor devolve o texto limpo e pronto
        resultado = gera_poema(st.session_state.tema_selecionado, semente_final)
        
        # Impressão Direta (Traduz apenas se idioma != PT)
        st.text(traduzir_texto(resultado, idioma))
    else:
        st.empty()

if __name__ == "__main__":
    main()
