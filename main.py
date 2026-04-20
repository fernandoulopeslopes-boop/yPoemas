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

MAPA_TEMAS = {
    "Ais": "ensaio", "Amaré": "poesia", "Anjos": "author", "Aolero": "ensaio",
    "Arerir": "ensaio", "Astros": "ensaio", "Atido": "poesia", "Augusto": "author",
    "Avevida": "poesia", "Babel": "ensaio", "Batismo": "metalinguagem", "Beaba": "metalinguagem",
    "Becos": "poesia", "Blablabla": "metalinguagem", "Bolero": "poesia", "Brado": "joco",
    "Bula": "joco", "Cadência": "metalinguagem", "Cartaz": "joco", "Circular": "poesia",
    "Ciuminho": "poesia", "Clandestino": "poesia", "Clarice": "poesia", "Conto": "poesia",
    "Cordel": "metalinguagem", "Críticas": "joco", "Crítico": "author", "Cromossomo": "joco",
    "Cuores": "poesia", "Destinos": "poesia", "Distintos": "poesia", "Dolores": "poesia",
    "Duralex": "joco", "Elogio": "poesia", "Enfrente": "ensaio", "Epitafiando": "poesia",
    "Escriba": "poesia", "Essa": "metalinguagem", "Essas": "ensaio", "Esses": "ensaio",
    "Estudo": "joco", "Fatos": "poesia", "Feiras": "metalinguagem", "Festim": "poesia",
    "Finalmentes": "joco", "Frases": "joco", "Fugaz": "poesia", "Gula": "joco",
    "HaiKai": "poesia", "i-Mundo": "poesia", "Impar": "ensaio", "Indolor": "poesia",
    "Inhos": "poesia", "Insano": "joco", "Joker": "joco", "Lato": "poesia",
    "Leituras": "metalinguagem", "Liberta": "poesia", "Loremipsum": "ensaio", "Machbeth": "poesia",
    "Machbrait": "poesia", "Manifesto": "poesia", "Manusgrite": "metalinguagem", "Manusgrito": "metalinguagem",
    "Meteoro": "joco", "Minuto": "joco", "Mirante": "poesia", "Nonono": "ensaio",
    "Nós": "poesia", "Oca": "poesia", "Ocio": "joco", "Oco": "poesia",
    "Oficio": "joco", "Ogiva": "poesia", "Olhares": "poesia", "Palyndro": "ensaio",
    "Papilio": "poesia", "Paroles": "metalinguagem", "Passagens": "poesia", "Pedidos": "poesia",
    "Perfil": "joco", "Pessoa": "poesia", "Portal": "poesia", "Posfácio": "poesia",
    "Preciso": "poesia", "Prefácil": "poesia", "Psiu": "poesia", "Reger": "poesia",
    "Reinos": "joco", "Remedeio": "joco", "Rever": "poesia", "Restos": "poesia",
    "Rito": "joco", "Salute": "joco", "Saudades": "poesia", "Seguro": "joco",
    "Sentença": "joco", "Ser": "poesia", "Silente": "poesia", "Sinais": "poesia",
    "Sinas": "ensaio", "Sn6=ball": "ensaio", "Sn8=ball": "ensaio", "SnowBall": "ensaio",
    "Sonoro": "poesia", "Sopros": "poesia", "Sos": "joco", "Tempo": "poesia",
    "Tiro": "metalinguagem", "Tolero": "poesia", "Usinas": "poesia", "Veio": "poesia",
    "Victor": "poesia", "Vozes": "joco", "Zelo": "poesia", "Zodiacaos": "zodíaco",
    "Zoia": "poesia", "Aquarius=f": "zodíaco", "Aquarius=m": "zodíaco", "Aries=f": "zodíaco",
    "Aries=m": "zodíaco", "Cancer=f": "zodíaco", "Cancer=m": "zodíaco", "Caprico=f": "zodíaco",
    "Caprico=m": "zodíaco", "Escorpio=f": "zodíaco", "Escorpio=m": "zodíaco", "Gemeos=f": "zodíaco",
    "Gemeos=m": "zodíaco", "Leao=f": "zodíaco", "Leao=m": "zodíaco", "Libra=f": "zodíaco",
    "Libra=m": "zodíaco", "Peixes=f": "zodíaco", "Peixes=m": "zodíaco", "Sagitari=f": "zodíaco",
    "Sagitari=m": "zodíaco", "Touro=f": "zodíaco", "Touro=m": "zodíaco", "Virgem=f": "zodíaco",
    "Virgem=m": "zodíaco"
}

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
if "lista_erros" not in st.session_state: # [PRO]
    st.session_state.lista_erros = [] # [PRO]

def ler_arquivo_rol(nome_livro): # [PRO]
    st.session_state.lista_erros.clear() # [PRO]

    if " " not in nome_livro and nome_livro in ["livro vivo"]: # [PRO]
        st.session_state.lista_erros.append(f"ERRO: nome_do_livro '{nome_livro}' deveria ter espaço") # [PRO]
    if " " in nome_livro and nome_livro not in ["livro vivo", "outros autores", "todos os temas", "todos os signos"]: # [PRO]
        st.session_state.lista_erros.append(f"ERRO: nome_do_livro '{nome_livro}' não deveria ter espaço") # [PRO]

    caminho = BASE_DIR / f"ROL_{nome_livro}.TXT"
    if not caminho.exists():
        st.session_state.lista_erros.append(f"ERRO: arquivo não encontrado {caminho}") # [PRO]
        if BASE_DIR.exists(): # [PRO]
            arquivos_base = [p.name for p in BASE_DIR.iterdir() if p.is_file()] # [PRO]
            st.session_state.lista_erros.append(f"Arquivos em base/: {arquivos_base}") # [PRO]
        return ["sem temas"], ["erro ao carregar livro"] # [PRO]

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as e: # [PRO]
        st.session_state.lista_erros.append(f"ERRO: falha ao ler {caminho}: {e}") # [PRO]
        return ["sem temas"], ["erro ao carregar livro"] # [PRO]

    blocos = [b.strip() for b in conteudo.split("---") if b.strip()]
    if not blocos:
        st.session_state.lista_erros.append(f"ERRO: {caminho} vazio ou sem separador ---") # [PRO]
        return ["sem temas"], ["arquivo vazio"] # [PRO]

    temas = [linha.strip() for linha in blocos[0].split("\n") if linha.strip()]
    paginas = blocos[1:] if len(blocos) > 1 else ["sem páginas"]

    if not temas:
        temas = ["sem temas"]
        st.session_state.lista_erros.append(f"ERRO: {caminho} sem temas no bloco 0") # [PRO]
    if not paginas:
        paginas = ["sem páginas"]
        st.session_state.lista_erros.append(f"ERRO: {caminho} sem páginas após ---") # [PRO]

    return temas, paginas

def buscar_imagem_tema(tema):
    subpasta = MAPA_TEMAS.get(tema, "Machina")
    if tema == "sem temas":
        subpasta = "Machina"
    caminho_pasta = IMG_DIR / subpasta

    if not caminho_pasta.exists() or not caminho_pasta.is_dir():
        st.session_state.lista_erros.append(f"AVISO: pasta {caminho_pasta} não existe. Usando Machina.") # [PRO]
        caminho_pasta = IMG_DIR / "Machina"

    if not caminho_pasta.exists():
        return str(PLACEHOLDER_IMG) if PLACEHOLDER_IMG.exists() else None

    imagens = [p for p in caminho_pasta.iterdir() if p.suffix.lower() in EXT_IMG]
    if not imagens:
        st.session_state.lista_erros.append(f"AVISO: pasta {caminho_pasta} sem imagens.") # [PRO]
        return str(PLACEHOLDER_IMG) if PLACEHOLDER_IMG.exists() else None

    return str(random.choice(imagens))

def traduzir_texto(texto, idioma_destino):
    if idioma_destino == "pt" or not texto.strip():
        return texto
    try:
        return GoogleTranslator(source="auto", target=idioma_destino).translate(texto)
    except Exception as e: # [PRO]
        st.session_state.lista_erros.append(f"AVISO: falha tradução: {e}") # [PRO]
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
    except Exception as e: # [PRO]
        st.session_state.lista_erros.append(f"AVISO: falha áudio: {e}") # [PRO]
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

    if st.session_state.lista_erros: # [PRO]
        st.markdown("---") # [PRO]
        st.markdown("**DEBUG**") # [PRO]
        for erro in st.session_state.lista_erros: # [PRO]
            st.caption(erro) # [PRO]

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
