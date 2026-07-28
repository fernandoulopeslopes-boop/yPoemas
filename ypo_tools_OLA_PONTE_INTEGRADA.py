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

APP_BUILD = "2026-07-01_atualizar_rodape_ypo_EOF"
APP_BUILD_NOTES = "CIA local: atualiza rodapé informativo dos .ypo sob demanda; update_tema/novo_tema atualizam o tema afetado."

from lay_2_ypo import gera_poema
from readings import (
    list_readings,
    update_readings,
    update_visy,
)

try:
    from ponte_ola_openai import gerar_analise_ola as _gerar_analise_ola_real
except Exception:
    _gerar_analise_ola_real = None


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
    "icones",
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
    "icones": ["ABOUT_icones.md"],
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
    page_title="a Machina de fazer Poesia - Análises",
    page_icon=":cyclone:",
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
            max-width: 320px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        .machina-sidebar-image-frame {
            width: 320px !important;
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

        # análise :: Machina / CIA / OLA
        "analysis_voice": "Machina",
        "analysis_kind": "Sintática",
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
    returns.append("")  # posição histórica removida: antigo botão arte
    returns.append(translate("voz"))

    return returns


def draw_check_buttons():
    """Botão arte removido: a sidebar já mostra/oculta a arte pela lógica de contexto."""
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



def render_help_pacote_centralizado(texto, key="help_pacote"):
    """Centraliza o pacote HELP mantendo cada item em linha própria.

    Importante: não usar <pre> aqui. Em alguns temas/versões do Streamlit,
    CSS global pode achatar o bloco visualmente. Renderizamos linha a linha
    dentro de um pacote centralizado, preservando o alinhamento interno.
    """
    linhas_html = []
    for line in str(texto or "").splitlines():
        # Help não deve carregar rodapé/copyright dentro do pacote de uso.
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

def _manual_ypoemas_texto():
    """Manual padrão da página yPoemas.

    Mantido no código para não depender do .md durante estes ajustes finos
    de Help. A Ficha Técnica/Matrix entram depois deste bloco.
    """
    return """yPoemas: modo de usar
___
Selecione um livro na lista de Livros
___
- ✚ = Gera um novo texto para o tema
- ◀ = Move para o tema anterior
- ✻ = Escolhe um tema aleatoriamente
- ▶ = Move para o próximo tema
♫ ouvir a leitura do texto
- ? = Modo de Usar & Manual do Usuário
___
Selecione um tema na lista de Temas
___
No navegador Google Chrome:
- Use as setas Ctrl + ou Ctrl -  para aumentar ou diminuir o tamanho da tela.
- Você pode usar Ctrl C e Ctrl V  para copiar e colar textos da tela.
- Use o botão direito do mouse para salvar um texto
  ou para pesquisar a palavra selecionada no Google.

- Para buscar palavras de sua escolha use a página eureka do menu.
___"""


def render_help_ypoemas_mesma_fonte():
    """Renderiza o Help yPoemas no padrão visual centralizado."""
    render_help_pacote_centralizado(_manual_ypoemas_texto(), key="help_ypoemas")


def _matrix_image_for_theme(nome_tema):
    """Localiza o gráfico Matrix do tema sem depender só de .capitalize()."""
    tema = str(nome_tema or "").strip()
    if not tema:
        return None

    matrix_dir = _project_path("images", "matrix")
    candidates = [
        os.path.join(matrix_dir, tema + ".jpg"),
        os.path.join(matrix_dir, tema + ".JPG"),
        os.path.join(matrix_dir, tema.capitalize() + ".jpg"),
        os.path.join(matrix_dir, tema.capitalize() + ".JPG"),
    ]

    # Fallback robusto: compara nome sem acento/caixa/pontuação.
    if os.path.isdir(matrix_dir):
        tema_key = _md_nome_chave(tema)
        for real_name in os.listdir(matrix_dir):
            if not real_name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                continue
            base = os.path.splitext(real_name)[0]
            if _md_nome_chave(base) == tema_key:
                candidates.append(os.path.join(matrix_dir, real_name))

    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    return None


def _formatar_milhar_ptbr(valor):
    """Formata inteiros com ponto de milhar, preservando textos comuns."""
    valor = str(valor or "").strip()
    if not valor.isdigit():
        return valor
    try:
        return f"{int(valor):,}".replace(",", ".")
    except Exception:
        return valor


def _formatar_linha_info_ptbr(linha):
    """Aplica ponto de milhar nos campos numéricos da Ficha Técnica."""
    linha = str(linha or "").strip()
    if ":" not in linha:
        return linha
    chave, valor = linha.split(":", 1)
    valor_limpo = valor.strip()
    if valor_limpo.isdigit():
        return f"{chave}: {_formatar_milhar_ptbr(valor_limpo)}"
    return linha


def _limpar_info_html_para_linhas(info_text):
    """Converte o load_info() antigo em linhas simples de Ficha Técnica."""
    texto = str(info_text or "")
    texto = texto.replace("<br/>", "\n").replace("<br />", "\n").replace("<br>", "\n")
    texto = re.sub(r"<[^>]+>", "", texto)
    texto = html.unescape(texto)
    linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
    return [_formatar_linha_info_ptbr(linha) for linha in linhas]

def render_matrix_ficha_tecnica_ypoemas(tema):
    """Mostra Matrix à esquerda e Ficha Técnica à direita, sem vazar HTML/base64."""
    tema = str(tema or "").strip()
    if not tema:
        return

    info_text = load_info(tema)
    if st.session_state.lang != "pt":
        info_text = translate(info_text)

    linhas_info = _limpar_info_html_para_linhas(info_text)
    matrix_image = _matrix_image_for_theme(tema)

    if linhas_info:
        linhas_html = "".join(
            f"<div class='machina-ficha-line'>{html.escape(linha)}</div>"
            for linha in linhas_info
        )
    else:
        linhas_html = "<div class='machina-ficha-line'>Ficha Técnica não encontrada em base/info.txt.</div>"

    st.markdown("___")
    st.markdown(
        """
        <div style="
            width:100%;
            max-width:860px;
            margin:0.35rem auto 0.65rem auto;
            box-sizing:border-box;
        ">
        """,
        unsafe_allow_html=True,
    )

    col_matrix, col_info = st.columns([1.05, 1.30], gap="large")

    with col_matrix:
        if matrix_image:
            st.image(matrix_image, use_container_width=True)
        else:
            st.markdown(
                "<div style='text-align:center; opacity:0.72; padding:1.2rem 0;'>Matrix não encontrada.</div>",
                unsafe_allow_html=True,
            )

    with col_info:
        st.markdown(
            f"""
            <div class="machina-ficha-tecnica" style="
                width:100%;
                max-width:420px;
                margin:0.10rem auto 0.35rem auto;
                padding:0.15rem 0.10rem;
                text-align:left;
                font-family:'Trebuchet MS', system-ui, sans-serif;
                font-size:0.98rem;
                line-height:1.42;
                box-sizing:border-box;
            ">
                <style>
                .machina-ficha-tecnica .machina-ficha-line {{
                    margin:0 0 0.18rem 0;
                    padding:0;
                }}
                </style>
                {linhas_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("___")

def render_help_ypoemas_com_ficha():
    """Help de yPoemas + Matrix e Ficha Técnica do tema em foco."""
    render_help_ypoemas_mesma_fonte()
    render_matrix_ficha_tecnica_ypoemas(st.session_state.get("tema", ""))


@st.cache_data

def _manual_talk_intro():
    """Linha padrão dos Helps: legenda da voz dentro da lista de botões."""
    return translate("📣 ouvir a leitura do texto")


def _manual_inserir_talk_entre_botoes(raw_text):
    """Insere a legenda da voz entre ▶ e ? no manual dos botões.

    Regra visual pedida:
    - ▶ = Move para o próximo tema
    - ♫ ouvir a leitura do texto
    - ?  = Modo de Usar & Manual do Usuário
    """
    linhas = []
    for line in str(raw_text or "").splitlines():
        if "ouvir a leitura do texto" in line.casefold():
            continue
        linhas.append(line)

    talk_line = _manual_talk_intro()

    # Preferência: inserir imediatamente antes da linha do botão ?.
    for idx, line in enumerate(linhas):
        clean = line.strip()
        if clean.startswith("?") and "=" in clean:
            linhas.insert(idx, talk_line)
            return "\n".join(linhas)

    # Fallback: inserir logo após a linha do botão ▶.
    for idx, line in enumerate(linhas):
        if "▶" in line:
            linhas.insert(idx + 1, talk_line)
            return "\n".join(linhas)

    # Último fallback: não joga no topo; coloca no fim.
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

    # Insere antes da seção dos nav_buttons quando ela existir.
    padrao = re.compile(r"(?im)^(\s*help.*nav_buttons.*|\s*nav_buttons.*)$")
    if padrao.search(manual) and bloco_listas not in manual:
        manual = padrao.sub(bloco_listas + r"\1", manual, count=1)
    elif bloco_listas not in manual:
        manual = bloco_listas + manual

    return manual


def _manual_mini_texto():
    """Manual Mini limpo: mantém a sequência visual dos botões.

    Ordem desejada no Help da página Mini:
    mini: modo de usar / ___ / ✚ / ✻ / 🔀 / ♫ / ?
    """
    manual = load_md_file("MANUAL_MINI.md")
    linhas = []

    for line in str(manual or "").splitlines():
        clean = line.strip()
        clean_fold = clean.casefold()

        # Mini: esta linha deixa o Help poluído e já não entra no manual.
        if "tempo de exibição" in clean_fold or "ajuste o tempo" in clean_fold:
            continue

        # Cabeçalho será inserido de forma padronizada no topo.
        if clean_fold in {"mini: modo de usar", "___"}:
            continue

        # Padrão visual: Help abre e fecha com ___, não com ---.
        if clean == "---":
            line = "___"

        # Remove qualquer sobra antiga da legenda de voz antes de reposicionar.
        if "ouvir a leitura do texto" in clean_fold:
            continue

        # Remove marcação markdown que transformava linhas em H1/H2.
        line = re.sub(r"^\s*#{1,6}\s+", "", line)
        line = line.replace("**", "")

        # Pedido: substituir o marcador antigo/palavra auto por ícone tipo random.
        line = line.replace("☐", "🔀")
        line = re.sub(r"\bauto\b", "🔀", line, flags=re.IGNORECASE)

        linhas.append(line)

    talk_line = _manual_talk_intro()
    help_line = translate("?  Modo de Usar & Manual do Usuário")

    # Remove duplicatas antigas do botão ? para reposicionar no fim do bloco dos botões.
    linhas_sem_help = []
    for line in linhas:
        clean = line.strip()
        if clean.startswith("?") and ("modo de usar" in clean.casefold() or "manual" in clean.casefold()):
            continue
        linhas_sem_help.append(line)
    linhas = linhas_sem_help

    # Regra específica da Mini: bloco dos botões deve ficar:
    # ✚ / ✻ / 🔀 / ♫ / ?
    inserted = False
    for idx, line in enumerate(linhas):
        fold = line.casefold()
        if "exibe temas automaticamente" in fold or line.strip().startswith("🔀"):
            linhas.insert(idx + 1, talk_line)
            linhas.insert(idx + 2, help_line)
            inserted = True
            break

    if not inserted:
        # Fallback: antes do Copyright, nunca depois dele.
        for idx, line in enumerate(linhas):
            if "copyright" in line.casefold():
                linhas.insert(idx, talk_line)
                linhas.insert(idx + 1, help_line)
                inserted = True
                break

    if not inserted:
        linhas.append(talk_line)
        linhas.append(help_line)

    # Cabeçalho padrão do Help da página Mini.
    header = [translate("mini: modo de usar"), "___"]
    return "\n".join(header + linhas)

def render_manual_mini():
    """Help padrão da página Mini."""
    render_help_pacote_centralizado(_manual_mini_texto(), key="help_mini")


def _manual_eureka_texto():
    """Manual padrão da página Eureka em formato de lista avaliável."""
    return """eureka: modo de usar
___
Digite pelo menos 3 letras para buscar uma palavra que você goste...
___
- ✚ = Gera novo texto para o tema
- ✻ = Escolhe uma palavra aleatoriamente
- ♫ ouvir a leitura do texto
- ? = Modo de Usar & Manual do Usuário
___
A lista mostra palavras/verbetes encontrados no léxico da Machina.
___"""


def render_manual_eureka():
    """Help padrão da página Eureka."""
    render_help_pacote_centralizado(_manual_eureka_texto(), key="help_eureka")


def render_manual_off_machina():
    """Help padrão da página Off-Machina."""
    render_help_pacote_centralizado(_manual_inserir_talk_entre_botoes(_manual_off_machina_texto()), key="help_off_machina")

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
        os.path.join("./md_files/ABOUT_INDEX.MD"),
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
    safe = _markdown_links_to_html(texto).replace("\n", "<br>")
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
                st.image(LOGO_IMAGE, use_container_width=True)
            with col_txt:
                st.markdown(_off_machina_html(LOGO_TEXTO), unsafe_allow_html=True)
            return
        except Exception:
            # Se a arte falhar, o texto ainda deve aparecer limpo.
            pass

    st.markdown(_off_machina_html(LOGO_TEXTO), unsafe_allow_html=True)

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
    - About/tools: imagem própria da página.
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

    # Mini :: botões padrão em ordem visual
    # ✚ = nova variação | ✻ = tema ao acaso | 🔀 = automático | ♫ = voz | ? = help
    foo1, more_col, rand_col, auto_col, voz_col, help_col, foo2 = st.columns([2.35, 1.0, 1.0, 1.35, 1.0, 1.0, 2.35])

    help_tips = load_help(st.session_state.lang)
    help_rand = help_tips[1]
    help_more = help_tips[4]
    help_talk = help_tips[6]

    with more_col:
        more = st.button("✚", key="mini_more_btn", help=help_more, use_container_width=True)

    with rand_col:
        rand = st.button("✻", key="mini_rand_btn", help=help_rand, use_container_width=True)

    with auto_col:
        if st.button("🔀", key="mini_auto_button", help="modo automático", use_container_width=True):
            st.session_state.auto = not st.session_state.auto

    with voz_col:
        if st.button("♫", key="mini_voz_btn", help=help_talk, use_container_width=True):
            st.session_state.talk = not st.session_state.talk

    # Pedido: o botão ? deve existir como botão real logo após o ♫.
    with help_col:
        manu = st.button("?", key="mini_help_btn", help="Modo de Usar & Manual do Usuário", use_container_width=True)

    mini_voz_slot = render_voz_slot()

    if st.session_state.auto:
        st.session_state.talk = False
        with st.sidebar:
            wait_time = st.slider(translate("tempo de exibição (em segundos): "), 5, 60, label_visibility="collapsed")

    if rand:
        st.session_state.rand = True
        st.session_state.mini = random.randrange(0, maxy_mini)
    else:
        st.session_state.rand = False

    st.session_state.tema = temas_list[st.session_state.mini]

    if more:
        st.session_state.rand = False

    lnew = not manu
    if manu:
        render_manual_mini()

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
            "🌀  "
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



MAX_ANALISE_CHARS = 900


def limpar_analise(texto, max_chars=MAX_ANALISE_CHARS):
    """Limpa a análise devolvida por rotina pura.

    Contrato:
    - texto simples;
    - sem HTML;
    - sem markdown pesado;
    - curto.
    """
    texto = str(texto or "")
    texto = texto.replace("<", "").replace(">", "")
    texto = re.sub(r"(?m)^\s*#{1,6}\s*", "", texto)
    texto = texto.replace("**", "").replace("__", "")
    texto = texto.replace("```", "")
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    texto = texto.strip()

    if len(texto) > int(max_chars):
        corte = texto[: int(max_chars)].rstrip()
        ultimo_ponto = max(corte.rfind("."), corte.rfind("!"), corte.rfind("?"))
        if ultimo_ponto >= int(max_chars * 0.62):
            corte = corte[: ultimo_ponto + 1]
        texto = corte.rstrip() + "..."

    return texto


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


def gerar_analise_ola(tipo, tema, ypoema_texto):
    """Ponte para a OLA real.

    A rotina real vive em ponte_ola_openai.py e segue o contrato:
    recebe tipo, tema e yPoema limpo; devolve texto simples.
    Sem Streamlit, sem renderização, sem alterar o yPoema.

    Se a ponte não estiver instalada/importável, não simula resposta.
    """
    if _gerar_analise_ola_real is None:
        return "OLA ainda não conectada. Arquivo ponte_ola_openai.py não encontrado ou não importável."

    return limpar_analise(_gerar_analise_ola_real(tipo, tema, ypoema_texto))


def gerar_analise_cia(tipo, tema, ypoema_texto):
    """Rotina pura da CIA.

    Recebe tipo, tema e yPoema limpo.
    Devolve análise curta em texto simples.
    Não renderiza.
    Não altera o yPoema.
    Não usa HTML.
    Não chama Streamlit.
    Não mexe em session_state.
    """
    tipo = str(tipo or "Sintática").strip()
    tema = str(tema or "").strip()
    titulo, versos = _analise_titulo_e_versos(tema, ypoema_texto)
    primeiro = _analise_primeiro_verso(versos)
    ultimo = _analise_ultimo_verso(versos)
    total = len(versos)

    if tipo == "Semântica":
        texto = (
            f"A CIA lê “{titulo}” pelo campo de sentidos que a variação acende. "
            f"O texto parte de “{primeiro}” e deixa que as imagens se aproximem sem obrigar uma única interpretação.\n\n"
            "A força semântica está na abertura: cada verso desloca o anterior e prepara outra possibilidade de leitura. "
            f"O fecho “{ultimo}” não encerra o sentido; apenas entrega ao leitor a última inflexão do percurso."
        )
    else:
        texto = (
            f"A CIA lê “{titulo}” pela construção da linguagem. A variação tem {total} linhas de leitura, e sua força aparece nos cortes, "
            "nas pausas e na ordem em que as imagens se encadeiam.\n\n"
            f"O primeiro apoio sintático vem de “{primeiro}”. A partir dele, o yPoema organiza uma respiração própria: não explica demais, "
            "não fecha cedo, e deixa a frase trabalhar como passagem para o leitor."
        )

    return limpar_analise(texto)


def gerar_analise_atual(ypoema_html, tema):
    """Seleciona CIA ou OLA conforme a sidebar e devolve texto de análise.

    Esta função é orquestração de tela: lê session_state e converte HTML em texto.
    As rotinas gerar_analise_ola / gerar_analise_cia permanecem puras.
    """
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
        if nav_cols[4].button("📣", help=help_tips[6], key="ypoemas_voz_btn", use_container_width=True):
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
        render_help_ypoemas_com_ficha()
        lnew = False

    if lnew:
        what_book = (
            "🌀  "
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

                LOGO_IMAGE = (
                    "./images/matrix/" + st.session_state.tema.capitalize() + ".jpg"
                )
                write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

        if st.session_state.talk:
            with ypoemas_voz_slot:
                talk(curr_ypoema)


def _hide_eureka_help():
    """Fecha o Help da página Eureka quando o leitor volta à busca/lista."""
    st.session_state["eureka_help_open"] = False


def _on_eureka_occurrence_change():
    """Selecionar item na lista de ocorrências limpa o Help do palco."""
    _hide_eureka_help()
    try:
        st.session_state.eureka = int(st.session_state.get("opt_ocur", st.session_state.get("eureka", 0)))
    except Exception:
        st.session_state.eureka = 0


def page_eureka():
    help_tips = load_help(st.session_state.lang)
    help_rand = help_tips[1]
    help_more = help_tips[4]
    help_talk = help_tips[6]

    # Mesmo desenho de yPoemas/off-Machina:
    # [ busca ] [ nav_buttons + player compacto ] [ lista de ocorrências ]
    # O player fica dentro da coluna central, logo abaixo dos botões.
    try:
        seed, nav_area, occurrences = st.columns(
            [3, 4, 3],
            vertical_alignment="bottom",
        )
        eureka_nav_needs_spacer = False
    except TypeError:
        seed, nav_area, occurrences = st.columns([3, 4, 3])
        eureka_nav_needs_spacer = True

    with seed:
        find_what = st.text_input(
            label=translate("buscar por..."),
            help=translate("digite pelo menos 3 letras para buscar uma palavra que você goste..."),
            key="eureka_find_what",
            on_change=_hide_eureka_help,
        )

    with nav_area:
        if eureka_nav_needs_spacer:
            st.markdown(
                "<div style='height:1.95rem; min-height:1.95rem;'></div>",
                unsafe_allow_html=True,
            )

        nav_cols = st.columns([1, 1, 1, 1])
        more = nav_cols[0].button("✚", help=help_more, use_container_width=True)
        rand = nav_cols[1].button("✻", help=help_rand, use_container_width=True)

        if nav_cols[2].button("📣", key="eureka_voz_btn", help=help_talk, use_container_width=True):
            _hide_eureka_help()
            st.session_state.talk = not st.session_state.talk

        manu = nav_cols[3].button("?", help="help !!!", use_container_width=True)

        eureka_voz_slot = render_voz_slot()

    if manu:
        st.session_state["eureka_help_open"] = True

    if more or rand:
        _hide_eureka_help()

    eureka_should_render_help = bool(st.session_state.get("eureka_help_open", False))

    if len(find_what) < 3:
        if eureka_should_render_help:
            render_manual_eureka()
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
            if eureka_should_render_help:
                render_manual_eureka()
            st.warning(
                translate(
                    'nenhuma ocorrência das letras " '
                    + find_what
                    + ' " foi encontrada...'
                )
            )
        elif len(seed_list) >= 1:
            seed_list.sort()
            info_find = '"' + str(find_what)
            if len(soma_tema) > 1:
                info_find += translate('" em ' + str(len(soma_tema)) + " temas")
            else:
                info_find += '"'

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
                    on_change=_on_eureka_occurrence_change,
                )

            previous_opt = st.session_state.get("_eureka_last_opt_ocur")
            if previous_opt is not None and previous_opt != opt_ocur:
                _hide_eureka_help()
                eureka_should_render_help = False
            st.session_state["_eureka_last_opt_ocur"] = opt_ocur

            if not rand:
                st.session_state.eureka = opt_ocur

            if eureka_should_render_help:
                render_manual_eureka()
                return

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
        if nav_cols[3].button("📣", help=help_tips[6], key="off_voz_btn", use_container_width=True):
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
        render_manual_off_machina()

    if lnew:
        what_book = (
            "🌀  "
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
                off_book_text = _pip_line_to_text(this_off_book[st.session_state.off_take])

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
                        write_off_machina_texto(off_book_text)  # aplica fonte/corpo do leitor
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
    try:
        total_temas_ficha = len([tema for tema in load_temas("todos os temas") if str(tema).strip()])
    except Exception:
        total_temas_ficha = len(temas)

    bloco = (
        f"{BUILD_AMBIENTE_LEXICO}\n\n"
        f"Total de Verbetes: {_tools_fmt_int(total_verbetes)}\n"
        f"Total de Verbetes únicos: {_tools_fmt_int(len(verbetes_unicos))}\n\n"
        f"Total de Ítimos: {_tools_fmt_int(total_itimos)}\n"
        f"Total de Ítimos únicos: {_tools_fmt_int(len(itimos_unicos))}\n\n"
        f"Total de Temas: {_tools_fmt_int(total_temas_ficha)}\n"
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



# -----------------------------------------------------------------------------
# Build_rimas :: Off Sina / bancada lexical
# -----------------------------------------------------------------------------
BUILD_RIMAS_WORD_RE = re.compile(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", re.UNICODE)
BUILD_RIMAS_RICH_SUFFIXES = {
    "ão", "ões",
    "ais", "eis", "éis", "ois", "óis", "ous",
    "ado", "ada", "ido", "ida",
    "oso", "osa", "esa", "eza",
    "ante", "ente", "inte", "onte", "unto",
    "al", "el", "il", "ol", "ul",
}
BUILD_RIMAS_WEAK_SUFFIXES = {
    "da", "de", "do",
    "me", "se", "te",
    "lhe", "nte",
}
BUILD_RIMAS_CLITIC_PRONOUNS = {
    "me", "te", "se", "nos", "vos",
    "o", "a", "os", "as",
    "lo", "la", "los", "las",
    "no", "na", "nas",
    "lhe", "lhes",
}
BUILD_RIMAS_PREFERRED_SHORT_SUFFIXES = {
    "ar", "er", "ir", "or",
    "as", "es", "is", "os",
    "ão", "õe", "am", "em", "ou", "ei",
    "al", "el", "il", "ol", "ul",
    "ante", "ente", "inte", "onte", "unto",
    "ões", "ais", "eis", "ous",
    "ado", "ada", "ido", "ida",
    "oso", "osa", "esa", "eza",
}


def _build_rimas_strip_accents(text):
    """Chave de ordenação sem acentos, preservando a palavra original na saída."""
    normalized = unicodedata.normalize("NFD", str(text or "").casefold())
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


def _build_rimas_normalize_word(word, mode):
    word = str(word or "").strip("-'")
    if mode == "upper":
        return word.upper()
    if mode == "preserve":
        return word
    return word.casefold()


def _build_rimas_verb_to_infinitive(word):
    clean = _build_rimas_strip_accents(word)
    if clean.endswith("ando"):
        return clean[:-4] + "ar"
    if clean.endswith("endo"):
        return clean[:-4] + "er"
    if clean.endswith("indo"):
        return clean[:-4] + "ir"
    if clean.endswith(("ar", "er", "ir", "or")):
        return clean
    if clean.endswith("a"):
        return clean + "r"
    if clean.endswith("e"):
        return clean + "r"
    return clean


def _build_rimas_expand_token(token):
    parts = [part for part in str(token or "").split("-") if part]
    if len(parts) <= 1:
        return parts

    last_part = _build_rimas_strip_accents(parts[-1])
    if last_part in BUILD_RIMAS_CLITIC_PRONOUNS:
        return [_build_rimas_verb_to_infinitive(parts[0])]

    return parts


def _build_rimas_extract_words(text, mode="lower", min_len=2):
    words = []
    for match in BUILD_RIMAS_WORD_RE.finditer(str(text or "")):
        for token in _build_rimas_expand_token(match.group(0)):
            word = _build_rimas_normalize_word(token, mode)
            if len(word) >= int(min_len):
                words.append(word)
    return words


def _build_rimas_sorted_words(words):
    return sorted(set(words), key=lambda value: (_build_rimas_strip_accents(value), value))


def _build_rimas_group_by_suffix(words, min_size=2, max_size=6):
    groups = {}
    for word in words:
        for size in range(int(min_size), int(max_size) + 1):
            if len(word) <= size:
                continue
            suffix = word[-size:]
            groups.setdefault(suffix, set()).add(word)

    candidates = []
    for suffix, values in groups.items():
        if len(values) >= 2 and _build_rimas_strip_accents(suffix) not in BUILD_RIMAS_WEAK_SUFFIXES:
            candidates.append((suffix, _build_rimas_sorted_words(values)))

    def is_preferred(suffix):
        return str(suffix).casefold() in BUILD_RIMAS_PREFERRED_SHORT_SUFFIXES

    def suffix_score(suffix):
        clean = _build_rimas_strip_accents(suffix)
        if str(suffix).casefold() in BUILD_RIMAS_RICH_SUFFIXES:
            return (0, len(suffix), clean, suffix)
        if is_preferred(suffix):
            return (1, len(suffix), clean, suffix)
        return (2, abs(5 - len(suffix)), clean, suffix)

    candidates.sort(key=lambda item: suffix_score(item[0]))

    result = {}
    seen_sets = set()
    for suffix, sorted_values in candidates:
        value_set = set(sorted_values)
        signature = tuple(sorted_values)
        if signature in seen_sets:
            continue
        if any(
            suffix.endswith(selected_suffix) and value_set.issubset(set(selected_words))
            for selected_suffix, selected_words in result.items()
        ):
            continue
        if not is_preferred(suffix):
            covered_words = set()
            for selected_suffix, selected_words in result.items():
                if selected_suffix.endswith(suffix):
                    covered_words.update(selected_words)
            if value_set.issubset(covered_words):
                continue
        seen_sets.add(signature)
        result[suffix] = sorted_values

    return dict(sorted(result.items(), key=lambda item: (len(item[0]), _build_rimas_strip_accents(item[0]), item[0])))


def _build_rimas_split_groups(groups):
    rich = {}
    support = {}
    for suffix, words in groups.items():
        if str(suffix).casefold() in BUILD_RIMAS_RICH_SUFFIXES:
            rich[suffix] = words
        else:
            support[suffix] = words
    return rich, support


def _build_rimas_sorted_by_suffix(words):
    return sorted(
        set(words),
        key=lambda word: (_build_rimas_strip_accents(word)[::-1], _build_rimas_strip_accents(word), word),
    )


def _build_rimas_render_list(lines):
    return "\n".join(lines) if lines else "(nenhum)"


def _build_rimas_render_groups(groups, marker="-"):
    parts = []
    for key, words in groups.items():
        label = f"[ {key} ]" if marker == "-" else f"[ {key}{marker} ]"
        parts.append(f"{label}\n{_build_rimas_render_list(words)}")
    return "\n\n".join(parts) if parts else "(nenhum grupo com 2 ou mais palavras)"


def build_rimas_texto(text, mode="lower", min_len=2, min_suffix=2, max_suffix=6):
    """Gera mapa lexical/rimas a partir de texto bruto. Não altera arquivos da Machina."""
    all_words = _build_rimas_extract_words(text, mode=mode, min_len=max(1, int(min_len)))
    unique_words = _build_rimas_sorted_words(all_words)

    suffix_groups = _build_rimas_group_by_suffix(unique_words, min_size=min_suffix, max_size=max_suffix)
    rich_groups, support_groups = _build_rimas_split_groups(suffix_groups)
    mapped_words = {word for words in rich_groups.values() for word in words}
    outside_words = _build_rimas_sorted_by_suffix(set(unique_words) - mapped_words)

    return "\n\n".join(
        [
            "Build_rimas",
            "___",
            f"Total de ocorrências: {len(all_words)}",
            f"Palavras únicas: {len(unique_words)}",
            f"Palavras em rimas ricas: {len(mapped_words)}",
            f"Palavras fora do mapa: {len(outside_words)}",
            "___",
            "RIMAS RICAS",
            _build_rimas_render_groups(rich_groups, "-"),
            "___",
            "RIMAS DE APOIO",
            _build_rimas_render_groups(support_groups, "-"),
            "___",
            "FORA DO MAPA",
            _build_rimas_render_list(outside_words),
            "___",
            "EOF()",
        ]
    )


def _build_rimas_decode_uploaded(uploaded_file):
    data = uploaded_file.getvalue()
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def render_build_rimas_tool():
    """Ferramenta local da Off Sina para mineração lexical/rimas."""
    st.markdown("### Build_rimas")
    st.caption("Off Sina: lê arquivo ou texto colado, organiza palavras únicas e monta mapa de rimas para curadoria.")

    pasted_text = st.text_area(
        "colar texto / área de descarte",
        value=st.session_state.get("build_rimas_pasted_text", ""),
        height=180,
        key="build_rimas_pasted_text",
        placeholder="Ctrl+V aqui basta para carregar o texto...",
    )

    uploaded = st.file_uploader(
        "arquivo .txt / .md / .doc",
        type=["txt", "md", "markdown", "doc"],
        key="build_rimas_upload",
    )

    col_case, col_min, col_suf = st.columns([1.2, 1.0, 1.4])
    with col_case:
        case_mode = st.selectbox(
            "caixa",
            ["lower", "upper", "preserve"],
            index=0,
            key="build_rimas_case",
        )
    with col_min:
        min_len = st.selectbox(
            "mínimo",
            list(range(1, 8)),
            index=1,
            key="build_rimas_min_len",
        )
    with col_suf:
        max_suffix = st.selectbox(
            "sufixo máx.",
            list(range(3, 9)),
            index=3,
            key="build_rimas_max_suffix",
        )

    pasted_text = str(pasted_text or "")
    has_paste = bool(pasted_text.strip())
    has_upload = uploaded is not None

    if has_paste:
        default_name = "texto_colado_rimas.txt"
        fonte_label = "texto colado"
    elif has_upload:
        default_name = os.path.splitext(uploaded.name)[0] + "_rimas.txt"
        fonte_label = uploaded.name
    else:
        default_name = "build_rimas.txt"
        fonte_label = ""

    output_name = st.text_input(
        "nome do arquivo de saída",
        value=default_name,
        key="build_rimas_output_name",
    ).strip() or default_name
    if not output_name.lower().endswith(".txt"):
        output_name += ".txt"

    if not has_paste and not has_upload:
        st.info("Cole um texto com Ctrl+V na área de descarte ou escolha um arquivo .txt/.md/.doc.")
        return

    if has_paste and has_upload:
        st.caption("Fonte ativa: texto colado. Para usar o arquivo, limpe a área de descarte.")

    if st.button("Build_rimas", use_container_width=True):
        texto = pasted_text if has_paste else _build_rimas_decode_uploaded(uploaded)
        mapa = build_rimas_texto(
            texto,
            mode=case_mode,
            min_len=min_len,
            min_suffix=2,
            max_suffix=max_suffix,
        )
        st.session_state["build_rimas_result"] = mapa
        st.session_state["build_rimas_download_name"] = output_name
        st.session_state["build_rimas_source_label"] = fonte_label
        st.success("Build_rimas concluído.")

    resultado = st.session_state.get("build_rimas_result", "")
    download_name = st.session_state.get("build_rimas_download_name", output_name)
    source_label = st.session_state.get("build_rimas_source_label", "")
    if resultado:
        if source_label:
            st.caption("fonte: " + str(source_label))
        st.text_area(
            "mapa lexical",
            value=resultado,
            height=420,
            key="build_rimas_textarea",
        )
        st.download_button(
            "baixar " + download_name,
            data=resultado + "\n",
            file_name=download_name,
            mime="text/plain",
            use_container_width=True,
        )

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

build_rimas
  Off Sina: lê um .txt/.md/.doc em texto UTF-8, extrai palavras únicas e gera mapa de rimas
  para curadoria. Não altera .ypo, base, md_files nem poesia.

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
#    st.caption("LOCAL. Lista funcional simples. Lê temas; não altera poesia.")

    tools_items = [
        "novo_tema",
        "remove_tema",
        "update_tema",
        "atualizar_rodape_ypo",
        "---",
        "build_indexy",
        "build_lexico",
        "build_off-lex",
        "build_rimas",
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

    if escolha == "build_rimas":
        render_build_rimas_tool()
        return

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

    # Respiro: desce o bloco de análise para aproveitar a área livre da sidebar.
    st.sidebar.markdown("<div style='height:1.85rem;'></div>", unsafe_allow_html=True)

    # Bloco de análise: mesmo eixo visual de fontes & letras + corpo.
    # CIA começa no eixo esquerdo da lista de fontes.
    # Os três botões têm larguras iguais.
    col_analysis, col_analysis_right = st.sidebar.columns([2.78, 1.32])

    with col_analysis:
        col_cia, col_machina = st.columns([1, 1])
    with col_analysis_right:
        col_ola = st.container()

        with col_cia:
            if st.button(
                "CIA",
                key="analysis_voice_cia_btn",
                use_container_width=True,
                type="primary" if current_key == "CIA" else "secondary",
            ):
                _set_analysis_voice("CIA")
                try:
                    st.rerun()
                except AttributeError:
                    st.experimental_rerun()

        with col_machina:
            if st.button(
                "MACHINA",
                key="analysis_voice_machina_btn",
                use_container_width=True,
                type="primary" if current_key == "MACHINA" else "secondary",
            ):
                _set_analysis_voice("Machina")
                try:
                    st.rerun()
                except AttributeError:
                    st.experimental_rerun()

        with col_ola:
            if st.button(
                "OLA",
                key="analysis_voice_ola_btn",
                use_container_width=True,
                type="primary" if current_key == "OLA" else "secondary",
            ):
                _set_analysis_voice("OLA")
                try:
                    st.rerun()
                except AttributeError:
                    st.experimental_rerun()

    if options:
        # Respiro maior entre botões e lista de análises.
        st.sidebar.markdown(
            "<div style='height:1.42rem;'></div>",
            unsafe_allow_html=True,
        )
        # A lista de análises usa a mesma regra visual da lista_idiomas:
        # selectbox nativo da sidebar com max-width 320px no CSS global.
        choice = st.sidebar.selectbox(
            "tipo",
            options,
            index=options.index(current_kind) if current_kind in options else 0,
            key="analysis_kind_select",
            label_visibility="collapsed",
        )
        st.session_state["analysis_kind"] = choice



def render_sidebar_for_page(chosen_id):
    """Renderiza os controles fixos do leitor, sem botão arte fóssil."""
    pick_lang()
    pick_stage_font()
    render_analysis_sidebar_block()


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
        page_labels = ["mini", "yPoemas", "eureka", "off-Machina", "tools"]
        page_ids = {
            "mini": "1",
            "yPoemas": "2",
            "eureka": "3",
            "off-Machina": "4",
            "tools": "5",
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
                    status = f"🌀  {st.session_state.lang} - {st.session_state.tema} ( {st.session_state.mini + 1} / {len(load_temas('todos os temas'))} )"

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
                    page_local_tools()
                    status = palco_status("tools")
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
