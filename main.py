import streamlit as st
import os
from pathlib import Path
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO

st.set_page_config(page_title="Machina", layout="wide")

BASE_DIR = Path(__file__).parent / "base"

IDIOMAS = {
    'Português': 'pt',
    'Espanhol': 'es',
    'Italiano': 'it',
    'Francês': 'fr',
    'Inglês': 'en',
    'Catalão': 'ca',
    'Córsico': 'co',
    'Galego': 'gl',
    'Basco': 'eu',
    'Esperanto': 'eo',
    'Latin': 'la',
    'Galês': 'cy',
    'Sueco': 'sv',
    'Polonês': 'pl',
    'Holandês': 'nl',
    'Norueguês': 'no',
    'Finlandês': 'fi',
    'Dinamarquês': 'da',
    'Irlandês': 'ga',
    'Romeno': 'ro',
    'Russo': 'ru'
}

LIVROS = [
    "livro vivo",
    "poemas",
    "ensaios",
    "jocosos",
    "variações",
    "metalinguagem",
    "sociais",
    "outros autores",
    "todos os temas",
    "todos os signos",
    "signos_fem",
    "signos_mas"
]

if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = 0
if "livro_selecionado" not in st.session_state:
    st.session_state.livro_selecionado = LIVROS[0]
if "idioma_selecionado" not in st.session_state:
    st.session_state.idioma_selecionado = "Português"
if "tema_selecionado" not in st.session_state:
    st.session_state.tema_selecionado = None

def ler_temas_livro(nome_livro):
    caminho = BASE_DIR / f"ROL_{nome_livro}.TXT"
    if not caminho.exists():
        return ["Sem temas"]
    with open(caminho, "r", encoding="utf-8") as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip()]
    return linhas if linhas else ["Sem temas"]

def carregar_paginas(nome_livro):
    caminho = BASE_DIR / f"ROL_{nome_livro}.TXT"
    if not caminho.exists():
        return ["Livro não encontrado."]
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()
    paginas = [p.strip() for p in conteudo.split("---") if p.strip()]
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
.stApp {background-color: #0e1117;}
.block-container {padding-top: 2rem; padding-bottom: 2rem;}
[data-testid="stSidebar"] > div:first-child {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Idioma")
    st.session_state.idioma_selecionado = st.selectbox(
        "Idioma",
        options=list(IDIOMAS.keys()),
        index=list(IDIOMAS.keys()).index(st.session_state.idioma_selecionado),
        label_visibility="collapsed"
    )

    st.markdown("### Livros")
    st.session_state.livro_selecionado = st.selectbox(
        "Livros",
        options=LIVROS,
        index=LIVROS.index(st.session_state.livro_selecionado),
        label_visibility="collapsed"
    )

    TEMAS = ler_temas_livro(st.session_state.livro_selecionado)
    if st.session_state.tema_selecionado not in TEMAS:
        st.session_state.tema_selecionado = TEMAS[0]

    st.markdown("### Temas")
    st.session_state.tema_selecionado = st.selectbox(
        "Temas",
        options=TEMAS,
        index=TEMAS.index(st.session_state.tema_selecionado),
        label_visibility="collapsed"
    )

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
