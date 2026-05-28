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

ABOUTS_LIST = [
    "comentários", "prefácil", "machina", "off-machina", "machina-IA", "livros", "outros autores",
    "imagens", "poly", "pensares", "tradittore", "bibliografia", "pontuação", "samizdàt", "notes", "license", "index",
]

ABOUTS_FILES = {
    "comentários": ["ABOUT_comentários.md"],
    "prefácil": ["ABOUT_prefácil.md"],
    "machina": ["ABOUT_machina I.md", "ABOUT_machina II.md"],
    "off-machina": ["ABOUT_off-machina.md"],
    "machina-IA": ["ABOUT_machina-IA.md"],
    "livros": ["ABOUT_livros.md"],
    "outros autores": ["ABOUT_outros_autores.md", "ABOUT_outros autores.md"],
    "imagens": ["ABOUT_imagens.md"],
    "poly": ["ABOUT_poly.md"],
    "pensares": ["ABOUT_pensares.md"],
    "tradittore": ["ABOUT_tradittore.md"],
    "bibliografia": ["ABOUT_bibliografia.md"],
    "pontuação": ["ABOUT_pontuação.md"],
    "samizdàt": ["ABOUT_samizdàt.md"],
    "notes": ["ABOUT_notes.md"],
    "license": ["ABOUT_license.md"],
    "index": ["ABOUT_index.md", "ABOUT_INDEX.md"],
}

BOOKS_LIST = [
    "todos os temas", "livro vivo", "poemas", "jocosos", "ensaios", "variações", 
    "metalinguagem", "sociais", "outros autores", "signos_fem", "signos_mas",
    "todos os signos",
]

OFF_BOOKS_LIST = [
    "a_torre_de_papel", "quase_que_eu_Poesia", "faz_de_conto", "um_romance",
    "linguafiada", "livro_vivo", "desvoto", "ensaios", "urbano", "essencial", "secreto",
]

PAGE_IMAGES = {
    "1": "img_mini.jpg", "2": "img_ypoemas.jpg", "3": "img_eureka.jpg",
    "4": "img_off-machina.jpg", "5": "img_about.jpg",
}

VOICES_EDGE_TTS = {
    "pt": "pt-BR-FranciscaNeural",
    "es": "es-ES-AlvaroNeural",
    "fr": "fr-FR-HenriNeural",
    "it": "it-IT-DiegoNeural",
    "en": "en-GB-RyanNeural",
    "en": "en-US-GuyNeural",
    "gl": "gl-ES-RoiNeural",
    "eu": "eu-ES-AnderNeural",
    "de": "de-DE-ConradNeural",
    "da": "da-DK-JeppeNeural",
    "nl": "nl-NL-MaartenNeural",
    "pl": "pl-PL-MarekNeural",
    "ro": "ro-RO-EmilNeural",
    "nb": "nb-NO-FinnNeural",
    "fi": "fi-FI-SelmaNeural",
    "is": "is-IS-GunnarNeural",
    "hu": "hu-HU-TamasNeural",
    "sv": "sv-SE-MattiasNeural",
    "ca": "ca-ES-EnricNeural",
    "ru": "ru-RU-DmitryNeural",
}

IDIOMAS_OFICIAIS = [
    ("Português", "Brasil", "pt", "poly_pt.txt"),
    ("Español", "Espanha", "es", "poly_es.txt"),
    ("Italiano", "Itália", "it", "poly_it.txt"),
    ("Français", "França", "fr", "poly_fr.txt"),
    ("Latin", "Latim", "la", "poly_la.txt"),
    ("Esperanto", "Esperanto", "eo", "poly_eo.txt"),    
    ("English", "Inglaterra", "en", "poly_en.txt"),
    ("Deutsch", "Alemanha", "de", "poly_de.txt"),
    ("Català", "Catalunha", "ca", "poly_ca.txt"),
    ("Euskara", "Basco", "eu", "poly_eu.txt"),
    ("Galego", "Galícia", "gl", "poly_gl.txt"),
    ("Nederlands", "Países Baixos", "nl", "poly_nl.txt"),
    ("Polski", "Polônia", "pl", "poly_pl.txt"),
    ("Română", "Romênia", "ro", "poly_ro.txt"),
    ("Русский", "Rússia", "ru", "poly_ru.txt"),
    ("Svenska", "Suécia", "sv", "poly_sv.txt"),
    ("Norsk", "Noruega", "no", "poly_no.txt"),
    ("Dansk", "Dinamarca", "da", "poly_da.txt"),
    ("Suomi", "Finlândia", "fi", "poly_fi.txt"),
    ("Íslenska", "Islândia", "is", "poly_is.txt"),
    ("Magyar", "Hungria", "hu", "poly_hu.txt"),
]


# -----------------------------------------------------------------------------
# Configuração inicial da página Streamlit.
# Deve permanecer antes de qualquer saída visual do Streamlit.
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
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
    """Aplica os estilos básicos da Machina e preserva o Palco sem controles."""
    st.markdown(
        """
        <style>
        /*#MainMenu {visibility: hidden;}*/
        footer {visibility: hidden;}
        
        /* Machina :: botões sem quebra de linha */
        div[data-testid="stButton"] button,
        div[data-testid="stButton"] button p {
            white-space: nowrap !important;
            word-break: keep-all !important;
            overflow-wrap: normal !important;
        }
</style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""
    <style>
    .stButton > button {
        white-space: nowrap !important;
    }
    </style>
    """, unsafe_allow_html=True)


    st.markdown(
        """
        <style>
        .reportview-container .main .block-container{
            padding-top: 0rem;
            padding-right: 0.04rem;
            padding-left: 0.04rem;
            padding-bottom: 0rem;
            max-width: 100vw;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
            width: 25vw;
            min-width: 25vw;
            max-width: 25vw;
        }

        /* Sidebar :: calibragem temporária com dragster visível */
        [data-testid="stSidebarResizer"],
        [data-testid="stSidebar"] [role="separator"] {
            display: none !important;
            width: 0 !important;
            opacity: 0.45 !important;
        }
        mark {
            background-color: powderblue;
            color: black;
        }
        .container {
            display: flex;
            gap: 8px;
            width: 100%;
        }
        .header {
            text-align:center;
        }
        .logo-text {
            font-weight: 600;
            font-size: 21px;
            font-family: 'Trebuchet';
            color: #000000;
            padding-top: 0px;
            padding-left: 8px;
        }

        .logo-img {
            float:right;
            margin-right: 0px;
            padding-right: 0px;
        }


        /* Palco :: ajuste fino de área útil */
        div[data-testid="stVerticalBlock"] {
            gap: 0.18rem;
        }

        div[data-testid="stExpander"] {
            margin-top: 0rem;
        }

        div[data-testid="stExpander"] details {
            padding-top: 0rem;
        }

        div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
            margin-top: 0rem;
        }

        
        /* Sidebar :: Centro de Controle */
        [data-testid="stSidebar"] {
            background-color: #eef6fb !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            background-color: #eef6fb !important;
        }

        [data-testid="stSidebar"] .stButton button {
            white-space: nowrap !important;
            word-break: keep-all !important;
            padding-left: 0.25rem !important;
            padding-right: 0.25rem !important;
            min-width: 100% !important;
        }

        
        /* Sidebar :: respiro vertical entre controles */
        [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
            gap: 0.85rem !important;
        }

        [data-testid="stSidebar"] div[data-testid="stElementContainer"] {
            margin-bottom: 0.12rem !important;
        }

        
        /* Território sem dono :: lista de páginas no topo, sem linha fantasma */
        iframe[title="extra_streamlit_components.TabBar.tab_bar"] {
            display: block !important;
            width: 100% !important;
            max-width: 100% !important;
            margin: -0.62rem 0 0 0 !important;
            padding: 0 !important;
            border: 0 !important;
            outline: 0 !important;
            box-shadow: none !important;
            background: transparent !important;
        }

        div[data-testid="stElementContainer"]:has(iframe[title="extra_streamlit_components.TabBar.tab_bar"]) {
            width: 100% !important;
            max-width: 100% !important;
            display: block !important;
            margin-top: -0.62rem !important;
            margin-bottom: 0rem !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            border: 0 !important;
            outline: 0 !important;
            box-shadow: none !important;
            background: transparent !important;
        }

        /* Sintonia fina :: subir páginas */
        iframe[title="extra_streamlit_components.TabBar.tab_bar"] {
            margin-top: -0.62rem !important;
            margin-bottom: 0 !important;
        }

        div[data-testid="stElementContainer"] {
            margin-top: 0 !important;
        }

        /* Free Gramado :: liberar área útil real */
        section.main > div.block-container {
            max-width: 100vw !important;
            width: 100% !important;
            padding-left: 0.00rem !important;
            padding-right: 0.00rem !important;
        }

        
        /* Centralização óptica dos títulos markdown */
        div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3 {
            text-align: center !important;
        }

        /* Títulos dos yPoemas :: eixo emocional do palco */
        .machina-titulo-poema,
        .titulo-poema {
            text-align: center !important;
            font-size: 1.24rem !important;
            font-weight: 500 !important;
            letter-spacing: 0.03rem !important;
            margin-top: 0.10rem !important;
            margin-bottom: 0.30rem !important;
        }

/* Gramado :: território principal */
        .main .block-container {
            padding-top: 0.00rem !important;
            padding-left: 0.00rem !important;
            padding-right: 0.00rem !important;
            padding-bottom: 0.16rem !important;
            max-width: 100vw !important;
            width: 100% !important;
        }

        .machina-gramado {
            background: #eef8ee;
            border-radius: 18px;
            padding: 0.04rem 0.10rem 0.20rem 0.10rem;
            min-height: 78vh;
            overflow-x: hidden;
            overflow-y: auto;
        }

        /* Gramado real: primeiro container criado no main */
        div[data-testid="stAppViewContainer"] main
        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]:first-child,
        div[data-testid="stAppViewContainer"] main
        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"]:first-child {
            background: #eef8ee !important;
            border-radius: 18px !important;
            padding: 0.00rem 0.00rem 0.22rem 0.00rem !important;
        }


        /* Território sem dono :: expander/palco no mesmo eixo */
        div[data-testid="stExpander"] {
            width: 100% !important;
            max-width: 100% !important;
        }

        div[data-testid="stExpander"] details {
            width: 100% !important;
            max-width: 100% !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }

        div[data-testid="stExpander"] summary {
            padding-left: 0 !important;
            padding-right: 0 !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }

        div[data-testid="stExpander"] div[data-testid="stVerticalBlock"] {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }

        .machina-palco-central {
            background: rgba(255, 255, 255, 0.72);
            border-radius: 18px;
            padding: 0.08rem 0.00rem 0.16rem 0.00rem;
            min-height: 61vh;
            overflow-x: hidden;
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
        }

        .machina-moldura-lateral {
            min-height: 61vh;
        }

        .machina-rodape-palco {
            font-size: 0.82rem;
            opacity: 0.72;
            text-align: center;
            margin-top: 0.35rem;
            padding-bottom: 0.1rem;
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
        "book": "poemas",
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
        "stage_font": "Trebuchet",
        "stage_size": 21,
        "sidebar_panel": "Machina",
        "cia_name": "",
        "cia_mood": "Sintática",

        # chave de ouro
        "key_open": False,
        "key_poema_texto": "",
        "key_poema_tema": "",
        "key_analise": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


apply_styles()
init_session_state()


def open_gramado():
    """Cria um container real para o gramado.

    Importante:
    st.markdown("<div>") não envolve elementos Streamlit seguintes.
    O gramado precisa ser um container usado com `with gramado:`.
    """
    return st.container()


def open_palco():
    """Cria um container real para o palco."""
    return st.container()


def palco_status(book=None, pos=None, total=None):
    book = book or st.session_state.get("book", "")
    if pos is None or total is None:
        return f"🌿  {st.session_state.lang} ( {book} )"
    return f"🌿  {st.session_state.lang} ( {book} ) ( {pos} / {total} )"

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


def pick_lang():  # lista oficial de idiomas + P.O.L.Y.
    options = []
    lookup = {}

    for nome, pais, code, poly_file in IDIOMAS_OFICIAIS:
        label = f"{nome} — {pais}"
        options.append(label)
        lookup[label] = {
            "lang": code,
            "poly_file": poly_file,
        }

    # Antes de desenhar a lista, sincroniza o idioma com a seleção já feita.
    # Isso evita label traduzido no idioma anterior.
    previous_choice = st.session_state.get("idioma_oficial_select")
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
        key="idioma_oficial_select",
    )

    selected = lookup[choice]
    if st.session_state.lang != selected["lang"]:
        st.session_state.last_lang = st.session_state.lang
        st.session_state.lang = selected["lang"]
        st.session_state.poly_file = selected["poly_file"]


FONTES_MACHINA = [
    ("IBM Plex Sans", "IBM Plex Sans"),
    ("Inter", "Inter"),
    ("Spectral", "Spectral"),
    ("EB Garamond", "EB Garamond"),
    ("Libre Baskerville", "Libre Baskerville"),
    ("Cormorant Garamond", "Cormorant Garamond"),
    ("Palatino", "Palatino Linotype"),
    ("Georgia", "Georgia"),
    ("Trebuchet", "Trebuchet MS"),
    ("Atkinson Hyperlegible", "Atkinson Hyperlegible"),
    ("OpenDyslexic", "OpenDyslexic"),
    ("JetBrains Mono", "JetBrains Mono"),
    ("Courier", "Courier New"),
]

CIA_WORD_1 = ["Informação", "Invenção", "Imaginação", "Imagética", "Injeção"]
CIA_WORD_2 = ["Analítica", "Artificial", "Analógica", "Afetiva", "Adicional", "Ampliada", "Avançada", "Acadêmica"]
CIA_MOODS = [
    "Sintática",
    "Sintética",
    "Formal",
    "Resumida",
    "Rápida",
    "Completa",
]


def ensure_cia_name(force=False):
    """Gera um nome mutável para a CIA e o preserva durante a sessão."""
    if force or not st.session_state.get("cia_name"):
        st.session_state["cia_name"] = (
            "Centro de "
            + random.choice(CIA_WORD_1)
            + " "
            + random.choice(CIA_WORD_2)
        )


def render_cia_sidebar():
    """Centro de Controle da Chave, exclusivo de yPoemas."""
    ensure_cia_name()
    st.sidebar.markdown("### CIA")
    st.sidebar.caption(st.session_state.get("cia_name", "Centro de Informação Analítica"))
    st.sidebar.markdown("---")
    st.sidebar.markdown("**moods**")

    for mood in CIA_MOODS:
        if mood == st.session_state.get("cia_mood", CIA_MOODS[0]):
            st.sidebar.markdown(f"**• {mood}**")
        else:
            st.sidebar.markdown(f"• {mood}")

    st.sidebar.caption("CIA v0: 1 mood funcional, mapa visual completo.")


def draw_sidebar_panel_buttons(chosen_id):
    """Alterna entre Machina e CIA com botões horizontais, apenas em yPoemas."""
    if chosen_id != "2":
        st.session_state["sidebar_panel"] = "Machina"
        return

    col_mach, col_cia = st.sidebar.columns([1, 1])
    with col_mach:
        if st.button("Machina", key="sidebar_panel_machina", use_container_width=True):
            st.session_state["sidebar_panel"] = "Machina"
    with col_cia:
        if st.button("CIA", key="sidebar_panel_cia", use_container_width=True):
            st.session_state["sidebar_panel"] = "CIA"



def _coerce_take(value, temas_list):
    """Converte diferentes formas de seleção de tema para índice inteiro válido."""
    if not temas_list:
        return 0

    if isinstance(value, int):
        take = value
    elif isinstance(value, str):
        if value.isdigit():
            take = int(value)
        elif value in temas_list:
            take = temas_list.index(value)
        else:
            take = 0
    else:
        take = 0

    if take < 0 or take >= len(temas_list):
        take = 0
    return take


def _sync_book_theme_state():
    """Mantém o estado canônico (book/take/tema) consistente."""
    books_list = BOOKS_LIST
    current_book = st.session_state.get("book", books_list[0])
    if current_book not in books_list:
        current_book = books_list[0]
    st.session_state.book = current_book

    temas_list = load_temas(current_book)
    if not temas_list:
        st.session_state.take = 0
        st.session_state.tema = ""
        return

    take = _coerce_take(st.session_state.get("take", 0), temas_list)

    st.session_state.take = take
    st.session_state.tema = temas_list[take]


def _prepare_book_widget(key):
    """Faz o widget espelhar `book` sem tomar conta do estado."""
    current = st.session_state.book
    if key in st.session_state and st.session_state.get(key) != current:
        del st.session_state[key]


def _prepare_theme_widget():
    """Normaliza o widget de temas para espelhar o `take` sem impor valor indevido."""
    temas_list = load_temas(st.session_state.book)
    current = _coerce_take(st.session_state.get("take", 0), temas_list)
    raw_value = st.session_state.get("opt_take_palco", current)
    normalized = _coerce_take(raw_value, temas_list)
    if normalized != raw_value:
        st.session_state["opt_take_palco"] = normalized


def _on_sidebar_book_change():
    choice = st.session_state.get("sidebar_book_select", st.session_state.book)
    if choice != st.session_state.book:
        st.session_state.book = choice
        st.session_state.take = 0
    _sync_book_theme_state()


def _on_palco_book_change():
    choice = st.session_state.get("palco_book_select", st.session_state.book)
    if choice != st.session_state.book:
        st.session_state.book = choice
        st.session_state.take = 0
    _sync_book_theme_state()


def _on_palco_theme_change():
    temas_list = load_temas(st.session_state.book)
    if not temas_list:
        st.session_state.take = 0
        st.session_state.tema = ""
        return

    take = _coerce_take(
        st.session_state.get("opt_take_palco", st.session_state.get("take", 0)),
        temas_list,
    )

    st.session_state.take = take
    st.session_state.tema = temas_list[take]


def pick_book_sidebar(where="sidebar"):
    """Escolhe o livro yPoemas na sidebar ou no palco."""
    _sync_book_theme_state()

    books_list = BOOKS_LIST
    current = st.session_state.book
    key = "sidebar_book_select" if where == "sidebar" else "palco_book_select"
    _prepare_book_widget(key)

    container = st.sidebar if where == "sidebar" else st
    if where == "sidebar":
        label = translate("yPoemas disponíveis...")
    else:
        label = f"{len(books_list)} " + translate("livros disponíveis...")
    callback = _on_sidebar_book_change if where == "sidebar" else _on_palco_book_change

    container.selectbox(
        label,
        books_list,
        index=books_list.index(current),
        key=key,
        on_change=callback,
    )


def pick_tema_palco():
    """Escolhe o tema atual do livro diretamente no palco."""
    _sync_book_theme_state()
    temas_list = load_temas(st.session_state.book)
    if not temas_list:
        return

    _prepare_theme_widget()
    options = list(range(len(temas_list)))
    st.selectbox(
        f"↓  {len(temas_list)} " + translate("temas"),
        options,
        index=_coerce_take(st.session_state.get("take", 0), temas_list),
        format_func=lambda z: temas_list[z],
        key="opt_take_palco",
        on_change=_on_palco_theme_change,
    )


def pick_stage_font():
    """Escolhe fonte e corpo de leitura do Palco."""
    labels = [label for label, fonte in FONTES_MACHINA]
    lookup = {label: fonte for label, fonte in FONTES_MACHINA}

    current_font = st.session_state.get("stage_font", "Trebuchet")
    current_label = next(
        (label for label, fonte in FONTES_MACHINA if fonte == current_font),
        labels[0],
    )

    corpos = list(range(15, 25))
    current_size = st.session_state.get("stage_size", 21)
    if current_size not in corpos:
        current_size = 21

    col_font, col_corpo = st.sidebar.columns([2.1, 0.9])

    with col_font:
        choice = st.selectbox(
            translate("fontes & letras"),
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


def show_icons():  # https://api.whatsapp.com/
    with st.sidebar:
        st.sidebar.markdown(
            f"""
            <nav>
            <a href='https://www.facebook.com/nandoulopes' target='_blank'>•••   face </a>
            <a href='mailto:lopes.fernando@hotmail.com' target='_blank'>  e-mail   </a>
            <a href='https://www.instagram.com/fernando.lopes.942/' target='_blank'>  insta  </a>
            <a href='https://web.whatsapp.com/send?phone=+5512991368181' target='_blank'>  zapp  •••</a>
            </nav>
            """,
            unsafe_allow_html=True,
        )


def load_help(idiom):
    returns = []
    returns.append(translate("tema anterior"))
    returns.append(translate("escolhe tema ao acaso"))
    returns.append(translate("próximo tema"))
    returns.append(translate("mais lidos..."))
    returns.append(translate("gera nova versão do tema"))
    returns.append(translate("arte"))
    returns.append(translate("voz"))

    return returns


def draw_check_buttons():
    help_tips = load_help(st.session_state.lang)
    help_draw = help_tips[5]
    help_talk = help_tips[6]

    col_arte, col_voz = st.sidebar.columns([1, 1])

    with col_arte:
        if st.button(
            translate("arte"),
            key="ctrl_arte",
            help=help_draw,
            use_container_width=True,
        ):
            st.session_state.draw = not st.session_state.draw

    with col_voz:
        if st.button(
            translate("voz"),
            key="ctrl_voz",
            help=help_talk,
            use_container_width=True,
        ):
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


# @st.cache_data
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

    # Padrão curatorial atual: ABOUT_index.md
    # Fallback histórico: ABOUT_INDEX.md
    index_candidates = [
        os.path.join("./md_files/ABOUT_index.md"),
        os.path.join("./md_files/ABOUT_INDEX.md"),
    ]

    index_file = None
    for candidate in index_candidates:
        if os.path.exists(candidate):
            index_file = candidate
            break

    if index_file is None:
        return index_list

    with open(index_file, encoding="utf-8") as lista:
        for line in lista:
            index_list.append(line)

    return index_list



def load_lypo():  # Load last yPoema & replace '\n' with '<br>' for translator returned text
    lypo_text = ""
    lypo_user = "LYPO_" + IPAddres
    with open(os.path.join("./temp/" + lypo_user), encoding="utf-8", errors="replace") as script:
        for line in script:
            line = line.strip()
            lypo_text += line + "<br>"

    return lypo_text


def load_typo():  # Load translated yPoema & clean translator returned bugs in text
    typo_text = ""
    typo_user = "TYPO_" + IPAddres
    with open(os.path.join("./temp/" + typo_user), encoding="utf-8", errors="replace") as script:
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


@st.cache_data
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

        
def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):  # ver save_img.py
    if LOGO_IMAGE is None:
        st.markdown(
            f"""
            <div class='container'>
                <p class='logo-text' style="font-family:{st.session_state.get('stage_font', 'Trebuchet MS')}; font-size:{st.session_state.get('stage_size', 21)}px;">{LOGO_TEXTO}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class='container'>
                <img class='logo-img' src='data:image/jpg;base64,{base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()}'>
                <p class='logo-text' style="font-family:{st.session_state.get('stage_font', 'Trebuchet MS')}; font-size:{st.session_state.get('stage_size', 21)}px;">{LOGO_TEXTO}</p>
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

    temas_list = load_temas("poemas")
    maxy_ypoemas = len(temas_list)
    st.session_state.take = random.randrange(0, maxy_ypoemas)
    st.session_state.tema = temas_list[st.session_state.take]

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

    foo1, more, rand, auto, foo2 = st.columns([3.55, 1, 1, 1.9, 3.55])

    help_tips = load_help(st.session_state.lang)
    help_rand = help_tips[1]
    help_more = help_tips[4]
    rand = rand.button("✻", help=help_rand)

    with auto:
        if st.button("auto", key="mini_auto_button", help="modo automático", use_container_width=True):
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

        mini_status = (
            "🌿  "
            + st.session_state.lang
            + " - "
            + st.session_state.tema
            + " ( "
            + str(st.session_state.mini + 1)
            + " / "
            + str(len(temas_list))
            + " )"
        )
        mini_expander = st.expander(mini_status, expanded=True)
        with mini_expander:
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
    if (
        st.session_state.take > maxy_ypoemas or st.session_state.take < 0
    ):  # just in case
        st.session_state.take = 0

    col_livros, col_nav, col_temas = st.columns([3.6, 2.8, 3.6])

    with col_livros:
        pick_book_sidebar("palco")

    with col_nav:
        help_tips = load_help(st.session_state.lang)
        help_last = help_tips[0]
        help_rand = help_tips[1]
        help_nest = help_tips[2]
        help_more = help_tips[4]

        nav_cols = st.columns([1, 1, 1, 1, 1])
        more = nav_cols[0].button("✚", help=help_more, use_container_width=True)
        last = nav_cols[1].button("◀", help=help_last, use_container_width=True)
        rand = nav_cols[2].button("✻", help=help_rand, use_container_width=True)
        nest = nav_cols[3].button("▶", help=help_nest, use_container_width=True)
        manu = nav_cols[4].button("?", help="help !!!", use_container_width=True)

    temas_list = load_temas(st.session_state.book)
    maxy_ypoemas = len(temas_list) - 1
    if st.session_state.take > maxy_ypoemas or st.session_state.take < 0:
        st.session_state.take = 0

    if last:
        st.session_state.take -= 1
        if st.session_state.take < 0:
            st.session_state.take = maxy_ypoemas
        _sync_book_theme_state()

    if rand:
        st.session_state.take = random.randrange(0, maxy_ypoemas + 1)
        _sync_book_theme_state()

    if nest:
        st.session_state.take += 1
        if st.session_state.take > maxy_ypoemas:
            st.session_state.take = 0
        _sync_book_theme_state()

    with col_temas:
        pick_tema_palco()

    temas_list = load_temas(st.session_state.book)
    _sync_book_theme_state()

    lnew = True
    if manu:
        st.subheader(load_md_file("MANUAL_YPOEMAS.md"))

    if lnew:
        what_book = (
            "🌿  "
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

        if st.session_state.get("sidebar_panel") == "CIA":
            with st.expander("🗝 Chave de Ouro — CIA v0", expanded=True):
                st.markdown(
                    "Mood ativo: **" + st.session_state.get("cia_mood", CIA_MOODS[0]) + "**  \n"
                    + "Tema em foco: **" + st.session_state.tema + "**  \n"
                    + "\nDescoberta da Chave em construção. O palco está preparado para a convivência entre yPoema e Chave.",
                    unsafe_allow_html=False,
                )

        # st.markdown(get_binary_file_downloader_html('./temp/'+'LYPO_' + IPAddres, '➪ '+st.session_state.tema), unsafe_allow_html=True)

def page_eureka():
    help_tips = load_help(st.session_state.lang)
    help_rand = help_tips[1]
    help_more = help_tips[4]

    seed, more, rand, manu, occurrences = st.columns([2.5, 1.5, 1.5, 0.7, 4])

    with seed:
        find_what = st.text_input(
            label=translate("buscar por..."),
            help=translate("digite uma palavra - ou parte dela - que você goste..."),
        )

    with more:
        more = more.button("✚", help=help_more)

    with rand:
        rand = rand.button("✻", help=help_rand)

    with manu:
        manu = manu.button("?", help="help !!!")

    if manu:
        st.subheader(load_md_file("MANUAL_EUREKA.md"))

    if len(find_what) < 3:
        st.warning(translate("comece com pelo menos 3 letras..."))
    else:
        seed_list = []
        soma_tema = []

        eureka_list = load_eureka(find_what)
        for line in eureka_list:
            this_line = line.strip("\n")
            part_line = this_line.partition(" : ")
            palas = part_line[0]
            fonte = part_line[2]
            seed_tema = fonte.partition("_")[0]
            if (palas is None) or (fonte is None):
                continue
            else:
                seed_list.append(palas + " ➪ " + fonte)
                if not seed_tema in soma_tema:
                    soma_tema.append(seed_tema)

        if (not more) and (not manu):
            st.session_state.eureka = 0

        if len(seed_list) == 0:
            st.warning(
                translate(
                    'nenhuma ocorrência das letras " '
                    + find_what
                    + ' " foi encontrada...'
                )
            )
        elif len(seed_list) >= 1:
            seed_list.sort()
            if len(seed_list) == 1:
                info_find = translate('ocorrência de "')
            else:
                info_find = translate('ocorrências de "')

            info_find += find_what
            if len(soma_tema) > 1:
                info_find += translate('" em ' + str(len(soma_tema)) + " temas")

            if rand:
                old_eureka = st.session_state.get("eureka", 0)
                if len(seed_list) > 1:
                    new_eureka = random.randrange(0, len(seed_list))
                    while new_eureka == old_eureka:
                        new_eureka = random.randrange(0, len(seed_list))
                    st.session_state.eureka = new_eureka
                else:
                    st.session_state.eureka = 0

                # O selectbox precisa refletir a ocorrência sorteada.
                st.session_state["opt_ocur"] = st.session_state.eureka

            with occurrences:
                options = list(range(len(seed_list)))
                opt_ocur = st.selectbox(
                    "↓  " + str(len(seed_list)) + " " + info_find,
                    options,
                    index=st.session_state.eureka,
                    format_func=lambda y: seed_list[y],
                    key="opt_ocur",
                )

            if not rand:
                st.session_state.eureka = opt_ocur

            this_seed = seed_list[st.session_state.eureka]
            part_line = this_seed.partition(" ➪ ")
            nome_tema = part_line[2]
            seed_tema = nome_tema.partition("_")[0]

            st.session_state.tema = seed_tema

            if st.session_state.lang != st.session_state.last_lang:
                curr_ypoema = load_lypo()  # changes in lang, keep LYPO
            else:
                curr_ypoema = load_poema(seed_tema, this_seed)
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

            lnew = True
            if lnew:
                eureka_expander = st.expander("", expanded=True)
                with eureka_expander:
                    LOGO_TEXTO = curr_ypoema
                    LOGO_IMAGE = None
                    if st.session_state.draw:
                        LOGO_IMAGE = load_arts(seed_tema)

                    write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
                    update_readings(seed_tema)

                if st.session_state.talk:
                    talk(curr_ypoema)
            if manu:
                lnew = False
                LOGO_TEXTO = load_info(seed_tema)
                if st.session_state.lang != "pt":  # translate if idioma <> pt
                    LOGO_TEXTO = translate(LOGO_TEXTO)

                LOGO_IMAGE = "./images/matrix/" + seed_tema.capitalize() + ".jpg"
                write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

        else:
            st.warning(
                translate(
                    "nenhum verbete encontrado com essas letras ---> " + find_what
                )
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
            "🌿  "
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



def load_about_md(title):
    """Carrega ABOUTs pelo padrão curatorial explícito.

    Padrão principal: ABOUT_nome_titulo.md.
    Sem uppercase automático: nome de arquivo é assunto de curadoria.
    """
    candidates = ABOUTS_FILES.get(title, ["ABOUT_" + title.replace(" ", "_") + ".md"])

    last_file = candidates[-1] if candidates else title
    for file_name in candidates:
        full_path = os.path.join("./md_files/" + file_name)
        if os.path.exists(full_path):
            return load_md_file(file_name)

    return translate("ooops... arquivo ( " + last_file + " ) não pode ser aberto.")


def page_abouts():
    abouts_list = ABOUTS_LIST

    options = list(range(len(abouts_list)))
    sobrios = "↓  " + translate("sobre")
    opt_abouts = st.selectbox(
        sobrios,
        options,
        format_func=lambda x: abouts_list[x],
        key="opt_abouts",
    )

    choice = abouts_list[opt_abouts]

    about_expander = st.expander("", True)
    with about_expander:
        if choice == "machina":
            st.subheader(load_md_file("ABOUT_machina I.md"))
            LOGO_TEXTO = load_info(st.session_state.tema)
            LOGO_IMAGE = "./images/matrix/" + st.session_state.tema + ".jpg"
            write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
            st.subheader(load_md_file("ABOUT_machina II.md"))
        else:
            st.subheader(load_about_md(choice))


### eof: pages


def render_sidebar_for_page(chosen_id):
    """Renderiza a sidebar na ordem curatorial correta."""
    pick_lang()
    pick_book_sidebar()
    pick_stage_font()
    draw_check_buttons()
    draw_sidebar_panel_buttons(chosen_id)



def main():
    gramado = open_gramado()

    with gramado:
        _pag_esq, _pag_centro, _pag_dir = st.columns([0.03, 9.94, 0.03])

        with _pag_centro:
            chosen_id = stx.tab_bar(
                data=[
                    stx.TabBarItemData(id=1, title="mini", description=""),
                    stx.TabBarItemData(id=2, title="yPoemas", description=""),
                    stx.TabBarItemData(id=3, title="eureka", description=""),
                    stx.TabBarItemData(id=4, title="off-mach", description=""),
                    stx.TabBarItemData(id=5, title="about", description=""),
                ],
                default=2,
            )

        chosen_id = str(chosen_id)

        page_image_map = {
            "1": "img_mini.jpg",
            "2": "img_ypoemas.jpg",
            "3": "img_eureka.jpg",
            "4": "img_off-machina.jpg",
            "5": "img_about.jpg",
        }
        magy = page_image_map.get(chosen_id, "img_ypoemas.jpg")

        render_sidebar_for_page(chosen_id)

        with st.sidebar:
            st.image("./images/" + magy)

        if chosen_id == "2" and st.session_state.get("sidebar_panel", "Machina") == "CIA":
            render_cia_sidebar()

        palco = st.container()
        with palco:
            palco_container = open_palco()

            with palco_container:
                if chosen_id == "1":
                    magy = "img_mini.jpg"
                    page_mini()
                    status = f"🌿  {st.session_state.lang} - {st.session_state.tema} ( {st.session_state.mini + 1} / {len(load_temas("todos os temas"))} )"
                elif chosen_id == "2":
                    magy = "img_ypoemas.jpg"
                    page_ypoemas()
                    status = palco_status(
                        st.session_state.book,
                        st.session_state.get("take", 0) + 1,
                        len(load_temas(st.session_state.book)),
                    )
                elif chosen_id == "3":
                    magy = "img_eureka.jpg"
                    page_eureka()
                    status = palco_status("eureka")
                elif chosen_id == "4":
                    magy = "img_off-machina.jpg"
                    page_off_machina()
                    status = palco_status("off-machina")
                elif chosen_id == "5":
                    magy = "img_about.jpg"
                    page_abouts()
                    status = palco_status("about")
                else:
                    magy = "img_ypoemas.jpg"
                    page_ypoemas()
                    status = palco_status(
                        st.session_state.book,
                        st.session_state.get("take", 0) + 1,
                        len(load_temas(st.session_state.book)),
                    )

                st.markdown(
                    f"<div class='machina-rodape-palco'>{status}</div>",
                    unsafe_allow_html=True,
                )


    show_icons()
    ##$ st.sidebar.state = True

if __name__ == "__main__":
    main()
