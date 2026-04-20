import streamlit as st
from pathlib import Path
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
import random

st.set_page_config(page_title="Machina", layout="wide", initial_sidebar_state="expanded")

BASE_DIR = Path(__file__).parent / "base"
YPO_DIR = Path(__file__).parent / "ypo"
IMG_DIR = Path(__file__).parent / "images"
PLACEHOLDER_IMG = IMG_DIR / "placeholder.jpg"
LYSTAS_FILE = BASE_DIR / "lystas.txt"

IDIOMAS = {
    'Português': 'pt', 'Espanhol': 'es', 'Italiano': 'it', 'Francês': 'fr',
    'Inglês': 'en', 'Catalão': 'ca', 'Córsico': 'co', 'Galego': 'gl',
    'Basco': 'eu', 'Esperanto': 'eo', 'Latin': 'la', 'Galês': 'cy',
    'Sueco': 'sv', 'Polonês': 'pl', 'Holandês': 'nl', 'Norueguês': 'no',
    'Finlandês': 'fi', 'Dinamarquês': 'da', 'Irlandês': 'ga',
    'Romeno': 'ro', 'Russo': 'ru'
}

LIVROS = [
    "metalinguagem", "livro vivo", "poemas", "ensaios", "jocosos", "variações",
    "sociais", "outros autores", "todos os temas",
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
if "lista_erros" not in st.session_state:
    st.session_state.lista_erros = []
if "mapa_temas" not in st.session_state:
    st.session_state.mapa_temas = None

def carregar_mapa_temas(): # [PRO]
    if st.session_state.mapa_temas is not None:
        return st.session_state.mapa_temas

    mapa = {}
    if LYSTAS_FILE.exists():
        try:
            with open(LYSTAS_FILE, "r", encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha or linha.startswith("#"): continue
                    if ":" in linha:
                        tema, categoria = linha.split(":", 1)
                        mapa[tema.strip()] = categoria.strip()
            st.session_state.lista_erros.append(f"DEBUG: lystas.txt carregado: {len(mapa)} mapeamentos")
        except Exception as e:
            st.session_state.lista_erros.append(f"ERRO: falha ao ler lystas.txt: {e}")
    else:
        st.session_state.lista_erros.append("AVISO: lystas.txt não encontrado. Mapeamento por nome de pasta.")

    st.session_state.mapa_temas = mapa
    return mapa

def buscar_arquivo_rol(nome_livro):
    variantes = [
        f"ROL_{nome_livro}.TXT", f"ROL_{nome_livro}.txt",
        f"rol_{nome_livro}.TXT", f"rol_{nome_livro}.txt"
    ]
    for v in variantes:
        caminho = BASE_DIR / v
        if caminho.exists():
            return caminho
    return None

def ler_arquivo_rol(nome_livro):
    st.session_state.lista_erros.clear()

    if not BASE_DIR.exists():
        st.session_state.lista_erros.append(f"ERRO: pasta base/ não existe em {BASE_DIR.parent}")
        return ["sem temas"], ["pasta base não encontrada"]

    caminho = buscar_arquivo_rol(nome_livro)
    st.session_state.lista_erros.append(f"DEBUG: buscando ROL_{nome_livro} com 4 variantes")

    if not caminho:
        st.session_state.lista_erros.append(f"ERRO: nenhuma variante de ROL_{nome_livro} encontrada")
        arquivos_base = [p.name for p in BASE_DIR.iterdir() if p.is_file()]
        st.session_state.lista_erros.append(f"Arquivos em base/: {arquivos_base}")
        return ["sem temas"], ["arquivo ROL não encontrado"]

    st.session_state.lista_erros.append(f"DEBUG: carregado {caminho.name}")

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as e:
        st.session_state.lista_erros.append(f"ERRO: falha ao ler {caminho}: {e}")
        return ["sem temas"], ["erro de leitura"]

    blocos = [b.strip() for b in conteudo.split("---") if b.strip()]
    if not blocos:
        st.session_state.lista_erros.append(f"ERRO: {caminho.name} sem separador ---")
        return ["sem temas"], ["arquivo sem blocos"]

    temas = [linha.strip() for linha in blocos[0].split("\n") if linha.strip()]
    paginas = blocos[1:] if len(blocos) > 1 else ["arquivo sem páginas"]

    if not temas:
        temas = ["sem temas"]
        st.session_state.lista_erros.append(f"ERRO: bloco 0 sem temas")
    if not paginas:
        paginas = ["arquivo sem páginas"]
        st.session_state.lista_erros.append(f"ERRO: sem páginas após ---")

    return temas, paginas

def buscar_imagem_tema(tema): # [PRO]
    mapa = carregar_mapa_temas()
    subpasta = mapa.get(tema)

    if not subpasta:
        if (IMG_DIR / tema).exists():
            subpasta = tema
        else:
            subpasta = "Machina"

    if tema == "sem temas":
        subpasta = "Machina"

    caminho_pasta = IMG_DIR / subpasta

    if not caminho_pasta.exists() or not caminho_pasta.is_dir():
        st.session_state.lista_erros.append(f"AVISO: pasta {caminho_pasta} não existe. Usando Machina.")
        caminho_pasta = IMG_DIR / "Machina"

    if not caminho_pasta.exists():
        return str(PLACEHOLDER_IMG) if PLACEHOLDER_IMG.exists() else None

    imagens = [p for p in caminho_pasta.iterdir() if p.suffix.lower() in EXT_IMG]
    if not imagens:
        st.session_state.lista_erros.append(f"AVISO: pasta {caminho_pasta} sem imagens.")
        return str(PLACEHOLDER_IMG) if PLACEHOLDER_IMG.exists() else None

    return str(random.choice(imagens))

def traduzir_texto(texto, idioma_destino):
    if idioma_destino == "pt" or not texto.strip():
        return texto
    try:
        return GoogleTranslator(source="auto", target=idioma_destino).translate(texto)
    except Exception as e:
        st.session_state.lista_erros.append(f"AVISO: falha tradução: {e}")
        return texto

def gerar_audio(texto, idioma):
    if not texto.strip():
        texto = "texto vazio"
    try:
        tts = gTTS(text=texto, lang=idioma, slow=False)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception as e:
        st.session_state.lista_erros.append(f"AVISO: falha áudio: {e}")
        return None

st.markdown("""
<style>
.stApp {background-color: #0e1117;}
.block-container {padding-top: 2rem; padding-bottom: 1rem;}
[data-testid="stSidebar"] > div:first-child {padding-top: 1rem;}
.main.block-container {background-color: #0e1117;}
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

    temas_validos = [t for t in TEMAS if t!= "sem temas"]
    if not temas_validos:
        temas_validos = ["sem temas"]

    if st.session_state.tema_selecionado not in temas_validos:
        st.session_state.tema_selecionado = temas_validos[0]

    if len(temas_validos) > 1 or temas_validos[0]!= "sem temas":
        tema_anterior = st.session_state.tema_selecionado
        st.session_state.tema_selecionado = st.selectbox(
            "Temas",
            options=temas_validos,
            index=temas_validos.index(st.session_state.tema_selecionado)
        )
        if tema_anterior!= st.session_state.tema_selecionado:
            st.session_state.pagina_atual = 0
            st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.art_ativo = st.toggle("Art", value=st.session_state.art_ativo)
    with col2:
        st.session_state.som_ativo = st.toggle("Som", value=st.session_state.som_ativo)

    if st.session_state.lista_erros:
        st.markdown("---")
        st.markdown("**DEBUG**")
        for erro in st.session_state.lista_erros:
            st.caption(erro)

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
            st.caption("sem imagem")
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
