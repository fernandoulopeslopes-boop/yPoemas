import os
import re
import time
import random
import string
import base64
import html
import unicodedata
import socket
import asyncio
import streamlit as st
import streamlit.components.v1 as components

APP_BUILD = "2026-07-03_ypo_seguro_sidebar_FBF"
APP_BUILD_NOTES = "Versão pública: imagem contextual na sidebar; palco sem colunas; página pública About preservada; tools local fora do menu."

from lay_2_ypo import gera_poema
from readings import (
    list_readings,
    update_readings,
    update_visy,
)


ABOUTS_LIST = [
    "comentários",
    "prefácil",
    "machina",
    "off-machina",
    "outros autores",
    "livros",
    "bibliografia",
    "notes",
    "imagens",
    "pontuação",
    "poly",
    "tradittore",
    "pensares",
    "machina-IA",
    "samizdàt",
    "index",
    "license",
]

ABOUTS_FILES = {
    "comentários": ["ABOUT_comentários.md"],
    "prefácil": ["ABOUT_prefácil.md"],
    "machina": ["ABOUT_machina.md"],
    "off-machina": ["ABOUT_off-machina.md", "ABOUT_off_machina.md", "ABOUT_off machina.md"],
    "outros autores": ["ABOUT_outros_autores.md", "ABOUT_outros autores.md"],
    "livros": ["ABOUT_livros.md"],
    "bibliografia": ["ABOUT_bibliografia.md"],
    "notes": ["ABOUT_notes.md"],
    "imagens": ["ABOUT_imagens.md"],
    "pontuação": ["ABOUT_pontuação.md"],
    "poly": ["ABOUT_poly.md"],
    "tradittore": ["ABOUT_tradittore.md"],
    "pensares": ["ABOUT_pensares.md"],
    "machina-IA": ["ABOUT_machina-IA.md"],
    "samizdàt": ["ABOUT_samizdàt.md"],
    "index": ["ABOUT_index.MD", "ABOUT_index.md", "ABOUT_INDEX.md"],
    "license": ["ABOUT_license.md"],
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
    page_title="a Machina de fazer Poesia - Ꭹᕈᗢᗴᗰᗩᔕ",
    page_icon="snowflake",
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
            margin: 0 auto 0 auto;
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
            max-width: min(96ch, 94%) !important;
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
            gap: 0.28rem !important;
        }

        [data-testid="stSidebar"] div[data-testid="stElementContainer"] {
            margin-bottom: 0.02rem !important;
        }

        /* Sidebar :: módulo visual unificado — idioma e imagem com mesma largura */
        [data-testid="stSidebar"] div[data-testid="stSelectbox"] {
            max-width: 240px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        .machina-sidebar-image-frame {
            width: 240px !important;
            height: 330px !important;
            max-width: 100% !important;
            margin: calc(0.18rem + 20px) auto 0 auto !important;
            padding: 0 !important;
            overflow: hidden !important;
            border-radius: 8px !important;
            background: transparent !important;
            line-height: 0 !important;
            box-sizing: border-box !important;
        }

        .machina-sidebar-image-frame img {
            display: block !important;
            width: 100% !important;
            height: 100% !important;
            object-fit: cover !important;
            object-position: center center !important;
            margin: 0 !important;
            padding: 0 !important;
            border: 0 !important;
        }

        .machina-voz-slot {
            margin: 0.10rem auto 0.08rem auto !important;
            max-width: min(680px, 96%) !important;
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

        /* Celular :: leitura antes de painel */
        @media (max-width: 700px) {
            .main .block-container,
            section.main > div.block-container {
                padding-left: 0.18rem !important;
                padding-right: 0.18rem !important;
                max-width: 100vw !important;
            }

            .machina-gramado {
                border-radius: 12px !important;
                padding-left: 0.08rem !important;
                padding-right: 0.08rem !important;
                overflow-x: hidden !important;
            }

            .machina-palco-central {
                border-radius: 12px !important;
                padding-left: 0.04rem !important;
                padding-right: 0.04rem !important;
                overflow-x: hidden !important;
            }

            .container {
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                gap: 0.35rem !important;
            }

            .logo-img {
                float: none !important;
                display: block !important;
                max-width: 92vw !important;
                width: auto !important;
                height: auto !important;
                margin: 0.10rem auto 0.35rem auto !important;
                padding: 0 !important;
            }

            .logo-text,
            .machina-ypoema-text {
                width: 100% !important;
                max-width: 97vw !important;
                padding-left: 0.20rem !important;
                padding-right: 0.20rem !important;
                margin-left: auto !important;
                margin-right: auto !important;
                box-sizing: border-box !important;
                line-height: 1.34 !important;
            }

            .machina-ypoema-solo .machina-ypoema-text {
                max-width: 94vw !important;
            }

            .machina-palco-titulo {
                margin-top: 0.08rem !important;
                margin-bottom: 0 !important;
            }
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
        "copy_qtd": 2,
        "copy_qtd_widget": 2,
        "copy_bundle_text": "",
        "copy_bundle_token": 0,
        "copy_bundle_qtd": 0,
        "copy_bundle_source": "",
        "ypo_theme_widget_token": 0,
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


def _normalizar_qtd_copias(value):
    """Quantidade em lote: 2..9. Para +1, o botão ✚ já cumpre esse papel."""
    try:
        qtd = int(value)
    except Exception:
        qtd = 2
    return max(2, min(9, qtd))


def _on_copy_qtd_change():
    """Lista de quantidade como ação: um clique já escolhe e prepara o resultado."""
    st.session_state["copy_qtd"] = _normalizar_qtd_copias(
        st.session_state.get("copy_qtd_widget", st.session_state.get("copy_qtd", 2))
    )
    st.session_state["copy_qtd_changed"] = True


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
        _bump_palco_theme_widget()


def _current_book():
    """Retorna o livro atual sem depender de atributo já criado no session_state."""
    book = st.session_state.get("book", BOOKS_LIST[0])
    return book if book in BOOKS_LIST else BOOKS_LIST[0]


def _prepare_book_widget(key):
    """Faz o widget espelhar `book` sem tomar conta do estado."""
    current = _current_book()
    if key in st.session_state and st.session_state.get(key) != current:
        del st.session_state[key]


def _bump_palco_theme_widget():
    """Força recriação segura da lista de temas sem escrever na key do widget."""
    st.session_state["ypo_theme_widget_token"] = int(
        st.session_state.get("ypo_theme_widget_token", 0)
    ) + 1


def _theme_widget_key():
    return "opt_take_palco_" + str(int(st.session_state.get("ypo_theme_widget_token", 0)))


def _prepare_theme_widget():
    """Mantém lista de temas sincronizada sem escrever na key do selectbox."""
    return _theme_widget_key()


def _on_palco_book_change():
    current_book = _current_book()
    choice = st.session_state.get("palco_book_select", current_book)
    if choice != current_book:
        st.session_state.book = choice
        st.session_state.take = 0
        limpar_copias_palco()
        st.session_state["cia_force_new_poema"] = True
        _bump_palco_theme_widget()
    _sync_book_theme_state()


def _on_palco_theme_change():
    temas_list = load_temas(_current_book())
    if not temas_list:
        st.session_state.take = 0
        st.session_state.tema = ""
        return

    widget_key = st.session_state.get("_ypo_theme_widget_key", _theme_widget_key())
    take = _coerce_take(
        st.session_state.get(widget_key, st.session_state.get("take", 0)),
        temas_list,
    )

    old_take = st.session_state.get("take", 0)
    st.session_state.take = take
    st.session_state.tema = temas_list[take]
    if take != old_take:
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

    widget_key = _prepare_theme_widget()
    st.session_state["_ypo_theme_widget_key"] = widget_key
    options = list(range(len(temas_list)))
    st.selectbox(
        f"↓  {len(temas_list)} " + translate("temas"),
        options,
        index=_coerce_take(st.session_state.get("take", 0), temas_list),
        format_func=lambda z: temas_list[z],
        key=widget_key,
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

    corpos = list(range(14, 35, 2))
    current_size = st.session_state.get("stage_size", 22)
    if current_size not in corpos:
        current_size = 22

    # Mesmo eixo visual da lista de idiomas: duas listas nativas lado a lado.
    # A soma das duas ocupa a largura útil da sidebar; corpo fica largo o
    # suficiente para exibir dois dígitos sem esmagar o título.
    col_font, col_corpo = st.sidebar.columns([2.78, 1.32])

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
    """Voz saiu da sidebar: agora é ação ♫ nos botões do palco."""
    return


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


def _project_path(*parts):
    """Resolve caminho tanto pelo diretório de execução quanto pelo diretório do .py."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(os.getcwd(), *parts),
        os.path.join(here, *parts),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return candidates[0]


def _md_nome_chave(nome):
    """Normaliza nomes de md_files para comparação robusta.

    A regra é geral: caixa, acento, espaço, hífen, underscore e pontuação
    não devem impedir abrir ABOUT_<assunto>.md.
    """
    nome = os.path.basename(str(nome or '').strip())
    nome = os.path.splitext(nome)[0]
    nome = nome.casefold()
    nome = unicodedata.normalize('NFD', nome)
    nome = ''.join(ch for ch in nome if unicodedata.category(ch) != 'Mn')
    nome = re.sub(r'^about', '', nome)
    nome = re.sub(r'[^a-z0-9]+', '', nome)
    return nome


def _md_assunto_de_about(nome):
    """Extrai a chave do assunto, removendo o prefixo ABOUT quando existir."""
    return _md_nome_chave(nome)


def _md_file_casefold_path(file_name):
    """Localiza arquivo em md_files por equivalência geral de nome.

    Não exige lista de exceções e não obriga renomear arquivos.
    Ex.: ABOUT_off-machina.md, ABOUT_off_machina.md e ABOUT_OFF MACHINA.MD
    são tratados como o mesmo assunto.
    """
    expected_name = str(file_name or '').strip()
    if not expected_name:
        return ''

    md_dir = _project_path('md_files')
    direct = os.path.join(md_dir, expected_name)
    if os.path.exists(direct):
        return direct

    if not os.path.isdir(md_dir):
        return ''

    expected_base = os.path.basename(expected_name)
    expected_fold = expected_base.casefold()
    expected_key = _md_nome_chave(expected_base)

    # Para ABOUT_<assunto>.md, também aceita comparar só o assunto.
    expected_subject = expected_key

    best = ''
    for real_name in os.listdir(md_dir):
        real_path = os.path.join(md_dir, real_name)
        if not os.path.isfile(real_path):
            continue
        if not real_name.casefold().endswith('.md'):
            continue

        real_fold = real_name.casefold()
        real_key = _md_nome_chave(real_name)

        if real_fold == expected_fold:
            return real_path
        if real_key == expected_key:
            return real_path
        if expected_subject and real_key == expected_subject:
            return real_path

        # Fallback sem exceções: se um nome é abreviação clara do outro.
        # Ex.: ABOUT_outros.md pode atender ABOUT_outros_autores.md.
        if expected_key and real_key:
            if real_key.startswith(expected_key) or expected_key.startswith(real_key):
                best = best or real_path

    return best


def load_md_file(file):  # Open files for about's
    path = _md_file_casefold_path(file)
    try:
        with open(path, encoding='utf-8') as file_to_open:
            file_text = file_to_open.read()

        if not 'rol_' in str(file).lower():  # do not translate theme
            file_text = translate(file_text)
    except Exception:
        file_text = translate('ooops... arquivo ( ' + str(file) + ' ) não pode ser aberto.')
        st.session_state.lang = 'pt'

    return file_text


def render_help_ypoemas_mesma_fonte():
    """Renderiza o Help yPoemas em texto normal, sem estilo Markdown."""
    raw = load_md_file("MANUAL_YPOEMAS.md")

    linhas = []
    for raw_line in str(raw).splitlines():
        line = raw_line.rstrip()
        clean = line.strip()

        heading = re.match(r"^#{1,6}\s+(.+)$", clean)
        if heading:
            line = heading.group(1).strip()
        else:
            line = re.sub(r"^>\s?", "", line)
            line = line.replace("**", "")

        linhas.append(line)

    st.text("\n".join(linhas))


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
        os.path.join("./md_files/ABOUT_index.MD"),
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


def _off_machina_texto_limpo(texto):
    """Texto Off-Machina para leitura direta.

    Remove restos de HTML/renderização antiga antes de exibir.
    Importante: o livro_vivo pode chegar como HTML cru OU HTML escapado
    (&lt;div&gt;...). Por isso a limpeza desescapa antes de remover tags.
    """
    texto = str(texto or "")

    # Se o texto chegou escapado, transforma primeiro em HTML real;
    # repetir cobre casos duplamente escapados sem afetar texto normal.
    for _ in range(3):
        novo = html.unescape(texto)
        if novo == texto:
            break
        texto = novo

    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    texto = texto.replace("<br/>", "\n").replace("<br />", "\n").replace("<br>", "\n")

    # Descarta blocos que nunca devem aparecer como texto no palco.
    texto = re.sub(r"<script\b[^>]*>.*?</script>", "", texto, flags=re.IGNORECASE | re.DOTALL)
    texto = re.sub(r"<style\b[^>]*>.*?</style>", "", texto, flags=re.IGNORECASE | re.DOTALL)
    texto = re.sub(r"<img\b[^>]*>", "", texto, flags=re.IGNORECASE | re.DOTALL)

    # Remove qualquer atributo/data URI que tenha sobrado fora de uma tag fechada.
    texto = re.sub(r"data:image/[^;]+;base64,[A-Za-z0-9+/=\s]+", "", texto, flags=re.IGNORECASE)

    # Remove tags estruturais mantendo o conteúdo textual interno.
    texto = re.sub(r"</?(?:div|p|span)\b[^>]*>", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"<[^>]+>", "", texto)

    # Última desescapada para aspas e entidades textuais legítimas.
    texto = html.unescape(texto)
    return _trim_blank_edges_preservando_recuo(texto.splitlines())


def write_off_machina_texto(LOGO_TEXTO):
    """Renderiza Off-Machina normal como texto, sem imagem/base64 no palco."""
    texto = _off_machina_texto_limpo(LOGO_TEXTO)
    safe = html.escape(texto).replace("\n", "<br>")
    st.markdown(f"<p class='logo-text'>{safe}</p>", unsafe_allow_html=True)


def write_livro_vivo_texto(LOGO_TEXTO, LOGO_IMAGE=None):
    """Renderiza livro_vivo sem usar write_ypoema.

    O livro_vivo continua sendo gerado on demand pelo motor da Machina,
    mas não deve embrulhar a saída em HTML com imagem/base64. A imagem,
    quando existir, é exibida por st.image; o texto é renderizado limpo.
    """
    texto = _off_machina_texto_limpo(LOGO_TEXTO)

    if LOGO_IMAGE:
        try:
            col_img, col_txt = st.columns([2.5, 7.5])
            with col_img:
                st.image(LOGO_IMAGE, use_container_width=True)
            with col_txt:
                safe = html.escape(texto).replace("\n", "<br>")
                st.markdown(f"<p class='logo-text'>{safe}</p>", unsafe_allow_html=True)
            return
        except Exception:
            # Se a arte falhar, o texto ainda deve aparecer limpo.
            pass

    safe = html.escape(texto).replace("\n", "<br>")
    st.markdown(f"<p class='logo-text'>{safe}</p>", unsafe_allow_html=True)


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
    """Monta 2..9 cópias/variações para leitura externa, em desenho clean."""
    qtd = _normalizar_qtd_copias(qtd)

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


def _copy_bundle_total_blocos(texto, qtd_real=None):
    """Calcula quantidade real de blocos/yPoemas no pacote de cópias."""
    try:
        total_blocos = int(qtd_real) if qtd_real is not None else 0
    except Exception:
        total_blocos = 0

    if total_blocos < 1:
        marcadores = len(re.findall(r"(?m)^___\s*$", str(texto or "")))
        total_blocos = marcadores - 1 if str(texto or "").strip().endswith("___") and marcadores > 1 else marcadores
        total_blocos = max(1, total_blocos)

    return total_blocos


def render_copy_bundle_button(texto, token):
    """Botão HTML/JS: copia de verdade e troca o próprio texto para 'copiado'."""
    import json

    texto = str(texto or "")
    js_text = json.dumps(texto, ensure_ascii=False)

    components.html(
        f"""
        <div style="font-family:system-ui, sans-serif; padding:0; margin-top:-5px;">
            <button id="copy_btn_{token}" style="
                width:100%;
                min-height:38px;
                border:1px solid rgba(49,51,63,.22);
                border-radius:8px;
                padding:7px 12px;
                cursor:pointer;
                background:white;
                color:rgb(49,51,63);
                font-size:14px;
                line-height:1.2;
                white-space:nowrap;">
                copiar...
            </button>
        </div>
        <script>
        const txt_{token} = {js_text};
        const btn_{token} = document.getElementById("copy_btn_{token}");

        async function fallbackCopy_{token}(text) {{
            const ta = document.createElement("textarea");
            ta.value = text;
            ta.setAttribute("readonly", "");
            ta.style.position = "fixed";
            ta.style.left = "-9999px";
            ta.style.top = "0";
            document.body.appendChild(ta);
            ta.focus();
            ta.select();
            const ok = document.execCommand("copy");
            document.body.removeChild(ta);
            return ok;
        }}

        if (btn_{token}) {{
            btn_{token}.addEventListener("click", async function() {{
                try {{
                    if (navigator.clipboard && window.isSecureContext) {{
                        await navigator.clipboard.writeText(txt_{token});
                    }} else {{
                        const ok = await fallbackCopy_{token}(txt_{token});
                        if (!ok) throw new Error("fallback copy failed");
                    }}
                    btn_{token}.innerText = "copiado";
                }} catch (e) {{
                    try {{
                        const ok = await fallbackCopy_{token}(txt_{token});
                        btn_{token}.innerText = ok ? "copiado" : "copiar...";
                    }} catch (e2) {{
                        btn_{token}.innerText = "copiar...";
                    }}
                }}
            }});
        }}
        </script>
        """,
        height=48,
    )


def render_copy_bundle_widget(texto, token, qtd_real=None):
    """Mostra o pacote completo para conferência e fallback de cópia."""
    if not texto:
        return

    texto = str(texto)
    total_blocos = _copy_bundle_total_blocos(texto, qtd_real)

    tema_label = str(st.session_state.get("tema", "") or "").strip()

    pacote_label = f'pacote para copiar ({total_blocos}) ("{tema_label}")'
    st.markdown(
        f"<div style='text-align:center; margin:0.10rem 0 0.36rem 0;'>{html.escape(pacote_label)}</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    st.text_area(
        pacote_label,
        value=texto,
        height=420,
        key=f"copy_bundle_textarea_{token}",
        label_visibility="collapsed",
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


def _set_sidebar_context_image_for_theme(nome_tema):
    """Define a imagem Machina contextual do tema atual para a sidebar.

    A curadoria existente continua valendo: tema == grupo de imagens.
    O destino visual muda: a imagem acompanha na sidebar, não no palco.
    """
    logo = load_arts(nome_tema)
    st.session_state["sidebar_context_image"] = logo or ""
    return logo or ""


def _resolve_off_machina_book_image(book_name):
    """Localiza imagem contextual do livro Off-Machina, sem imagem decorativa de página."""
    book_name = str(book_name or "").strip()
    if not book_name:
        return ""

    candidates = [
        os.path.join("./off-machina", "capa_" + book_name + ".jpg"),
        os.path.join("./off_machina", "capa_" + book_name + ".jpg"),
        os.path.join("./off-machina", book_name + ".jpg"),
        os.path.join("./off_machina", book_name + ".jpg"),
        os.path.join("./images/off_machina", "capa_" + book_name + ".jpg"),
        os.path.join("./images/off-machina", "capa_" + book_name + ".jpg"),
        os.path.join("./images/off_machina", book_name + ".jpg"),
        os.path.join("./images/off-machina", book_name + ".jpg"),
        os.path.join("./images/off", book_name + ".jpg"),
        os.path.join("./images/livros", book_name + ".jpg"),
        os.path.join("./images/books", book_name + ".jpg"),
        os.path.join("./images", book_name + ".jpg"),
    ]

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    return ""


def _about_author_images():
    """Lista imagens de autores disponíveis para a página About."""
    author_dir = "./images/author"
    author_images = []
    if os.path.isdir(author_dir):
        for file in sorted(os.listdir(author_dir)):
            low = file.lower()
            if low.endswith((".jpg", ".jpeg", ".png", ".webp")):
                author_images.append(os.path.join(author_dir, file))
    return author_images


def _set_about_author_image_next():
    """Homenageia um autor diferente a cada entrada/click na página About."""
    author_images = _about_author_images()
    if not author_images:
        st.session_state["about_author_image"] = ""
        return ""

    previous = st.session_state.get("about_author_image", "")
    available = [img for img in author_images if img != previous]
    chosen = random.choice(available or author_images)
    st.session_state["about_author_image"] = chosen
    return chosen


def render_sidebar_image_fit(image_path):
    """Renderiza imagem contextual da sidebar em quadro fixo 240x360, sem faixa branca."""
    if not image_path or not os.path.exists(image_path):
        return

    with open(image_path, "rb") as img_file:
        img_b64 = base64.b64encode(img_file.read()).decode()

    ext = os.path.splitext(image_path)[1].lower().replace(".", "")
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext or "jpeg"

    with st.sidebar:
        st.markdown(
            f"""
            <div class="machina-sidebar-image-frame">
                <img src="data:image/{mime};base64,{img_b64}" />
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_sidebar_context_image(chosen_id):
    """Renderiza a imagem contextual adequada na sidebar.

    - páginas que geram yPoemas: imagem Machina do tema em foco;
    - Off-Machina: imagem do livro em foco;
    - About: 1 autor homenageado por sessão.
    """
    image_path = ""

    if str(chosen_id) in {"1", "2", "3"}:
        image_path = st.session_state.get("sidebar_context_image", "")
    elif str(chosen_id) == "4":
        try:
            off_books_list = load_all_offs()
            off_idx = int(st.session_state.get("off_book", 0))
            if off_books_list and 0 <= off_idx < len(off_books_list):
                image_path = _resolve_off_machina_book_image(off_books_list[off_idx])
        except Exception:
            image_path = ""
    elif str(chosen_id) == "5":
        image_path = ""

    if image_path and os.path.exists(image_path):
        render_sidebar_image_fit(image_path)


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
    corpo_partes = partes[1:]
    while corpo_partes and not corpo_partes[0].strip():
        corpo_partes.pop(0)

    corpo = marcador.join(corpo_partes).strip()
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
    return max(14, min(34, corpo))


def _corpo_palco_cia():
    """Corpo protegido para palcos auxiliares legados."""
    return int(st.session_state.get("cia_palco_size", st.session_state.get("cia_size", 18)))


def write_ypoema_cia_palco(LOGO_TEXTO, LOGO_IMAGE=None):
    """Renderiza o yPoema em palco auxiliar legado."""
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

    logo_css = f"""
        <style>
        .logo-text {{
            font-weight: 600 !important;
            font-size: {stage_size}px !important;
            font-family: '{stage_font}' !important;
            color: #000000 !important;
            line-height: 1.35 !important;
            padding-top: 0px !important;
            padding-left: 8px !important;
            text-align: left !important;
            display: table !important;
            max-width: min(96ch, 94%) !important;
            margin-left: auto !important;
            margin-right: auto !important;
            box-sizing: border-box !important;
        }}
        </style>
    """

    if LOGO_IMAGE is None:
        st.markdown(
            f"{logo_css}<p class='logo-text'>{LOGO_TEXTO}</p>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            {logo_css}
            <div class='container'>
                <img class='logo-img' src='data:image/jpg;base64,{base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()}'>
                <p class='logo-text'>{LOGO_TEXTO}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

def write_cia_header(LOGO_TEXTO, LOGO_IMAGE=None):
    """Renderiza cabeçalho auxiliar legado em duas linhas."""
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


def render_voz_slot():
    """Reserva a linha do player de voz logo abaixo dos nav_buttons."""
    st.markdown("<div class='machina-voz-slot'>", unsafe_allow_html=True)
    slot = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)
    return slot

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

    foo1, more, rand, auto, voz_col, foo2 = st.columns([3.1, 1, 1, 1.9, 1, 3.1])

    help_tips = load_help(st.session_state.lang)
    help_rand = help_tips[1]
    help_more = help_tips[4]
    help_talk = help_tips[6]
    rand = rand.button("✻", help=help_rand)

    with auto:
        if st.button("auto", key="mini_auto_button", help="modo automático", use_container_width=True):
            st.session_state.auto = not st.session_state.auto

    with voz_col:
        if st.button("♫", key="mini_voz_btn", help=help_talk, use_container_width=True):
            st.session_state.talk = not st.session_state.talk

    mini_voz_slot = render_voz_slot()

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
        _set_sidebar_context_image_for_theme(st.session_state.tema)

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
                    write_ypoema(LOGO_TEXTO, None)

                if st.session_state.talk:
                    with mini_voz_slot:
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
                    _set_sidebar_context_image_for_theme(st.session_state.tema)

                    with mini_place_holder:
                        mini_place_holder.empty()
                        write_ypoema(LOGO_TEXTO, None)
                        secs = wait_time
                        while secs >= 0:
                            time.sleep(1)
                            secs -= 1


def page_ypoemas():
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
        nav_cols = st.columns([1, 1, 1, 1, 1, 1])
        more = nav_cols[0].button("✚", help=help_more, use_container_width=True)
        last = nav_cols[1].button("◀", help=help_last, use_container_width=True)
        rand = nav_cols[2].button("✻", help=help_rand, use_container_width=True)
        nest = nav_cols[3].button("▶", help=help_nest, use_container_width=True)
        if nav_cols[4].button("♫", help=help_tips[6], key="ypoemas_voz_btn", use_container_width=True):
            st.session_state.talk = not st.session_state.talk
        manu = nav_cols[5].button("?", help="help !!!", use_container_width=True)

        ypoemas_voz_slot = render_voz_slot()

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
        limpar_copias_palco()
        st.session_state.take -= 1
        if st.session_state.take < 0:
            st.session_state.take = maxy_ypoemas
        _sync_book_theme_state()
        _bump_palco_theme_widget()

    if rand:
        limpar_copias_palco()
        st.session_state.take = random.randrange(0, maxy_ypoemas + 1)
        _sync_book_theme_state()
        _bump_palco_theme_widget()

    if nest:
        limpar_copias_palco()
        st.session_state.take += 1
        if st.session_state.take > maxy_ypoemas:
            st.session_state.take = 0
        _sync_book_theme_state()
        _bump_palco_theme_widget()

    with col_temas:
        pick_tema_palco()

    temas_list = load_temas(_current_book())
    _sync_book_theme_state()

    if more:
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
    if manu:
        render_help_ypoemas_mesma_fonte()
        lnew = False

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

            st.session_state.ypoema_em_analise = curr_ypoema
            st.session_state.tema_em_analise = st.session_state.tema
            st.session_state.book_em_analise = _current_book()
            st.session_state.take_em_analise = st.session_state.take
            st.session_state.lang_em_analise = st.session_state.lang

            st.session_state["more_same_book"] = ""
            st.session_state["more_same_take"] = -1
            st.session_state["more_same_tema"] = ""
            st.session_state["ypo_anchor_book"] = _current_book()
            st.session_state["ypo_anchor_take"] = int(st.session_state.get("take", 0))
            st.session_state["ypo_anchor_tema"] = st.session_state.get("tema", "")

            LOGO_TEXTO = curr_ypoema
            _set_sidebar_context_image_for_theme(st.session_state.tema)

            write_ypoema(LOGO_TEXTO, None)

            # Copiar 2..9 ocorrências do tema atual para leituras externas.
            # Para apenas +1 variação, o botão ✚ já cumpre esse papel.
            # Mantém o yPoema exibido como #1 e gera variações extras sem alterar o palco.
            copy_bundle_text = st.session_state.get("copy_bundle_text", "")
            if st.session_state.get("copy_bundle_source", "") != _copy_bundle_source_key(curr_ypoema):
                copy_bundle_text = ""

            st.markdown("<br>", unsafe_allow_html=True)

            qtd_copias_atual = _normalizar_qtd_copias(
                st.session_state.get("copy_qtd_widget", st.session_state.get("copy_qtd", 2))
            )
            st.session_state["copy_qtd"] = qtd_copias_atual

            # Cópias clean:
            # [ criar (X) variações ] [ qtd ] [ copiar yPoemas gerados ]
            copy_left, copy_generate_col, copy_qtd_col, copy_all_col, copy_right = st.columns([3.00, 3.35, 2.10, 3.30, 3.00])

            with copy_generate_col:
                copy_submit = st.button(
                    f"criar ( {qtd_copias_atual} ) variações",
                    key="copy_variacoes_btn",
                    use_container_width=True,
                )

            with copy_qtd_col:
                qtd_copias = st.selectbox(
                    "quantidade de cópias",
                    list(range(2, 10)),
                    index=list(range(2, 10)).index(qtd_copias_atual),
                    key="copy_qtd_widget",
                    label_visibility="collapsed",
                    on_change=_on_copy_qtd_change,
                )

            qtd_copias = _normalizar_qtd_copias(qtd_copias)
            st.session_state["copy_qtd"] = qtd_copias

            copy_qtd_changed = bool(st.session_state.pop("copy_qtd_changed", False))
            copy_submit = bool(copy_submit or copy_qtd_changed)

            if copy_submit:
                qtd_copias = _normalizar_qtd_copias(st.session_state.get("copy_qtd", 2))
                st.session_state["copy_bundle_text"] = montar_copias_ypoema(
                    curr_ypoema,
                    st.session_state.get("tema", ""),
                    qtd_copias,
                )
                st.session_state["copy_bundle_qtd"] = qtd_copias
                st.session_state["copy_bundle_source"] = _copy_bundle_source_key(curr_ypoema)
                st.session_state["copy_bundle_token"] = int(st.session_state.get("copy_bundle_token", 0)) + 1
                copy_bundle_text = st.session_state.get("copy_bundle_text", "")

            # O botão "copiar..." só aparece quando há pacote real na área de cópias.
            # Novo tema ou nova geração recriam o token e o texto volta para "copiar...".
            with copy_all_col:
                if copy_bundle_text:
                    render_copy_bundle_button(
                        copy_bundle_text,
                        int(st.session_state.get("copy_bundle_token", 0)),
                    )

            render_copy_bundle_widget(
                copy_bundle_text,
                int(st.session_state.get("copy_bundle_token", 0)),
                st.session_state.get("copy_bundle_qtd", None),
            )

            if manu:
                LOGO_TEXTO = load_info(st.session_state.tema)
                if st.session_state.lang != "pt":  # translate if idioma <> pt
                    LOGO_TEXTO = translate(LOGO_TEXTO)

                _set_sidebar_context_image_for_theme(st.session_state.tema)
                write_ypoema(LOGO_TEXTO, None)

        if st.session_state.talk:
            with ypoemas_voz_slot:
                talk(curr_ypoema)


def page_eureka():
    help_tips = load_help(st.session_state.lang)
    help_rand = help_tips[1]
    help_more = help_tips[4]
    help_talk = help_tips[6]

    seed, more, rand, voz_col, manu, occurrences = st.columns([2.5, 1.3, 1.3, 0.8, 0.7, 3.9])

    with seed:
        find_what = st.text_input(
            label=translate("buscar por..."),
            help=translate("digite uma palavra - ou parte dela - que você goste..."),
        )

    with more:
        more = more.button("✚", help=help_more)

    with rand:
        rand = rand.button("✻", help=help_rand)

    with voz_col:
        if st.button("♫", key="eureka_voz_btn", help=help_talk, use_container_width=True):
            st.session_state.talk = not st.session_state.talk

    with manu:
        manu = manu.button("?", help="help !!!")

    eureka_voz_slot = render_voz_slot()

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
                    _set_sidebar_context_image_for_theme(seed_tema)

                    write_ypoema(LOGO_TEXTO, None)
                    update_readings(seed_tema)

                if st.session_state.talk:
                    with eureka_voz_slot:
                        talk(curr_ypoema)
            if manu:
                lnew = False
                LOGO_TEXTO = load_info(seed_tema)
                if st.session_state.lang != "pt":  # translate if idioma <> pt
                    LOGO_TEXTO = translate(LOGO_TEXTO)

                _set_sidebar_context_image_for_theme(seed_tema)
                write_ypoema(LOGO_TEXTO, None)

        else:
            st.warning(
                translate(
                    "nenhum verbete encontrado com essas letras ---> " + find_what
                )
            )


def page_off_machina():  # available off_machina_books
    nav_changed = False
    off_books_list = load_all_offs()
    if not off_books_list:
        st.warning(translate("nenhum livro off-machina encontrado"))
        return

    if st.session_state.off_book < 0 or st.session_state.off_book >= len(off_books_list):
        st.session_state.off_book = 0
    if st.session_state.off_take < 0:
        st.session_state.off_take = 0

    # Header limpo, herdado do palco yPoemas:
    # [ lista_livros ] [ ◀ ✻ ▶ ? ] [ lista_temas ]
    try:
        col_livros, col_nav, col_temas = st.columns(
            [3, 4, 3],
            vertical_alignment="bottom",
        )
        off_nav_needs_spacer = False
    except TypeError:
        col_livros, col_nav, col_temas = st.columns([3, 4, 3])
        off_nav_needs_spacer = True

    with col_livros:
        options = list(range(len(off_books_list)))
        sobrios = "↓  " + str(len(off_books_list)) + " livros"
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
        st.session_state["off_take_widget_token"] = int(
            st.session_state.get("off_take_widget_token", 0)
        ) + 1

    off_book_name = off_books_list[st.session_state.off_book]
    this_off_book = load_off_book(off_book_name)
    off_book_pagys = load_book_pages(this_off_book)

    if not off_book_pagys:
        st.warning(translate("nenhum título encontrado para este livro"))
        return

    maxy_off_machina = len(off_book_pagys) - 1
    if st.session_state.off_take > maxy_off_machina:
        st.session_state.off_take = 0

    with col_nav:
        help_tips = load_help(st.session_state.lang)
        help_last = help_tips[0]
        help_rand = help_tips[1]
        help_nest = help_tips[2]

        if off_nav_needs_spacer:
            st.markdown(
                "<div style='height:1.95rem; min-height:1.95rem;'></div>",
                unsafe_allow_html=True,
            )
        nav_cols = st.columns([1, 1, 1, 1, 1])
        last = nav_cols[0].button("◀", help=help_last, use_container_width=True)
        rand = nav_cols[1].button("✻", help=help_rand, use_container_width=True)
        nest = nav_cols[2].button("▶", help=help_nest, use_container_width=True)
        if nav_cols[3].button("♫", help=help_tips[6], key="off_voz_btn", use_container_width=True):
            st.session_state.talk = not st.session_state.talk
        manu = nav_cols[4].button("?", help="help !!!", use_container_width=True)

        off_voz_slot = render_voz_slot()

    if last:
        nav_changed = True
        st.session_state.off_take -= 1
        if st.session_state.off_take < 0:
            st.session_state.off_take = maxy_off_machina

    if rand:
        nav_changed = True
        st.session_state.off_take = random.randrange(0, maxy_off_machina + 1)

    if nest:
        nav_changed = True
        st.session_state.off_take += 1
        if st.session_state.off_take > maxy_off_machina:
            st.session_state.off_take = 0

    if st.session_state.off_take > maxy_off_machina:  # just in case...
        st.session_state.off_take = 0

    # Mantém a lista_temas sincronizada com os botões ◀ ✻ ▶,
    # sem escrever diretamente na key interna do widget.
    if nav_changed:
        st.session_state["off_take_widget_token"] = int(
            st.session_state.get("off_take_widget_token", 0)
        ) + 1

    with col_temas:
        options = list(range(len(off_book_pagys)))
        sobrios = "↓ " + str(len(off_book_pagys)) + " temas"
        opt_off_take_key = "opt_off_take_" + str(
            int(st.session_state.get("off_take_widget_token", 0))
        )
        opt_off_take = st.selectbox(
            sobrios,
            options,
            index=st.session_state.off_take,
            format_func=lambda x: off_book_pagys[x],
            key=opt_off_take_key,
        )

    if opt_off_take != st.session_state.off_take:
        st.session_state.off_take = opt_off_take

    lnew = True
    if manu:
        lnew = False
        st.subheader(load_md_file("MANUAL_OFF-MACHINA.md"))

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
            if off_book_name == "livro_vivo" and "@ " in pipe_line[1]:
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
                            st.image(LOGO_CAPA, use_container_width=True)
                    else:
                        st.image(
                            "./off_machina/capa_" + off_book_name + ".jpg",
                            use_container_width=True,
                        )
                with isbn:
                    if off_book_name == "livro_vivo":
                        write_off_machina_texto(off_book_text)
                    else:
                        st.markdown(
                            off_book_text, unsafe_allow_html=True
                        )  # finally... write it
            else:
                if st.session_state.lang != "pt":
                    off_book_text = translate(off_book_text)

                LOGO_TEXTO = off_book_text

                if off_book_name == "livro_vivo":
                    LOGO_IMAGE = load_arts(off_book_name)
                    write_livro_vivo_texto(LOGO_TEXTO, LOGO_IMAGE)
                else:
                    write_off_machina_texto(LOGO_TEXTO)
                update_readings(off_book_name)

        if st.session_state.talk:
            with off_voz_slot:
                talk(off_book_text)


def _about_candidates(title):
    """Gera nomes esperados para ABOUT_<assunto>.md sem lista infinita de exceções."""
    title = str(title or "").strip()
    candidates = list(ABOUTS_FILES.get(title, []))

    stems = [
        title,
        title.replace(" ", "_"),
        title.replace(" ", "-"),
        title.replace("-", "_"),
        title.replace("_", "-"),
    ]

    for stem in stems:
        name = "ABOUT_" + stem + ".md"
        if name not in candidates:
            candidates.append(name)

    return candidates


def load_about_md(title):
    """Carrega ABOUT pelo padrão geral: ABOUT_ + assunto.

    Procura o nome esperado e depois varre md_files comparando o assunto
    normalizado. Funciona para caixa, acentos, espaço, hífen e underscore.
    """
    title = str(title or "").strip()
    candidates = _about_candidates(title)

    for file_name in candidates:
        path = _md_file_casefold_path(file_name)
        if path:
            return load_md_file(os.path.basename(path))

    md_dir = "./md_files"
    wanted_key = _md_nome_chave(title)
    if os.path.isdir(md_dir):
        best = ""
        for real_name in os.listdir(md_dir):
            real_path = os.path.join(md_dir, real_name)
            if not os.path.isfile(real_path):
                continue
            if not real_name.lower().endswith(".md"):
                continue

            real_key = _md_nome_chave(real_name)
            if real_key == wanted_key:
                return load_md_file(real_name)

            if wanted_key and real_key:
                if real_key.startswith(wanted_key) or wanted_key.startswith(real_key):
                    best = best or real_name

        if best:
            return load_md_file(best)

    expected = "ABOUT_" + title + ".md"
    return translate("ooops... arquivo ( " + expected + " ) não pode ser aberto.")


def page_abouts():
    abouts_list = ABOUTS_LIST

    # About homenageia um autor diferente a cada entrada/click.
    _set_about_author_image_next()

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
            st.subheader(load_md_file("ABOUT_machina.md"))
            LOGO_TEXTO = load_info(st.session_state.tema)
            write_ypoema(LOGO_TEXTO, None)
#            st.subheader(load_md_file("ABOUT_machina II.md"))
        else:
            st.subheader(load_about_md(choice))


# -----------------------------------------------------------------------------
# Tools locais da Machina
# -----------------------------------------------------------------------------
# Cópia privada/local. Não vai para GitHub, deploy ou público.
# Regra: lê temas .YPO/.ypo; não altera conteúdo autoral; não cria poesia.

BUILD_INDEXY_FILE = "ABOUT_index.MD"
BUILD_AMBIENTE_LEXICO = "--- Ambiente Léxico da Machina"
BUILD_ESCALA = [
    "mil", "milhões", "bilhões", "trilhões", "quatrilhões", "quintilhões",
    "sextilhões", "setilhões", "octilhões", "nonilhões", "decilhões",
    "undecilhões", "dodecilhões", "tredecilhões", "quatuordecilhões",
    "quindecilhões", "sedecilhões", "septendecilhões",
]

def _tools_fmt_int(valor):
    return f"{int(valor):,}".replace(",", ".")


def _tools_potencia_nome(valor):
    num = f"{int(valor):,}"
    pontos = num.count(",") - 1
    if 0 <= pontos < len(BUILD_ESCALA):
        return BUILD_ESCALA[pontos]
    return "nonono"


def _tools_backup_path(path):
    """Cria backup local antes de qualquer gravação derivada/cadastral."""
    if not os.path.exists(path):
        return ""
    backup_dir = _project_path("backups", "local_tools")
    os.makedirs(backup_dir, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    base = os.path.basename(path)
    dst = os.path.join(backup_dir, f"{stamp}_{base}")
    with open(path, "rb") as src, open(dst, "wb") as out:
        out.write(src.read())
    return dst


def _tools_write_text(path, texto):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    _tools_backup_path(path)
    with open(path, "w", encoding="utf-8") as file:
        file.write(texto)


def _tools_add_unique_line(path, line, key):
    """Adiciona linha se a chave ainda não existir. Preserva o arquivo fora disso."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    line = str(line).rstrip("\n")
    key = str(key).casefold().strip()
    linhas = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as file:
            linhas = file.read().splitlines()

    for raw in linhas:
        parte = raw.partition(" : ")[0].strip().casefold()
        if not parte and raw.startswith("|"):
            campos = raw.split("|")
            if len(campos) > 1:
                parte = campos[1].strip().casefold()
        if parte == key or raw.strip().casefold() == key:
            return False

    _tools_backup_path(path)
    with open(path, "a", encoding="utf-8") as file:
        if linhas and linhas[-1] != "":
            file.write("\n")
        file.write(line + "\n")
    return True


def _tools_resolve_ypo_path(tema):
    tema = str(tema or "").strip()
    candidatos = [
        _project_path("data", tema + ".ypo"),
        _project_path("data", tema + ".YPO"),
    ]
    for path in candidatos:
        if os.path.exists(path):
            return path
    return candidatos[0]


def _tools_temas_ativos():
    temas = []
    ativos_path = _project_path("base", "ativos.txt")
    with open(ativos_path, encoding="utf-8") as file:
        for raw in file:
            linha = raw.strip("\n")
            if not linha.strip():
                continue
            tema = linha.partition(" : ")[0].strip()
            if tema:
                temas.append((tema, _tools_resolve_ypo_path(tema)))
    return temas


def _tools_temas_para_remover():
    """Lista temas em circulação, usando as mesmas listas vistas pelos yPoemas.

    A remoção precisa enxergar temas que aparecem em rol_*.txt mesmo que
    alguma lista cadastral esteja desencontrada.
    """
    nomes = []

    def add(nome):
        nome = str(nome or "").strip()
        if nome and nome not in nomes:
            nomes.append(nome)

    # 1) Lista canônica usada pelo livro "todos os temas" no palco.
    try:
        for nome in load_temas("todos os temas"):
            add(nome)
    except Exception:
        pass

    # 2) Todos os rol_*.txt, para capturar livros específicos.
    base_dir = _project_path("base")
    if os.path.isdir(base_dir):
        for file_name in sorted(os.listdir(base_dir)):
            if not (file_name.lower().startswith("rol_") and file_name.lower().endswith(".txt")):
                continue
            try:
                with open(os.path.join(base_dir, file_name), encoding="utf-8") as file:
                    for raw in file:
                        add(raw.replace(" ", "").strip())
            except Exception:
                pass

    # 3) Ativos, caso algum tema esteja cadastrado mas fora dos livros.
    try:
        for tema, path in _tools_temas_ativos():
            add(tema)
    except Exception:
        pass

    # 4) Arquivos em ./data, para permitir remover clone recém-criado mesmo
    #    quando as listas ficaram desencontradas.
    data_dir = _project_path("data")
    if os.path.isdir(data_dir):
        for file_name in sorted(os.listdir(data_dir), key=natural_keys):
            if file_name.lower().endswith(".ypo"):
                add(os.path.splitext(file_name)[0])

    return sorted(nomes, key=natural_keys)


def _tools_linhas_ypo(path):
    """Lê linhas estruturais do .YPO em UTF-8 estrito, informando arquivo se falhar."""
    try:
        with open(path, encoding="utf-8") as file:
            for line in file:
                if line.startswith("|"):
                    yield line.rstrip("\n").split("|")
    except UnicodeDecodeError as exc:
        raise UnicodeDecodeError(
            exc.encoding,
            exc.object,
            exc.start,
            exc.end,
            f"{exc.reason} em {path}"
        ) from exc


def build_tools_utf8_temas():
    """Verifica UTF-8 em base/ativos.txt e em todos os temas ativos, sem alterar arquivos."""
    start_time = time.time()
    problemas = []
    verificados = 0

    ativos_path = _project_path("base", "ativos.txt")
    try:
        with open(ativos_path, encoding="utf-8") as file:
            ativos_linhas = file.read().splitlines()
    except UnicodeDecodeError as exc:
        return (
            "UTF-8 temas: falha em ./base/ativos.txt\n"
            f"arquivo: {ativos_path}\n"
            f"posição: {exc.start}\n"
            f"erro: {exc}"
        )

    for raw in ativos_linhas:
        linha = raw.strip()
        if not linha:
            continue
        tema = linha.partition(" : ")[0].strip()
        if not tema:
            continue
        path = _tools_resolve_ypo_path(tema)
        if not os.path.exists(path):
            problemas.append(f"não encontrado: {path}")
            continue
        try:
            with open(path, encoding="utf-8") as file:
                file.read()
            verificados += 1
        except UnicodeDecodeError as exc:
            problemas.append(
                f"UTF-8 inválido: {path} | posição {exc.start} | {exc}"
            )

    if problemas:
        return (
            f"UTF-8 temas: {len(problemas)} problema(s) encontrado(s).\n"
            + "\n".join(problemas)
            + f"\nRuntime: {time.time() - start_time:.2f}s"
        )

    return f"UTF-8 temas: OK. {verificados} tema(s) ativo(s) verificado(s). Runtime: {time.time() - start_time:.2f}s"


def _tools_payload_itimos(campos):
    if len(campos) <= 8:
        return []
    return [item for item in campos[7:-1] if item != ""]


def _tools_normaliza_unico(texto):
    return re.sub(r"\s+", " ", str(texto or "").strip().casefold())


def _tools_palavras_de_itimo(itimo):
    palavras = []
    for word in str(itimo or "").split():
        if "-" not in word:
            for c in string.punctuation:
                word = word.replace(c, "")
        word = word.strip().casefold()
        if len(word) >= 3:
            palavras.append(word)
    return palavras


def _tools_calcular_variacoes_tema(path):
    fontes_list = []
    corrige_qtd = 1
    qtd_itimos_list = []
    for campos in _tools_linhas_ypo(path):
        if len(campos) >= 8:
            nova_fonte = campos[3]
            total_itimos = len(_tools_payload_itimos(campos))
            if nova_fonte not in fontes_list:
                fontes_list.append(nova_fonte)
                qtd_itimos_list.append(total_itimos)
            else:
                index = fontes_list.index(nova_fonte)
                saldo_itimos = qtd_itimos_list[index] - corrige_qtd
                if saldo_itimos == 0:
                    saldo_itimos = 1
                fontes_list.append(nova_fonte)
                qtd_itimos_list.append(saldo_itimos)
                corrige_qtd += 1
    qtd_variatio = 1
    for qtd in qtd_itimos_list:
        qtd_variatio = +(qtd_variatio * qtd)
    return abs(qtd_variatio)


def build_tools_lexico():
    """Regera léxico textual a partir dos temas, sem alterar .ypo."""
    start_time = time.time()
    linhas_lexico = []
    vistos_lexico = set()
    verbetes = []
    vistos_verbetes = set()

    for tema, path in _tools_temas_ativos():
        if not os.path.exists(path):
            continue
        for campos in _tools_linhas_ypo(path):
            if len(campos) < 8:
                continue
            fonte = campos[3]
            for itimo in _tools_payload_itimos(campos):
                for palavra in _tools_palavras_de_itimo(itimo):
                    chave = palavra + " : " + fonte
                    if chave not in vistos_lexico:
                        vistos_lexico.add(chave)
                        linhas_lexico.append(chave)
                    if palavra not in vistos_verbetes:
                        vistos_verbetes.add(palavra)
                        verbetes.append(palavra)

    base_dir = _project_path("base")
    texto_lexico = "\n".join(sorted(linhas_lexico)) + "\n"
    texto_verbetes = "\n".join(sorted(verbetes)) + "\n"
    # Machina atual usa apenas lexico_pt.txt como léxico de trabalho.
    _tools_write_text(os.path.join(base_dir, "lexico_pt.txt"), texto_lexico)
    _tools_write_text(os.path.join(base_dir, "verbetes.txt"), texto_verbetes)
    return f"Build_Léxico: {len(linhas_lexico)} verbete(s)-fonte; {len(verbetes)} verbete(s) únicos. Runtime: {time.time() - start_time:.2f}s"


def build_tools_indexy():
    start_time = time.time()
    temas = _tools_temas_ativos()
    index_list = []
    error_list = []
    acm_variatio = 0
    for tema, path in temas:
        try:
            qtd_variatio = _tools_calcular_variacoes_tema(path)
            acm_variatio += qtd_variatio
            index_list.append(f"{tema} : {qtd_variatio:,} ({_tools_potencia_nome(qtd_variatio)})")
        except Exception as exc:
            error_list.append(f"{tema}: {exc}")

    md_dir = _project_path("md_files")
    about_index = os.path.join(md_dir, BUILD_INDEXY_FILE)
    linhas = []
    linhas.append("variações para cada tema:  ")
    linhas.append("___  ")
    for linha in index_list:
        linhas.append(linha.replace(",", ".") + "  ")
    linhas.extend([
        "___",
        "[escala dos nomes das potências de 10]  ",
        "  ",
        "> mil=1.000|10e3|  ",
        "> milhão=1.000.000|10e6|  ",
        "> bilhão=1.000.000.000|10e9|  ",
        "> trilhão=1.000.000.000.000|10e12|  ",
        "> quatrilhão=1.000.000.000.000.000|10e15|  ",
        "> quintilhão=1.000.000.000.000.000.000|10e18|  ",
        "> sextilhão=1.000.000.000.000.000.000.000|10e21|  ",
        "> setilhão=1.000.000.000.000.000.000.000.000|10e24|  ",
        "> octilhão=1.000.000.000.000.000.000.000.000.000|10e27|  ",
        "> nonilhão=1.000.000.000.000.000.000.000.000.000.000|10e30|  ",
        "> decilhão=1.000.000.000.000.000.000.000.000.000.000.000|10e33|  ",
        "> undecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000|10e36|  ",
        "> dodecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000|10e39|  ",
        "> tredecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000.000|10e42|  ",
        "> quatordecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000|10e45|  ",
        "> quindecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000|10e48|  ",
        "> sedecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000|10e51|  ",
        "> septendecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000|10e54|  ",
        "> googol=dez duotrigintilhões|10e100|  ",
        "> googolplexo=quanto dá isso?|10e googol|  ",
        "> googolplexiano=por enquanto, o maior número com nome|10e googolplexo|  ",
        "  ",
        "[fonte dos dados](http://www.fisica-interessante.com/matematica-divertida-ordens-classes-multiplos.html)  ",
        "___",
        "Copyright © 1983-2022 Nando Lopes - **yPoemas @ máquina de fazer Poesia**  ",
        "",
        f"Total de variações: {acm_variatio:,} ({_tools_potencia_nome(acm_variatio)})".replace(",", "."),
        "",
    ])
    _tools_write_text(about_index, "\n".join(linhas))
    extra = f" Erros: {len(error_list)}." if error_list else ""
    return f"Build_Indexy: {len(index_list)} tema(s). Saída: {about_index}.{extra} Runtime: {time.time() - start_time:.2f}s"


def _tools_matrix_um_tema(tema, path):
    try:
        import numpy as np
        import matplotlib.pyplot as plt
    except Exception as exc:
        raise RuntimeError(f"dependência ausente ou indisponível: {exc}")

    tabela = tema.capitalize()  # comportamento histórico do Build_Matrix.
    matrix_dir = _project_path("images", "matrix")
    os.makedirs(matrix_dir, exist_ok=True)
    curlin = "01"
    linini = 1
    itimos_acm = 0
    x_pos = np.array([]); y_pos = np.array([]); z_pos = np.array([]); z_val = np.array([])

    with open(path, encoding="utf-8") as file:
        for line in file:
            if line.startswith("|", 0, 1):
                campos = line.split("|")
                if len(campos) < 6:
                    continue
                newcol = int(campos[2])
                if campos[1] != curlin:
                    linini += 1
                    curlin = campos[1]
                if newcol == 0:
                    x_pos = np.append(x_pos, linini); y_pos = np.append(y_pos, 0); z_pos = np.append(z_pos, 0); z_val = np.append(z_val, 0)
                else:
                    itimos = int(campos[5])
                    itimos_acm += itimos
                    x_pos = np.append(x_pos, linini - 1); y_pos = np.append(y_pos, newcol - 1); z_pos = np.append(z_pos, 0); z_val = np.append(z_val, itimos)

    x_val = np.ones(len(x_pos)); y_val = np.ones(len(y_pos)); z_pos = np.ones(len(z_pos))
    if len(x_val) > 0:
        fg = plt.figure(figsize=(7, 7))
        ax = fg.add_subplot(111, projection="3d")
        ax.set_xlabel("x ➪ linhas", fontsize=14)
        ax.set_ylabel("y ➪ versos", fontsize=14)
        ax.set_zlabel("z ➪ ítimos", fontsize=14)
        ax.view_init(elev=30, azim=-30)
        ax.bar3d(x_pos, y_pos, z_pos, x_val, y_val, z_val, color="#00ccaa", alpha=0.85, edgecolor="k")
        plt.savefig(os.path.join(matrix_dir, tabela + ".jpg"), dpi=50)
        plt.close(fg)
    return tabela, linini, itimos_acm


def _tools_atualizar_linha_chave(path, chave, nova_linha):
    linhas = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as file:
            linhas = file.read().splitlines()
    chave_norm = str(chave).casefold().strip()
    nova_linha = str(nova_linha).strip()
    saida = []
    alterou = False
    for linha in linhas:
        parte = linha.partition(" : ")[0].strip().casefold()
        if parte == chave_norm:
            if not alterou:
                saida.append(nova_linha)
                alterou = True
            continue
        saida.append(linha)
    if not alterou:
        saida.append(nova_linha)
    _tools_write_text(path, "\n".join(saida).rstrip() + "\n")


def build_tools_matrix(tema_unico=None):
    start_time = time.time()
    temas = _tools_temas_ativos()
    if tema_unico:
        temas = [(tema, path) for tema, path in temas if tema == tema_unico]
    lista_itimos = []
    lista_versos = []
    for tema, path in temas:
        if not os.path.exists(path):
            continue
        tabela, versos, itimos = _tools_matrix_um_tema(tema, path)
        lista_versos.append(f"{tabela} : {versos}")
        lista_itimos.append(f"{tabela} : {itimos}")

    base_dir = _project_path("base")
    if tema_unico:
        for linha in lista_itimos:
            chave = linha.partition(" : ")[0]
            _tools_atualizar_linha_chave(os.path.join(base_dir, "itimos.txt"), chave, linha)
        for linha in lista_versos:
            chave = linha.partition(" : ")[0]
            _tools_atualizar_linha_chave(os.path.join(base_dir, "versos.txt"), chave, linha)
    else:
        _tools_write_text(os.path.join(base_dir, "itimos.txt"), "\n".join(lista_itimos).rstrip() + "\n")
        _tools_write_text(os.path.join(base_dir, "versos.txt"), "\n".join(lista_versos).rstrip() + "\n")
    modo = f"tema {tema_unico}" if tema_unico else "todos os temas"
    return f"Build_Matrix: {modo}; {len(lista_itimos)} Matrix 3D gerada(s)/atualizada(s). Runtime: {time.time() - start_time:.2f}s"


def build_tools_ficha_lexica():
    start_time = time.time()
    temas = _tools_temas_ativos()
    total_itimos = 0
    itimos_unicos = set()
    total_verbetes = 0
    verbetes_unicos = set()
    for tema, path in temas:
        if not os.path.exists(path):
            continue
        for campos in _tools_linhas_ypo(path):
            for itimo in _tools_payload_itimos(campos):
                total_itimos += 1
                itimos_unicos.add(_tools_normaliza_unico(itimo))
                palavras = _tools_palavras_de_itimo(itimo)
                total_verbetes += len(palavras)
                verbetes_unicos.update(palavras)
    bloco = (
        f"{BUILD_AMBIENTE_LEXICO}\n\n"
        f"Total de Verbetes: {_tools_fmt_int(total_verbetes)}\n"
        f"Total de Verbetes únicos: {_tools_fmt_int(len(verbetes_unicos))}\n\n"
        f"Total de Ítimos: {_tools_fmt_int(total_itimos)}\n"
        f"Total de Ítimos únicos: {_tools_fmt_int(len(itimos_unicos))}\n\n"
        f"Total de Temas: {_tools_fmt_int(len(temas))}\n"
    )
    md_dir = _project_path("md_files")
    index_path = os.path.join(md_dir, "INDEX.txt")
    texto = ""
    if os.path.exists(index_path):
        with open(index_path, encoding="utf-8") as file:
            texto = file.read()
    pos = texto.find(BUILD_AMBIENTE_LEXICO)
    if pos >= 0:
        texto = texto[:pos].rstrip() + "\n\n" + bloco
    else:
        texto = (texto.rstrip() + "\n\n" + bloco) if texto.strip() else bloco
    _tools_write_text(index_path, texto)
    return f"Ficha Léxica atualizada em {index_path}. Runtime: {time.time() - start_time:.2f}s\n\n{bloco}"


def _tools_imagem_tema(tema):
    """Busca o grupo de imagem do tema em ./base/images.txt, sem depender de módulos externos."""
    tema_norm = str(tema or "").strip().casefold()
    images_path = _project_path("base", "images.txt")
    if os.path.exists(images_path):
        with open(images_path, encoding="utf-8") as file:
            for raw in file:
                linha = raw.strip()
                if not linha:
                    continue
                nome, sep, resto = linha.partition(" : ")
                if nome.strip().casefold() == tema_norm and sep:
                    return resto.strip() or "Machina"
    return "Machina"


def _tools_info_tema(tema, path):
    """Calcula a linha técnica de ./base/info.txt para um tema ativo.

    Fonte única dos temas: ./base/ativos.txt.
    Não importa build_info.py nem tools.py.
    Não altera .YPO; apenas lê estrutura e escreve documentação derivada.
    """
    genero = "Machina"
    imagem = _tools_imagem_tema(tema)
    versos = 0
    qtd_itimos = 0
    verbetes_tema = set()

    curlin = "star"
    curlin = ""
    for campos in _tools_linhas_ypo(path):
        if len(campos) < 8:
            continue

        # campos: ['', linha, coluna, id/fonte, tipo, qtd, ..., ítimos..., '']
        linha_id = campos[1].strip() if len(campos) > 1 else ""
        if linha_id and linha_id != curlin:
            versos += 1
            curlin = linha_id

        payload = _tools_payload_itimos(campos)
        qtd_itimos += len(payload)
        for itimo in payload:
            verbetes_tema.update(_tools_palavras_de_itimo(itimo))

    qtd_wordin = len(verbetes_tema)
    qtd_lexico = len(verbetes_tema)
    qtd_variatio = _tools_calcular_variacoes_tema(path)
    qtd_cienti = f"{qtd_variatio:.2e}"

    return (
        f"|{tema}|{genero}|{imagem}|{versos}|{qtd_wordin}|"
        f"{qtd_lexico}|{qtd_itimos}|{qtd_variatio}|{qtd_cienti}|"
    )


def _tools_dados_rodape_ypo(path):
    """Calcula apenas o rodapé informativo do .YPO, sem alterar corpo poético."""
    verbetes_no_texto = 0
    total_itimos = 0

    for campos in _tools_linhas_ypo(path):
        if len(campos) < 8:
            continue
        verbetes_no_texto += 1
        total_itimos += len(_tools_payload_itimos(campos))

    total_verbetes = verbetes_no_texto + total_itimos
    qtd_variacoes = _tools_calcular_variacoes_tema(path)
    return {
        "verbetes_no_texto": verbetes_no_texto,
        "total_itimos": total_itimos,
        "total_verbetes": total_verbetes,
        "qtd_variacoes": qtd_variacoes,
    }


def _tools_linhas_rodape_ypo(path):
    dados = _tools_dados_rodape_ypo(path)
    variacoes = dados["qtd_variacoes"]
    return [
        f"Verbetes no Texto = {dados['verbetes_no_texto']}",
        f"  Total de ítimos = {dados['total_itimos']}",
        f"Total de verbetes = {dados['total_verbetes']}",
        f"Qtd. de Variações = {_tools_fmt_int(variacoes)} ({_tools_potencia_nome(variacoes)})",
    ]


def _tools_atualizar_rodape_ypo_um_tema(tema, path):
    """Atualiza só as 4 linhas informativas do rodapé; preserva Build_By_Lay_2_Ipo."""
    novas = _tools_linhas_rodape_ypo(path)
    chaves = {
        "verbetes no texto",
        "total de ítimos",
        "total de itimos",
        "total de verbetes",
        "qtd. de variações",
        "qtd. de variacoes",
    }

    def _eh_linha_rodape_info(linha):
        chave = str(linha or "").strip().partition("=")[0].strip().casefold()
        chave_ascii = unicodedata.normalize("NFKD", chave).encode("ascii", "ignore").decode("ascii")
        return chave in chaves or chave_ascii in chaves

    with open(path, encoding="utf-8") as file:
        linhas = file.read().splitlines()

    eof_idx = None
    for idx, linha in enumerate(linhas):
        if linha.strip().upper() == "<EOF>":
            eof_idx = idx
            break

    build_idx = None
    for idx, linha in enumerate(linhas):
        if linha.strip().casefold().startswith("build_by_lay_2_ipo"):
            build_idx = idx
            break

    if eof_idx is not None:
        # <EOF> é o fim real do tema. Tudo que estiver depois dele é
        # rodapé/documentação e pode ser remontado sem risco de tocar o corpo
        # poético. Preserva apenas a linha histórica Build_By_Lay_2_Ipo.
        build_line = linhas[build_idx] if build_idx is not None else None
        saida = linhas[: eof_idx + 1]
        while saida and saida[-1].strip() == "":
            saida.pop()
        saida.extend(novas)
        if build_line:
            saida.append(build_line)
    elif build_idx is not None:
        # Fallback para arquivos antigos sem <EOF>: mexe somente no bloco
        # informativo imediatamente antes da linha histórica Build_By_Lay_2_Ipo.
        fim_bloco = build_idx
        while fim_bloco > 0 and linhas[fim_bloco - 1].strip() == "":
            fim_bloco -= 1
        ini = fim_bloco
        while ini > 0 and _eh_linha_rodape_info(linhas[ini - 1]):
            ini -= 1
        saida = linhas[:ini] + novas + linhas[build_idx:]
    else:
        # Último fallback: sem <EOF> e sem Build_By, remove linhas
        # informativas conhecidas e acrescenta o bloco no fim.
        saida = [linha for linha in linhas if not _eh_linha_rodape_info(linha)]
        while saida and saida[-1].strip() == "":
            saida.pop()
        saida.extend(novas)

    novo_texto = "\n".join(saida).rstrip() + "\n"
    texto_atual = "\n".join(linhas).rstrip() + "\n"
    if novo_texto != texto_atual:
        _tools_write_text(path, novo_texto)
        return f"{tema}: atualizado"
    return f"{tema}: sem alteração"

def build_tools_atualizar_rodape_ypo(tema_unico=None):
    """Atualiza rodapé informativo dos .YPO sob demanda, localmente."""
    start_time = time.time()
    temas = _tools_temas_ativos()
    if tema_unico:
        temas = [(tema, path) for tema, path in temas if tema == tema_unico]
        if not temas:
            return f"atualizar_rodape_ypo: tema não encontrado em ./base/ativos.txt: {tema_unico}"

    resultados = []
    erros = []
    for tema, path in temas:
        if not os.path.exists(path):
            erros.append(f"{tema}: arquivo não encontrado ({path})")
            continue
        try:
            resultados.append(_tools_atualizar_rodape_ypo_um_tema(tema, path))
        except Exception as exc:
            erros.append(f"{tema}: {exc}")

    try:
        st.cache_data.clear()
    except Exception:
        pass

    alvo = f"tema {tema_unico}" if tema_unico else "todos os temas ativos"
    msg = f"atualizar_rodape_ypo: {alvo}; {len(resultados)} tema(s). Runtime: {time.time() - start_time:.2f}s"
    if resultados:
        msg += "\n" + "\n".join(resultados)
    if erros:
        msg += "\nErros:\n" + "\n".join(erros)
    return msg


def build_tools_info():
    """Atualiza ./base/info.txt pela Central local, lendo diretamente ./base/ativos.txt."""
    start_time = time.time()
    linhas = []
    erros = []

    for tema, path in _tools_temas_ativos():
        if not os.path.exists(path):
            erros.append(f"{tema}: arquivo não encontrado ({path})")
            continue
        try:
            linhas.append(_tools_info_tema(tema, path))
        except Exception as exc:
            erros.append(f"{tema}: {exc}")

    info_path = _project_path("base", "info.txt")
    _tools_write_text(info_path, "\n".join(linhas).rstrip() + "\n")

    msg = f"Build_Info: {len(linhas)} tema(s) em ./base/info.txt. Runtime: {time.time() - start_time:.2f}s"
    if erros:
        msg += "\nErros:\n" + "\n".join(erros)
    return msg


def build_tools_update(tema):
    """Atualiza derivados de tema já existente."""
    tema = str(tema or "").strip()
    temas = dict(_tools_temas_ativos())
    if tema not in temas:
        return "Build_update: tema não encontrado em ./base/ativos.txt."
    if not os.path.exists(temas[tema]):
        return f"Build_update: arquivo do tema não encontrado: {temas[tema]}"
    resultados = [
        build_tools_lexico(),
        build_tools_matrix(tema),
        build_tools_atualizar_rodape_ypo(tema),
        build_tools_indexy(),
        build_tools_ficha_lexica(),
        build_tools_info(),
    ]
    try:
        st.cache_data.clear()
    except Exception:
        pass
    return "\n\n".join(resultados)


def build_tools_novo_tema(tema):
    """Cadastro técnico de novo tema já criado pelo autor em ./data."""
    tema = str(tema or "").strip()
    if not tema:
        return "Build_Novo_Tema: informe o nome do tema."
    if any(sep in tema for sep in ("/", "\\", ":", "*", "?", '"', "<", ">", "|")):
        return "Build_Novo_Tema: nome de tema contém caractere inválido para arquivo."
    ypo_path = _tools_resolve_ypo_path(tema)
    if not os.path.exists(ypo_path):
        return f"Build_Novo_Tema: crie antes o arquivo autoral em ./data/{tema}.YPO ou ./data/{tema}.ypo. Nada foi cadastrado."

    alteracoes = []
    if _tools_add_unique_line(_project_path("base", "ativos.txt"), f"{tema} : Machina", tema):
        alteracoes.append("base/ativos.txt")
    if _tools_add_unique_line(_project_path("base", "images.txt"), f"{tema} : machina", tema):
        alteracoes.append("base/images.txt")
    if _tools_add_unique_line(_project_path("temp", "readings.txt"), f"|{tema}|0|", tema):
        alteracoes.append("temp/readings.txt")
    if _tools_add_unique_line(_project_path("base", "rol_todos os temas.txt"), tema, tema):
        alteracoes.append("base/rol_todos os temas.txt")

    resultados = [
        "Build_Novo_Tema: cadastro técnico verificado.",
        "Arquivos cadastrais alterados: " + (", ".join(alteracoes) if alteracoes else "nenhum; tema já estava cadastrado"),
        build_tools_update(tema),
    ]
    return "\n\n".join(resultados)


def _tools_remove_linhas_por_tema(path, tema):
    """Remove linhas cadastrais/derivadas relacionadas a um tema. Retorna qtd removida."""
    tema_norm = str(tema or "").strip().casefold()
    if not tema_norm or not os.path.exists(path):
        return 0

    with open(path, encoding="utf-8") as file:
        linhas = file.read().splitlines()

    saida = []
    removidas = 0
    for raw in linhas:
        raw_strip = raw.strip()
        chave = raw_strip.partition(" : ")[0].strip().casefold()

        if raw_strip.startswith("|"):
            campos = raw_strip.split("|")
            if len(campos) > 1:
                chave = campos[1].strip().casefold()

        remove = False
        if chave == tema_norm:
            remove = True
        elif raw_strip.casefold() == tema_norm:
            remove = True

        if remove:
            removidas += 1
        else:
            saida.append(raw)

    if removidas:
        _tools_write_text(path, "\n".join(saida).rstrip() + ("\n" if saida else ""))
    return removidas


def _tools_remover_arquivo(path):
    """Remove arquivo se existir. Retorna True/False."""
    if path and os.path.exists(path) and os.path.isfile(path):
        os.remove(path)
        return True
    return False


def build_tools_remove_tema(tema):
    """Remove tecnicamente um tema do ambiente local e atualiza derivados."""
    tema = str(tema or "").strip()
    if not tema:
        return "remove_tema: escolha um tema."

    ypo_path = _tools_resolve_ypo_path(tema)
    removidos = []

    # Listas cadastrais e derivadas simples.
    arquivos_lista = [
        _project_path("base", "ativos.txt"),
        _project_path("base", "images.txt"),
        _project_path("temp", "readings.txt"),
        _project_path("base", "itimos.txt"),
        _project_path("base", "versos.txt"),
    ]

    base_dir = _project_path("base")
    if os.path.isdir(base_dir):
        for name in sorted(os.listdir(base_dir)):
            if name.lower().startswith("rol_") and name.lower().endswith(".txt"):
                arquivos_lista.append(os.path.join(base_dir, name))

    vistos = set()
    for path in arquivos_lista:
        if path in vistos:
            continue
        vistos.add(path)
        qtd = _tools_remove_linhas_por_tema(path, tema)
        if qtd:
            removidos.append(f"{os.path.relpath(path, _project_path())}: {qtd} linha(s)")

    # Imagem Matrix derivada do tema, se existir.
    matrix_dir = _project_path("images", "matrix")
    matrix_candidates = {
        os.path.join(matrix_dir, tema + ".jpg"),
        os.path.join(matrix_dir, tema.capitalize() + ".jpg"),
        os.path.join(matrix_dir, tema + ".JPG"),
        os.path.join(matrix_dir, tema.capitalize() + ".JPG"),
    }
    for candidate in sorted(matrix_candidates):
        if _tools_remover_arquivo(candidate):
            removidos.append(f"{os.path.relpath(candidate, _project_path())}: removido")

    # Arquivo autoral do tema. remove_tema é ação explícita do usuário.
    ypo_removido = False
    for candidate in [ypo_path, _project_path("data", tema + ".ypo"), _project_path("data", tema + ".YPO")]:
        if _tools_remover_arquivo(candidate):
            removidos.append(f"{os.path.relpath(candidate, _project_path())}: removido")
            ypo_removido = True

    resultados = [
        f"remove_tema: {tema}",
        "Alterações: " + ("\n" + "\n".join(removidos) if removidos else "nenhuma ocorrência encontrada"),
    ]

    # Recria derivados que dependem do conjunto ativo restante.
    resultados.extend([
        build_tools_lexico(),
        build_tools_indexy(),
        build_tools_ficha_lexica(),
        build_tools_info(),
    ])

    try:
        st.cache_data.clear()
    except Exception:
        pass

    if not ypo_removido:
        resultados.insert(2, "Arquivo .YPO/.ypo não encontrado em ./data; listas/derivados foram tratados mesmo assim.")

    return "\n\n".join(resultados)


def build_tools_off_lex():
    start_time = time.time()
    off_dir = _project_path("off_machina")
    if not os.path.isdir(off_dir):
        return "Build_Off_Lex: pasta ./off_machina não encontrada."
    list_lexico = []
    list_verbet = []
    for name in sorted(os.listdir(off_dir)):
        if not name.lower().endswith(".pip"):
            continue
        script = os.path.join(off_dir, name)
        with open(script, encoding="utf-8") as file:
            for line in file:
                if not line.startswith("|"):
                    continue
                alinhas = line.split("|")
                if len(alinhas) < 3:
                    continue
                fonte = alinhas[1]
                if "Dados de Catalogação" in fonte or "copyrights" in fonte:
                    continue
                for itimo in alinhas[2:len(alinhas)-1]:
                    for word in itimo.split(" "):
                        if "-" not in word:
                            for c in string.punctuation:
                                word = word.replace(c, "")
                        word = word.strip().lower()
                        if len(word) >= 3:
                            if word not in list_verbet:
                                list_verbet.append(word)
                            chave = word + "|" + fonte
                            if chave not in list_lexico:
                                list_lexico.append(chave)
    _tools_write_text(os.path.join(off_dir, "off_lexico.txt"), "".join("|" + line + "|\n" for line in list_lexico))
    _tools_write_text(os.path.join(off_dir, "off_verbet.txt"), "".join(line + "\n" for line in list_verbet))
    return f"Build_Off_Lex: {len(list_lexico)} ocorrência(s); {len(list_verbet)} verbete(s). Runtime: {time.time() - start_time:.2f}s"


def build_tools_all():
    resultados = [
        build_tools_lexico(),
        build_tools_matrix(),
        build_tools_indexy(),
        build_tools_ficha_lexica(),
        build_tools_info(),
    ]
    try:
        st.cache_data.clear()
    except Exception:
        pass
    return "\n\n".join(resultados)


def _tools_run_button(label, func, *args):
    if st.button(label, use_container_width=True):
        with st.spinner(label + "..."):
            try:
                resultado = func(*args)
                st.success(label + " concluído.")
                st.text(resultado)
            except Exception as exc:
                st.error(f"{label} falhou: {exc}")


def _tools_help_text():
    return """help_? — Tools locais da Machina

novo_tema
  Cadastra tecnicamente um tema novo que já existe em ./data como .YPO/.ypo.
  Atualiza arquivos cadastrais necessários e depois roda update_tema.

remove_tema
  Remove tecnicamente um tema do ambiente local. A lista de remoção vem dos
  yPoemas/rol_*.txt, ativos e ./data para capturar listas desencontradas.
  Remove listas cadastrais, rol_*.txt, arquivo .YPO/.ypo e Matrix derivada,
  depois atualiza os derivados.

update_tema
  Atualiza derivados de um tema já existente em ./base/ativos.txt.
  Roda léxico, matrix do tema, rodapé informativo do .ypo, indexy, ficha_lexico e info.

atualizar_rodape_ypo
  Atualiza sob demanda as 4 linhas informativas do rodapé dos .ypo.
  Mantém a linha Build_By_Lay_2_Ipo como está.

build_indexy
  Atualiza ./md_files/ABOUT_index.MD com as variações combinatórias por tema.

build_lexico
  Regera ./base/lexico_pt.txt e ./base/verbetes.txt a partir dos temas ativos.

build_off-lex
  Regera ./off_machina/off_lexico.txt e ./off_machina/off_verbet.txt.
  Base futura da eureka_off_machina.

build_matrix
  Gera as imagens Matrix 3D XYZ e atualiza ./base/itimos.txt e ./base/versos.txt.
  Requer numpy + matplotlib no ambiente local.

build_info
  Atualiza ./base/info.txt pela própria Central local, lendo diretamente ./base/ativos.txt.

build_all
  Reconstrução geral dos derivados principais: léxico, matrix, indexy, ficha_lexico e info.

ficha_lexico
  Atualiza o bloco final “Ambiente Léxico da Machina” em ./md_files/INDEX.txt.

chk_utf-8
  Verifica ./base/ativos.txt e todos os temas ativos em UTF-8 estrito.
  Não converte nem altera arquivos.
"""


def page_local_tools():
    st.subheader("ypo_seguro_tools")
    st.caption("LOCAL. Lista funcional simples. Lê temas; não altera poesia.")

    tools_items = [
        "novo_tema",
        "remove_tema",
        "update_tema",
        "atualizar_rodape_ypo",
        "---",
        "build_indexy",
        "build_lexico",
        "build_off-lex",
        "build_matrix",
        "build_info",
        "build_all",
        "---",
        "ficha_lexico",
        "chk_utf-8",
        "---",
        "help_?",
    ]

    try:
        temas_local = [tema for tema, path in _tools_temas_ativos()]
    except Exception:
        temas_local = []

    try:
        temas_remocao = _tools_temas_para_remover()
    except Exception:
        temas_remocao = temas_local

    escolha = st.selectbox(
        "tools",
        tools_items,
        index=tools_items.index("help_?"),
        key="tools_lista_funcional",
    )

    if escolha == "---":
        st.info("separador")
        return

    tema_update = None
    tema_remove = None
    tema_rodape = None
    novo_tema = ""

    if escolha == "update_tema":
        if temas_local:
            tema_update = st.selectbox(
                "tema",
                temas_local,
                key="tools_lista_update_tema",
            )
        else:
            st.warning("Nenhum tema encontrado em ./base/ativos.txt.")
            return

    elif escolha == "remove_tema":
        if temas_remocao:
            tema_remove = st.selectbox(
                "tema",
                temas_remocao,
                key="tools_lista_remove_tema",
            )
        else:
            st.warning("Nenhum tema encontrado nas listas dos yPoemas ou em ./data.")
            return

    elif escolha == "atualizar_rodape_ypo":
        opcoes_rodape = ["todos os temas"] + temas_local
        tema_rodape = st.selectbox(
            "tema",
            opcoes_rodape,
            key="tools_lista_rodape_ypo",
        )
        if tema_rodape == "todos os temas":
            tema_rodape = None

    elif escolha == "novo_tema":
        novo_tema = st.text_input(
            "novo tema já existente em ./data",
            key="tools_lista_novo_tema",
        )

    if escolha == "help_?":
        st.text(_tools_help_text())
        return

    mapa = {
        "novo_tema": (build_tools_novo_tema, (novo_tema,)),
        "remove_tema": (build_tools_remove_tema, (tema_remove,)),
        "update_tema": (build_tools_update, (tema_update,)),
        "atualizar_rodape_ypo": (build_tools_atualizar_rodape_ypo, (tema_rodape,)),
        "build_indexy": (build_tools_indexy, ()),
        "build_lexico": (build_tools_lexico, ()),
        "build_off-lex": (build_tools_off_lex, ()),
        "build_matrix": (build_tools_matrix, ()),
        "build_info": (build_tools_info, ()),
        "build_all": (build_tools_all, ()),
        "ficha_lexico": (build_tools_ficha_lexica, ()),
        "chk_utf-8": (build_tools_utf8_temas, ()),
    }

    func, args = mapa[escolha]
    if st.button(escolha, use_container_width=True):
        with st.spinner(escolha + "..."):
            try:
                resultado = func(*args)
                st.success(escolha + " concluído.")
                st.text(resultado)
            except Exception as exc:
                st.error(f"{escolha} falhou: {exc}")


### eof: pages


SIDEBAR_FILHOTE_WIDTH_PX = 64
CIA_MOOD_OPTIONS = [
    "Sintática",
    "Sintética",
    "Formal",
    "Completa",
    "Index",
]
def render_sidebar_for_page(chosen_id):
    """Renderiza os controles fixos do leitor."""
    pick_lang()
    pick_stage_font()
    draw_check_buttons()


def _set_machina_page(page_label, page_id):
    """Fixa a página ativa em estado explícito.

    Evita que cliques internos de uma página, especialmente a navegação
    da Off-Machina, caiam de volta no foco inicial yPoemas.
    """
    st.session_state["machina_page_select"] = page_label
    st.session_state["machina_page_id"] = str(page_id)


def _sync_machina_page_state(page_labels, page_ids):
    """Mantém label e id coerentes sem resetar indevidamente para yPoemas."""
    ids_to_labels = {str(page_id): label for label, page_id in page_ids.items()}

    saved_id = str(st.session_state.get("machina_page_id", "")).strip()
    saved_label = st.session_state.get("machina_page_select", "")

    if saved_id in ids_to_labels:
        _set_machina_page(ids_to_labels[saved_id], saved_id)
        return

    if saved_label in page_labels:
        _set_machina_page(saved_label, page_ids[saved_label])
        return

    _set_machina_page("yPoemas", page_ids["yPoemas"])


def main():
    gramado = open_gramado()

    with gramado:
        page_labels = ["mini", "yPoemas", "eureka", "off-Machina", "About"]
        page_ids = {
            "mini": "1",
            "yPoemas": "2",
            "eureka": "3",
            "off-Machina": "4",
            "About": "5",
        }

        _sync_machina_page_state(page_labels, page_ids)

        page_cols = st.columns(len(page_labels))
        for page_label, page_col in zip(page_labels, page_cols):
            with page_col:
                if st.button(
                    page_label,
                    key=f"machina_page_btn_{page_label}",
                    use_container_width=True,
                    type="primary" if page_label == st.session_state["machina_page_select"] else "secondary",
                ):
                    _set_machina_page(page_label, page_ids[page_label])
                    try:
                        st.rerun()
                    except AttributeError:
                        st.experimental_rerun()

        chosen_label = st.session_state["machina_page_select"]
        chosen_id = st.session_state.get("machina_page_id", page_ids.get(chosen_label, "2"))

        st.divider()

        render_sidebar_for_page(chosen_id)

        palco = st.container()
        with palco:
            palco_container = open_palco()

            with palco_container:
                if chosen_id == "1":
                    page_mini()
                    status = f"🌿  {st.session_state.lang} - {st.session_state.tema} ( {st.session_state.mini + 1} / {len(load_temas('todos os temas'))} )"

                elif chosen_id == "2":
                    page_ypoemas()
                    current_book = _current_book()
                    status = palco_status(
                        current_book,
                        st.session_state.get("take", 0) + 1,
                        len(load_temas(current_book)),
                    )
                elif chosen_id == "3":
                    page_eureka()
                    status = palco_status("eureka")
                elif chosen_id == "4":
                    page_off_machina()
                    status = palco_status("off-machina")
                elif chosen_id == "5":
                    page_abouts()
                    status = palco_status("About")
                else:
                    page_ypoemas()
                    current_book = _current_book()
                    status = palco_status(
                        current_book,
                        st.session_state.get("take", 0) + 1,
                        len(load_temas(current_book)),
                    )

                render_sidebar_context_image(chosen_id)


if __name__ == "__main__":
    main()
