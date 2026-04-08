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
        except: pass
    return texto_final.replace('\r\n', '\n').replace('\n\n', '\n').strip()

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
                margin: 0 12px !important; 
            }
        </style>
    """, unsafe_allow_html=True)

LISTA_TEMAS = ["Fatos", "Amaré", "Anjos", "Babel"] # Lista oficial do motor
PAGINAS = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]

def main():
    st.set_page_config(layout="wide", page_title="yPoemas")
    aplicar_estetica_machina()

    # --- ESTADOS ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 1
    if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = 0
    if 'tema_idx' not in st.session_state: st.session_state.tema_idx = 0

    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    tema_atual = LISTA_TEMAS[st.session_state.tema_idx]

    # --- SIDEBAR ---
    with st.sidebar:
        idioma = st.selectbox("L", ["PT - Português", "ES - Español", "IT - Italiano", "EN - English"], label_visibility="collapsed")
        # Seletor sincronizado com o estado tema_idx
        tema_selecionado = st.selectbox("Tema", LISTA_TEMAS, index=st.session_state.tema_idx)
        if tema_selecionado != tema_atual:
            st.session_state.tema_idx = LISTA_TEMAS.index(tema_selecionado)
            st.rerun()

    # --- NAVEGAÇÃO SUPERIOR ---
    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)

    # --- CONTROLES DO PALCO ---
    cl, c1, c2, c3, c4, c5, cr = st.columns([3, 1, 1, 1, 1, 1, 3])
    
    # ❰ (Anterior)
    if c1.button("❰"):
        if aba_atual == "eureka":
            st.session_state.seed_eureka -= 1
        else:
            st.session_state.tema_idx = (st.session_state.tema_idx - 1) % len(LISTA_TEMAS)
        st.rerun()

    # ✱ (Ao Acaso)
    if c2.button("✱"):
        if aba_atual == "eureka":
            st.session_state.seed_eureka = random.randint(0, 999999)
        else:
            st.session_state.tema_idx = random.randint(0, len(LISTA_TEMAS) - 1)
        st.rerun()

    # ❱ (Próximo)
    if c3.button("❱"):
        if aba_atual == "eureka":
            st.session_state.seed_eureka += 1
        else:
            st.session_state.tema_idx = (st.session_state.tema_idx + 1) % len(LISTA_TEMAS)
        st.rerun()

    # ✚ (Mais/Variação - Geralmente associado a semente ou reload)
    if c4.button("✚"):
        st.session_state.seed_eureka += 1 # Para Eureka
        st.rerun()

    # ? (Help/Info)
    if c5.button("?"):
        st.info(f"Página: {aba_atual.upper()} | Tema Atual: {tema_atual}")

    if aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_clicada)
        st.rerun()

    st.markdown("---")
    
    # --- RENDERIZAÇÃO ---
    if aba_atual in ["mini", "ypoemas", "eureka"]:
        semente = st.session_state.seed_eureka if aba_atual == "eureka" else ""
        poema_bruto = gera_poema(tema_atual, semente)
        st.text(normalizar_e_traduzir(poema_bruto, idioma))

if __name__ == "__main__":
    main()
