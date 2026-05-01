import streamlit as st
import asyncio
from deep_translator import GoogleTranslator
import edge_tts
import io

# 1. SISTEMA DE TRADUÇÃO (TEXTO PURO APENAS)
def t(texto, sigla_destino="pt"):
    try:
        # Blindagem: traduz apenas o núcleo do texto
        tradutor = GoogleTranslator(source='auto', target=sigla_destino)
        return tradutor.translate(texto).lower()
    except:
        return texto.lower()

# 2. MOTOR DE VOZ (EDGE-TTS)
async def gerar_audio(texto, voz):
    communicate = edge_tts.Communicate(texto, voz)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

# 3. INTERFACE DA MACHINA
def main():
    if 'pagina_ativa' not in st.session_state:
        st.session_state.pagina_ativa = "mini"
    if 'som_ativo' not in st.session_state:
        st.session_state.som_ativo = False

    st.markdown("""
        <style>
            .main .block-container { max-width: 100%; padding: 2rem; }
            [data-testid="stSidebar"] { width: 300px; max-width: 300px; }
            .stButton button { width: 100%; }
            .footer-social { position: fixed; bottom: 20px; width: 260px; text-align: center; }
        </style>
    """, unsafe_allow_html=True)

    # Listas Blindadas
    lista_idiomas = [
        "Português", "Espanhol", "Italiano", "Francês", "Inglês", 
        "Catalão", "Córsico", "Galego", "Basco", "Esperanto", 
        "Latim", "Galês", "Sueco", "Polonês", "Holandês", 
        "Norueguês", "Finlandês", "Dinamarquês", "Irlandês", 
        "Romeno", "Russo"
    ]

    mapa_linguas = {
        "Português": ("pt", "pt-BR-AntonioNeural"), "Espanhol": ("es", "es-ES-AlvaroNeural"),
        "Italiano": ("it", "it-IT-DiegoNeural"), "Francês": ("fr", "fr-FR-HenriNeural"),
        "Inglês": ("en", "en-US-GuyNeural"), "Catalão": ("ca", "es-ES-AlvaroNeural"),
        "Córsico": ("co", "fr-FR-HenriNeural"), "Galego": ("gl", "es-ES-AlvaroNeural"),
        "Basco": ("eu", "es-ES-AlvaroNeural"), "Esperanto": ("eo", "en-US-GuyNeural"),
        "Latim": ("la", "it-IT-DiegoNeural"), "Galês": ("cy", "en-GB-ThomasNeural"),
        "Sueco": ("sv", "sv-SE-MattiasNeural"), "Polonês": ("pl", "pl-PL-MarekNeural"),
        "Holandês": ("nl", "nl-NL-MaartenNeural"), "Norueguês": ("no", "nb-NO-FinnNeural"),
        "Finlandês": ("fi", "fi-FI-HarriNeural"), "Dinamarquês": ("da", "da-DK-JeppeNeural"),
        "Irlandês": ("ga", "en-IE-ConnorNeural"), "Romeno": ("ro", "ro-RO-EmilNeural"),
        "Russo": ("ru", "ru-RU-DmitryNeural")
    }

    with st.sidebar:
        idioma_nome = st.selectbox(t("idiomas disponíveis"), lista_idiomas)
        sigla, voz_ativa = mapa_linguas[idioma_nome]

        col1, col2 = st.columns(2)
        with col1: 
            # Recomposição: Emoji + Tradução(Texto)
            st.button(f"🎨 {t('arte', sigla)}", help=t("visualizar mandalas e artes", sigla))
        
        with col2:
            # Recomposição: Emoji + Tradução(Texto)
            label_som = f"🔊 {t('som', sigla)}"
            marca_traduzida = t("yPoemas", sigla)
            # Dica: Tradução(Texto base) + Variável traduzida
            dica_som = f"{t('ouvir o', sigla)} {marca_traduzida}"
            
            if st.button(label_som, help=dica_som):
                st.session_state.som_ativo = not st.session_state.som_ativo

        st.divider()
        st.markdown(f"### {t('info', sigla)}: {t(st.session_state.pagina_ativa, sigla)}")
        st.image("https://via.placeholder.com/260x260.png?text=arte+da+pagina", use_column_width=True)

    # Palco Expansivo
    st.title(f"{t('a Machina de fazer Poesia', sigla)} / {t(st.session_state.pagina_ativa, sigla)}")
    
    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre"]
    cols = st.columns(len(paginas))
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(t(pg, sigla), key=f"palco_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

    if st.session_state.som_ativo:
        texto_ouvir = t(st.session_state.pagina_ativa, sigla)
        try:
            audio_bytes = asyncio.run(gerar_audio(texto_ouvir, voz_ativa))
            _, col_audio, _ = st.columns([1, 2, 1])
            with col_audio:
                st.audio(audio_bytes, format='audio/mp3')
        except:
            pass

    with st.container(border=True):
        st.warning(t(f"under construction: {st.session_state.pagina_ativa}", sigla))

if __name__ == "__main__":
    main()
