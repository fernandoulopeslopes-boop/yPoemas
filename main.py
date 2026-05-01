import streamlit as st
import asyncio
from deep_translator import GoogleTranslator
import edge_tts
import os

# 1. SISTEMA DE TRADUÇÃO COM PROTEÇÃO LÉXICA
def t(texto, sigla_destino="pt"):
    protecao_lexica = {
        "arte": {"pt": "arte", "es": "arte", "it": "arte", "fr": "art", "en": "art", "ca": "art", "gl": "arte"},
        "áudio": {"pt": "áudio", "es": "audio", "it": "audio", "fr": "audio", "en": "audio"},
        "idiomas disponíveis": {"pt": "idiomas disponíveis", "es": "idiomas disponibles", "it": "lingue disponibili", "en": "available languages"}
    }
    chave = texto.lower().strip()
    if chave in protecao_lexica and sigla_destino in protecao_lexica[chave]:
        return protecao_lexica[chave][sigla_destino]
    try:
        tradutor = GoogleTranslator(source='auto', target=sigla_destino)
        return tradutor.translate(texto).lower()
    except:
        return texto.lower()

# 2. MOTOR DE VOZ
async def gerar_audio(texto, voz):
    try:
        communicate = edge_tts.Communicate(texto, voz)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        return audio_data
    except:
        return None

def main():
    if 'pagina_ativa' not in st.session_state:
        st.session_state.pagina_ativa = "mini"
    if 'som_ativo' not in st.session_state:
        st.session_state.som_ativo = False
    if 'sigla_atual' not in st.session_state:
        st.session_state.sigla_atual = "pt"

    # CSS: PALCO EXPANSIVO E SIDEBAR
    st.markdown("""
        <style>
            .main .block-container { max-width: 98% !important; padding: 1.5rem 2rem; }
            [data-testid="stSidebar"] { min-width: 300px !important; width: 300px !important; }
            .sidebar-footer { text-align: center; font-size: 26px; padding-top: 20px; }
            .sidebar-footer a { margin: 0 10px; text-decoration: none; }
        </style>
    """, unsafe_allow_html=True)

    # PASTAS CRIATIVOS_OBVIOS
    pasta_md = "md_files"
    pasta_jpg = "jpg_files"
    base_path = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # IDIOMAS CURADOS
    topo = ["Português", "Espanhol", "Italiano", "Francês", "Inglês", "Catalão"]
    outros = sorted(["Basco", "Córsico", "Dinamarquês", "Esperanto", "Finlandês", "Galego", "Galês", "Holandês", "Irlandês", "Latim", "Norueguês", "Polonês", "Romeno", "Russo", "Sueco"])
    lista_idiomas = topo + [i for i in outros if i not in topo]

    mapa_linguas = {
        "Português": ("pt", "pt-BR-AntonioNeural"), "Espanhol": ("es", "es-ES-AlvaroNeural"),
        "Italiano": ("it", "it-IT-DiegoNeural"), "Francês": ("fr", "fr-FR-HenriNeural"),
        "Inglês": ("en", "en-US-GuyNeural"), "Catalão": ("ca", "es-ES-AlvaroNeural"),
        "Basco": ("eu", "es-ES-AlvaroNeural"), "Córsico": ("co", "fr-FR-HenriNeural"),
        "Dinamarquês": ("da", "da-DK-JeppeNeural"), "Esperanto": ("eo", "en-US-GuyNeural"),
        "Finlandês": ("fi", "fi-FI-HarriNeural"), "Galego": ("gl", "es-ES-AlvaroNeural"),
        "Galês": ("cy", "en-GB-ThomasNeural"), "Holandês": ("nl", "nl-NL-MaartenNeural"),
        "Irlandês": ("ga", "en-IE-ConnorNeural"), "Latim": ("la", "it-IT-DiegoNeural"),
        "Norueguês": ("no", "nb-NO-FinnNeural"), "Polonês": ("pl", "pl-PL-MarekNeural"),
        "Romeno": ("ro", "ro-RO-EmilNeural"), "Russo": ("ru", "ru-RU-DmitryNeural"),
        "Sueco": ("sv", "sv-SE-MattiasNeural")
    }

    with st.sidebar:
        # BOTÕES DE IDIOMAS
        selecao = st.selectbox(t("idiomas disponíveis", st.session_state.sigla_atual), lista_idiomas)
        sigla, voz_ativa = mapa_linguas[selecao]
        st.session_state.sigla_atual = sigla

        col1, col2 = st.columns(2)
        with col1: st.button(f"🎨 {t('arte', sigla)}")
        with col2:
            if st.button(f"🔊 {t('áudio', sigla)}"):
                st.session_state.som_ativo = not st.session_state.som_ativo

        st.divider()
        
        # INFO_PAGINA
        nome_pg = st.session_state.pagina_ativa
        caminho_md = os.path.join(base_path, pasta_md, f"info_{nome_pg}.md")
        if os.path.exists(caminho_md):
            with open(caminho_md, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        
        st.divider()

        # IMG_PAGINA
        caminho_img = os.path.join(base_path, pasta_jpg, f"img_{nome_pg}.JPG")
        if os.path.exists(caminho_img):
            st.image(caminho_img, use_column_width=True)

        # REDES SOCIAIS
        st.markdown('<div class="sidebar-footer"><a>📘</a><a>📸</a><a>🐦</a><a>📺</a></div>', unsafe_allow_html=True)

    # PALCO
    st.title(f"{t('a Machina de fazer Poesia', sigla)} / {nome_pg}")
    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre"]
    cols = st.columns(len(paginas))
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"p_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

    # VIDA REAL: FIM DA "CONSTRUÇÃO" PARA OFF-MACHINA
    if st.session_state.som_ativo:
        audio = asyncio.run(gerar_audio(t(nome_pg, sigla), voz_ativa))
        if audio: st.audio(audio, format='audio/mp3')

    with st.container(border=True):
        status = "vida real" if nome_pg == "off-machina" else t("em construção", sigla)
        st.info(f"{nome_pg.upper()} — {status}")

if __name__ == "__main__":
    main()
