import streamlit as st
import os
import base64
from pathlib import Path
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO

st.set_page_config(page_title="Machina", layout="wide")

BASE_DIR = Path(__file__).parent / "base"

IDIOMAS = {
    "Português": "pt",
    "English": "en",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
    "Italiano": "it",
    "日本語": "ja",
    "中文": "zh-cn",
    "Русский": "ru",
    "العربية": "ar",
    "हिन्दी": "hi",
    "한국어": "ko",
    "Türkçe": "tr",
    "Nederlands": "nl",
    "Svenska": "sv",
    "Polski": "pl",
    "Ελληνικά": "el",
    "עברית": "he",
    "ไทย": "th",
    "Tiếng Việt": "vi",
    "Indonesia": "id"
}

TEMAS = [
    "Amizade",
    "Coragem",
    "Família",
    "Natureza",
    "Aventura",
    "Mistério",
    "Magia",
    "Animais",
    "Escola",
    "Sonhos"
]

if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = 0
if "livro_selecionado" not in st.session_state:
    st.session_state.livro_selecionado = None
if "idioma_selecionado" not in st.session_state:
    st.session_state.idioma_selecionado = "Português"
if "tema_selecionado" not in st.session_state:
    st.session_state.tema_selecionado = None

def listar_livros():
    arquivos = sorted(BASE_DIR.glob("rol_*.TXT"))
    return [arq.stem for arq in arquivos]

def carregar_paginas(livro):
    caminho = BASE_DIR / f"{livro}.TXT"
    if not caminho.exists():
        return ["Livro não encontrado."]
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()
    paginas = [p.strip() for p in conteudo.split("\n\n") if p.strip()]
    return paginas if paginas else ["Livro vazio."]

def traduzir_texto(texto, idioma_destino):
    if idioma_destino == "pt":
        return texto
    try:
        return GoogleTranslator(source="auto", target=idioma_destino).translate(texto)
    except:
        return texto

def gerar_audio(texto, idioma):
    try:
        tts = gTTS(text=texto, lang=idioma, slow=False)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except:
        return None

st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}
.tema-texto {
    background: none;
    border: none;
    color: #fafafa;
    text-align: left;
    padding: 0.25rem 0;
    width: 100%;
    cursor: pointer;
    font-size: 1rem;
}
.tema-texto:hover {
    color: #ff4b4b;
}
.tema-selecionado {
    color: #ff4b4b;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Idioma")
    idioma = st.selectbox(
        "Idioma",
        options=list(IDIOMAS.keys()),
        index=list(IDIOMAS.keys()).index(st.session_state.idioma_selecionado),
        label_visibility="collapsed"
    )
    st.session_state.idioma_selecionado = idioma

    st.markdown("### Temas")
    for tema in TEMAS:
        classe = "tema-selecionado" if tema == st.session_state.tema_selecionado else ""
        if st.button(tema, key=f"tema_{tema}", use_container_width=True):
            st.session_state.tema_selecionado = tema
            st.rerun()

    st.markdown("### Livros")
    livros = listar_livros()
    if livros:
        livro_idx = 0
        if st.session_state.livro_selecionado in livros:
            livro_idx = livros.index(st.session_state.livro_selecionado)
        livro = st.selectbox(
            "Livros",
            options=livros,
            index=livro_idx,
            label_visibility="collapsed"
        )
        st.session_state.livro_selecionado = livro
    else:
        st.write("Nenhum livro na base.")
        st.session_state.livro_selecionado = None

if st.session_state.livro_selecionado:
    paginas = carregar_paginas(st.session_state.livro_selecionado)
    total_paginas = len(paginas)

    if st.session_state.pagina_atual >= total_paginas:
        st.session_state.pagina_atual = 0

    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        if st.button("◀", disabled=st.session_state.pagina_atual == 0):
            st.session_state.pagina_atual -= 1
            st.rerun()

    with col3:
        if st.button("▶", disabled=st.session_state.pagina_atual >= total_paginas - 1):
            st.session_state.pagina_atual += 1
            st.rerun()

    with col2:
        st.markdown(f"**Página {st.session_state.pagina_atual + 1} de {total_paginas}**")

    texto_original = paginas[st.session_state.pagina_atual]
    idioma_codigo = IDIOMAS[st.session_state.idioma_selecionado]
    texto_traduzido = traduzir_texto(texto_original, idioma_codigo)

    st.markdown("---")
    st.write(texto_traduzido)

    audio = gerar_audio(texto_traduzido, idioma_codigo)
    if audio:
        st.audio(audio, format="audio/mp3")

    st.markdown("---")
    cols_paginas = st.columns(min(total_paginas, 10))
    for i in range(min(total_paginas, 10)):
        with cols_paginas[i]:
            if st.button(str(i + 1), key=f"pag_{i}"):
                st.session_state.pagina_atual = i
                st.rerun()
else:
    st.info("Selecione um livro na barra lateral para começar.")
