import streamlit as st
import asyncio
from deep_translator import GoogleTranslator
import edge_tts
import os

# 1. SISTEMA DE TRADUÇÃO (ESTRITAMENTE TEXTO PURO)
def t(texto, sigla_destino="pt"):
    try:
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

# 3. INTERFACE E LÓGICA
def main():
    if 'pagina_ativa' not in st.session_state:
        st.session_state.pagina_ativa = "mini"
    if 'som_ativo' not in st.session_state:
        st.session_state.som_ativo = False

    # CSS: PALCO EXPANSIVO, SIDEBAR 300px E RODAPÉ SOCIAL
    st.markdown("""
        <style>
            .main .block-container { 
                max-width: 100%; 
                padding: 2rem 5rem; 
            }
            [data-testid="stSidebar"] { 
                min-width: 300px !important;
                width: 300px !important; 
            }
            .stTitle { font-size: 2rem !important; }
            .stButton button { width: 100%; }
            .sidebar-footer {
                text-align: center;
                padding-top: 20px;
                font-size: 20px;
            }
            .sidebar-footer a { margin: 0 8px; text-decoration: none; }
        </style>
    """, unsafe_allow_html=True)

    # 4. ORGANIZAÇÃO DAS LÍNGUAS (TOP 6 + ALFABÉTICA)
    topo = ["Português", "Espanhol", "Italiano", "Francês", "Inglês", "Catalão"]
    outros = sorted([
        "Córsico", "Galego", "Basco", "Esperanto", "Latim", "Galês", "Sueco", 
        "Polonês", "Holandês", "Norueguês", "Finlandês", "Dinamarquês", 
        "Irlandês", "Romeno", "Russo"
    ])
    lista_idiomas = topo + outros

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

    # SIDEBAR: CENTRO DE CONTROLE
    with st.sidebar:
        # Idiomas e Help Context traduzidos
        idioma_nome = st.selectbox(
            t("idiomas disponíveis"), 
            lista_idiomas,
            help=t("selecione o idioma para tradução e áudio")
        )
        sigla, voz_ativa = mapa_linguas[idioma_nome]

        col1, col2 = st.columns(2)
        with col1: 
            st.button(f"🎨 {t('arte', sigla)}", help=t("visualizar mandalas e artes", sigla))
        with col2:
            label_audio = f"🔊 {t('áudio', sigla)}"
            if st.button(label_audio, help=f"{t('ouvir o', sigla)} {t('yPoemas', sigla)}"):
                st.session_state.som_ativo = not st.session_state.som_ativo

        st.divider()
        
        # Info dinâmico da página (.md)
        nome_pg = st.session_state.pagina_ativa
        st.markdown(f"#### info_{nome_pg}.md")
        
        # Tenta ler o arquivo markdown real
        if os.path.exists(f"info_{nome_pg}.md"):
            with open(f"info_{nome_pg}.md", "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.caption(t(f"contexto de {nome_pg} em construção...", sigla))
        
        # Arte correspondente à página (img_nome.JPG)
        nome_img = f"img_{nome_pg}.JPG"
        st.image(f"https://via.placeholder.com/260x260.png?text={nome_img}", use_column_width=True)

        # Rodapé Social
        st.markdown("""
            <div class="sidebar-footer">
                <a href="#">📘</a><a href="#">📸</a><a href="#">🐦</a><a href="#">📺</a>
            </div>
        """, unsafe_allow_html=True)

    # PALCO: NOMES ORIGINAIS EM PORTUGUÊS
    st.title(f"{t('a Machina de fazer Poesia', sigla)} / {nome_pg}")
    
    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre/about"]
    cols = st.columns(len(paginas))
    
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"palco_{pg}", help=t(pg, sigla)):
                st.session_state.pagina_ativa = pg
                st.rerun()

    # ÁUDIO (EDGE-TTS)
    if st.session_state.som_ativo:
        texto_ouvir = t(nome_pg, sigla)
        try:
            audio_bytes = asyncio.run(gerar_audio(texto_ouvir, voz_ativa))
            _, col_audio, _ = st.columns([1, 2, 1])
            with col_audio:
                st.audio(audio_bytes, format='audio/mp3')
        except:
            pass

    # MOLDURA DO PALCO
    with st.container(border=True):
        st.info(f"{nome_pg.upper()} — {t('em construção', sigla)}")

if __name__ == "__main__":
    main()
