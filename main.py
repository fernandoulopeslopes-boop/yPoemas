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
PLACEHOLDER_IMG = IMG_DIR / "placeholder.jpg" # [PRO]

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

MAPA_TEMAS = { # [PRO]
    "Ais": "ensaio", "Amaré": "poesia", "Anjos": "author", "Aolero": "ensaio", # [PRO]
    "Arerir": "ensaio", "Astros": "ensaio", "Atido": "poesia", "Augusto": "author", # [PRO]
    "Avevida": "poesia", "Babel": "ensaio", "Batismo": "metalinguagem", "Beaba": "metalinguagem", # [PRO]
    "Becos": "poesia", "Blablabla": "metalinguagem", "Bolero": "poesia", "Brado": "joco", # [PRO]
    "Bula": "joco", "Cadência": "metalinguagem", "Cartaz": "joco", "Circular": "poesia", # [PRO]
    "Ciuminho": "poesia", "Clandestino": "poesia", "Clarice": "poesia", "Conto": "poesia", # [PRO]
    "Cordel": "metalinguagem", "Críticas": "joco", "Crítico": "author", "Cromossomo": "joco", # [PRO]
    "Cuores": "poesia", "Destinos": "poesia", "Distintos": "poesia", "Dolores": "poesia", # [PRO]
    "Duralex": "joco", "Elogio": "poesia", "Enfrente": "ensaio", "Epitafiando": "poesia", # [PRO]
    "Escriba": "poesia", "Essa": "metalinguagem", "Essas": "ensaio", "Esses": "ensaio", # [PRO]
    "Estudo": "joco", "Fatos": "poesia", "Feiras": "metalinguagem", "Festim": "poesia", # [PRO]
    "Finalmentes": "joco", "Frases": "joco", "Fugaz": "poesia", "Gula": "joco", # [PRO]
    "HaiKai": "poesia", "i-Mundo": "poesia", "Impar": "ensaio", "Indolor": "poesia", # [PRO]
    "Inhos": "poesia", "Insano": "joco", "Joker": "joco", "Lato": "poesia", # [PRO]
    "Leituras": "metalinguagem", "Liberta": "poesia", "Loremipsum": "ensaio", "Machbeth": "poesia", # [PRO]
    "Machbrait": "poesia", "Manifesto": "poesia", "Manusgrite": "metalinguagem", "Manusgrito": "metalinguagem", # [PRO]
    "Meteoro": "joco", "Minuto": "joco", "Mirante": "poesia", "Nonono": "ensaio", # [PRO]
    "Nós": "poesia", "Oca": "poesia", "Ocio": "joco", "Oco": "poesia", # [PRO]
    "Oficio": "joco", "Ogiva": "poesia", "Olhares": "poesia", "Palyndro": "ensaio", # [PRO]
    "Papilio": "poesia", "Paroles": "metalinguagem", "Passagens": "poesia", "Pedidos": "poesia", # [PRO]
    "Perfil": "joco", "Pessoa": "poesia", "Portal": "poesia", "Posfácio": "poesia", # [PRO]
    "Preciso": "poesia", "Prefácil": "poesia", "Psiu": "poesia", "Reger": "poesia", # [PRO]
    "Reinos": "joco", "Remedeio": "joco", "Rever": "poesia", "Restos": "poesia", # [PRO]
    "Rito": "joco", "Salute": "joco", "Saudades": "poesia", "Seguro": "joco", # [PRO]
    "Sentença": "joco", "Ser": "poesia", "Silente": "poesia", "Sinais": "poesia", # [PRO]
    "Sinas": "ensaio", "Sn6=ball": "ensaio", "Sn8=ball": "ensaio", "SnowBall": "ensaio", # [PRO]
    "Sonoro": "poesia", "Sopros": "poesia", "Sos": "joco", "Tempo": "poesia", # [PRO]
    "Tiro": "metalinguagem", "Tolero": "poesia", "Usinas": "poesia", "Veio": "poesia", # [PRO]
    "Victor": "poesia", "Vozes": "joco", "Zelo": "poesia", "Zodiacaos": "zodíaco", # [PRO]
    "Zoia": "poesia", "Aquarius=f": "zodíaco", "Aquarius=m": "zodíaco", "Aries=f": "zodíaco", # [PRO]
    "Aries=m": "zodíaco", "Cancer=f": "zodíaco", "Cancer=m": "zodíaco", "Caprico=f": "zodíaco", # [PRO]
    "Caprico=m": "zodíaco", "Escorpio=f": "zodíaco", "Escorpio=m": "zodíaco", "Gemeos=f": "zodíaco", # [PRO]
    "Gemeos=m": "zodíaco", "Leao=f": "zodíaco", "Leao=m": "zodíaco", "Libra=f": "zodíaco", # [PRO]
    "Libra=m": "zodíaco", "Peixes=f": "zodíaco", "Peixes=m": "zodíaco", "Sagitari=f": "zodíaco", # [PRO]
    "Sagitari=m": "zodíaco", "Touro=f": "zodíaco", "Touro=m": "zodíaco", "Virgem=f": "zodíaco", # [PRO]
    "Virgem=m": "zodíaco" # [PRO]
} # [PRO]

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
        return ["sem temas"], ["livro não encontrado"]
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except:
        return ["sem temas"], ["livro não encontrado"]

    blocos = [b.strip() for b in conteudo.split("---") if b.strip()]
    if not blocos:
        return ["sem temas"], ["livro não encontrado"]

    temas = [linha.strip() for linha in blocos[0].split("\n") if linha.strip()]
    paginas = blocos[1:] if len(blocos) > 1 else ["livro não encontrado"]

    if not temas:
        temas = ["sem temas"]
    if not paginas:
        paginas = ["livro não encontrado"]

    return temas, paginas

def buscar_imagem_tema(tema): # [PRO]
    subpasta = MAPA_TEMAS.get(tema, "Machina") # [PRO]
    if tema == "sem temas": # [PRO]
        subpasta = "Machina" # [PRO]
    caminho_pasta = IMG_DIR / subpasta # [PRO]

    if not caminho_pasta.exists() or not caminho_pasta.is_dir(): # [PRO]
        caminho_pasta = IMG_DIR / "Machina" # [PRO]

    if not caminho_pasta.exists(): # [PRO]
        return str(PLACEHOLDER_IMG) if PLACEHOLDER_IMG.exists() else None # [PRO]

    imagens = [p for p in caminho_pasta.iterdir() if p.suffix.lower() in EXT_IMG] # [PRO]
    if not imagens: # [PRO]
        return str(PLACEHOLDER_IMG) if PLACEHOLDER_IMG.exists() else None # [PRO]

    return str(random.choice(imagens)) # [PRO]

def traduzir_texto(texto, idioma_destino):
    if idioma_destino == "pt" or not texto.strip():
        return texto
    try:
        return GoogleTranslator(source="auto", target=idioma_destino).translate(texto)
    except:
        return texto

def gerar_audio(texto, idioma):
    if not texto.strip():
        texto = "livro não encontrado"
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

    temas_validos = [t for t in TEMAS if t!= "sem temas"] # [PRO]
    if not temas_validos: # [PRO]
        temas_validos = [TEMAS[0]] # [PRO]

    if st.session_state.tema_selecionado not in temas_validos: # [PRO]
        st.session_state.tema_selecionado = temas_validos[0] # [PRO]

    if len(temas_validos) > 1 or temas_validos[0]!= "sem temas": # [PRO]
        tema_anterior = st.session_state.tema_selecionado # [PRO]
        st.session_state.tema_selecionado = st.selectbox( # [PRO]
            "Temas", # [PRO]
            options=temas_validos, # [PRO]
            index=temas_validos.index(st.session_state.tema_selecionado) # [PRO]
        ) # [PRO]
        if tema_anterior!= st.session_state.tema_selecionado: # [PRO]
            st.session_state.pagina_atual = 0 # [PRO]
            st.rerun() # [PRO]

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
