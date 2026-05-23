"""
main.py :: yPoemas / Machina
CLEAN conservador + gramado/sidebar transplantados.

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
import unicodedata
from datetime import datetime

import streamlit as st
from extra_streamlit_components import TabBar as stx

from lay_2_ypo import gera_poema

# ABOUTS:
# Os arquivos da documentação são descobertos automaticamente em ./md_files
# pelo padrão ABOUT_*.md.
# A parte "ABOUT_" é a chave geral.
# O restante do nome, em lower, vira o título/menu da página About.
# Exceção: ABOUT_machina_A.md + ABOUT_machina_D.md formam um único item "machina".
ABOUTS_LIST = [
    "comments", "prefácil", "machina", "off-machina", "MACHINA-IA", "livros", "outros autores",
    "imagens", "traduttore", "bibliografia", "samizdát", "notes", "license", "index",
]

BOOKS_LIST = [
    "todos os temas", "livro vivo", "poemas", "jocosos", "ensaios", "sociais",
    "variações", "metalinguagem", "outros autores", "signos_fem", "signos_mas",
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

VOICES_EDGE_TTS = {
    "pt": "pt-BR-AntonioNeural",
    "en": "en-US-GuyNeural",
    "es": "es-ES-AlvaroNeural",
    "fr": "fr-FR-RemyNeural",
    "it": "it-IT-DiegoNeural",
    "de": "de-DE-ConradNeural",
    "ca": "ca-ES-EnricNeural",
    "nl": "nl-NL-MaartenNeural",
    "pl": "pl-PL-MarekNeural",
    "ru": "ru-RU-DmitryNeural",
    "sv": "sv-SE-MattiasNeural",
    "da": "da-DK-JeppeNeural",
    "fi": "fi-FI-HarriNeural",
    "no": "nb-NO-FinnNeural",
    "nb": "nb-NO-FinnNeural",
    "ro": "ro-RO-EmilNeural",
}


IDIOMAS_OFICIAIS = [
    ("Português", "", "pt", "poly_pt.txt"),
    ("Espanhol", "", "es", "poly_es.txt"),
    ("Italiano", "", "it", "poly_it.txt"),
    ("Francês", "", "fr", "poly_fr.txt"),
    ("Inglês", "", "en", "poly_en.txt"),
    ("Esperanto", "", "eo", "poly_eo.txt"),
    ("Latin", "", "la", "poly_la.txt"),
    ("Basco", "", "eu", "poly_eu.txt"),
    ("Catalão", "", "ca", "poly_ca.txt"),
    ("Córsico", "", "co", "poly_co.txt"),
    ("Galego", "", "gl", "poly_gl.txt"),
    ("Galês", "", "cy", "poly_cy.txt"),
    ("Polonês", "", "pl", "poly_pl.txt"),
    ("Holandês", "", "nl", "poly_nl.txt"),
    ("Irlandês", "", "ga", "poly_ga.txt"),
    ("Norueguês", "", "no", "poly_no.txt"),
    ("Finlandês", "", "fi", "poly_fi.txt"),
    ("Dinamarquês", "", "da", "poly_da.txt"),
    ("Romeno", "", "ro", "poly_ro.txt"),
    ("Russo", "", "ru", "poly_ru.txt"),
    ("Sueco", "", "sv", "poly_sv.txt"),
]


FONTES_MACHINA = [
    ("IBM Plex Sans", "'IBM Plex Sans', Arial, sans-serif"),
    ("Georgia", "Georgia, 'Times New Roman', serif"),
    ("Palatino", "'Palatino Linotype', Palatino, serif"),
    ("Trebuchet", "'Trebuchet MS', Arial, sans-serif"),
    ("Courier", "'Courier New', Courier, monospace"),
]


# -----------------------------------------------------------------------------
# Configuração inicial da página Streamlit.
# Deve permanecer antes de qualquer saída visual do Streamlit.
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="yPoemas @ a Machina de fazer Poesia",
    page_icon=":star:",
    layout="wide",
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
    """Aplica a identidade visual estável: Centro de Controle + gramado + Palco."""
    st.markdown(
        """
        <style>
        footer {visibility: hidden;}

        :root {
            --machina-gramado: #eef7e8;
            --machina-sidebar: #eef6fb;
        }

        div[data-testid="stAppViewContainer"],
        div[data-testid="stAppViewContainer"] main {
            background: var(--machina-gramado) !important;
            overflow-x: hidden !important;
        }

        div[data-testid="stAppViewContainer"] main .block-container {
            background: var(--machina-gramado) !important;
            padding-top: 0rem !important;
            padding-left: 0.65rem !important;
            padding-right: 0.65rem !important;
            padding-bottom: 0rem !important;
            max-width: none !important;
            width: 100% !important;
            min-height: calc(100vh - 140px) !important;
            max-height: none !important;
            overflow-x: hidden !important;
            overflow-y: visible !important;
        }


        /* Machina :: sidebar topo compacto para alinhar idiomas com páginas */
        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
            padding-top: 0rem !important;
            margin-top: -1.10rem !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
            gap: 0.18rem !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stElementContainer"] {
            margin-top: 0.02rem !important;
            margin-bottom: 0.02rem !important;
        }

        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] > div,
        [data-testid="stSidebarUserContent"],
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            background: var(--machina-sidebar) !important;
        }

        [data-testid="stSidebarResizer"],
        [data-testid="stSidebar"] [role="separator"] {
            display: none !important;
            pointer-events: none !important;
            width: 0 !important;
        }



        /* Machina :: largura canônica da sidebar */
        [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
            width: 400px;
            min-width: 400px;
            max-width: 400px;
        }


        /* Sidebar :: topo sem faixa excedente e sem mexer na largura */
        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
            padding-top: 0rem !important;
            margin-top: -1.10rem !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
            gap: 0.28rem !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stElementContainer"] {
            margin-top: 0rem !important;
            margin-bottom: 0.04rem !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stSelectbox"] {
            margin-top: 0rem !important;
            margin-bottom: 0.15rem !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stSelectbox"] label {
            margin-bottom: 0rem !important;
            padding-bottom: 0rem !important;
            line-height: 1.05 !important;
        }

        section[data-testid="stSidebar"] .stButton button {
            white-space: nowrap !important;
            word-break: keep-all !important;
            padding-left: 0.25rem !important;
            padding-right: 0.25rem !important;
        }

        mark {
            background-color: powderblue;
            color: black;
        }

        .container {
            display: flex;
            width: 100%;
            gap: 0px;
        }

        .header {
            text-align:center;
        }

        .logo-text {
            font-weight: 500;
            font-size: 21px;
            line-height: 1.35;
            font-family: 'IBM Plex Sans';
            color: #000000;
            padding-top: 0px;
            padding-left: 15px;
            margin-left: 0px;
        }

        .logo-img {
            float: right;
            margin-right: 0px;
            padding-right: 0px;
        }

        .ypo-title {
            display: block;
            width: 100%;
            text-align: center !important;
            font-weight: 700;
            margin: 0rem 0rem 1.35rem 0rem;
            padding: 0rem;
            letter-spacing: 0.015em;
        }

        hr {
            margin-left: 0rem !important;
            margin-right: 0rem !important;
        }

        /* machina-tabbar-tuning */
        div[data-testid="stAppViewContainer"] iframe[title="extra_streamlit_components.TabBar.tab_bar"] {
            margin-top: -32px !important;
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
        "stage_font": "IBM Plex Sans",
        "stage_size": 21,
        "book_changed": False,
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

def pick_lang():  # define idioma pela lista oficial
    options = []
    lookup = {}

    for nome, pais, code, poly_file in IDIOMAS_OFICIAIS:
        label = f"{nome} — {pais}" if pais else nome
        options.append(label)
        lookup[label] = {
            "lang": code,
            "poly_file": poly_file,
        }

    # Pré-sincroniza o idioma antes de desenhar o selectbox.
    # Assim o label "idiomas disponíveis..." já aparece no idioma escolhido.
    previous_choice = st.session_state.get("idioma_machina_oficial")
    if previous_choice in lookup:
        selected_previous = lookup[previous_choice]
        if st.session_state.lang != selected_previous["lang"]:
            st.session_state.last_lang = st.session_state.lang
            st.session_state.lang = selected_previous["lang"]
            st.session_state.poly_file = selected_previous["poly_file"]

    current = next(
        (
            label
            for label, data in lookup.items()
            if data["lang"] == st.session_state.lang
        ),
        options[0],
    )

    choice = st.sidebar.selectbox(
        translate("idiomas disponíveis..."),
        options,
        index=options.index(current),
        key="idioma_machina_oficial",
    )

    selected = lookup[choice]

    if st.session_state.lang != selected["lang"]:
        st.session_state.last_lang = st.session_state.lang
        st.session_state.lang = selected["lang"]
        st.session_state.poly_file = selected["poly_file"]


def show_icons():  # https://api.whatsapp.com/
    with st.sidebar:
        st.sidebar.markdown(
            f"""
            <nav>
            <a href='https://www.facebook.com/nandoulopes' target='_blank'>• facebook</a> |
            <a href='mailto:lopes.fernando@hotmail.com' target='_blank'>e-mail</a> |
            <a href='https://www.instagram.com/fernando.lopes.942/' target='_blank'>instagram</a> |
            <a href='https://web.whatsapp.com/send?phone=+5512991368181' target='_blank'>whatsapp</a>
            </nav>
            """,
            unsafe_allow_html=True,
        )


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
    returns.append(translate("anterior"))
    returns.append(translate("ao acaso"))
    returns.append(translate("próximo"))
    returns.append(translate("mais lidos"))
    returns.append(translate("novo"))
    returns.append(translate("arte"))
    returns.append(translate("voz"))
    return returns



def pick_book():
    """Escolhe o livro ativo sem abrir página redundante."""
    books_list = BOOKS_LIST
    current = st.session_state.get("book", "livro vivo")
    if current not in books_list:
        current = "livro vivo" if "livro vivo" in books_list else books_list[0]

    choice = st.sidebar.selectbox(
        translate("livros disponíveis..."),
        books_list,
        index=books_list.index(current),
        key="sidebar_book_select",
    )

    if choice != st.session_state.book:
        st.session_state.book = choice
        st.session_state.take = 0
        st.session_state.book_changed = True


def pick_stage_font():
    """Escolhe fonte e corpo de leitura do Palco."""
    labels = [label for label, fonte in FONTES_MACHINA]
    lookup = {label: fonte for label, fonte in FONTES_MACHINA}

    current_font = st.session_state.get("stage_font", "'IBM Plex Sans', Arial, sans-serif")
    current_label = next(
        (label for label, fonte in FONTES_MACHINA if fonte == current_font),
        labels[0],
    )

    corpos = list(range(15, 26))
    current_size = st.session_state.get("stage_size", 21)
    if current_size not in corpos:
        current_size = 21

    # Fonte ainda maior que corpo, mas corpo comporta 2 dígitos.
    col_font, col_corpo = st.sidebar.columns([2.10, 0.90])

    with col_font:
        choice = st.selectbox(
            translate("fontes"),
            labels,
            index=labels.index(current_label),
            key="sidebar_font_select",
        )

    with col_corpo:
        size = st.selectbox(
            translate("corpo"),
            corpos,
            index=corpos.index(current_size),
            key="sidebar_size_select",
        )

    st.session_state.stage_font = lookup[choice]
    st.session_state.stage_size = size


def draw_check_buttons():
    help_tips = load_help(st.session_state.lang)
    help_draw = help_tips[5]
    help_talk = help_tips[6]

    col_arte, col_voz = st.sidebar.columns([1, 1])

    with col_arte:
        if col_arte.button(translate("arte"), key="ctrl_arte", help=help_draw, use_container_width=True):
            st.session_state.draw = not st.session_state.draw

    with col_voz:
        if col_voz.button(translate("voz"), key="ctrl_voz", help=help_talk, use_container_width=True):
            st.session_state.talk = not st.session_state.talk


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


@st.cache_data
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


def normalize_about_key(value):
    value = str(value).strip().lower()
    value = value.replace("about_", "")
    value = value.replace(".md", "")
    value = value.replace("-", "_")
    value = value.replace(" ", "_")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return value


ABOUT_ALIASES = {
    "comments": ["comments", "comentarios", "comentários"],
    "prefácil": ["prefacil", "prefácil", "prefacio", "prefácio"],
    "machina": ["machina", "machina_a", "machina_d"],
    "off-machina": ["off_machina", "off-machina", "offmachina"],
    "MACHINA-IA": ["machina_ia", "machina-ia", "ia"],
    "livros": ["livros", "books"],
    "outros autores": ["outros_autores", "outros", "autores"],
    "imagens": ["imagens", "images"],
    "traduttore": ["traduttore", "traducoes", "traduções", "tradutor"],
    "bibliografia": ["bibliografia"],
    "samizdát": ["samizdat", "samizdát"],
    "notes": ["notes", "notas"],
    "license": ["license", "licenca", "licença"],
    "index": ["index", "indice", "índice"],
}


def about_title_from_file(file_name):
    stem = os.path.splitext(os.path.basename(file_name))[0]
    if stem.upper().startswith("ABOUT_"):
        stem = stem[6:]
    key = normalize_about_key(stem)
    if key in ("machina_a", "machina_d"):
        return "machina"
    return key


def discover_about_files():
    found_by_key = {}

    try:
        md_names = os.listdir("./md_files")
    except Exception:
        return {}

    for file_name in md_names:
        if file_name.upper().startswith("ABOUT_") and file_name.lower().endswith(".md"):
            key = about_title_from_file(file_name)
            found_by_key.setdefault(key, []).append(file_name)

    abouts = {}
    for title in ABOUTS_LIST:
        candidates = [normalize_about_key(title)]
        candidates += [normalize_about_key(alias) for alias in ABOUT_ALIASES.get(title, [])]

        files = []
        for key in candidates:
            files.extend(found_by_key.get(key, []))

        if normalize_about_key(title) == "machina":
            files = []
            for key in ("machina", "machina_a", "machina_d"):
                files.extend(found_by_key.get(key, []))

        unique_files = []
        seen = set()
        for file_name in files:
            if file_name not in seen:
                unique_files.append(file_name)
                seen.add(file_name)

        if normalize_about_key(title) == "machina":
            def machina_part_order(name):
                low = name.lower()
                if "_a.md" in low:
                    return 0
                if "_d.md" in low:
                    return 2
                return 1
            unique_files = sorted(unique_files, key=machina_part_order)

        if unique_files:
            abouts[title] = unique_files

    return abouts


def about_markdown_css():
    font = st.session_state.get("stage_font", "'IBM Plex Sans', Arial, sans-serif")
    size = st.session_state.get("stage_size", 21)

    st.markdown(
        f"""
        <style>
        .about-reader,
        .about-reader p,
        .about-reader li,
        .about-reader blockquote {{
            font-family: {font} !important;
            font-size: {size}px !important;
            line-height: 1.68 !important;
        }}

        .about-reader {{
            max-width: 920px;
            margin: 0 auto;
            padding: 0.25rem 0.35rem 2.5rem 0.35rem;
        }}

        .about-reader h1,
        .about-reader h2,
        .about-reader h3,
        .about-reader h4 {{
            font-family: {font} !important;
            line-height: 1.24 !important;
        }}

        .about-reader blockquote {{
            border-left: 3px solid rgba(128, 128, 128, 0.32);
            padding-left: 1rem;
            margin-left: 0.20rem;
            opacity: 0.96;
        }}

        .about-reader hr {{
            margin: 1.65rem 0 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )



@st.cache_data
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


@st.cache_data
def load_temas(book):  # List of themes inside a Book
    book_list = []
    with open(
        os.path.join("./base/rol_" + book + ".txt"), "r", encoding="utf-8"
    ) as file:
        for line in file:
            line = line.replace(" ", "")
            book_list.append(line.strip("\n"))

    return book_list


@st.cache_data
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

@st.cache_data
def load_index():  # Load indexes numbers for all themes
    index_list = []
    index_file = os.path.join("./md_files/ABOUT_index.md")

    # fallback apenas para instalações antigas ainda não padronizadas
    if not os.path.exists(index_file):
        index_file = os.path.join("./md_files/ABOUT_INDEX.md")

    with open(index_file, encoding="utf-8") as lista:
        for line in lista:
            index_list.append(line)

    return index_list


def load_lypo():  # Load last yPoema & replace '\n' with '<br>' for translator returned text
    lypo_text = ""
    lypo_user = "LYPO_" + IPAddres
    with open(
        os.path.join("./temp/" + lypo_user),
        encoding="utf-8",
        errors="replace",
    ) as script:
        for line in script:
            line = line.strip()
            lypo_text += line + "<br>"

    return lypo_text


def load_typo():  # Load translated yPoema & clean translator returned bugs in text
    typo_text = ""
    typo_user = "TYPO_" + IPAddres
    with open(
        os.path.join("./temp/" + typo_user),
        encoding="utf-8",
        errors="replace",
    ) as script:
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
    """Retorna a lista oficial de livros do modo off-machina."""
    return OFF_BOOKS_LIST


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


def load_poema(nome_tema, seed_eureka):  # generate new yPoema
    script = gera_poema(nome_tema, seed_eureka)
    novo_ypoema = ""
    lypo_user = "LYPO_" + IPAddres

    with open(os.path.join("./temp/" + lypo_user), "w", encoding="utf-8") as save_lypo:
        save_lypo.write(
            nome_tema
        )  # include title of yPoema in first line for translations
        save_lypo.write("\n")

        for line in script:
            if line == "\n":
                save_lypo.write("\n")
                novo_ypoema += "<br>"
            else:
                save_lypo.write(line + "\n")
                novo_ypoema += line + "<br>"

    save_lypo.close()  # save last generated in LYPO

    return novo_ypoema


def load_images():
    images_list = []
    with open(os.path.join("./base/images.txt"), encoding="utf-8") as lista:
        for line in lista:
            images_list.append(line)

    return images_list


def load_arts(nome_tema):  # Select image for arts
    path = "./images/machina/"
    path_list = load_images()
    for line in path_list:
        if line.startswith(nome_tema):
            this_line = line.strip("\n")
            part_line = this_line.partition(" : ")
            if nome_tema == part_line[0]:
                path = "./images/" + part_line[2] + "/"
                break

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

        

def split_ypo_title(logo_text):
    """
    Separa a primeira linha do yPoema para tratá-la como título.
    LYPO costuma trazer o título na primeira linha.
    """
    if not logo_text:
        return "", ""

    parts = logo_text.split("<br>", 1)
    title = parts[0].strip()
    body = parts[1].strip() if len(parts) > 1 else ""

    return title, body



def copy_to_clipboard_button(texto):
    import html
    import json

    # clipboard deve receber texto limpo, não HTML.
    texto_limpo = html.unescape(texto)

    texto_limpo = (
        texto_limpo
        .replace("<br><br>", "\n\n")
        .replace("<br>", "\n")
        .replace("<br/>", "\n")
        .replace("<br />", "\n")
    )

    safe_json = json.dumps(texto_limpo)

    html_code = f"""
    <div style="width:100%; text-align:right; margin-bottom:-8px;">
        <button
            id="copy_btn"
            title="copiar yPoema"
            style="
                border:none;
                background:rgba(255,255,255,0.06);
                border-radius:6px;
                padding:2px 6px;
                cursor:pointer;
                font-size:18px;
                opacity:0.78;
                transition:0.2s;
            "
            onmouseover="this.style.opacity='1.0'"
            onmouseout="this.style.opacity='0.78'"
        >📋</button>

        <span
            id="copy_msg"
            style="
                margin-left:8px;
                font-size:11px;
                opacity:0;
                transition:0.25s;
            "
        >✓ yPoema copiado</span>
    </div>

    <script>
    const copyBtn = document.getElementById("copy_btn");
    const copyMsg = document.getElementById("copy_msg");

    copyBtn.addEventListener("click", async () => {{
        await navigator.clipboard.writeText({safe_json});
        copyMsg.style.opacity = "1";
        setTimeout(() => {{
            copyMsg.style.opacity = "0";
        }}, 1200);
    }});
    </script>
    """

    st.components.v1.html(html_code, height=32)


def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):  # ver save_img.py
    title, body = split_ypo_title(LOGO_TEXTO)

    fonte_palco = st.session_state.get("stage_font", "'IBM Plex Sans', Arial, sans-serif")
    corpo_palco = st.session_state.get("stage_size", 21)

    titulo_html = ""
    if title:
        titulo_html = (
            f"<div class='ypo-title' "
            f"style=\"font-family:{fonte_palco}; font-size:{corpo_palco}px;\">"
            f"{title}</div><br>"
        )

    texto_html = body if body else ""

    if LOGO_IMAGE == None:
        st.markdown(
            f"""
            <div class='container'>
                <div class='logo-text' style="font-family:{fonte_palco}; font-size:{corpo_palco}px; line-height:1.35;">{titulo_html}{texto_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class='container'>
                <img class='logo-img' src='data:image/jpg;base64,{base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()}'>
                <div class='logo-text' style="font-family:{fonte_palco}; font-size:{corpo_palco}px; line-height:1.35;">{titulo_html}{texto_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def talk(text):
    """Lê o yPoema no idioma atual usando edge-tts, quando disponível."""
    if edge_tts is None:
        st.warning("Motor de voz neural indisponível.")
        return

    # Limpeza para a voz não ler tags
    text_clean = text.replace("<br>", " ").replace("< br>", "").replace("<br >", "").replace("<br/>", " ")
    
    # Mapeamento de vozes neurais de alta qualidade
    selected_voice = VOICES_EDGE_TTS.get(st.session_state.lang, "pt-BR-AntonioNeural")

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

    if auto.button("auto", key="mini_auto_button", help=translate("modo auto")):
        st.session_state.auto = not st.session_state.auto

    if st.session_state.auto:
        st.session_state.talk = False
        with st.sidebar:
            wait_time = st.slider(translate("tempo de exibição (em segundos): "), 5, 60)

    if rand:
        st.session_state.rand = True
        st.session_state.mini = random.randrange(0, maxy_mini)
    else:
        st.session_state.rand = False

    st.session_state.tema = temas_list[st.session_state.mini]
    analise = say_number(st.session_state.tema)
    more = more.button("✚", help=help_more)

    if more:
        st.session_state.rand = False

    lnew = True
    if lnew or st.session_state.auto:
        if st.session_state.rand:
            st.session_state.mini = random.randrange(0, maxy_mini)
            st.session_state.tema = temas_list[st.session_state.mini]

        if st.session_state.lang != st.session_state.last_lang:
            curr_ypoema = load_lypo()  # changes in lang, keep LYPO
        elif more or rand or st.session_state.rand:
            curr_ypoema = load_poema(st.session_state.tema, "")
            curr_ypoema = load_lypo()
        else:
            try:
                curr_ypoema = load_lypo()
            except Exception:
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
    temas_list = load_temas(st.session_state.book)
    maxy_ypoemas = len(temas_list) - 1

    if "take_widget_nonce" not in st.session_state:
        st.session_state.take_widget_nonce = 0

    if st.session_state.take > maxy_ypoemas or st.session_state.take < 0:
        st.session_state.take = 0
        st.session_state.take_widget_nonce += 1

    # Palco: listas laterais + cluster centralizado de navegação.
    # Livros/temas +20% para evitar corte visual.
    book_col, spacer_l, more, last, rand, nest, manu, spacer_r, tema_col = st.columns(
        [2.70, 0.45, 0.72, 0.72, 0.72, 0.72, 0.72, 0.45, 2.70]
    )

    nav_changed = bool(st.session_state.get("book_changed", False))
    st.session_state.book_changed = False

    with book_col:
        books_list = BOOKS_LIST
        current_book = st.session_state.get("book", "livro vivo")
        if current_book not in books_list:
            current_book = "livro vivo" if "livro vivo" in books_list else books_list[0]

        new_book = st.selectbox(
            "livros",
            books_list,
            index=books_list.index(current_book),
            key="palco_book_select",
            label_visibility="collapsed",
        )

        if new_book != st.session_state.book:
            st.session_state.book = new_book
            st.session_state.take = 0
            st.session_state.book_changed = True
            nav_changed = True
            st.session_state.take_widget_nonce += 1
            temas_list = load_temas(st.session_state.book)
            maxy_ypoemas = len(temas_list) - 1

    help_tips = load_help(st.session_state.lang)
    help_last = help_tips[0]
    help_rand = help_tips[1]
    help_nest = help_tips[2]
    help_more = help_tips[4]

    more_clicked = more.button("✚", key="ypo_more", help=help_more, use_container_width=True)
    last_clicked = last.button("◀", key="ypo_last", help=help_last, use_container_width=True)
    rand_clicked = rand.button("✻", key="ypo_rand", help=help_rand, use_container_width=True)
    nest_clicked = nest.button("▶", key="ypo_next", help=help_nest, use_container_width=True)
    manu_clicked = manu.button("?", key="ypo_help", help=translate("ajuda"), use_container_width=True)

    if last_clicked:
        nav_changed = True
        st.session_state.take -= 1
        if st.session_state.take < 0:
            st.session_state.take = maxy_ypoemas
        st.session_state.take_widget_nonce += 1

    if rand_clicked:
        nav_changed = True
        old_take = st.session_state.take
        if len(temas_list) > 1:
            new_take = random.randrange(0, len(temas_list))
            while new_take == old_take:
                new_take = random.randrange(0, len(temas_list))
            st.session_state.take = new_take
        else:
            st.session_state.take = 0
        st.session_state.take_widget_nonce += 1

    if nest_clicked:
        nav_changed = True
        st.session_state.take += 1
        if st.session_state.take > maxy_ypoemas:
            st.session_state.take = 0
        st.session_state.take_widget_nonce += 1

    with tema_col:
        options = list(range(len(temas_list)))
        selected_take = st.selectbox(
            "temas",
            options,
            index=st.session_state.take,
            format_func=lambda z: temas_list[z],
            key="take_select_" + str(st.session_state.take_widget_nonce),
            label_visibility="collapsed",
        )

    if selected_take != st.session_state.take:
        st.session_state.take = selected_take
        nav_changed = True

    st.session_state.tema = temas_list[st.session_state.take]

    if manu_clicked:
        st.subheader(load_md_file("MANUAL_YPOEMAS.md"))

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
        if st.session_state.lang != st.session_state.last_lang:
            curr_ypoema = load_lypo()
        elif more_clicked or nav_changed:
            curr_ypoema = load_poema(st.session_state.tema, "")
            curr_ypoema = load_lypo()
        else:
            try:
                curr_ypoema = load_lypo()
            except Exception:
                curr_ypoema = load_poema(st.session_state.tema, "")
                curr_ypoema = load_lypo()

        if st.session_state.lang != "pt":
            curr_ypoema = translate(curr_ypoema)
            typo_user = "TYPO_" + IPAddres
            with open(os.path.join("./temp/" + typo_user), "w", encoding="utf-8") as save_typo:
                save_typo.write(curr_ypoema)
            curr_ypoema = load_typo()

        update_readings(st.session_state.tema)

        LOGO_TEXTO = curr_ypoema
        LOGO_IMAGE = None
        if st.session_state.draw:
            LOGO_IMAGE = load_arts(st.session_state.tema)

        copy_to_clipboard_button(curr_ypoema)
        write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

        if manu_clicked:
            LOGO_TEXTO = load_info(st.session_state.tema)
            if st.session_state.lang != "pt":
                LOGO_TEXTO = translate(LOGO_TEXTO)

            LOGO_IMAGE = "./images/matrix/" + st.session_state.tema.capitalize() + ".jpg"
            write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

    if st.session_state.talk:
        talk(curr_ypoema)


def page_eureka():
    seed, more, rand, manu, occurrences = st.columns([2.5, 1.5, 1.5, 0.7, 4])

    with seed:
        find_what = st.text_input(
            label=translate("digite algo para buscar..."),
        )

    help_tips = load_help(st.session_state.lang)
    help_rand = help_tips[1]
    help_more = help_tips[4]

    with more:
        more = more.button("✚", help=help_more)

    with rand:
        rand = rand.button("✻", help=help_rand)

    with manu:
        manu = manu.button("?", help=translate("ajuda"))

    if manu:
        st.subheader(load_md_file("MANUAL_EUREKA.md"))

    if len(find_what) < 3:
        st.warning(translate("digite pelo menos 3 letras..."))
        return

    seed_list = []
    soma_tema = []

    eureka_list = load_eureka(find_what)
    for line in eureka_list:
        this_line = line.strip("\n")
        part_line = this_line.partition(" : ")
        palas = part_line[0]
        fonte = part_line[2]
        seed_tema = fonte[0:-5]

        if (palas is None) or (fonte is None):
            continue

        seed_list.append(palas + " ➪ " + fonte)
        if seed_tema not in soma_tema:
            soma_tema.append(seed_tema)

    if len(seed_list) == 0:
        st.warning(
            translate(
                'nenhuma ocorrência das letras " '
                + find_what
                + ' " foi encontrada...'
            )
        )
        return

    seed_list.sort()

    if len(seed_list) == 1:
        info_find = translate('ocorrência de "')
    else:
        info_find = translate('ocorrências de "')

    info_find += find_what
    if len(soma_tema) > 1:
        info_find += translate('" em ' + str(len(soma_tema)) + " temas")

    # st.session_state.eureka é o índice canônico.
    # ✻ varre a lista de ocorrências; ✚ gera nova versão da ocorrência atual.
    if "eureka_widget_nonce" not in st.session_state:
        st.session_state.eureka_widget_nonce = 0

    if rand:
        old_eureka = st.session_state.get("eureka", 0)

        if len(seed_list) > 1:
            new_eureka = random.randrange(0, len(seed_list))
            while new_eureka == old_eureka:
                new_eureka = random.randrange(0, len(seed_list))
            st.session_state.eureka = new_eureka
        else:
            st.session_state.eureka = 0

        # força o selectbox a reconstruir com o novo index
        st.session_state.eureka_widget_nonce += 1

    if st.session_state.eureka >= len(seed_list) or st.session_state.eureka < 0:
        st.session_state.eureka = 0
        st.session_state.eureka_widget_nonce += 1

    with occurrences:
        options = list(range(len(seed_list)))
        selected_eureka = st.selectbox(
            "↓  " + str(len(seed_list)) + " " + info_find,
            options,
            index=st.session_state.eureka,
            format_func=lambda y: seed_list[y],
            key="eureka_select_" + str(st.session_state.eureka_widget_nonce),
        )

    if selected_eureka != st.session_state.eureka:
        st.session_state.eureka = selected_eureka

    this_seed = seed_list[st.session_state.eureka]
    part_line = this_seed.partition(" ➪ ")
    nome_tema = part_line[2]
    seed_tema = nome_tema[0:-5]

    st.session_state.tema = seed_tema

    if st.session_state.lang != st.session_state.last_lang:
        curr_ypoema = load_lypo()
    else:
        curr_ypoema = load_poema(seed_tema, this_seed)
        curr_ypoema = load_lypo()

    if st.session_state.lang != "pt":
        curr_ypoema = translate(curr_ypoema)
        typo_user = "TYPO_" + IPAddres
        with open(
            os.path.join("./temp/" + typo_user), "w", encoding="utf-8"
        ) as save_typo:
            save_typo.write(curr_ypoema)
        curr_ypoema = load_typo()

    eureka_expander = st.expander("", expanded=True)
    with eureka_expander:
        LOGO_TEXTO = curr_ypoema
        LOGO_IMAGE = None
        if st.session_state.draw:
            LOGO_IMAGE = load_arts(seed_tema)

        copy_to_clipboard_button(curr_ypoema)
        write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
        update_readings(seed_tema)

    if st.session_state.talk:
        talk(curr_ypoema)

    if manu:
        LOGO_TEXTO = load_info(seed_tema)
        if st.session_state.lang != "pt":
            LOGO_TEXTO = translate(LOGO_TEXTO)

        LOGO_IMAGE = "./images/matrix/" + seed_tema.capitalize() + ".jpg"
        write_ypoema(LOGO_TEXTO, LOGO_IMAGE)


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
    manu = manu.button("?", help=translate("ajuda"))

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
                        st.image(LOGO_CAPA, width="stretch")
                    else:
                        st.image(
                            "./off_machina/capa_" + off_book_name + ".jpg",
                            width="stretch",
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
        books_list = BOOKS_LIST

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
            doit = st.button("✔")

        lnew = True
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
        doit = st.button("✔")

    if doit:
        poly_pais = poly_pais[opt_poly]
        poly_ling = poly_ling[opt_poly]
        st.session_state.poly_name = translate(poly_pais)
        st.session_state.poly_lang = poly_ling
        st.session_state.poly_take = opt_poly

        st.session_state.last_lang = st.session_state.lang
        st.session_state.lang = st.session_state.poly_lang

    lnew = True
    if lnew:
        poly_expander = st.expander("", True)
        with poly_expander:
            st.subheader(load_md_file("MANUAL_POLY.md"))


def page_abouts():
    abouts_map = discover_about_files()

    if not abouts_map:
        st.warning(translate("nenhum arquivo ABOUT_*.md encontrado em ./md_files"))
        return

    # Ordem autoral. Nunca usar sorted() aqui.
    abouts_list = [title for title in ABOUTS_LIST if title in abouts_map]

    options = list(range(len(abouts_list)))
    opt_abouts = st.selectbox(
        "sobre",
        options,
        format_func=lambda x: abouts_list[x],
        key="opt_abouts",
        label_visibility="collapsed",
    )

    choice = abouts_list[opt_abouts]

    about_expander = st.expander("", True)
    with about_expander:
        about_markdown_css()

        if normalize_about_key(choice) == "machina":
            st.markdown("<div class='about-reader'>", unsafe_allow_html=True)

            for file_name in abouts_map[choice]:
                if file_name.lower().endswith("_a.md"):
                    st.subheader(load_md_file(file_name))

                    LOGO_TEXTO = load_info(st.session_state.tema)
                    LOGO_IMAGE = "./images/matrix/" + st.session_state.tema + ".jpg"
                    write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

                elif file_name.lower().endswith("_d.md"):
                    st.subheader(load_md_file(file_name))

                else:
                    st.subheader(load_md_file(file_name))

            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.markdown("<div class='about-reader'>", unsafe_allow_html=True)
            for file_name in abouts_map[choice]:
                st.subheader(load_md_file(file_name))
            st.markdown("</div>", unsafe_allow_html=True)


### eof: pages


def main():
    chosen_id = stx.tab_bar(
        data=[
            stx.TabBarItemData(id=1, title="mini", description=""),
            stx.TabBarItemData(id=2, title="yPoemas", description=""),
            stx.TabBarItemData(id=3, title="eureka", description=""),
            stx.TabBarItemData(id=4, title="off-mach", description=""),
            stx.TabBarItemData(id=6, title="poly", description=""),
            stx.TabBarItemData(id=7, title="about", description=""),
        ],
        default=2,
    )

    chosen_id = str(chosen_id)

    pick_lang()
    pick_book()
    pick_stage_font()
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
    elif chosen_id == "6":
        st.sidebar.info(load_md_file("INFO_POLY.md"))
        magy = "img_poly.jpg"
        page_polys()
    elif chosen_id == "7":
        st.sidebar.info(load_md_file("INFO_ABOUT.md"))
        magy = "img_about.jpg"
        page_abouts()

    with st.sidebar:
        st.image("./images/" + magy)

    #show_icons()
    ##$ st.sidebar.state = True


if __name__ == "__main__":
    main()
