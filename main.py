import streamlit as st
import asyncio
from deep_translator import GoogleTranslator
import edge_tts
import os

# 1. TRADUÇÃO CIRÚRGICA
def t(texto, sigla_destino="pt"):
    protecao = {
        "arte": {"pt": "arte", "es": "arte", "it": "arte", "fr": "art", "en": "art", "ca": "art", "gl": "arte"},
        "som": {"pt": "som", "es": "sonido", "it": "suono", "fr": "son", "en": "sound"},
        "idiomas disponíveis": {"pt": "idiomas disponíveis", "es": "idiomas disponibles", "it": "lingue disponibili", "en": "available languages"}
    }
    chave = texto.lower().strip()
    if chave in protecao and sigla_destino in protecao[chave]:
        return protecao[chave][sigla_destino]
    try:
        return GoogleTranslator(source='auto', target=sigla_destino).translate(texto).lower()
    except:
        return texto.lower()

# 2. MOTOR DE ÁUDIO EM SEGUNDO PLANO
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
    # REINVENÇÃO DO ESTADO: Persistência absoluta
    for chave, valor in {"pagina_ativa": "mini", "som_ativo": False, "sigla_atual": "pt"}.items():
        if chave not in st.session_state: st.session_state[chave] = valor

    # ARQUITETURA GEOMÉTRICA (Sidebar 300px / Palco 98vw)
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] { width: 100vw !important; }
            .main .block-container { max-width: 98vw !important; width: 98vw !important; padding: 1rem !important; }
            [data-testid="stSidebar"] { min-width: 300px !important; width: 300px !important; }
            .sidebar-footer { text-align: center; font-size: 24px; padding-top: 20px; }
            .sidebar-footer a { margin: 0 10px; color: white !important; text-decoration: none; cursor: pointer; }
        </style>
    """, unsafe_allow_html=True)

    # CURADORIA DE IDIOMAS (Hierarquia de Castas)
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
    lista_idiomas = ["Português", "Espanhol", "Italiano", "Francês", "Inglês", "Catalão"] + sorted([k for k in mapa_linguas.keys() if k not in ["Português", "Espanhol", "Italiano", "Francês", "Inglês", "Catalão"]])

    # SINCRONIA LINGUÍSTICA
    sigla_para_nome = {v[0]: k for k, v in mapa_linguas.items()}
    index_idioma = lista_idiomas.index(sigla_para_nome.get(st.session_state.sigla_atual, "Português"))

    with st.sidebar:
        # Seletor sem reset
        selecao = st.selectbox(t("idiomas disponíveis", st.session_state.sigla_atual), lista_idiomas, index=index_idioma)
        sigla, voz_ativa = mapa_linguas[selecao]
        st.session_state.sigla_atual = sigla

        c1, c2 = st.columns(2)
        with c1: st.button(f"🎨 {t('arte', sigla)}")
        with c2: 
            if st.button(f"🔊 {t('som', sigla)}"): st.session_state.som_ativo = not st.session_state.som_ativo

        st.divider()
        
        # O PENSAMENTO: Injeção direta de conteúdo (Sem carcaças técnicas)
        nome_pg = st.session_state.pagina_ativa
        path_md = os.path.join(os.getcwd(), "md_files", f"info_{nome_pg}.md")
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        
        st.divider()

        # A VISÃO: Raiz do projeto
        path_img = os.path.join(os.getcwd(), f"img_{nome_pg}.JPG")
        if os.path.exists(path_img):
            st.image(path_img, use_column_width=True)

        st.markdown('<div class="sidebar-footer"><a>📘</a><a>📸</a><a>🐦</a><a>📺</a></div>', unsafe_allow_html=True)

    # O PALCO: Navegação Purificada
    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre"]
    cols = st.columns(len(paginas))
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"p_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

    # STATUS: Vida Real vs Construção
    if st.session_state.som_ativo:
        audio = asyncio.run(gerar_audio(t(nome_pg, sigla), voz_ativa))
        if audio: st.audio(audio, format='audio/mp3')

    with st.container(border=True):
        status = "vida real" if nome_pg in ["off-machina", "sobre"] else t("em construção", sigla)
        st.info(f"{nome_pg.upper()} — {status}")

if __name__ == "__main__":
    main()
