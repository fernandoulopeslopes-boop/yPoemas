import streamlit as st
import asyncio
from deep_translator import GoogleTranslator
import edge_tts
import os

# --- SISTEMA DE APOIO ---
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
    # 1. ESTADOS E CONSTANTES
    if 'pagina_ativa' not in st.session_state: st.session_state.pagina_ativa = "mini"
    if 'som_ativo' not in st.session_state: st.session_state.som_ativo = False
    if 'sigla_atual' not in st.session_state: st.session_state.sigla_atual = "pt"

    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre"]
    big_page_atual = st.session_state.pagina_ativa # A página em foco

    # 2. ARQUITETURA CSS DINÂMICA (A solução estética)
    # Aqui definimos que botões normais são 18px e o botão ativo é 24px
    st.markdown(f"""
        <style>
            [data-testid="stAppViewContainer"] {{ width: 100vw !important; }}
            .main .block-container {{ max-width: 98vw !important; width: 98vw !important; padding: 1rem !important; }}
            [data-testid="stSidebar"] {{ min-width: 300px !important; width: 300px !important; }}
            
            /* Estilo dos Botões de Navegação */
            div.stButton > button {{
                border: none !important;
                background-color: transparent !important;
                color: #888 !important;
                font-size: 18px !important; /* Tamanho das outras páginas */
                transition: all 0.3s ease;
                width: auto !important;
                padding: 0px 5px !important;
            }}

            /* Estilo Específico para a Página em Foco (Releitura) */
            /* Usamos um seletor que identifica o botão ativo pelo estado da Machina */
            div.stButton > button:has(div p:contains("{big_page_atual}")) {{
                color: white !important;
                font-size: 24px !important; /* Tamanho da página em foco */
                font-weight: bold !important;
                border-bottom: 2px solid white !important;
            }}
            
            .sidebar-footer {{ text-align: center; font-size: 24px; padding-top: 20px; }}
        </style>
    """, unsafe_allow_html=True)

    base_path = os.getcwd()
    
    # 3. SIDEBAR (Control Center)
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
    topo = ["Português", "Espanhol", "Italiano", "Francês", "Inglês", "Catalão"]
    outros = sorted([k for k in mapa_linguas.keys() if k not in topo])
    lista_idiomas = topo + outros

    sigla_para_nome = {{v[0]: k for k, v in mapa_linguas.items()}}
    index_idioma = lista_idiomas.index(sigla_para_nome.get(st.session_state.sigla_atual, "Português"))

    with st.sidebar:
        selecao = st.selectbox(t("idiomas disponíveis", st.session_state.sigla_atual), lista_idiomas, index=index_idioma)
        sigla, voz_ativa = mapa_linguas[selecao]
        st.session_state.sigla_atual = sigla

        c1, c2 = st.columns(2)
        with c1: st.button(f"🎨 {t('arte', sigla)}")
        with c2: 
            if st.button(f"🔊 {t('som', sigla)}"): st.session_state.som_ativo = not st.session_state.som_ativo

        st.divider()
        path_md = os.path.join(base_path, "md_files", f"info_{big_page_atual}.md")
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        
        st.divider()
        path_img = os.path.join(base_path, f"img_{big_page_atual}.JPG")
        if os.path.exists(path_img):
            st.image(path_img, use_column_width=True)

        st.markdown('<div class="sidebar-footer"><a>📘</a><a>📸</a><a>🐦</a><a>📺</a></div>', unsafe_allow_html=True)

    # 4. PALCO: NAVEGAÇÃO COM FOCO TIPOGRÁFICO
    # Criamos colunas dinâmicas para acomodar os diferentes tamanhos
    cols = st.columns([1.5 if pg == big_page_atual else 1 for pg in paginas])
    
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

    # 5. AUDIO E STATUS
    if st.session_state.som_ativo:
        audio = asyncio.run(gerar_audio(t(big_page_atual, sigla), voz_ativa))
        if audio: st.audio(audio, format='audio/mp3')

    with st.container(border=True):
        status = "vida real" if big_page_atual in ["off-machina", "sobre"] else t("em construção", sigla)
        st.info(f"{big_page_atual.upper()} — {status}")

if __name__ == "__main__":
    main()
