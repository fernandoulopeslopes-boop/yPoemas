# moby.py
# MACHINA — Mobile ultra-light
# Etapa 022: rodapé fixo + swap Machina/Off-Mach + links no topo + OLA no foco.
# Não altera basico.py, DNA, .ypo, .pip ou conteúdo autoral.

from pathlib import Path
import base64
import html
import random
import re

import streamlit as st

from lay_2_ypo import gera_poema

try:
    from ponte_ola_openai import gerar_analise_ola as _gerar_analise_ola_real
except Exception:
    _gerar_analise_ola_real = None


st.set_page_config(
    page_title="Moby — a Machina Mobile",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =============================================================================
# DNA — autoridade das listas do Moby
# =============================================================================
DNA_PATH = Path("./base/DNA.TXT")
LINKS_PATH = Path("./base/links.txt")
IMAGES_ROOT = Path("./images")
IMAGES_MAP_PATH = Path("./base/images.txt")
OFF_DIR = Path("./off_machina")

IDIOMAS_MACHINA = [
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

FONTES_MACHINA = [
    ("Courier", "Courier New"),
    ("OpenDyslexic", "OpenDyslexic"),
    ("Trebuchet", "Trebuchet MS"),
    ("Cormorant", "Cormorant Garamond"),
    ("Palatino", "Palatino Linotype"),
    ("Georgia", "Georgia"),
    ("Jet_Brains", "JetBrains Mono"),
    ("IBM Plex Sans", "IBM Plex Sans"),
    ("Saira", "Saira"),
    ("Comic Relief", "Comic Relief"),
    ("Hand Writing", "Hand Writing"),
]

# Mesmo bootstrap tipográfico usado nos deploys anteriores da Machina.
GOOGLE_FONTS_CSS = (
    "https://fonts.googleapis.com/css2?"
    "family=Comic+Relief:wght@400;700&"
    "family=Cormorant+Garamond:wght@400;600;700&"
    "family=IBM+Plex+Sans:wght@400;600;700&"
    "family=JetBrains+Mono:wght@400;600;700&"
    "family=Saira:wght@400;600;700&"
    "display=swap"
)

FONTES_PALCO_CSS = {
    "Courier New": '"Courier New", Courier, monospace',
    "OpenDyslexic": '"OpenDyslexic", sans-serif',
    "Trebuchet MS": '"Trebuchet MS", Trebuchet, Arial, sans-serif',
    "Cormorant Garamond": '"Cormorant Garamond", Georgia, serif',
    "Palatino Linotype": '"Palatino Linotype", Palatino, "Book Antiqua", serif',
    "Georgia": 'Georgia, "Times New Roman", serif',
    "JetBrains Mono": '"JetBrains Mono", Consolas, "Courier New", monospace',
    "IBM Plex Sans": '"IBM Plex Sans", Arial, sans-serif',
    "Saira": 'Saira, Arial, sans-serif',
    "Comic Relief": '"Comic Relief", "Comic Sans MS", cursive',
    "Hand Writing": '"Segoe Print", "Bradley Hand", cursive',
}

def fonte_palco_css(family=None):
    family = str(family or st.session_state.get("moby_font_family", "Trebuchet MS")).strip()
    return FONTES_PALCO_CSS.get(family, f'"{family}", sans-serif')

def open_dyslexic_font_face():
    fonts_dir = Path("./fonts")
    if not fonts_dir.is_dir():
        return ""
    regular = None
    bold = None
    for path in sorted(fonts_dir.iterdir()):
        low = path.name.casefold()
        if not path.is_file() or "opendyslexic" not in low or path.suffix.casefold() not in {".ttf", ".otf"}:
            continue
        if "bold" in low:
            bold = bold or path
        else:
            regular = regular or path
    regras = []
    for path, peso in ((regular, 400), (bold, 700)):
        if path is None:
            continue
        try:
            payload = base64.b64encode(path.read_bytes()).decode("ascii")
        except OSError:
            continue
        ext = path.suffix.casefold()
        mime = "font/otf" if ext == ".otf" else "font/ttf"
        formato = "opentype" if ext == ".otf" else "truetype"
        regras.append(
            "@font-face{"
            "font-family:'OpenDyslexic';"
            f"src:url(data:{mime};base64,{payload}) format('{formato}');"
            f"font-weight:{peso};font-style:normal;font-display:swap;"
            "}"
        )
    return "".join(regras)

def bootstrap_fontes_machina():
    local_open = open_dyslexic_font_face()
    st.markdown(
        f"""
        <style>
        @import url('{GOOGLE_FONTS_CSS}');
        {local_open}
        </style>
        """,
        unsafe_allow_html=True,
    )

CORPOS_MOBY = list(range(16, 37, 2))


def load_dna(path=DNA_PATH):
    if not path.exists():
        raise FileNotFoundError(f"DNA não encontrado: {path}")

    linhas = path.read_text(encoding="utf-8-sig").splitlines()
    if not linhas:
        raise RuntimeError("DNA vazio.")

    header = None
    rows = []

    for raw in linhas:
        linha = raw.strip()

        if not linha:
            continue
        if linha == "<EOF>":
            break
        if not (linha.startswith("|") and linha.endswith("|")):
            continue

        campos = linha[1:-1].split("|")

        if header is None:
            header = campos
            continue

        if len(campos) != len(header):
            continue

        rows.append(dict(zip(header, campos)))

    if not header or "tema" not in header or "livro" not in header:
        raise RuntimeError("DNA sem os campos mínimos tema/livro.")

    return rows


def temas_do_livro(rows, livro):
    """Ordem = ordem física/natural dos registros no DNA."""
    alvo = str(livro or "").strip().casefold()
    temas = []

    for row in rows:
        if str(row.get("ativo", "")).strip().upper() != "S":
            continue

        livros = [
            item.strip().casefold()
            for item in str(row.get("livro", "")).split(";")
            if item.strip()
        ]

        if alvo not in livros:
            continue

        tema = str(row.get("tema", "")).strip()
        if tema:
            temas.append(tema)

    return temas


def nome_normalizado(valor):
    return "".join(str(valor or "").split()).casefold()


def links_do_tema(tema, path=LINKS_PATH):
    """LINK canônico: DE->PARA; sem DE próprio, usa PARA->DE como fallback."""
    if not path.exists():
        return []

    alvo = nome_normalizado(tema)
    diretos = []
    diretos_cf = set()
    inversos = []
    inversos_cf = set()

    try:
        with path.open(encoding="utf-8-sig") as arquivo:
            for raw in arquivo:
                linha = raw.strip()
                if not linha or linha.startswith("#"):
                    continue
                if not (linha.startswith("|") and linha.endswith("|")):
                    continue

                campos = [campo.strip() for campo in linha[1:-1].split("|")]
                if len(campos) < 2 or not campos[0]:
                    continue

                origem = campos[0].strip()
                origem_cf = nome_normalizado(origem)
                destinos = [campo.strip() for campo in campos[1:] if campo.strip()]

                # DE -> PARA
                if origem_cf == alvo:
                    for destino in destinos:
                        destino_cf = nome_normalizado(destino)
                        if destino_cf and destino_cf != alvo and destino_cf not in diretos_cf:
                            diretos.append(destino)
                            diretos_cf.add(destino_cf)
                    continue

                # PARA -> DE
                if any(nome_normalizado(destino) == alvo for destino in destinos):
                    if origem_cf and origem_cf != alvo and origem_cf not in inversos_cf:
                        inversos.append(origem)
                        inversos_cf.add(origem_cf)

    except OSError:
        return []

    # Regra canônica: o sentido inverso só é usado se não houver DE próprio.
    return diretos if diretos else inversos


def registro_do_tema(rows, tema):
    alvo = nome_normalizado(tema)
    for row in rows:
        if nome_normalizado(row.get("tema", "")) == alvo:
            return row
    return {}


def primeiro_livro_do_tema(rows, tema):
    row = registro_do_tema(rows, tema)
    for livro in str(row.get("livro", "")).split(";"):
        livro = livro.strip()
        if livro:
            return livro
    return ""


def banco_de_imagens_do_tema(tema, path=IMAGES_MAP_PATH):
    """Resolve a curadoria canônica tema -> grupo a partir de base/images.txt."""
    alvo = str(tema or "").strip()
    if path.exists():
        try:
            with path.open(encoding="utf-8-sig") as arquivo:
                for raw in arquivo:
                    linha = raw.strip()
                    if not linha or linha.startswith("#") or " : " not in linha:
                        continue
                    nome, grupo = linha.split(" : ", 1)
                    if nome.strip() == alvo and grupo.strip():
                        return grupo.strip().strip("/\\")
        except OSError:
            pass
    return "machina"


def imagens_do_tema(rows, tema):
    """Escolhe duas imagens distintas do mesmo banco temático curado."""
    if str(st.session_state.get("moby_mode", "Machina")) == "Off-Machina":
        livro_off = current_off_book_path()
        nome_mapeado = livro_off.stem if livro_off else ""
        banco = banco_de_imagens_do_tema(nome_mapeado)
    else:
        banco = banco_de_imagens_do_tema(tema)

    pasta = IMAGES_ROOT / banco
    if not pasta.is_dir():
        return None, None

    imagens = [
        item for item in pasta.iterdir()
        if item.is_file() and item.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    ]
    if not imagens:
        return None, None

    usadas = set(st.session_state.get("moby_arts", []))
    disponiveis = [img for img in imagens if str(img) not in usadas]
    pool = disponiveis if len(disponiveis) >= 2 else imagens

    if len(pool) >= 2:
        primeira, segunda = random.sample(pool, 2)
    else:
        primeira = pool[0]
        segunda = None

    historico = list(st.session_state.get("moby_arts", []))
    historico.extend(str(img) for img in (primeira, segunda) if img is not None)
    st.session_state.moby_arts = historico[-36:]
    return primeira, segunda


try:
    DNA_ROWS = load_dna()
except Exception as exc:
    st.error(f"Moby não conseguiu ler o DNA: {exc}")
    st.stop()


def livros_do_dna(rows):
    """Livros reais, na ordem natural da primeira aparição no DNA."""
    livros = []
    vistos = set()

    for row in rows:
        if str(row.get("ativo", "")).strip().upper() != "S":
            continue

        for item in str(row.get("livro", "")).split(";"):
            livro = item.strip()
            chave = livro.casefold()
            if livro and chave not in vistos:
                vistos.add(chave)
                livros.append(livro)

    return livros


MOBY_BOOKS = livros_do_dna(DNA_ROWS)

if not MOBY_BOOKS:
    st.error("O DNA não contém livros ativos.")
    st.stop()


# Para a auditoria visual, abre o livro REAL mais povoado.
MOBY_DEFAULT_BOOK = max(
    MOBY_BOOKS,
    key=lambda livro: len(temas_do_livro(DNA_ROWS, livro)),
)


# =============================================================================
# ESTADO LÓGICO
# =============================================================================
if "moby_sidebar_open" not in st.session_state:
    st.session_state.moby_sidebar_open = False

if "moby_help_open" not in st.session_state:
    st.session_state.moby_help_open = False

if "moby_reading_n" not in st.session_state:
    st.session_state.moby_reading_n = 1

if "moby_book" not in st.session_state:
    st.session_state.moby_book = MOBY_DEFAULT_BOOK

if "moby_theme_index" not in st.session_state:
    st.session_state.moby_theme_index = 0

if "moby_link_pending" not in st.session_state:
    st.session_state.moby_link_pending = ""

if "moby_image_theme" not in st.session_state:
    st.session_state.moby_image_theme = ""

if "moby_image_path" not in st.session_state:
    st.session_state.moby_image_path = ""

if "moby_image_path_2" not in st.session_state:
    st.session_state.moby_image_path_2 = ""

if "moby_image_visible" not in st.session_state:
    st.session_state.moby_image_visible = True


if "moby_arts" not in st.session_state:
    st.session_state.moby_arts = []

if "moby_poem_signature" not in st.session_state:
    st.session_state.moby_poem_signature = None

if "moby_poem_html" not in st.session_state:
    st.session_state.moby_poem_html = ""


if "moby_lang" not in st.session_state:
    st.session_state.moby_lang = "pt"

if "moby_font_family" not in st.session_state:
    st.session_state.moby_font_family = "Trebuchet MS"

if "moby_font_size" not in st.session_state:
    st.session_state.moby_font_size = 16

if "moby_mode" not in st.session_state:
    st.session_state.moby_mode = "Machina"

if "moby_off_book_index" not in st.session_state:
    st.session_state.moby_off_book_index = 0

if "moby_off_take" not in st.session_state:
    st.session_state.moby_off_take = 0

if "moby_ola_requested" not in st.session_state:
    st.session_state.moby_ola_requested = False

if "moby_ola_signature" not in st.session_state:
    st.session_state.moby_ola_signature = None

if "moby_ola_text" not in st.session_state:
    st.session_state.moby_ola_text = ""

if "moby_analysis_kind" not in st.session_state:
    st.session_state.moby_analysis_kind = "Sintática"

if "moby_portrait_image" not in st.session_state:
    st.session_state.moby_portrait_image = ""

if "moby_seal_path" not in st.session_state:
    st.session_state.moby_seal_path = ""

if "moby_seal_signature" not in st.session_state:
    st.session_state.moby_seal_signature = None


def current_themes():
    return temas_do_livro(DNA_ROWS, st.session_state.moby_book)


def normalize_theme_index():
    temas = current_themes()
    if not temas:
        st.session_state.moby_theme_index = 0
        return
    st.session_state.moby_theme_index %= len(temas)


def current_theme():
    temas = current_themes()
    if not temas:
        return ""
    normalize_theme_index()
    return temas[st.session_state.moby_theme_index]


def off_books():
    """Livros .Pip reais disponíveis no Off-Machina."""
    if not OFF_DIR.is_dir():
        return []
    livros = []
    for path in sorted(OFF_DIR.iterdir(), key=lambda p: p.name.casefold()):
        if path.is_file() and path.suffix.casefold() == ".pip":
            livros.append(path)
    return livros


def off_pages(path):
    """Lê cada registro .Pip como uma página Off-Machina."""
    try:
        linhas = path.read_text(encoding="utf-8-sig").splitlines()
    except OSError:
        return []
    paginas = []
    for raw in linhas:
        line = raw.rstrip("\r\n")
        if not line.strip():
            continue
        if line.strip() == "<EOF>":
            break
        if line.startswith("|"):
            line = line[1:]
        if line.endswith("|"):
            line = line[:-1]
        partes = line.split("|")
        if not partes:
            continue
        titulo = partes[0].strip() or path.stem
        corpo = "\n".join(partes[1:]) if len(partes) > 1 else titulo
        paginas.append((titulo, corpo))
    return paginas


def current_off_book_path():
    livros = off_books()
    if not livros:
        return None
    idx = int(st.session_state.get("moby_off_book_index", 0)) % len(livros)
    st.session_state.moby_off_book_index = idx
    return livros[idx]


def current_off_pages():
    path = current_off_book_path()
    return off_pages(path) if path else []


def current_off_page():
    paginas = current_off_pages()
    if not paginas:
        return ("Off-Machina", "")
    idx = int(st.session_state.get("moby_off_take", 0)) % len(paginas)
    st.session_state.moby_off_take = idx
    return paginas[idx]



def apply_pending_link():
    """Aplica navegação LINK antes da instanciação dos widgets."""
    destino = str(st.session_state.get("moby_link_pending", "")).strip()
    if not destino:
        return

    livro = primeiro_livro_do_tema(DNA_ROWS, destino)
    if not livro:
        st.session_state.moby_link_pending = ""
        return

    temas = temas_do_livro(DNA_ROWS, livro)
    alvo = nome_normalizado(destino)

    for idx, tema in enumerate(temas):
        if nome_normalizado(tema) == alvo:
            st.session_state.moby_book = livro
            st.session_state.moby_theme_index = idx
            st.session_state.moby_reading_n = 1
            invalidate_real_poem()
            break

    st.session_state.moby_link_pending = ""
    invalidate_ola()


def update_real_image():
    """Mantém uma imagem por leitura/página respeitando o mapeamento real de imagens."""
    if str(st.session_state.get("moby_mode", "Machina")) == "Off-Machina":
        path = current_off_book_path()
        assinatura = ("Off-Machina", str(path or ""), int(st.session_state.get("moby_off_take", 0)))
        tema = current_off_page()[0]
    else:
        tema = current_theme()
        assinatura = ("Machina", tema, int(st.session_state.get("moby_reading_n", 1)))
    if st.session_state.get("moby_image_theme") == assinatura:
        return

    img1, img2 = imagens_do_tema(DNA_ROWS, tema)
    st.session_state.moby_image_theme = assinatura
    st.session_state.moby_image_path = str(img1) if img1 else ""
    st.session_state.moby_image_path_2 = str(img2) if img2 else ""


def invalidate_real_poem():
    """Marca o palco para gerar outra leitura somente quando a leitura muda."""
    st.session_state.moby_poem_signature = None


def invalidate_real_image():
    """Força nova escolha de imagem sem alterar o yPoema."""
    st.session_state.moby_image_theme = ""
    st.session_state.moby_image_path = ""
    st.session_state.moby_image_path_2 = ""


def random_seal_path():
    """Escolhe um ex-libris RANDOM de ./images/selos, sem alterar o arquivo."""
    pasta = Path("./images/selos")
    if not pasta.is_dir():
        return None
    arquivos = [
        p for p in sorted(pasta.iterdir())
        if p.is_file() and p.suffix.casefold() in {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    ]
    if not arquivos:
        return None
    anterior = str(st.session_state.get("moby_seal_path", ""))
    candidatos = [p for p in arquivos if str(p) != anterior]
    return random.choice(candidatos or arquivos)


def update_random_seal():
    """Mantém um selo por leitura/página, em paralelo à imagem atual."""
    assinatura = st.session_state.get("moby_image_theme")
    if st.session_state.get("moby_seal_signature") == assinatura:
        return
    selo = random_seal_path()
    st.session_state.moby_seal_signature = assinatura
    st.session_state.moby_seal_path = str(selo) if selo else ""


def invalidate_ola():
    st.session_state.moby_ola_requested = False
    st.session_state.moby_ola_signature = None
    st.session_state.moby_ola_text = ""


def ypoema_html_to_text(ypoema_html):
    texto = str(ypoema_html or "")
    texto = texto.replace("<br/>", "\n").replace("<br />", "\n").replace("<br>", "\n")
    texto = re.sub(r"<[^>]+>", "", texto)
    return html.unescape(texto).strip()


def limpar_analise(texto, max_chars=900):
    texto = html.unescape(re.sub(r"<[^>]+>", "", str(texto or ""))).strip()
    if len(texto) > int(max_chars):
        texto = texto[:int(max_chars)].rstrip() + "..."
    return texto


def request_ola():
    dismiss_help()
    st.session_state.moby_ola_requested = True


def update_ola_analysis(titulo, corpo_html):
    if not st.session_state.get("moby_ola_requested", False):
        return ""
    assinatura = (str(st.session_state.get("moby_mode", "Machina")), str(titulo), str(corpo_html))
    if st.session_state.get("moby_ola_signature") == assinatura:
        return st.session_state.get("moby_ola_text", "")
    if _gerar_analise_ola_real is None:
        analise = "OLA ainda não conectada. Arquivo ponte_ola_openai.py não encontrado ou não importável."
    else:
        try:
            analise = limpar_analise(
                _gerar_analise_ola_real(
                    st.session_state.get("moby_analysis_kind", "Sintática"),
                    str(titulo),
                    ypoema_html_to_text(corpo_html),
                )
            )
        except Exception as exc:
            analise = f"OLA não conseguiu analisar esta leitura: {exc}"
    st.session_state.moby_ola_signature = assinatura
    st.session_state.moby_ola_text = analise
    return analise


def swap_machina_off():
    dismiss_help()
    if st.session_state.get("moby_mode") == "Off-Machina":
        st.session_state.moby_mode = "Machina"
    else:
        st.session_state.moby_mode = "Off-Machina"
        st.session_state.moby_off_take = 0
    invalidate_real_image()
    invalidate_ola()


def prepare_portrait():
    """Congela uma das duas imagens da leitura para o Retrato, por par/ímpar."""
    dismiss_help()
    update_real_image()
    img1 = str(st.session_state.get("moby_image_path", ""))
    img2 = str(st.session_state.get("moby_image_path_2", ""))
    if st.session_state.get("moby_mode") == "Off-Machina":
        indice = int(st.session_state.get("moby_off_take", 0))
    else:
        indice = int(st.session_state.get("moby_reading_n", 1))
    st.session_state.moby_portrait_image = img2 if (indice % 2 and img2) else img1


def update_real_poem():
    """Gera e congela o yPoema real da leitura atual no palco do Moby."""
    tema = current_theme()
    assinatura = (tema, int(st.session_state.get("moby_reading_n", 1)))

    if st.session_state.get("moby_poem_signature") == assinatura:
        return

    try:
        script = gera_poema(tema, "")
    except Exception as exc:
        st.session_state.moby_poem_html = (
            '<div class="moby-poem-error">'
            f'Moby não conseguiu gerar esta leitura: {exc}'
            '</div>'
        )
        st.session_state.moby_poem_signature = assinatura
        return

    linhas = []
    for line in script:
        if line == "\n":
            linhas.append("")
        else:
            linhas.append(str(line).rstrip("\r\n"))

    st.session_state.moby_poem_html = "<br>".join(linhas)
    st.session_state.moby_poem_signature = assinatura


def link_picked():
    destino = str(st.session_state.get("moby_links_pick", "")).strip()
    if destino and destino != "links":
        st.session_state.moby_link_pending = destino



def sidebar_language_changed():
    dismiss_help()
    escolha = st.session_state.get("moby_lang_pick", "")
    for nome, pais, code in IDIOMAS_MACHINA:
        if escolha == f"{nome} — {pais}":
            st.session_state.moby_lang = code
            return


def sidebar_font_changed():
    dismiss_help()
    escolha = st.session_state.get("moby_font_pick", "")
    for label, family in FONTES_MACHINA:
        if escolha == label:
            st.session_state.moby_font_family = family
            return


def sidebar_size_changed():
    dismiss_help()
    st.session_state.moby_font_size = int(
        st.session_state.get("moby_size_pick", 16)
    )


def sidebar_mode_changed():
    dismiss_help()
    st.session_state.moby_mode = str(
        st.session_state.get("moby_mode_pick", "Machina")
    )
    if st.session_state.moby_mode == "Machina":
        st.session_state.moby_sidebar_open = False


def open_sidebar():
    dismiss_help()
    st.session_state.moby_sidebar_open = True


def close_sidebar_to_machina():
    """Volta ao palco Machina em um único clique."""
    dismiss_help()
    st.session_state.moby_mode = "Machina"
    invalidate_real_image()
    st.session_state.moby_sidebar_open = False


def select_off_machina_sidebar():
    """Abre o Off-Machina real preservando o mapeamento livro -> pasta de imagens."""
    dismiss_help()
    st.session_state.moby_mode = "Off-Machina"
    st.session_state.moby_off_take = 0
    invalidate_real_image()
    st.session_state.moby_sidebar_open = False


def select_ola_sidebar():
    dismiss_help()
    st.session_state.moby_mode = "OLA"


def toggle_help():
    st.session_state.moby_help_open = not st.session_state.moby_help_open


def dismiss_help():
    st.session_state.moby_help_open = False


def toggle_image():
    dismiss_help()
    st.session_state.moby_image_visible = not st.session_state.moby_image_visible


def new_reading():
    dismiss_help()
    invalidate_ola()
    if st.session_state.get("moby_mode") == "Off-Machina":
        return
    st.session_state.moby_reading_n += 1
    invalidate_real_poem()


def previous_theme():
    dismiss_help()
    invalidate_ola()
    if st.session_state.get("moby_mode") == "Off-Machina":
        paginas = current_off_pages()
        if paginas:
            st.session_state.moby_off_take = (st.session_state.moby_off_take - 1) % len(paginas)
            invalidate_real_image()
        return
    temas = current_themes()
    if temas:
        st.session_state.moby_theme_index = (st.session_state.moby_theme_index - 1) % len(temas)
        st.session_state.moby_reading_n = 1
        invalidate_real_poem()


def next_theme():
    dismiss_help()
    invalidate_ola()
    if st.session_state.get("moby_mode") == "Off-Machina":
        paginas = current_off_pages()
        if paginas:
            st.session_state.moby_off_take = (st.session_state.moby_off_take + 1) % len(paginas)
            invalidate_real_image()
        return
    temas = current_themes()
    if temas:
        st.session_state.moby_theme_index = (st.session_state.moby_theme_index + 1) % len(temas)
        st.session_state.moby_reading_n = 1
        invalidate_real_poem()


def random_theme():
    dismiss_help()
    invalidate_ola()
    if st.session_state.get("moby_mode") == "Off-Machina":
        paginas = current_off_pages()
        if paginas:
            atual = int(st.session_state.get("moby_off_take", 0))
            candidatos = [i for i in range(len(paginas)) if i != atual]
            st.session_state.moby_off_take = random.choice(candidatos) if candidatos else atual
            invalidate_real_image()
        return
    temas = current_themes()
    if not temas:
        return
    atual = st.session_state.moby_theme_index
    candidatos = [i for i in range(len(temas)) if i != atual]
    st.session_state.moby_theme_index = random.choice(candidatos) if candidatos else atual
    st.session_state.moby_reading_n = 1
    invalidate_real_poem()


def book_changed():
    st.session_state.moby_theme_index = 0
    st.session_state.moby_reading_n = 1
    invalidate_real_poem()


def theme_picked():
    temas = current_themes()
    escolha = st.session_state.get("moby_theme_pick", "")
    if escolha in temas:
        st.session_state.moby_theme_index = temas.index(escolha)
        st.session_state.moby_reading_n = 1
        invalidate_real_poem()


apply_pending_link()
normalize_theme_index()

# Na primeira abertura da bancada, prioriza um tema real com LINK
# para que a aparição possa ser auditada visualmente.
if not st.session_state.get("moby_started", False):
    temas_iniciais = current_themes()
    for idx, tema in enumerate(temas_iniciais):
        if links_do_tema(tema):
            st.session_state.moby_theme_index = idx
            break
    st.session_state.moby_started = True

update_real_image()
update_real_poem()
bootstrap_fontes_machina()


# =============================================================================
# CSS — "CELULAR" NA TELA DO NOTEBOOK
# =============================================================================
st.markdown(
    """
    <style>
    .stApp { background: #ececec; }

    .block-container {
        max-width: 430px !important;
        margin: 18px auto 60px auto !important;
        padding: 18px 18px 28px 18px !important;
        background: white;
        border: 1px solid rgba(0,0,0,.18);
        border-radius: 28px;
        box-shadow: 0 10px 35px rgba(0,0,0,.10);
        height: 820px;
        min-height: 820px;
        max-height: 820px;
        overflow: hidden;
    }

    div[data-testid="stVerticalBlock"] { gap: .48rem; }

    div[data-testid="stSelectbox"] label {
        font-size: .76rem !important;
        margin-bottom: .04rem !important;
    }

    .moby-brand {
        font-size: 1.05rem;
        font-weight: 600;
        margin-top: .10rem;
    }

    .theme-image-shell {
        display:flex;
        justify-content:center;
        margin: 7px 0 8px 0;
    }

    .theme-image {
        width: 146px;
        aspect-ratio: 2 / 3;
        border-radius: 8px;
        border: 1px solid rgba(0,0,0,.14);
        background:
            linear-gradient(155deg, rgba(0,0,0,.05), rgba(0,0,0,.01)),
            repeating-linear-gradient(
                45deg,
                rgba(0,0,0,.035) 0px,
                rgba(0,0,0,.035) 8px,
                transparent 8px,
                transparent 16px
            );
        display:flex;
        align-items:center;
        justify-content:center;
        text-align:center;
        padding:10px;
        font-size:.78rem;
        opacity:.78;
    }

    .poem-title {
        text-align:center;
        font-weight:700;
        text-decoration: underline;
        margin: 3px 0 4px 0;
    }

    .ypoema {
        line-height: 1.60;
        padding: 0 8px 0 3px;
        margin: 4px 0 8px 0;
        overflow-wrap: anywhere;
        max-height: 315px;
        overflow-y: auto;
        overflow-x: hidden;
        overscroll-behavior: contain;
        scrollbar-gutter: stable;
    }

    .moby-ola-inline {
        margin: 18px 2px 4px 2px;
        padding-top: 10px;
        border-top: 1px solid rgba(0,0,0,.14);
        line-height: 1.42;
    }

    .moby-ola-inline-title {
        text-align:center;
        font-weight:700;
        margin-bottom:6px;
    }

    .moby-poem-error {
        font-size: .82rem;
        opacity: .72;
        line-height: 1.45;
    }

    .moby-help {
        border: 1px solid rgba(0,0,0,.12);
        border-radius: 10px;
        padding: 9px 12px 7px 12px;
        font-size: .84rem;
        line-height: 1.42;
        background: rgba(248,248,248,.92);
        margin: 2px 0 4px;
    }

    .moby-help ul {
        margin: .15rem 0 .15rem 1.05rem;
        padding: 0;
    }

    .moby-help li {
        margin: .18rem 0;
    }

    .moby-sidebar-card {
        border: 1px solid rgba(0,0,0,.18);
        border-radius: 14px;
        padding: 13px 13px 10px 13px;
        background: #fafafa;
        box-shadow: 0 7px 20px rgba(0,0,0,.08);
        margin-bottom: 7px;
    }

    .moby-sidebar-title {
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: .35rem;
    }

    .moby-sidebar-note {
        font-size: .78rem;
        opacity: .70;
        line-height: 1.42;
    }


    .end-rule {
        border-top:1px solid rgba(0,0,0,.12);
        margin: 15px 0 8px 0;
    }

    div[data-testid="stButton"] button {
        min-height: 38px;
        border-radius: 9px;
        padding-left: .35rem !important;
        padding-right: .35rem !important;
        font-size: .88rem !important;
    }

    #MainMenu, footer, header { visibility: hidden; }

    section[data-testid="stSidebar"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# CABEÇALHO — SWAP + LINKS + SIDEBAR
# =============================================================================
modo_label = "¿" if st.session_state.get("moby_mode") == "Off-Machina" else "❓"
head_mode, head_links, head_side = st.columns([1.35, 4.3, 1.35], gap="small")

with head_mode:
    if st.session_state.get("moby_mode") == "Off-Machina":
        st.markdown("<style>.st-key-moby_mode_swap button {color:#d40000 !important; font-weight:800 !important;}</style>", unsafe_allow_html=True)
    st.button(modo_label, key="moby_mode_swap", width="stretch", on_click=swap_machina_off)

with head_links:
    if st.session_state.get("moby_mode") != "Off-Machina":
        links_top = links_do_tema(current_theme())
        if links_top:
            st.selectbox(
                "links",
                links_top,
                index=None,
                placeholder="links",
                key="moby_links_pick",
                on_change=link_picked,
                label_visibility="collapsed",
            )
        else:
            st.markdown("<div style='height:38px'></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='height:38px'></div>", unsafe_allow_html=True)

with head_side:
    st.button("☰", key="moby_open_sidebar", width="stretch", on_click=open_sidebar)


if st.session_state.moby_sidebar_open:
    s1, s2 = st.columns(2, gap="small")
    with s1:
        st.button("yPoemas", width="stretch", disabled=True)
    with s2:
        st.button("About", width="stretch", on_click=dismiss_help)

    idioma_labels = [f"{nome} — {pais}" for nome, pais, _ in IDIOMAS_MACHINA]
    idioma_atual = next(
        (f"{nome} — {pais}" for nome, pais, code in IDIOMAS_MACHINA if code == st.session_state.moby_lang),
        idioma_labels[0],
    )
    st.session_state["moby_lang_pick"] = idioma_atual
    st.selectbox("idiomas disponíveis...", idioma_labels, key="moby_lang_pick", on_change=sidebar_language_changed)

    fonte_labels = [label for label, _ in FONTES_MACHINA]
    fonte_lookup = {label: family for label, family in FONTES_MACHINA}
    fonte_atual = next(
        (label for label, family in FONTES_MACHINA if family == st.session_state.moby_font_family),
        "Trebuchet",
    )
    corpo_atual = int(st.session_state.get("moby_font_size", 16))
    if corpo_atual not in CORPOS_MOBY:
        corpo_atual = 16

    fonte_col, corpo_col = st.columns([2.15, 1], gap="small")
    with fonte_col:
        fonte_escolhida = st.selectbox(
            "fontes & letras", fonte_labels, index=fonte_labels.index(fonte_atual),
            key="moby_font_pick", on_change=sidebar_font_changed,
        )
    with corpo_col:
        corpo_escolhido = st.selectbox(
            "corpo", CORPOS_MOBY, index=CORPOS_MOBY.index(corpo_atual),
            key="moby_size_pick", on_change=sidebar_size_changed,
        )
    st.session_state.moby_font_family = fonte_lookup.get(fonte_escolhida, st.session_state.moby_font_family)
    st.session_state.moby_font_size = int(corpo_escolhido)

    if st.button("Fechar", key="moby_close_sidebar", width="stretch"):
        st.session_state.moby_sidebar_open = False
        st.rerun()

    st.stop()


# =============================================================================
# LIVRO + OLA + TEMA / OFF-MACHINA
# =============================================================================
if st.session_state.get("moby_mode") == "Off-Machina":
    livros_off = off_books()
    if not livros_off:
        st.error("Off-Machina não encontrou arquivos .Pip em ./off_machina.")
        st.stop()

    nomes_off = [p.stem for p in livros_off]
    idx_off = int(st.session_state.get("moby_off_book_index", 0)) % len(livros_off)
    col_book, col_ola, col_theme = st.columns([3, 1.25, 3], gap="small")
    with col_book:
        livro_off = st.selectbox("Livro", nomes_off, index=idx_off, key="moby_off_book_pick")
        novo_idx = nomes_off.index(livro_off)
        if novo_idx != st.session_state.moby_off_book_index:
            st.session_state.moby_off_book_index = novo_idx
            st.session_state.moby_off_take = 0
            invalidate_real_image()
            invalidate_ola()
            st.rerun()

    paginas_off = current_off_pages()
    if not paginas_off:
        st.error(f'Off-Machina não encontrou páginas em "{livro_off}".')
        st.stop()
    titulos_off = [titulo for titulo, _ in paginas_off]
    st.session_state.moby_off_take %= len(paginas_off)
    st.session_state["moby_off_page_pick"] = titulos_off[st.session_state.moby_off_take]

    with col_ola:
        st.markdown("<div style='height:1.45rem'></div>", unsafe_allow_html=True)
        st.button("OLA", key="moby_ola_focus_off", width="stretch", on_click=request_ola)

    with col_theme:
        titulo_off = st.selectbox("Tema", titulos_off, key="moby_off_page_pick")
        novo_take = titulos_off.index(titulo_off)
        if novo_take != st.session_state.moby_off_take:
            st.session_state.moby_off_take = novo_take
            invalidate_real_image()
            invalidate_ola()
            st.rerun()
else:
    temas = current_themes()
    if not temas:
        st.error(f'O DNA não contém temas ativos para o livro "{st.session_state.moby_book}".')
        st.stop()

    st.session_state["moby_theme_pick"] = current_theme()
    col_book, col_ola, col_theme = st.columns([3, 1.25, 3], gap="small")
    with col_book:
        st.selectbox("Livro", MOBY_BOOKS, key="moby_book", on_change=book_changed)
    with col_ola:
        st.markdown("<div style='height:1.45rem'></div>", unsafe_allow_html=True)
        st.button("OLA", key="moby_ola_focus", width="stretch", on_click=request_ola)
    with col_theme:
        st.selectbox("Tema", temas, key="moby_theme_pick", on_change=theme_picked)


# =============================================================================
# PAINEL DE COMANDO DO LEITOR
# =============================================================================
b_plus, b_prev, b_rand, b_next, b_sound, b_help = st.columns(6, gap="small")

with b_plus:
    st.button(
        "+",
        key="moby_plus",
        width="stretch",
        on_click=new_reading,
    )

with b_prev:
    st.button(
        "<",
        key="moby_prev",
        width="stretch",
        on_click=previous_theme,
    )

with b_rand:
    st.button(
        "*",
        key="moby_rand",
        width="stretch",
        on_click=random_theme,
    )

with b_next:
    st.button(
        ">",
        key="moby_next",
        width="stretch",
        on_click=next_theme,
    )

with b_sound:
    st.button(
        "♫",
        key="moby_sound",
        width="stretch",
        on_click=dismiss_help,
    )

with b_help:
    st.button(
        "?",
        key="moby_help",
        width="stretch",
        on_click=toggle_help,
    )


if st.session_state.moby_help_open:
    st.markdown(
        """
        <div class="moby-help">
        <ul>
          <li><b>+</b> nova leitura do tema</li>
          <li><b>&lt;</b> tema anterior</li>
          <li><b>*</b> tema ao acaso</li>
          <li><b>&gt;</b> próximo tema</li>
          <li><b>♫</b> som</li>
          <li><b>?</b> help</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# PALCO DE PROVA
# =============================================================================
fonte_palco = str(st.session_state.get("moby_font_family", "Trebuchet MS"))
fonte_css = fonte_palco_css(fonte_palco)
corpo_palco = int(st.session_state.get("moby_font_size", 16))
altura_palco = 315 if st.session_state.moby_image_visible else 520

if st.session_state.get("moby_mode") == "Off-Machina":
    titulo_palco, corpo_off = current_off_page()
    poema_html = html.escape(str(corpo_off)).replace("\n", "<br>")
else:
    update_real_poem()
    titulo_palco = current_theme()
    poema_html = st.session_state.get("moby_poem_html", "")

# Aspas simples no atributo: as pilhas CSS contêm aspas duplas nos nomes das fontes.
st.markdown(
    f"<div class='poem-title' style='font-family:{fonte_css}; font-size:{corpo_palco}px;'>"
    f"{html.escape(str(titulo_palco))}</div>",
    unsafe_allow_html=True,
)

analise_ola = update_ola_analysis(titulo_palco, poema_html)
ola_html = ""
if analise_ola:
    ola_html = (
        "<div class='moby-ola-inline'>"
        "<div class='moby-ola-inline-title'>OLA</div>"
        + html.escape(str(analise_ola)).replace("\n", "<br>")
        + "</div>"
    )

st.markdown(
    f"<div class='ypoema' style='font-family:{fonte_css}; font-size:{corpo_palco}px; height:{altura_palco}px; max-height:{altura_palco}px;'>"
    f"{poema_html}{ola_html}</div>",
    unsafe_allow_html=True,
)

st.markdown('<div class="end-rule"></div>', unsafe_allow_html=True)


# =============================================================================
# AÇÕES FINAIS
# =============================================================================
c1, c2, c3 = st.columns(3, gap="small")

with c1:
    st.button("Copiar", key="moby_copy", width="stretch", on_click=dismiss_help)

with c2:
    st.button("Imagem", key="moby_image", width="stretch", on_click=toggle_image)

with c3:
    st.button("Retrato", key="moby_portrait", width="stretch", on_click=prepare_portrait)

# Duas imagens distintas do mesmo banco temático no rodapé — apenas FIT.
update_real_image()
imagem_1 = str(st.session_state.get("moby_image_path", "")).strip()
imagem_2 = str(st.session_state.get("moby_image_path_2", "")).strip()

if st.session_state.moby_image_visible:
    def _img_data_uri(path_text):
        path = Path(path_text)
        if not path.is_file():
            return ""
        try:
            payload = base64.b64encode(path.read_bytes()).decode("ascii")
        except OSError:
            return ""
        ext = path.suffix.lower().lstrip(".")
        mime = "jpeg" if ext in {"jpg", "jpeg"} else (ext or "jpeg")
        return f"data:image/{mime};base64,{payload}"

    uri_1 = _img_data_uri(imagem_1)
    uri_2 = _img_data_uri(imagem_2)

    def _foto_html(uri, alt):
        if not uri:
            return ""
        return (
            f'<img src="{uri}" alt="{alt}" '
            'style="max-width:100%; max-height:185px; width:auto; height:auto; object-fit:contain; display:block;" />'
        )

    foto_1 = _foto_html(uri_1, "imagem temática 1")
    foto_2 = _foto_html(uri_2, "imagem temática 2")

    st.markdown(
        f"""
        <div style="height:205px; width:100%; display:flex; align-items:center; justify-content:center; gap:10px; overflow:hidden; padding:5px 4px 10px 4px; box-sizing:border-box;">
            <div style="width:187px; height:185px; display:flex; align-items:center; justify-content:center; overflow:hidden;">
                {foto_1}
            </div>
            <div style="width:187px; height:185px; display:flex; align-items:center; justify-content:center; overflow:hidden;">
                {foto_2}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
