import streamlit as st
import asyncio
from deep_translator import GoogleTranslator
import edge_tts
import matplotlib.pyplot as plt
import numpy as np

# 1. SISTEMA DE TRADUÇÃO (LIBERDADE TOTAL PARA A MARCA)
def t(texto, idioma_destino_sigla="pt"):
    try:
        # A marca yPoemas flui livremente para avaliação de fronteiras
        tradutor = GoogleTranslator(source='auto', target=idioma_destino_sigla)
        resultado = tradutor.translate(texto)
        return resultado.lower()
    except:
        return texto.lower()

# 2. MOTOR DE VOZ (UTILIZANDO EDGE-TTS CONFORME REQUIREMENTS)
async def gerar_audio(texto, voz):
    communicate = edge_tts.Communicate(texto, voz)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

# 3. INTERFACE E LÓGICA
def main():
    # Estado da Sessão
    if 'pagina_ativa' not in st.session_state:
        st.session_state.pagina_ativa = "mini"
    if 'som_ativo' not in st.session_state:
        st.session_state.som_ativo = False

    # CSS para Expansão (100% width) e Sidebar (300px)
    st.markdown("""
        <style>
            .main .block-container { max-width: 100%; padding: 2rem; }
            [data-testid="stSidebar"] { width: 300px; max-width: 300px; }
            .stButton button { width: 100%; }
            .footer-social { position: fixed; bottom: 20px; width: 260px; text-align: center; }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar: Centro de Controle
    with st.sidebar:
        # Mapeamento de idiomas e vozes para o edge-tts
        idiomas = {
            "Português": ("pt", "pt-BR-AntonioNeural"),
            "Inglês": ("en", "en-US-GuyNeural"),
            "Espanhol": ("es", "es-ES-AlvaroNeural"),
            "Francês": ("fr", "fr-FR-HenriNeural"),
            "Russo": ("ru", "ru-RU-DmitryNeural")
        }
        
        escolha = st.selectbox(t("idiomas disponíveis"), list(idiomas.keys()))
        sigla, voz_id = idiomas[escolha]

        col1, col2 = st.columns(2)
        with col1: 
            st.button(t("🎨 arte", sigla), help=t("visualizar mandalas e artes", sigla))
        with col2:
            marca_ouvida = t("yPoemas", sigla)
            if st.button(t("🔊 som", sigla), help=t(f"ouvir o {marca_ouvida} em {escolha}", sigla)):
                st.session_state.som_ativo = not st.session_state.som_ativo

        st.divider()
        st.markdown(f"### {t('info', sigla)}: {t(st.session_state.pagina_ativa, sigla)}")
        st.info(t(f"under construction: {st.session_state.pagina_ativa}", sigla))

    # Palco
    st.title(f"{t('a Machina de fazer Poesia', sigla)} / {t(st.session_state.pagina_ativa, sigla)}")
    
    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre/about"]
    cols = st.columns(len(paginas))
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(t(pg, sigla), key=f"palco_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

    # Espaço do Som (Centralizado entre botões e moldura)
    if st.session_state.som_ativo:
        texto_som = t(st.session_state.pagina_ativa, sigla)
        audio_bytes = asyncio.run(gerar_audio(texto_som, voz_id))
        _, col_audio, _ = st.columns([1, 2, 1])
        with col_audio:
            st.audio(audio_bytes, format='audio/mp3')

    # Moldura do Palco
    with st.container(border=True):
        st.warning(t(f"⚠️ under construction: {st.session_state.pagina_ativa}", sigla))

# VERIFICAÇÃO DO PTC NO EOF()
if __name__ == "__main__":
    main()
