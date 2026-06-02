import os
import re
import time
import random
import base64
import socket
import asyncio
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components
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
    initial_sidebar_state="expanded",
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
            width: 315px !important;
            min-width: 315px !important;
            max-width: 315px !important;
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
            font-family: 'Trebuchet MS';
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

        
        /* Sidebar :: Centro de Controle fixo */
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }

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
            gap: 0.56rem !important;
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

        .cia-stage-box {
            background: rgba(255, 255, 255, 0.58);
            border-radius: 16px;
            padding: 0.25rem 0.55rem 0.35rem 0.55rem;
            min-height: 1.4;
            box-sizing: border-box;
            overflow-x: hidden;
        }

        .cia-stage-body {
            line-height: 1.35;
        }

        .cia-stage-title {
            text-align: center;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
            opacity: 0.88;
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
        "cia_line0_offset_px": -385,
        "cia_font": "Trebuchet MS",
        "cia_size": 18,
        "tema_last_analise": "",

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

CIA_WORD_1 = ["Informação", "Invenção", "Imaginação", "Imagética", "Injeção"]
CIA_WORD_2 = ["Analítica", "Artificial", "Analógica", "Afetiva", "Adicional", "Ampliada", "Avançada", "Acadêmica"]
CIA_MOODS = [
    "Sintática",
    "Sintética",
    "Formal",
    "Reduzida",
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


def generate_poema_preview(nome_tema, seed_eureka=""):
    """Gera um poema inline sem sobrescrever o LYPO em disco."""
    try:
        script = gera_poema(nome_tema, seed_eureka)
    except Exception:
        return nome_tema

    text_lines = [nome_tema]
    for line in script:
        if line == "\n":
            text_lines.append("")
        else:
            text_lines.append(line)
    return "<br>".join(text_lines)


def build_cia_header():
    """Descrição poética da CIA, gerada pela própria Machina sem repetir o título."""
    ensure_cia_name()
    header = generate_poema_preview("Cia", "")
    if st.session_state.lang != "pt":
        header = translate(header)
        typo_user = "TYPO_" + IPAddres
        with open(os.path.join("./temp/" + typo_user), "w", encoding="utf-8") as save_typo:
            save_typo.write(header)
        header = load_typo()

    parts = [part.strip() for part in header.replace("<br/>", "<br>").split("<br>")]
    body_parts = [part for part in parts[1:] if part] if len(parts) > 1 else [part for part in parts if part]
    return "<br>".join(body_parts)


def _cia_first_token(line):
    token = line.strip().split(" ")[0] if line.strip() else ""
    return token.strip("“”\"'()[]{}.,;:!?…-").lower()


def _cia_first_two_tokens(line):
    parts = [p.strip("“”\"'()[]{}.,;:!?…-").lower() for p in line.strip().split()[:2]]
    return " ".join([p for p in parts if p])


def _cia_poema_lines(curr_ypoema):
    """Extrai linhas reais do yPoema, preservando apenas o corpo do texto."""
    raw_parts = [part.strip() for part in curr_ypoema.replace("<br/>", "<br>").split("<br>")]
    lines = [part for part in raw_parts if part]
    return lines[1:] if len(lines) > 1 else []


def _cia_clip(line, limit=62):
    """Mantém o trecho legível no palco, sem deixar a citação dominar o parágrafo."""
    clean = re.sub(r"\s+", " ", str(line or "")).strip()
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + "..."


def _cia_join(blocks):
    """Une blocos sem trailing spaces visuais; o HTML da CIA cuida dos parágrafos."""
    return "\n\n".join([str(block).strip() for block in blocks if str(block).strip()])


def _cia_pick_unused(candidates, used_lines, fallback=""):
    """Escolhe um verso ainda não mobilizado e o registra como usado."""
    for line in candidates:
        if line and line not in used_lines:
            used_lines.add(line)
            return line
    if fallback:
        used_lines.add(fallback)
        return fallback
    for line in candidates:
        if line:
            used_lines.add(line)
            return line
    return ""


def _cia_destaques(poema_lines):
    """Trechos com maior probabilidade de rendimento crítico, sem transformar isso em fórmula."""
    marked = [line for line in poema_lines if "..." in line or "…" in line or "?" in line or line.count(",") >= 1]
    inner_caps = []
    for line in poema_lines:
        words = line.split()
        if len(words) > 1 and any(w.strip("“”\"'()[]{}.,;:!?…-")[:1].isupper() for w in words[1:]):
            inner_caps.append(line)
    curtas_fortes = [line for line in poema_lines if 2 <= len(line.split()) <= 6]
    return marked + inner_caps + curtas_fortes + poema_lines


def _cia_critico_abertura(poema_lines, used_lines):
    """Primeiro bloco fixo: cria eixo de leitura sem virar fórmula."""
    abertura = _cia_pick_unused([poema_lines[0]], used_lines, poema_lines[0])
    return random.choice([
        f"Desde **“{_cia_clip(abertura)}”**, o poema estabelece um campo de tensão que orienta a leitura sem entregar tudo de saída.",
        f"A entrada em **“{_cia_clip(abertura)}”** já define um modo de aproximação: o poema começa como gesto, não apenas como enunciado.",
        f"Logo em **“{_cia_clip(abertura)}”**, o texto escolhe seu passo e prepara a pressão que irá circular pelos versos.",
        f"**“{_cia_clip(abertura)}”** funciona como porta de entrada do poema: abre o percurso e já deixa uma tensão em suspensão.",
    ])


def _cia_critico_fecho(poema_lines, used_lines, prefer_specific=True):
    """Último bloco fixo: recolhe a leitura sem fechar o poema."""
    fecho = poema_lines[-1]
    if prefer_specific and fecho not in used_lines:
        used_lines.add(fecho)
        return random.choice([
            f"No fecho, **“{_cia_clip(fecho)}”** recolhe o percurso sem esgotá-lo; a última linha concentra a pressão e deixa o poema ainda reverberando.",
            f"A chegada a **“{_cia_clip(fecho)}”** dá ao poema seu ponto de recolhimento: não fecha o sentido, mas organiza o eco do que veio antes.",
            f"Em **“{_cia_clip(fecho)}”**, o poema encontra uma saída que ainda preserva atrito. O fim recolhe a leitura sem transformar a tensão em resposta única.",
            f"O verso final — **“{_cia_clip(fecho)}”** — funciona como mar da leitura: para ali converge o percurso, mas o texto continua vibrando depois da chegada.",
        ])
    return random.choice([
        "O fechamento recolhe as linhas de força sem reduzir o poema a uma resposta. A leitura termina com eco, não com explicação.",
        "O percurso crítico se encerra onde o poema preserva sua zona de ressonância: o sentido se organiza, mas não se deixa domesticar.",
        "Ao fim, permanece uma tensão produtiva. O poema não pede solução; pede que a leitura conserve o que nele ficou em movimento.",
    ])


def _cia_filter_candidates(candidates, used_lines, target_count, min_count=1):
    """Seleciona blocos intermediários evitando repetir trechos já mobilizados."""
    shuffled = candidates[:]
    random.shuffle(shuffled)
    chosen = []
    for item in shuffled:
        item_lines = set(item.get("lines", []))
        if item_lines and item_lines & used_lines:
            continue
        chosen.append(item)
        used_lines.update(item_lines)
        if len(chosen) >= target_count:
            break
    if len(chosen) < min_count:
        for item in shuffled:
            if item in chosen:
                continue
            item_lines = set(item.get("lines", []))
            # repetição só como último recurso, quando há pouco material no poema
            chosen.append(item)
            used_lines.update(item_lines)
            if len(chosen) >= min_count:
                break
    return chosen


def build_cia_analysis(curr_ypoema):
    """Leitura sintática com fluxo fixo: abertura, desenvolvimento e fecho."""
    poema_lines = _cia_poema_lines(curr_ypoema)
    tema = st.session_state.get("tema", "")

    if not poema_lines:
        st.session_state["_cia_used_lines"] = []
        return "**requer apuração manual**"

    candidates = []

    def add(lines_used, text):
        cleaned = [line for line in lines_used if line]
        candidates.append({"lines": cleaned, "text": text})

    perguntas = [line for line in poema_lines if "?" in line]
    if perguntas:
        line = perguntas[0]
        add([line],
            f"Em **“{_cia_clip(line)}”** a interrogação não funciona como simples pergunta: ela instala uma zona de instabilidade e obriga o poema a respirar pelo intervalo da dúvida."
        )

    reticencias = [line for line in poema_lines if "..." in line or "…" in line]
    if reticencias:
        line = reticencias[0]
        add([line],
            f"As reticências de **“{_cia_clip(line)}”** suspendem o fechamento e deixam a frase continuar fora da linha, como se o sentido ainda estivesse procurando onde pousar."
        )

    incisos = [line for line in poema_lines if "(" in line or ")" in line]
    if incisos:
        line = incisos[0]
        add([line],
            f"O inciso em **“{_cia_clip(line)}”** cria uma dobra interna: o verso se desvia por um instante e volta ao poema com outra respiração."
        )

    first_tokens = {}
    first_two = {}
    for line in poema_lines:
        t1 = _cia_first_token(line)
        t2 = _cia_first_two_tokens(line)
        if t1:
            first_tokens.setdefault(t1, []).append(line)
        if t2:
            first_two.setdefault(t2, []).append(line)

    parallel_key = next((k for k, v in first_two.items() if len(v) >= 2 and len(k.split()) == 2), None)
    anafora_key = next((k for k, v in first_tokens.items() if len(v) >= 2), None)

    if parallel_key:
        exemplos = first_two[parallel_key][:2]
        add(exemplos,
            f"O paralelismo entre **“{_cia_clip(exemplos[0])}”** e **“{_cia_clip(exemplos[1])}”** dá cadência ao poema: a estrutura retorna, mas não repete simplesmente a mesma intensidade."
        )
    elif anafora_key:
        exemplos = first_tokens[anafora_key][:2]
        add(exemplos,
            f"A repetição inicial em **“{_cia_clip(exemplos[0])}”** e **“{_cia_clip(exemplos[1])}”** cria anáfora. O retorno do mesmo arranque firma um eixo verbal para o percurso."
        )

    enumeracoes = [line for line in poema_lines if line.count(",") >= 2]
    if enumeracoes:
        line = enumeracoes[0]
        add([line],
            f"A enumeração em **“{_cia_clip(line)}”** trabalha por acúmulo. O verso não se limita a listar: ele engrossa o campo de forças do poema."
        )

    subordinadas = [line for line in poema_lines if re.search(r"\b(se|quando|embora|porque|que)\b", line.lower())]
    coordenadas = [line for line in poema_lines if re.search(r"\b(e|ou|mas)\b", line.lower()) and "," in line]

    if subordinadas:
        line = subordinadas[0]
        add([line],
            f"Em **“{_cia_clip(line)}”**, a subordinação cria dependência interna: a frase avança por condição, tempo ou explicação, e não por simples sequência."
        )
    elif coordenadas:
        line = coordenadas[0]
        add([line],
            f"A coordenação em **“{_cia_clip(line)}”** aproxima segmentos sem fundi-los por completo. O verso ganha soma, contraste ou desvio lateral."
        )

    cortes = []
    for i, line in enumerate(poema_lines[:-1]):
        nxt = poema_lines[i + 1]
        if line and line[-1] not in ".?!:;…)" and (nxt[:1].islower() or len(line.split()) <= 4):
            cortes.append((line, nxt))
    if cortes:
        l1, l2 = cortes[0]
        add([l1, l2],
            f"No corte entre **“{_cia_clip(l1)}”** e **“{_cia_clip(l2)}”**, a sintaxe atravessa a linha. A leitura é empurrada para diante antes de encontrar repouso."
        )

    used_lines = set()
    abertura = _cia_critico_abertura(poema_lines, used_lines)

    if candidates:
        max_figures = min(4, len(candidates))
        min_figures = min(2, len(candidates))
        target_count = max_figures if max_figures <= 2 else random.randint(min_figures, max_figures)
        chosen = _cia_filter_candidates(candidates, used_lines, target_count, min_figures)
        desenvolvimento = [item["text"] for item in chosen]
    else:
        desenvolvimento = [random.choice([
            "A construção verbal do poema trabalha menos por explicação do que por pressão acumulada: cada linha desloca um pouco o eixo da leitura.",
            "Mesmo sem uma figura dominante imediatamente nomeável, o poema sustenta seu efeito pela distribuição de cortes, pausas e retomadas.",
            "A sintaxe opera como corrente subterrânea: o sentido avança por pequenas tensões, não por declaração direta.",
        ])]

    fecho = _cia_critico_fecho(poema_lines, used_lines, prefer_specific=True)

    st.session_state.tema_last_analise = tema
    st.session_state["_cia_used_lines"] = list(used_lines)
    return _cia_join([abertura] + desenvolvimento + [fecho])


def build_cia_analysis_free(curr_ypoema):
    """Outro ângulo: leitura de contraste, sem mencionar método e sem repetir trechos por comodidade."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "Sem texto em foco para leitura."

    used = set(st.session_state.get("_cia_used_lines", []))
    local_used = set(used)

    abertura_line = _cia_pick_unused([poema_lines[0]], local_used, poema_lines[0])
    destaque_line = _cia_pick_unused(_cia_destaques(poema_lines), local_used, poema_lines[len(poema_lines) // 2])
    fecho_line = _cia_pick_unused([poema_lines[-1]], local_used, poema_lines[-1])

    abertura = random.choice([
        f"Outro ângulo surge já em **“{_cia_clip(abertura_line)}”**: o verso não apenas inicia o texto, mas define uma temperatura de leitura.",
        f"Por outro caminho, **“{_cia_clip(abertura_line)}”** abre uma zona de expectativa. O poema começa antes de se explicar.",
        f"Há uma entrada discreta, mas decisiva, em **“{_cia_clip(abertura_line)}”**: dali o texto já escolhe o seu modo de respirar.",
    ])

    desenvolvimento = random.choice([
        f"No corpo do poema, **“{_cia_clip(destaque_line)}”** concentra uma energia própria. A formulação desloca a linguagem do uso comum e cria densidade.",
        f"O ponto de maior pressão aparece em **“{_cia_clip(destaque_line)}”**. O verso não apenas comunica: cria uma zona de sentido ao redor de si.",
        f"Em **“{_cia_clip(destaque_line)}”**, a linguagem ganha espessura. Há ali uma pequena torção que impede a leitura de seguir por caminho óbvio.",
    ])

    if fecho_line in {abertura_line, destaque_line} and len(poema_lines) > 2:
        fecho = random.choice([
            "O encerramento recolhe essa tensão sem resolver tudo. O poema termina preservando uma zona de eco.",
            "Ao final, a leitura não encontra uma explicação única, mas um resto de intensidade que continua trabalhando.",
            "O fim não domestica o percurso: apenas concentra sua última reverberação.",
        ])
    else:
        fecho = random.choice([
            f"No encerramento, **“{_cia_clip(fecho_line)}”** recolhe a tensão anterior e devolve o poema com outro peso.",
            f"A chegada a **“{_cia_clip(fecho_line)}”** desloca retrospectivamente o que veio antes e deixa o texto em estado de eco.",
            f"Quando chega a **“{_cia_clip(fecho_line)}”**, o poema muda de temperatura e conserva uma pressão residual depois do fim.",
        ])

    return _cia_join([abertura, desenvolvimento, fecho])


def build_cia_analysis_sintetica(curr_ypoema):
    """Sintética: núcleo de tensão com atmosfera, sem virar resumo banal."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "**requer apuração manual**"

    used_lines = set()
    abertura_line = _cia_pick_unused([poema_lines[0]], used_lines, poema_lines[0])
    destaque_line = _cia_pick_unused(_cia_destaques(poema_lines), used_lines, poema_lines[len(poema_lines) // 2])

    abertura = random.choice([
        f"Desde **“{_cia_clip(abertura_line)}”**, o poema se apresenta como concentração: pouco se espalha, muito se adensa.",
        f"A entrada em **“{_cia_clip(abertura_line)}”** já arma o núcleo do texto, com uma pressão que prefere sugerir a explicar.",
        f"Em **“{_cia_clip(abertura_line)}”**, o poema encontra seu primeiro eixo e começa a trabalhar por condensação.",
    ])

    desenvolvimento = random.choice([
        f"O centro de força passa por **“{_cia_clip(destaque_line)}”**. A formulação concentra imagem, tensão e atmosfera sem dissolver o mistério.",
        f"Em **“{_cia_clip(destaque_line)}”**, a linguagem ganha densidade: o verso parece reunir o que o poema tem de mais vivo.",
        f"Há em **“{_cia_clip(destaque_line)}”** uma medula verbal. O poema se mostra breve na superfície e mais largo por dentro.",
    ])

    fecho = _cia_critico_fecho(poema_lines, used_lines, prefer_specific=True)
    return _cia_join([abertura, desenvolvimento, fecho])


def build_cia_analysis_formal(curr_ypoema):
    """Formal: arquitetura visível do poema, sem repetir o padrão da Sintética ou da Reduzida."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "**requer apuração manual**"

    raw_lines = curr_ypoema.replace("<br/>", "<br>").split("<br>")
    raw_poem = raw_lines[1:] if len(raw_lines) > 1 else []
    qtd_linhas = len(poema_lines)
    blocos = max(
        1,
        sum(
            1
            for i, line in enumerate(raw_poem)
            if line.strip() and (i == 0 or not raw_poem[i - 1].strip())
        ),
    )

    curtas = sum(1 for line in poema_lines if len(line.split()) <= 4)
    longas = sum(1 for line in poema_lines if len(line.split()) >= 7)
    medias = max(0, qtd_linhas - curtas - longas)
    reticencias = [line for line in poema_lines if "..." in line or "…" in line]
    perguntas = [line for line in poema_lines if "?" in line]

    repeticoes_iniciais = {}
    for line in poema_lines:
        first = line.split()[0].strip("“”\"'()[]{}.,;:!?…-").lower() if line.split() else ""
        if first:
            repeticoes_iniciais[first] = repeticoes_iniciais.get(first, 0) + 1
    repetido = next((k for k, v in repeticoes_iniciais.items() if v >= 2), None)

    abertura = random.choice([
        f"A primeira presença do poema é o seu desenho: **{qtd_linhas} linhas** em **{blocos} bloco{'s' if blocos != 1 else ''}** dão ao texto uma forma de chegada antes mesmo da interpretação.",
        f"O poema se apresenta como arquitetura visível: **{qtd_linhas} linhas** e **{blocos} bloco{'s' if blocos != 1 else ''}** regulam o modo como a leitura entra no texto.",
        f"Antes do sentido se explicar, há uma forma em cena: **{qtd_linhas} linhas** distribuídas em **{blocos} bloco{'s' if blocos != 1 else ''}** organizam o fôlego inicial da leitura.",
    ])

    desenvolvimento = []

    desenvolvimento.append(random.choice([
        f"A alternância de extensão também trabalha: **{curtas} linhas breves**, **{medias} médias** e **{longas} mais longas** criam variação de fôlego, evitando que o poema avance em linha reta demais.",
        f"O ritmo nasce da medida dos versos: linhas breves, médias e longas se revezam e fazem a leitura acelerar, conter-se ou respirar conforme o desenho pede.",
        f"A diferença entre versos curtos e extensos não é ornamento gráfico; ela distribui pausas e pressões dentro do próprio corpo do poema.",
    ]))

    if repetido:
        desenvolvimento.append(random.choice([
            f"A recorrência inicial de **“{_cia_clip(repetido)}”** atua como marca de coesão. O poema ganha reconhecimento pelo retorno, não por simples repetição.",
            f"O retorno de **“{_cia_clip(repetido)}”** no começo de versos cria uma coluna interna: a forma passa a insistir antes mesmo do argumento.",
            f"Quando **“{_cia_clip(repetido)}”** reaparece em posição inicial, o poema firma uma pequena ossatura de repetição e reconhecimento.",
        ]))

    if reticencias or perguntas:
        mark = reticencias[0] if reticencias else perguntas[0]
        desenvolvimento.append(random.choice([
            f"A pontuação em **“{_cia_clip(mark)}”** interfere no desenho do tempo: o verso não apenas diz, ele regula a demora da leitura.",
            f"Em **“{_cia_clip(mark)}”**, a pontuação vira gesto formal. Ela cria pausa, suspensão ou pressão dentro da superfície do poema.",
            f"O sinal gráfico em **“{_cia_clip(mark)}”** participa da arquitetura: muda o modo como o verso se oferece ao olhar e à escuta.",
        ]))

    if len(desenvolvimento) > 2:
        random.shuffle(desenvolvimento)
        desenvolvimento = desenvolvimento[:2]

    fecho = random.choice([
        "O resultado é uma forma que não apenas abriga o poema, mas participa de sua força: linhas, pausas e retornos dão ao texto uma presença própria.",
        "A forma recolhe a leitura sem precisar explicar o poema: o desenho visível organiza o percurso e deixa uma última impressão de arquitetura viva.",
        "Ao final, o que permanece não é só o que foi dito, mas o modo como o texto ocupou o espaço e conduziu o olhar até o seu repouso.",
    ])

    return _cia_join([abertura] + desenvolvimento + [fecho])

def build_cia_analysis_rapida(curr_ypoema):
    """Leitura rápida: primeiro clarão do poema, breve e diferente da resumida."""
    raw_parts = [part.strip() for part in curr_ypoema.replace("<br/>", "<br>").split("<br>")]
    lines = [part for part in raw_parts if part]
    poema_lines = lines[1:] if len(lines) > 1 else []

    if not poema_lines:
        return "**requer apuração manual**"

    abertura = poema_lines[0]
    fecho = poema_lines[-1]
    meio = poema_lines[len(poema_lines) // 2]
    destaque = next((line for line in poema_lines if "..." in line or "…" in line or "?" in line or "," in line), meio)

    p1 = random.choice([
        f"Primeiro clarão: **“{abertura}”** já entrega o pulso do poema e chama o leitor para dentro sem pedir explicação prévia.",
        f"A entrada em **“{abertura}”** funciona como impacto inicial: curta ou longa, ela já decide a temperatura da leitura.",
        f"Lido de passagem, o poema começa a se abrir em **“{abertura}”**. É ali que o leitor recebe o primeiro sinal de direção.",
    ])

    p2 = random.choice([
        f"O ponto que mais acende a leitura é **“{destaque}”**: o verso concentra uma pequena pressão de imagem, corte ou pensamento.",
        f"Em **“{destaque}”**, o texto mostra seu gesto mais imediato. Não é resumo: é lampejo de entrada.",
        f"A leitura rápida se fixa em **“{destaque}”** porque ali o poema parece piscar com mais força para o leitor.",
    ])

    p3 = random.choice([
        f"O fecho em **“{fecho}”** deixa o último eco. A leitura rápida não fecha o poema: apenas aponta onde ele continua vibrando.",
        f"Quando chega a **“{fecho}”**, o poema deixa uma impressão final que vale mais como eco do que como conclusão.",
        f"A última linha — **“{fecho}”** — funciona como sinal de saída, mas ainda carrega o rastro do percurso.",
    ])

    body = [p1, p2, p3]
    random.shuffle(body)
    return "  \n\n".join(body)


def build_cia_analysis_resumida(curr_ypoema):
    """Reduzida: leitura curta, objetiva e distinta da Sintética."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "**requer apuração manual**"

    used_lines = set()
    abertura_line = _cia_pick_unused([poema_lines[0]], used_lines, poema_lines[0])
    destaque_line = _cia_pick_unused(_cia_destaques(poema_lines), used_lines, poema_lines[len(poema_lines) // 2])

    abertura = random.choice([
        f"O percurso se abre em **“{_cia_clip(abertura_line)}”** e já define o eixo mínimo da leitura.",
        f"A entrada em **“{_cia_clip(abertura_line)}”** fixa o primeiro movimento do poema.",
        f"Logo em **“{_cia_clip(abertura_line)}”**, o texto indica sua direção principal.",
    ])

    desenvolvimento = random.choice([
        f"O ponto de maior concentração aparece em **“{_cia_clip(destaque_line)}”**: ali o poema reúne sua tensão mais visível.",
        f"Em **“{_cia_clip(destaque_line)}”**, a leitura encontra o núcleo mais direto do texto.",
        f"**“{_cia_clip(destaque_line)}”** resume a pressão central sem esgotar o poema.",
    ])

    fecho = _cia_critico_fecho(poema_lines, used_lines, prefer_specific=True)
    return _cia_join([abertura, desenvolvimento, fecho])

def build_cia_analysis_completa(curr_ypoema):
    """Completa: cartografia articulada com abertura, desenvolvimento e fecho fixos."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "**requer apuração manual**"

    used_lines = set()
    qtd_linhas = len(poema_lines)
    abertura_line = _cia_pick_unused([poema_lines[0]], used_lines, poema_lines[0])
    destaque_line = _cia_pick_unused(_cia_destaques(poema_lines), used_lines, poema_lines[len(poema_lines) // 2])

    abertura = random.choice([
        f"Desde **“{_cia_clip(abertura_line)}”**, o poema arma um campo de leitura que não se limita ao enunciado: a entrada instala direção, tom e tensão.",
        f"Logo em **“{_cia_clip(abertura_line)}”**, o texto fixa um eixo. O começo já orienta o modo como o poema quer ser acompanhado.",
        f"Em **“{_cia_clip(abertura_line)}”**, a abertura pesa como gesto inaugural; o que vem depois parece nascer sob essa primeira pressão verbal.",
    ])

    nucleo = random.choice([
        f"No corpo do texto, **“{_cia_clip(destaque_line)}”** concentra parte decisiva da força verbal. A imagem ou tensão ali ganha espessura.",
        f"Há um centro de gravidade em **“{_cia_clip(destaque_line)}”**. O poema reúne ali uma de suas zonas de maior densidade.",
        f"Em **“{_cia_clip(destaque_line)}”**, o texto adensa seu movimento: a linguagem deixa de apenas conduzir e passa a pesar mais diretamente.",
    ])

    forma = random.choice([
        f"A distribuição em **{qtd_linhas} linhas** participa do efeito do poema: pausas e cortes regulam o ritmo de aparição do sentido.",
        f"O desenho visível do texto — suas **{qtd_linhas} linhas**, pausas e quebras — atua como arquitetura, não como suporte neutro.",
        f"Também a forma pesa: as **{qtd_linhas} linhas** organizam o fôlego e modulam a intensidade do percurso.",
    ])

    ampliacao = random.choice([
        "O poema vale não só pelo que nomeia, mas pelo modo como organiza pressão, intervalo, reaparição e eco.",
        "A força do texto está no modo como regula sua intensidade e a devolve ao leitor em camadas.",
        "O texto conduz, interrompe, reaperta e libera o próprio movimento sem reduzir-se a uma explicação única.",
    ])

    meio = [nucleo, forma, ampliacao]
    random.shuffle(meio)
    fecho = _cia_critico_fecho(poema_lines, used_lines, prefer_specific=True)
    return _cia_join([abertura] + meio + [fecho])

def render_cia_stage(curr_ypoema):
    """Renderiza a análise da CIA; na Sintática, mantém o anexo comparativo. Na Sintética, entrega só a leitura."""
    cia_offset = int(st.session_state.get("cia_line0_offset_px", 0))
    cia_font = st.session_state.get("cia_font", "Trebuchet MS")
    cia_size = int(st.session_state.get("cia_size", 18))
    mood = st.session_state.get("cia_mood", CIA_MOODS[0])

    def _to_html_block(markdown_text):
        html = markdown_text
        while "**" in html:
            html = html.replace("**", "<strong>", 1)
            html = html.replace("**", "</strong>", 1)
        html = html.replace("  \n", "\n")
        html = html.replace("\r\n", "\n")
        html = re.sub(r"\n{3,}", "\n\n", html)
        paragraphs = [p.strip() for p in html.split("\n\n") if p.strip()]
        return "".join(f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paragraphs)

    st.markdown(
        f"<div class='cia-stage-box' style='margin-top:{cia_offset}px;'>",
        unsafe_allow_html=True,
    )
    write_ypoema(build_cia_header(), None)
    st.markdown("&nbsp;", unsafe_allow_html=True)

    if mood == "Sintética":
        analysis_html = _to_html_block(build_cia_analysis_sintetica(curr_ypoema))
        content = analysis_html
    elif mood == "Sintática":
        analysis_html = _to_html_block(build_cia_analysis(curr_ypoema))
        analysis_free_html = _to_html_block(build_cia_analysis_free(curr_ypoema))
        content = f"""{analysis_html}
            <div class='cia-stage-sep'><strong>Outro ângulo</strong></div>
            {analysis_free_html}"""
    elif mood == "Formal":
        analysis_html = _to_html_block(build_cia_analysis_formal(curr_ypoema))
        content = analysis_html
    elif mood in ("Reduzida", "Resumida"):
        analysis_html = _to_html_block(build_cia_analysis_resumida(curr_ypoema))
        content = analysis_html
    elif mood == "Completa":
        analysis_html = _to_html_block(build_cia_analysis_completa(curr_ypoema))
        content = analysis_html
    else:
        analysis_html = _to_html_block("Este mood ainda não entrou em operação na CIA.")
        content = analysis_html

    st.markdown(
        f"""
        <style>
        .cia-stage-box .cia-stage-text p {{
            margin: 0 0 1.15em 0;
        }}
        .cia-stage-box .cia-stage-text p:last-child {{
            margin-bottom: 0;
        }}
        .cia-stage-box .cia-stage-sep {{
            margin: 1.25em 0 1em 0;
            padding-top: 0.8em;
            border-top: 1px solid rgba(0,0,0,0.12);
            opacity: 0.95;
        }}
        </style>
        <div class='cia-stage-text' style="font-family:{cia_font}; font-size:{cia_size}px; line-height:1.42;">
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_cia_sidebar():
    """Renderiza apenas os moods da CIA, sem cabeçalho redundante."""
    current_mood = st.session_state.get("cia_mood", CIA_MOODS[0])
    if current_mood not in CIA_MOODS:
        current_mood = CIA_MOODS[0]

    selected_mood = st.sidebar.radio(
        "mood",
        CIA_MOODS,
        index=CIA_MOODS.index(current_mood),
        key="cia_mood_radio",
        label_visibility="collapsed",
    )
    st.session_state.cia_mood = selected_mood


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


def pick_book_palco():
    """Escolhe o livro yPoemas diretamente no palco."""
    _sync_book_theme_state()

    books_list = BOOKS_LIST
    current = st.session_state.book
    key = "palco_book_select"
    _prepare_book_widget(key)

    st.selectbox(
        f"{len(books_list)} " + translate("livros disponíveis..."),
        books_list,
        index=books_list.index(current),
        key=key,
        on_change=_on_palco_book_change,
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


def show_icons():
    """Redes sociais removidas da sidebar para reduzir scroll."""
    return


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

    col_livros, col_nav, col_temas = st.columns([3, 4, 3])

    with col_livros:
        pick_book_palco()

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

            if st.session_state.get("sidebar_panel") != "CIA" and st.session_state.draw:
                LOGO_IMAGE = load_arts(st.session_state.tema)

            if st.session_state.get("sidebar_panel") == "CIA":
                col_poema, col_cia = st.columns([5, 5])
                with col_poema:
                    write_ypoema(LOGO_TEXTO, None)
                with col_cia:
                    render_cia_stage(curr_ypoema)
            else:
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
    """Renderiza os controles fixos do leitor."""
    pick_lang()
    pick_stage_font()
    draw_check_buttons()



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


        if chosen_id == "2":
            draw_sidebar_panel_buttons(chosen_id)
            if st.session_state.get("sidebar_panel", "Machina") == "CIA":
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

if __name__ == "__main__":
    main()
