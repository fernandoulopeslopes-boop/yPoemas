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

try:
    from ponte_ola_openai import gerar_analise_ola as _gerar_analise_ola_real
except Exception:
    _gerar_analise_ola_real = None

APP_BUILD = "2026-07-02_PUBLICA_LIMPA"
APP_BUILD_NOTES = "Versão pública limpa."

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
    "versão Mobile",
    "carta de Guimarães Rosa",
    "veredas",
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
    "versão Mobile": ["ABOUT_mobile.md"],
    "carta de Guimarães Rosa": ["A incrível carta de Guimarães Rosa.md"],
    "veredas": ["ABOUT_veredas.md"],
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
    "pt": "pt-BR-AntonioNeural",
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
    page_title="a Machina de fazer Poesia @ Mobile",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# -----------------------------------------------------------------------------
# Versao mobile/portrait.
# Mantem o motor poetico intacto e troca apenas a ergonomia visual:
# toda area que no desktop usava colunas passa a ser lida em sequencia.
# -----------------------------------------------------------------------------
MACHINA_MOBILE_PORTRAIT = True
_MACHINA_DESKTOP_COLUMNS = getattr(getattr(st, "_main", None), "columns", st.columns)
st._machina_original_columns = _MACHINA_DESKTOP_COLUMNS

BOTOES_MOBILE = {
    "mais_uma_versao": "\u271a",
    "tema_anterior": "\u25c0",
    "tema_ao_acaso": "\u273b",
    "proximo_tema": "\u25b6",
    "voz": "\U0001f4e3",
    "automatico": "\U0001f500",
    "help": "?",
}

HINTS_MOBILE = {
    "mais_uma_versao": "mais_uma_versao",
    "tema_anterior": "tema_anterior",
    "tema_ao_acaso": "tema_ao_acaso",
    "proximo_tema": "proximo_tema",
    "voz": "voz",
    "automatico": "automatico",
    "help": "help",
}


def _machina_mobile_columns(spec, *args, **kwargs):
    """Empilha colunas no mobile, preservando a assinatura usada no desktop."""
    if not MACHINA_MOBILE_PORTRAIT:
        return _MACHINA_DESKTOP_COLUMNS(spec, *args, **kwargs)

    count = int(spec) if isinstance(spec, int) else len(spec)
    return [st.container() for _ in range(count)]


# Mantem st.columns original. O empilhamento mobile agora e feito caso a caso;
# as barras de navegacao usam containers horizontais nativos.
st.columns = _MACHINA_DESKTOP_COLUMNS


def mobile_row_columns(spec, *args, **kwargs):
    """Linha real para botoes compactos no mobile."""
    return st.columns(spec, *args, **kwargs)


def mobile_button_row(scope, buttons):
    """Desenha botoes nativos em uma unica linha, sem navegar/recarregar a aba."""
    clicked = ""
    try:
        row = st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center", gap="small")
    except TypeError:
        row = st.container()

    with row:
        for button in buttons:
            action = str(button.get("action", ""))
            if st.button(
                str(button.get("label", "")),
                key=f"machina_mobile_{scope}_{action}",
                help=str(button.get("help", "")),
                type=str(button.get("type", "secondary")),
                width="stretch",
            ):
                clicked = action

    return clicked


def mobile_header_zones():
    """Cria tres zonas horizontais: lista esquerda, navegacao, lista direita."""
    try:
        return mobile_row_columns([3, 4, 3], vertical_alignment="bottom")
    except TypeError:
        return mobile_row_columns([3, 4, 3])


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
    if MACHINA_MOBILE_PORTRAIT:
        st.markdown(
            """
            <style>
            .main .block-container,
            section.main > div.block-container {
                padding-left: 0.24rem !important;
                padding-right: 0.24rem !important;
                max-width: 100vw !important;
            }

            div[data-testid="stButton"] button {
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                min-height: 2.78rem !important;
                width: 100% !important;
                font-size: 1.06rem !important;
                text-align: center !important;
                margin-top: 0.06rem !important;
                margin-bottom: 0.06rem !important;
            }

            div[data-testid="stButton"] button p {
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                width: 100% !important;
                margin: 0 !important;
                text-align: center !important;
                line-height: 1 !important;
            }

            div[data-testid="stButton"] button > div,
            div[data-testid="stButton"] button span {
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                width: 100% !important;
                text-align: center !important;
            }

            .st-key-copy_qtd_widget div[data-baseweb="select"] > div {
                min-height: 2.78rem !important;
                height: 2.78rem !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }

            .st-key-copy_qtd_widget div[data-baseweb="select"] span,
            .st-key-copy_qtd_widget div[data-baseweb="select"] input {
                line-height: 1 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
            }

            .st-key-copy_variacoes_btn button {
                border: 1px solid rgba(49, 51, 63, 0.35) !important;
                border-radius: 0.42rem !important;
                background: white !important;
                color: rgb(49, 51, 63) !important;
                box-shadow: none !important;
                font-size: 0.98rem !important;
                padding-left: 0.18rem !important;
                padding-right: 0.18rem !important;
            }

            div[data-testid="stHorizontalBlock"] {
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                align-items: stretch !important;
                gap: 0.18rem !important;
                width: 100% !important;
                max-width: 100% !important;
            }

            div[data-testid="stHorizontalBlock"] > div,
            div[data-testid="stHorizontalBlock"] div[data-testid="column"] {
                min-width: 0 !important;
                max-width: none !important;
                padding-left: 0 !important;
                padding-right: 0 !important;
            }

            div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] {
                width: 100% !important;
                min-width: 0 !important;
            }

            .machina-mobile-link-row {
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                align-items: stretch !important;
                gap: 0.16rem !important;
                width: 100% !important;
                max-width: 100% !important;
                margin: 0.08rem 0 0.12rem 0 !important;
            }

            .machina-mobile-link-btn {
                flex: 1 1 0 !important;
                min-width: 0 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                min-height: 3.05rem !important;
                padding: 0.18rem 0.10rem !important;
                border-radius: 0.42rem !important;
                border: 1px solid rgba(49, 51, 63, 0.20) !important;
                background: #ffffff !important;
                color: #31333f !important;
                text-decoration: none !important;
                font-size: 1.08rem !important;
                line-height: 1 !important;
                white-space: nowrap !important;
                box-sizing: border-box !important;
            }

            .machina-mobile-link-btn:hover,
            .machina-mobile-link-btn:focus {
                border-color: rgba(49, 51, 63, 0.40) !important;
                color: #31333f !important;
                text-decoration: none !important;
            }

            .machina-mobile-link-active {
                background: #eef8ee !important;
                border-color: rgba(49, 51, 63, 0.44) !important;
                font-weight: 700 !important;
            }

            div[data-testid="stSelectbox"],
            div[data-testid="stTextInput"] {
                width: 100% !important;
                max-width: 100% !important;
            }

            .machina-palco-central,
            .machina-gramado {
                border-radius: 12px !important;
                min-height: auto !important;
                overflow-x: hidden !important;
            }

            .machina-ypoema-text {
                max-width: 94vw !important;
                width: 100% !important;
                line-height: 1.38 !important;
                padding-left: 0.18rem !important;
                padding-right: 0.18rem !important;
                box-sizing: border-box !important;
            }

            .logo-text {
                line-height: 1.38 !important;
                box-sizing: border-box !important;
            }

            .machina-sidebar-image-frame {
                width: min(82vw, 260px) !important;
                height: auto !important;
                aspect-ratio: 8 / 11 !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

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
            font-size: 0.84rem !important;
        }

        [data-testid="stSidebar"] .stButton button p {
            margin: 0 !important;
            padding: 0 !important;
            text-indent: 0 !important;
            font-size: 0.84rem !important;
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
            width: min(180px, 34vw) !important;
            max-width: min(180px, 34vw) !important;
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
        "talk": True,
        "arts": [],
        "auto": False,
        "rand": False,
        "stage_font": "Trebuchet",
        "stage_size": 21,
        "sidebar_panel": "Machina",
        "analysis_voice": "Machina",
        "analysis_kind": "Sintática",
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
        "ypo_focus_key": "",
        "ypo_focus_text": "",
        "mini_focus_key": "",
        "mini_focus_text": "",
        "eureka_focus_key": "",
        "eureka_focus_text": "",
        "eureka_last_find": "",
        "off_focus_key": "",
        "off_focus_text": "",
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


def _ypo_focus_key():
    """Identidade do texto em foco no palco yPoemas."""
    return "|".join([
        str(st.session_state.get("book", "")),
        str(st.session_state.get("take", "")),
        str(st.session_state.get("tema", "")),
        str(st.session_state.get("lang", "")),
    ])


def _remember_focus(prefix, key, text):
    st.session_state[f"{prefix}_focus_key"] = key
    st.session_state[f"{prefix}_focus_text"] = text


def _has_focus(prefix, key):
    return (
        st.session_state.get(f"{prefix}_focus_key", "") == key
        and bool(st.session_state.get(f"{prefix}_focus_text", ""))
    )


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
    """Lista de quantidade: escolhe, mas não dispara a geração."""
    st.session_state["copy_qtd"] = _normalizar_qtd_copias(
        st.session_state.get("copy_qtd_widget", st.session_state.get("copy_qtd", 2))
    )
    limpar_copias_palco()
    st.session_state["copy_qtd_changed"] = False


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


### bof: helpers

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


def pick_book_palco(label_text=None, label_visibility="visible"):
    """Escolhe o livro yPoemas diretamente no palco."""
    _sync_book_theme_state()

    books_list = BOOKS_LIST
    current = _current_book()
    key = "palco_book_select"
    _prepare_book_widget(key)

    st.selectbox(
        label_text if label_text is not None else str(len(books_list)) + " ↓",
        books_list,
        index=books_list.index(current),
        key=key,
        on_change=_on_palco_book_change,
        label_visibility=label_visibility,
    )


def pick_tema_palco(label_text=None, label_visibility="visible"):

    """Escolhe o tema atual do livro diretamente no palco."""
    _sync_book_theme_state()
    temas_list = load_temas(_current_book())
    if not temas_list:
        return

    widget_key = _prepare_theme_widget()
    st.session_state["_ypo_theme_widget_key"] = widget_key
    options = list(range(len(temas_list)))
    st.selectbox(
        label_text if label_text is not None else f"{len(temas_list)} ↓",
        options,
        index=_coerce_take(st.session_state.get("take", 0), temas_list),
        format_func=lambda z: temas_list[z],
        key=widget_key,
        on_change=_on_palco_theme_change,
        label_visibility=label_visibility,
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
    returns.append(HINTS_MOBILE["tema_anterior"])
    returns.append(HINTS_MOBILE["tema_ao_acaso"])
    returns.append(HINTS_MOBILE["proximo_tema"])
    returns.append(translate("mais lidos..."))
    returns.append(HINTS_MOBILE["mais_uma_versao"])
    returns.append(translate("arte"))
    returns.append(HINTS_MOBILE["voz"])
    returns.append(HINTS_MOBILE["automatico"])
    returns.append(HINTS_MOBILE["help"])

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


### eof: helpers
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


def render_help_pacote_centralizado(texto, key="help_pacote"):
    """Centraliza o pacote HELP mantendo cada item em linha própria."""
    linhas_html = []
    for line in str(texto or "").splitlines():
        if "copyright" in str(line or "").casefold():
            continue

        safe_line = html.escape(line)
        if safe_line.strip():
            linhas_html.append(f"<div class='machina-help-line'>{safe_line}</div>")
        else:
            linhas_html.append("<div class='machina-help-blank'>&nbsp;</div>")

    corpo = "\n".join(linhas_html)
    st.markdown(
        f"""
        <div class="machina-help-pacote-wrap" style="
            width:100%;
            max-width:100%;
            display:flex;
            justify-content:center;
            align-items:flex-start;
            margin:0.25rem auto 0.75rem auto;
            box-sizing:border-box;
        ">
            <div class="machina-help-pacote" style="
                display:block;
                text-align:left;
                width:fit-content;
                max-width:min(78ch, 100%);
                margin:0 auto;
                padding:0.40rem 0.80rem;
                font-family:'Trebuchet MS', system-ui, sans-serif;
                font-size:0.98rem;
                line-height:1.42;
                background:transparent;
                border:0;
                box-sizing:border-box;
            ">
                <style>
                .machina-help-pacote .machina-help-line {{
                    margin:0 0 0.55rem 0;
                    padding:0;
                    white-space:normal;
                }}
                .machina-help-pacote .machina-help-blank {{
                    height:0.20rem;
                    min-height:0.20rem;
                    line-height:0.20rem;
                }}
                </style>
                {corpo}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def _manual_talk_intro():
    """Linha padrão dos Helps: legenda da voz dentro da lista de botões."""
    return translate("📣 ouvir a leitura do texto")


def _manual_inserir_talk_entre_botoes(raw_text):
    """Insere a legenda da voz entre ▶ e ? no manual dos botões."""
    linhas = []
    for line in str(raw_text or "").splitlines():
        if "ouvir a leitura do texto" in line.casefold():
            continue
        linhas.append(line)

    talk_line = _manual_talk_intro()
    for idx, line in enumerate(linhas):
        clean = line.strip()
        if clean.startswith("?") and "=" in clean:
            linhas.insert(idx, talk_line)
            return "\n".join(linhas)

    for idx, line in enumerate(linhas):
        if "▶" in line:
            linhas.insert(idx + 1, talk_line)
            return "\n".join(linhas)

    linhas.append(talk_line)
    return "\n".join(linhas)


def _manual_text_sem_linha(raw_text, trecho):
    """Remove linhas de manual que contenham determinado trecho."""
    linhas = []
    alvo = str(trecho or "").casefold()
    for line in str(raw_text or "").splitlines():
        if alvo and alvo in line.casefold():
            continue
        linhas.append(line)
    return "\n".join(linhas)


def _manual_off_machina_texto():
    """Manual Off-Machina com ajuste fino pedido para o item 4."""
    manual = load_md_file("MANUAL_OFF-MACHINA.md")
    manual = _manual_text_sem_linha(manual, "selecione um livro da lista para ler")

    bloco_listas = (
        '- selecione o livro na "lista de livros";\n'
        '- selecione o tema na "lista de temas".\n\n'
    )

    padrao = re.compile(r"(?im)^(\s*help.*nav_buttons.*|\s*nav_buttons.*)$")
    if padrao.search(manual) and bloco_listas not in manual:
        manual = padrao.sub(bloco_listas + r"\1", manual, count=1)
    elif bloco_listas not in manual:
        manual = bloco_listas + manual

    return manual


def render_manual_off_machina():
    """Help padrão da página Off-Machina."""
    render_help_pacote_centralizado(
        _manual_inserir_talk_entre_botoes(_manual_off_machina_texto()),
        key="help_off_machina",
    )


def _help_html_to_text(value):
    """Converte blocos antigos com <br> em texto nativo do Streamlit."""
    texto = str(value or "")
    texto = texto.replace("<br/>", "\n").replace("<br />", "\n").replace("<br>", "\n")
    texto = re.sub(r"<[^>]+>", "", texto)
    texto = html.unescape(texto)
    linhas = [linha.rstrip() for linha in texto.splitlines()]
    while linhas and not linhas[0].strip():
        linhas.pop(0)
    while linhas and not linhas[-1].strip():
        linhas.pop()
    return "\n".join(linhas)


def render_help_ypoemas_mesma_fonte():
    """Help yPoemas: desenho simples original.

    Manual + info.txt + Matrix + write_ypoema().
    """
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

    if not st.session_state.get("tema", ""):
        return

    LOGO_TEXTO = load_info(st.session_state.tema)
    if st.session_state.lang != "pt":  # translate if idioma <> pt
        LOGO_TEXTO = translate(LOGO_TEXTO)

    LOGO_IMAGE = (
        "./images/matrix/" + st.session_state.tema.capitalize() + ".jpg"
    )
    write_ypoema(LOGO_TEXTO, LOGO_IMAGE)


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
    def _format_milhar(valor):
        digits = re.sub(r"\D", "", str(valor or ""))
        if not digits:
            return str(valor or "")
        try:
            return f"{int(digits):,}".replace(",", ".")
        except Exception:
            return str(valor or "")

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
                    result += "Análise : " + _format_milhar(qtd_analiz) + "  " + "<br>"
                    result += "Notação Científica: " + qtd_cienti + "  " + "<br>"
                    result += "<br>"

        return result

def _find_ypo_file(nome_tema):
    """Localiza o .ypo do tema em foco sem depender de caixa/acento."""
    tema = str(nome_tema or "").strip()
    if not tema:
        return ""

    data_dir = _project_path("data")
    direct_candidates = [
        os.path.join(data_dir, tema + ".ypo"),
        os.path.join(data_dir, tema + ".YPO"),
        os.path.join(data_dir, tema.capitalize() + ".ypo"),
        os.path.join(data_dir, tema.capitalize() + ".YPO"),
    ]
    for candidate in direct_candidates:
        if os.path.exists(candidate):
            return candidate

    if not os.path.isdir(data_dir):
        return ""

    tema_key = _md_nome_chave(tema)
    for real_name in os.listdir(data_dir):
        if not real_name.lower().endswith(".ypo"):
            continue
        real_base = os.path.splitext(real_name)[0]
        if _md_nome_chave(real_base) == tema_key:
            return os.path.join(data_dir, real_name)

    return ""


def _find_matrix_image(nome_tema):
    """Localiza o gráfico 3D Matrix do tema em foco sem depender só de capitalize()."""
    tema = str(nome_tema or "").strip()
    if not tema:
        return None

    matrix_dir = _project_path("images", "matrix")
    extensions = [".jpg", ".jpeg", ".png", ".webp"]
    names = [tema, tema.capitalize(), tema.upper(), tema.lower()]
    for name in names:
        for ext in extensions:
            candidate = os.path.join(matrix_dir, name + ext)
            if os.path.exists(candidate):
                return candidate

    if not os.path.isdir(matrix_dir):
        return None

    tema_key = _md_nome_chave(tema)
    for real_name in os.listdir(matrix_dir):
        low = real_name.lower()
        if not low.endswith(tuple(extensions)):
            continue
        real_base = os.path.splitext(real_name)[0]
        if _md_nome_chave(real_base) == tema_key:
            return os.path.join(matrix_dir, real_name)

    return None


def load_rodape_ypo(nome_tema):
    """Lê o rodapé informativo do .ypo: tudo que vem depois de <EOF>.

    O Help apenas exibe. Não altera o .ypo.
    """
    path = _find_ypo_file(nome_tema)
    if not path:
        return ""

    try:
        with open(path, "r", encoding="utf-8") as file:
            linhas = file.read().splitlines()
    except Exception:
        return ""

    rodape = []
    achou_eof = False
    for line in linhas:
        if achou_eof:
            rodape.append(line.rstrip())
        elif line.strip().upper() == "<EOF>":
            achou_eof = True

    while rodape and not rodape[0].strip():
        rodape.pop(0)
    while rodape and not rodape[-1].strip():
        rodape.pop()

    if not rodape:
        return ""

    result = "<br>"
    for line in rodape:
        result += html.escape(line) + "<br>"
    result += "<br>"
    return result


def _plain_info_tema(nome_tema):
    """Lê de base/info.txt apenas os dados estáveis da ficha.

    Os números técnicos passam a vir do rodapé pós-EOF do .ypo,
    para evitar duas fontes contraditórias no Help.
    """
    info = {
        "titulo": str(nome_tema or "").strip(),
        "genero": "",
        "imagem": "",
        "versos": "",
    }

    try:
        with open(os.path.join("./base/" + "info.txt"), "r", encoding="utf-8") as file:
            for line in file:
                if not line.startswith("|"):
                    continue
                pipe = line.split("|")
                if len(pipe) < 10:
                    continue
                if pipe[1].upper() == str(nome_tema).upper():
                    info["titulo"] = pipe[1].strip() or info["titulo"]
                    info["genero"] = pipe[2].strip()
                    info["imagem"] = pipe[3].strip()
                    info["versos"] = pipe[4].strip()
                    break
    except Exception:
        pass

    return info


def _parse_rodape_ypo(nome_tema):
    """Extrai os campos técnicos do rodapé pós-EOF do .ypo."""
    rodape_html = load_rodape_ypo(nome_tema)
    fields = {
        "verbetes_no_texto": "",
        "total_itimos": "",
        "total_verbetes": "",
        "qtd_variacoes": "",
        "qtd_variacoes_numero": "",
    }
    if not rodape_html:
        return fields

    # O rodapé já vem escapado para HTML; desfazemos só para ler os pares chave=valor.
    plain = html.unescape(rodape_html.replace("<br>", "\n"))
    for raw_line in plain.splitlines():
        line = raw_line.strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key_norm = key.strip().casefold()
        value = value.strip()

        if key_norm == "verbetes no texto":
            fields["verbetes_no_texto"] = value
        elif key_norm == "total de ítimos" or key_norm == "total de itimos":
            fields["total_itimos"] = value
        elif key_norm == "total de verbetes":
            fields["total_verbetes"] = value
        elif key_norm == "qtd. de variações" or key_norm == "qtd. de variacoes":
            fields["qtd_variacoes"] = value
            fields["qtd_variacoes_numero"] = value.split("(", 1)[0].strip()

    return fields


def _notacao_cientifica(valor):
    """Gera notação científica curta a partir de número formatado em pt-BR."""
    digits = re.sub(r"\D", "", str(valor or ""))
    if not digits:
        return ""
    try:
        return f"{int(digits):.2e}"
    except Exception:
        return ""


def load_help_ficha_tecnica_tema(nome_tema):
    """Monta uma única ficha técnica coerente para o Help yPoemas.

    Regra: dados técnicos vêm do rodapé limpo pós-EOF.
    O bloco antigo de info.txt não é exibido inteiro para não duplicar
    """
    info = _plain_info_tema(nome_tema)
    rodape = _parse_rodape_ypo(nome_tema)

    result = ""
    result += "Título: " + html.escape(info.get("titulo", "")) + "<br>"

    if info.get("genero"):
        result += "Gênero: " + html.escape(info["genero"]) + "  <br>"
    if info.get("imagem"):
        result += "Imagem: " + html.escape(info["imagem"]) + "  <br>"
    if info.get("versos"):
        result += "Versos: " + html.escape(info["versos"]) + "  <br>"

    if rodape.get("verbetes_no_texto"):
        result += "Verbetes no Texto: " + html.escape(rodape["verbetes_no_texto"]) + "  <br>"
    if rodape.get("total_itimos"):
        result += "Banco de Ítimos: " + html.escape(rodape["total_itimos"]) + "  <br>"
    if rodape.get("total_verbetes"):
        result += "Total de Verbetes: " + html.escape(rodape["total_verbetes"]) + "  <br>"
    if rodape.get("qtd_variacoes"):
        result += "Qtd. de Variações: " + html.escape(rodape["qtd_variacoes"]) + "  <br>"
        cientifica = _notacao_cientifica(rodape.get("qtd_variacoes_numero"))
        if cientifica:
            result += "Notação Científica: " + html.escape(cientifica) + "  <br>"

    # Fallback: se ainda não houver rodapé pós-EOF, mostra a ficha histórica.
    # Assim o Help não fica vazio enquanto o tema ainda não tiver rodapé atualizado.
    if not any(rodape.values()):
        historica = load_info(nome_tema)
        if historica:
            return historica

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


def _pip_line_to_text(line):
    """Converte uma linha .Pip em texto de leitura.

    Regra Off-Machina:
    - cada pipe | vira quebra de linha;
    - dois pipes || geram uma linha em branco;
    - pipes de borda só delimitam o registro e não viram linha vazia extra.
    """
    texto = str(line or "").rstrip("\n")
    if texto.startswith("|"):
        texto = texto[1:]
    if texto.endswith("|"):
        texto = texto[:-1]
    return _trim_blank_edges_preservando_recuo(texto.split("|"))


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


def _markdown_links_to_html(texto):
    """Preserva links markdown [texto](url) dentro do HTML seguro do Off-Machina."""
    texto = str(texto or "")
    pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    out = []
    pos = 0
    for match in pattern.finditer(texto):
        out.append(html.escape(texto[pos:match.start()]))
        label = html.escape(match.group(1).strip())
        url = match.group(2).strip()
        safe_url = html.escape(url, quote=True)
        if re.match(r"^(https?://|mailto:)", url, flags=re.IGNORECASE):
            out.append(
                f'<a href="{safe_url}" target="_blank" rel="noopener noreferrer">{label}</a>'
            )
        else:
            out.append(html.escape(match.group(0)))
        pos = match.end()
    out.append(html.escape(texto[pos:]))
    return "".join(out)


def _off_machina_css():
    """CSS próprio do Off-Machina: obedece fonte/corpo do leitor."""
    stage_font = _fonte_palco_leitor()
    stage_size = _corpo_palco_leitor()
    return f"""
        <style>
        .machina-off-text,
        .machina-off-text p,
        .machina-off-text div,
        .machina-off-text span {{
            font-family: '{stage_font}' !important;
            font-size: {stage_size}px !important;
            line-height: 1.35 !important;
            color: #000000 !important;
            text-align: left !important;
            font-weight: 600 !important;
        }}
        .machina-off-text .machina-off-title {{
            display: block !important;
            text-align: center !important;
            font-weight: 700 !important;
            text-decoration: underline !important;
            text-underline-offset: 0.18em !important;
            margin: 0.08rem auto 0.88rem auto !important;
            line-height: 1.28 !important;
        }}
        .machina-off-text {{
            display: block !important;
            width: fit-content !important;
            max-width: min(96ch, 94%) !important;
            margin-left: auto !important;
            margin-right: auto !important;
            box-sizing: border-box !important;
            padding-left: 8px !important;
            padding-right: 8px !important;
            text-align: left !important;
        }}
        </style>
    """


def _off_machina_html(LOGO_TEXTO):
    """HTML seguro do Off-Machina preservando quebras e links Markdown."""
    texto = _off_machina_texto_limpo(LOGO_TEXTO)
    linhas = texto.splitlines()
    while linhas and not linhas[0].strip():
        linhas.pop(0)
    if linhas:
        titulo = linhas[0].strip()
        corpo = _trim_blank_edges_preservando_recuo(linhas[1:])
        safe_title = _markdown_links_to_html(titulo)
        safe_body = _markdown_links_to_html(corpo).replace("\n", "<br>")
        safe = "<span class='machina-off-title'>" + safe_title + "</span>"
        if safe_body:
            safe += safe_body
    else:
        safe = ""
    return f"{_off_machina_css()}<div class='machina-off-text'>{safe}</div>"


def write_off_machina_texto(LOGO_TEXTO):
    """Renderiza Off-Machina com fonte/corpo próprios, sem cair na classe logo-text."""
    st.markdown(_off_machina_html(LOGO_TEXTO), unsafe_allow_html=True)


def write_livro_vivo_texto(LOGO_TEXTO, LOGO_IMAGE=None):
    """Renderiza livro_vivo com a mesma fonte/corpo do leitor."""
    if LOGO_IMAGE:
        try:
            col_img, col_txt = st.columns([2.5, 7.5])
            with col_img:
                st.image(LOGO_IMAGE, width="stretch")
            with col_txt:
                st.markdown(_off_machina_html(LOGO_TEXTO), unsafe_allow_html=True)
            return
        except Exception:
            # Se a arte falhar, o texto ainda deve aparecer limpo.
            pass

    st.markdown(_off_machina_html(LOGO_TEXTO), unsafe_allow_html=True)


def _analise_texto_cru_do_ypoema(ypoema_html):
    """Converte o yPoema atual para texto simples usado pelas análises."""
    return _ypoema_html_to_text(ypoema_html)


def _analise_linhas_validas(texto):
    """Linhas significativas do yPoema, preservando leitura simples."""
    linhas = []
    for line in str(texto or "").splitlines():
        clean = line.strip()
        if clean:
            linhas.append(clean)
    return linhas


def _analise_titulo_e_versos(tema, ypoema_texto):
    """Separa título provável e versos sem alterar o yPoema original."""
    linhas = _analise_linhas_validas(ypoema_texto)
    tema_limpo = str(tema or "").strip()

    if linhas and linhas[0].casefold() == tema_limpo.casefold():
        return tema_limpo, linhas[1:]

    return tema_limpo, linhas


def _analise_primeiro_verso(versos):
    if versos:
        return versos[0]
    return ""


def _analise_ultimo_verso(versos):
    if versos:
        return versos[-1]
    return ""


def limpar_analise(texto):
    """Normaliza espaços da análise sem achatar parágrafos."""
    linhas = []
    for line in str(texto or "").replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        linhas.append(re.sub(r"[ \t]+", " ", line).strip())

    while linhas and not linhas[0]:
        linhas.pop(0)
    while linhas and not linhas[-1]:
        linhas.pop()

    return "\n".join(linhas)


def gerar_analise_ola(tipo, tema, ypoema_texto):
    """Ponte para a OLA real, quando disponível no ambiente."""
    if _gerar_analise_ola_real is None:
        return "OLA ainda não conectada. Arquivo ponte_ola_openai.py não encontrado ou não importável."

    return limpar_analise(_gerar_analise_ola_real(tipo, tema, ypoema_texto))


def gerar_analise_cia(tipo, tema, ypoema_texto):
    """Rotina pura da CIA, alinhada à oficina local."""
    tipo = str(tipo or "Sintática").strip()
    tema = str(tema or "").strip()
    titulo, versos = _analise_titulo_e_versos(tema, ypoema_texto)
    primeiro = _analise_primeiro_verso(versos)
    ultimo = _analise_ultimo_verso(versos)
    total = len(versos)

    if tipo == "Semântica":
        texto = (
            f'A CIA lê "{titulo}" pelo campo de sentidos que a variação acende. '
            f'O texto parte de "{primeiro}" e deixa que as imagens se aproximem sem obrigar uma única interpretação.\n\n'
            "A força semântica está na abertura: cada verso desloca o anterior e prepara outra possibilidade de leitura. "
            f'O fecho "{ultimo}" não encerra o sentido; apenas entrega ao leitor a última inflexão do percurso.'
        )
    else:
        texto = (
            f'A CIA lê "{titulo}" pela construção da linguagem. A variação tem {total} linhas de leitura, e sua força aparece nos cortes, '
            "nas pausas e na ordem em que as imagens se encadeiam.\n\n"
            f'O primeiro apoio sintático vem de "{primeiro}". A partir dele, o yPoema organiza uma respiração própria: não explica demais, '
            "não fecha cedo, e deixa a frase trabalhar como passagem para o leitor."
        )

    return limpar_analise(texto)


def gerar_analise_atual(ypoema_html, tema):
    """Seleciona CIA ou OLA conforme a sidebar e devolve texto de análise."""
    voice = str(st.session_state.get("analysis_voice", "CIA")).upper()
    kind = st.session_state.get("analysis_kind", "Sintática")
    ypoema_texto = _analise_texto_cru_do_ypoema(ypoema_html)

    if voice == "OLA":
        return gerar_analise_ola(kind, tema, ypoema_texto)

    return gerar_analise_cia(kind, tema, ypoema_texto)


def _analysis_voice_title(voice):
    """Nome expandido da voz de análise no cabeçalho do palco."""
    voice = str(voice or "CIA").upper()
    if voice == "OLA":
        return "Onda Leitora Analítica"
    return "Centro Imaginativo Aplicado"


def _analysis_kind_label(kind):
    """Tipo da análise em caixa baixa para o subtítulo."""
    return str(kind or "").strip().casefold()


def render_analise_palco(texto):
    """Renderiza análise no palco direito, com cabeçalho padrão."""
    stage_font = _fonte_palco_leitor()
    stage_size = max(14, min(30, int(st.session_state.get("stage_size", 21)) - 1))

    voice = str(st.session_state.get("analysis_voice", "CIA")).upper()
    kind = st.session_state.get("analysis_kind", "")
    titulo = _analysis_voice_title(voice)
    subtitulo = _analysis_kind_label(kind)

    safe_text = html.escape(str(texto or "")).replace("\n", "<br>")
    safe_title = html.escape(titulo)
    safe_subtitle = html.escape(subtitulo)

    st.markdown(
        f"""
        <div class="machina-analise-palco" style="
            display:block;
            width:fit-content;
            max-width:min(72ch, 96%);
            margin:0 auto;
            padding:0.20rem 0.45rem 0.35rem 0.45rem;
            box-sizing:border-box;
            text-align:left;
            font-family:'{stage_font}', system-ui, sans-serif;
            font-size:{stage_size}px;
            line-height:1.42;
            color:#000000;
            font-weight:500;
        ">
            <div style="
                text-align:center;
                font-weight:650;
                margin:0 0 0.10rem 0;
                line-height:1.22;
            ">{safe_title}</div>
            <div style="
                text-align:center;
                font-weight:500;
                opacity:0.88;
                margin:0 0 0.75rem 0;
                line-height:1.22;
            ">( {safe_subtitle} )</div>
            <div>{safe_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
                text-align:center;
                white-space:nowrap;">
                copiar
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
                        btn_{token}.innerText = ok ? "copiado" : "copiar";
                    }} catch (e2) {{
                        btn_{token}.innerText = "copiar";
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
    - About: imagem própria da página.
    """
    if str(st.session_state.get("analysis_voice", "Machina")).upper() in {"CIA", "OLA"}:
        return

    if not bool(st.session_state.get("draw", True)):
        return

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
        page_image = PAGE_IMAGES.get("5", "")
        if page_image:
            image_path = os.path.join("./images", page_image)

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


def _clean_audio_text(text):
    """Remove marcas HTML simples antes da geracao de audio."""
    return str(text or "").replace("<br>", " ").replace("< br>", "").replace("<br >", "").replace("<br/>", " ")


@st.cache_data(show_spinner=False)
def _audio_bytes_edge_tts(text_clean, lang):
    """Gera audio uma vez por texto/idioma e reaproveita nos reruns."""
    selected_voice = VOICES_EDGE_TTS.get(lang, "pt-BR-AntonioNeural")

    async def generate_audio():
        communicate = edge_tts.Communicate(text_clean, selected_voice)
        audio_bytes = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes += chunk["data"]
        return audio_bytes

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(generate_audio())


def talk(text):
    """Le o yPoema no idioma atual usando edge-tts, quando disponivel."""
    if edge_tts is None:
        st.warning("Motor de voz neural indisponivel.")
        return

    try:
        audio_output = _audio_bytes_edge_tts(_clean_audio_text(text), st.session_state.lang)
        st.audio(audio_output, format="audio/mp3")
    except Exception as e:
        st.error(f"Erro na voz neural: {e}")


def render_voz_slot(initial_text="Machina."):
    """Reserva a linha do player de voz logo abaixo dos nav_buttons."""
    voz_left, voz_mid, voz_right = st.columns([0.1, 9.8, 0.1])
    with voz_mid:
        slot = st.empty()
        with slot:
            talk(initial_text)
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

    help_tips = load_help(st.session_state.lang)
    help_last = help_tips[0]
    help_rand = help_tips[1]
    help_nest = help_tips[2]
    help_more = help_tips[4]
    help_talk = help_tips[6]
    help_auto = help_tips[7]
    help_manual = help_tips[8]

    mini_left, mini_nav, mini_right = st.columns([3, 4, 3])
    with mini_nav:
        nav_cols = st.columns([1, 1, 1, 1, 1, 1, 1])
        more = nav_cols[0].button(BOTOES_MOBILE["mais_uma_versao"], key="mini_more", help=help_more, width="stretch")
        last = nav_cols[1].button(BOTOES_MOBILE["tema_anterior"], key="mini_last", help=help_last, width="stretch")
        rand = nav_cols[2].button(BOTOES_MOBILE["tema_ao_acaso"], key="mini_rand", help=help_rand, width="stretch")
        nest = nav_cols[3].button(BOTOES_MOBILE["proximo_tema"], key="mini_nest", help=help_nest, width="stretch")
        mini_voz = nav_cols[4].button(BOTOES_MOBILE["voz"], key="mini_voz", help=help_talk, width="stretch")
        auto = nav_cols[5].button(BOTOES_MOBILE["automatico"], key="mini_auto", help=help_auto, width="stretch")
        manu = nav_cols[6].button(BOTOES_MOBILE["help"], key="mini_help", help=help_manual, width="stretch")

    mini_player_left, mini_player, mini_player_right = st.columns([3, 4, 3])
    with mini_player:
        mini_voz_slot = render_voz_slot()

    if auto:
        st.session_state.auto = not st.session_state.auto

    if st.session_state.auto:
        with st.sidebar:
            wait_time = st.slider(translate("tempo de exibição (em segundos): "), 5, 60)

    if last:
        st.session_state.rand = False
        st.session_state.mini -= 1
        if st.session_state.mini < 0:
            st.session_state.mini = maxy_mini - 1

    if rand:
        st.session_state.rand = True
        st.session_state.mini = random.randrange(0, maxy_mini)
    else:
        st.session_state.rand = False

    if nest:
        st.session_state.rand = False
        st.session_state.mini += 1
        if st.session_state.mini >= maxy_mini:
            st.session_state.mini = 0

    if more:
        st.session_state.rand = False

    st.session_state.tema = temas_list[st.session_state.mini]

    lnew = not manu
    if manu:
        st.subheader(load_md_file("MANUAL_MINI.md"))
    if lnew or st.session_state.auto:
        if st.session_state.rand:
            st.session_state.mini = random.randrange(0, maxy_mini)
            st.session_state.tema = temas_list[st.session_state.mini]

        mini_focus_key = "|".join([
            "mini",
            str(st.session_state.get("mini", "")),
            str(st.session_state.get("tema", "")),
            str(st.session_state.get("lang", "")),
        ])
        mini_keep_focus = (
            not st.session_state.auto
            and not any([more, last, rand, nest])
            and _has_focus("mini", mini_focus_key)
        )

        if mini_keep_focus:
            curr_ypoema = st.session_state.get("mini_focus_text", "")
        elif st.session_state.lang != st.session_state.last_lang:
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

        _remember_focus("mini", mini_focus_key, curr_ypoema)
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

                if mini_voz:
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

    help_tips = load_help(st.session_state.lang)
    help_last = help_tips[0]
    help_rand = help_tips[1]
    help_nest = help_tips[2]
    help_talk = help_tips[6]
    help_manual = help_tips[8]
    help_more = help_tips[4]

    try:
        nav_left, col_nav, nav_right = st.columns([3, 4, 3], vertical_alignment="bottom")
        col_livros, col_player, col_temas = st.columns([3, 4, 3], vertical_alignment="bottom")
        machina_nav_needs_spacer = False
    except TypeError:
        nav_left, col_nav, nav_right = st.columns([3, 4, 3])
        col_livros, col_player, col_temas = st.columns([3, 4, 3])
        machina_nav_needs_spacer = True

    with col_nav:
        if machina_nav_needs_spacer:
            st.markdown(
                "<div style='height:0.12rem; min-height:0.12rem;'></div>",
                unsafe_allow_html=True,
            )
        nav_cols = st.columns([1, 1, 1, 1, 1, 1])
        more = nav_cols[0].button(BOTOES_MOBILE["mais_uma_versao"], key="ypoema_more", help=help_more, width="stretch")
        last = nav_cols[1].button(BOTOES_MOBILE["tema_anterior"], key="ypoema_last", help=help_last, width="stretch")
        rand = nav_cols[2].button(BOTOES_MOBILE["tema_ao_acaso"], key="ypoema_rand", help=help_rand, width="stretch")
        nest = nav_cols[3].button(BOTOES_MOBILE["proximo_tema"], key="ypoema_nest", help=help_nest, width="stretch")
        ypoema_voz = nav_cols[4].button(BOTOES_MOBILE["voz"], key="ypoema_voz", help=help_talk, width="stretch")
        manu = nav_cols[5].button(BOTOES_MOBILE["help"], key="ypoema_help", help=help_manual, width="stretch")

    with col_livros:
        pick_book_palco()

    with col_player:
        ypoemas_voz_slot = render_voz_slot()

    with col_temas:
        pick_tema_palco("↓ " + str(len(temas_list)))

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
            LOGO_TEXTO = load_md_file("MANUAL_YPOEMAS.md")
            st.markdown(LOGO_TEXTO)

            LOGO_IMAGE = (
                "./images/matrix/" + st.session_state.tema.capitalize() + ".jpg"
            )

            LOGO_INFO = load_info(st.session_state.tema)
            if st.session_state.lang != "pt":  # translate if idioma <> pt
                LOGO_INFO = translate(LOGO_INFO)

            st.markdown("<br>", unsafe_allow_html=True)
            col_matrix, col_info = st.columns([3, 7])
            with col_matrix:
                st.image(LOGO_IMAGE, width="stretch")
            with col_info:
                st.markdown(LOGO_INFO, unsafe_allow_html=True)

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
            focus_key = _ypo_focus_key()
            keep_focus = (
                not any([more, last, rand, nest])
                and st.session_state.get("ypo_focus_key", "") == focus_key
                and bool(st.session_state.get("ypo_focus_text", ""))
            )

            if keep_focus:
                curr_ypoema = st.session_state.get("ypo_focus_text", "")
            elif st.session_state.lang != st.session_state.last_lang:
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

            _remember_focus("ypo", focus_key, curr_ypoema)
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

            analysis_voice_atual = str(st.session_state.get("analysis_voice", "Machina")).upper()

            if analysis_voice_atual in {"CIA", "OLA"}:
                analise_texto = gerar_analise_atual(LOGO_TEXTO, st.session_state.tema)

                col_poema, col_analise = st.columns([1.05, 0.95], gap="large")
                with col_poema:
                    write_ypoema(LOGO_TEXTO, None)
                with col_analise:
                    render_analise_palco(analise_texto)
            else:
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
            # antes: [ variações ] [ qtd ]; depois: [ qtd ] [ copiar ]
            pacote_pronto = bool(copy_bundle_text)
            copy_submit = False

            if pacote_pronto:
                copy_left, copy_qtd_col, copy_all_col, copy_right = st.columns([3.80, 1.00, 2.20, 3.80])
            else:
                copy_left, copy_variacoes_col, copy_qtd_col, copy_right = st.columns([2.95, 2.45, 1.00, 2.95])
                with copy_variacoes_col:
                    copy_submit = st.button(
                        "variações",
                        key="copy_variacoes_btn",
                        width="stretch",
                    )

            with copy_qtd_col:
                qtd_options = list(range(9, 1, -1))
                qtd_copias = st.selectbox(
                    "quantidade de cópias",
                    qtd_options,
                    index=qtd_options.index(qtd_copias_atual),
                    key="copy_qtd_widget",
                    label_visibility="collapsed",
                    on_change=_on_copy_qtd_change,
                )

            qtd_copias = _normalizar_qtd_copias(qtd_copias)
            st.session_state["copy_qtd"] = qtd_copias

            st.session_state.pop("copy_qtd_changed", None)
            copy_submit = bool(copy_submit)

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

            # O botão "copiar" só aparece quando há pacote real na área de cópias.
            # Novo tema ou nova geração recriam o token e o texto volta para "copiar".
            if copy_bundle_text:
                if not pacote_pronto:
                    copy_now_left, copy_all_col, copy_now_right = st.columns([4.25, 2.15, 4.25])
                with copy_all_col:
                    render_copy_bundle_button(
                        copy_bundle_text,
                        int(st.session_state.get("copy_bundle_token", 0)),
                    )

            render_copy_bundle_widget(
                copy_bundle_text,
                int(st.session_state.get("copy_bundle_token", 0)),
                st.session_state.get("copy_bundle_qtd", None),
            )


        if ypoema_voz:
            with ypoemas_voz_slot:
                talk(curr_ypoema)


def page_eureka():
    help_tips = load_help(st.session_state.lang)
    help_rand = help_tips[1]
    help_more = help_tips[4]
    help_talk = help_tips[6]
    help_manual = help_tips[8]

    try:
        col_busca, col_nav, col_ocorrencias = st.columns(
            [3, 4, 3],
            vertical_alignment="bottom",
        )
        eureka_nav_needs_spacer = False
    except TypeError:
        col_busca, col_nav, col_ocorrencias = st.columns([3, 4, 3])
        eureka_nav_needs_spacer = True

    with col_busca:
        eureka_info_slot = st.empty()
        find_what = st.text_input(
            label=translate("buscar..."),
            help=translate("digite uma palavra - ou parte dela - que você goste..."),
        )
        components.html(
            """
            <script>
            window.addEventListener("keydown", function(event) {
              if (event.key === "Enter" && document.activeElement) {
                setTimeout(function(){ document.activeElement.blur(); }, 40);
              }
            }, true);
            </script>
            """,
            height=0,
        )

    with col_nav:
        if eureka_nav_needs_spacer:
            st.markdown(
                "<div style='height:1.95rem; min-height:1.95rem;'></div>",
                unsafe_allow_html=True,
            )

        nav_cols = st.columns([1, 1, 1, 1])
        more = nav_cols[0].button(BOTOES_MOBILE["mais_uma_versao"], help=help_more, width="stretch")
        rand = nav_cols[1].button(BOTOES_MOBILE["tema_ao_acaso"], help=help_rand, width="stretch")
        eureka_voz = nav_cols[2].button(BOTOES_MOBILE["voz"], key="eureka_voz_btn", help=help_talk, width="stretch")
        manu = nav_cols[3].button(BOTOES_MOBILE["help"], help=help_manual, width="stretch")

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

        if find_what != st.session_state.get("eureka_last_find", ""):
            st.session_state.eureka = 0
            st.session_state["eureka_last_find"] = find_what

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
            info_find = (
                "💡 "
                + str(len(seed_list))
                + ' "'
                + find_what
                + '" em '
                + str(len(soma_tema))
                + " temas"
            )
            with eureka_info_slot:
                st.markdown(
                    "<div style='text-align:left; font-weight:600; margin-bottom:0.12rem;'>"
                    + html.escape(info_find)
                    + "</div>",
                    unsafe_allow_html=True,
                )

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

            with col_ocorrencias:
                options = list(range(len(seed_list)))
                opt_ocur = st.selectbox(
                    str(len(seed_list)) + " ↓",
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

            eureka_focus_key = "|".join([
                "eureka",
                str(find_what),
                str(st.session_state.get("eureka", "")),
                str(this_seed),
                str(seed_tema),
                str(st.session_state.get("lang", "")),
            ])
            eureka_keep_focus = (
                not any([more, rand])
                and not manu
                and _has_focus("eureka", eureka_focus_key)
            )

            if eureka_keep_focus:
                curr_ypoema = st.session_state.get("eureka_focus_text", "")
            elif st.session_state.lang != st.session_state.last_lang:
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

            _remember_focus("eureka", eureka_focus_key, curr_ypoema)
            lnew = True
            if lnew:
                eureka_expander = st.expander("", expanded=True)
                with eureka_expander:
                    LOGO_TEXTO = curr_ypoema
                    _set_sidebar_context_image_for_theme(seed_tema)

                    write_ypoema(LOGO_TEXTO, None)
                    update_readings(seed_tema)

                if eureka_voz:
                    with eureka_voz_slot:
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
    nav_changed = False
    off_books_list = load_all_offs()
    if not off_books_list:
        st.warning(translate("nenhum livro off-machina encontrado"))
        return

    if st.session_state.off_book < 0 or st.session_state.off_book >= len(off_books_list):
        st.session_state.off_book = 0
    if st.session_state.off_take < 0:
        st.session_state.off_take = 0

    off_book_name = off_books_list[st.session_state.off_book]
    this_off_book = load_off_book(off_book_name)
    off_book_pagys = load_book_pages(this_off_book)

    try:
        nav_left, col_nav, nav_right = st.columns([3, 4, 3], vertical_alignment="bottom")
        col_livros, col_player, col_temas = st.columns([3, 4, 3], vertical_alignment="bottom")
        off_nav_needs_spacer = False
    except TypeError:
        nav_left, col_nav, nav_right = st.columns([3, 4, 3])
        col_livros, col_player, col_temas = st.columns([3, 4, 3])
        off_nav_needs_spacer = True

    with col_nav:
        help_tips = load_help(st.session_state.lang)
        help_last = help_tips[0]
        help_rand = help_tips[1]
        help_nest = help_tips[2]
        help_talk = help_tips[6]
        help_manual = help_tips[8]

        if off_nav_needs_spacer:
            st.markdown(
                "<div style='height:0.12rem; min-height:0.12rem;'></div>",
                unsafe_allow_html=True,
            )
        nav_cols = st.columns([1, 1, 1, 1, 1])
        last = nav_cols[0].button(BOTOES_MOBILE["tema_anterior"], help=help_last, width="stretch")
        rand = nav_cols[1].button(BOTOES_MOBILE["tema_ao_acaso"], help=help_rand, width="stretch")
        nest = nav_cols[2].button(BOTOES_MOBILE["proximo_tema"], help=help_nest, width="stretch")
        off_voz = nav_cols[3].button(BOTOES_MOBILE["voz"], help=help_talk, key="off_voz_btn", width="stretch")
        manu = nav_cols[4].button(BOTOES_MOBILE["help"], help=help_manual, width="stretch")

    with col_livros:
        options = list(range(len(off_books_list)))
        opt_off_book = st.selectbox(
            str(len(off_books_list)) + " ↓",
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

    with col_player:
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
        opt_off_take_key = "opt_off_take_" + str(
            int(st.session_state.get("off_take_widget_token", 0))
        )
        opt_off_take = st.selectbox(
            "↓ " + str(len(off_book_pagys)),
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
        render_manual_off_machina()

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
            off_focus_key = "|".join([
                "off",
                str(off_book_name),
                str(st.session_state.get("off_take", "")),
                str(st.session_state.get("lang", "")),
            ])
            off_keep_focus = (
                not any([last, rand, nest])
                and not manu
                and _has_focus("off", off_focus_key)
            )
            if off_book_name == "livro_vivo" and "@ " in pipe_line[1]:
                if off_keep_focus:
                    off_book_text = st.session_state.get("off_focus_text", "")
                elif st.session_state.lang != st.session_state.last_lang:
                    off_book_text = load_lypo()  # changes in lang, keep LYPO
                else:
                    nome_tema = pipe_line[1].replace("@ ", "")
                    off_book_text = load_poema(nome_tema, "")  # no seed_eureka
                    off_book_text = "<br>" + load_lypo()
            else:
                off_book_text = _pip_line_to_text(this_off_book[st.session_state.off_take])

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
                    if off_book_name == "livro_vivo":
                        write_off_machina_texto(off_book_text)
                    else:
                        write_off_machina_texto(off_book_text)
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

            _remember_focus("off", off_focus_key, off_book_text)

        if off_voz:
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


### eof: pages


SIDEBAR_FILHOTE_WIDTH_PX = 64
CIA_ANALYSIS_OPTIONS = [
    "Sintática",
    "Semântica",
]

OLA_ANALYSIS_OPTIONS = [
    "Sintética",
    "Sintática",
    "Aparição",
    "Completa",
]


def _analysis_options_for_voice(voice):
    """Retorna a lista de análises da voz escolhida."""
    if str(voice or "").upper() == "OLA":
        return OLA_ANALYSIS_OPTIONS
    return CIA_ANALYSIS_OPTIONS


def _set_analysis_voice(voice):
    """Seleciona Machina/CIA/OLA e ajusta a lista única."""
    voice_raw = str(voice or "Machina").strip()
    voice_key = voice_raw.upper()

    if voice_key == "MACHINA":
        st.session_state["analysis_voice"] = "Machina"
        return

    if voice_key not in {"CIA", "OLA"}:
        voice_key = "CIA"

    st.session_state["analysis_voice"] = voice_key
    options = _analysis_options_for_voice(voice_key)

    if options:
        st.session_state["analysis_kind"] = options[0]
    else:
        st.session_state["analysis_kind"] = ""


def render_analysis_sidebar_block():
    """Bloco centralizado: CIA / Machina / OLA, com lista só nas análises."""
    current_voice = str(st.session_state.get("analysis_voice", "Machina"))
    current_key = current_voice.upper()
    if current_key not in {"MACHINA", "CIA", "OLA"}:
        current_voice = "Machina"
        current_key = "MACHINA"
        st.session_state["analysis_voice"] = current_voice

    options = [] if current_key == "MACHINA" else _analysis_options_for_voice(current_key)
    current_kind = st.session_state.get("analysis_kind", options[0] if options else "")
    if options and current_kind not in options:
        current_kind = options[0]
        st.session_state["analysis_kind"] = current_kind

    st.sidebar.markdown("<div style='height:1.85rem;'></div>", unsafe_allow_html=True)

    col_cia, col_machina, col_ola = st.sidebar.columns([2.5, 5, 2.5])

    with col_cia:
        if st.button(
            "CIA",
            key="analysis_voice_cia_btn",
            width="stretch",
            type="primary" if current_key == "CIA" else "secondary",
        ):
            _set_analysis_voice("CIA")
            st.rerun()

    with col_machina:
        if st.button(
            "MACHINA",
            key="analysis_voice_machina_btn",
            width="stretch",
            type="primary" if current_key == "MACHINA" else "secondary",
        ):
            _set_analysis_voice("Machina")
            st.rerun()

    with col_ola:
        if st.button(
            "OLA",
            key="analysis_voice_ola_btn",
            width="stretch",
            type="primary" if current_key == "OLA" else "secondary",
        ):
            _set_analysis_voice("OLA")
            st.rerun()

    if options:
        st.sidebar.markdown(
            "<div style='height:1.42rem;'></div>",
            unsafe_allow_html=True,
        )
        choice = st.sidebar.selectbox(
            "tipo",
            options,
            index=options.index(current_kind) if current_kind in options else 0,
            key="analysis_kind_select",
            label_visibility="collapsed",
        )
        st.session_state["analysis_kind"] = choice


def render_sidebar_for_page(chosen_id):
    """Renderiza os controles fixos do leitor."""
    pick_lang()
    pick_stage_font()
    render_analysis_sidebar_block()



def _set_machina_page(page_label, page_id):
    """Fixa a página ativa em estado explícito.

    Evita que cliques internos de uma página, especialmente a navegação
    da Off-Machina, caiam de volta no foco inicial yPoemas.
    """
    previous_id = str(st.session_state.get("machina_page_id", "")).strip()
    if previous_id == "2" and str(page_id) != "2":
        limpar_copias_palco()
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

    _set_machina_page("ypoema", page_ids["ypoema"])


def main():
    gramado = open_gramado()

    with gramado:
        page_labels = ["mini", "ypoema", "eureka", "off-mach", "about"]
        page_ids = {
            "mini": "1",
            "ypoema": "2",
            "eureka": "3",
            "off-mach": "4",
            "about": "5",
        }

        _sync_machina_page_state(page_labels, page_ids)

        try:
            page_row = st.container(
                horizontal=True,
                horizontal_alignment="center",
                vertical_alignment="center",
                gap="small",
            )
        except TypeError:
            page_row = st.container()

        with page_row:
            page_display = {"ypoema": "yPoemas", "off-mach": "OFF"}
            for page_label in page_labels:
                display_label = page_display.get(page_label, page_label)
                st.button(
                    display_label,
                    key=f"machina_page_btn_{page_label}",
                    help=page_label,
                    type="primary" if page_label == st.session_state["machina_page_select"] else "secondary",
                    width="stretch",
                    on_click=_set_machina_page,
                    args=(page_label, page_ids[page_label]),
                )

        chosen_label = st.session_state["machina_page_select"]
        chosen_id = st.session_state.get("machina_page_id", page_ids.get(chosen_label, "2"))

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
