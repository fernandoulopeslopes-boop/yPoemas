"""
main.py :: yPoemas / Machina

Primeiro CLEAN conservador.

Objetivo:
- manter o fluxo original conhecido pelo autor;
- preservar o Palco, LYPO, TYPO e o Eixo Z;
- reduzir ruído visual do código;
- preparar futura divisão em módulos sem quebrar a Machina.
"""

import os
import re
import time
import random
import base64
import socket
import asyncio
from datetime import datetime

import streamlit as st
from extra_streamlit_components import TabBar as stx

from lay_2_ypo import gera_poema

try:
    from core.padroes import (
        ABOUTS_LIST,
        BOOKS_LIST,
        LANG_FILES,
        OFF_BOOKS_LIST,
        PAGE_IMAGES,
        PAGE_INFO_FILES,
        VOICES_EDGE_TTS,
    )
except ImportError:
    # Fallback para manter o main.py executável mesmo antes de copiar core/padroes.py.
    ABOUTS_LIST = [
        "comments", "prefácio", "machina", "off-machina", "outros", "traduttore",
        "bibliografia", "imagens", "samizdát", "notes", "license", "index",
    ]
    BOOKS_LIST = [
        "livro vivo", "poemas", "jocosos", "ensaios", "variações", "metalinguagem",
        "sociais", "todos os temas", "outros autores", "signos_fem", "signos_mas",
        "todos os signos",
    ]
    OFF_BOOKS_LIST = [
        "a_torre_de_papel", "quase_que_eu_Poesia", "faz_de_conto", "um_romance",
        "linguafiada", "livro_vivo", "desvoto", "ensaio", "urbano", "essencial", "secreto",
    ]
    PAGE_IMAGES = {
        "1": "img_mini.jpg", "2": "img_ypoemas.jpg", "3": "img_eureka.jpg",
        "4": "img_off-machina.jpg", "5": "img_books.jpg", "6": "img_poly.jpg", "7": "img_about.jpg",
    }
    PAGE_INFO_FILES = {
        "1": "INFO_MINI.md", "2": "INFO_YPOEMAS.md", "3": "INFO_EUREKA.md",
        "4": "INFO_OFF-MACHINA.md", "5": "INFO_BOOKS.md", "6": "INFO_POLY.md", "7": "INFO_ABOUT.md",
    }
    LANG_FILES = {"pt": "poly_pt.txt", "es": "poly_es.txt", "it": "poly_it.txt", "fr": "poly_fr.txt", "en": "poly_en.txt"}
    VOICES_EDGE_TTS = {
        "pt": "pt-BR-AntonioNeural", "en": "en-US-GuyNeural", "es": "es-ES-AlvaroNeural",
        "fr": "fr-FR-RemyNeural", "it": "it-IT-DiegoNeural",
    }


# -----------------------------------------------------------------------------
# Configuração inicial da página Streamlit.
# Deve permanecer antes de qualquer saída visual do Streamlit.
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)


def have_internet(host="1.1.1.1", port=80, timeout=3):
    """Verifica conexão antes de ativar tradução e voz neural."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except OSError:
        return False


# Recursos externos opcionais.
GoogleTranslator = None
edge_tts = None

if have_internet():
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        st.warning("Google Translator não encontrado no ambiente...")

    try:
        import edge_tts
    except ImportError:
        st.warning("Motor de voz neural (edge-tts) não conectado.")
else:
    st.warning("Internet não conectada. Traduções e Vozes Neurais indisponíveis.")


# Identificador atual usado por LYPO/TYPO.
# Mantido neste CLEAN por preservar a persistência do último yPoema gerado.
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)


def apply_styles():
    """Aplica os estilos básicos da Machina e preserva o Palco sem controles."""
    st.markdown(
        """
        <style>
        /*#MainMenu {visibility: hidden;}*/
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        .reportview-container .main .block-container{
            padding-top: 0rem;
            padding-right: 0rem;
            padding-left: 0rem;
            padding-bottom: 0rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
            width: 310px;
        }
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] * {
            font-family: 'IBM Plex Sans', sans-serif !important;
        }
        [data-testid="stSidebar"] {
            font-size: 13px !important;
            line-height: 1.25 !important;
        }
        mark {
            background-color: powderblue;
            color: black;
        }
        .container {
            display: flex;
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
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_session_state():
    """Inicializa o estado vivo da Machina no Streamlit."""
    defaults = {
        "lang": "pt",
        "last_lang": "pt",
        "book": "livro vivo",
        "take": 0,
        "mini": 0,
        "tema": "Fatos",
        "off_book": 0,
        "off_take": 0,
        "eureka": 0,
        "poly_lang": "ca",
        "poly_name": "català",
        "poly_take": 12,
        "poly_file": "poly_pt.txt",
        "visy": True,
        "nany_visy": 0,
        "draw": False,
        "talk": False,
        "arts": [],
        "auto": False,
        "rand": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


apply_styles()
init_session_state()


### bof: tools



def translate(input_text):
    """Traduz textos de apoio e yPoemas quando o idioma atual não é português."""
    if st.session_state.lang == "pt":  # don't need translations here
        return input_text

    if not have_internet() or GoogleTranslator is None:
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
    except Exception:
        return "Arquivo muito grande para ser traduzido."


IDIOMAS_SEGUROS = [
    ("Português", "pt", "poly_pt.txt"),
    ("Español", "es", "poly_es.txt"),
    ("Italiano", "it", "poly_it.txt"),
    ("Français", "fr", "poly_fr.txt"),
    ("English", "en", "poly_en.txt"),
    ("Català", "ca", "poly_pt.txt"),
    ("Deutsch", "de", "poly_pt.txt"),
    ("Dansk", "da", "poly_pt.txt"),
    ("Esperanto", "eo", "poly_pt.txt"),
    ("Galego", "gl", "poly_pt.txt"),
    ("Latin", "la", "poly_pt.txt"),
    ("Íslenska", "is", "poly_pt.txt"),
    ("Nederlands", "nl", "poly_pt.txt"),
    ("Norsk", "no", "poly_pt.txt"),
    ("Polski", "pl", "poly_pt.txt"),
    ("Portuñol", "pt", "poly_pt.txt"),
    ("Română", "ro", "poly_pt.txt"),
    ("Русский", "ru", "poly_pt.txt"),
    ("Svenska", "sv", "poly_pt.txt"),
    ("Suomi", "fi", "poly_pt.txt"),
    ("Magyar", "hu", "poly_pt.txt"),
]


def pick_lang():  # define idioma
    labels = [item[0] for item in IDIOMAS_SEGUROS]
    codes = {label: code for label, code, _ in IDIOMAS_SEGUROS}
    files = {label: poly_file for label, _, poly_file in IDIOMAS_SEGUROS}

    current_label = next(
        (label for label, code, _ in IDIOMAS_SEGUROS if code == st.session_state.lang),
        "Português",
    )

    choice = st.sidebar.selectbox(
        "Idiomas disponíveis...",
        labels,
        index=labels.index(current_label),
        key="idioma_disponivel",
    )

    new_lang = codes[choice]
    new_poly_file = files[choice]

    if new_lang != st.session_state.lang:
        st.session_state.last_lang = st.session_state.lang
        st.session_state.lang = new_lang
        st.session_state.poly_file = new_poly_file
        st.success(translate("idioma atual") + " ➪ " + st.session_state.lang)


@st.cache_data
def load_help_tips():
    help_list = []
    with open(os.path.join("./base/helpers.txt"), encoding="utf-8") as file:
        for line in file:
            help_list.append(line)
    file.close()

    return help_list


def load_help(idiom):
    returns = []
    if idiom in "_pt_es_it_fr_en":
        helpers = load_help_tips()
        for line in helpers:
            pipe_line = line.split("|")
            if pipe_line[1].startswith(idiom + "_"):
                text = pipe_line[2]
                returns.append(text)
    else:
        returns.append(translate("anterior"))
        returns.append(translate("escolhe tema ao acaso"))
        returns.append(translate("próximo"))
        returns.append(translate("mais lidos..."))
        returns.append(translate("gera novo yPoema"))
        returns.append(translate("arte"))
        returns.append(translate("audio"))

    return returns


def draw_check_buttons():
    foo = ""
    draw_text, foo, foo, talk_text = st.sidebar.columns([4,1,1,4])
    help_tips = load_help(st.session_state.lang)
    help_draw = help_tips[5]
    help_talk = help_tips[6]
    st.session_state.draw = draw_text.checkbox(
        help_draw, st.session_state.draw, key="draw_machina"
    )
    st.session_state.talk = talk_text.checkbox(
        help_talk, st.session_state.talk, key="talk_machina"
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


def update_visy():  # count one more visitor
    with open(os.path.join("./temp/visitors.txt"), "r", encoding="utf-8") as visitors:
        tots = int(visitors.read())
        tots = tots + 1
        st.session_state.nany_visy = tots

    with open(os.path.join("./temp/visitors.txt"), "w", encoding="utf-8") as visitors:
        visitors.write(str(tots))

    visitors.close()


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


# @st.cache(allow_output_mutation=True)
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


# @st.cache(allow_output_mutation=True)
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


# @st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_temas(book):  # List of themes inside a Book
    book_list = []
    with open(
        os.path.join("./base/rol_" + book + ".txt"), "r", encoding="utf-8"
    ) as file:
        for line in file:
            line = line.replace(" ", "")
            book_list.append(line.strip("\n"))

    return book_list


# @st.cache(allow_output_mutation=True)
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

###< p1 >

