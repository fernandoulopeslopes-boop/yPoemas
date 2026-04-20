import streamlit as st
from pathlib import Path
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
import random

st.set_page_config(page_title="Machina", layout="wide")

BASE_DIR = Path(__file__).parent / "base"
YPO_DIR = Path(__file__).parent / "ypo"
IMG_DIR = Path(__file__).parent / "images"

IDIOMAS = {
    'Português': 'pt', 'Espanhol': 'es', 'Italiano': 'it', 'Francês': 'fr',
    'Inglês': 'en', 'Catalão': 'ca', 'Córsico': 'co', 'Galego': 'gl',
    'Basco': 'eu', 'Esperanto': 'eo', 'Latin': 'la', 'Galês': 'cy',
    'Sueco': 'sv', 'Polonês': 'pl', 'Holandês': 'nl', 'Norueguês': 'no',
    'Finlandês': 'fi', 'Dinamarquês': 'da', 'Irlandês': 'ga',
    'Romeno': 'ro', 'Russo': 'ru'
}

LIVROS = [
    "livro vivo", "poemas", "ensaios", "jocosos", "variações",
    "metalinguagem", "sociais", "outros autores", "todos os temas",
    "todos os signos", "signos_fem", "signos_mas"
]

EXT_IMG = {'.jpg', '.jpeg', '.png', '.webp'}

if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = 0
if "livro_selecionado" not in st.session_state:
    st.session_state.livro_selecionado = LIVROS[0]
if "idioma_selecionado" not in st.session_state:
    st.session_state.idioma_selecionado = "Português"
if "tema_selecionado" not in st.session_state:
    st.session_state.tema_selecionado = None
if "art_ativo" not in st.session_state:
    st.session_state.art_ativo = False
if "som_ativo" not in st.session_state:
    st.session_state.som_ativo = False

def ler_arquivo_rol(nome_livro):
    caminho = BASE_DIR / f"ROL_{nome_livro}.TXT"
    if not caminho.exists():
        return ["Sem temas"], ["Arquivo ROL_{nome_livro}.TXT não encontrado."]
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()
    blocos = [b.strip() for b in conteudo.split("---") if b.strip()]
    if not blocos:
        return ["Sem temas"], ["Livro vazio."]
    temas = [linha.strip() for linha in blocos[0].split("\n") if linha.strip()]
    paginas = blocos[1:] if len(blocos) > 1 else ["Sem conteúdo."]
    return temas if temas else ["Sem temas"], paginas

def ler_mapeamento_imagens():
    mapa = {}
    arq = YPO_DIR / "images.txt"
    if not arq.exists():
        return mapa
    with open(arq, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if " : " in linha:
                tema, pasta = linha.split(" : ", 1)
                mapa[tema.strip()] = pasta.strip()
    return mapa

def buscar_imagem_tema(tema):
    mapa = ler_mapeamento_imagens()
    subpasta = mapa.get(tema, "Machina")
    caminho_pasta = IMG_DIR / subpasta

    if not caminho_pasta.exists() or not caminho_pasta.is_dir():
        caminho_pasta = IMG_DIR / "Machina"

    if not caminho_pasta.exists():
        return None

    imagens = [p for p in caminho_pasta.iterdir() if p.suffix.lower() in EXT_IMG]
    if not imagens:
        caminho_pasta = IMG_DIR / "Machina"
        imagens = [p for p in caminho_pasta.iterdir() if p.suffix.lower() in EXT_IMG]
        if not imagens:
            return None

    return str(random.choice(imagens))

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
.block-container {padding-top: 2rem; padding-bottom: 1rem;}
[data-testid="stSidebar"] > div:first-child {padding-top: 1rem;}
</style>
""", unsafe_allow_html=True)

TEMAS, PAGINAS = ler_arquivo_rol(st.session_state.livro_selecionado)

with st.sidebar:
    st.session_state.idioma_selecionado = st.selectbox(
        "Idioma",
        options=list(IDIOMAS.keys()),
        index=list(IDIOMAS.keys()).index(st.session_state.idioma_selecionado)
    )

    livro_anterior = st.session_state.livro_selecionado
    st.session_state.livro_selecionado = st.selectbox(
        "Livros",
        options=LIVROS,
        index=LIVROS.index(st.session_state.livro_selecionado)
    )
    if livro_anterior!= st.session_state.livro_selecionado:
        st.session_state.pagina_atual = 0
        st.session_state.tema_selecionado = None
        st.rerun()

    if st.session_state.tema_selecionado not in TEMAS:
        st.session_state.tema_selecionado = TEMAS[0]

    st.session_state.tema_selecionado = st.selectbox(
        "Temas",
        options=TEMAS,
        index=TEMAS.index(st.session_state.tema_selecionado)
    )

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.art_ativo = st.toggle("Art", value=st.session_state.art_ativo)
    with col2:
        st.session_state.som_ativo = st.toggle("Som", value=st.session_state.som_ativo)

total_paginas = len(PAGINAS)
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
    st.markdown(f"<center><b>Página {st.session_state.pagina_atual + 1} de {total_paginas}</b></center>", unsafe_allow_html=True)

texto_original = PAGINAS[st.session_state.pagina_atual]
idioma_codigo = IDIOMAS[st.session_state.idioma_selecionado]
texto_traduzido = traduzir_texto(texto_original, idioma_codigo)

st.markdown("---")

if st.session_state.art_ativo:
    col_img, col_txt = st.columns([260, 1000])
    with col_img:
        img_path = buscar_imagem_tema(st.session_state.tema_selecionado)
        if img_path:
            st.image(img_path, width=240)
        else:
            st.caption("Sem imagem")
    with col_txt:
        st.write(texto_traduzido)
else:
    st.write(texto_traduzido)

if st.session_state.som_ativo:
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
