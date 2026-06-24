import os
import re
import time
import random
import base64
import html
import socket
import asyncio
import streamlit as st
import streamlit.components.v1 as components

APP_BUILD = "2026-06-24_a_sidebar_de_verdade__copy_reset"
APP_BUILD_NOTES = "Sidebar nativa + respiro CIA + limpeza do pacote de cópias ao trocar yPoema."
from extra_streamlit_components import TabBar as stx

from lay_2_ypo import gera_poema
from readings import (
    list_readings,
    update_readings,
    update_visy,
)


from controle_cia import (
    configure_cia,
    draw_sidebar_panel_buttons,
    render_cia_stage,
    guia_do_leitor_cia,
    limpar_cia_palco,
    _cia_objeto_analise_existe,
    _cia_fixar_objeto_analise,
    _cia_restaurar_identidade_objeto,
    _restore_cia_freeze_before_sync,
    render_cia_mood_selectbox,
    _cia_sidebar_filha_active,
    apply_sidebar_mae_filha_styles,
    render_sidebar_filha,
)


ABOUTS_LIST = [
    "comentários", "prefácil", "machina", "off-machina", "outros autores", "livros", "bibliografia",
    "notes", "imagens", "pontuação", "poly", "tradittore", "pensares", "machina-IA", "samizdàt", "index", "license",
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
    "a_torre_de_papel", "quase_que_eu_Poesia", "faz_de_conto", "um_romance", "parafernália",
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
    "en": "en-US-AvaNeural",
    "gl": "gl-ES-RoiNeural",
    "eu": "eu-ES-AnderNeural",
    "de": "de-DE-ConradNeural",
    "da": "da-DK-JeppeNeural",
    "nl": "nl-NL-MaartenNeural",
    "pl": "pl-PL-MarekNeural",
    "ro": "ro-RO-EmilNeural",
    "no": "nb-NO-PernilleNeural",
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
    page_icon=":bulb:",
    layout="wide",
    initial_sidebar_state="collapsed",
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
        .machina-palco-titulo {
            display: block;
            text-align: center;
            text-decoration: underline;
            text-underline-offset: 0.18em;
            margin: 0 auto 0.35em auto;
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
            font-family: 'Trebuchet MS';
            color: #000000;
            padding-top: 0px;
            padding-left: 8px;
        }

        .machina-ypoema-text {
            font-family: var(--machina-ypoema-font, 'Trebuchet MS') !important;
            font-size: var(--machina-ypoema-size, 21px) !important;
            line-height: 1.35 !important;
        }

        /* yPoema sem arte: ocupa o palco sem coluna fantasma */
        .machina-ypoema-solo {
            width: 100% !important;
            max-width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            align-items: flex-start !important;
            box-sizing: border-box !important;
            padding: 0.10rem 0.35rem 0.25rem 0.35rem !important;
        }

        .machina-ypoema-solo .machina-ypoema-text {
            display: block !important;
            width: auto !important;
            max-width: min(78ch, 86%) !important;
            margin-left: auto !important;
            margin-right: auto !important;
            padding-left: 0 !important;
            text-align: left !important;
            box-sizing: border-box !important;
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


        /* Sidebar :: nativa/recolhível — oficina disponível, palco livre */
        [data-testid="stSidebar"] {
            background-color: #eef6fb !important;
        }

        [data-testid="stSidebar"] .machina-sidebar-title {
            text-align: center;
            font-family: 'Trebuchet MS';
            font-size: 1.04rem;
            font-weight: 600;
            letter-spacing: 0.025rem;
            margin: -0.15rem 0 0.25rem 0;
            opacity: 0.88;
        }

        [data-testid="stSidebar"] > div:first-child {
            background-color: #eef6fb !important;
            padding-top: 0.00rem !important;
        }

        /* Sidebar :: scroll_inho — sobe discretamente o primeiro controle */
        [data-testid="stSidebar"] div[data-testid="stSidebarContent"] {
            padding-top: 0.00rem !important;
            margin-top: -0.55rem !important;
        }

        [data-testid="stSidebar"] div[data-testid="stElementContainer"]:first-child {
            margin-top: -0.35rem !important;
        }

        [data-testid="stSidebar"] .stButton button {
            white-space: nowrap !important;
            word-break: keep-all !important;
            padding-left: 0.25rem !important;
            padding-right: 0.25rem !important;
            min-width: 100% !important;
        }

        [data-testid="stSidebar"] div[data-testid="stButton"] {
            margin-top: -0.12rem !important;
            margin-bottom: -0.12rem !important;
        }

        [data-testid="stSidebar"] .stButton button {
            min-height: 1.94rem !important;
            padding-top: 0.11rem !important;
            padding-bottom: 0.11rem !important;
        }

        [data-testid="stSidebar"] .stButton button p {
            margin: 0 !important;
            padding: 0 !important;
            text-indent: 0 !important;
        }

        [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
            gap: 0.68rem !important;
        }


        /* Sidebar :: respiro vertical entre controles */
        [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
            gap: 0.50rem !important;
        }

        [data-testid="stSidebar"] div[data-testid="stElementContainer"] {
            margin-bottom: 0.12rem !important;
        }


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

        iframe[title="extra_streamlit_components.TabBar.tab_bar"] {
            margin-top: -0.62rem !important;
            margin-bottom: 0 !important;
        }

        div[data-testid="stElementContainer"] {
            margin-top: 0 !important;
        }

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
            margin-left: auto !important;
            margin-right: auto !important;
            box-sizing: border-box !important;
        }
        /* Palco e divider :: mesma largura visual */

        .machina-divider-palco {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0.04rem auto 0.16rem auto !important;
            padding: 0 !important;
            box-sizing: border-box !important;
            border: 0 !important;
            box-shadow: none !important;
            outline: 0 !important;
        }

        .machina-divider-palco hr {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            border: 0 !important;
            border-top: 1px solid rgba(0,0,0,0.18) !important;
            box-shadow: none !important;
            outline: 0 !important;
        }

        div[data-testid="stHorizontalBlock"],
        div[data-testid="stHorizontalBlock"] > div,
        div[data-testid="stHorizontalBlock"] button {
            border: 0 !important;
            border-bottom: 0 !important;
            box-shadow: none !important;
            outline: 0 !important;
        }

        /* Palco :: remove a sombra/linha fantasma entre labels e controles */
        div[data-testid="stSelectbox"],
        div[data-testid="stSelectbox"] > div,
        div[data-testid="stSelectbox"] [data-baseweb="select"],
        div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
        div[data-testid="stSelectbox"] [data-baseweb="select"] div,
        div[data-testid="stButton"] > button,
        div[data-testid="stButton"] > button:hover,
        div[data-testid="stButton"] > button:focus,
        div[data-testid="stButton"] > button:active {
            border-top: 0 !important;
            border-right: 0 !important;
            border-bottom: 0 !important;
            border-left: 0 !important;
            box-shadow: none !important;
            outline: 0 !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] > div:hover,
        div[data-testid="stSelectbox"] [data-baseweb="select"] > div:focus,
        div[data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within {
            border: 0 !important;
            box-shadow: none !important;
            outline: 0 !important;
        }

        /* Navegação :: solução invisível
           Desce os botões para alinhar com os selectboxes de livros/temas.
           A linha fantasma deixa de atravessar visualmente os botões. */
        .machina-nav-spacer {
            height: 1.72rem !important;
            min-height: 1.72rem !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1.72rem !important;
            font-size: 1px !important;
        }

        .machina-nav-spacer p {
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1.72rem !important;
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
        "cia_reading_mode": False,
        "cia_mood_select": "Sintática",
        "cia_line0_offset_px": -385,
        "cia_font": "Trebuchet MS",
        "cia_size": 18,
        "cia_palco_size": 18,
        "tema_last_analise": "",
        "ypoema_em_analise": "",
        "tema_em_analise": "",
        "book_em_analise": "",
        "take_em_analise": -1,
        "lang_em_analise": "",
        "cia_mood_changed": False,
        "cia_force_new_poema": False,
        "cia_freeze_book": "",
        "cia_freeze_take": -1,
        "cia_freeze_tema": "",

        # chave de ouro
        "key_open": False,
        "key_poema_texto": "",
        "key_poema_tema": "",
        "key_analise": "",
        "copy_qtd": 1,
        "copy_qtd_widget": 1,
        "copy_bundle_text": "",
        "copy_bundle_token": 0,
        "copy_bundle_qtd": 0,
        "copy_bundle_source": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


apply_styles()
init_session_state()


def _copy_bundle_source_key(curr_ypoema=""):
    """Identidade do yPoema usado pelo pacote de cópias.

    Evita que um pacote montado para um tema/variação continue visível
    depois de troca de tema, livro, idioma ou nova variação.
    """
    texto = str(curr_ypoema or "")
    return "|".join([
        str(st.session_state.get("book", "")),
        str(st.session_state.get("take", "")),
        str(st.session_state.get("tema", "")),
        str(st.session_state.get("lang", "")),
        str(hash(texto)),
    ])


def limpar_copias_palco():
    """Remove pacote de cópias antigo sem alterar a quantidade escolhida."""
    st.session_state["copy_bundle_text"] = ""
    st.session_state["copy_bundle_qtd"] = 0
    st.session_state["copy_bundle_source"] = ""
    st.session_state["copy_bundle_token"] = int(st.session_state.get("copy_bundle_token", 0)) + 1


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
    ("Trebuchet", "Trebuchet MS"),
    ("Inter", "Inter"),
    ("Spectral", "Spectral"),
    ("EB Garamond", "EB Garamond"),
    ("Libre Baskerville", "Libre Baskerville"),
    ("Cormorant Garamond", "Cormorant Garamond"),
    ("Palatino", "Palatino Linotype"),
    ("Georgia", "Georgia"),
    ("Atkinson Hyperlegible", "Atkinson Hyperlegible"),
    ("OpenDyslexic", "OpenDyslexic"),
    ("JetBrains Mono", "JetBrains Mono"),
    ("Courier", "Courier New"),
    ("IBM Plex Sans", "IBM Plex Sans"),
]

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

    old_take = st.session_state.get("take", 0)
    st.session_state.take = take
    st.session_state.tema = temas_list[take]
    if take != old_take:
        st.session_state["cia_force_new_poema"] = True


def _current_book():
    """Retorna o livro atual sem depender de atributo já criado no session_state."""
    book = st.session_state.get("book", BOOKS_LIST[0])
    return book if book in BOOKS_LIST else BOOKS_LIST[0]


def _prepare_book_widget(key):
    """Faz o widget espelhar `book` sem tomar conta do estado."""
    current = _current_book()
    if key in st.session_state and st.session_state.get(key) != current:
        del st.session_state[key]


def _prepare_theme_widget():
    """Normaliza o widget de temas para espelhar sempre o `take` atual."""
    temas_list = load_temas(_current_book())
    current = _coerce_take(st.session_state.get("take", 0), temas_list)
    raw_value = st.session_state.get("opt_take_palco", current)
    normalized = _coerce_take(raw_value, temas_list)

    # A lista de temas deve seguir o yPoema exibido no palco.
    # Se navegação por botões alterou `take`, o widget precisa espelhar isso
    # antes de ser instanciado pelo Streamlit neste ciclo.
    if normalized != current:
        st.session_state["opt_take_palco"] = current
    elif normalized != raw_value:
        st.session_state["opt_take_palco"] = normalized

def _on_palco_book_change():
    current_book = _current_book()
    choice = st.session_state.get("palco_book_select", current_book)
    if choice != current_book:
        st.session_state.book = choice
        st.session_state.take = 0
        st.session_state["cia_last_action"] = "book_change"
        limpar_cia_palco()
        limpar_copias_palco()
        st.session_state["cia_force_new_poema"] = True
    _sync_book_theme_state()


def _on_palco_theme_change():
    temas_list = load_temas(_current_book())
    if not temas_list:
        st.session_state.take = 0
        st.session_state.tema = ""
        return

    take = _coerce_take(
        st.session_state.get("opt_take_palco", st.session_state.get("take", 0)),
        temas_list,
    )

    old_take = st.session_state.get("take", 0)
    st.session_state.take = take
    st.session_state.tema = temas_list[take]
    if take != old_take:
        st.session_state["cia_last_action"] = "theme_change"
        limpar_cia_palco()
        limpar_copias_palco()
        st.session_state["cia_force_new_poema"] = True


def pick_book_palco():
    """Escolhe o livro yPoemas diretamente no palco."""
    _sync_book_theme_state()

    books_list = BOOKS_LIST
    current = _current_book()
    key = "palco_book_select"
    _prepare_book_widget(key)

    st.selectbox(
        "↓  " + str(len(books_list)) + " livros",
        books_list,
        index=books_list.index(current),
        key=key,
        on_change=_on_palco_book_change,
    )


def pick_tema_palco():

    """Escolhe o tema atual do livro diretamente no palco."""
    _sync_book_theme_state()
    temas_list = load_temas(_current_book())
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


def render_help_ypoemas_mesma_fonte():
    """Renderiza o Help yPoemas com a fonte/corpo escolhidos pelo leitor.

    Cabeçalhos Markdown (#, ##, ###) viram apenas negrito para evitar
    poluição visual e respeitar a escala do palco.
    """
    raw = load_md_file("MANUAL_YPOEMAS.md")
    stage_font = st.session_state.get("stage_font", "Trebuchet MS")
    stage_size = int(st.session_state.get("stage_size", 21))

    html_lines = []
    for raw_line in str(raw).splitlines():
        line = raw_line.strip()
        if not line:
            html_lines.append("")
            continue

        heading = re.match(r"^#{1,6}\s+(.+)$", line)
        if heading:
            text = html.escape(heading.group(1).strip())
            html_lines.append(f"<strong>{text}</strong>")
            continue

        text = html.escape(line)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        html_lines.append(text)

    content = "<br>".join(html_lines)

    st.markdown(
        f"""
        <div class='container'>
            <p class='logo-text machina-ypoema-text' style="--machina-ypoema-font:'{stage_font}'; --machina-ypoema-size:{stage_size}px; font-family:'{stage_font}' !important; font-size:{stage_size}px !important; line-height:1.42 !important;">{content}</p>
        </div>
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


def _trim_blank_edges_preservando_recuo(linhas):
    """Remove só linhas vazias nas bordas, sem apagar recuos autorais.

    Importante: recuos vindos do |$| podem chegar ao pacote como &emsp;.
    Depois de html.unescape, &emsp; vira espaço largo real (\u2003).
    Portanto não usar .strip() no texto inteiro, senão o recuo da primeira
    linha desaparece.
    """
    linhas = [str(linha).rstrip() for linha in linhas]
    while linhas and not linhas[0].strip():
        linhas.pop(0)
    while linhas and not linhas[-1].strip():
        linhas.pop()
    return "\n".join(linhas)


def _ypoema_html_to_text(ypoema_html):
    """Converte o yPoema renderizado em HTML simples para texto copiável."""
    texto = str(ypoema_html or "")
    texto = texto.replace("<br/>", "\n").replace("<br />", "\n").replace("<br>", "\n")
    texto = re.sub(r"<[^>]+>", "", texto)
    texto = html.unescape(texto)
    return _trim_blank_edges_preservando_recuo(texto.splitlines())


def _gerar_ypoema_texto_cru(nome_tema):
    """Gera uma variação sem alterar LYPO/TYPO nem o yPoema do palco."""
    script = gera_poema(nome_tema, "")
    linhas = [nome_tema]
    for line in script:
        if line == "\n":
            linhas.append("")
        else:
            # Preserva recuos autorais do |$|: &emsp; vira espaço largo real.
            linhas.append(html.unescape(str(line).rstrip("\n")))
    return _trim_blank_edges_preservando_recuo(linhas)


def _remover_titulo_inicial_duplicado(texto, nome_tema):
    """Remove o título interno quando ele repete o nome do tema, preservando recuos."""
    linhas = str(texto or "").splitlines()
    while linhas and not linhas[0].strip():
        linhas.pop(0)

    if linhas and linhas[0].strip().casefold() == str(nome_tema or "").strip().casefold():
        linhas.pop(0)
        while linhas and not linhas[0].strip():
            linhas.pop(0)

    return _trim_blank_edges_preservando_recuo(linhas)


def montar_copias_ypoema(curr_ypoema, nome_tema, qtd):
    """Monta 1..9 cópias/variações para leitura externa, em desenho clean."""
    try:
        qtd = int(qtd)
    except Exception:
        qtd = 1
    qtd = max(1, min(9, qtd))

    partes = []
    atual = _ypoema_html_to_text(curr_ypoema)

    for n in range(1, qtd + 1):
        if n == 1 and atual:
            texto = atual
        else:
            texto = _gerar_ypoema_texto_cru(nome_tema)

        texto = _remover_titulo_inicial_duplicado(texto, nome_tema)

        partes.append(
            f"___\n\n"
            f"{nome_tema} #{n}\n\n"
            f"{texto}"
        )

    return ("\n".join(partes).strip() + "\n___").strip()


def render_copy_bundle_widget(texto, token, qtd_real=None):
    """Mostra o pacote completo para copiar.

    Regra deste GO:
    - o texto final precisa conter TODAS as variações pedidas;
    - o leitor precisa conseguir conferir o pacote inteiro;
    - o botão JS é só atalho; o st.text_area é o fallback confiável.
    """
    if not texto:
        return

    texto = str(texto)
    try:
        total_blocos = int(qtd_real) if qtd_real is not None else 0
    except Exception:
        total_blocos = 0
    if total_blocos < 1:
        # Conta os blocos pelo desenho clean: cada yPoema começa com uma linha "___".
        # Se houver "___" final de fechamento, ele não entra na conta.
        marcadores = len(re.findall(r"(?m)^___\s*$", texto))
        total_blocos = marcadores - 1 if texto.strip().endswith("___") and marcadores > 1 else marcadores
        total_blocos = max(1, total_blocos)

    # Fallback nativo e visível: mesmo se o clipboard do navegador/iframe falhar,
    # este campo contém o pacote inteiro para Ctrl+A / Ctrl+C.
    st.text_area(
        f"pacote para copiar ({total_blocos} yPoema(s))",
        value=texto,
        height=420,
        key=f"copy_bundle_textarea_{token}",
        label_visibility="visible",
    )

    # Atalho JS: usa JSON para preservar quebras de linha, aspas, crases etc.
    import json
    js_text = json.dumps(texto, ensure_ascii=False)

    components.html(
        f"""
        <div style="font-family:system-ui, sans-serif; font-size:13px; padding:2px 0 6px 0;">
            <button id="copy_btn_{token}" style="
                border:0;
                border-radius:8px;
                padding:6px 10px;
                cursor:pointer;
                background:#eef6fb;
                font-size:13px;">
                📋 copiar pacote inteiro
            </button>
            <span id="copy_msg_{token}" style="margin-left:8px; opacity:.72;"></span>
        </div>
        <script>
        const txt_{token} = {js_text};
        const btn_{token} = document.getElementById("copy_btn_{token}");
        const msg_{token} = document.getElementById("copy_msg_{token}");

        async function copyMachina_{token}() {{
            try {{
                await navigator.clipboard.writeText(txt_{token});
                msg_{token}.innerText = "copiado";
            }} catch (e) {{
                msg_{token}.innerText = "use Ctrl+A / Ctrl+C no campo acima";
            }}
        }}

        btn_{token}.addEventListener("click", copyMachina_{token});
        </script>
        """,
        height=52,
    )


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

    if not arts_list:
        return None

    available_arts = [image for image in arts_list if image not in st.session_state.arts]
    if not available_arts:
        available_arts = arts_list

    image = random.choice(available_arts)
    st.session_state.arts.append(image)

    if len(st.session_state.arts) > 36:  # remove first
        del st.session_state.arts[0]

    logo = path + image

    return logo


### eof: loaders
### bof: functions




def _palco_titulo_centralizado(LOGO_TEXTO):
    """Centraliza e sublinha o título do texto no palco, mantendo o corpo intacto."""
    texto = str(LOGO_TEXTO or "")
    marcador = "<br>"
    texto = texto.replace("<br/>", marcador).replace("<br />", marcador)

    partes = texto.split(marcador)
    if len(partes) <= 1:
        return texto

    titulo = partes[0].strip()
    corpo = marcador.join(partes[1:]).strip()
    if not titulo or not corpo:
        return texto

    return (
        "<span class='machina-palco-titulo'>"
        + titulo
        + "</span>"
        + marcador
        + corpo
    )


def _fonte_palco_leitor():
    """Fonte escolhida pelo leitor para o yPoema."""
    fonte = st.session_state.get("stage_font", "Trebuchet MS")
    if fonte == "Trebuchet":
        fonte = "Trebuchet MS"
    return fonte


def _corpo_palco_leitor():
    """Corpo escolhido pelo leitor para o yPoema."""
    try:
        corpo = int(st.session_state.get("stage_size", 21))
    except Exception:
        corpo = 21
    return max(15, min(24, corpo))


def _corpo_palco_cia():
    """Corpo protegido pela Machina quando yPoema e CIA dividem o palco."""
    return int(st.session_state.get("cia_palco_size", st.session_state.get("cia_size", 18)))


def write_ypoema_cia_palco(LOGO_TEXTO, LOGO_IMAGE=None):
    """Renderiza o yPoema no palco da CIA: mesma fonte, corpo protegido."""
    LOGO_TEXTO = _palco_titulo_centralizado(LOGO_TEXTO)
    stage_font = _fonte_palco_leitor()
    palco_size = _corpo_palco_cia()

    if LOGO_IMAGE is None:
        st.markdown(
            f"""
            <div class='container'>
                <p class='logo-text' style="font-family:{stage_font}; font-size:{palco_size}px;">{LOGO_TEXTO}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class='container'>
                <img class='logo-img' src='data:image/jpg;base64,{base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()}'>
                <p class='logo-text' style="font-family:{stage_font}; font-size:{palco_size}px;">{LOGO_TEXTO}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):  # ver save_img.py
    LOGO_TEXTO = _palco_titulo_centralizado(LOGO_TEXTO)
    stage_font = _fonte_palco_leitor()
    stage_size = _corpo_palco_leitor()
    ypo_style = (
        f"--machina-ypoema-font:'{stage_font}'; "
        f"--machina-ypoema-size:{stage_size}px; "
        f"font-family:'{stage_font}' !important; "
        f"font-size:{stage_size}px !important;"
    )

    if LOGO_IMAGE is None:
        st.markdown(
            f"""
            <div class='machina-ypoema-solo'>
                <p class='logo-text machina-ypoema-text' style="{ypo_style}">{LOGO_TEXTO}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class='container'>
                <img class='logo-img' src='data:image/jpg;base64,{base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()}'>
                <p class='logo-text machina-ypoema-text' style="{ypo_style}">{LOGO_TEXTO}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

def write_cia_header(LOGO_TEXTO, LOGO_IMAGE=None):
    """Renderiza o cabeçalho da CIA em duas linhas: descritivo + mood."""
    if LOGO_IMAGE is not None:
        write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
        return

    mood = st.session_state.get("cia_mood", "")
    mood_label = f"({mood})" if mood else ""
    stage_font = st.session_state.get("cia_font", "Trebuchet MS")
    stage_size = int(st.session_state.get("cia_size", 18))
    mood_size = max(13, int(stage_size * 0.82))

    st.markdown(
        f"""
        <div class='cia-header-container' style="text-align:center; width:100%; margin:0 auto 1.15em auto;">
            <p class='cia-header-text' style="font-family:{stage_font}; font-size:{stage_size}px; margin:0 0 0.12em 0; text-align:center; text-decoration:underline; text-underline-offset:0.18em;">{LOGO_TEXTO}</p>
            <p class='cia-header-mood' style="font-family:{stage_font}; font-size:{mood_size}px; margin:0; opacity:0.92; text-align:center; text-decoration:underline; text-underline-offset:0.18em;">{mood_label}</p>
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
    selected_voice = VOICES_EDGE_TTS.get(st.session_state.lang, "pt-BR-FranciscaNeural")

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

    if st.session_state.mini >= maxy_mini:  # just in case
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
    _restore_cia_freeze_before_sync()
    _sync_book_theme_state()
    temas_list = load_temas(_current_book())
    maxy_ypoemas = len(temas_list) - 1
    if (
        st.session_state.take > maxy_ypoemas or st.session_state.take < 0
    ):  # just in case
        st.session_state.take = 0

    try:
        col_livros, col_nav, col_temas = st.columns(
            [3, 4, 3],
            vertical_alignment="bottom",
        )
        machina_nav_needs_spacer = False
    except TypeError:
        col_livros, col_nav, col_temas = st.columns([3, 4, 3])
        machina_nav_needs_spacer = True

    with col_livros:
        pick_book_palco()

    with col_nav:
        help_tips = load_help(st.session_state.lang)
        help_last = help_tips[0]
        help_rand = help_tips[1]
        help_nest = help_tips[2]
        help_more = help_tips[4]

        if machina_nav_needs_spacer:
            st.markdown(
                "<div style='height:1.95rem; min-height:1.95rem;'></div>",
                unsafe_allow_html=True,
            )
        nav_cols = st.columns([1, 1, 1, 1, 1])
        more = nav_cols[0].button("✚", help=help_more, use_container_width=True)
        last = nav_cols[1].button("◀", help=help_last, use_container_width=True)
        rand = nav_cols[2].button("✻", help=help_rand, use_container_width=True)
        nest = nav_cols[3].button("▶", help=help_nest, use_container_width=True)
        manu_help = "guia do leitor da CIA" if st.session_state.get("sidebar_panel") == "CIA" else "help !!!"
        manu = nav_cols[4].button("?", help=manu_help, use_container_width=True)

    temas_list = load_temas(_current_book())
    maxy_ypoemas = len(temas_list) - 1
    if st.session_state.take > maxy_ypoemas or st.session_state.take < 0:
        st.session_state.take = 0

    # Âncora estável: usada pelo ✚ para evitar que qualquer callback de lista
    # troque tema antes da geração de "mais uma versão do mesmo tema".
    if not st.session_state.get("ypo_anchor_book"):
        st.session_state["ypo_anchor_book"] = _current_book()
        st.session_state["ypo_anchor_take"] = int(st.session_state.get("take", 0))
        st.session_state["ypo_anchor_tema"] = st.session_state.get("tema", "")

    if more:
        # ✚ = recarregar / mais uma versão do mesmo tema.
        # Usa a última âncora estável, não o eventual valor alterado por callback.
        frozen_book = st.session_state.get("ypo_anchor_book", _current_book())
        frozen_take = int(st.session_state.get("ypo_anchor_take", st.session_state.get("take", 0)))
        frozen_tema = st.session_state.get("ypo_anchor_tema", st.session_state.get("tema", ""))
        st.session_state["cia_last_action"] = "more_same_theme"
        st.session_state["more_same_book"] = frozen_book
        st.session_state["more_same_take"] = frozen_take
        st.session_state["more_same_tema"] = frozen_tema
        st.session_state.book = frozen_book
        st.session_state.take = frozen_take
        if frozen_tema:
            st.session_state.tema = frozen_tema
        # Não escrever em keys de widgets já instanciados pelo Streamlit.
        # O congelamento é feito no estado canônico: book/take/tema.

    if last:
        st.session_state["cia_last_action"] = "nav"
        limpar_cia_palco()
        limpar_copias_palco()
        st.session_state.take -= 1
        if st.session_state.take < 0:
            st.session_state.take = maxy_ypoemas
        _sync_book_theme_state()

    if rand:
        st.session_state["cia_last_action"] = "nav"
        limpar_cia_palco()
        limpar_copias_palco()
        st.session_state.take = random.randrange(0, maxy_ypoemas + 1)
        _sync_book_theme_state()

    if nest:
        st.session_state["cia_last_action"] = "nav"
        limpar_cia_palco()
        limpar_copias_palco()
        st.session_state.take += 1
        if st.session_state.take > maxy_ypoemas:
            st.session_state.take = 0
        _sync_book_theme_state()

    with col_temas:
        pick_tema_palco()

    temas_list = load_temas(_current_book())
    _sync_book_theme_state()

    if more and st.session_state.get("cia_last_action") == "more_same_theme":
        frozen_book = st.session_state.get("more_same_book", _current_book())
        frozen_take = int(st.session_state.get("more_same_take", st.session_state.get("take", 0)))
        frozen_tema = st.session_state.get("more_same_tema", "")
        st.session_state.book = frozen_book
        st.session_state.take = frozen_take
        if frozen_tema:
            st.session_state.tema = frozen_tema
        temas_list = load_temas(_current_book())
        maxy_ypoemas = len(temas_list) - 1
        if st.session_state.take > maxy_ypoemas or st.session_state.take < 0:
            st.session_state.take = 0
            st.session_state.tema = temas_list[0] if temas_list else ""

    lnew = True
    cia_mode_page = st.session_state.get("sidebar_panel") == "CIA"
    if manu:
        if cia_mode_page:
            st.markdown(guia_do_leitor_cia())
        else:
            render_help_ypoemas_mesma_fonte()

    if lnew:
        what_book = (
            "🌿  "
            + st.session_state.lang
            + " ( "
            + _current_book()
            + " ) ( "
            + str(st.session_state.take + 1)
            + " / "
            + str(len(temas_list))
            + " )"
        )

        ypoemas_expander = st.expander(what_book, expanded=True)
        with ypoemas_expander:
            cia_mode = st.session_state.get("sidebar_panel") == "CIA"
            cia_mood_changed = bool(st.session_state.get("cia_mood_changed", False))
            cia_force_new_poema = bool(st.session_state.get("cia_force_new_poema", False))
            cia_last_action = st.session_state.get("cia_last_action", "")

            explicit_poem_change = bool(
                last
                or rand
                or nest
                or cia_last_action in {"nav", "book_change", "theme_change"}
            )
            more_same_theme = bool(more or cia_last_action == "more_same_theme")

            if cia_mode and (cia_mood_changed or cia_last_action == "cia_mood"):
                _cia_restaurar_identidade_objeto()
                force_new_poema = False
            else:
                force_new_poema = bool(explicit_poem_change or cia_force_new_poema or more_same_theme)

            preserve_cia_poema = (
                cia_mode
                and _cia_objeto_analise_existe()
                and not force_new_poema
            )

            if preserve_cia_poema:
                # Troca de lente CIA: usa exatamente o mesmo objeto de análise.
                _cia_restaurar_identidade_objeto()
                curr_ypoema = st.session_state.get("ypoema_atual_para_analise", "")
                generated_new_poema = False
                st.session_state["cia_mood_changed"] = False
                st.session_state["cia_force_new_poema"] = False
                st.session_state["cia_freeze_book"] = ""
                st.session_state["cia_freeze_take"] = -1
                st.session_state["cia_freeze_tema"] = ""
                st.session_state["cia_last_action"] = ""
            else:
                st.session_state["cia_mood_changed"] = False
                st.session_state["cia_force_new_poema"] = False

                if cia_mode and more_same_theme and _cia_objeto_analise_existe():
                    _cia_restaurar_identidade_objeto()

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

                if cia_mode:
                    _cia_fixar_objeto_analise(curr_ypoema)
                else:
                    st.session_state.ypoema_em_analise = curr_ypoema
                    st.session_state.tema_em_analise = st.session_state.tema
                    st.session_state.book_em_analise = _current_book()
                    st.session_state.take_em_analise = st.session_state.take
                    st.session_state.lang_em_analise = st.session_state.lang

                generated_new_poema = True
                st.session_state["cia_last_action"] = ""
                st.session_state["more_same_book"] = ""
                st.session_state["more_same_take"] = -1
                st.session_state["more_same_tema"] = ""
                st.session_state["ypo_anchor_book"] = _current_book()
                st.session_state["ypo_anchor_take"] = int(st.session_state.get("take", 0))
                st.session_state["ypo_anchor_tema"] = st.session_state.get("tema", "")

            if generated_new_poema:
                update_readings(st.session_state.tema)

            LOGO_TEXTO = curr_ypoema
            LOGO_IMAGE = None

            if st.session_state.get("sidebar_panel") != "CIA" and st.session_state.draw:
                LOGO_IMAGE = load_arts(st.session_state.tema)

            if st.session_state.get("sidebar_panel") == "CIA":
                col_poema, col_cia = st.columns([5, 5])
                with col_poema:
                    write_ypoema_cia_palco(LOGO_TEXTO, None)
                with col_cia:
                    render_cia_stage(curr_ypoema)
            else:
                write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

            # Copiar 1..9 ocorrências do tema atual para leituras externas.
            # Mantém o yPoema exibido como #1 e gera variações extras sem alterar o palco.
            #
            # Importante: não usar st.number_input dentro de st.form aqui.
            # Na prática ele estava ficando preso no valor antigo/default (=1) em alguns ciclos,
            # e o hint nativo do input ainda poluía a tela. O selectbox 1..9 é estável e sem hint.
            copy_left, copy_qtd_col, copy_btn_col, copy_right = st.columns([7.3, 1.10, 0.85, 7.3])
            with copy_qtd_col:
                qtd_copias = st.selectbox(
                    "1 a 9",
                    list(range(1, 10)),
                    index=max(0, min(8, int(st.session_state.get("copy_qtd", 1)) - 1)),
                    key="copy_qtd_widget",
                    label_visibility="visible",
                )

            with copy_btn_col:
                st.markdown(
                    "<div style='height:1.72rem; min-height:1.72rem;'></div>",
                    unsafe_allow_html=True,
                )
                copy_submit = st.button("📋", key="copy_variacoes_btn", use_container_width=True)

            st.session_state["copy_qtd"] = int(qtd_copias)

            if copy_submit:
                qtd_copias = int(st.session_state.get("copy_qtd", 1))
                st.session_state["copy_bundle_text"] = montar_copias_ypoema(
                    curr_ypoema,
                    st.session_state.get("tema", ""),
                    qtd_copias,
                )
                st.session_state["copy_bundle_qtd"] = qtd_copias
                st.session_state["copy_bundle_source"] = _copy_bundle_source_key(curr_ypoema)
                st.session_state["copy_bundle_token"] = int(st.session_state.get("copy_bundle_token", 0)) + 1

            copy_bundle_text = st.session_state.get("copy_bundle_text", "")
            if st.session_state.get("copy_bundle_source", "") != _copy_bundle_source_key(curr_ypoema):
                copy_bundle_text = ""

            render_copy_bundle_widget(
                copy_bundle_text,
                int(st.session_state.get("copy_bundle_token", 0)),
                st.session_state.get("copy_bundle_qtd", None),
            )

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
        st.session_state.off_take = random.randrange(0, maxy_off_machina + 1)

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
                        if LOGO_CAPA:
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


SIDEBAR_FILHOTE_WIDTH_PX = 64
CIA_MOOD_OPTIONS = [
    "Sintática",
    "Sintética",
    "Formal",
    "Completa",
    "Index",
]
                    # Sem rerun manual: o clique do Streamlit já atualiza a página uma vez.
                    # Forçar st.rerun() aqui duplicava/triplicava recarregamentos.







def render_sidebar_for_page(chosen_id):
    """Renderiza os controles fixos do leitor."""
    pick_lang()
    pick_stage_font()
    draw_check_buttons()


configure_cia(
    translate_func=translate,
    load_typo_func=load_typo,
    write_ypoema_func=write_cia_header,
    ip_address=IPAddres,
    current_book_func=_current_book,
    say_number_func=say_number,
    render_sidebar_for_page_func=render_sidebar_for_page,
)

def main():
    gramado = open_gramado()

    with gramado:
        _pag_esq, _pag_centro, _pag_dir = st.columns([0.15, 9.7, 0.15])

        with _pag_centro:
            chosen_id = stx.tab_bar(
                data=[
                    stx.TabBarItemData(id=1, title="mini", description=""),
                    stx.TabBarItemData(id=2, title="yPoemas", description=""),
                    stx.TabBarItemData(id=3, title="eureka", description=""),
                    stx.TabBarItemData(id=4, title="off-Machina", description=""),
                    stx.TabBarItemData(id=5, title="about", description=""),
                ],
                default=2,
            )

        chosen_id = str(chosen_id)

        st.markdown("<div class='machina-divider-palco'><hr /></div>", unsafe_allow_html=True)

        magy = PAGE_IMAGES.get(chosen_id, "img_ypoemas.jpg")
        apply_sidebar_mae_filha_styles(chosen_id)

        if _cia_sidebar_filha_active(chosen_id):
            render_sidebar_filha()
        else:
            render_sidebar_for_page(chosen_id)

            if chosen_id == "2":
                draw_sidebar_panel_buttons(chosen_id)

                if st.session_state.get("sidebar_panel", "Machina") == "CIA":
                    st.session_state["cia_reading_mode"] = False
                    render_cia_mood_selectbox()
                else:
                    st.session_state["cia_reading_mode"] = False
                    st.session_state["cia_mood_select"] = st.session_state.get("cia_mood", "Sintática")

            with st.sidebar:
                cia_sidebar_publica = (
                    chosen_id == "2"
                    and st.session_state.get("sidebar_panel", "Machina") == "CIA"
                )
                if not cia_sidebar_publica:
                    st.image("./images/" + magy)


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
                    current_book = _current_book()
                    status = palco_status(
                        current_book,
                        st.session_state.get("take", 0) + 1,
                        len(load_temas(current_book)),
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
                    current_book = _current_book()
                    status = palco_status(
                        current_book,
                        st.session_state.get("take", 0) + 1,
                        len(load_temas(current_book)),
                    )

                st.markdown(
                    f"<div class='machina-rodape-palco'>{status}</div>",
                    unsafe_allow_html=True,
                )


if __name__ == "__main__":
    main()
