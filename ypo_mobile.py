# =============================================================================
# ypo_mobile.py — MACHINA MOBILE / FONTE PÚBLICA
# =============================================================================
# Leitura da casa:
# terreno/configuração -> funções/estado/componentes comuns
# -> 1 Mini -> 2 yPoemas -> 3 Eureka/ACROS -> 4 Off-Machina
# -> 5 ABOUT -> saída/roteamento.
#
# Nomes históricos e funcionais permanecem.
# Nomes novos: claros, simples, autoexplicativos, sem redundância.
# =============================================================================

import os
import re
import time
import random
import string
import base64
import html
import json
import unicodedata
import socket
import asyncio
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
import streamlit as st
import streamlit.components.v1 as components
import dna as dna_core
# ✅

APP_BUILD = "2026-08-12_YPO_RAIZ_CLEAN"
APP_BUILD_NOTES = "ACROS integrado à Eureka como aparição; Copiar/Retrato preservam a assinatura da Machina."

from lay_2_ypo import gera_poema, fala_nome_OLA
from acros import gerar_acros, AcrosError
from akros_motor import gerar_akros, AkrosError


try:
    from ponte_ola_openai import gerar_analise_ola as gerar_analise_ola_real
except Exception:
    gerar_analise_ola_real = None

livros_list = [
    "todos os temas", "livro vivo", "poemas", "jocosos", "ensaios", "variações",
    "metalinguagem", "sociais", "outros autores", "signos_fem", "signos_mas",
    "todos os signos",
]

off_livros_list = [
    "a_torre_de_papel", "quase_que_eu_Poesia", "faz_de_conto", "um_romance", "parafernália",
    "linguafiada", "livro_vivo", "desvoto", "ensaios", "urbano", "essencial", "secreto",
]

PAGE_IMAGES = {
    "1": "img_mini.jpg", "2": "img_ypoemas.jpg", "3": "img_eureka.jpg",
    "4": "img_off-machina.jpg", "5": "img_about.jpg",
}

vozes_tts = {
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
    ("Português", "Brasil", "pt"),
    ("Español", "Espanha", "es"),
    ("Italiano", "Itália", "it"),
    ("Français", "França", "fr"),
    ("Latin", "Latim", "la"),
    ("Esperanto", "Esperanto", "eo"),
    ("English", "Inglaterra", "en"),
    ("Deutsch", "Alemanha", "de"),
    ("Català", "Catalunha", "ca"),
    ("Euskara", "Basco", "eu"),
    ("Galego", "Galícia", "gl"),
    ("Nederlands", "Países Baixos", "nl"),
    ("Polski", "Polônia", "pl"),
    ("Română", "Romênia", "ro"),
    ("Русский", "Rússia", "ru"),
    ("Svenska", "Suécia", "sv"),
    ("Norsk", "Noruega", "no"),
    ("Dansk", "Dinamarca", "da"),
    ("Suomi", "Finlândia", "fi"),
    ("Íslenska", "Islândia", "is"),
    ("Magyar", "Hungria", "hu"),
]

# -----------------------------------------------------------------------------
# Configuração inicial da página Streamlit.
# Deve permanecer antes de qualquer saída visual do Streamlit.
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="A Machina de fazer Poesia - Mobile",
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
host = socket.gethostname()
ip = socket.gethostbyname(host)

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
            font-weight: 700;
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
            height: 360px !important;
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
            object-fit: contain !important;
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
        "book": "todos os temas",
        "take": 0,
        "mini": 0,
        "tema": "Fatos",
        "off_book": 0,
        "off_take": 0,
        "eureka": 0,
        "poly_lang": "ca",
        "poly_name": "català",
        "poly_take": 12,
        "visy": True,
        "nany_visy": 0,
        "draw": False,
        "talk": False,
        "arts": [],
        "auto": False,
        "rand": False,

        "fonte_palco": "Trebuchet",
        "corpo_palco": 21,
        "sidebar_panel": "Machina",

        "tema_last_analise": "",
        "ypoema_analise": "",
        "tema_analise": "",
        "livro_analise": "",
        "take_analise": -1,
        "lang_analise": "",

        # chave de ouro
        "key_open": False,
        "key_poema_texto": "",
        "key_poema_tema": "",
        "key_analise": "",
        "qtd_copias": 2,
        "pick_qtd_copias": 2,
        "texto_pacote_copias": "",
        "key_pacote_copias": 0,
        "qtd_pacote_copias": 0,
        "origem_pacote_copias": "",
        "tema_key_num": 0,

        # análise :: Machina / OLA
        "voz_analise": "Machina",
        "tipo_analise": "Sintática",

        # ACROS — aparição na Eureka
        "acros_on": False,
        "acros_html": "",
        "acros_texto": "",
        "acros_entrada": "",
        "acros_modo_pedido": "Bem",
        "acros_genero_pedido": "Masculino",
        "acros_key": 0,
        "acros_imagem": "",
        "acros_poetico_pedido": False,
        "acros_open": False,
        "acros_nome": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

apply_styles()
init_session_state()


def limpar_retrato(prefixo):
    """Apaga o Retrato da página indicada sem alterar o conteúdo do palco."""
    for nome in (
        "imagem_retrato",
        "nome_retrato",
        "retrato_focus",
        "contexto_retrato",
        "retrato_keep_palco",
        "retrato_origem_image",
    ):
        st.session_state.pop(f"{prefixo}_{nome}", None)

def limpar_retratos():
    """Apaga qualquer Retrato existente ao sair/navegar entre páginas."""
    for prefixo in ("mini", "ypo", "eureka", "acros", "off"):
        limpar_retrato(prefixo)

def limpar_retrato_off():
    """Compatibilidade interna da página Off-Machina."""
    limpar_retrato("off")


def _limpar_retrato_contextual(prefixo):
    """Compatibilidade interna: usa a mesma limpeza para todas as páginas."""
    limpar_retrato(prefixo)

def focar_retrato_no_palco(anchor_id):
    """Move o foco visual para o Retrato recém-gerado."""
    anchor_id = re.sub(r"[^A-Za-z0-9_-]+", "_", str(anchor_id or "retrato_gerado"))
    components.html(
        f"""
        <script>
        setTimeout(function() {{
            const alvo = window.parent.document.getElementById({anchor_id!r});
            if (alvo) {{
                alvo.scrollIntoView({{behavior: 'smooth', block: 'start'}});
            }}
        }}, 80);
        </script>
        """,
        height=0,
    )


def make_retrato_xerox(prefixo):
    """Retrata exatamente o que o leitor vê; só depois renova a imagem da sidebar."""
    texto = st.session_state.get(f"{prefixo}_palco_xerox_text", "")
    titulo = st.session_state.get(f"{prefixo}_palco_xerox_title", "")
    contexto = st.session_state.get(f"{prefixo}_palco_xerox_context")

    # Fidelidade visual do clique: usa a ÚLTIMA imagem efetivamente renderizada
    # na sidebar, não uma variável de estado que já possa ter sido renovada.
    # Essa chave é gravada por render_sidebar_context_image() no fim de cada rerun.
    imagem = st.session_state.get("sidebar_image_visible_path", "")

    # Fallback defensivo para a primeira execução/estado antigo.
    if not imagem:
        if prefixo == "off":
            imagem = st.session_state.get("off_machina_images_pasta", "")
        else:
            imagem = st.session_state.get("save_image_tema", "")
    if not imagem:
        imagem = st.session_state.get(f"{prefixo}_palco_xerox_image", "")

    png = criar_retrato_png(texto, imagem, titulo, selo_size=RETRATO_SELO_SIZE)
    if not png:
        return

    st.session_state[f"{prefixo}_imagem_retrato"] = png
    st.session_state[f"{prefixo}_retrato_origem_image"] = imagem

    if prefixo == "acros":
        nome_retrato = str(st.session_state.get("acros_entrada", "") or "").strip()
        nome_retrato = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", nome_retrato).strip(" .") or "retrato"
    else:
        nome_retrato = re.sub(
            r"[^A-Za-z0-9_-]+",
            "_",
            str(titulo or "retrato"),
        ).strip("_") or "retrato"

    st.session_state[f"{prefixo}_nome_retrato"] = nome_retrato
    st.session_state[f"{prefixo}_contexto_retrato"] = contexto
    st.session_state[f"{prefixo}_retrato_focus"] = True

    # Só depois da captura fiel: prepara uma nova imagem para a sidebar.
    if prefixo == "off":
        try:
            book_pos = int(st.session_state.get("off_book", 0))
            book_name = off_livros_list[book_pos]
        except (TypeError, ValueError, IndexError):
            book_name = ""
        grupo = _off_book_image_group(book_name)
        images = _images_from_group(grupo) if grupo else _images_from_group("anima")
        if images:
            disponiveis = [img for img in images if img != imagem]
            st.session_state["off_machina_images_pasta"] = random.choice(disponiveis or images)
            st.session_state["off_retrato_sidebar_renovada"] = True
    else:
        tema_contexto = titulo or st.session_state.get("tema", "Fatos") or "Fatos"
        # ACROS não usa título de tema no Retrato; a curadoria vem do tema da Eureka.
        if prefixo == "acros":
            tema_contexto = st.session_state.get("tema", "Fatos") or "Fatos"
        imagem_nova = load_arts(tema_contexto)
        if imagem_nova:
            st.session_state["save_image_tema"] = imagem_nova
            st.session_state[f"{prefixo}_retrato_sidebar_renovada"] = True

    # O rerun preserva o texto retratado; a imagem da sidebar já pode mudar.
    st.session_state[f"{prefixo}_retrato_keep_palco"] = True

def show_retrato_no_topo(prefixo):
    """Mostra o Retrato como resultado principal no topo do palco."""
    png = st.session_state.get(f"{prefixo}_imagem_retrato")
    if not png:
        return False

    anchor = f"retrato_{prefixo}_gerado"
    st.markdown(f'<div id="{anchor}"></div>', unsafe_allow_html=True)
    st.image(png, use_container_width=True)
    if st.session_state.pop(f"{prefixo}_retrato_focus", False):
        focar_retrato_no_palco(anchor)
    return True


def _toggle_sidebar_image():
    """Liga/desliga somente a imagem contextual da sidebar."""
    st.session_state["draw"] = not bool(st.session_state.get("draw", True))

def show_copy_retrato_xerox(prefixo, texto_copia):
    """Copy/Imagem/Retrato com o mesmo comportamento em todas as páginas."""
    st.markdown("<br>", unsafe_allow_html=True)
    left, copy_col, image_col, retrato_col, right = st.columns([2.6, 2.0, 2.0, 2.0, 2.6])

    with copy_col:
        with st.popover("Copy", help="copiar texto", use_container_width=True):
            st.code(str(texto_copia or ""), language=None, wrap_lines=True)

    with image_col:
        st.button(
            "Imagem",
            key=f"{prefixo}_imagem_btn",
            help="ligar/desligar imagem",
            use_container_width=True,
            on_click=_toggle_sidebar_image,
        )

    with retrato_col:
        st.button(
            "Retrato",
            key=f"{prefixo}_retrato_btn",
            help="mostrar Retrato",
            use_container_width=True,
            on_click=make_retrato_xerox,
            args=(prefixo,),
        )

    png = st.session_state.get(f"{prefixo}_imagem_retrato")
    if png:
        col_left, col_save, col_right = st.columns([1, 1, 1])
        with col_save:
            st.download_button(
                "salvar Retrato",
                data=png,
                file_name=f"{st.session_state.get(f'{prefixo}_nome_retrato', 'retrato')}.png",
                mime="image/png",
                key=f"{prefixo}_retrato_save",
                use_container_width=True,
                on_click="ignore",
            )

def get_key_pacote_copias(curr_ypoema=""):
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
    st.session_state["texto_pacote_copias"] = ""
    st.session_state["qtd_pacote_copias"] = 0
    st.session_state["origem_pacote_copias"] = ""
    st.session_state["key_pacote_copias"] = int(st.session_state.get("key_pacote_copias", 0)) + 1

def fix_qtd_copias(qtd):
    """Quantidade em lote: 2..9. Para +1, o botão ✚ já cumpre esse papel."""
    try:
        qtd = int(qtd)
    except Exception:
        qtd = 2
    return max(2, min(9, qtd))

def change_qtd_copias():
    """Lista de quantidade como ação: um clique já escolhe e prepara o resultado."""
    st.session_state["qtd_copias"] = fix_qtd_copias(
        st.session_state.get("pick_qtd_copias", st.session_state.get("qtd_copias", 2))
    )
    st.session_state["change_qtd_copias"] = True

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
        return f"🍃  {st.session_state.lang} ( {book} )"
    return f"🍃  {st.session_state.lang} ( {book} ) ( {pos} / {total} )"

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

    for nome, pais, code in IDIOMAS_OFICIAIS:
        label = f"{nome} — {pais}"
        options.append(label)
        lookup[label] = {
            "lang": code,
        }

    # Antes de desenhar a lista, sincroniza o idioma com a seleção já feita.
    # Isso evita label traduzido no idioma anterior.
    previous_choice = st.session_state.get("pick_idioma")
    if previous_choice in lookup:
        selected_previous = lookup[previous_choice]
        if st.session_state.lang != selected_previous["lang"]:
            st.session_state.last_lang = st.session_state.lang
            st.session_state.lang = selected_previous["lang"]

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
        key="pick_idioma",
    )

    selected = lookup[choice]
    if st.session_state.lang != selected["lang"]:
        st.session_state.last_lang = st.session_state.lang
        st.session_state.lang = selected["lang"]

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

def fix_take(take, temas):
    """Converte diferentes formas de seleção de tema para índice inteiro válido."""
    if not temas:
        return 0

    if isinstance(take, int):
        take = take
    elif isinstance(take, str):
        if take.isdigit():
            take = int(take)
        elif take in temas:
            take = temas.index(take)
        else:
            take = 0
    else:
        take = 0

    if take < 0 or take >= len(temas):
        take = 0
    return take

def sync_livro_tema():
    """Mantém o estado canônico (book/take/tema) consistente."""
    books_list = livros_list
    current_book = st.session_state.get("book", books_list[0])
    if current_book not in books_list:
        current_book = books_list[0]
    st.session_state.book = current_book

    temas = load_temas(current_book)
    if not temas:
        st.session_state.take = 0
        st.session_state.tema = ""
        return

    take = fix_take(st.session_state.get("take", 0), temas)

    old_take = st.session_state.get("take", 0)
    st.session_state.take = take
    st.session_state.tema = temas[take]
    if take != old_take:

        next_tema_key()

def _current_book():
    """Retorna o livro atual sem depender de atributo já criado no session_state."""
    book = st.session_state.get("book", livros_list[0])
    return book if book in livros_list else livros_list[0]

def set_livro_key(key):
    """Faz o widget espelhar `book` sem tomar conta do estado."""
    current = _current_book()
    if key in st.session_state and st.session_state.get(key) != current:
        del st.session_state[key]

def next_tema_key():
    """Força recriação segura da lista de temas sem escrever na key do widget."""
    st.session_state["tema_key_num"] = int(
        st.session_state.get("tema_key_num", 0)
    ) + 1

def get_tema_key():
    return "opt_take_palco_" + str(int(st.session_state.get("tema_key_num", 0)))

def set_tema_key():
    """Mantém lista de temas sincronizada sem escrever na key do selectbox."""
    return get_tema_key()

def change_livro_palco():
    limpar_retrato("ypo")
    current_book = _current_book()
    choice = st.session_state.get("pick_livro_palco", current_book)
    if choice != current_book:
        st.session_state.book = choice
        st.session_state.take = 0
        limpar_copias_palco()

        next_tema_key()
    sync_livro_tema()

def change_tema_palco():
    limpar_retrato("ypo")
    temas = load_temas(_current_book())
    if not temas:
        st.session_state.take = 0
        st.session_state.tema = ""
        return

    widget_key = st.session_state.get("tema_key", get_tema_key())
    take = fix_take(
        st.session_state.get(widget_key, st.session_state.get("take", 0)),
        temas,
    )

    old_take = st.session_state.get("take", 0)
    st.session_state.take = take
    st.session_state.tema = temas[take]
    if take != old_take:
        limpar_copias_palco()

def pick_livro_palco():
    """Escolhe o livro yPoemas diretamente no palco."""
    sync_livro_tema()

    books_list = livros_list
    current = _current_book()
    key = "pick_livro_palco"
    set_livro_key(key)

    st.selectbox(
        "↓  " + str(len(books_list)) + " livros",
        books_list,
        index=books_list.index(current),
        key=key,
        on_change=change_livro_palco,
    )

def pick_tema_palco():

    """Escolhe o tema atual do livro diretamente no palco."""
    sync_livro_tema()
    temas = load_temas(_current_book())
    if not temas:
        return

    widget_key = set_tema_key()
    st.session_state["tema_key"] = widget_key
    options = list(range(len(temas)))
    st.selectbox(
        f"↓  {len(temas)} " + translate("temas"),
        options,
        index=fix_take(st.session_state.get("take", 0), temas),
        format_func=lambda z: temas[z],
        key=widget_key,
        on_change=change_tema_palco,
    )

def pick_fonte_palco():
    """Escolhe fonte e corpo de leitura do Palco."""
    labels = [label for label, fonte in FONTES_MACHINA]
    lookup = {label: fonte for label, fonte in FONTES_MACHINA}

    current_font = st.session_state.get("fonte_palco", "Trebuchet")
    current_label = next(
        (label for label, fonte in FONTES_MACHINA if fonte == current_font),
        labels[0],
    )

    corpos = list(range(14, 35, 2))
    current_size = st.session_state.get("corpo_palco", 22)
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

    st.session_state.fonte_palco = lookup[choice]
    st.session_state.corpo_palco = size

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
    with open(bin_file, "rb") as arquivo:
        data = arquivo.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">download {file_label}</a>'

    return href

def atoi(text):  # human reading number functions for sorting
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(parte) for parte in re.split(r"(\d+)", text)]


# =============================================================================
# LEITURAS / VISITAS — serviço comum da casa (ex-readings.py)
# =============================================================================
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

def _md_nome_variantes(nome):
    """Gera variantes seguras do nome para comparação de arquivos MD.

    Inclui reparo de mojibake UTF-8/Latin-1, sem alterar o catálogo nem o arquivo.
    """
    original = str(nome or "").strip()
    variantes = [original]

    # Alguns nomes podem ter sido gravados/exibidos como UTF-8 interpretado em Latin-1.
    try:
        reparado = original.encode("latin-1").decode("utf-8")
        if reparado and reparado not in variantes:
            variantes.append(reparado)
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass

    return variantes

def find_md_file(file_name):
    """Localiza um arquivo de md_files sem inferir outro conteúdo.

    Ordem:
    1. caminho literal;
    2. equivalência Unicode/caixa;
    3. equivalência do nome completo sem diacríticos;
    4. reparo restrito de mojibake no nome completo.
    """
    expected_name = str(file_name or "").strip()
    if not expected_name:
        return ""

    md_dir = _project_path("md_files")
    if not os.path.isdir(md_dir):
        return ""

    expected_candidates = []
    for variante in _md_nome_variantes(expected_name):
        base = os.path.basename(variante.strip())
        if not base:
            continue
        expected_candidates.append(base)
        if not os.path.splitext(base)[1]:
            expected_candidates.append(base + ".md")

    # Caminho literal primeiro.
    for candidate in expected_candidates:
        direct = os.path.join(md_dir, candidate)
        if os.path.isfile(direct):
            return direct

    expected_folds = {
        unicodedata.normalize("NFC", item).casefold()
        for item in expected_candidates
    }
    expected_keys = {
        _md_nome_chave(item)
        for item in expected_candidates
        if _md_nome_chave(item)
    }

    key_matches = []
    for real_name in os.listdir(md_dir):
        real_path = os.path.join(md_dir, real_name)
        if not os.path.isfile(real_path):
            continue
        if not real_name.casefold().endswith(".md"):
            continue

        real_variants = _md_nome_variantes(real_name)

        real_folds = {
            unicodedata.normalize("NFC", item).casefold()
            for item in real_variants
        }
        if expected_folds & real_folds:
            return real_path

        real_keys = {
            _md_nome_chave(item)
            for item in real_variants
            if _md_nome_chave(item)
        }
        if expected_keys & real_keys:

            key_matches.append(real_path)

    # Só retorna por chave sem diacríticos quando há uma única correspondência.
    unique_matches = list(dict.fromkeys(key_matches))
    if len(unique_matches) == 1:
        return unique_matches[0]

    return ""

def load_md_file(file):  # Open files for about's
    path = find_md_file(file)
    try:
        with open(path, encoding='utf-8-sig') as file_to_open:
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
- ♫ = ouvir a leitura do texto
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

def _fmt_numero_leitor(numero):
    """Pontua inteiros para leitura humana sem alterar o valor interno."""
    try:
        return f"{int(numero):,}".replace(",", ".")
    except (TypeError, ValueError):
        return str(numero or "").strip()

def _palavras_visiveis(texto):
    """Extrai verbetes do yPoema materializado, ignorando marcação HTML."""
    texto = html.unescape(re.sub(r"<[^>]+>", " ", str(texto or "")))
    return re.findall(r"[^\W_]+(?:-[^\W_]+)*", texto, flags=re.UNICODE)

def _help_find_ypo_file(nome_tema):
    tema = str(nome_tema or "").strip()
    data_dir = _project_path("data")
    for ext in (".ypo", ".YPO"):
        arquivo = os.path.join(data_dir, tema + ext)
        if os.path.exists(arquivo):
            return arquivo
    if os.path.isdir(data_dir):
        tema_key = _md_nome_chave(tema)
        for nome in os.listdir(data_dir):
            if nome.lower().endswith(".ypo") and _md_nome_chave(os.path.splitext(nome)[0]) == tema_key:
                return os.path.join(data_dir, nome)
    return ""

def _help_info_estavel(nome_tema):
    """Ficha cadastral: autoridade permanente = base/DNA.TXT."""
    row = dna_core.registro(nome_tema)
    if not row:
        return {"titulo": str(nome_tema or "").strip()}
    return {
        "titulo": row.get("tema", "").strip() or str(nome_tema or "").strip(),
        "ativo": row.get("ativo", "").strip(),
        "livro": row.get("livro", "").strip(),
        "banco_tematico": row.get("banco_tematico", "").strip(),
        "versos": row.get("versos", "").strip(),
        "verbetes_no_texto": row.get("verbetes_no_texto", "").strip(),
        "verbetes_do_tema": row.get("verbetes_do_tema", "").strip(),
        "total_de_itimos": row.get("total_de_itimos", "").strip(),
        "qtd_de_variacoes": row.get("qtd_de_variacoes", "").strip(),
        "qtd_cientifica": row.get("qtd_cientifica", "").strip(),
    }

def _dados_vivos_do_tema(nome_tema):
    """Recalcula a realidade do tema e do yPoema no instante do Help."""
    dados_tema = {"verbetes_no_texto": 0, "total_itimos": 0, "total_verbetes": 0}
    poema = st.session_state.get("ypoema_analise", "")
    dados_tema["verbetes_no_texto"] = len(_palavras_visiveis(poema))

    path = _help_find_ypo_file(nome_tema)
    if not path or not os.path.exists(path):
        return dados_tema

    try:
        with open(path, encoding="utf-8") as arquivo:
            for linha in arquivo:
                if not linha.startswith("|"):
                    continue
                campos = linha.rstrip("\n").split("|")
                if len(campos) < 8:
                    continue
                try:
                    dados_tema["total_itimos"] += max(0, int(str(campos[5]).strip()))
                except Exception:
                    pass
                payload = [itimo for itimo in campos[7:-1] if itimo != ""]
                for itimo in payload:
                    dados_tema["total_verbetes"] += len(_palavras_visiveis(itimo))
    except Exception:
        pass
    return dados_tema

def _grandeza_index(valor):
    """Mantém o número do INDEX e corrige somente sua palavra de grandeza."""
    texto = str(valor or "").strip()
    if not texto:
        return ""

    match = re.fullmatch(r"([0-9][0-9.,]*)(?:\s*\([^)]*\))?", texto)
    if not match:
        return texto

    numero_texto = match.group(1)
    digitos = re.sub(r"[^0-9]", "", numero_texto).lstrip("0") or "0"
    numero = int(digitos)

    grandezas = [
        (10**33, "decilhões", "decilhão"),
        (10**30, "nonilhões", "nonilhão"),
        (10**27, "octilhões", "octilhão"),
        (10**24, "septilhões", "septilhão"),
        (10**21, "sextilhões", "sextilhão"),
        (10**18, "quintilhões", "quintilhão"),
        (10**15, "quadrilhões", "quadrilhão"),
        (10**12, "trilhões", "trilhão"),
        (10**9, "bilhões", "bilhão"),
        (10**6, "milhões", "milhão"),
        (10**3, "mil", "mil"),
    ]

    for limite, plural, singular in grandezas:
        if numero >= limite:
            palavra = singular if numero == limite else plural
            return f"{numero_texto} ({palavra})"

    return numero_texto


def _qtd_variacoes_rodape_ypo(nome_tema):
    """Fallback: lê a quantidade de variações já registrada no rodapé do próprio tema."""
    path = _help_find_ypo_file(nome_tema)
    if not path or not os.path.exists(path):
        return ""

    try:
        with open(path, encoding="utf-8-sig") as arquivo:
            apos_eof = False
            for raw in arquivo:
                linha = str(raw or "").strip()
                if linha == "<EOF>":
                    apos_eof = True
                    continue
                if not apos_eof:
                    continue

                match = re.match(r"^Qtd\.\s*de\s*Variações\s*=\s*(.+?)\s*$", linha, flags=re.IGNORECASE)
                if match:
                    return _grandeza_index(match.group(1))
    except Exception:
        pass

    return ""


def _qtd_variacoes_index(nome_tema):
    """Lê o INDEX; se faltar o tema, usa o rodapé vigente do próprio .ypo."""
    tema_key = _md_nome_chave(str(nome_tema or ""))
    if not tema_key:
        return ""

    try:
        for raw in load_index():
            linha = str(raw or "").strip()
            if not linha:
                continue

            nome, separador, valor = linha.partition(" : ")
            if not separador:
                continue
            if _md_nome_chave(nome) != tema_key:
                continue

            return _grandeza_index(valor)
    except Exception:
        pass

    return _qtd_variacoes_rodape_ypo(nome_tema)

def _build_seal_from_ypo(nome_tema):
    """Lê o selo build_by real do tema, sem inventar assinatura paralela."""
    path = os.path.join("./data", str(nome_tema or "").strip() + ".ypo")
    try:
        with open(path, encoding="utf-8-sig") as file:
            for raw in file:
                line = str(raw or "").strip()
                if line.casefold().startswith("build_by lay_2_ypo"):
                    selo = line
        return locals().get("selo", "")
    except (OSError, UnicodeError):
        return ""

def update_help_info(nome_tema):
    """Ficha Técnica é uma visão do DNA; não recalcula cadastro em paralelo."""
    info = _help_info_estavel(nome_tema)
    if not info or not info.get("titulo"):
        return []
    linhas = [f"Título: {info.get('titulo') or nome_tema}"]
    if info.get("livro"):
        linhas.append(f"Livro: {info['livro']}")
    if info.get("banco_tematico"):
        linhas.append(f"Banco temático: {info['banco_tematico']}")
    if info.get("versos"):
        linhas.append(f"Versos: {_fmt_numero_leitor(info['versos'])}")
    if info.get("verbetes_no_texto"):
        linhas.append(f"Verbetes no Texto: {_fmt_numero_leitor(info['verbetes_no_texto'])}")
    if info.get("verbetes_do_tema"):
        linhas.append(f"Verbetes do Tema: {_fmt_numero_leitor(info['verbetes_do_tema'])}")
    if info.get("total_de_itimos"):
        linhas.append(f"Total de ítimos: {_fmt_numero_leitor(info['total_de_itimos'])}")
    if info.get("qtd_de_variacoes"):
        linhas.append(f"Qtd. de Variações: {_fmt_numero_leitor(info['qtd_de_variacoes'])}")
    selo = _build_seal_from_ypo(nome_tema)
    if selo:
        linhas.append(selo)
    return linhas

def render_matrix_ficha_tecnica_ypoemas(tema):
    """Mostra Matrix à esquerda e Ficha Técnica à direita, sem vazar HTML/base64."""
    tema = str(tema or "").strip()
    if not tema:
        return

    linhas_info = update_help_info(tema)
    if st.session_state.lang != "pt":
        linhas_info = [translate(linha) for linha in linhas_info]

    matrix_image = _matrix_image_for_theme(tema)

    if linhas_info:
        linhas_html = "".join(
            f"<div class='machina-ficha-line'>{html.escape(linha)}</div>"
            for linha in linhas_info
        )
    else:
        linhas_html = "<div class='machina-ficha-line'>Ficha Técnica não encontrada em base/DNA.TXT.</div>"

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
    return translate("♫ ouvir a leitura do texto")

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
    trecho = str(trecho or "").casefold()
    for line in str(raw_text or "").splitlines():
        if trecho and trecho in line.casefold():
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

def load_temas(book):  # List of themes inside a Book
    """DNA ÚNICO: lista temas do livro sem consultar rol_*.txt."""
    return dna_core.temas_do_livro(book, include_testes=True)

@st.cache_data
def load_info(nome_tema):
    """Compatibilidade de apresentação: lê exclusivamente o DNA."""
    row = dna_core.registro(nome_tema)
    if not row:
        return "nonono"
    linhas = [
        f"Titulo: {row.get('tema', nome_tema)}",
        f"Livro: {row.get('livro', '')}",
        f"Banco temático: {row.get('banco_tematico', '')}",
        f"Versos: {row.get('versos', '')}",
        f"Verbetes no texto: {row.get('verbetes_no_texto', '')}",
        f"Verbetes do Tema: {row.get('verbetes_do_tema', '')}",
        f"• Banco de Ítimos: {row.get('total_de_itimos', '')}",
        f"Qtd. de Variações: {row.get('qtd_de_variacoes', '')}",
    ]
    return "<br><br><br>" + "<br>".join(linhas) + "<br>"

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
    lypo_user = "LYPO_" + ip
    with open(os.path.join("./temp/" + lypo_user), encoding="utf-8", errors="replace") as script:
        for line in script:
            line = line.strip()
            lypo_text += line + "<br>"

    return lypo_text

def load_typo():  # Load translated yPoema & clean translator returned bugs in text
    typo_text = ""
    typo_user = "TYPO_" + ip
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
    return off_livros_list

def _off_book_path(book):
    """Localiza o arquivo .Pip sem depender da caixa da extensão."""
    book = str(book or "").strip()
    off_dir = _project_path("off_machina")
    for ext in (".Pip", ".pip", ".PIP"):
        path = os.path.join(off_dir, book + ext)
        if os.path.isfile(path):
            return path
    return os.path.join(off_dir, book + ".Pip")

def _off_book_has_catalog(book):
    """Confere a primeira linha física do .Pip, tolerando BOM, caixa e espaços externos."""
    try:
        with open(_off_book_path(book), encoding="utf-8-sig") as file:
            primeira = file.readline().rstrip("\r\n").lstrip()
    except Exception:
        return False
    esperado = "|Dados de Catalogação na Publicação Internacional||"
    return primeira.casefold().startswith(esperado.casefold())

def load_off_book(book):  # Load selected off_book
    book_full = []

    with open(_off_book_path(book), encoding="utf-8-sig") as file:
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
    lypo_user = "LYPO_" + ip

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
    fonte_palco = _fonte_palco_leitor()
    corpo_palco = _corpo_palco_leitor()
    return f"""
        <style>
        .machina-off-text,
        .machina-off-text p,
        .machina-off-text div,
        .machina-off-text span {{
            font-family: '{fonte_palco}' !important;
            font-size: {corpo_palco}px !important;
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
    qtd = fix_qtd_copias(qtd)

    partes = []
    atual = _ypoema_html_to_text(curr_ypoema)

    for num in range(1, qtd + 1):
        if num == 1 and atual:
            texto = atual
        else:
            texto = _gerar_ypoema_texto_cru(nome_tema)

        texto = _remover_titulo_inicial_duplicado(texto, nome_tema)

        partes.append(
            f"___\n\n"
            f"{nome_tema} #{num}\n\n"
            f"{texto}"
        )

    return ("\n".join(partes).strip() + "\n___").strip()

def count_pacote_copias(texto, qtd_real=None):
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

def copy_pacote_button(texto, token):
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
                white-space:nowrap;" title="variações">
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

def show_pacote_copias(texto, token, qtd_real=None):
    """Mostra o pacote completo para conferência e fallback de cópia."""
    if not texto:
        return

    texto = str(texto)
    total_blocos = count_pacote_copias(texto, qtd_real)

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

RETRATO_ORIGEM_URL = "ypoemas.streamlit.app"
RETRATO_SELO_SIZE = 40
RETRATO_SELO_RESPIRO = 30

# yP original incorporado ao executável para que a assinatura viaje com o PNG
# sem depender de arquivo externo. A geometria dos pixels é preservada.
RETRATO_YP_B64 = "AAABAAEAQEAAAAEAIAAoQgAAFgAAACgAAABAAAAAgAAAAAEAIAAAAAAAAEAAAIy4AACMuAAAAAAAAAAAAAD///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////7//v////7///////7////+/////v////7////9/v////7//////v/+//3//v7///7+/f/+/v3//P7+//7+/v/7/v3//f79//3+/v///v////////7////+/////////////////v///P////7//v///////v////7////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////+/////P////7////+//7////+//3//v/9//7///79//79/P/++/z//vv9//77/f/////////////////////////////////9/////Pz8//79/P/9/Pv///39//7//v/8//////7///z////8//7///////3////+/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////v////z////+//////7///z+/f/9/Pz//vz9//////////////////7////8////8+7v//Do6P/x6en/8erp//Hq6f/w5ub/9/n4///////////////////////8/////Pz8//79+//8//z/+v/////+///9//7//v/+//7////+//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////7//v/+/f7//fz+//36/P/////////////////3+ff/6NjU/9mqpP/Ndm//03lx/79IRP+1PTn/tUA6/7k+Of+5QTf/tjwz/8lbVP/VeHP/0oF9/9y8t//w5eP//f7//////////////v3///v6+//+/f3//f/+/////v/+/////f/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////9/f3/+vv7////////////9vPw/9+3tf/Jgn7/xFJL/8A2Lv+2MSr/vUU//7pDP//RdW7/1YJ7/9OAeP/TgHj/0396/9SEf//FY13/uEA7/7lCOv+2Lib/wD42/8ViWv/Ok43/5s3L//z//v/////////+//77+//7/////f/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////+/Pz////////////v6ub/3ayn/8NRTP+9LCf/uzw1/8FnYP/Vl5P/58fG//Xu7v/z7u///f//////////////////////////////+fz7//Pv7f/x5uP/5bi2/8mFgP+/WVL/vTIr/7oxLP/LbGj/3bCs//f69v///////v7///z9/P/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////9/////f/////9/v/9+/z///////v8/P/UmJX/vUU7/7YwJ/+/VlL/2aSj/+7g3f/8//////////////////////////7+/v/+/Pz//vz9//78/f/+/f3//vz8/////////////////////////////fr8/+XNzf/RjYj/vEE7/7guJ//EW1T/3bq0//3//////////fz6//7+/f/9//7///////7////9/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////f////z+/P/9/////////+bJxv/DY1n/vyso/8VmYv/ixMD/9/X1///////+/////f39///7/P/+/Pz///7+///+/v////////////////////////////////////7///7+//7+/v/+/Pz//v38//////////////////Dp5P/XqKL/wEpH/70uJv/Ne3T/7+Dh///////8/P3//P39/////v/9/v///f7////////////////////////////////////////////////////////////////////////////////////////////////////////////////+//78+v//////+/z8/9CXkv+6NzD/vEI7/9aemv/7///////////////4+/v//Pz8///9/v/6/////f///////v///////////////////////////////////////////////////////f////7//////v7/+/z8//77/f////////////Ty8P/OioT/vTQs/7lBN//gvrf///////v////+/fz//v/+///+//////////////////////////////////////////////////////////////////////////////////////////////////////////////38+///////9/L0/8dnZP+8KSL/ynp1//Dq5////////P38//z7/P/8/v7//f/////+///7////+v/////+///+//7///////////////////////////////////////////////////////3////+/////v/+//7//f/9//7///z+//76/P/+/////////+fMy//AWVL/uTUq/9OWkv/+//////////v8+//9//////////////////////////////////////////////////////////////////////////////////////////////////////////77/P//////6tXU/8FbV/+5Myr/1J+X//3//////////////////////f7//Pv8//z////+/////v/////+/////v///f///////////////////////////////////////////////////////////v///P////z////+//7//f/9//3//v/9//7/+/77///8/P//////9/b4/8p0cP+4KyX/xnFt//n49v///////f38///////////////////////////////////////////////////////////////////////////////////////+/////v////38+///////69vX/75FPv++Qzr/3L24///////8/f3/3dzd/8rLy//X2Nj////////////+/v7//v7+///////+/////f////7///////////////////////////////////////////////////////////////7//////v////7///7+///+/////f/+//3+/////v//+/v6///////6+vr/0pGL/74wJ//Cc2z/+/38///////9/f3///////7////+//////////////////////////////////////////////////////////////////7//v7///38/P//////7uLe/8FMRf+/Pzn/59DM///////+/P3/+fn5/ygoJ/8AAAD/Dw8P/z8/P/+tra3////////////9/f3////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////+/f3//v/////////QmpL/vS0k/8x6eP/9/////v7+//z8/f/8/v7//f7///3////+//////////////////////////////////////////////////////////v9/P/+////9+/x/8BTUf+7OzX/5MfC///////5+fr///////v7+/8eHh7/AAAA/wMDA/8AAAD/AAAA/3d3d///////+/v7/////////////////////////////////////////////v7+//z8/P/8/Pz//Pz8//v7+//8/Pz///////////////////////////////////////////////////////z9/v/7/fz//////9GNjv+8KyX/y4uE///////5+/z//f/6///+/v/9/v///v/////////////////////////////////////////////////////+///8/vz//v///9CHhP+6MCj/37u2///////8+/v//v7+///////5+/v/Hh4e/wAAAP8BAQH/BQUF/wYGBv8AAAD/oqKi///////7+/v//////////////////////////////////v7+//////////////////////////////////7+/v///////////////////////////////////////////////////v///f39//78/v/+////zn94/7o0Kf/iwb7///////z8+v/+/v/////////////////////////////////////////////////////////////++vz//////9y7tf+4LiX/zIJ5///////+/f7//f////3+/v/9////+vr6/yYmJv8AAAD/DQ0N/wQEBP8CAgL/AAAA/w4ODv/Hx8f///////z8/P/+/v7//////////////////v7+///////u7u7/vr6+/7a2tv+2trb/srKy/8TExP///////v7+//////////////////////////////////////////////////7////3/fn///////Hp6f++UUn/u0I6/+3d3f///////Pz9//3////////////////////////////////////////////////////+/v7///////bx7v+7TUb/xmFc//r+/P///////f79///+///9/////v////z+/f/m5ub/5eXl/9LS0v88PDz/AAAA/wcHB/8AAAD/Wlpa///////8/Pz//v7+//////////////////39/f//////z8/P/wAAAP8AAAD/AAAA/wAAAP8nJyf///////7+/v////////////////////////////7+/v////////////3////+//7//v/+//r7+v//////6NXT/7k5MP/Icmz////////+/v/+/v////////////////////////////////////////3////+//7///v9///////SjIX/vC8o/9+9vv///////fv6///////+////////////////////////////////////3t7e/wsLC/8AAAD/AgIC/wwMDP/CwsL///////z8/P/+/v7//v7+///////9/f3//////9LS0v8AAAD/BAQE/wYGBv8AAAD/Kioq///////+/v7////////////////////////////+/v7////////////9///////+///+///9////+/z7///////UlJL/uTEo/9q0sv///////fv7/////////////////////////////f////7////+/////Pz8///////lzc3/ujYu/8t7c///////+v38//7+/v////////////////////////////7+/v/+/v7/+Pj4//////+IiIj/AAAA/wgICP8AAAD/h4eH///////6+vr//v7+//7+/v///////f39///////R0dH/AAAA/wEBAf8CAgL/AAAA/ygoKP///////v7+///////////////////////////////////////////////////////////////////+/v//////8+zq/75HQP/DWFL/9/r2///////+/v7///////////////////////v////9//////7///78+//8////0Hdz/74xLP/l0c3///////v7+v///v7///////////////////////////////////////z8/P//////x8fH/wAAAP8FBQX/AAAA/zY2Nv///////f39//////////////////39/f//////0NDQ/wAAAP8BAQH/AgIC/wAAAP8tLS3///////7+/v/+/v7//////////////////////////////////////////////////////////////////vz7///////brqv/ty8n/+C0sv///////fz8//////////////////////////7//v/+//79/f//////79jV/783Mf/Pgnz//v/////9/f////7////////////////////////////////////////////9/f3//////9DQ0P8BAQH/AAAA/wMDA/8AAAD/uLi4///////8/Pz////////////9/f3//////9DQ0P8AAAD/AQEB/wMDA/8AAAD/MDAw///////+/v7///////////////////////////////////////////////////////z8/P/+/v7///////z+/v/+////+Pb3/8JUSf/IYF7//P///////v///////////////////////v///////v/9+/z//////9alnP+6Miv/59DM///////9/Pz//P///////v///////////////////////////////////////f39///////Z2dn/BwcH/wAAAP8EBAT/AAAA/1ZWVv//////+/v7/////////////f39///////R0dH/AAAA/wEBAf8CAgL/AAAA/ycnJ//////////////////////////////////////////////////////////////////+/v7////////////6//7//Pr7///////TjYf/ujky/+3Z1v///////v39//////////////////3///////7//v7////////IaGD/vU9J//j29f////7//P78//z///////7///////////////////////////////////////z8/P//////x8fH/wAAAP8BAQH/AgIC/wAAAP8UFBT/7e3t///////+/v7///////39/f//////0dHR/wAAAP8BAQH/AgIC/wAAAP8pKSn///////v7+//8/Pz//f39//v7+//8/Pz//v7+/////////////////////////////////////////////v////38/P//////6trX/7w2LP/PkI3///////78/P///////////////////v///P79///////v49//vjsz/9Sbmf///////vz7//z//v/+///////////////////////////////////////////////8/Pz//////5WVlf8AAAD/AgIC/wAAAP8CAgL/AAAA/8jIyP///////Pz8///////9/f3//////9HR0f8AAAD/AQEB/wICAv8AAAD/Jycn///////////////////////////////////////6+vr//Pz8//7+/v///////////////////////////////////v7///////z+/v/CYVn/x1pT//z+/f////////79//3////+/////v////v9/P//////16qn/7YyKv/qx8f///////37+//+///////////////////////////////////////////////+/v7///////r6+v8nJyf/AAAA/wICAv8AAAD/BAQE/wAAAP9oaGj///////v7+////////f39///////R0dH/AAAA/wEBAf8BAQH/AAAA/xQUFP/Y2Nj/lpaW/0dHR/+Dg4P/l5eX/6qqqv/z8/P////////////7+/v//////////////////////////////v///v/+//v8/P//////yYeA/7w/Nv/v5eP///////39+//+//////7///3////8/Pz//////9aEgv+9QDr/8+3r///////+/f3///////7////+/////////////////////f39//7+/v///////Pz8//////+mpqb/AAAA/wMDA/8AAAD/AAAA/wICAv8AAAD/Gxsb//f39////////v7+//39/f//////0dHR/wAAAP8BAQH/AQEB/wAAAP8LCwv/NTU1/wAAAP8AAAD/AAAA/wAAAP8AAAD/Hh4e/2dnZ//c3Nz///////v7+////////////////////////v////7////+/P3//////+i8uP+4MCr/38G////////6/Pr///7///7////9/v7//v////r/+//EYVv/ymhj//v////+///////////////+/////f////////////////////////////////////v7+///////YGBg/wAAAP8EBAT/AAAA/wAAAP8AAAD/AgIC/wAAAP+urq7///////z8/P/9/f3//////9HR0f8AAAD/AQEB/wAAAP8BAQH/AAAA/wAAAP8EBAT/AwMD/wEBAf8DAwP/AwMD/wAAAP8AAAD/GRkZ/9vb2///////+/v7///////////////////////+/////f7+///////z7ur/vEM7/9aMh////////fz7//7////+//7//v79///////5+fb/uUlB/897dv///////vz8//7////+/////v////7///////////////////////////////39/f//////5OTk/x8fH/8AAAD/AgIC/wEBAf8CAgL/AAAA/wMDA/8AAAD/R0dH///////8/Pz//f39///////R0dH/AAAA/wEBAf8AAAD/AAAA/wAAAP8CAgL/AAAA/wAAAP8CAgL/AQEB/wAAAP8BAQH/BwcH/wAAAP8UFBT/tLS0///////7+/v//////////////////f////3+/v//////8/Hy/7pEPP/Zhn////////37+//+/////v/+//79/f//////79/c/7w+Nv/WnZj///////79/P/+/////f////7////////////////////////////////////7+/v//////5OTk/8AAAD/BQUF/wEBAf8AAAD/AAAA/wEBAf8BAQH/AAAA/xsbG//x8fH///////z8/P//////0dHR/wAAAP8BAQH/AAAA/wAAAP8AAAD/AAAA/wEBAf8CAgL/AAAA/wAAAP8DAwP/AQEB/wAAAP8FBQX/AAAA/x8fH//w8PD///////39/f////////////3////9//7//v39///////Pc2r/vlZO//f6+//+/////v7+/////v/+/Pz//////+bDwf+4Lyb/48XB///////+/Pz//////////////////////////////////////////////////Pz8//////89PT3/AAAA/wQEBP8AAAD/QUFB/zU1Nf8AAAD/AwMD/wQEBP8AAAD/lZWV///////5+fn//////9HR0f8AAAD/AQEB/wAAAP8AAAD/AAAA/wICAv8BAQH/AAAA/x0dHf8ODg7/AAAA/wAAAP8BAQH/AAAA/wICAv8AAAD/X19f//z8/P///////v7+///////9/////v/+//78/f//////0394/7tJQv/39vf///////7+/v///////fz8///////rxsX/tzIo/96/u////////vz8/////////////////////////////////////////////Pz8///////BwcH/AAAA/wEBAf8AAAD/AAAA/6ysrP+np6f/AAAA/wUFBf8CAgL/AAAA/yYmJv/t7e3////////////Q0ND/AAAA/wEBAf8AAAD/AAAA/wEBAf8CAgL/AAAA/5OTk//+/v7/6enp/3d3d/8HBwf/AQEB/wAAAP8BAQH/AAAA/wAAAP+ysrL///////z8/P///////f///////v/+/f3//////9J8df+8TET/+Pf4///////+/v7///////38/P//////7MXE/7gxKP/dwbz///////78/P////////////////////////////////////////////z8/P//////R0dH/wAAAP8FBQX/AAAA/wsLC//IyMj//////zg4OP8AAAD/BAQE/wAAAP8FBQX/0tLS////////////0NDQ/wAAAP8BAQH/AAAA/wAAAP8CAgL/AAAA/5GRkf//////////////////////tLS0/xgYGP8AAAD/AQEB/wMDA/8AAAD/X19f///////8/Pz///////3///////7//vz8///////SfHX/vEtE//j29////////v7+///////+/Pz//////+nHxf+5MSj/38C7///////+/fz//////////////////////////////////v7+//v7+///////1dXV/wEBAf8BAQH/AwMD/wAAAP8mJib/7e3t//////+dnZ3/AAAA/wUFBf8DAwP/AAAA/4+Pj////////////9HR0f8AAAD/AQEB/wAAAP8DAwP/AAAA/1hYWP///////Pz8//7+/v/9/f3/+vr6//////+Ghob/AgIC/wICAv8EBAT/AAAA/yQkJP/w8PD///////39/f/9///////+//78/P//////03t1/71MRf/49/j///////7+/v///////fv8///////jxsP/tjAm/+XAvf///////vz8///////////////////////////////////////6+vr//////2VlZf8AAAD/BQUF/wQEBP8AAAD/eXl5///////+/v7/9PT0/yAgIP8AAAD/BQUF/wAAAP8oKCj/9fX1///////Q0ND/AAAA/wEBAf8AAAD/BQUF/wAAAP95eXn///////r6+v////////////z8/P//////7u7u/ycnJ/8AAAD/BAQE/wICAv8BAQH/ycnJ///////8/Pz//f///////v/++/v//////9d9eP+7R0D/9/X2///////+/v7///////z9/v//////9ezr/71GPf/SiYb////////9/P////7//P////3////////////////////8/Pz//////8LCwv8AAAD/AgIC/wEBAf8CAgL/AAAA/8XFxf//////+Pj4//////+pqan/AAAA/wQEBP8EBAT/AAAA/56env//////zc3N/wAAAP8BAQH/AAAA/wQEBP8AAAD/hISE///////7+/v/////////////////+vr6//////+AgID/AAAA/wQEBP8CAgL/AAAA/8DAwP///////Pz8///////8/v7///////X19v+/Ukz/y2li//r////+//7///7+///////9/v7///////f3+P+2SUD/1X12///////7/fz//v////7////+/////////////////////v7+//////8zMzP/AAAA/wcHB/8FBQX/AAAA/x8fH//z8/P///////7+/v/9/f3//////ysrK/8AAAD/BgYG/wAAAP9KSkr//////87Ozv8AAAD/AQEB/wAAAP8EBAT/AAAA/4uLi///////+/v7//////////////////v7+///////k5OT/wAAAP8FBQX/AAAA/wYGBv/R0dH///////39/P/+////+v7+///////18vH/t0Q6/9WHgP//////+/v5///+/////v////7////+/v/9////znFp/75aUv/6/Pz//v////z+/////v///v///////////////v7+///////39/f/Dw8P/wAAAP8AAAD/AAAA/wAAAP9WVlb///////z8/P//////+/v7//////+dnZ3/AAAA/wcHB/8FBQX/AAAA/6enp//h4eH/AAAA/wEBAf8AAAD/AwMD/wAAAP+QkJD///////v7+//////////////////7+/v//////6CgoP8AAAD/BAQE/wMDA/8AAAD/ubm5///////8/Pv//f////39/f//////8eXh/7k/N//YmZX///////78+v///v///f/////////9/Pz//////9aKhv+6PDT/7+Ph///////9/P3/+/////3////+////////////////////+vr6/3p6ev8+Pj7/TExM/05OTv9CQkL/y8vL///////9/f3///////39/f//////7u7u/x0dHf8AAAD/AAAA/wAAAP9wcHD/zs7O/wAAAP8BAQH/AAAA/wQEBP8AAAD/d3d3///////7+/v/////////////////+/v7//////+bm5v/AAAA/wQEBP8DAwP/AAAA/7q6uv///////Pv8//3////9/P3//////92rpv+3MCr/5MzJ///////8/Pr///7///3////9//7//fz8///////fvLv/uS8p/+TAu////////vn6///+/////v///v////////////////////7+/v/////////////////////////////////+/v7//////////////////f39///////BwcH/kJCQ/5OTk/+SkpL/0dHR/87Ozv8DAwP/AQEB/wAAAP8EBAT/AAAA/3h4eP//////+vr6//////////////////v7+///////kZGR/wAAAP8FBQX/AwMD/wAAAP+5ubn///////v7+//9/////vz9///////HfHX/xUM+//Xu7f/8////+/78///+///+//7//P/+///9/v//////9e7t/8JEP//RgoH//P////z9/P/+/v////////////////////////7+/v/+/v7//Pz8//v7+//7+/v//Pz8//v7+//8/Pz////////////////////////////9/f3////////////////////////////T09P/CwsL/wAAAP8BAQH/AwMD/wAAAP9GRkb///////39/f/////////////////7+/v//////5SUlP8AAAD/BQUF/wICAv8AAAD/u7u7///////8/Pz///79///////3+ff/w1FN/8hpYv/9/////v79//7+/f///v///P/+///+///9/////v39///////JeXL/ukI7//Pv7//+/////v78///+///+//7///////////////////////////////////////////////////////////////////////////////////////z8/P/7+/v/+/v7//n5+f//////z8/P/woKCv8CAgL/AAAA/wICAv8AAAD/ICAg//39/f//////////////////////+/v7//////+ZmZn/AAAA/wUFBf8CAgL/AAAA/7+/v///////+/z7//38+///////48TA/7wyK//hu7b///////78/P////////////7////+/v///f/+//77/P//////3rWv/74uKP/drq3///////z7+////v///v/+///////////////////////////////////////////////////////////////////////////////////////////////////////9/f3//////9HR0f8BAQH/AQEB/wAAAP8AAAD/AgIC/wAAAP+/v7////////n5+f/+/v7///////j4+P//////goKC/wAAAP8EBAT/AwMD/wAAAP+6u7v///////j7+v/8+fz//////858dP/APzr/9Ono///////+/v7//////////////////f////3////9/f7///////Hn5P/CRUD/x1xU//n5+f/+/////f/+/////v///////////////////////////////////////////////////////////////////////////////////////////////////////f39///////Q0ND/AAAA/wICAv8AAAD/AAAA/wQEBP8AAAD/QEBA////////////////////////////3d3d/w0NDf8AAAD/AgIC/wAAAP8NDQ3/5OTk///////9+/v//////+zm4P++RTv/zHVz//7////+/v7///////////////////////3////9/v///v7///77/P//////0JSQ/7cwJv/huLj///////v7+v/9/v7///////////////////////////////////////////////////////////////////////////////////////////////////////39/f//////0dHR/wICAv8BAQH/AQEB/wEBAf8BAQH/AQEB/wAAAP8sLCz/uLi4//j4+P/5+fn/1dXV/x0dHf8AAAD/AwMD/wMDA/8AAAD/OTk5///////+/v7//fv8///////Le3b/vjEr/+fNy////////f39///////////////////////////////////////+/v7//v////b28/++T0j/xVxX//n69////////v39///////////////////////////////////////////////////////////////////////////////////////////////////////9/f3//////9PT0/8LCwv/AQEB/wEBAf8CAgL/AQEB/wAAAP8CAgL/AAAA/w4ODv8zMzP/JSUl/wUFBf8AAAD/AwMD/wAAAP8EBAT/AAAA/1xcXP//////+/n5///////q29b/wjg0/815dP/9/////P39//7///////////////////////////////3////7/////v/+//78/P//////2qun/7otI//RnZr///////38/P/+///////////////+/////////////////////////////////////////////////////////////////////////////////////f39///////R0dH/AQEB/wEBAf8BAQH/AwMD/wQEBP8AAAD/AAAA/wQEBP8AAAD/AAAA/wAAAP8AAAD/AwMD/wAAAP8AAAD/BQYG/wAAAP9ra2v///////r6+v//////y3Vu/7o6M//t4N7///////78/P/////////////////////////////////+/////v///////////////f7+//3////Ea2X/vDw1/+zc2f//////+/z8/////////v///v7///////////////////////////////////////////////////////////////////////////////////39/f//////0NDQ/wAAAP8BAQH/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AQEB/wICAv8CAgL/AQEB/wAAAP8AAAD/AgEB/wAAAP8AAAD/0s/Q///////+////3bGt/7kvJf/QlIv///////37/f/+//3///////////////////////////////////////////////////////z8/P//////6djV/7s8Nv/DX1n/+v37///////+/fz//P////7+///+/v/////////////////////////////////////////////////////////////////////////////9/f3//////9LS0v8HBwf/AQEB/wEBAf8AAAD/AQEB/wQEBP8CAgL/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AgIC/wQDA/8AAAD/goOA///////+////5s/N/7o4Mv/CXFn/9fTy///////7/v3//P/////////////////////////////////////////////////////////9/////Pv7///////Zran/uS0k/9OSi////////P3+//z9/v/9/////f///////////////////////////////////////////////////////////////////////////////f39///////Pz8//AAAA/wQEBP8AAAD/AwMD/wAAAP8AAAD/AAAA/wUFBf8CAgL/AgIC/wICAv8DAwP/BQUF/wAAAP8AAAD/cnBx///////8////9PPu/8VcVv+7Qzn/7+Ti///////7/fn//f/+///+/////////////////////////////////////////////////////////v7///3+/f/+/////f///8d6df+8LSX/1ZqU/////////f///f35//7+/f////////////////////////////////////////////////////////////////////////////39/f//////zc3N/wAAAP8AAAD/BQUF/wAAAP8oKCj/j4+P/ysrK/8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8UFBT/hoeH//z8/P//////9vbz/8lmX//AMCn/2bOr///////8+/v////+//3+///+//7////+///////////////////////////////////////////////////+/////v//+/39///////8/fv/ym9t/7svKv/Yop3//////////v/9+/v////////////////////////////////////////////////////////////////////////////9/f3//////9nZ2f9OTk7/JCQk/zo6Ov8qKir/gICA///////p6Oj/YmJi/x4eHv8qKir/HBwc/z4+Pv+ampr/5eXl////////////+fv4/8Ruav+7Lij/2aii///////9+/v//P77//3+///+/////v/+///////////////////////////////////////////////////////9//7//f7////+///9/fz///////j49//CaWP/wCwh/8x5dv/7//////////38+////v7//f/+//////////////////////////////////7////////////////////////////////////+/v7///////7+/v/6+vr//v7+///+///5+vv////////////7+/v//f3+//r4+f///////////////v//////697b/8BhW//ALSb/05+Y///////9+/7//v79//7//f/////////+//////////////////////////////////////////////////////////////////////////////////79/f//////+ff1/9CLhP+8Lif/yGtm/+/g3/////////7+//v8/P/+/////v7///3////8//7//f/+///////+//////////////////////////////////////////7+/v////////////////////7//v/+//39/v/7+/v///////7//v/+//7/9/r6//v9/v//////4L66/8JIQf+6Ozb/37e0///////8/v3//P78/////////////////////////////////////////////////////////////////////////////////////////////////////////////fz9////////////zpmP/743LP/BQz//27Sy//3//////////fz9//z9/P///vz//f/+//7//v///v////7///7//////////////////////////////////////////v7+//7+/v///v///f/9//3//v/+/////v7///3+/v/9+/v//P39///////07+3/1JqY/7w2MP++TEP/4sXD///////9/Pz//f36///+/f////////////////////////////////////////////////////////////////////////////////////////////////////////////7////6/f3//v79///////lyMf/w1VL/7ouJf/HbGj/7uLg/////////////f////v7/P/+/P7//P7///z//v////7////////////////////////////////////////////////////////9///9/P///Pz8//j8+v////////////7////fvbv/wE1F/7ksI//Kd3L/8+vq///////8+/n////9//3////9/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////f/+//7//v/7+/z///////Pw7v/Rlo7/vjYv/8A+Nf/IeXL/5czL//n8/P////////////r//v/9+/r//vv7//78/P///v7///7+///+/v///v7///7+///+/v/+/f3//vz8//79/f/+/Pz//////////////////fz5/9qwrf/IY1v/vDMq/7pOSP/duLf//v/////////++/v////9//z+///+/v/////+//////////////////////////////////////////////////////////////////////////////////////////////////////////////////3//////v///P/+//z7+v///////////+TKx//RgHr/vD03/8EwKv/CX1j/3rKs//Hm4v/7/v7///////////////////////////////////////////////////////////////////////b39v/u2NX/1ZmU/8JXUP+5Lyf/vUlA/9OKhf/v6Of///////78/f/8/fz///////z+///8//////7///7//v////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////7//////////v79//78/f///////////+zc1//Ri4b/wlBL/7kwKv+4PTf/xWJc/9WSjv/ixcH/4MPB//Xv7f/7+fn/+fb3//n39//49vb//Pv5/+ve3P/fwr//4bm2/9OAe//AU03/uDYx/70zMP/FX1r/1aef//Xw7v////////////38+//+//7////+//////////////////7////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////9/////f39//38/P////////////f08//iwcL/04J//8JYUf+3ODD/ti8n/7UvJv/ESED/xk5I/8RMRv/GTUX/xU1F/8hPR/+/Pjb/tCwk/7kzKf+4QDb/ymdg/9SWkP/o2dT//f/9/////////////v39//7+/v////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////7///3////8/////vz9//77+v/////////////////4+/j/7drZ/9+urf/isK7/yHV0/79oY//AbGb/w2pl/8RsZv/AZWH/04yJ/+WysP/it7b/8ejo//r///////////////z////7+/z///7+//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////7///////////7///3+///8//////79//38/P/8/P3///////////////////////////////////////7//////////v/////////////////////////9//7//fz8//77/f/9/f///f7//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////v////7//////////v7///7////9//////7////9/v/7/f3/+/z7//77+//+/v3///79///9/v/+/f7///7+//7+/v/9/f3//vz7//78+v/8/v3///7+//7//v/8//7//f/+//7//v////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////7//////////////v////7//////v///v///////v/+//7/+//////+///+/v//+/////3+///+/v///f/+//7//////v////////3////6/////v////7+/////////f////7+/v/+/v7/////////////////////////////////////////////////////////////////////////////////////////////////////////////////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="

def _retrato_logo_yp(size):
    """Retorna o yP original no tamanho de teste, sem suavizar seus pixels."""
    try:
        raw = base64.b64decode(RETRATO_YP_B64)
        with Image.open(BytesIO(raw)) as source:
            logo = ImageOps.exif_transpose(source).convert("RGBA")
        return logo.resize((int(size), int(size)), Image.Resampling.NEAREST)
    except Exception:
        return None

def _aplicar_selo_origem(canvas, size, respiro=RETRATO_SELO_RESPIRO, family=None):
    """Assina o Retrato com yP + endereço de origem no canto inferior direito."""
    logo = _retrato_logo_yp(size)
    if logo is None:
        return canvas

    draw = ImageDraw.Draw(canvas)
    url_font = _retrato_font(max(16, int(round(size * 0.72))), family=family)
    url = RETRATO_ORIGEM_URL
    bbox = draw.textbbox((0, 0), url, font=url_font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    gap = max(8, int(round(size * 0.35)))

    group_w = size + gap + text_w
    pos_x = canvas.width - int(respiro) - group_w
    pos_y = canvas.height - int(respiro) - size

    canvas.paste(logo, (pos_x, pos_y), logo)
    text_y = pos_y + max(0, (size - text_h) // 2) - bbox[1]
    draw.text((pos_x + size + gap, text_y), url, font=url_font, fill=(45, 45, 45))
    return canvas

def _retrato_font(size, bold=False, family=None):
    """Carrega no PNG a fonte escolhida em Fontes & Letras."""
    family = str(family or "Trebuchet MS").strip()

    # Arquivos mais prováveis no Windows e no Linux/Streamlit Cloud.
    nomes = {
        "Trebuchet MS": ("trebucbd.ttf", "trebuc.ttf"),
        "Inter": ("Inter-Bold.ttf", "Inter-Regular.ttf"),
        "Spectral": ("Spectral-Bold.ttf", "Spectral-Regular.ttf"),
        "EB Garamond": ("EBGaramond-Bold.ttf", "EBGaramond-Regular.ttf"),
        "Libre Baskerville": ("LibreBaskerville-Bold.ttf", "LibreBaskerville-Regular.ttf"),
        "Cormorant Garamond": ("CormorantGaramond-Bold.ttf", "CormorantGaramond-Regular.ttf"),
        "Palatino Linotype": ("palab.ttf", "pala.ttf"),
        "Georgia": ("georgiab.ttf", "georgia.ttf"),
        "Atkinson Hyperlegible": ("AtkinsonHyperlegible-Bold.ttf", "AtkinsonHyperlegible-Regular.ttf"),
        "OpenDyslexic": ("OpenDyslexic-Bold.otf", "OpenDyslexic-Regular.otf"),
        "JetBrains Mono": ("JetBrainsMono-Bold.ttf", "JetBrainsMono-Regular.ttf"),
        "Courier New": ("courbd.ttf", "cour.ttf"),
        "IBM Plex Sans": ("IBMPlexSans-Bold.ttf", "IBMPlexSans-Regular.ttf"),
    }

    bold_name, regular_name = nomes.get(family, ("", ""))
    filename = bold_name if bold else regular_name
    candidates = []

    if filename:
        candidates.extend([
            _project_path("fonts", filename),
            os.path.join("C:/Windows/Fonts", filename),
            filename,
        ])

    # Alguns pacotes Linux usam diretórios e nomes ligeiramente diferentes.
    linux_aliases = {
        "Inter": ["/usr/share/fonts/truetype/inter/Inter-Bold.ttf" if bold else "/usr/share/fonts/truetype/inter/Inter-Regular.ttf"],
        "EB Garamond": ["/usr/share/fonts/truetype/ebgaramond/EBGaramond-Bold.ttf" if bold else "/usr/share/fonts/truetype/ebgaramond/EBGaramond-Regular.ttf"],
        "JetBrains Mono": ["/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf"],
    }
    candidates.extend(linux_aliases.get(family, []))

    # Fallback Unicode seguro, apenas quando a fonte escolhida não existe
    # como arquivo acessível ao Pillow naquele computador.
    candidates.extend([
        _project_path("fonts", "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ])

    for candidate in candidates:
        try:
            if not candidate:
                continue
            if os.path.isabs(candidate) and not os.path.exists(candidate):
                continue
            return ImageFont.truetype(candidate, size=int(size))
        except Exception:
            pass

    try:
        return ImageFont.load_default()
    except Exception as exc:
        raise RuntimeError("Fonte Unicode não encontrada para gerar o Retrato.") from exc

def _retrato_wrap(draw, texto, font, largura):
    """Quebra o texto preservando o recuo autoral com espaços ASCII."""
    linhas_finais = []
    for linha in str(texto or "").splitlines():
        linha = linha.replace("\t", "    ")
        if not linha:
            linhas_finais.append("")
            continue

        recuo = linha[: len(linha) - len(linha.lstrip(" "))]
        conteudo = linha[len(recuo):]

        if not conteudo:
            linhas_finais.append(recuo)
            continue

        palavras = conteudo.split(" ")
        atual = recuo
        for palavra in palavras:
            if palavra == "":
                continue
            tentativa = atual + palavra if atual.endswith(" ") else atual + " " + palavra
            bbox = draw.textbbox((0, 0), tentativa, font=font)
            if bbox[2] - bbox[0] <= largura or atual == recuo:
                atual = tentativa
            else:
                linhas_finais.append(atual.rstrip())
                atual = recuo + palavra
        linhas_finais.append(atual.rstrip())
    return linhas_finais

def criar_retrato_png(ypoema_html, image_path, tema, selo_size=24):
    """Monta o Retrato com a imagem e o texto exibidos no palco."""
    if not image_path or not os.path.exists(image_path):
        return None

    texto = unicodedata.normalize("NFC", _ypoema_html_to_text(ypoema_html))
    titulo = unicodedata.normalize("NFC", str(tema or "").strip())

    # O título já é desenhado no topo do Retrato, centralizado.
    # Portanto, qualquer linha do corpo que seja exatamente esse título
    # é descartada antes da composição. Conteúdo apenas parecido permanece.
    titulo_key = titulo.casefold()
    linhas_texto = []
    for linha in texto.splitlines():
        linha_key = unicodedata.normalize("NFC", linha.strip()).casefold()
        if titulo_key and linha_key == titulo_key:
            continue
        linhas_texto.append(linha)
    texto = "\n".join(linhas_texto)

    def _limpar_recuo_retrato(linha):
        prefixo = []
        pos = 0
        while pos < len(linha):
            ch = linha[pos]
            if ch == " ":
                prefixo.append(" ")
                pos += 1
                continue
            if ch == "\t":
                prefixo.append("    ")
                pos += 1
                continue
            if ch == "\u00A0" or "\u2000" <= ch <= "\u200A" or ch in ("\u202F", "\u205F", "\u3000"):
                prefixo.append("  ")
                pos += 1
                continue
            break
        return "".join(prefixo) + linha[pos:]

    texto = "\n".join(_limpar_recuo_retrato(linha) for linha in texto.splitlines())
    if not texto:
        return None

    margin = 64
    gap = 58
    fonte_retrato = _fonte_palco_leitor()
    # No Retrato, a família tipográfica segue "Fontes & Letras",
    # mas o corpo do texto fica fixo para manter presença visual.
    corpo_png = 40
    body_font = _retrato_font(corpo_png, family=fonte_retrato)
    title_font = _retrato_font(max(corpo_png + 4, int(round(corpo_png * 1.18))), family=fonte_retrato)

    medida = Image.new("RGB", (1, 1), "white")
    draw_medida = ImageDraw.Draw(medida)
    text_w_max = 900

    with Image.open(image_path) as source:
        art = ImageOps.exif_transpose(source).convert("RGB")
        image_w, image_h = art.size

    linhas = _retrato_wrap(draw_medida, texto, body_font, text_w_max)
    bbox_linha = draw_medida.textbbox((0, 0), "Ag", font=body_font)
    line_gap = max(8, int(round(corpo_png * 0.28)))
    line_h = max(1, bbox_linha[3] - bbox_linha[1]) + line_gap
    altura_texto = max(line_h, len(linhas) * line_h)

    larguras_linhas = []
    for linha in linhas:
        if linha:
            bbox = draw_medida.textbbox((0, 0), linha, font=body_font)
            larguras_linhas.append(max(1, bbox[2] - bbox[0]))
    largura_texto_real = max(larguras_linhas or [1])

    selo_real = max(1, int(round(int(selo_size) * 0.60)))
    footer_font = _retrato_font(max(16, int(round(selo_real * 0.72))), family=fonte_retrato)
    footer_bbox = draw_medida.textbbox((0, 0), RETRATO_ORIGEM_URL, font=footer_font)
    footer_text_w = footer_bbox[2] - footer_bbox[0]
    footer_gap_x = max(8, int(round(selo_real * 0.35)))
    footer_group_w = selo_real + footer_gap_x + footer_text_w
    footer_h = selo_real
    footer_gap_y = 34

    text_area_w = max(largura_texto_real, 420)
    top_content_w = image_w + gap + text_area_w
    largura_conteudo = margin + top_content_w + margin
    largura_rodape = margin + footer_group_w + margin
    canvas_w = max(700, largura_conteudo, largura_rodape)

    title_gap = 28
    title_h = 0
    if titulo:
        title_bbox = draw_medida.textbbox((0, 0), titulo, font=title_font)
        title_h = max(1, title_bbox[3] - title_bbox[1])
    content_h = max(image_h, altura_texto)
    content_top = margin + (title_h + title_gap if titulo else 0)
    canvas_h = max(520, content_top + content_h + footer_gap_y + footer_h + margin)

    canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
    draw = ImageDraw.Draw(canvas)
    if titulo:
        title_bbox = draw.textbbox((0, 0), titulo, font=title_font)
        title_w = max(1, title_bbox[2] - title_bbox[0])
        draw.text(((canvas_w - title_w) // 2, margin), titulo, font=title_font, fill="black")

    image_y = content_top + max(0, (content_h - image_h) // 2)
    canvas.paste(art, (margin, image_y))
    text_area_x = margin + image_w + gap
    pos_y = content_top + max(0, (content_h - altura_texto) // 2)
    for linha in linhas:
        if linha:
            bbox = draw.textbbox((0, 0), linha, font=body_font)
            line_w = max(1, bbox[2] - bbox[0])
        else:
            line_w = 0
        text_x = text_area_x + max(0, (text_area_w - line_w) // 2)
        draw.text((text_x, pos_y), linha, font=body_font, fill="black")
        pos_y += line_h

    _aplicar_selo_origem(canvas, selo_real, RETRATO_SELO_RESPIRO, family=fonte_retrato)
    output = BytesIO()
    canvas.save(output, format="PNG", optimize=True)
    return output.getvalue()

def load_images():
    """Compatibilidade exclusiva do Off-Machina; temas não consultam images.txt."""
    images_list = []
    path = os.path.join("./base", "images.txt")
    if not os.path.exists(path):
        return images_list
    with open(path, encoding="utf-8-sig") as lista:
        images_list.extend(lista.readlines())
    return images_list

def load_arts(nome_tema):  # Select image for arts
    """Banco visual do tema vem exclusivamente do DNA."""
    nome_tema = str(nome_tema or "").strip()
    grupo = dna_core.banco_do_tema(nome_tema) or "machina"
    path = "./images/" + grupo + "/"
    if not os.path.isdir(path):
        return None
    arts_list = [
        file for file in os.listdir(path)
        if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ]
    if not arts_list:
        return None
    available_arts = [image for image in arts_list if image not in st.session_state.arts]
    if not available_arts:
        available_arts = arts_list
    image = random.choice(available_arts)
    st.session_state.arts.append(image)
    return path + image

def load_image_tema(nome_tema):
    """Define a imagem Machina contextual do tema atual para a sidebar.

    A curadoria existente continua valendo: tema == grupo de imagens.
    O destino visual muda: a imagem acompanha na sidebar, não no palco.
    """
    logo = load_arts(nome_tema)
    st.session_state["save_image_tema"] = logo or ""
    return logo or ""

def _resolve_off_machina_book_image(book_name):
    """Localiza capa_<info_book>.jpg com comparação segura de caixa/Unicode."""
    info_book = os.path.splitext(os.path.basename(str(book_name or "").strip()))[0]
    if not info_book:
        return ""

    wanted = ("capa_" + info_book + ".jpg").casefold()
    dirs = [

        _project_path("images", "anima"),
        _project_path("images"),
        _project_path("off_machina"),
        _project_path("off-machina"),
        _project_path("images", "off_machina"),
        _project_path("images", "off-machina"),
        _project_path("images", "livros"),
        _project_path("images", "books"),
    ]
    for folder in dirs:
        if not os.path.isdir(folder):
            continue
        for real_name in os.listdir(folder):
            if real_name.casefold() == wanted:
                path = os.path.join(folder, real_name)
                if os.path.isfile(path):
                    return path
    return ""

def _images_from_group(group_name):
    """Lista imagens do grupo indicado, sem inferir ou alterar curadoria."""
    group_dir = os.path.join("./images", str(group_name or "").strip())
    images = []
    if os.path.isdir(group_dir):
        for file in sorted(os.listdir(group_dir)):
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                images.append(os.path.join(group_dir, file))
    return images

def _set_group_sidebar_image_next(group_name, state_key):
    """Escolhe a próxima imagem de um grupo para a sidebar."""
    images = _images_from_group(group_name)
    if not images:
        st.session_state[state_key] = ""
        return ""

    previous = st.session_state.get(state_key, "")
    available = [img for img in images if img != previous]
    chosen = random.choice(available or images)
    st.session_state[state_key] = chosen
    return chosen

def _image_group_for_entity(entity_name, fallback="machina"):
    """Resolve entidade -> banco visual em base/images.txt, com fallback saudável."""
    wanted = str(entity_name or "").strip().casefold()
    for raw in load_images():
        left, sep, right = str(raw or "").strip().partition(" : ")
        if sep and left.strip().casefold() == wanted and right.strip():
            return right.strip()
    return str(fallback or "machina").strip() or "machina"

def _set_about_image_next():
    grupo = _image_group_for_entity("ABOUT", "author")
    return _set_group_sidebar_image_next(grupo, "about_image")

def _set_off_anima_image_next():
    return _set_group_sidebar_image_next("anima", "off_machina_images_pasta")

def _off_book_image_group(book_name):
    wanted = str(book_name or "").strip()
    for raw in load_images():
        line = str(raw or "").strip()
        left, sep, right = line.partition(" : ")
        if sep and left.strip().casefold() == wanted.casefold() and right.strip():
            return right.strip()
    return ""

def _set_off_book_group_image_next(book_name):
    grupo = _off_book_image_group(book_name)
    if not grupo:
        st.session_state["off_machina_images_pasta"] = ""
        return ""
    return _set_group_sidebar_image_next(grupo, "off_machina_images_pasta")

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
    if (
        str(chosen_id) != "4"
        and str(st.session_state.get("voz_analise", "Machina")).upper() == "OLA"
    ):
        return

    if not bool(st.session_state.get("draw", True)):
        return

    image_path = ""

    if str(chosen_id) in {"1", "2", "3"}:
        image_path = st.session_state.get("save_image_tema", "")
    elif str(chosen_id) == "4":

        image_path = st.session_state.get("off_machina_images_pasta", "")

    elif str(chosen_id) == "5":
        image_path = st.session_state.get("about_image", "") or _set_about_image_next()
    if image_path and os.path.exists(image_path):
        # Autoridade do que o leitor realmente viu. O clique em Retrato usa
        # esta cópia estável antes de qualquer renovação da imagem contextual.
        st.session_state["sidebar_image_visible_path"] = image_path
        render_sidebar_image_fit(image_path)
    else:
        st.session_state["sidebar_image_visible_path"] = ""

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
    fonte = st.session_state.get("fonte_palco", "Trebuchet MS")
    if fonte == "Trebuchet":
        fonte = "Trebuchet MS"
    return fonte

def _corpo_palco_leitor():
    """Corpo escolhido pelo leitor para o yPoema."""
    try:
        corpo = int(st.session_state.get("corpo_palco", 21))
    except Exception:
        corpo = 21
    return max(14, min(34, corpo))

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):  # ver save_img.py
    LOGO_TEXTO = _palco_titulo_centralizado(LOGO_TEXTO)

    fonte_palco = _fonte_palco_leitor()
    corpo_palco = _corpo_palco_leitor()

    logo_css = f"""
        <style>
        .logo-text {{
            font-weight: 600 !important;
            font-size: {corpo_palco}px !important;
            font-family: '{fonte_palco}' !important;
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

def talk(text):
    """Lê o yPoema no idioma atual usando edge-tts, quando disponível."""
    if edge_tts is None:
        st.warning("Motor de voz neural indisponível.")
        return

    # Limpeza para a voz não ler tags
    text_clean = text.replace("<br>", " ").replace("< br>", "").replace("<br >", "").replace("<br/>", " ")

    # Mapeamento de vozes neurais de alta qualidade
    selected_voice = vozes_tts.get(st.session_state.lang, "pt-BR-AntonioNeural")

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

if st.session_state.visy:  # check visitor once; rand initial temas
    update_visy()

    temas = load_temas("poemas")
    maxy_ypoemas = len(temas)
    st.session_state.take = random.randrange(0, maxy_ypoemas)
    st.session_state.tema = temas[st.session_state.take]

    temas = load_temas("todos os temas")
    maxy_mini = len(temas)
    st.session_state.mini = random.randrange(0, maxy_mini)

    st.session_state.draw = True
    st.session_state.visy = False

st.session_state.last_lang = st.session_state.lang

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
    if gerar_analise_ola_real is None:
        return "OLA ainda não conectada. Arquivo ponte_ola_openai.py não encontrado ou não importável."

    return limpar_analise(gerar_analise_ola_real(tipo, tema, ypoema_texto))

def gerar_analise_atual(ypoema_html, tema):
    """Envia o yPoema atual para a ponte OLA, sem simulação local."""
    kind = st.session_state.get("tipo_analise", "Sintática")
    ypoema_texto = _analise_texto_cru_do_ypoema(ypoema_html)
    return gerar_analise_ola(kind, tema, ypoema_texto)

def _analysis_voice_title(voice):
    """Expande OLA com o mesmo gerador randômico usado pelo marcador < nome_ola >."""
    if str(voice or "").strip().upper() == "OLA":
        return fala_nome_OLA().strip()
    return str(voice or "Machina").strip() or "Machina"

def _analysis_kind_label(kind):
    """Tipo da análise em caixa baixa para o subtítulo."""
    return str(kind or "").strip().casefold()

def render_analise_palco(texto):
    """Renderiza análise no palco direito, com cabeçalho padrão."""
    fonte_palco = _fonte_palco_leitor()
    corpo_palco = max(14, min(30, int(st.session_state.get("corpo_palco", 21)) - 1))

    voice = str(st.session_state.get("voz_analise", "OLA")).upper()
    kind = st.session_state.get("tipo_analise", "")
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
            font-family:'{fonte_palco}', system-ui, sans-serif;
            font-size:{corpo_palco}px;
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

def _analysis_options_for_voice(voice):
    """Retorna as análises disponíveis para a OLA."""
    return OLA_ANALYSIS_OPTIONS if str(voice or "").upper() == "OLA" else []

def _set_analysis_voice(voice):
    """Seleciona Machina ou OLA e ajusta a lista única."""
    voice_key = str(voice or "Machina").strip().upper()
    if voice_key == "OLA":
        st.session_state["voz_analise"] = "OLA"
        st.session_state["tipo_analise"] = OLA_ANALYSIS_OPTIONS[0]
    else:
        st.session_state["voz_analise"] = "Machina"
        st.session_state["tipo_analise"] = ""

def render_analysis_sidebar_block():
    """Bloco centralizado: Machina / OLA, somente com a OLA."""
    current_key = str(st.session_state.get("voz_analise", "Machina")).upper()
    if current_key not in {"MACHINA", "OLA"}:
        current_key = "MACHINA"
        st.session_state["voz_analise"] = "Machina"

    options = _analysis_options_for_voice(current_key)
    current_kind = st.session_state.get("tipo_analise", options[0] if options else "")
    if options and current_kind not in options:
        current_kind = options[0]
        st.session_state["tipo_analise"] = current_kind

    st.sidebar.markdown("<div style='height:1.85rem;'></div>", unsafe_allow_html=True)
    col_machina, col_ola = st.sidebar.columns(2)

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
        st.sidebar.markdown("<div style='height:1.42rem;'></div>", unsafe_allow_html=True)
        choice = st.sidebar.selectbox(
            "tipo",
            options,
            index=options.index(current_kind) if current_kind in options else 0,
            key="analysis_kind_select",
            label_visibility="collapsed",
        )
        st.session_state["tipo_analise"] = choice

def render_sidebar_for_page(chosen_id):
    """Renderiza os controles fixos do leitor, sem botão arte fóssil."""
    pick_lang()
    pick_fonte_palco()
    render_analysis_sidebar_block()

def _set_machina_page(page_label, page_id):
    """Fixa a página ativa em estado explícito.

    Evita que cliques internos de uma página, especialmente a navegação
    da Off-Machina, caiam de volta no foco inicial yPoemas.
    """
    st.session_state["pick_pagina"] = page_label
    st.session_state["pagina"] = str(page_id)

def _sync_machina_page_state(page_labels, page_ids):
    """Mantém label e id coerentes sem resetar indevidamente para yPoemas."""
    ids_to_labels = {str(page_id): label for label, page_id in page_ids.items()}

    saved_id = str(st.session_state.get("pagina", "")).strip()
    saved_label = st.session_state.get("pick_pagina", "")

    if saved_id in ids_to_labels:
        _set_machina_page(ids_to_labels[saved_id], saved_id)
        return

    if saved_label in page_labels:
        _set_machina_page(saved_label, page_ids[saved_label])
        return

    _set_machina_page("yPoemas", page_ids["yPoemas"])

# =============================================================================
# < Beginning Of Page > 1 — MINI
# =============================================================================
def page_mini():
    temas = load_temas("todos os temas")
    maxy_mini = len(temas)

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
        auto_clicked = st.button(
            "🔀",
            key="mini_auto_button",
            help="modo automático",
            use_container_width=True,
        )
        if auto_clicked:
            st.session_state.auto = not st.session_state.auto

    with voz_col:
        if st.button("♫", key="mini_voz_btn", help=help_talk, use_container_width=True):
            st.session_state.talk = not st.session_state.talk

    # Pedido: o botão ? deve existir como botão real logo após o ♫.
    with help_col:
        manu = st.button("?", key="mini_help_btn", help="Modo de Usar & Manual do Usuário", use_container_width=True)

    mini_voz_slot = render_voz_slot()

    if more or rand or auto_clicked or manu:
        limpar_retrato("mini")

    if st.session_state.auto:
        st.session_state.talk = False
        with st.sidebar:
            wait_time = st.slider(translate("tempo de exibição (em segundos): "), 5, 60, label_visibility="collapsed")

    if rand:
        st.session_state.rand = True
        st.session_state.mini = random.randrange(0, maxy_mini)
    else:
        st.session_state.rand = False

    st.session_state.tema = temas[st.session_state.mini]

    if more:
        st.session_state.rand = False

    lnew = not manu
    if manu:
        render_manual_mini()

    if lnew or st.session_state.auto:
        if st.session_state.rand:
            st.session_state.mini = random.randrange(0, maxy_mini)
            st.session_state.tema = temas[st.session_state.mini]

        mini_contexto = (int(st.session_state.get("mini", 0)), str(st.session_state.get("tema", "")), str(st.session_state.get("lang", "pt")))
        preservar_mini = bool(st.session_state.pop("mini_retrato_keep_palco", False))
        usou_xerox_mini = bool(preservar_mini and tuple(st.session_state.get("mini_palco_xerox_context") or ()) == mini_contexto and st.session_state.get("mini_palco_xerox_text"))
        if usou_xerox_mini:
            curr_ypoema = st.session_state.get("mini_palco_xerox_text", "")
        elif st.session_state.lang != st.session_state.last_lang:
            curr_ypoema = load_lypo()  # changes in lang, keep LYPO
        else:
            curr_ypoema = load_poema(st.session_state.tema, "")
            curr_ypoema = load_lypo()

        if st.session_state.lang != "pt" and not usou_xerox_mini:  # translate if idioma <> pt
            curr_ypoema = translate(curr_ypoema)
            typo_user = "TYPO_" + ip
            with open(
                os.path.join("./temp/" + typo_user), "w", encoding="utf-8"
            ) as save_typo:
                save_typo.write(curr_ypoema)
                save_typo.close()
            curr_ypoema = load_typo()  # to normalize line breaks in text

        update_readings(st.session_state.tema)
        LOGO_TEXTO = curr_ypoema
        if not st.session_state.pop("mini_retrato_sidebar_renovada", False):
            load_image_tema(st.session_state.tema)

        mini_status = (
            "🍃  "
            + st.session_state.lang
            + " - "
            + st.session_state.tema
            + " ( "
            + str(st.session_state.mini + 1)
            + " / "
            + str(len(temas))
            + " )"
        )
        mini_expander = st.expander(mini_status, expanded=True)
        with mini_expander:
            mini_place_holder = st.empty()
            mini_place_holder.empty()
            st.write("")

            if st.session_state.auto == False:
                if not show_retrato_no_topo("mini"):
                    with mini_place_holder:
                        write_ypoema(LOGO_TEXTO, None)

                st.session_state["mini_palco_xerox_text"] = LOGO_TEXTO
                st.session_state["mini_palco_xerox_title"] = st.session_state.tema
                st.session_state["mini_palco_xerox_image"] = st.session_state.get("save_image_tema", "")
                st.session_state["mini_palco_xerox_context"] = mini_contexto
                if st.session_state.get("mini_contexto_retrato") and tuple(st.session_state.get("mini_contexto_retrato")) != mini_contexto:
                    _limpar_retrato_contextual("mini")
                show_copy_retrato_xerox("mini", _ypoema_html_to_text(LOGO_TEXTO))

                if st.session_state.talk:
                    with mini_voz_slot:
                        talk(curr_ypoema)

            else:
                while st.session_state.auto:
                    if st.session_state.rand:
                        st.session_state.mini = random.randrange(0, maxy_mini)
                        st.session_state.tema = temas[st.session_state.mini]

                    if st.session_state.lang != st.session_state.last_lang:
                        curr_ypoema = load_lypo()  # changes in lang, keep LYPO
                    else:
                        curr_ypoema = load_poema(st.session_state.tema, "")
                        curr_ypoema = load_lypo()

                    if st.session_state.lang != "pt":  # translate if idioma <> pt
                        curr_ypoema = translate(curr_ypoema)
                        typo_user = "TYPO_" + ip
                        with open(
                            os.path.join("./temp/" + typo_user), "w", encoding="utf-8"
                        ) as save_typo:
                            save_typo.write(curr_ypoema)
                            save_typo.close()
                        curr_ypoema = load_typo()  # to normalize line breaks in text

                    update_readings(st.session_state.tema)
                    LOGO_TEXTO = curr_ypoema
                    load_image_tema(st.session_state.tema)

                    with mini_place_holder:
                        mini_place_holder.empty()
                        write_ypoema(LOGO_TEXTO, None)
                        secs = wait_time
                        while secs >= 0:
                            time.sleep(1)
                            secs -= 1


# =============================================================================
# < End Of Page > 1 — MINI
# =============================================================================

# =============================================================================
# < Beginning Of Page > 2 — yPOEMAS
# =============================================================================
def page_ypoemas():
    sync_livro_tema()
    temas = load_temas(_current_book())
    maxy_ypoemas = len(temas) - 1
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
        pick_livro_palco()

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

    if more or last or rand or nest or manu:
        limpar_retrato("ypo")

    temas = load_temas(_current_book())
    maxy_ypoemas = len(temas) - 1
    if st.session_state.take > maxy_ypoemas or st.session_state.take < 0:
        st.session_state.take = 0

    # Âncora estável: usada pelo ✚ para evitar que qualquer callback de lista
    # troque tema antes da geração de "mais uma versão do mesmo tema".
    if not st.session_state.get("ypo_keep_book"):
        st.session_state["ypo_keep_book"] = _current_book()
        st.session_state["ypo_keep_take"] = int(st.session_state.get("take", 0))
        st.session_state["ypo_keep_tema"] = st.session_state.get("tema", "")

    if more:
        # ✚ = recarregar / mais uma versão do mesmo tema.
        # Usa a última âncora estável, não o eventual valor alterado por callback.
        frozen_book = st.session_state.get("ypo_keep_book", _current_book())
        frozen_take = int(st.session_state.get("ypo_keep_take", st.session_state.get("take", 0)))
        frozen_tema = st.session_state.get("ypo_keep_tema", st.session_state.get("tema", ""))
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
        sync_livro_tema()
        next_tema_key()

    if rand:
        limpar_copias_palco()
        st.session_state.take = random.randrange(0, maxy_ypoemas + 1)
        sync_livro_tema()
        next_tema_key()

    if nest:
        limpar_copias_palco()
        st.session_state.take += 1
        if st.session_state.take > maxy_ypoemas:
            st.session_state.take = 0
        sync_livro_tema()
        next_tema_key()

    with col_temas:
        pick_tema_palco()

    temas = load_temas(_current_book())
    sync_livro_tema()

    if more:
        frozen_book = st.session_state.get("more_same_book", _current_book())
        frozen_take = int(st.session_state.get("more_same_take", st.session_state.get("take", 0)))
        frozen_tema = st.session_state.get("more_same_tema", "")
        st.session_state.book = frozen_book
        st.session_state.take = frozen_take
        if frozen_tema:
            st.session_state.tema = frozen_tema
        temas = load_temas(_current_book())
        maxy_ypoemas = len(temas) - 1
        if st.session_state.take > maxy_ypoemas or st.session_state.take < 0:
            st.session_state.take = 0
            st.session_state.tema = temas[0] if temas else ""

    lnew = True
    if manu:
        render_help_ypoemas_com_ficha()
        lnew = False

    if lnew:
        what_book = (
            "🍃  "
            + st.session_state.lang
            + " ( "
            + _current_book()
            + " ) ( "
            + str(st.session_state.take + 1)
            + " / "
            + str(len(temas))
            + " )"
        )

        ypoemas_expander = st.expander(what_book, expanded=True)
        with ypoemas_expander:
            ypo_contexto = (str(_current_book()), int(st.session_state.get("take", 0)), str(st.session_state.get("tema", "")), str(st.session_state.get("lang", "pt")))
            preservar_ypo = bool(st.session_state.pop("ypo_retrato_keep_palco", False))
            usou_xerox_ypo = bool(preservar_ypo and tuple(st.session_state.get("ypo_palco_xerox_context") or ()) == ypo_contexto and st.session_state.get("ypo_palco_xerox_text"))
            if usou_xerox_ypo:
                curr_ypoema = st.session_state.get("ypo_palco_xerox_text", "")
            elif st.session_state.lang != st.session_state.last_lang:
                curr_ypoema = load_lypo()  # changes in lang, keep LYPO
            else:
                curr_ypoema = load_poema(st.session_state.tema, "")
                curr_ypoema = load_lypo()

            if st.session_state.lang != "pt" and not usou_xerox_ypo:  # translate if idioma <> pt
                curr_ypoema = translate(curr_ypoema)
                typo_user = "TYPO_" + ip
                with open(
                    os.path.join("./temp/" + typo_user), "w", encoding="utf-8"
                ) as save_typo:
                    save_typo.write(curr_ypoema)
                    save_typo.close()
                curr_ypoema = load_typo()  # to normalize line breaks in text

            update_readings(st.session_state.tema)

            st.session_state.ypoema_analise = curr_ypoema
            st.session_state.tema_analise = st.session_state.tema
            st.session_state.livro_analise = _current_book()
            st.session_state.take_analise = st.session_state.take
            st.session_state.lang_analise = st.session_state.lang

            st.session_state["more_same_book"] = ""
            st.session_state["more_same_take"] = -1
            st.session_state["more_same_tema"] = ""
            st.session_state["ypo_keep_book"] = _current_book()
            st.session_state["ypo_keep_take"] = int(st.session_state.get("take", 0))
            st.session_state["ypo_keep_tema"] = st.session_state.get("tema", "")

            LOGO_TEXTO = curr_ypoema
            if not st.session_state.pop("ypo_retrato_sidebar_renovada", False):
                load_image_tema(st.session_state.tema)

            analysis_voice_atual = str(st.session_state.get("voz_analise", "Machina")).upper()

            if show_retrato_no_topo("ypo"):
                pass
            elif analysis_voice_atual == "OLA":
                analise_texto = gerar_analise_atual(LOGO_TEXTO, st.session_state.tema)

                col_poema, col_analise = st.columns([1.05, 0.95], gap="large")
                with col_poema:
                    write_ypoema(LOGO_TEXTO, None)
                with col_analise:
                    render_analise_palco(analise_texto)
            else:
                write_ypoema(LOGO_TEXTO, None)

            st.session_state["ypo_palco_xerox_text"] = LOGO_TEXTO
            st.session_state["ypo_palco_xerox_title"] = st.session_state.get("tema", "")
            st.session_state["ypo_palco_xerox_image"] = st.session_state.get("save_image_tema", "")
            st.session_state["ypo_palco_xerox_context"] = ypo_contexto
            if st.session_state.get("ypo_contexto_retrato") and tuple(st.session_state.get("ypo_contexto_retrato")) != ypo_contexto:
                _limpar_retrato_contextual("ypo")
            show_copy_retrato_xerox("ypo", _ypoema_html_to_text(LOGO_TEXTO))

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

# =============================================================================
# < End Of Page > 2 — yPOEMAS
# =============================================================================

# =============================================================================
# < Beginning Of Page > 3 — EUREKA / ACROS
# =============================================================================
def _hide_eureka_help():
    """Fecha o Help da página Eureka quando o leitor volta à busca/lista."""
    st.session_state["help_eureka_open"] = False

def _on_eureka_find_change():
    """Nova busca limpa Help e Retrato anteriores."""
    _hide_eureka_help()
    limpar_retrato("eureka")

def _on_eureka_occurrence_change():
    """Selecionar outra ocorrência limpa Help e Retrato anteriores."""
    _hide_eureka_help()
    limpar_retrato("eureka")
    try:
        st.session_state.eureka = int(st.session_state.get("opt_ocur_key", st.session_state.get("eureka", 0)))
    except Exception:
        st.session_state.eureka = 0

def _acros_resultado_html(resultado):
    """Converte o resultado ACROS em HTML seguro para o palco da Eureka."""
    linhas = []
    for linha in resultado.linhas:
        if linha.verbete is None:
            linhas.append(html.escape(linha.markdown))
            continue

        entrada = html.escape(str(linha.entrada).upper())
        restante = html.escape(linha.verbete[1:] if len(linha.verbete) > 1 else "")
        linhas.append("<strong>" + entrada + "</strong> " + restante)

    return "<br>".join(linhas)


def _acros_fechar():
    """Encerra a aparição ACROS e limpa o estado que pertence a ela."""
    _limpar_retrato_contextual("acros")
    st.session_state["acros_on"] = False
    st.session_state["acros_html"] = ""
    st.session_state["acros_texto"] = ""
    st.session_state["acros_entrada"] = ""
    st.session_state["acros_modo_pedido"] = "Bem"
    st.session_state["acros_genero_pedido"] = "Masculino"
    st.session_state["acros_imagem"] = ""
    st.session_state["acros_poetico_pedido"] = False
    st.session_state["acros_open"] = False


def _acros_gerar_encontro(entrada, modo, genero, poetico=False):
    """Gera a aparição ACROS no modo Simples ou Poético, no mesmo território visual."""
    _limpar_retrato_contextual("acros")
    gerador = gerar_akros if poetico else gerar_acros
    resultado = gerador(
        entrada=entrada,
        modo=modo,
        genero=genero,
        base_dir=_project_path("data", "acros"),
    )

    st.session_state["acros_on"] = True
    st.session_state["acros_html"] = _acros_resultado_html(resultado)
    st.session_state["acros_texto"] = resultado.texto
    st.session_state["acros_entrada"] = entrada
    st.session_state["acros_modo_pedido"] = modo
    st.session_state["acros_genero_pedido"] = genero
    st.session_state["acros_poetico_pedido"] = bool(poetico)

    # O Retrato usa a imagem normal da Machina; nenhuma regra visual própria.
    tema_contexto = st.session_state.get("tema", "Fatos") or "Fatos"
    imagem = load_image_tema(tema_contexto)
    st.session_state["acros_imagem"] = imagem
    _hide_eureka_help()


def _acros_abrir():
    """🍒 recebe o visitante ACROS sem apagar o estado da Eureka."""
    _acros_fechar()
    _hide_eureka_help()
    st.session_state["acros_nome"] = ""
    st.session_state["acros_key"] = int(st.session_state.get("acros_key", 0)) + 1
    st.session_state["acros_open"] = True


def _render_acros_cereja():
    """🍒 abre uma entrada ACROS limpa, sem manter aparições anteriores."""
    st.button(
        "🍒",
        key="acros_cereja",
        help="acrósticos",
        use_container_width=True,
        on_click=_acros_abrir,
    )


def _acros_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()


def clean_acros_input(nome_anterior):
    """Click/tap mantém; a primeira nova letra substitui o nome/texto anterior."""
    nome_anterior = str(nome_anterior or "")
    if not nome_anterior:
        return

    nome_js = json.dumps(nome_anterior, ensure_ascii=False)
    components.html(
        f"""
        <script>
        (function() {{
            const parentDoc = window.parent.document;
            const inputs = Array.from(parentDoc.querySelectorAll('input'));
            const input = inputs.find(el =>
                el.getAttribute('aria-label') === 'nome para o acróstico'
                || el.getAttribute('placeholder') === 'digite um nome:'
            );
            if (!input) return;

            const anterior = {nome_js};
            if (input.value !== anterior) return;
            if (input.dataset.acrosCleanReady === '1') return;

            input.dataset.acrosCleanReady = '1';

            const cleanOnFirstLetter = function(ev) {{
                const isLetter =
                    ev.key &&
                    ev.key.length === 1 &&
                    !ev.ctrlKey &&
                    !ev.metaKey &&
                    !ev.altKey;

                if (!isLetter) return;
                if (input.value !== anterior) {{
                    input.removeEventListener('keydown', cleanOnFirstLetter);
                    input.dataset.acrosCleanReady = '0';
                    return;
                }}

                input.select();
                input.removeEventListener('keydown', cleanOnFirstLetter);
                input.dataset.acrosCleanReady = '0';
            }};

            input.addEventListener('keydown', cleanOnFirstLetter);
        }})();
        </script>
        """,
        height=0,
    )


def _render_acros_painel_eureka():
    """Cabine ACROS compacta e alinhada; resultado cresce abaixo na mesma largura."""
    acros_html = st.session_state.get("acros_html", "")
    acros_texto = st.session_state.get("acros_texto", "")
    tem_resultado = bool(acros_html)

    # Mantém as escolhas coerentes com o último acróstico gerado.
    modo_atual = st.session_state.get("acros_modo_pedido", "Bem")
    modo_ui_default = "bondades" if modo_atual == "Bem" else '"maldades"'
    if st.session_state.get("acros_modo") not in ("bondades", '"maldades"'):
        st.session_state["acros_modo"] = modo_ui_default

    salvar_sem_retrato = False
    retrato = False

    margem_esq, palco_centro, margem_dir = st.columns([1.1, 8.8, 1.1])
    with palco_centro:
        try:
            painel = st.container(border=True)
        except TypeError:
            painel = st.container()

        with painel:
            st.markdown(
                """
                <style>
                /* ACROS — hints inferiores flutuantes, sem alterar a altura da cabine. */
                div[data-testid="stElementContainer"]:has(.acros-hint-marker) {
                    display: none !important;
                }

                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-copy) button,
                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-more) button,
                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-retrato) button,
                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-salvar) button {
                    position: relative !important;
                    overflow: visible !important;
                }

                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-copy) button::after,
                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-more) button::after,
                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-retrato) button::after,
                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-salvar) button::after {
                    position: absolute;
                    top: calc(100% + 0.28rem);
                    left: 50%;
                    transform: translateX(-50%);
                    z-index: 9999;
                    padding: 0.22rem 0.42rem;
                    border-radius: 0.35rem;
                    background: rgba(49, 51, 63, 0.96);
                    color: white;
                    font-size: 0.72rem;
                    font-weight: 400;
                    line-height: 1.15;
                    white-space: nowrap;
                    pointer-events: none;
                    opacity: 0;
                    visibility: hidden;
                    transition: opacity 0.10s ease;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.22);
                }

                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-copy) button::after {
                    content: "copiar texto";
                }
                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-more) button::after {
                    content: "gerar novo acróstico";
                }
                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-retrato) button::after {
                    content: "mostrar retrato";
                }
                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-salvar) button::after {
                    content: "salvar retrato";
                }

                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-copy) button:hover::after,
                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-more) button:hover::after,
                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-retrato) button:hover::after,
                div[data-testid="stElementContainer"]:has(+ div[data-testid="stElementContainer"] .acros-hint-salvar) button:hover::after {
                    opacity: 1;
                    visibility: visible;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            # Linha 1: nome + bolo + porta de saída sempre visível.
            nome_col, bolo_col, sair_col = st.columns([7.2, 1.0, 1.6])
            with nome_col:
                entrada = st.text_input(
                    "nome para o acróstico",
                    key="acros_nome",
                    placeholder="digite um nome:",
                    label_visibility="collapsed",
                )
                clean_acros_input(st.session_state.get("acros_entrada", ""))
            with bolo_col:
                gerar = st.button(
                    "✅",
                    key="acros_gerar",
                    help="gerar acróstico",
                    use_container_width=True,
                )
            with sair_col:
                sair = st.button(
                    "Sair",
                    key="acros_sair",
                    use_container_width=True,
                )

            st.markdown("<div style='height:0.35rem'></div>", unsafe_allow_html=True)

            # Linha 2: cinco pares verticais alinhados.
            genero_col, modo_col, leitura_col, acao1_col, acao2_col = st.columns([1.8, 1.9, 1.7, 1.5, 1.5])

            with genero_col:
                genero = st.radio(
                    "gênero",
                    ["Feminino", "Masculino"],
                    key="acros_genero",
                    label_visibility="collapsed",
                )

            with modo_col:
                escolha_modo = st.radio(
                    "modo",
                    ["bondades", '"maldades"'],
                    key="acros_modo",
                    label_visibility="collapsed",
                )
                modo = "Bem" if escolha_modo == "bondades" else "Mal"

            with leitura_col:
                leitura = st.radio(
                    "leitura",
                    ["Simples", "Poético"],
                    key="acros_leitura",
                    label_visibility="collapsed",
                )
                poetico = leitura == "Poético"

            with acao1_col:
                if tem_resultado:
                    with st.popover("Copiar", use_container_width=True):
                        st.code(str(acros_texto or ""), language=None, wrap_lines=True)
                    st.markdown('<span class="acros-hint-marker acros-hint-copy"></span>', unsafe_allow_html=True)
                else:
                    st.button("Copiar", key="acros_copiar_vazio", use_container_width=True, disabled=True)
                    st.markdown('<span class="acros-hint-marker acros-hint-copy"></span>', unsafe_allow_html=True)

                mais = st.button(
                    "✚ Mais",
                    key="acros_nova_variacao",
                    use_container_width=True,
                    disabled=not tem_resultado,
                )
                st.markdown('<span class="acros-hint-marker acros-hint-more"></span>', unsafe_allow_html=True)

            with acao2_col:
                retrato = st.button(
                    "Retrato",
                    key="acros_retrato_btn_top",
                    use_container_width=True,
                    disabled=not tem_resultado,
                )
                st.markdown('<span class="acros-hint-marker acros-hint-retrato"></span>', unsafe_allow_html=True)

                preview_png = st.session_state.get("acros_imagem_retrato")
                if preview_png:
                    st.download_button(
                        "Salvar",
                        data=preview_png,
                        file_name=f"{st.session_state.get('acros_nome_retrato', 'retrato')}.png",
                        mime="image/png",
                        key="acros_retrato_save_top",
                        use_container_width=True,
                        on_click="ignore",
                    )
                    st.markdown('<span class="acros-hint-marker acros-hint-salvar"></span>', unsafe_allow_html=True)
                    salvar_sem_retrato = False
                else:
                    salvar_sem_retrato = st.button(
                        "Salvar",
                        key="acros_retrato_save_alert",
                        use_container_width=True,
                    )
                    st.markdown('<span class="acros-hint-marker acros-hint-salvar"></span>', unsafe_allow_html=True)

        if sair:
            _acros_fechar()
            _acros_rerun()
            return True

        if salvar_sem_retrato:
            st.warning("Retrato não gerado.")

        pedido_gerar = bool(gerar or mais)
        if pedido_gerar:
            entrada = str(entrada or "").strip()
            if not entrada:
                st.error("digite um nome ou palavra")
            else:
                try:
                    _acros_gerar_encontro(entrada, modo, genero, poetico=poetico)
                except (AcrosError, AkrosError) as exc:
                    st.error(str(exc))
                except (OSError, UnicodeError) as exc:
                    fonte_dir = _project_path("data", "acros")
                    st.error(
                        "ACROS — erro de leitura não identificado.\n"
                        f"território: {fonte_dir}\n"
                        f"detalhe: {exc}"
                    )
                else:
                    st.session_state["acros_open"] = False
                    _acros_rerun()
                    return True

        # Xerox precisa existir antes de Retrato; fica invisível para a interface.
        if tem_resultado:
            imagem = st.session_state.get("acros_imagem", "")
            st.session_state["acros_palco_xerox_text"] = acros_html
            st.session_state["acros_palco_xerox_title"] = ""
            st.session_state["acros_palco_xerox_image"] = imagem
            contexto = (
                str(st.session_state.get("acros_entrada", "")),
                str(st.session_state.get("acros_modo_pedido", "")),
                str(st.session_state.get("acros_genero_pedido", "")),
                str(acros_texto or ""),
            )
            st.session_state["acros_palco_xerox_context"] = contexto
            if st.session_state.get("acros_contexto_retrato") and tuple(st.session_state.get("acros_contexto_retrato")) != contexto:
                _limpar_retrato_contextual("acros")

            if retrato:
                make_retrato_xerox("acros")
                _acros_rerun()
                return True

            # O Retrato assume o palco. Sem Retrato ativo, o texto ACROS aparece normalmente.
            if not show_retrato_no_topo("acros"):
                _render_acros_texto(acros_html)

    return True


def _render_acros_entrada():
    """Compatibilidade interna: a entrada agora usa a mesma cabine fixa do ACROS."""
    return _render_acros_painel_eureka()



def _render_eureka_registro(texto_html, texto_copia, tema, imagem, key_prefix, sem_hints=False):
    """Copy + Retrato da Eureka; ACROS usa a mesma família de estado."""
    prefixo = "acros" if str(key_prefix).startswith("acros") else "eureka"

    st.session_state[f"{prefixo}_palco_xerox_text"] = texto_html
    st.session_state[f"{prefixo}_palco_xerox_title"] = tema
    st.session_state[f"{prefixo}_palco_xerox_image"] = imagem

    if prefixo == "eureka":
        contexto = (
            str(st.session_state.get("eureka_find", "")),
            str(tema or ""),
            str(st.session_state.get("lang", "pt")),
            str(texto_copia or ""),
        )
    else:
        contexto = (
            str(st.session_state.get("acros_entrada", "")),
            str(st.session_state.get("acros_modo_pedido", "")),
            str(st.session_state.get("acros_genero_pedido", "")),
            str(texto_copia or ""),
        )

    st.session_state[f"{prefixo}_palco_xerox_context"] = contexto

    contexto_retrato = st.session_state.get(f"{prefixo}_contexto_retrato")
    if contexto_retrato and tuple(contexto_retrato) != contexto:
        limpar_retrato(prefixo)

    show_copy_retrato_xerox(prefixo, texto_copia)

def _render_acros_texto(acros_html):
    """Renderiza ACROS como corpo puro: sem título, cabeçalho ou sublinhado."""
    fonte_palco = _fonte_palco_leitor()
    corpo_palco = _corpo_palco_leitor()
    st.markdown(
        f"""
        <div class="acros-resultado" style="
            font-family:'{fonte_palco}';
            font-size:{corpo_palco}px;
            line-height:1.35;
            font-weight:400;
            color:#000;
            width:fit-content;
            max-width:min(96ch,94%);
            margin:0 auto;
            padding:0.10rem 0.35rem 0.25rem 0.35rem;
            text-align:left;
            text-decoration:none;
        ">{acros_html}</div>
        """,
        unsafe_allow_html=True,
    )


def _render_acros_palco_eureka():
    """Compatibilidade interna: resultado e comandos vivem na cabine fixa."""
    return _render_acros_painel_eureka()

def page_eureka():
    help_tips = load_help(st.session_state.lang)
    acros_visitando = bool(
        st.session_state.get("acros_open", False)
        or st.session_state.get("acros_on", False)
    )

    # Swap de palco: durante a aparição ACROS, a faixa de comandos da Eureka
    # sai de cena inteira. Sair do ACROS apenas restaura a Eureka preservada.
    if acros_visitando:
        _hide_eureka_help()
        _render_acros_painel_eureka()
        return

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
            key="eureka_find",
            on_change=_on_eureka_find_change,
            disabled=acros_visitando,
        )

    with nav_area:
        if eureka_nav_needs_spacer:
            st.markdown(
                "<div style='height:1.95rem; min-height:1.95rem;'></div>",
                unsafe_allow_html=True,
            )

        nav_cols = st.columns([1, 1, 1, 1, 1])
        more = nav_cols[0].button("✚", help=help_more, use_container_width=True, disabled=acros_visitando)
        rand = nav_cols[1].button("✻", help=help_rand, use_container_width=True, disabled=acros_visitando)

        with nav_cols[2]:
            if acros_visitando:
                st.button("🍒", key="acros_cereja_congelada", help="acrósticos", use_container_width=True, disabled=True)
            else:
                _render_acros_cereja()

        if nav_cols[3].button("♫", key="eureka_voz_btn", help=help_talk, use_container_width=True, disabled=acros_visitando):
            _hide_eureka_help()
            st.session_state.talk = not st.session_state.talk

        manu = nav_cols[4].button("?", help="help !!!", use_container_width=True, disabled=acros_visitando)

        eureka_voz_slot = render_voz_slot()

    if more or rand or manu:
        limpar_retrato("eureka")

    if manu:
        st.session_state["help_eureka_open"] = True

    if more or rand:
        _hide_eureka_help()

    show_help_eureka = bool(st.session_state.get("help_eureka_open", False))

    if len(find_what) < 3:
        if show_help_eureka:
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

        if (not more) and (not manu) and not st.session_state.get("eureka_retrato_keep_palco", False):
            st.session_state.eureka = 0

        if len(seed_list) == 0:
            if show_help_eureka:
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
                st.session_state["opt_ocur_key"] = st.session_state.eureka

            with occurrences:
                options = list(range(len(seed_list)))
                opt_ocur_key = st.selectbox(
                    "↓  " + str(len(seed_list)) + " " + info_find,
                    options,
                    index=st.session_state.eureka,
                    format_func=lambda y: seed_list[y],
                    key="opt_ocur_key",
                    on_change=_on_eureka_occurrence_change,
                )

            previous_opt = st.session_state.get("eureka_last_ocur")
            if previous_opt is not None and previous_opt != opt_ocur_key:
                _hide_eureka_help()
                show_help_eureka = False
            st.session_state["eureka_last_ocur"] = opt_ocur_key

            if not rand:
                st.session_state.eureka = opt_ocur_key

            if show_help_eureka:
                render_manual_eureka()
                return

            this_seed = seed_list[st.session_state.eureka]
            part_line = this_seed.partition(" ➪ ")
            nome_tema = part_line[2]
            seed_tema = nome_tema.partition("_")[0]

            st.session_state.tema = seed_tema

            preservar_eureka = bool(st.session_state.pop("eureka_retrato_keep_palco", False))
            usou_xerox_eureka = bool(preservar_eureka and st.session_state.get("eureka_palco_xerox_text", ""))
            if usou_xerox_eureka:
                curr_ypoema = st.session_state.get("eureka_palco_xerox_text", "")
            elif st.session_state.lang != st.session_state.last_lang:
                curr_ypoema = load_lypo()  # changes in lang, keep LYPO
            else:
                curr_ypoema = load_poema(seed_tema, this_seed)
                curr_ypoema = load_lypo()

            if st.session_state.lang != "pt" and not usou_xerox_eureka:  # translate if idioma <> pt
                curr_ypoema = translate(curr_ypoema)
                typo_user = "TYPO_" + ip
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
                    if not st.session_state.pop("eureka_retrato_sidebar_renovada", False):
                        load_image_tema(seed_tema)

                    if not show_retrato_no_topo("eureka"):
                        write_ypoema(LOGO_TEXTO, None)
                    update_readings(seed_tema)

                _render_eureka_registro(
                    LOGO_TEXTO,
                    _ypoema_html_to_text(LOGO_TEXTO),
                    seed_tema,
                    st.session_state.get("save_image_tema", ""),
                    "eureka_tema",
                )

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

# =============================================================================
# < End Of Page > 3 — EUREKA / ACROS
# =============================================================================

# =============================================================================
# < Beginning Of Page > 4 — OFF-MACHINA
# =============================================================================
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
        limpar_retrato_off()
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

    if manu:
        limpar_retrato_off()

    if last:
        limpar_retrato_off()
        nav_changed = True
        st.session_state.off_take -= 1
        if st.session_state.off_take < 0:
            st.session_state.off_take = maxy_off_machina

    if rand:
        limpar_retrato_off()
        nav_changed = True
        st.session_state.off_take = random.randrange(0, maxy_off_machina + 1)

    if nest:
        limpar_retrato_off()
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
        limpar_retrato_off()
        st.session_state.off_take = opt_off_take

    off_sidebar_contexto = (
        int(st.session_state.get("off_book", 0)),
        int(st.session_state.get("off_take", 0)),
    )
    if st.session_state.get("off_retrato_keep_palco", False):
        # Retrato já capturou a imagem anterior e preparou a próxima para a sidebar.
        st.session_state.pop("off_retrato_sidebar_renovada", None)
    elif st.session_state.off_take == 0:
        st.session_state["off_machina_images_pasta"] = _resolve_off_machina_book_image(off_book_name)
        st.session_state["off_sidebar_image_context"] = off_sidebar_contexto
    elif (
        tuple(st.session_state.get("off_sidebar_image_context") or ()) != off_sidebar_contexto
        or not st.session_state.get("off_machina_images_pasta")
    ):
        _set_off_book_group_image_next(off_book_name)
        st.session_state["off_sidebar_image_context"] = off_sidebar_contexto

    off_retrato_contexto_atual = (
        int(st.session_state.get("off_book", 0)),
        int(st.session_state.get("off_take", 0)),
        str(st.session_state.get("lang", "pt")),
    )
    off_retrato_contexto_salvo = st.session_state.get("off_contexto_retrato")
    if off_retrato_contexto_salvo and tuple(off_retrato_contexto_salvo) != off_retrato_contexto_atual:
        limpar_retrato_off()

    preservar_palco_retrato_off = bool(
        st.session_state.pop("off_retrato_keep_palco", False)
    )

    lnew = True
    if manu:
        lnew = False
        render_manual_off_machina()

    if lnew:
        what_book = (
            "🍃  "
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
            off_xerox_contexto = (
                int(st.session_state.get("off_book", 0)),
                int(st.session_state.get("off_take", 0)),
                str(st.session_state.get("lang", "pt")),
            )
            usou_xerox_off = bool(
                preservar_palco_retrato_off
                and tuple(st.session_state.get("off_palco_xerox_context") or ()) == off_xerox_contexto
                and st.session_state.get("off_palco_xerox_text")
            )
            titulo_pip = pipe_line[1] if len(pipe_line) > 1 else ""
            if usou_xerox_off:
                off_book_text = st.session_state["off_palco_xerox_text"]
            elif str(titulo_pip).lstrip().startswith("@"):
                if st.session_state.lang != st.session_state.last_lang:
                    off_book_text = load_lypo()
                else:
                    nome_tema = str(titulo_pip).lstrip()[1:].strip()
                    off_book_text = load_poema(nome_tema, "")
                    off_book_text = "<br>" + load_lypo()
            else:
                off_book_text = _pip_line_to_text(this_off_book[st.session_state.off_take])

            capo = st.session_state.off_take == 0

            if st.session_state.lang != "pt" and not capo and not usou_xerox_off:
                off_book_text = translate(off_book_text)

            LOGO_TEXTO = off_book_text
            off_title = off_book_pagys[st.session_state.off_take]

            st.session_state.ypoema_analise = LOGO_TEXTO
            st.session_state.tema_analise = off_title
            st.session_state.livro_analise = off_book_name
            st.session_state.take_analise = st.session_state.off_take
            st.session_state.lang_analise = st.session_state.lang

            def render_off_texto():
                write_off_machina_texto(LOGO_TEXTO)

            analysis_voice_atual = str(st.session_state.get("voz_analise", "Machina")).upper()
            if show_retrato_no_topo("off"):
                pass
            elif analysis_voice_atual == "OLA":
                analise_texto = gerar_analise_atual(LOGO_TEXTO, off_title)
                col_texto, col_analise = st.columns([1.05, 0.95], gap="large")
                with col_texto:
                    render_off_texto()
                with col_analise:
                    render_analise_palco(analise_texto)
            else:
                render_off_texto()

            update_readings(off_book_name)

            st.session_state["off_palco_xerox_text"] = LOGO_TEXTO
            st.session_state["off_palco_xerox_context"] = off_xerox_contexto
            st.session_state["off_palco_xerox_title"] = off_title
            st.session_state["off_palco_xerox_image"] = st.session_state.get("off_machina_images_pasta", "")

            show_copy_retrato_xerox(
                "off",
                _off_machina_texto_limpo(LOGO_TEXTO),
            )

        if st.session_state.talk:
            with off_voz_slot:
                talk(off_book_text)

# =============================================================================
# < End Of Page > 4 — OFF-MACHINA
# =============================================================================

# =============================================================================
# < Beginning Of Page > 5 — ABOUT
# =============================================================================
def _about_candidates(title):
    """Gera nomes esperados para ABOUT_<assunto>.md sem tabela interna."""
    title = str(title or "").strip()
    candidates = []

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
        path = find_md_file(file_name)
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

def load_md_files_catalog():
    """Carrega o catálogo externo da página ABOUT.
                                                     
                                 
                                     
               
                            
                                                  
                                             

                      
                                                          
                                             
                                   
                               
                                                    
                                                         
                        

                            
                                                   
                                       
                            
                               
               


                                  
                                  
                  
                                             
                                             
     
                           
                                
                       
                        


                          
              
                                                     
                                                     
                        
                                   
                                 
                        
                                                    
                    
                                                                   
                


    Formato obrigatório de cada linha:
        texto_na_pagina_About|nome_exato_do_arquivo_em_md_files

    O primeiro campo é apenas o rótulo exibido. O segundo é usado literalmente
    para abrir o arquivo; não há filtro ABOUT_, dedução, tradução ou renomeação.
    """
    candidates = [

        _project_path("md_files.txt"),

        _project_path("base", "md_files.txt"),

    ]
    catalog = []
    for path in candidates:

        if not os.path.isfile(path):
            continue

        with open(path, encoding="utf-8") as file:

            for raw in file:
                line = raw.rstrip("\r\n")
                if not line.strip() or line.lstrip().startswith("#"):
                    continue

                if line.strip().upper() == "<EOF>":
                    break
                label, sep, file_name = line.partition("|")
                label = label.strip()
                file_name = file_name.strip()
                if not sep or not label or not file_name:
                    continue

                # O segundo campo pode conter alternativas separadas por vírgula.
                # O catálogo continua sendo a autoridade; o leitor tentará cada
                # nome na ordem informada, sem concatená-los.
                file_name = file_name.strip()
                if not file_name:
                    continue
                catalog.append((label, file_name))
        return catalog
    return catalog

def _md_catalog_name_candidates(file_spec):
    """Expande uma entrada do catálogo em nomes de arquivo tentáveis.
                         
                    

    Regras aceitas pelo catálogo real:
    - alternativas separadas por vírgula;
    - nome literal com extensão;
    - nome literal sem extensão, tentando também o mesmo nome + .md.
    """
    candidates = []
    for raw_name in str(file_spec or "").split(","):
        name = raw_name.strip().strip(chr(34)).strip(chr(39))
        if not name:
            continue
        if name not in candidates:
            candidates.append(name)
        if not os.path.splitext(name)[1]:
            with_md = name + ".md"
            if with_md not in candidates:
                candidates.append(with_md)
    return candidates

def _md_catalog_exact_path(file_name):
    """Localiza o nome do catálogo, tolerando somente Unicode e caixa."""
    requested = os.path.basename(str(file_name or "").strip())
    if not requested:
        return ""

    md_dir = _project_path("md_files")
    direct = os.path.join(md_dir, requested)
    if os.path.isfile(direct):
        return direct
    if not os.path.isdir(md_dir):
        return ""

    def canon(name):
        value = unicodedata.normalize("NFC", str(name or "")).casefold()
        return unicodedata.normalize("NFD", value)

    wanted = canon(requested)
    for real_name in os.listdir(md_dir):
        real_path = os.path.join(md_dir, real_name)
        if os.path.isfile(real_path) and canon(real_name) == wanted:
            return real_path

    # Último fallback restrito ao nome completo: ignora apenas diacríticos,
    # espaços Unicode invisíveis nas bordas e caixa. Não usa aproximação,
    # prefixo, abreviação ou comparação parcial.
    def canon_sem_diacriticos(name):
        value = unicodedata.normalize("NFKD", str(name or "")).casefold().strip()
        value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
        value = value.replace("\u200b", "").replace("\ufeff", "")
        return value

    wanted_plain = canon_sem_diacriticos(requested)
    matches = []
    for real_name in os.listdir(md_dir):
        real_path = os.path.join(md_dir, real_name)
        if os.path.isfile(real_path) and canon_sem_diacriticos(real_name) == wanted_plain:
            matches.append(real_path)

    # Só abre quando há correspondência única; em caso de ambiguidade, falha.
    if len(matches) == 1:

        return matches[0]
    return ""

def _load_md_catalog_file(file_spec):
    """Abre a primeira alternativa existente indicada por md_files.txt."""
    attempted = []
    for file_name in _md_catalog_name_candidates(file_spec):
        attempted.append(file_name)
        path = _md_catalog_exact_path(file_name)
        if not path:
            continue
        try:
            with open(path, encoding="utf-8-sig") as file:
                return translate(file.read())
        except (OSError, UnicodeError):

            continue

    return translate(
        "ooops... arquivo ( " + str(file_spec) + " ) não pode ser aberto."

    )

def page_abouts():
    catalog = load_md_files_catalog()

    if not catalog:
        st.warning(translate("md_files.txt vazio ou não encontrado"))
        return

    if not st.session_state.get("about_image"):
        _set_about_image_next()

    options = list(range(len(catalog)))
    sobrios = "↓  " + translate("sobre")
    opt_abouts = st.selectbox(
        sobrios,
        options,
        format_func=lambda x: catalog[x][0],
        key="opt_abouts",
        on_change=_set_about_image_next,
    )

    _label, file_name = catalog[opt_abouts]
    about_expander = st.expander("", True)
    with about_expander:
        st.subheader(_load_md_catalog_file(file_name))

SIDEBAR_FILHOTE_WIDTH_PX = 64
OLA_ANALYSIS_OPTIONS = [
    "Sintética",
    "Sintática",
    "Aparição",
    "Completa",
]

# =============================================================================
# < End Of Page > 5 — ABOUT
# =============================================================================

# =============================================================================
# SAÍDA / ROTEAMENTO
# =============================================================================
def main():
    gramado = open_gramado()

    with gramado:
        page_labels = ["mini", "yPoemas", "eureka", "off-Machina", "ABOUT"]
        page_ids = {
            "mini": "1",
            "yPoemas": "2",
            "eureka": "3",
            "off-Machina": "4",
            "ABOUT": "5",
        }

        _sync_machina_page_state(page_labels, page_ids)

        # Navegação MOBILE: 4 páginas principais + A/B/C/D.
        # A abre o ABOUT atual.
        # B/C/D permanecem reservados para as páginas documentais correspondentes.
        nav_items = [
            ("mini", "mini", 1.0),
            ("yPoemas", "yPoemas", 1.0),
            ("eureka", "eureka", 1.0),
            ("off-Mach", "off-Machina", 1.0),
            ("A", "ABOUT", 0.5),
            ("B", None, 0.5),
            ("C", None, 0.5),
            ("D", None, 0.5),
        ]

        page_cols = st.columns([item[2] for item in nav_items])
        for (display_label, target_label, _weight), page_col in zip(nav_items, page_cols):
            with page_col:
                selected = (
                    target_label is not None
                    and target_label == st.session_state["pick_pagina"]
                )
                clicked = st.button(
                    display_label,
                    key=f"machina_page_btn_{display_label}",
                    use_container_width=True,
                    type="primary" if selected else "secondary",
                )
                if clicked and target_label is not None:
                    limpar_retratos()
                    if st.session_state.get("acros_on", False):
                        _acros_fechar()
                    _set_machina_page(target_label, page_ids[target_label])
                    try:
                        st.rerun()
                    except AttributeError:
                        st.experimental_rerun()

        chosen_label = st.session_state["pick_pagina"]
        chosen_id = st.session_state.get("pagina", page_ids.get(chosen_label, "2"))

        if str(chosen_id) != "3" and st.session_state.get("acros_on", False):
            _acros_fechar()

        st.divider()

        render_sidebar_for_page(chosen_id)

        palco = st.container()
        with palco:
            palco_container = open_palco()

            with palco_container:
                if chosen_id == "1":
                    page_mini()
                    status = f"🍃  {st.session_state.lang} - {st.session_state.tema} ( {st.session_state.mini + 1} / {len(load_temas('todos os temas'))} )"

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
                    status = palco_status("ABOUT")
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
