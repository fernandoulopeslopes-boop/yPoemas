import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

# 1. SISTEMA DE TRADUÇÃO (LIBERDADE TOTAL PARA A MARCA)
def t(texto, idioma_destino_sigla="pt"):
    try:
        # A marca yPoemas agora transmutada para outros idiomas
        tradutor = GoogleTranslator(source='auto', target=idioma_destino_sigla)
        resultado = tradutor.translate(texto)
        return resultado.lower()
    except:
        return texto.lower()

# 2. CONFIGURAÇÃO DA PÁGINA (TRADUZIDA)
def configurar_pagina(sigla):
    st.set_page_config(page_title=t("a Machina de fazer Poesia", sigla), layout="wide")

# 3. INTERFACE E LÓGICA
def main():
    # Estado da Sessão
    if 'pagina_ativa' not in st.session_state:
        st.session_state.pagina_ativa = "mini"
    if 'som_ativo' not in st.session_state:
        st.session_state.som_ativo = False

    # CSS para Expansão e Sidebar
    st.markdown("""
        <style>
            .main .block-container { max-width: 100%; padding: 2rem; }
            [data-testid="stSidebar"] { width: 300px; max-width: 300px; }
            .stButton button { width: 100%; }
            .footer-social { position: fixed; bottom: 20px; width: 260px; text-align: center; font-size: 20px; }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar: Centro de Controle
    with st.sidebar:
        idiomas = {
            "Português": "pt", "Espanhol": "es", "Italiano": "it", "Francês": "fr", 
            "Inglês": "en", "Catalão": "ca", "Córsico": "co", "Galego": "gl", 
            "Basco": "eu", "Esperanto": "eo", "Latin": "la", "Galês": "cy", 
            "Sueco": "sv", "Polonês": "pl", "Holandês": "nl", "Norueguês": "no", 
            "Finlandês": "fi", "Dinamarquês": "da", "Irlandês": "ga", "Romeno": "ro",
            "Russo": "ru"
        }
        escolha = st.selectbox(t("idiomas disponíveis"), list(idiomas.keys()))
        sigla = idiomas[escolha]

        col1, col2 = st.columns(2)
        with col1: st.button(t("🎨 arte", sigla), help=t("visualizar mandalas e artes", sigla))
        with col2:
            marca_ouvida = t("yPoemas", sigla)
            if st.button(t("🔊 som", sigla), help=t(f"ouvir o {marca_ouvida} em {escolha}", sigla)):
                st.session_state.som_ativo = not st.session_state.som_ativo

        st.divider()
        st.markdown(f"### {t('info', sigla)}: {t(st.session_state.pagina_ativa, sigla)}")
        st.image("https://via.placeholder.com/260x260.png?text=arte+da+pagina", use_column_width=True)

    # Palco
    st.title(f"{t('a Machina de fazer Poesia', sigla)} / {t(st.session_state.pagina_ativa, sigla)}")
    
    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre/about"]
    cols = st.columns(len(paginas))
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(t(pg, sigla), key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

    # Som Ativado
    if st.session_state.som_ativo:
        texto_som = t(st.session_state.pagina_ativa, sigla)
        tts = gTTS(text=texto_som, lang=sigla)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')

    # Moldura
    with st.container(border=True):
        st.warning(t(f"under construction: {st.session_state.pagina_ativa}", sigla))

# VERIFICAÇÃO DO PTC NO EOF()
if __name__ == "__main__":
    main()
