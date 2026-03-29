r"""

yPoemas is an app that randomly collects words and phrases
from specific databases and organizes them
in different new poems or poetic texts.

All texts are unique and will only be repeated  
after they are sold out the thourekasands  
of combinations possible to each theme.

[Epitaph]
Passei boa parte da minha vida escrevendo a "machina".
A leitura fica para os amanhãs.
Não vivo no meu tempo.

º¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°

ツpoemas

AlfaBetaAção == C:/WINDOWS/new.ini
config.toml  == C:/Users/dkvece/.streamlit

https://ypoemas-production.up.railway.app/share : https://share.streamlit.io/
deploy: https://share.streamlit.io/nandoulopes/ypoemas/main/ypo.py
runnin: https://nandoulopes-ypoemas-ypo-gf4z3l.streamlitapp.com/
config: chrome://settings/content/siteDetails?site=https%3A%2F%2Fauth.streamlit.io
github: https://github.com/NandouLopes/yPoemas
instag: https://www.instagram.com/maquina_de_fazer_ypoemas/
youtub: https://youtu.be/uL6T3roTtAs
google: https://console.cloud.google.com/welcome?project=ypoemas&cloudshell=false
prosas: https://prosas.com.br/dashboards/my-proposals
bairro: https://www.superbairro.com.br/joseense-cria-maquina-de-produzir-poemas-2/

para novos temas:
- incluir novo_tema em /ypo/base/ativos.txt
- incluir novo_tema em /ypo/base/images.txt
- incluir novo_tema em /ypo/temp/readings.txt
- incluir novo_tema em /base/rol_*.txt
- atualizar ABOUT_NOTES.md se necessário...

VISY == New Visitor
NANY_VISY == Number of Visitors
LYPO == Last YPOema created from curr_ypoema
TYPO == Translated YPOema from LYPO
POLY == Poliglot Idiom == Changed on Catalán

One more test...
"""

import os
import re
import time
import random
import base64
import socket

import streamlit as st

st.cache_data.clear() # Limpa a memória de 4 anos atrás

import os
import streamlit as st

# --- O TRILHO DEFINITIVO ---
# Pega a pasta onde o ypo.py está morando agora
this_folder = os.path.dirname(__file__)

# Define o caminho para a pasta data que você acabou de me mostrar
# 2. OS RAMAIS (Caminhos para as pastas)
path_data = os.path.join(this_folder, "data")
path_base = os.path.join(this_folder, "base")

# my_way: O caminho absoluto e seguro para o léxico
my_way = os.path.join(path_base, "lexico_pt.txt") # Ou o nome correto do seu léxico

import edge_tts
import asyncio

from extra_streamlit_components import TabBar as stx
from datetime import datetime
from lay_2_ypo import gera_poema

### bof: settings

# Inicialização Global - O alicerce da Torre
global LOGO_TEXTO, LOGO_IMAGE
LOGO_TEXTO = ""
LOGO_IMAGE = None

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        return False


if have_internet():
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        st.warning("Google Translator não encontrado no ambiente...")
    
    try:
        import edge_tts
        import asyncio
        # O gTTS não é mais estritamente necessário se usarmos o Edge, 
        # mas se quiser mantê-lo como "plano B", pode deixar aqui.
    except ImportError:
        st.warning("Motor de voz neural (edge-tts) não conectado.")
else:
    st.warning("Internet não conectada. Traduções e Vozes Neurais indisponíveis.")
    
# the User IPAddres for LYPO, TYPO
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# hide Streamlit Menu and Footer
st.markdown( """ <style>
    /*#MainMenu {visibility: hidden;}*/
    footer {visibility: hidden;}
    </style> """,
    unsafe_allow_html=True,
)


# change padding between components
st.markdown(
    f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {0}rem;
        padding-right: {0}rem;
        padding-left: {0}rem;
        padding-bottom: {0}rem;
    }} </style> """,
    unsafe_allow_html=True,
)


# change sidebar width
st.markdown(
    """ 
    <style>
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 310px;
    }
    </style> """,
    unsafe_allow_html=True,
)


# load_poema settings
st.markdown(
    """
    <style>
    mark {
      background-color: powderblue;
      color: black;
    }
    .container {
        display: flex;
        /* justify-content: center; */
    }

    .header {
        text-align:center;
    }
    .logo-text {
        font-weight: 600;
        font-size: 18px;
        font-family: 'IBM Plex Sans';
        color: #000000;
        padding-top: 0px;
        padding-left: 15px;
    }
    .logo-img {
        float:right;
    }
    </style> """,
    unsafe_allow_html=True,
)


# Initialize SessionState

if "lang" not in st.session_state:
    st.session_state.lang = "pt"
if "last_lang" not in st.session_state:
    st.session_state.last_lang = "pt"

if "book" not in st.session_state:  #  index for books_list
    st.session_state.book = "livro vivo"
if "take" not in st.session_state:  #  index for selected tema in books_list
    st.session_state.take = 0
if "mini" not in st.session_state:  #  index for selected tema in page_mini
    st.session_state.mini = 0
if "tema" not in st.session_state:  #  selected tema for all pages
    st.session_state.tema = "Fatos"

if "off_book" not in st.session_state:  #  index for off_books_list
    st.session_state.off_book = 0
if "off_take" not in st.session_state:  #  index for selected book in off_books_list
    st.session_state.off_take = 0

if "eureka" not in st.session_state:  #  index for random tema in page_eureka
    st.session_state.eureka = 0

if "poly_lang" not in st.session_state:
    st.session_state.poly_lang = "ca"
if "poly_name" not in st.session_state:
    st.session_state.poly_name = "català"
if "poly_take" not in st.session_state:
    st.session_state.poly_take = 12
if "poly_file" not in st.session_state:
    st.session_state.poly_file = "poly_pt.txt"

if "visy" not in st.session_state:
    st.session_state.visy = True
if "nany_visy" not in st.session_state:
    st.session_state.nany_visy = 0

if "draw" not in st.session_state:
    st.session_state.draw = False
if "talk" not in st.session_state:
    st.session_state.talk = False
if "vydo" not in st.session_state:
    st.session_state.vydo = False
if "arts" not in st.session_state:
    st.session_state.arts = []
if "auto" not in st.session_state:
    st.session_state.auto = False
if "rand" not in st.session_state:
    st.session_state.rand = False
if "poema_atual" not in st.session_state:
    st.session_state.poema_atual = ""

### eof: settings
### bof: tools


def translate(input_text):
    if st.session_state.lang == "pt":  # don't need translations here
        return input_text

    if not have_internet():
        st.session_state.lang = "pt"
        return input_text

    try:
        output_text = GoogleTranslator(
            source="pt", target=st.session_state.lang
        ).translate(text=input_text)

        output_text = output_text.replace("<br>>", "<br>")
        output_text = output_text.replace("< br>", "<br>")
        output_text = output_text.replace("<br >", "<br>")
        output_text = output_text.replace("<br ", "<br>")
        output_text = output_text.replace(" br>", "<br>")
        return output_text
    except:
        return translate("Arquivo muito grande para ser traduzido.")


def show_icons():  # links de contato
    with st.sidebar:
        st.markdown(
            f"""
            <nav style='text-align: center;'>
            <a href='https://www.facebook.com/nandoulopes' target='_blank'>• facebook</a> |
            <a href='mailto:lopes.fernando@hotmail.com' target='_blank'>e-mail</a> |
            <a href='https://www.instagram.com/fernando.lopes.942/' target='_blank'>instagram</a> |
            <a href='https://web.whatsapp.com/send?phone=+5512991368181' target='_blank'>whatsapp</a>
            </nav>
            """,
            unsafe_allow_html=True
        ) # <-- O PARÊNTESE QUE FALTAVA ESTÁ AQUI!


def load_help_tips():
    help_list = []
    caminho_help = os.path.join("base", "helpers.txt")
    with open(caminho_help, "r", encoding="utf-8") as file:
        for line in file:
            help_list.append(line.strip())
    return help_list

# --- SEPARAÇÃO ---

def load_help(idiom):
    returns = []
    if idiom in "_pt_es_it_fr_en":
        helpers = load_help_tips()
        for line in helpers:
            pipe_line = line.split("|")
            # Verifica se a linha tem o formato esperado antes de acessar o índice
            if len(pipe_line) > 2 and pipe_line[1].startswith(idiom + "_"):
                text = pipe_line[2]
                returns.append(text)
    else:
        # Se o idioma não for um dos fixos, usa a tradução automática
        returns.append(translate("anterior"))
        returns.append(translate("escolhe tema ao acaso"))
        returns.append(translate("próximo"))
        returns.append(translate("mais lidos..."))
        returns.append(translate("gera novo yPoema"))
        returns.append(translate("imagem"))
        returns.append(translate("áudio"))
        returns.append(translate("vídeo"))

    return returns
    

def draw_check_buttons():
    draw_text, talk_text, vyde_text = st.sidebar.columns([3.8, 3.2, 3])
    help_tips = load_help(st.session_state.lang)
    help_draw = help_tips[5]
    help_talk = help_tips[6]
    help_vyde = help_tips[7]
    st.session_state.draw = draw_text.checkbox(
        help_draw, st.session_state.draw, key="draw_machina"
    )
    st.session_state.talk = talk_text.checkbox(
        help_talk, st.session_state.talk, key="talk_machina"
    )
    st.session_state.vydo = vyde_text.checkbox(
        help_vyde, st.session_state.vydo, key="vyde_machina"
    )


def get_binary_file_downloader_html(bin_file, file_label="File"):
    with open(bin_file, "rb") as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">download {file_label}</a>'

    return href


def atoi(text):  # human reading number functions for sorting
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r"(\d+)", text)]


### eof: tools
### bof: update themes readings


@st.cache_data(show_spinner=False)
def update_visy():  # count one more visitor
    with open(os.path.join("./temp/visitors.txt"), "r", encoding="utf-8") as visitors:
        tots = int(visitors.read())
        tots = tots + 1
        st.session_state.nany_visy = tots

    with open(os.path.join("./temp/visitors.txt"), "w", encoding="utf-8") as visitors:
        visitors.write(str(tots))

    visitors.close()


@st.cache_data(show_spinner=False)
def load_readings():
    readers_list = []
    with open(os.path.join("./temp/read_list.txt"), encoding="utf-8") as reader:
        for line in reader:
            readers_list.append(line)
    reader.close()

    return readers_list


def update_readings(tema):
    read_changes = []
    readings = load_readings()
    for line in readings:
        pipe_line = line.split("|")
        name = pipe_line[1]
        if name == tema:
            qtds = int(pipe_line[2]) + 1
            new_line = "|" + name + "|" + str(qtds) + "|\n"
            read_changes.append(new_line)
        else:
            read_changes.append(line)

    with open(
        os.path.join("./temp/read_list.txt"), "w", encoding="utf-8"
    ) as new_reader:
        for line in read_changes:
            new_reader.write(line)
    new_reader.close()


def list_readings():
    sum_all_days = 0
    read_days = []  # days
    readings = load_readings()
    for line in readings:
        pipe_line = line.split("|")
        name = pipe_line[1]
        qtds = pipe_line[2]
        sum_all_days += int(qtds)
        if qtds != "0":
            new_line = str(qtds) + " - " + name + "\n"
            read_days.append(new_line)

    read_days.sort(key=natural_keys, reverse=True)

    total_viewes = st.session_state.nany_visy
    currrent_day = datetime.now()
    begining_day = datetime(2021, 7, 6)
    days_of_runs = begining_day - currrent_day
    days_of_runs = abs(days_of_runs.days)
    views_by_day = total_viewes / days_of_runs
    reads_by_day = sum_all_days / total_viewes

    options = list(range(len(read_days)))
    st.selectbox(
        "↓  "
        + str(len(read_days))
        + " temas, "
        + str(sum_all_days)
        + " leituras por "
        + str(total_viewes)
        + " visitantes ( "
        + str(int(views_by_day))
        + " / "
        + f"{reads_by_day:.2}"
        + " )",
        options,
        format_func=lambda x: read_days[x],
        key="opt_readings",
    )


### eof: update themes readings
### bof: loaders


@st.cache_data(show_spinner=False)
def load_md_file(file):  # Open files for about's
    try:
        with open(os.path.join("./md_files/" + file), encoding="utf-8") as file_to_open:
            file_text = file_to_open.read()

        if not "rol_" in file.lower():  # do not translate theme
            file_text = translate(file_text)
    except:
        file_text = translate("ooops... arquivo ( " + file + " ) não pode ser aberto.")
        st.session_state.lang = "pt"

    return file_text


@st.cache_data(show_spinner=False)

def load_eureka(part_of_word):
    lexico_list = []
    with open(os.path.join("./base/lexico_pt.txt"), encoding="utf-8") as lista:
        for line in lista:
            this_line = line.strip("\n")
            part_line = this_line.partition(" : ")
            palas = part_line[0]
            if part_of_word.lower() in palas.lower():
                lexico_list.append(line)

    return lexico_list


@st.cache_data(show_spinner=False)
def load_temas(book):  # List of themes inside a Book
    book_list = []
    with open(
        os.path.join("./base/rol_" + book + ".txt"), "r", encoding="utf-8"
    ) as file:
        for line in file:
            line = line.replace(" ", "")
            book_list.append(line.strip("\n"))

    return book_list


@st.cache_data(show_spinner=False)
def load_info(nome_tema):
    with open(os.path.join("./base/" + "info.txt"), "r", encoding="utf-8") as file:
        result = "nonono"
        for line in file:
            if line.startswith("|"):
                pipe = line.split("|")
                if pipe[1].upper() == nome_tema.upper():
                    genero = pipe[2]
                    imagem = pipe[3]
                    qtd_versos = pipe[4]
                    qtd_wordin = pipe[5]
                    qtd_lexico = pipe[6]
                    qtd_itimos = pipe[7]
                    qtd_analiz = pipe[8]
                    qtd_cienti = pipe[9]
                    result = "<br>"
                    result += "<br>"
                    result += "<br>"
                    result += "Titulo: " + nome_tema + "<br>"
                    result += "Gênero: " + genero + "  " + "<br>"
                    result += "Imagem: " + imagem + "  " + "<br>"
                    result += "Versos: " + qtd_versos + "  " + "<br>"
                    result += "Verbetes no texto: " + qtd_wordin + "  " + "<br>"
                    result += "Verbetes  do Tema: " + qtd_lexico + "  " + "<br>"
                    result += "• Banco de Ítimos: " + qtd_itimos + "  " + "<br>"
                    result += "Análise : " + qtd_analiz + "  " + "<br>"
                    result += "Notação Científica: " + qtd_cienti + "  " + "<br>"
                    result += "<br>"

        return result


@st.cache_data(show_spinner=False)
def load_index():  # Load indexes numbers for all themes
    index_list = []
    with open(os.path.join("./md_files/ABOUT_INDEX.md"), encoding="utf-8") as lista:
        for line in lista:
            index_list.append(line)

    return index_list


@st.cache_data(show_spinner=False)
def load_lypo():  # Load last yPoema & replace '\n' with '<br>' for translator returned text
    lypo_text = ""
    lypo_user = "LYPO_" + IPAddres
    with open(os.path.join("./temp/" + lypo_user), encoding="utf-8") as script:
        for line in script:
            line = line.strip()
            lypo_text += line + "<br>"

    return lypo_text


@st.cache_data(show_spinner=False)
def load_typo():  # Load translated yPoema & clean translator returned bugs in text
    typo_text = ""
    typo_user = "TYPO_" + IPAddres
    with open(os.path.join("./temp/" + typo_user), encoding="utf-8") as script:
        for line in script:  # just 1 line
            line = line.strip()
            if " >" in line:
                line = line.replace(" >", "\n")
            elif "< " in line:
                line = line.replace("< ", "\n")
            elif " br " in line:
                line = line.replace(" br", "\n")
            elif "br " in line:
                line = line.replace("br ", "\n")
            elif " br" in line:
                line = line.replace(" br", "\n")
            line = line.replace("< <", ">")
            line = line.replace("> >", ">")
            typo_text += line + "<br>"

    return typo_text


def load_all_offs():
    all_books_off = [
        "a_torre_de_papel",
        "linguafiada",
        "livro_vivo",
        "faz_de_conto",
        "um_romance",
        "quase_que_eu_Poesia",
        "segredo_público",
    ]
    return all_books_off


def load_off_book(book):  # Load selected off_book
    book_full = []
    full_name = os.path.join("./off_machina/", book) + ".Pip"
    with open(full_name, encoding="utf-8") as file:
        for line in file:
            if line.startswith("|"):
                book_full.append(line)

    return book_full

def load_book_pages(book):  # Load Book pages for off_book
    book_pages = []
    for line in book:
        if line.startswith("<EOF>"):
            break

        if line.startswith("|"):  # only valid lines in PIP
            pipe_line = line.split("|")
            book_pages.append(pipe_line[1])

    return book_pages

def load_poema(tema, subtema=""):
    # 1. Construção do Caminho (Case Sensitive para Linux/Streamlit)
    tema_limpo = str(tema).capitalize().strip()
    caminho = os.path.join("data", f"{tema_limpo}.ypo")
    
    try:
        # 2. Abertura com Encoding Seguro (UTF-8 é vital para poesia)
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                conteudo = f.read()
                
                # 3. O Ponto de Falha: Verifique se o conteúdo subiu
                if conteudo.strip():
                    return conteudo
                else:
                    return "⚠️ O arquivo existe, mas a leitura retornou vácuo."
        else:
            return f"❌ Arquivo não encontrado no disco: {caminho}"
            
    except Exception as e:
        return f"💥 Colapso na lida do arquivo: {str(e)}"

@st.cache_data(show_spinner=False)
def load_images():
    images_list = []
    caminho = os.path.join("base", "images.txt") 
    
    with open(caminho, encoding="utf-8") as lista:
        for line in lista:
            images_list.append(line.strip()) 
            
    return images_list # <-- Agora retornando a lista corretamente!


def load_arts(nome_tema):
    # Select image for arts
    path = "./images/machina/"
    path_list = load_images()
    
    for line in path_list:
        if line.startswith(nome_tema):
            this_line = line.strip("\n")
            part_line = this_line.partition(" : ")
            if nome_tema == part_line[0]:
                path = "./images/" + part_line[2] + "/"
                break
    # Importante: você provavelmente vai querer dar um 'return path' aqui no final!
    # return path
    
    arts_list = []
    for file in os.listdir(path):
        if file.endswith(".jpg"):
            arts_list.append(file)

    sorte = random.randrange(0, len(arts_list))
    image = arts_list[sorte]

    if image in st.session_state.arts:  # insert new image
        while image in st.session_state.arts:
            sorte = random.randrange(0, len(arts_list))
            image = arts_list[sorte]
        st.session_state.arts.append(image)
        image = st.session_state.arts[-1]
    else:
        st.session_state.arts.append(image)

    if len(st.session_state.arts) > 36:  # remove first
        del st.session_state.arts[0]

    logo = path + image

    return logo

### eof: loaders
### bof: functions

# --- TESTE DE EMERGÊNCIA (O BYPASS) ---

st.write("--- DEBUG DA MACHINA ---")
st.write(f"Tema Atual: {st.session_state.tema}")
if LOGO_TEXTO:
    st.info(f"O Texto existe! Tamanho: {len(LOGO_TEXTO)} caracteres.")
    st.code(LOGO_TEXTO) # O st.code força uma moldura cinza, impossível de ficar invisível
else:
    st.error("O LOGO_TEXTO chegou vazio na entrega final!")
    
def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):  # ver save_img.py
    if LOGO_IMAGE == None:
        st.markdown(
            f"""
            <div class='container'>
                <p class='logo-text'>{LOGO_TEXTO}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class='container'>
                <img class='logo-img' src='data:image/jpg;base64,{base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()}'>
                <p class='logo-text'>{LOGO_TEXTO}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

def talk(text):
    # Limpeza para a voz não ler tags
    text_clean = text.replace("<br>", " ").replace("< br>", "").replace("<br >", "").replace("<br/>", " ")
    
    # Mapeamento de vozes neurais de alta qualidade
    voices = {
        "pt": "pt-BR-AntonioNeural",
        "en": "en-US-GuyNeural",
        "es": "es-ES-AlvaroNeural",
        "fr": "fr-FR-RemyNeural",
        "it": "it-IT-DiegoNeural"
    }
    selected_voice = voices.get(st.session_state.lang, "pt-BR-AntonioNeural")

    async def generate_audio():
        communicate = edge_tts.Communicate(text_clean, selected_voice)
        audio_bytes = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes += chunk["data"]
        return audio_bytes

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_output = loop.run_until_complete(generate_audio())
        st.audio(audio_output, format="audio/mp3")
    except Exception as e:
        st.error(f"Erro na voz neural: {e}")
        
    
def show_video(pagina):  # vídeo-tutorial da página
    st.sidebar.info(load_md_file("INFO_VYDE.md"))
    video_name = os.path.join("./base/" + "video_" + pagina + ".webm")
    video_file = open(video_name, "rb")
    video_byts = video_file.read()
    st.video(video_byts, format="webm")
    video_file.close()


def say_number(tema):  # search index title for eureka
    analise = "nonono"
    indexes = load_index()
    for line in indexes:
        if line.startswith(tema):
            this_line = line.strip("\n")
            part_line = this_line.partition(" : ")
            analise = part_line[2]
            break

    return translate(analise)


### eof: functions
### bof: pages


if st.session_state.visy:  # check visitor once; rand initial temas
    update_visy()

    temas_list = load_temas(st.session_state.book)
    maxy_ypoemas = len(temas_list)
    st.session_state.take = random.randrange(0, maxy_ypoemas)

    temas_list = load_temas("todos os temas")
    maxy_mini = len(temas_list)
    st.session_state.mini = random.randrange(0, maxy_mini)

    st.success(translate("bem vindo à **máquina de fazer Poesia...**"))
    st.session_state.draw = True
    st.session_state.visy = False


st.session_state.last_lang = st.session_state.lang


def page_mini():
    temas_list = load_temas("todos os temas")
    maxy_mini = len(temas_list)

    if st.session_state.mini > maxy_mini:  # just in case
        st.session_state.mini = 0

    foo1, more, rand, auto, foo2 = st.columns([4, 1, 1, 1, 4])

    help_tips = load_help(st.session_state.lang)
    help_rand = help_tips[1]
    help_more = help_tips[4]
    rand = rand.button("✻", help=help_rand)
    st.session_state.auto = auto.checkbox("auto")

    if st.session_state.auto:
        st.session_state.talk = False
        st.session_state.vydo = False
        with st.sidebar:
            wait_time = st.slider(translate("tempo de exibição (em segundos): "), 5, 60)

    if rand:
        st.session_state.rand = True
        st.session_state.mini = random.randrange(0, maxy_mini)
    else:
        st.session_state.rand = False

    st.session_state.tema = temas_list[st.session_state.mini]
    analise = say_number(st.session_state.tema)
    more = more.button("✚", help=help_more + " • " + analise)

    if more:
        st.session_state.rand = False

    lnew = True
    if st.session_state.vydo:
        lnew = False
        show_video("mini")
        update_readings("video_mini")
        st.session_state.vydo = False

    if lnew or st.session_state.auto:
        if st.session_state.rand:
            st.session_state.mini = random.randrange(0, maxy_mini)
            st.session_state.tema = temas_list[st.session_state.mini]

        if st.session_state.lang != st.session_state.last_lang:
            curr_ypoema = load_lypo()  # changes in lang, keep LYPO
        else:
            curr_ypoema = load_poema(st.session_state.tema, "")
            curr_ypoema = load_lypo()

        if st.session_state.lang != "pt":
            # 1. Carrega o original em PT
            poema_base = load_poema(str(temas_list[opt_take]), "") 
            
            # 2. Traduz (certifique-se de passar o idioma se mudamos a função)
            curr_ypoema = translate(poema_base)
            
            # 3. NORMALIZAÇÃO (O que o load_typo fazia, fazemos aqui na RAM)
            # Se o load_typo apenas trocava \n por <br>, faça aqui:
            curr_ypoema = curr_ypoema.replace("\n", "<br>")
            
            # 4. Grava o backup se quiser, mas NÃO use ele para a exibição agora
            typo_user = "TYPO_" + IPAddres
            with open(os.path.join("./temp/" + typo_user), "w", encoding="utf-8") as save_typo:
                save_typo.write(curr_ypoema)
            
            # REGRAS DE OURO: 
            # NÃO chame curr_ypoema = load_typo() aqui! 
            # O poema já está na variável curr_ypoema.
        update_readings(st.session_state.tema)
        LOGO_TEXTO = curr_ypoema
        LOGO_IMAGE = None

        if st.session_state.draw:
            LOGO_IMAGE = load_arts(st.session_state.tema)

        mini_place_holder = st.empty()
        mini_place_holder.empty()
        st.write("")

        if st.session_state.auto == False:
            with mini_place_holder:
                write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

            if st.session_state.talk:
                talk(curr_ypoema)

        else:
            while st.session_state.auto:
                if st.session_state.rand:
                    st.session_state.mini = random.randrange(0, maxy_mini)
                    st.session_state.tema = temas_list[st.session_state.mini]

                if st.session_state.lang != st.session_state.last_lang:
                    curr_ypoema = load_lypo()  # changes in lang, keep LYPO
                else:
                    curr_ypoema = load_poema(st.session_state.tema, "")
                    curr_ypoema = load_lypo()

                if st.session_state.lang != "pt":  # translate if idioma <> pt
                    curr_ypoema = translate(curr_ypoema)
                    typo_user = "TYPO_" + IPAddres
                    with open(
                        os.path.join("./temp/" + typo_user), "w", encoding="utf-8"
                    ) as save_typo:
                        save_typo.write(curr_ypoema)
                        save_typo.close()
                    curr_ypoema = load_typo()  # to normalize line breaks in text

                update_readings(st.session_state.tema)
                LOGO_TEXTO = curr_ypoema
                LOGO_IMAGE = None

                if st.session_state.draw:
                    LOGO_IMAGE = load_arts(st.session_state.tema)

                with mini_place_holder:
                    mini_place_holder.empty()
                    write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
                    secs = wait_time
                    while secs >= 0:
                        time.sleep(1)
                        secs -= 1

def page_ypoemas():
    lnew_ypo = True
    LOGO_TEXTO = ""
    LOGO_IMAGE = None
    
    # --- 2. FORMATAÇÃO DO TEMA (O padrão: Tema_comum) ---
    tema_formatado = str(st.session_state.tema).capitalize()
    
    # Rótulo do Expander
    what_book = f"⚫ {st.session_state.lang} | {tema_formatado}"

    # --- 4. ENTREGA FINAL (O Palco) ---
    if LOGO_TEXTO:
        write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
    else:
        st.write("Aguardando o sopro da Machina...")
    
    # --- 1. O ALICERCE DE CONTROLE ---
    lnew_ypo = True    # Controla a geração/exibição do texto (.ypo)
    lnew_img = False   # Controla se a arte (load_arts) deve aparecer
    lnew_vydo = False  # Controla a exibição do vídeo
    
    # Inicialização das saídas
    LOGO_TEXTO = ""
    LOGO_IMAGE = None

    # --- 2. A LÓGICA DE INTERRUPÇÃO (Sensores) ---
    # Se o usuário clicou para ver o vídeo
    if st.session_state.vydo:
        lnew_vydo = True
        lnew_ypo = False # O vídeo "toma" o palco do texto
        
    # Se o modo de desenho estiver ativo
    if st.session_state.draw:
        lnew_img = True

    # --- 3. CONSTRUÇÃO E CARGA ---
# --- 1. PREPARAÇÃO DOS RÓTULOS (Sempre antes do uso) ---
    try:
        what_book = (
            "⚫ " + str(st.session_state.lang) + 
            " ( " + str(st.session_state.book) + " ) " +
            "( " + str(st.session_state.take + 1) + " / " + str(len(temas_list)) + " )"
        )
    except:
        what_book = "yPoemas - A Machina"

    
# --- 1. PREPARAÇÃO (Fora de qualquer 'if') ---
    LOGO_TEXTO = ""
    LOGO_IMAGE = None
    tema_formatado = str(st.session_state.tema).capitalize().strip()
    
    # Rótulo seguro
    try:
        what_book = f"⚫ {st.session_state.lang} ( {st.session_state.book} )"
    except:
        what_book = "yPoemas - A Machina"

    # --- 2. O BLOCO DE CONSTRUÇÃO ---
    if lnew_ypo:
        # CRIAMOS O EXPANDER DIRETAMENTE (Isso mata o UnboundLocalError)
        with st.expander(what_book, expanded=True):
            
            caminho_arquivo = os.path.join("data", f"{tema_formatado}.ypo")
            
            if os.path.exists(caminho_arquivo):
                try:
                    # TENTATIVA DE LEITURA DIRETA (Para testar se a load_poema falha)
                    with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as f:
                        conteudo = f.read()
                    
                    if conteudo.strip():
                        LOGO_TEXTO = conteudo
                    else:
                        # Se chegar aqui, o arquivo físico no GitHub está realmente sem texto
                        LOGO_TEXTO = f"⚠️ O arquivo '{caminho_arquivo}' existe mas está sem conteúdo."
                except Exception as e:
                    LOGO_TEXTO = f"💥 Erro ao abrir arquivo: {e}"
            else:
                LOGO_TEXTO = f"❌ Arquivo não encontrado: {caminho_arquivo}"

            # CARGA DA ARTE
            if st.session_state.draw:
                LOGO_IMAGE = load_arts(tema_formatado)

    # --- 3. ENTREGA FINAL (Fora do expander para garantir visibilidade) ---
    if LOGO_TEXTO:
        write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
    else:
        st.write("Aguardando o sopro da Machina...")

    
    # --- 4. A ENTREGA FINAL ---
    if LOGO_TEXTO:
        write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
    elif not lnew_vydo:
        st.write("Aguardando o sopro da Machina...")
        
    curr_ypoema = "" 
    LOGO_TEXTO = ""
    LOGO_IMAGE = None
    temas_list = load_temas(st.session_state.book)
    maxy_ypoemas = len(temas_list) - 1
    if (
        st.session_state.take > maxy_ypoemas or st.session_state.take < 0
    ):  # just in case
        st.session_state.take = 0

    foo1, more, last, rand, nest, manu, foo2 = st.columns([3, 1, 1, 1, 1, 1, 3])

    help_tips = load_help(st.session_state.lang)
    help_last = help_tips[0]
    help_rand = help_tips[1]
    help_nest = help_tips[2]
    help_more = help_tips[4]

    more = more.button("✚", help=help_more)
    last = last.button("◀", help=help_last)
    rand = rand.button("✻", help=help_rand)
    nest = nest.button("▶", help=help_nest)
    manu = manu.button("?", help="help !!!")

    if last:
        st.session_state.take -= 1
        if st.session_state.take < 0:
            st.session_state.take = maxy_ypoemas
            st.rerun()

    if rand:
        st.session_state.take = random.randrange(0, maxy_ypoemas)
        st.rerun()

    if nest:
        st.session_state.take += 1
        if st.session_state.take > maxy_ypoemas:
            st.session_state.take = 0

    if not st.session_state.draw:
        options = list(range(len(temas_list)))
        sobrios = "↓  " + translate("lista de Temas")
        opt_take = st.selectbox(
            sobrios,
            options,
            index=st.session_state.take,
            format_func=lambda z: temas_list[z],
            key="opt_take",
        )

        if opt_take != st.session_state.take:
            st.session_state.take = opt_take

    st.session_state.tema = temas_list[st.session_state.take]

    if LOGO_TEXTO:
        write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
    else:
        st.write("Aguardando o sopro da Machina...")   
        
    if manu:
        st.subheader(load_md_file("MANUAL_YPOEMAS.md"))

    if st.session_state.vydo:
        lnew_vydo = True
        lnew_ypo = False # O vídeo "toma" o palco do texto
        show_video("ypoemas")
        update_readings("video_ypoemas")
        st.session_state.vydo = False
   
    if lnew_ypo:
        with st.expander(what_book, expanded=True):
            # --- RASTREADOR DE CAMINHOS ---
            nome_arquivo = f"{st.session_state.tema}.ypo"
            caminho_tentado = os.path.join("data", nome_arquivo)
            
            # Verificação Real de Existência
            if os.path.exists(caminho_tentado):
                curr_ypoema = load_poema(str(st.session_state.tema), "")
            else:
                # Se cair aqui, o Python nos dirá ONDE ele procurou
                diretorio_atual = os.getcwd()
                arquivos_na_data = os.listdir("data") if os.path.exists("data") else "Pasta 'data' não encontrada!"
                
                curr_ypoema = (
                    f"❌ ERRO DE LOCALIZAÇÃO\n"
                    f"Arquivo buscado: {nome_arquivo}\n"
                    f"Diretório atual no Servidor: {diretorio_atual}\n"
                    f"Arquivos vistos na pasta 'data': {arquivos_na_data}"
                )

            LOGO_TEXTO = curr_ypoema
            
        with ypoemas_expander:
            # 2. Tente carregar o poema
            try:
                if st.session_state.lang != st.session_state.last_lang:
                    curr_ypoema = load_lypo()
                else:
                    curr_ypoema = load_poema(str(st.session_state.tema), "")
            except Exception as e:
                curr_ypoema = f"Erro ao carregar tema {st.session_state.tema}: {e}"

            # 3. Se ainda estiver vazio após o load, dê um susto na Machina
            if not curr_ypoema:
                curr_ypoema = "A página está em branco, aguardando o sopro..."
                LOGO_TEXTO = curr_ypoema
            

    if lnew_ypo:
        what_book = (
            "⚫  "
            + st.session_state.lang
            + " ( "
            + st.session_state.book
            + " ) ( "
            + str(st.session_state.take + 1)
            + " / "
            + str(len(temas_list))
            + " )"
        )

        ypoemas_expander = st.expander(what_book, expanded=True)
        with ypoemas_expander:
            LOGO_TEXTO = curr_ypoema 
            if st.session_state.draw:
                LOGO_IMAGE = load_arts(st.session_state.tema)

            if st.session_state.lang != st.session_state.last_lang:
                curr_ypoema = load_lypo()  # changes in lang, keep LYPO
            else:
                curr_ypoema = load_poema(str(st.session_state.tema), "")

            if st.session_state.lang != "pt":  # translate if idioma <> pt
                curr_ypoema = translate(curr_ypoema)
                typo_user = "TYPO_" + IPAddres
                with open(os.path.join("./temp/" + typo_user), "w", encoding="utf-8") as save_typo:
                    save_typo.write(curr_ypoema)
                    save_typo.close()
                    
                curr_ypoema = load_typo()  # to normalize line breaks in text

            update_readings(st.session_state.tema)
            LOGO_TEXTO = curr_ypoema
            LOGO_IMAGE = None
            if st.session_state.draw:
                LOGO_IMAGE = load_arts(st.session_state.tema)

            write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

            if manu:
                LOGO_TEXTO = load_info(st.session_state.tema)
                if st.session_state.lang != "pt":  # translate if idioma <> pt
                    LOGO_TEXTO = translate(LOGO_TEXTO)

                LOGO_IMAGE = (
                    "./images/matrix/" + st.session_state.tema.capitalize() + ".jpg"
                )
                write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

        if st.session_state.talk:
            talk(curr_ypoema)

        # st.markdown(get_binary_file_downloader_html('./temp/'+'LYPO_' + IPAddres, '➪ '+st.session_state.tema), unsafe_allow_html=True)


import streamlit as st
from lay_2_ypo import gera_poema  # Importando sua função com o 'return'

# --- ENGRENAGENS DE BUSCA (A Ferramenta) ---
def load_eureka(part_of_word):
    """
    Usa o 'my_way' para filtrar sementes no léxico.
    """
    lexico_list = []
    
    # O trilho my_way que definimos no topo do arquivo
    if os.path.exists(my_way):
        try:
            with open(my_way, "r", encoding="utf-8") as lista:
                for line in lista:
                    this_line = line.strip("\n")
                    # Filtra apenas o que o usuário digitou (part_of_word)
                    if part_of_word.lower() in this_line.lower():
                        lexico_list.append(this_line)
        except Exception as e:
            st.error(f"Erro ao ler o DNA da Machina: {e}")
            
    return lexico_list

def page_eureka():
    # Título simples, sem emojis ou termos complexos
    st.title("Gerador de Poemas")
    st.write("---")

    # 1. Seletor de Tema
    # Usei uma KEY nova para garantir que ele resete o estado anterior
    seed_tema = st.selectbox(
        "Selecione o Tema:", 
        lista_temas, 
        key="sb_eureka_limpo"
    )
    
    # 2. Input de Semente
    this_seed = st.text_input(
        "Semente (Número):", 
        "42", 
        key="ti_eureka_limpo"
    )

    # 3. Botão de Ação (Nome Simples: 'Criar Poema')
    if st.button("Criar Poema", key="btn_eureka_limpo"):
        # Chama a função que retorna a string
        poema_vivo = gera_poema(seed_tema, this_seed)
        
        # Exibição padrão do Streamlit (Fundo cinza claro, letra monoespaçada)
        st.text_area("Poema Gerado:", value=poema_vivo, height=400)
        
        st.write("---")
        
        # 4. Download
        st.download_button(
            label="Baixar Arquivo TXT",
            data=poema_vivo,
            file_name=f"{seed_tema}.txt",
            key="dl_eureka_limpo"
        )        
        
def page_euruka():
    # --- FAXINA VISUAL (Mata o Retângulo Azul e Bordas) ---
    st.markdown("""
        <style>
            .stAlert { background-color: transparent !important; border: none !important; }
            div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) { border: none !important; }
        </style>
    """, unsafe_allow_html=True)

    st.title("✨ Machina de Fazer Poesia")
    
    # Supondo que você tenha uma lista de temas ou um input
    lista_temas = ["Aolero", "Machbeth", "Tempo", "Amor", "Mar"] # Adicione os seus
    seed_tema = st.selectbox("Escolha o Horizonte Temático:", lista_temas)
    
    this_seed = st.text_input("Semente da Sorte (Opcional):", "42")

    if st.button("Gerar Poema Samizdát"):
        # --- O MILAGRE DA RAM (Sem arquivos .lypo) ---
        poema_vivo = gera_poema(seed_tema, this_seed)

        # Se houver tradução (opcional conforme seu código)
        # if st.session_state.get('lang', 'pt') != "pt":
        #    poema_vivo = translate(poema_vivo)

        st.markdown("---")
        
        # --- EXIBIÇÃO PURA (O fim do retângulo azul) ---
        corpo_html = poema_vivo.replace('\n', '<br>')
        
        st.markdown(f"""
            <div style="font-family:'Courier New', Courier, monospace; 
                        text-align:center; font-size:1.3em; 
                        line-height:1.6; color:#2c3e50; 
                        padding:20px; border:none; background:transparent;">
                <h2 style="color:#4B3621; border-bottom:1px solid #eee; padding-bottom:10px;">
                    * {seed_tema.upper()} *
                </h2>
                <p style="font-style: italic;">{corpo_html}</p>
            </div>
        """, unsafe_allow_html=True)

        # Download direto da memória
        st.download_button(
            label="📥 Baixar esta Pérola",
            data=poema_vivo,
            file_name=f"poema_{seed_tema.lower()}.txt",
            mime="text/plain"
        )

def page_off_machina():  # available off_machina_books
    off_books_list = load_all_offs()
    options = list(range(len(off_books_list)))
    sobrios = "↓  " + translate("lista de Livros")
    opt_off_book = st.selectbox(
        sobrios,
        options,
        index=st.session_state.off_book,
        format_func=lambda x: off_books_list[x],
        key="opt_off_book",
    )

    if opt_off_book != st.session_state.off_book:
        st.session_state.off_book = opt_off_book
        st.session_state.off_take = 0

    off_book_name = off_books_list[st.session_state.off_book]

    help_tips = load_help(st.session_state.lang)
    help_last = help_tips[0]
    help_rand = help_tips[1]
    help_nest = help_tips[2]
    help_love = help_tips[3]

    foo1, last, rand, nest, love, manu, foo2 = st.columns([2.5, 1, 1, 1, 1, 1, 2.5])
    last = last.button("◀", help=help_last)
    rand = rand.button("✻", help=help_rand)
    nest = nest.button("▶", help=help_nest)
    love = love.button("❤", help=help_love)
    manu = manu.button("?", help="help !!!")

    this_off_book = load_off_book(off_book_name)
    off_book_pagys = load_book_pages(this_off_book)
    maxy_off_machina = len(off_book_pagys) - 1

    if last:
        st.session_state.off_take -= 1
        if st.session_state.off_take < 0:
            st.session_state.off_take = maxy_off_machina

    if rand:
        st.session_state.off_take = random.randrange(0, maxy_off_machina)

    if nest:
        st.session_state.off_take += 1
        if st.session_state.off_take > maxy_off_machina:
            st.session_state.off_take = 0

    if st.session_state.off_take > maxy_off_machina:  # just in case...
        st.session_state.off_take = 0

    st.Rerun()

    if not st.session_state.draw:
        options = list(range(len(off_book_pagys)))
        sobrios = "↓  " + translate("lista de Títulos")
        opt_off_take = st.selectbox(
            sobrios,
            options,
            index=st.session_state.off_take,
            format_func=lambda x: off_book_pagys[x],
            key="opt_off_take",
        )

        if opt_off_take != st.session_state.off_take:
            st.session_state.off_take = opt_off_take

    lnew = True
    if manu:
        lnew = False
        st.subheader(load_md_file("MANUAL_OFF-MACHINA.md"))

    if love:
        lnew = False
        list_readings()
        st.markdown(
            get_binary_file_downloader_html("./temp/read_list.txt", "views"),
            unsafe_allow_html=True,
        )

    if st.session_state.vydo:
        lnew = False
        show_video("off-machina")
        update_readings("video_off-machina")
        st.session_state.vydo = False

    if lnew:
        what_book = (
            "⚫  "
            + st.session_state.lang
            + " ( "
            + str(st.session_state.off_take + 1)
            + "/"
            + str(len(off_book_pagys))
            + " )"
        )

        off_machina_expander = st.expander(what_book, True)
        with off_machina_expander:
            off_book_text = ""
            pipe_line = this_off_book[st.session_state.off_take].split("|")
            if "@ " in pipe_line[1]:
                if st.session_state.lang != st.session_state.last_lang:
                    off_book_text = load_lypo()  # changes in lang, keep LYPO
                else:
                    nome_tema = pipe_line[1].replace("@ ", "")
                    off_book_text = load_poema(nome_tema, "")  # no seed_eureka
                    off_book_text = "<br>" + load_lypo()
            else:
                for text in pipe_line:
                    off_book_text += text + "<br>"

            capo = st.session_state.off_take == 0

            if capo:
                capa, isbn = st.columns([2.5, 7.5])
                with capa:
                    if off_book_name == "livro_vivo":
                        LOGO_CAPA = load_arts("livro_vivo")
                        st.image(LOGO_CAPA, use_column_width=True)
                    else:
                        st.image(
                            "./off_machina/capa_" + off_book_name + ".jpg",
                            use_column_width=True,
                        )
                with isbn:
                    st.markdown(
                        off_book_text, unsafe_allow_html=True
                    )  # finally... write it
            else:
                if st.session_state.lang != "pt":
                    off_book_text = translate(off_book_text)

                LOGO_TEXTO = off_book_text
                LOGO_IMAGE = None
                if st.session_state.draw:
                    LOGO_IMAGE = load_arts(off_book_name)

                write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
                update_readings(off_book_name)

        if st.session_state.talk:
            talk(off_book_text)


def page_books():  # available books
    books, ok = st.columns([9.3, 0.7])
    with books:
        books_list = [
            "livro vivo",
            "poemas",
            "jocosos",
            "ensaios",
            "variações",
            "metalinguagem",
            "sociais",
            "todos os temas",
            "outros autores",
            "signos_fem",
            "signos_mas",
            "todos os signos",
        ]

        options = list(range(len(books_list)))
        sobrios = "↓  " + translate("lista de Livros")
        opt_book = st.selectbox(
            sobrios,
            options,
            index=books_list.index(st.session_state.book),
            format_func=lambda x: books_list[x],
            key="opt_book",
        )

        with ok:
            doit = st.button("✔", help="confirm ?")

        lnew = True
        if st.session_state.vydo:
            lnew = False
            show_video("books")
            update_readings("video_books")
            st.session_state.vydo = False

        if lnew:
            list_book = ""
            temas_list = load_temas(books_list[opt_book])
            for line in temas_list:
                list_book += line.strip() + ", "
            st.write(list_book[:-2] + " ▶ " + str(int(len(temas_list))) + " páginas")

            books_expander = st.expander("", True)
            with books_expander:
                st.subheader(load_md_file("MANUAL_BOOKS.md"))

            if doit:
                st.session_state.take = 0
                st.session_state.book = books_list[opt_book]


def page_polys():  # available languages
    polys, ok = st.columns([9.3, 0.7])
    with polys:
        poly_list = []
        poly_pais = []
        poly_ling = []
        with open(
            os.path.join("./base/" + st.session_state.poly_file), encoding="utf-8"
        ) as poly:
            for line in poly:
                poly_list.append(line)
                this_line = line.strip("\n")
                part_line = this_line.partition(" : ")
                poly_pais.append(translate(part_line[0]))
                poly_ling.append(part_line[2])
        poly.close()

        options = list(range(len(poly_list)))
        opt_poly = st.selectbox(
            "↓  lista: " + str(len(poly_list)) + " idiomas",
            options,
            index=st.session_state.poly_take,
            format_func=lambda x: poly_list[x],
            key="opt_poly",
        )

    with ok:
        doit = st.button("✔", help="confirm ?")

    lnew = True
    if st.session_state.vydo:
        lnew = False
        show_video("poly")
        update_readings("video_poly")
        st.session_state.vydo = False

    if doit:
        poly_pais = poly_pais[opt_poly]
        poly_ling = poly_ling[opt_poly]
        st.session_state.poly_name = translate(poly_pais)
        st.session_state.poly_lang = poly_ling
        st.session_state.poly_take = opt_poly

        st.session_state.last_lang = st.session_state.lang
        st.session_state.lang = st.session_state.poly_lang

    if lnew:
        poly_expander = st.expander("", True)
        with poly_expander:
            st.subheader(load_md_file("MANUAL_POLY.md"))


def page_abouts():
    abouts_list = [
        "comments",
        "prefácio",
        "machina",
        "off-machina",
        "outros",
        "traduttore",
        "bibliografia",
        "imagens",
        "samizdát",
        "notes",
        "license",
        "index",
    ]


    options = list(range(len(abouts_list)))
    sobrios = "↓  " + translate("sobre")
    opt_abouts = st.selectbox(
        sobrios,
        options,
        format_func=lambda x: abouts_list[x],
        key="opt_abouts",
    )

    lnew = True
    if st.session_state.vydo:
        lnew = False
        show_video("about")
        update_readings("video_about")
        st.session_state.vydo = False

    if lnew:
        choice = abouts_list[opt_abouts].upper()
        about_expander = st.expander("", True)
        with about_expander:
            if choice == "MACHINA":
                st.subheader(load_md_file("ABOUT_MACHINA_A.md"))
                LOGO_TEXTO = load_info(st.session_state.tema)
                LOGO_IMAGE = "./images/matrix/" + st.session_state.tema + ".jpg"
                write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
                st.subheader(load_md_file("ABOUT_MACHINA_D.md"))
            else:
                st.subheader(load_md_file("ABOUT_" + choice + ".md"))


### eof: pages


def main():
    chosen_id = stx.tab_bar(
        data=[
            stx.TabBarItemData(id=1, title="mini", description=""),
            stx.TabBarItemData(id=2, title="yPoemas", description=""),
            stx.TabBarItemData(id=3, title="eureka", description=""),
            stx.TabBarItemData(id=4, title="off-machina", description=""),
            stx.TabBarItemData(id=5, title="books", description=""),
            stx.TabBarItemData(id=6, title="poly", description=""),
            stx.TabBarItemData(id=7, title="about", description=""),
        ],
        default=2,
    )

   
    draw_check_buttons()

    if chosen_id == "1":
        st.sidebar.info(load_md_file("INFO_MINI.md"))
        magy = "img_mini.jpg"
        page_mini()
    elif chosen_id == "2":
        st.sidebar.info(load_md_file("INFO_YPOEMAS.md"))
        magy = "img_ypoemas.jpg"
        page_ypoemas()
    elif chosen_id == "3":
        st.sidebar.info(load_md_file("INFO_EUREKA.md"))
        magy = "img_eureka.jpg"
        page_eureka()
    elif chosen_id == "4":
        st.sidebar.info(load_md_file("INFO_OFF-MACHINA.md"))
        magy = "img_off-machina.jpg"
        page_off_machina()
    elif chosen_id == "5":
        st.sidebar.info(load_md_file("INFO_BOOKS.md"))
        magy = "img_books.jpg"
        page_books()
    elif chosen_id == "6":
        st.sidebar.info(load_md_file("INFO_POLY.md"))
        magy = "img_poly.jpg"
        page_polys()
    elif chosen_id == "7":
        st.sidebar.info(load_md_file("INFO_ABOUT.md"))
        magy = "img_about.jpg"
        page_abouts()
        ##$ page_docs()

    with st.sidebar:
        st.image(magy)

    st.sidebar.state = True

def pick_lang():
    # 1. Garante que as variáveis de estado existam
    if 'lang' not in st.session_state:
        st.session_state.lang = 'pt'
    if 'last_lang' not in st.session_state:
        st.session_state.last_lang = 'pt'
    if 'poly_name' not in st.session_state:
        st.session_state.poly_name = "Poliglota"

    # 2. Mapeamento Simples
    langs_info = {
        "Português": {"lang": "pt", "file": "poly_pt.txt"},
        "Español": {"lang": "es", "file": "poly_es.txt"},
        "Italiano": {"lang": "it", "file": "poly_it.txt"},
        "Français": {"lang": "fr", "file": "poly_fr.txt"},
        "English": {"lang": "en", "file": "poly_en.txt"},
        st.session_state.poly_name: {"lang": st.session_state.poly_lang, "file": st.session_state.poly_file}
    }
    
    lista_nomes = list(langs_info.keys())
    
    # 3. Encontra o índice do idioma atual para o Selectbox não resetar
    try:
        indice_atual = [v["lang"] for v in langs_info.values()].index(st.session_state.lang)
    except:
        indice_atual = 0

    # 4. O componente visual (Selectbox substitui os botões antigos)
    escolha_nome = st.sidebar.selectbox("Idioma / Language", options=lista_nomes, index=indice_atual)
    
    # 5. Lógica de troca (Executa apenas se mudar a seleção)
    info = langs_info[escolha_nome]
    if info["lang"] != st.session_state.lang:
        st.session_state.last_lang = st.session_state.lang
        st.session_state.lang = info["lang"]
        st.session_state.poly_file = info["file"]
        st.rerun()

# --- FIM DA FUNÇÃO ---

# CHAMADA DA FUNÇÃO (Fora do def, sem espaços na esquerda)
pick_lang()

if __name__ == "__main__":
    main()
