# moby_v063.py
# Etapa 063: EUREKA substitui OLA no Moby; usa listas existentes e preserva o palco.
# MACHINA — Mobile ultra-light
# Blindagem HTML preservada; não altera basico.py, DNA, .ypo, .pip ou conteúdo autoral.

from pathlib import Path
import asyncio
import base64
import html
import importlib.util
import os
import random
import re
import unicodedata
import urllib.parse
import urllib.request
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont, ImageOps
import streamlit as st

try:
    import edge_tts
except Exception:
    edge_tts = None

try:
    from deep_translator import GoogleTranslator
except Exception:
    GoogleTranslator = None

from lay_2_ypo import gera_poema


def _bootstrap_openai_key():
    """No Streamlit Cloud, expõe a secret também ao bridge OLA legado."""
    if os.getenv("OPENAI_API_KEY", "").strip():
        return
    try:
        key = str(st.secrets.get("OPENAI_API_KEY", "")).strip()
    except Exception:
        key = ""
    if key:
        os.environ["OPENAI_API_KEY"] = key


def _load_ola_bridge():
    """Aceita a ponte na raiz ou em ./md_files, como no repositório atual."""
    _bootstrap_openai_key()
    try:
        from ponte_ola_openai import gerar_analise_ola
        return gerar_analise_ola
    except Exception:
        pass

    bridge_path = Path("./md_files/ponte_ola_openai.py")
    if not bridge_path.is_file():
        return None
    try:
        spec = importlib.util.spec_from_file_location("moby_ponte_ola_openai", bridge_path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, "gerar_analise_ola", None)
    except Exception:
        return None


st.set_page_config(
    page_title="Moby — a Machina Mobile",
    page_icon="❓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


_gerar_analise_ola_real = _load_ola_bridge()


# =============================================================================
# DNA — autoridade das listas do Moby
# =============================================================================
DNA_PATH = Path("./base/DNA.TXT")
LINKS_PATH = Path("./base/links.txt")
IMAGES_ROOT = Path("./images")
IMAGES_MAP_PATH = Path("./base/images.txt")
OFF_DIR = Path("./off_machina")

# Autoridade autoral do Off-Machina: existir como .pip não publica um livro.
OFF_BOOKS_LIST = [
    "a_torre_de_papel",
    "quase_que_eu_Poesia",
    "faz_de_conto",
    "um_romance",
    "parafernália",
    "linguafiada",
    "livro_vivo",
    "desvoto",
    "ensaios",
    "urbano",
    "essencial",
    "secreto",
    "cunho",
]

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
    ("OpenDyslexic", "OpenDyslexic"),
    ("MV Boli", "MV Boli"),
    ("Source Code SemiBold", "Source Code Pro"),
    ("Comic Relief", "Comic Relief"),
    ("JetBrains Mono", "JetBrains Mono"),
    ("Ubuntu Condensed", "Ubuntu Condensed"),
]

# Conjunto único de variantes para as seis famílias.
# A permanência de cada variante será decidida pelo efeito visual real no palco.
ESTILOS_MACHINA = [
    "normal",
    "itálico",
    "bold",
    "bold itálico",
]

FONTES_PESO_BASE = {
    "OpenDyslexic": 400,
    "MV Boli": 400,
    "Source Code Pro": 600,
    "Comic Relief": 400,
    "JetBrains Mono": 400,
    "Ubuntu Condensed": 400,
}

# Famílias web abertas; OpenDyslexic e eventuais arquivos locais continuam
# podendo ser servidos pela pasta ./fonts.
GOOGLE_FONTS_CSS = (
    "https://fonts.googleapis.com/css2?"
    "family=Comic+Relief:ital,wght@0,400;0,700;1,400;1,700&"
    "family=JetBrains+Mono:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&"
    "family=Source+Code+Pro:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&"
    "family=Ubuntu+Condensed&"
    "display=swap"
)

FONTES_PALCO_CSS = {
    "OpenDyslexic": '"OpenDyslexic", sans-serif',
    "MV Boli": '"MV Boli", "Segoe Print", cursive',
    "Source Code Pro": '"Source Code Pro", Consolas, "Courier New", monospace',
    "Comic Relief": '"Comic Relief", "Comic Sans MS", cursive',
    "JetBrains Mono": '"JetBrains Mono", Consolas, "Courier New", monospace',
    "Ubuntu Condensed": '"Ubuntu Condensed", "Arial Narrow", Arial, sans-serif',
}

def fonte_palco_css(family=None):
    family = str(family or st.session_state.get("moby_font_family", "Comic Relief")).strip()
    return FONTES_PALCO_CSS.get(family, f'"{family}", sans-serif')

def estilo_palco_atual():
    estilo = str(st.session_state.get("moby_font_style", "normal")).strip().casefold()
    return estilo if estilo in ESTILOS_MACHINA else "normal"

def estilo_palco_css(family=None, estilo=None):
    family = str(family or st.session_state.get("moby_font_family", "Comic Relief")).strip()
    estilo = str(estilo or estilo_palco_atual()).strip().casefold()
    peso_base = int(FONTES_PESO_BASE.get(family, 400))
    peso = 700 if "bold" in estilo else peso_base
    inclinacao = "italic" if "itálico" in estilo else "normal"
    return peso, inclinacao

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
        
/* Moby: remove o controle interno "Clear value" dos selectbox. */
[data-baseweb="select"] [aria-label="Clear value"] {{
    display: none !important;
}}
</style>
        """,
        unsafe_allow_html=True,
    )

CORPOS_MOBY = list(range(16, 37, 1))


VOICES_EDGE_TTS = {
    "pt": "pt-BR-FranciscaNeural", "es": "es-ES-AlvaroNeural",
    "fr": "fr-FR-HenriNeural", "it": "it-IT-DiegoNeural",
    "en": "en-US-AvaNeural", "gl": "gl-ES-RoiNeural",
    "eu": "eu-ES-AnderNeural", "de": "de-DE-ConradNeural",
    "da": "da-DK-JeppeNeural", "nl": "nl-NL-MaartenNeural",
    "pl": "pl-PL-MarekNeural", "ro": "ro-RO-EmilNeural",
    "no": "nb-NO-PernilleNeural", "fi": "fi-FI-SelmaNeural",
    "is": "is-IS-GunnarNeural", "hu": "hu-HU-TamasNeural",
    "sv": "sv-SE-MattiasNeural", "ca": "ca-ES-EnricNeural",
    "ru": "ru-RU-DmitryNeural",
}


RETRATO_WEBFONT_FAMILIES = {
    "JetBrains Mono",
    "Source Code Pro",
    "Comic Relief",
    "Ubuntu Condensed",
}


def _font_key(value):
    value = unicodedata.normalize("NFKD", str(value or "")).casefold()
    return re.sub(
        r"[^a-z0-9]+",
        "",
        "".join(ch for ch in value if not unicodedata.combining(ch)),
    )


def _moby_local_font_files(family):
    """Localiza em ./fonts arquivos pertencentes à família escolhida."""
    family = str(family or "").strip()
    fonts_dir = Path("./fonts")
    if not family or not fonts_dir.is_dir():
        return []

    wanted = _font_key(family)
    aliases = {
        "sourcecodepro": {"sourcecodepro", "sourcecodesemibold"},
        "mvboli": {"mvboli"},
        "comicrelief": {"comicrelief"},
        "jetbrainsmono": {"jetbrainsmono"},
        "ubuntucondensed": {"ubuntucondensed"},
        "opendyslexic": {"opendyslexic"},
    }
    targets = aliases.get(wanted, {wanted})
    found = []

    for path in sorted(fonts_dir.iterdir()):
        if not path.is_file() or path.suffix.casefold() not in {".ttf", ".otf", ".woff", ".woff2"}:
            continue

        file_key = _font_key(path.stem)
        matched = any(target and target in file_key for target in targets)

        if not matched:
            try:
                probe = ImageFont.truetype(str(path), 14)
                real_family, _real_style = probe.getname()
                real_key = _font_key(real_family)
                matched = any(
                    target and (target in real_key or real_key in target)
                    for target in targets
                )
            except Exception:
                matched = False

        if matched:
            found.append(path)

    return found


def _moby_google_font_urls(family, bold=False):
    """Obtém a mesma família web usada pelo palco para o PNG do Retrato."""
    family = str(family or "").strip()
    if family not in RETRATO_WEBFONT_FAMILIES:
        return []

    base_weight = int(FONTES_PESO_BASE.get(family, 400))
    weight = 700 if bold else base_weight
    query_family = urllib.parse.quote_plus(family)
    css_url = (
        "https://fonts.googleapis.com/css2?"
        f"family={query_family}:wght@{weight}&display=swap"
    )

    try:
        req = urllib.request.Request(
            css_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/152 Safari/537.36"
                )
            },
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            css = response.read().decode("utf-8", errors="replace")
    except Exception:
        return []

    urls = re.findall(r"url\\((https://[^)]+)\\)", css)
    return list(dict.fromkeys(reversed(urls)))


def _moby_webfont_cache(family, bold=False):
    """Cache temporário da webfont selecionada para uso pelo Pillow."""
    urls = _moby_google_font_urls(family, bold=bold)
    if not urls:
        return None

    cache_dir = Path("./temp/font_cache")
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        return None

    base_weight = int(FONTES_PESO_BASE.get(family, 400))
    weight = 700 if bold else base_weight
    safe = re.sub(r"[^A-Za-z0-9_-]+", "_", str(family)).strip("_") or "font"

    for index, url in enumerate(urls):
        ext = ".woff2" if ".woff2" in url.casefold() else ".woff"
        target = cache_dir / f"{safe}_{weight}_{index}{ext}"

        try:
            if not (target.is_file() and target.stat().st_size > 1024):
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "Mozilla/5.0 Machina-yPoemas"},
                )
                with urllib.request.urlopen(req, timeout=8) as response:
                    data = response.read()
                if len(data) <= 1024:
                    continue
                target.write_bytes(data)

            test_font = ImageFont.truetype(str(target), size=18)
            del test_font
            return target
        except Exception:
            try:
                if target.is_file():
                    target.unlink()
            except Exception:
                pass

    return None


def _moby_font(size, bold=False, family=None):
    """Carrega no Retrato a família que o leitor selecionou no Moby."""
    family = str(
        family or st.session_state.get("moby_font_family", "OpenDyslexic")
    ).strip()

    candidates = []

    local_files = _moby_local_font_files(family)

    def score_font(path):
        low = path.name.casefold()
        is_bold = any(tag in low for tag in ("bold", "semibold", "demibold", "600", "700"))
        if family == "Source Code Pro" and not bold:
            return (0 if ("semibold" in low or "600" in low) else 1, len(low), low)
        return (0 if bool(is_bold) == bool(bold) else 1, len(low), low)

    candidates.extend(sorted(local_files, key=score_font))

    if family == "OpenDyslexic":
        candidates.append(
            Path("./fonts/OpenDyslexic-Bold.otf" if bold else "./fonts/OpenDyslexic-Regular.otf")
        )

    # MV Boli é família nativa do Windows; usa-a quando realmente disponível.
    if family == "MV Boli":
        candidates.extend([
            Path("C:/Windows/Fonts/mvboli.ttf"),
            Path("mvboli.ttf"),
        ])

    webfont = _moby_webfont_cache(family, bold=bold)
    if webfont is not None:
        candidates.append(webfont)

    # Fallback técnico apenas se a família escolhida não estiver disponível.
    candidates.extend([
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ])

    for candidate in candidates:
        try:
            if candidate.is_file():
                return ImageFont.truetype(str(candidate), int(size))
        except Exception:
            pass

    return ImageFont.load_default()


def _wrap_portrait(draw, text, font, width):
    lines = []
    for raw in str(text or "").splitlines():
        if not raw.strip():
            lines.append("")
            continue
        indent = len(raw) - len(raw.lstrip("  "))
        prefix = " " * indent
        words = raw.strip().split()
        current = prefix
        for word in words:
            trial = (current + " " + word).rstrip() if current.strip() else prefix + word
            if draw.textbbox((0, 0), trial, font=font)[2] <= width:
                current = trial
            else:
                if current.strip():
                    lines.append(current)
                current = prefix + word
        lines.append(current)
    return lines


def create_moby_portrait_png(poem_html, image_path, title):
    """Retrato do texto atual com uma das duas imagens que a Machina mostrou."""
    if not image_path or not Path(image_path).is_file():
        return None
    body = ypoema_html_to_text(poem_html)
    if not body:
        return None
    body = (str(title or "").strip() + "\n\n" + body).strip()
    margin, gap = 54, 44
    portrait_family = "OpenDyslexic"
    portrait_style = estilo_palco_atual()
    portrait_bold = "bold" in portrait_style
    body_font = _moby_font(28, bold=portrait_bold, family=portrait_family)
    footer_font = _moby_font(17, family=portrait_family)
    measure = Image.new("RGB", (1, 1), "white")
    draw = ImageDraw.Draw(measure)
    with Image.open(image_path) as source:
        art = ImageOps.exif_transpose(source).convert("RGB")
        scale = min(1.0, 360 / max(1, art.width))
        art = art.resize((max(1, round(art.width * scale)), max(1, round(art.height * scale))), Image.Resampling.LANCZOS)
    lines = _wrap_portrait(draw, body, body_font, 720)
    bbox = draw.textbbox((0, 0), "Ag", font=body_font)
    line_h = max(34, bbox[3] - bbox[1] + 9)
    text_h = max(line_h, len(lines) * line_h)
    canvas_w = max(760, margin + art.width + gap + 720 + margin)
    canvas_h = max(520, margin + max(art.height, text_h) + 62 + margin)
    canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
    canvas.paste(art, (margin, max(margin, (canvas_h - 62 - art.height)//2)))
    draw = ImageDraw.Draw(canvas)
    x, y = margin + art.width + gap, margin
    for line in lines:
        draw.text((x, y), line, font=body_font, fill="black")
        y += line_h
    footer = "ypoemas.streamlit.app"
    fb = draw.textbbox((0, 0), footer, font=footer_font)
    draw.text((canvas_w - margin - (fb[2]-fb[0]), canvas_h - margin - (fb[3]-fb[1])), footer, font=footer_font, fill=(60,60,60))
    output = BytesIO()
    canvas.save(output, format="PNG", optimize=True)
    return output.getvalue()


ABOUTS_FALLBACK = [
    ("comentários", "ABOUT_comentários.md"),
    ("prefácil", "ABOUT_prefácil.md"),
    ("notes", "ABOUT_notes.md"),
    ("machina", "ABOUT_machine.md"),
    ("off-machina", "ABOUT_off-machina.md"),
    ("outros autores", "ABOUT_outros_autores.md"),
    ("livros", "ABOUT_livros.md"),
    ("bibliografia", "ABOUT_bibliografia.md"),
    ("versão Mobile", "ABOUT_mobile.md"),
    ("imagens", "ABOUT_imagens.md"),
    ("seleção das imagens", "ABOUT_seleção das imagens"),
    ("certidão de nascimento", "ABOUT_certidão de nascimento"),
    ("ítimos", "ABOUT_ítimos.md"),
    ("o átomo do ítimo", "ABOUT_o átomo do ítimo.md"),
    ("eixo Z", "ABOUT_eixo_Z.md"),
    ("pontuação", "ABOUT_pontuação.md"),
    ("poly", "ABOUT_poly.md"),
    ("tradittore", "ABOUT_tradittore.md"),
    ("veredas", "ABOUT_veredas.md"),
    ("carta de Guimarães Rosa", "A incrível carta de Guimarães Rosa.md"),
    ("samizdàt", "ABOUT_samizdàt.md"),
    ("a ABA da Machina", "a ABA da Machina.md"),
    ("anjos", "ABOUT_Augusto dos Anjos.md"),
    ("o Autor e uma IA - conversas", "ABOUT_Autor_da_Machina_e_uma_IA.md"),
    ("machina-IA", "ABOUT_machina-IA.md"),
    ("icones", "ABOUT_icones.md"),
    ("pensares", "ABOUT_pensares.md"),
    ("index", "ABOUT_index.md"),
    ("license", "ABOUT_license.md"),
]


def load_about_catalog(path=Path("./base/lista_abouts.txt")):
    """A lista autoral em base/lista_abouts.txt é a autoridade do ABOUT."""
    rows = []
    if path.is_file():
        try:
            for raw in path.read_text(encoding="utf-8-sig").splitlines():
                line = raw.strip()
                if not line:
                    continue
                if line == "<EOF>":
                    break
                if "|" not in line:
                    continue
                title, filename = line.split("|", 1)
                title = title.strip()
                filename = filename.strip().strip('"').strip()
                if title:
                    rows.append((title, filename))
        except OSError:
            rows = []
    return rows or list(ABOUTS_FALLBACK)


ABOUTS_CATALOG = load_about_catalog()
ABOUTS_LIST = [title for title, _ in ABOUTS_CATALOG]
ABOUTS_FILES = {title: [filename] for title, filename in ABOUTS_CATALOG if filename}

ABOUT_ALIASES = {
    "machina": ["ABOUT_machine.md", "ABOUT_machina.md"],
    "versão Mobile": ["ABOUT_mobile.md"],
    "carta de Guimarães Rosa": ["A incrível carta de Guimarães Rosa.md"],
    "off-machina": ["ABOUT_off-machina.md", "ABOUT_off_machina.md", "ABOUT_off machina.md"],
    "outros autores": ["ABOUT_outros_autores.md", "ABOUT_outros autores.md"],
}


OUTLOOK_ICON_DATA = "data:image/svg+xml;base64," + base64.b64encode(
    b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect x="10" y="12" width="44" height="40" rx="5" fill="#0A64C9"/>
<path d="M14 20h36v26H14z" fill="#1B78D0"/>
<path d="M14 21l18 14 18-14" fill="none" stroke="white" stroke-width="4" stroke-linejoin="round"/>
<rect x="6" y="16" width="25" height="32" rx="3" fill="#075FB5"/>
<circle cx="18.5" cy="32" r="8.5" fill="none" stroke="white" stroke-width="4"/>
</svg>"""
).decode("ascii")


PERSONAL_LINKS = [
    {
        "label": "Facebook",
        "url": "https://www.facebook.com/nandoulopes",
        "icon": "https://cdn.simpleicons.org/facebook/1877F2",
        "kind": "facebook",
    },
    {
        "label": "Instagram",
        "url": "https://www.instagram.com/fernando.lopes.942/",
        "icon": "https://cdn.simpleicons.org/instagram/E4405F",
        "kind": "instagram",
    },
    {
        "label": "Outlook",
        "url": "mailto:lopes.fernando@hotmail.com",
        "icon": OUTLOOK_ICON_DATA,
        "kind": "outlook",
    },
    {
        "label": "Gmail",
        "url": "mailto:lopes.fernando@gmail.com",
        "icon": "https://cdn.simpleicons.org/gmail/EA4335",
        "kind": "gmail",
    },
    {
        "label": "Buy Me a Coffee",
        "url": "https://www.buymeacoffee.com/yPoemas",
        "icon": "https://cdn.simpleicons.org/buymeacoffee/FFDD00",
        "kind": "coffee",
    },
    {
        "label": "WhatsApp / Pix",
        "url": "https://wa.me/5512991368181",
        "icon": "https://cdn.simpleicons.org/whatsapp/25D366",
        "icon_2": "https://cdn.simpleicons.org/pix/32BCAD",
        "kind": "whatsapp",
    },
]


def _doc_key(value):
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def _about_candidates(title):
    aliases = list(ABOUTS_FILES.get(title, [])) + list(ABOUT_ALIASES.get(title, []))
    aliases.extend([
        f"ABOUT_{title}.md",
        f"ABOUT_{title.replace(' ', '_')}.md",
        f"ABOUT_{title.replace(' ', '-')}.md",
    ])
    return aliases


def load_manual_moby():
    path = Path("./md_files/Manual_Moby.md")
    try:
        return path.read_text(encoding="utf-8-sig")
    except OSError:
        return 'ooops... documentação "Manual_Moby.md" não encontrada.'


def load_about_text(title):
    roots = [Path("./md_files"), Path(".")]
    candidates = _about_candidates(title)
    candidate_keys = {_doc_key(Path(name).stem) for name in candidates}
    title_keys = {_doc_key(title), _doc_key("ABOUT_" + title)}

    for root in roots:
        if not root.exists():
            continue
        for name in candidates:
            direct = root / name
            if direct.is_file():
                try:
                    return direct.read_text(encoding="utf-8-sig")
                except OSError:
                    pass
        try:
            for path in root.rglob("*.md"):
                stem_key = _doc_key(path.stem)
                if stem_key in candidate_keys or stem_key in title_keys:
                    try:
                        return path.read_text(encoding="utf-8-sig")
                    except OSError:
                        continue
        except OSError:
            pass
    return f'ooops... documentação "{title}" não encontrada.'


def translate_poem_html(poem_html):
    """Mesmo mecanismo histórico da Machina: traduz o yPoema, preservando <br>."""
    lang = str(st.session_state.get("moby_lang", "pt"))
    source = str(poem_html or "")
    if lang == "pt" or not source.strip() or GoogleTranslator is None:
        return source

    signature = (lang, source)
    if st.session_state.get("moby_translation_signature") == signature:
        return st.session_state.get("moby_translation_html", source)

    try:
        translated = GoogleTranslator(source="pt", target=lang).translate(text=source)
        translated = str(translated or source)
        translated = translated.replace("<br>>", "<br>")
        translated = translated.replace("< br>", "<br>")
        translated = translated.replace("<br >", "<br>")
        translated = translated.replace("<br ", "<br>")
        translated = translated.replace(" br>", "<br>")
    except Exception:
        translated = source

    st.session_state.moby_translation_signature = signature
    st.session_state.moby_translation_html = translated
    return translated

def _moby_eureka_mark_html(texto_html, termo):
    """Destaca TODAS as aparições da ocorrência EUREKA no texto visível."""
    texto_html = str(texto_html or "")
    termo = str(termo or "").strip()
    if not termo:
        return texto_html

    # O motor histórico já pode devolver uma marca única. Normalizamos primeiro
    # para impedir marca parcial/nested e depois marcamos todas as aparições.
    texto_html = re.sub(r"</?mark>", "", texto_html, flags=re.IGNORECASE)
    texto_html = texto_html.replace("&lt;mark&gt;", "").replace("&lt;/mark&gt;", "")

    pattern = re.compile(re.escape(termo), flags=re.IGNORECASE)
    partes = []
    for trecho in re.split(r"(<[^>]+>)", texto_html):
        if trecho.startswith("<") and trecho.endswith(">"):
            partes.append(trecho)
        else:
            partes.append(
                pattern.sub(lambda m: "<mark>" + m.group(0) + "</mark>", trecho)
            )
    return "".join(partes)


def sidebar_show_about():
    st.session_state.moby_sidebar_panel = "about"


def sidebar_show_links():
    st.session_state.moby_sidebar_panel = "links"


def sidebar_return_to_stage():
    """Fecha a documentação e devolve imediatamente o leitor ao palco."""
    st.session_state.moby_sidebar_open = False


def render_social_links():
    """Painel visual direto: presença da Machina no mundo, sem paginação."""
    cards = []
    for item in PERSONAL_LINKS:
        label = html.escape(str(item.get("label", "")))
        url = html.escape(str(item.get("url", "")), quote=True)
        icon = html.escape(str(item.get("icon", "")), quote=True)
        icon_2 = html.escape(str(item.get("icon_2", "")), quote=True)
        kind = html.escape(str(item.get("kind", "")), quote=True)

        icons = f"<img src='{icon}' alt='' loading='lazy'>"
        if icon_2:
            icons += f"<img src='{icon_2}' alt='' loading='lazy'>"

        external = "" if url.startswith("mailto:") else " target='_blank' rel='noopener noreferrer'"
        cards.append(
            f"<a class='moby-social-card {kind}' href='{url}'{external}>"
            f"<span class='moby-social-icons'>{icons}</span>"
            f"<span class='moby-social-label'>{label}</span>"
            "</a>"
        )

    st.markdown(
        "<div class='moby-social-stage'>"
        "<div class='moby-social-grid'>"
        + "".join(cards)
        + "</div></div>",
        unsafe_allow_html=True,
    )


def toggle_sound():
    dismiss_help()
    st.session_state.moby_sound_open = not bool(st.session_state.get("moby_sound_open", False))


def _generate_sound_bytes(text):
    if edge_tts is None:
        return b""
    clean = re.sub(r"\s+", " ", str(text or "")).strip()
    if not clean:
        return b""
    voice = VOICES_EDGE_TTS.get(st.session_state.get("moby_lang", "pt"), "pt-BR-FranciscaNeural")
    async def _run():
        audio = bytearray()
        communicate = edge_tts.Communicate(clean, voice)
        async for chunk in communicate.stream():
            if chunk.get("type") == "audio":
                audio.extend(chunk.get("data", b""))
        return bytes(audio)
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(_run())
    finally:
        loop.close()


def update_sound_audio(title, poem_html):
    """A voz lê somente o conteúdo; o título dá lugar ao player."""
    body = ypoema_html_to_text(poem_html)
    signature = (st.session_state.get("moby_lang", "pt"), str(title), body)
    if st.session_state.get("moby_sound_signature") == signature:
        return st.session_state.get("moby_sound_audio", b"")
    try:
        audio = _generate_sound_bytes(body)
    except Exception:
        audio = b""
    st.session_state.moby_sound_signature = signature
    st.session_state.moby_sound_audio = audio
    return audio


def render_sound_player(audio_bytes):
    if not audio_bytes:
        st.markdown("<div class='moby-sound-slot'>som indisponível</div>", unsafe_allow_html=True)
        return
    payload = base64.b64encode(audio_bytes).decode("ascii")
    st.markdown(
        f"<div class='moby-sound-slot'><audio controls autoplay preload='auto' src='data:audio/mpeg;base64,{payload}'></audio></div>",
        unsafe_allow_html=True,
    )


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


def _rol_temas(livro):
    """Lê a ordem autoral do livro em base/rol_<livro>.txt."""
    path = Path("./base") / f"rol_{livro}.txt"
    if not path.is_file():
        return []
    temas = []
    try:
        for raw in path.read_text(encoding="utf-8-sig").splitlines():
            tema = raw.strip().strip("|").strip()
            if not tema or tema.startswith("#") or tema == "<EOF>":
                continue
            temas.append(tema)
    except OSError:
        return []
    return temas


def temas_do_livro(rows, livro):
    """rol_<livro>.txt é a autoridade integral de conteúdo e ordem; DNA é fallback."""
    ordem = _rol_temas(livro)
    if ordem:
        return ordem

    alvo = str(livro or "").strip().casefold()
    temas = []
    vistos = set()
    for row in rows:
        if str(row.get("ativo", "")).strip().upper() != "S":
            continue
        livros = [item.strip().casefold() for item in str(row.get("livro", "")).split(";") if item.strip()]
        tema = str(row.get("tema", "")).strip()
        chave = nome_normalizado(tema)
        if tema and alvo in livros and chave not in vistos:
            temas.append(tema)
            vistos.add(chave)
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

if "moby_footer_view" not in st.session_state:
    st.session_state.moby_footer_view = "images"


if "moby_arts" not in st.session_state:
    st.session_state.moby_arts = []

if "moby_poem_signature" not in st.session_state:
    st.session_state.moby_poem_signature = None

if "moby_poem_html" not in st.session_state:
    st.session_state.moby_poem_html = ""


if "moby_lang" not in st.session_state:
    st.session_state.moby_lang = "pt"

if "moby_font_family" not in st.session_state:
    st.session_state.moby_font_family = "Comic Relief"

if "moby_font_style" not in st.session_state:
    st.session_state.moby_font_style = "normal"

if "moby_font_size" not in st.session_state:
    st.session_state.moby_font_size = 20

if "moby_mode" not in st.session_state:
    st.session_state.moby_mode = "Machina"

if "moby_off_book_index" not in st.session_state:
    st.session_state.moby_off_book_index = 0

if "moby_off_take" not in st.session_state:
    st.session_state.moby_off_take = 0

if "moby_off_plus_help" not in st.session_state:
    st.session_state.moby_off_plus_help = False

if "moby_ola_requested" not in st.session_state:
    st.session_state.moby_ola_requested = False

if "moby_ola_signature" not in st.session_state:
    st.session_state.moby_ola_signature = None

if "moby_ola_text" not in st.session_state:
    st.session_state.moby_ola_text = ""

if "moby_eureka_open" not in st.session_state:
    st.session_state.moby_eureka_open = False
if "moby_eureka_seed" not in st.session_state:
    st.session_state.moby_eureka_seed = ""
if "moby_eureka_index" not in st.session_state:
    st.session_state.moby_eureka_index = 0
if "moby_eureka_pick" not in st.session_state:
    st.session_state.moby_eureka_pick = ""

if "moby_eureka_mark_term" not in st.session_state:
    st.session_state.moby_eureka_mark_term = ""

if "moby_eureka_seed_ref" not in st.session_state:
    st.session_state.moby_eureka_seed_ref = ""

if "moby_eureka_tema_motor" not in st.session_state:
    st.session_state.moby_eureka_tema_motor = ""

if "moby_analysis_kind" not in st.session_state:
    st.session_state.moby_analysis_kind = "Sintática"

if "moby_portrait_image" not in st.session_state:
    st.session_state.moby_portrait_image = ""
if "moby_portrait_png" not in st.session_state:
    st.session_state.moby_portrait_png = b""
if "moby_portrait_name" not in st.session_state:
    st.session_state.moby_portrait_name = "retrato"
if "moby_sound_open" not in st.session_state:
    st.session_state.moby_sound_open = False
if "moby_sound_audio" not in st.session_state:
    st.session_state.moby_sound_audio = b""
if "moby_sound_signature" not in st.session_state:
    st.session_state.moby_sound_signature = None
if "moby_current_title" not in st.session_state:
    st.session_state.moby_current_title = ""
if "moby_current_poem_html" not in st.session_state:
    st.session_state.moby_current_poem_html = ""
if "moby_translation_signature" not in st.session_state:
    st.session_state.moby_translation_signature = None
if "moby_translation_html" not in st.session_state:
    st.session_state.moby_translation_html = ""
if "moby_sidebar_panel" not in st.session_state:
    st.session_state.moby_sidebar_panel = "about"
if "moby_about_pick" not in st.session_state:
    st.session_state.moby_about_pick = "machina"

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
    """Livros Off-Machina publicados, na ordem da autoridade autoral."""
    if not OFF_DIR.is_dir():
        return []

    pip_por_nome = {
        path.stem.casefold(): path
        for path in OFF_DIR.iterdir()
        if path.is_file() and path.suffix.casefold() == ".pip"
    }

    return [
        pip_por_nome[nome.casefold()]
        for nome in OFF_BOOKS_LIST
        if nome.casefold() in pip_por_nome
    ]


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
        marcador = line.strip()
        if marcador == "<EOF>" or marcador.strip("|").strip() == "<EOF>":
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
    """LINK navega somente dentro do livro atualmente selecionado."""
    destino = str(st.session_state.get("moby_link_pending", "")).strip()
    if not destino:
        return

    livro_atual = str(st.session_state.get("moby_book", "")).strip()
    temas = temas_do_livro(DNA_ROWS, livro_atual)
    alvo = nome_normalizado(destino)

    for idx, tema in enumerate(temas):
        if nome_normalizado(tema) == alvo:
            st.session_state.moby_theme_index = idx
            st.session_state["moby_theme_pick"] = tema
            st.session_state.moby_reading_n = 1
            invalidate_real_poem()
            invalidate_real_image()
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
    """Força nova dupla de imagens sem alterar o yPoema."""
    st.session_state.moby_image_theme = ""
    st.session_state.moby_image_path = ""
    st.session_state.moby_image_path_2 = ""
    st.session_state.moby_portrait_png = b""
    st.session_state.moby_portrait_image = ""


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


def image_path_to_data_uri(path):
    path = Path(path)
    ext = path.suffix.casefold()
    mime = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(ext, "application/octet-stream")
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def limpar_analise(texto, max_chars=900):
    texto = html.unescape(re.sub(r"<[^>]+>", "", str(texto or ""))).strip()
    if len(texto) > int(max_chars):
        texto = texto[:int(max_chars)].rstrip() + "..."
    return texto


def toggle_eureka():
    """EUREKA ocupa o lugar da OLA sem criar nova página."""
    dismiss_help()
    st.session_state.moby_eureka_open = not bool(st.session_state.get("moby_eureka_open", False))
    st.session_state.moby_eureka_index = 0
    st.session_state.moby_eureka_pick = ""
    st.session_state.moby_eureka_seed_ref = ""
    st.session_state.moby_eureka_tema_motor = ""
    invalidate_real_poem()
    invalidate_ola()


def _moby_eureka_seed_changed():
    dismiss_help()
    st.session_state.moby_eureka_index = 0
    st.session_state.moby_eureka_pick = ""
    st.session_state.moby_eureka_mark_term = ""
    st.session_state.moby_eureka_seed_ref = ""
    st.session_state.moby_eureka_tema_motor = ""
    invalidate_real_poem()
    invalidate_real_image()
    invalidate_ola()


def _moby_eureka_theme_from_source(fonte):
    """Extrai do GPS o nome EXATO do tema usado pelo motor.

    build_lexico grava:
        TEMA_EXATO + "_" + linha(2) + ideia(2) + posição(3)

    Portanto o tema é tudo antes do ÚLTIMO "_".
    Isso preserva nomes como nós_nos_nós e, mais importante,
    mantém exatamente a mesma grafia usada pelo motor.
    """
    fonte = str(fonte or "").strip()
    tema, sep, coords = fonte.rpartition("_")
    if not sep or not tema or re.fullmatch(r"\d{7}", coords) is None:
        return ""
    return tema


def _moby_eureka_ypo_results(seed):
    """Encontra a seed no verbete do léxico e usa tema+GPS só como endereço."""
    seed = str(seed or "").strip()
    if len(seed) < 3:
        return []

    path = Path("./base/lexico_pt.txt")
    if not path.is_file():
        return []

    out = []
    alvo = seed.casefold()
    try:
        linhas = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []

    for raw in linhas:
        this_line = str(raw).strip()
        if not this_line:
            continue

        verbete, sep, fonte = this_line.partition(" : ")
        if not sep:
            continue

        # Engenharia original da EUREKA:
        # seed -> verbete encontrado -> tema + GPS exato.
        # O nome do tema é somente a chave do .ypo; nunca vira seed.
        ocorrencias = len(
            list(
                re.finditer(
                    rf"(?={re.escape(alvo)})",
                    verbete.casefold(),
                )
            )
        )
        if ocorrencias == 0:
            continue

        fonte = fonte.strip()
        tema = _moby_eureka_theme_from_source(fonte)
        if not tema:
            continue

        item = {
            "label": f"{verbete} ➪ {fonte}",
            "tema": tema,
            "fonte": fonte,
            "seed": seed,
            # O motor recebe a seed procurada à esquerda e o GPS exato à direita.
            "seed_ref": f"{seed} ➪ {fonte}",
            "mark_term": seed,
        }
        for _ in range(ocorrencias):
            out.append(dict(item))

    out.sort(key=lambda item: item["label"].casefold())
    return out

def _moby_eureka_off_results(seed):
    """Busca a seed diretamente em todos os .pip do Off-Machina."""
    seed = str(seed or "").strip()
    if len(seed) < 3 or not OFF_DIR.is_dir():
        return []

    alvo = seed.casefold()
    out = []
    for path in off_books():
        paginas = off_pages(path)
        for idx, (titulo, corpo) in enumerate(paginas):
            texto = f"{titulo}\n{corpo}"
            if alvo not in texto.casefold():
                continue

            verbete = seed
            for token in re.findall(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", texto, flags=re.UNICODE):
                if alvo in token.casefold():
                    verbete = token
                    break

            out.append(
                {
                    "label": f"{verbete} ➪ {path.stem} / {titulo}",
                    "book": path.stem,
                    "page_index": idx,
                    "titulo": titulo,
                    "mark_term": seed,
                }
            )

    out.sort(key=lambda item: item["label"].casefold())
    return out


def moby_eureka_results():
    seed = str(st.session_state.get("moby_eureka_seed", "")).strip()
    if st.session_state.get("moby_mode") == "Off-Machina":
        return _moby_eureka_off_results(seed)
    return _moby_eureka_ypo_results(seed)


def _moby_book_for_theme(tema):
    """Descobre um livro Moby que contenha o tema encontrado pelo EUREKA."""
    alvo = nome_normalizado(tema)
    for book in MOBY_BOOKS:
        temas = temas_do_livro(DNA_ROWS, book)
        for item in temas:
            if nome_normalizado(item) == alvo:
                return book
    return None


def apply_eureka_occurrence(index=None):
    """Faz as listas existentes apontarem para a ocorrência escolhida."""
    resultados = moby_eureka_results()
    if not resultados:
        st.session_state.moby_eureka_index = 0
        return

    if index is None:
        try:
            index = int(st.session_state.get("moby_eureka_pick", st.session_state.get("moby_eureka_index", 0)))
        except Exception:
            index = 0

    index = max(0, min(int(index), len(resultados) - 1))
    st.session_state.moby_eureka_index = index
    item = resultados[index]
    st.session_state.moby_eureka_mark_term = str(
        item.get("mark_term", st.session_state.get("moby_eureka_seed", ""))
    ).strip()

    if st.session_state.get("moby_mode") == "Off-Machina":
        livros = off_books()
        nomes = [p.stem for p in livros]
        book = str(item.get("book", ""))
        if book in nomes:
            st.session_state.moby_off_book_index = nomes.index(book)
            st.session_state["moby_off_book_pick"] = book
            paginas = current_off_pages()
            if paginas:
                take = max(0, min(int(item.get("page_index", 0)), len(paginas) - 1))
                st.session_state.moby_off_take = take
                st.session_state["moby_off_page_pick"] = paginas[take][0]
        invalidate_real_image()
        invalidate_ola()
        return

    tema = str(item.get("tema", "")).strip()
    book = _moby_book_for_theme(tema)
    if book:
        st.session_state.moby_book = book
        st.session_state["moby_book_pick"] = book

    temas = current_themes()
    for i, nome in enumerate(temas):
        if nome_normalizado(nome) == nome_normalizado(tema):
            st.session_state.moby_theme_index = i
            st.session_state["moby_theme_pick"] = nome
            break

    # GPS EUREKA: palavra + endereço exato LLIIPPP.
    # A geração fica centralizada em update_real_poem(); assim nenhum rerun
    # pode regenerar o tema sem o endereço e "perder o GPS".
    seed_ref = str(item.get("seed_ref", "")).strip()
    st.session_state.moby_eureka_seed_ref = seed_ref
    st.session_state.moby_eureka_tema_motor = str(item.get("tema", "")).strip()
    invalidate_real_poem()

    invalidate_real_image()
    invalidate_ola()


def eureka_occurrence_picked():
    apply_eureka_occurrence()


def eureka_previous():
    resultados = moby_eureka_results()
    if not resultados:
        return
    atual = int(st.session_state.get("moby_eureka_index", 0))
    novo = (atual - 1) % len(resultados)
    st.session_state.moby_eureka_index = novo
    st.session_state.moby_eureka_pick = novo
    apply_eureka_occurrence(novo)


def eureka_next():
    resultados = moby_eureka_results()
    if not resultados:
        return
    atual = int(st.session_state.get("moby_eureka_index", 0))
    novo = (atual + 1) % len(resultados)
    st.session_state.moby_eureka_index = novo
    st.session_state.moby_eureka_pick = novo
    apply_eureka_occurrence(novo)


def eureka_random():
    resultados = moby_eureka_results()
    if not resultados:
        return
    atual = int(st.session_state.get("moby_eureka_index", 0))
    candidatos = [i for i in range(len(resultados)) if i != atual]
    novo = random.choice(candidatos) if candidatos else atual
    st.session_state.moby_eureka_index = novo
    st.session_state.moby_eureka_pick = novo
    apply_eureka_occurrence(novo)


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
    st.session_state.moby_off_plus_help = False
    if st.session_state.get("moby_mode") == "Off-Machina":
        st.session_state.moby_mode = "Machina"
    else:
        st.session_state.moby_mode = "Off-Machina"
        paginas = current_off_pages()
        st.session_state.moby_off_take = random.randrange(len(paginas)) if paginas else 0
    invalidate_real_image()
    invalidate_ola()


def prepare_portrait():
    """Retrato usa diretamente a imagem #1 da leitura atual."""
    dismiss_help()
    chosen = str(st.session_state.get("moby_image_path", "")).strip()
    if not chosen or not Path(chosen).is_file():
        return
    st.session_state.moby_portrait_image = chosen
    title = st.session_state.get("moby_current_title", "retrato")
    poem_html = st.session_state.get("moby_current_poem_html", "")
    png = create_moby_portrait_png(poem_html, chosen, title)
    if png:
        st.session_state.moby_portrait_png = png
        st.session_state.moby_footer_view = "portrait"
        st.session_state.moby_image_visible = False
        safe = re.sub(r"[^A-Za-z0-9_-]+", "_", str(title or "retrato")).strip("_") or "retrato"
        st.session_state.moby_portrait_name = safe


def update_real_poem():
    """Gera e congela a leitura atual; no EUREKA o GPS LLIIPPP é obrigatório."""
    tema = current_theme()
    tema_motor = tema
    reading_n = int(st.session_state.get("moby_reading_n", 1))

    eureka_ativa = (
        st.session_state.get("moby_mode") != "Off-Machina"
        and bool(st.session_state.get("moby_eureka_open", False))
    )

    seed_ref = ""
    if eureka_ativa:
        seed_ref = str(st.session_state.get("moby_eureka_seed_ref", "")).strip()
        tema_motor = str(st.session_state.get("moby_eureka_tema_motor", "")).strip() or tema

        # Defesa contra rerun/estado incompleto: reconstrói o GPS diretamente
        # da ocorrência selecionada, nunca apenas da palavra ou do tema.
        if not seed_ref:
            resultados = moby_eureka_results()
            if resultados:
                indice = int(st.session_state.get("moby_eureka_index", 0))
                indice = max(0, min(indice, len(resultados) - 1))
                item = resultados[indice]
                seed_ref = str(item.get("seed_ref", "")).strip()
                tema_motor = str(item.get("tema", "")).strip() or tema
                st.session_state.moby_eureka_seed_ref = seed_ref
                st.session_state.moby_eureka_tema_motor = tema_motor
                st.session_state.moby_eureka_mark_term = str(
                    item.get("mark_term", st.session_state.get("moby_eureka_seed", ""))
                ).strip()

    if eureka_ativa and seed_ref:
        assinatura = ("EUREKA", tema_motor, seed_ref, reading_n)
    else:
        assinatura = (tema, reading_n)

    if st.session_state.get("moby_poem_signature") == assinatura:
        return

    try:
        # GPS_NAO_FALHA:
        # EUREKA -> "palavra ➪ tema_LLIIPPP"
        # leitura comum -> seed vazia
        script = gera_poema(
            tema_motor if eureka_ativa else tema,
            seed_ref if eureka_ativa else "",
        )
    except Exception as exc:
        st.session_state.moby_poem_html = html.escape(
            f"Moby não conseguiu gerar esta leitura: {exc}"
        )
        st.session_state.moby_poem_signature = assinatura
        return

    linhas = []
    for line in script:
        if line == "\n":
            linhas.append("")
        else:
            texto_linha = str(line).rstrip("\r\n")
            texto_linha = texto_linha.replace("&emsp;", "\u2003")

            link_autoral_nos = (
                '<a href="https://thispersondoesnotexist.com/" target="_blank">'
                '... quem será essa pessoa que não existe?</a>'
            )

            if texto_linha.strip() == link_autoral_nos:
                linhas.append(texto_linha)
            else:
                # Preserva somente a marca produzida pelo GPS do motor.
                # Todo o restante continua escapado como antes.
                partes = re.split(r"(</?mark>)", texto_linha, flags=re.IGNORECASE)
                seguro = []
                for parte in partes:
                    if re.fullmatch(r"</?mark>", parte, flags=re.IGNORECASE):
                        seguro.append(parte.lower())
                    else:
                        seguro.append(html.escape(parte))
                linhas.append("".join(seguro))

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
            st.session_state.moby_translation_signature = None
            st.session_state.moby_translation_html = ""
            st.session_state.moby_sound_signature = None
            st.session_state.moby_sound_audio = b""
            return


def sidebar_font_changed():
    dismiss_help()
    escolha = st.session_state.get("moby_font_pick", "")
    for label, family in FONTES_MACHINA:
        if escolha == label:
            st.session_state.moby_font_family = family
            return


def sidebar_style_changed():
    dismiss_help()
    estilo = str(st.session_state.get("moby_style_pick", "normal")).strip().casefold()
    st.session_state.moby_font_style = estilo if estilo in ESTILOS_MACHINA else "normal"


def sidebar_size_changed():
    dismiss_help()
    st.session_state.moby_font_size = int(
        st.session_state.get("moby_size_pick", 18)
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
    paginas = current_off_pages()
    st.session_state.moby_off_take = random.randrange(len(paginas)) if paginas else 0
    invalidate_real_image()
    st.session_state.moby_sidebar_open = False


def select_ola_sidebar():
    dismiss_help()
    st.session_state.moby_mode = "OLA"


def _matrix_image_path_for_theme(nome_tema):
    """Localiza a Matrix do tema atual em ./images/matrix."""
    tema = str(nome_tema or "").strip()
    if not tema:
        return None

    matrix_dir = Path("./images/matrix")
    if not matrix_dir.is_dir():
        return None

    def chave(valor):
        normal = unicodedata.normalize("NFKD", str(valor or ""))
        sem_acentos = "".join(c for c in normal if not unicodedata.combining(c))
        return re.sub(r"[^a-z0-9]+", "", sem_acentos.casefold())

    alvo = chave(tema)
    for path in sorted(matrix_dir.iterdir()):
        if path.is_file() and path.suffix.casefold() in {".jpg", ".jpeg", ".png", ".webp"}:
            if chave(path.stem) == alvo:
                return path
    return None



def _fmt_help_numero(valor):
    texto = str(valor or "").strip()
    if not texto:
        return ""
    try:
        return f"{int(texto):,}".replace(",", ".")
    except (TypeError, ValueError):
        return texto



def _numero_por_extenso_pt(valor):
    """Leitura humana de número inteiro em português."""
    texto = str(valor or "").strip()
    digitos = re.sub(r"[^0-9]", "", texto)
    if not digitos:
        return ""
    numero = int(digitos)
    if numero == 0:
        return "zero"

    unidades = ["", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove"]
    especiais = {10:"dez",11:"onze",12:"doze",13:"treze",14:"quatorze",15:"quinze",16:"dezesseis",17:"dezessete",18:"dezoito",19:"dezenove"}
    dezenas = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"]
    centenas = ["", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos", "setecentos", "oitocentos", "novecentos"]

    def bloco_999(n):
        if n == 0: return ""
        if n == 100: return "cem"
        partes = []
        c, r = divmod(n, 100)
        if c: partes.append(centenas[c])
        if r:
            if r < 10: partes.append(unidades[r])
            elif r < 20: partes.append(especiais[r])
            else:
                d, u = divmod(r, 10)
                trecho = dezenas[d] + ((" e " + unidades[u]) if u else "")
                partes.append(trecho)
        return " e ".join(partes)

    escalas = [
        ("", ""), ("mil", "mil"), ("milhão", "milhões"), ("bilhão", "bilhões"),
        ("trilhão", "trilhões"), ("quadrilhão", "quadrilhões"), ("quintilhão", "quintilhões"),
        ("sextilhão", "sextilhões"), ("septilhão", "septilhões"), ("octilhão", "octilhões"),
        ("nonilhão", "nonilhões"), ("decilhão", "decilhões"), ("undecilhão", "undecilhões"),
        ("duodecilhão", "duodecilhões"), ("tredecilhão", "tredecilhões"),
        ("quatuordecilhão", "quatuordecilhões"), ("quindecilhão", "quindecilhões"),
        ("sexdecilhão", "sexdecilhões"), ("septendecilhão", "septendecilhões"),
        ("octodecilhão", "octodecilhões"), ("novendecilhão", "novendecilhões"),
        ("vigintilhão", "vigintilhões"),
    ]
    grupos=[]; n=numero
    while n:
        grupos.append(n%1000); n//=1000
    if len(grupos) > len(escalas):
        return f"{numero} (10 elevado a {len(str(numero))-1})"
    partes=[]
    for i in range(len(grupos)-1,-1,-1):
        g=grupos[i]
        if not g: continue
        if i==0:
            partes.append(bloco_999(g)); continue
        singular, plural=escalas[i]
        if i==1:
            partes.append("mil" if g==1 else f"{bloco_999(g)} mil")
        else:
            partes.append(f"{'um' if g==1 else bloco_999(g)} {singular if g==1 else plural}")
    if len(partes)==1: return partes[0]
    return ", ".join(partes[:-1]) + " e " + partes[-1]


def _variacoes_humano(valor):
    texto = str(valor or "").strip()
    match = re.search(r"[0-9][0-9.,]*", texto)
    return _numero_por_extenso_pt(match.group(0)) if match else ""


def _build_seal_from_ypo(nome_tema):
    path = Path("./data") / f"{str(nome_tema or '').strip()}.ypo"
    selo = ""
    try:
        for raw in path.read_text(encoding="utf-8-sig").splitlines():
            line = raw.strip()
            if line.casefold().startswith("build_by lay_2_ypo"):
                selo = line
    except (OSError, UnicodeError):
        pass
    return selo


def _help_ficha_linhas(nome_tema):
    row = registro_do_tema(DNA_ROWS, nome_tema)
    if not row:
        return []
    pares = [
        ("Título", row.get("tema", "") or nome_tema),
        ("Livro", row.get("livro", "")),
        ("Banco temático", row.get("banco_tematico", "")),
        ("Versos", row.get("versos", "")),
        ("Verbetes no Texto", row.get("verbetes_no_texto", "")),
        ("Verbetes do Tema", row.get("verbetes_do_tema", "")),
        ("Total de ítimos", row.get("total_de_itimos", "")),
        ("Qtd. de Variações", row.get("qtd_de_variacoes", "")),
    ]
    linhas = []
    for rotulo, valor in pares:
        valor_bruto = valor
        valor = _fmt_help_numero(valor) if rotulo not in {"Título", "Livro", "Banco temático"} else str(valor or "").strip()
        if valor:
            linhas.append(f"{rotulo}: {valor}")
            if rotulo == "Qtd. de Variações":
                humano = _variacoes_humano(valor_bruto)
                if humano:
                    linhas.append(humano)
    selo = _build_seal_from_ypo(nome_tema)
    if selo:
        linhas.append(selo)
    return linhas

@st.dialog("Retrato", width="large")
def ampliar_retrato_moby(png):
    st.image(png, width="stretch")


def toggle_help():
    st.session_state.moby_help_open = not st.session_state.moby_help_open


def dismiss_help():
    st.session_state.moby_help_open = False


def toggle_image():
    """Imagem recolhe/abre a ilustração; o espaço liberado volta ao palco."""
    dismiss_help()
    if st.session_state.get("moby_footer_view", "images") == "images":
        st.session_state.moby_footer_view = "none"
        st.session_state.moby_image_visible = False
    else:
        st.session_state.moby_footer_view = "images"
        st.session_state.moby_image_visible = True


def new_reading():
    dismiss_help()
    invalidate_ola()
    if st.session_state.get("moby_mode") == "Off-Machina":
        st.session_state.moby_off_plus_help = True
        return
    st.session_state.moby_off_plus_help = False
    st.session_state.moby_reading_n += 1
    if st.session_state.get("moby_eureka_open", False) and moby_eureka_results():
        apply_eureka_occurrence(st.session_state.get("moby_eureka_index", 0))
        return
    invalidate_real_poem()
    invalidate_real_image()


def previous_theme():
    dismiss_help()
    invalidate_ola()
    st.session_state.moby_off_plus_help = False
    if st.session_state.get("moby_eureka_open", False):
        eureka_previous()
        return
    if st.session_state.get("moby_mode") == "Off-Machina":
        paginas = current_off_pages()
        if paginas:
            st.session_state.moby_off_take = (st.session_state.moby_off_take - 1) % len(paginas)
            invalidate_real_image()
        return
    temas = current_themes()
    if temas:
        st.session_state.moby_theme_index = (st.session_state.moby_theme_index - 1) % len(temas)
        st.session_state["moby_theme_pick"] = temas[st.session_state.moby_theme_index]
        st.session_state.moby_reading_n = 1
        invalidate_real_poem()
        invalidate_real_image()


def next_theme():
    dismiss_help()
    invalidate_ola()
    st.session_state.moby_off_plus_help = False
    if st.session_state.get("moby_eureka_open", False):
        eureka_next()
        return
    if st.session_state.get("moby_mode") == "Off-Machina":
        paginas = current_off_pages()
        if paginas:
            st.session_state.moby_off_take = (st.session_state.moby_off_take + 1) % len(paginas)
            invalidate_real_image()
        return
    temas = current_themes()
    if temas:
        st.session_state.moby_theme_index = (st.session_state.moby_theme_index + 1) % len(temas)
        st.session_state["moby_theme_pick"] = temas[st.session_state.moby_theme_index]
        st.session_state.moby_reading_n = 1
        invalidate_real_poem()
        invalidate_real_image()


def random_theme():
    dismiss_help()
    invalidate_ola()
    st.session_state.moby_off_plus_help = False
    if st.session_state.get("moby_eureka_open", False):
        eureka_random()
        return
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
    st.session_state["moby_theme_pick"] = temas[st.session_state.moby_theme_index]
    st.session_state.moby_reading_n = 1
    invalidate_real_poem()
    invalidate_real_image()


def book_changed():
    escolha = str(st.session_state.get("moby_book_pick", st.session_state.get("moby_book", MOBY_DEFAULT_BOOK)))
    if escolha in MOBY_BOOKS:
        st.session_state.moby_book = escolha
    st.session_state.moby_theme_index = 0
    temas = current_themes()
    if temas:
        st.session_state["moby_theme_pick"] = temas[0]
    else:
        st.session_state.pop("moby_theme_pick", None)
    st.session_state.moby_reading_n = 1
    invalidate_real_poem()
    invalidate_real_image()
    invalidate_ola()


def theme_picked():
    temas = current_themes()
    escolha = st.session_state.get("moby_theme_pick", "")
    if escolha in temas:
        st.session_state.moby_theme_index = temas.index(escolha)
        st.session_state.moby_reading_n = 1
        invalidate_real_poem()
        invalidate_real_image()


apply_pending_link()
normalize_theme_index()

# Na primeira abertura, a Machina entra por um tema ao acaso.
if not st.session_state.get("moby_started", False):
    temas_iniciais = current_themes()
    if temas_iniciais:
        st.session_state.moby_theme_index = random.randrange(len(temas_iniciais))
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
    .stApp {
        background: #ececec;
    }

    mark {
        background-color: powderblue;
        color: black;
    }

    /* Sidebar: o botão FECHAR precisa aparecer visualmente. */
    .st-key-moby_close_sidebar button {
        background: #f3b6c8 !important;
        border-color: #d98da5 !important;
        color: #111 !important;
    }
    .st-key-moby_close_sidebar button:hover {
        background: #eca5ba !important;
        border-color: #cf7895 !important;
        color: #111 !important;
    }

    /* st.markdown(<style>) não deve ocupar uma linha invisível no layout. */
    div[data-testid="stElementContainer"]:has(style) {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
        height: 0 !important;
        min-height: 0 !important;
    }

    .block-container,
    div[data-testid="stMainBlockContainer"] {
        max-width: 430px !important;
        margin: 0 auto !important;
        padding: 12px !important;
        background: white;
        border: 1px solid rgba(0,0,0,.18);
        border-radius: 28px;
        box-shadow: 0 10px 35px rgba(0,0,0,.10);
        height: auto !important;
        min-height: 0 !important;
        max-height: none !important;
        overflow: visible !important;
        box-sizing: border-box !important;
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
        margin: 7px 0 14px 0;
    }

    .moby-images-bottom-space {
        height: 18px;
        min-height: 18px;
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

    .moby-poem-title {
        text-align: center;
        font-weight: 700;
        text-decoration: underline;
        text-underline-offset: .18em;
        margin: 2px 0 8px 0;
    }

    .ypoema {
        line-height: 1.60;
        padding: 0 8px 0 3px;
        margin: 4px 0 8px 0;
        overflow-wrap: anywhere;
    }

    .st-key-moby_stage_scroll {
        height: 355px;
        min-height: 355px;
        max-height: 355px;
        overflow-y: auto;
        overflow-x: hidden;
        overscroll-behavior: contain;
        padding: 2px 5px 8px 1px;
        margin-top: 2px;
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

    .st-key-moby_about_text {
        max-height: 465px;
        overflow-y: auto;
        overflow-x: hidden;
        overscroll-behavior: contain;
        scrollbar-gutter: stable;
        padding: 0 14px 26px 14px;
        margin: 0 2px 10px 2px;
    }

    .st-key-moby_footer_zone {
        height: 182px;
        min-height: 182px;
        max-height: 182px;
        overflow: hidden;
        margin-top: 2px;
        padding: 0;
    }

    .st-key-moby_footer_controls {
        margin: 0;
        padding: 0;
    }

    .st-key-moby_footer_controls div[data-testid="stHorizontalBlock"] {
        gap: 2px !important;
    }

    .st-key-moby_footer_controls button {
        min-height: 34px !important;
        height: 34px !important;
        margin-bottom: 0 !important;
    }

    .st-key-moby_images_stage {
        height: 146px;
        min-height: 146px;
        max-height: 146px;
        overflow: hidden;
        margin: 2px 0 0 0;
        padding: 0;
    }

    .st-key-moby_portrait_stage {
        width: 100%;
        max-width: 100%;
        height: 158px;
        min-height: 158px;
        max-height: 158px;
        overflow: hidden;
        margin: 2px 0 0 0;
        padding: 0 0 7px 0;
        box-sizing: border-box;
    }

    .st-key-moby_portrait_stage div[data-testid="stHorizontalBlock"],
    .st-key-moby_portrait_stage div[data-testid="stColumn"],
    .st-key-moby_portrait_stage div[data-testid="stImage"],
    .st-key-moby_portrait_stage figure {
        min-width: 0 !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    .st-key-moby_images_stage .moby-footer-images-flex {
        width: 100%;
        height: 142px;
        display: grid;
        grid-template-columns: 1fr 2fr 1fr 2fr 1fr;
        align-items: center;
        gap: 0;
        overflow: hidden;
    }

    .st-key-moby_images_stage .moby-footer-image-cell {
        min-width: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }

    .st-key-moby_images_stage .moby-footer-image {
        display: block;
        max-height: 142px;
        max-width: 100%;
        width: auto;
        height: auto;
        object-fit: contain;
        border-radius: 8px;
        margin: 0 auto;
    }

    .st-key-moby_portrait_stage img {
        display: block !important;
        max-height: 150px !important;
        width: auto !important;
        max-width: 100% !important;
        height: auto !important;
        margin: 0 auto !important;
        object-fit: contain !important;
        box-sizing: border-box !important;
    }

    .st-key-moby_portrait_save button {
        min-height: 28px !important;
        height: 28px !important;
        padding-top: .05rem !important;
        padding-bottom: .05rem !important;
    }

    .moby-social-stage {
        margin-top: .15rem;
        padding: .25rem .05rem .4rem .05rem;
    }

    .moby-social-title {
        text-align: center;
        font-weight: 700;
        font-size: 1.05rem;
        margin: .35rem 0 .08rem 0;
        letter-spacing: .01em;
    }

    .moby-social-subtitle {
        text-align: center;
        font-size: .76rem;
        opacity: .58;
        margin-bottom: .75rem;
    }

    .moby-social-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: .55rem;
    }

    .moby-social-card {
        min-height: 68px;
        border: 1px solid rgba(0,0,0,.12);
        border-radius: 13px;
        background: #fff;
        text-decoration: none !important;
        color: #202124 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        gap: .34rem;
        padding: .58rem .42rem;
        box-shadow: 0 3px 10px rgba(0,0,0,.06);
        transition: transform .13s ease, box-shadow .13s ease, border-color .13s ease;
    }

    .moby-social-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 17px rgba(0,0,0,.11);
        border-color: rgba(0,0,0,.25);
    }

    .moby-social-icons {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: .30rem;
        min-height: 24px;
    }

    .moby-social-icons img {
        width: 24px;
        height: 24px;
        object-fit: contain;
        display: block;
    }

    .moby-social-label {
        font-size: .82rem;
        font-weight: 600;
        line-height: 1.1;
        text-align: center;
    }


    .moby-sound-slot {
        height: 24px;
        min-height: 24px;
        display:flex;
        align-items:center;
        justify-content:center;
        margin: 3px 0 4px 0;
        font-size:.78rem;
        opacity:.88;
        overflow:hidden;
    }
    .moby-sound-slot audio {
        width:100%;
        height:24px;
    }

    .end-rule {
        border-top:1px solid rgba(0,0,0,.12);
        margin: 15px 0 8px 0;
    }


    /* ALADIN — lâmpada revela; 34x34; callback Streamlit preservado. */
    .st-key-moby_eureka_focus button,
    .st-key-moby_eureka_focus_off button,
    .st-key-moby_eureka_focus_close button {
        background-image: url("data:image/png;base64,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") !important;
        background-repeat: no-repeat !important;
        background-position: center center !important;
        background-size: 34px 34px !important;
        color: transparent !important;
        text-shadow: none !important;
        overflow: hidden !important;
    }
    .st-key-moby_eureka_focus button *,
    .st-key-moby_eureka_focus_off button *,
    .st-key-moby_eureka_focus_close button * {
        color: transparent !important;
        fill: transparent !important;
    }

    /* CHAVE DE OURO — sinaliza o ambiente Off-Machina no swap principal. */
    .st-key-moby_mode_swap_off button {
        background-image: url("data:image/png;base64,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") !important;
        background-repeat: no-repeat !important;
        background-position: center center !important;
        background-size: 34px 34px !important;
        color: transparent !important;
        text-shadow: none !important;
        overflow: hidden !important;
    }
    .st-key-moby_mode_swap_off button * {
        color: transparent !important;
        fill: transparent !important;
    }

    div[data-testid="stButton"] button {
        min-height: 38px;
        border-radius: 9px;
        padding-left: .35rem !important;
        padding-right: .35rem !important;
        font-size: .88rem !important;
    }



    /* Copiar: mesma altura visual de Imagem/Retrato. */
    .st-key-moby_footer_controls div[data-testid="stPopover"] > button,
    .st-key-moby_footer_controls div[data-testid="stPopover"] button {
        width: 100% !important;
        min-height: 34px !important;
        height: 34px !important;
        max-height: 34px !important;
        border-radius: 9px !important;
        font-size: .88rem !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin: 0 !important;
    }
    /* Fullscreen nativo fora do Moby: Retrato usa apenas Ampliar/Salvar. */
    button[title*="fullscreen" i],
    button[aria-label*="fullscreen" i],
    button[data-testid="stImageFullscreenButton"],
    [data-testid="stImageFullscreenButton"],
    [data-testid*="Fullscreen"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        min-width: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        border: 0 !important;
        overflow: hidden !important;
        pointer-events: none !important;
    }


    #MainMenu, footer, header {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* Moby em celular vertical: as barras continuam barras, não pilhas. */
    @media (max-width: 600px) {
        .block-container,
        div[data-testid="stMainBlockContainer"] {
            width: calc(100vw - 24px) !important;
            max-width: 430px !important;
            margin: 0 auto !important;
            padding: 12px !important;
            height: auto !important;
            min-height: 0 !important;
            max-height: none !important;
            overflow: visible !important;
            border-radius: 20px;
            box-sizing: border-box !important;
        }

        div[data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
            gap: .28rem !important;
        }

        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            min-width: 0 !important;
            width: auto !important;
        }

        div[data-testid="stHorizontalBlock"] button {
            min-width: 0 !important;
            padding-left: .18rem !important;
            padding-right: .18rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# CONFIG — TERCEIRA VIA
# Decide o território antes de qualquer componente do PALCO/CABEÇALHO nascer.
# =============================================================================
if st.session_state.moby_sidebar_open:
    # Idiomas passam a ocupar o topo da sidebar.
    idioma_labels = [f"{nome} — {pais}" for nome, pais, _ in IDIOMAS_MACHINA]
    idioma_atual = next(
        (f"{nome} — {pais}" for nome, pais, code in IDIOMAS_MACHINA if code == st.session_state.moby_lang),
        idioma_labels[0],
    )
    if str(st.session_state.get("moby_lang_pick", "")) not in idioma_labels:
        st.session_state["moby_lang_pick"] = idioma_atual
    st.selectbox("idiomas disponíveis...", idioma_labels, key="moby_lang_pick", on_change=sidebar_language_changed)

    fonte_labels = [label for label, _ in FONTES_MACHINA]
    fonte_lookup = {label: family for label, family in FONTES_MACHINA}
    fonte_atual = next(
        (label for label, family in FONTES_MACHINA if family == st.session_state.moby_font_family),
        fonte_labels[0],
    )
    estilo_atual = estilo_palco_atual()
    corpo_atual = int(st.session_state.get("moby_font_size", 20))
    if corpo_atual not in CORPOS_MOBY:
        corpo_atual = 20

    # Efeito: um único conjunto de controles — fonte | estilo | corpo.
    fonte_col, estilo_col, corpo_col = st.columns([1.75, 1.20, 0.72], gap="small")
    with fonte_col:
        if str(st.session_state.get("moby_font_pick", "")) not in fonte_labels:
            st.session_state["moby_font_pick"] = fonte_atual
        fonte_escolhida = st.selectbox(
            "fonte", fonte_labels,
            key="moby_font_pick", on_change=sidebar_font_changed,
        )
    with estilo_col:
        if str(st.session_state.get("moby_style_pick", "")) not in ESTILOS_MACHINA:
            st.session_state["moby_style_pick"] = estilo_atual
        estilo_escolhido = st.selectbox(
            "estilo", ESTILOS_MACHINA,
            key="moby_style_pick", on_change=sidebar_style_changed,
        )
    with corpo_col:
        if st.session_state.get("moby_size_pick") not in CORPOS_MOBY:
            st.session_state["moby_size_pick"] = corpo_atual
        corpo_escolhido = st.selectbox(
            "corpo", CORPOS_MOBY,
            key="moby_size_pick", on_change=sidebar_size_changed,
        )
    st.session_state.moby_font_family = fonte_lookup.get(fonte_escolhida, st.session_state.moby_font_family)
    st.session_state.moby_font_style = estilo_escolhido if estilo_escolhido in ESTILOS_MACHINA else "normal"
    st.session_state.moby_font_size = int(corpo_escolhido)

    about_col, close_col, links_col = st.columns([1.55, 1.25, 1.55], gap="small")
    with about_col:
        st.button("about", key="moby_sidebar_about", width="stretch", on_click=sidebar_show_about)
    with close_col:
        st.button("fechar", key="moby_close_sidebar", width="stretch", on_click=sidebar_return_to_stage)
    with links_col:
        st.button("links", key="moby_sidebar_links", width="stretch", on_click=sidebar_show_links)

    if st.session_state.get("moby_sidebar_panel", "about") == "links":
        render_social_links()
    else:
        current_about = str(st.session_state.get("moby_about_pick", "machina"))
        if current_about not in ABOUTS_LIST:
            current_about = "machina"
        if str(st.session_state.get("moby_about_pick", "")) not in ABOUTS_LIST:
            st.session_state["moby_about_pick"] = current_about
        about_choice = st.selectbox(
            "sobre",
            ABOUTS_LIST,
            key="moby_about_pick",
        )
        about_family = str(st.session_state.get("moby_font_family", "Comic Relief"))
        about_font_css = fonte_palco_css(about_family)
        about_weight, about_style_css = estilo_palco_css(about_family)
        about_size = int(st.session_state.get("moby_font_size", 20))
        st.markdown(
            f"""
            <style>
            .st-key-moby_about_text,
            .st-key-moby_about_text * {{
                font-family: {about_font_css} !important;
                font-style: {about_style_css} !important;
            }}
            .st-key-moby_about_text p,
            .st-key-moby_about_text li {{
                font-size: {about_size}px !important;
                font-weight: {about_weight};
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        with st.container(key="moby_about_text"):
            st.markdown(load_about_text(about_choice))


    st.stop()


# =============================================================================
# CABEÇALHO — SWAP + LINKS + SIDEBAR
# =============================================================================
modo_off = st.session_state.get("moby_mode") == "Off-Machina"
modo_label = "❓"
if not modo_off:
    st.markdown(
        """
        <style>
        .st-key-moby_mode_swap button {
            color: #c40000 !important;
            font-weight: 800 !important;
            font-size: 1.18rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
head_mode, head_links, head_side = st.columns([1.35, 4.3, 1.35], gap="small")

with head_mode:
    modo_key = "moby_mode_swap_off" if modo_off else "moby_mode_swap"
    st.button(modo_label, key=modo_key, width="stretch", on_click=swap_machina_off)

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




# =============================================================================
# LIVRO + EUREKA + TEMA / OFF-MACHINA
# EUREKA usa o mesmo território das listas existentes.
# =============================================================================
eureka_aberta = bool(st.session_state.get("moby_eureka_open", False))

if eureka_aberta:
    resultados_eureka = moby_eureka_results()
    col_book, col_eureka, col_theme = st.columns([3, 1.25, 3], gap="small")

    with col_book:
        st.text_input(
            "buscar por...",
            key="moby_eureka_seed",
            on_change=_moby_eureka_seed_changed,
            placeholder="buscar por...",
        )

    with col_eureka:
        st.markdown("<div style='height:1.45rem'></div>", unsafe_allow_html=True)
        st.button("EUREKA", key="moby_eureka_focus_close", width="stretch", on_click=toggle_eureka)

    with col_theme:
        seed_atual = str(st.session_state.get("moby_eureka_seed", "")).strip()
        if len(seed_atual) < 3:
            st.selectbox(
                "ocorrências",
                ["digite pelo menos 3 letras..."],
                key="moby_eureka_wait",
                disabled=True,
            )
        elif not resultados_eureka:
            st.selectbox(
                "ocorrências",
                ["nenhuma ocorrência"],
                key="moby_eureka_none",
                disabled=True,
            )
        else:
            indice = int(st.session_state.get("moby_eureka_index", 0))
            indice = max(0, min(indice, len(resultados_eureka) - 1))
            options = list(range(len(resultados_eureka)))

            # A lista visual acompanha sempre a mesma posição dos nav_buttons.
            if st.session_state.get("moby_eureka_pick") != indice:
                st.session_state.moby_eureka_pick = indice

            st.selectbox(
                f"tema: {indice + 1}/{len(resultados_eureka)}",
                options,
                format_func=lambda i: resultados_eureka[i]["label"],
                key="moby_eureka_pick",
                on_change=eureka_occurrence_picked,
            )

    # A ocorrência só precisa ser aplicada quando o GPS ainda não foi firmado.
    # Reaplicá-la em todo rerun invalida a imagem/retrato recém-gerado.
    if resultados_eureka and not str(st.session_state.get("moby_eureka_seed_ref", "")).strip():
        apply_eureka_occurrence(st.session_state.get("moby_eureka_index", 0))

elif st.session_state.get("moby_mode") == "Off-Machina":
    livros_off = off_books()
    if not livros_off:
        st.error("Off-Machina não encontrou arquivos .Pip em ./off_machina.")
        st.stop()

    nomes_off = [p.stem for p in livros_off]
    idx_off = int(st.session_state.get("moby_off_book_index", 0)) % len(livros_off)
    col_book, col_eureka, col_theme = st.columns([3, 1.25, 3], gap="small")
    with col_book:
        if str(st.session_state.get("moby_off_book_pick", "")) not in nomes_off:
            st.session_state["moby_off_book_pick"] = nomes_off[idx_off]
        livro_off = st.selectbox(f"livros: {idx_off + 1} / {len(nomes_off)}", nomes_off, key="moby_off_book_pick")
        novo_idx = nomes_off.index(livro_off)
        if novo_idx != st.session_state.moby_off_book_index:
            st.session_state.moby_off_plus_help = False
            st.session_state.moby_off_book_index = novo_idx
            paginas_novo_livro = current_off_pages()
            st.session_state.moby_off_take = (
                random.randrange(len(paginas_novo_livro)) if paginas_novo_livro else 0
            )
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

    with col_eureka:
        st.markdown("<div style='height:1.45rem'></div>", unsafe_allow_html=True)
        st.button("EUREKA", key="moby_eureka_focus_off", width="stretch", on_click=toggle_eureka)

    with col_theme:
        titulo_off = st.selectbox(f"temas: {st.session_state.moby_off_take + 1} / {len(titulos_off)}", titulos_off, key="moby_off_page_pick")
        novo_take = titulos_off.index(titulo_off)
        if novo_take != st.session_state.moby_off_take:
            st.session_state.moby_off_plus_help = False
            st.session_state.moby_off_take = novo_take
            invalidate_real_image()
            invalidate_ola()
            st.rerun()
else:
    temas = current_themes()
    if not temas:
        st.error(f'O DNA não contém temas ativos para o livro "{st.session_state.moby_book}".')
        st.stop()

    livro_atual_idx = MOBY_BOOKS.index(st.session_state.moby_book) if st.session_state.moby_book in MOBY_BOOKS else 0
    tema_atual_idx = int(st.session_state.get("moby_theme_index", 0)) % len(temas)
    col_book, col_eureka, col_theme = st.columns([3, 1.25, 3], gap="small")
    with col_book:
        st.selectbox(
            f"livros: {livro_atual_idx + 1} / {len(MOBY_BOOKS)}",
            MOBY_BOOKS,
            index=livro_atual_idx,
            key="moby_book_pick",
            on_change=book_changed,
        )
    with col_eureka:
        st.markdown("<div style='height:1.45rem'></div>", unsafe_allow_html=True)
        st.button("EUREKA", key="moby_eureka_focus", width="stretch", on_click=toggle_eureka)
    with col_theme:
        current = current_theme()
        if st.session_state.get("moby_theme_pick") not in temas:
            st.session_state["moby_theme_pick"] = current
        st.selectbox(
            f"temas: {tema_atual_idx + 1} / {len(temas)}",
            temas,
            key="moby_theme_pick",
            on_change=theme_picked,
        )


# =============================================================================
# PAINEL DE COMANDO DO LEITOR
# =============================================================================
b_rand, b_prev, b_plus, b_next, b_sound, b_help = st.columns(6, gap="small")

with b_rand:
    st.button(
        "*",
        key="moby_rand",
        width="stretch",
        on_click=random_theme,
    )

with b_prev:
    st.button(
        "<",
        key="moby_prev",
        width="stretch",
        on_click=previous_theme,
    )

with b_plus:
    st.button(
        "+",
        key="moby_plus",
        width="stretch",
        on_click=new_reading,
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
        on_click=toggle_sound,
    )

with b_help:
    st.button(
        "?",
        key="moby_help",
        width="stretch",
        on_click=toggle_help,
    )


# =============================================================================
# PALCO — área de aparição; única região rolável
# =============================================================================
fonte_palco = str(st.session_state.get("moby_font_family", "Comic Relief"))
fonte_css = fonte_palco_css(fonte_palco)
peso_palco, estilo_css = estilo_palco_css(fonte_palco)
corpo_palco = int(st.session_state.get("moby_font_size", 20))

if st.session_state.get("moby_mode") == "Off-Machina":
    titulo_palco, corpo_off = current_off_page()
    poema_html_original = html.escape(str(corpo_off)).replace("\n", "<br>")
else:
    update_real_poem()
    titulo_palco = current_theme()
    poema_html_original = str(st.session_state.get("moby_poem_html", ""))

poema_html = translate_poem_html(poema_html_original)

if st.session_state.get("moby_eureka_open", False):
    termo_eureka = st.session_state.get(
        "moby_eureka_mark_term",
        st.session_state.get("moby_eureka_seed", ""),
    )
    poema_html = _moby_eureka_mark_html(poema_html, termo_eureka)

st.session_state.moby_current_title = str(titulo_palco)
st.session_state.moby_current_poem_html = str(poema_html)

with st.container(key="moby_stage_scroll", border=False):
    if (
        st.session_state.get("moby_mode") == "Off-Machina"
        and st.session_state.get("moby_off_plus_help", False)
    ):
        st.markdown(
            "<div style='font-family:\"MV Boli\", \"Segoe Print\", cursive; font-size:.95rem; line-height:1.55; padding:20px 12px;'>"
            "<b>Os livros Off-Machina não têm variações.</b><br>"
            "Cada poema pertence a um livro do autor e é único.<br>"
            "Os outros botões navegam por essas páginas."
            "</div>",
            unsafe_allow_html=True,
        )
    elif st.session_state.moby_help_open:
        with st.container(key="moby_help_text"):
            st.markdown(load_manual_moby())
        if st.session_state.get("moby_mode") == "Machina":
            tema_help = current_theme()
            matrix_path = _matrix_image_path_for_theme(tema_help)
            if matrix_path:
                st.image(str(matrix_path), width="stretch")
            linhas_ficha = _help_ficha_linhas(tema_help)
            if linhas_ficha:
                st.text("\n".join(linhas_ficha))
    else:
        # Título do yPoema: referência visual permanente do palco.
        # A voz lê somente o conteúdo e não substitui o título.
        st.markdown(
            f"<div class='moby-poem-title'>{html.escape(str(titulo_palco))}</div>",
            unsafe_allow_html=True,
        )
        if st.session_state.get("moby_sound_open", False):
            render_sound_player(update_sound_audio(titulo_palco, poema_html))

        st.markdown(
            f"<div class='ypoema' style='font-family:{fonte_css}; font-size:{corpo_palco}px; font-weight:{peso_palco}; font-style:{estilo_css};'>"
            f"{poema_html}</div>",
            unsafe_allow_html=True,
        )

# =============================================================================
# RODAPÉ — bloco físico fixo: controles + ilustração dispensável
# =============================================================================
update_real_image()
imagem_1 = str(st.session_state.get("moby_image_path", "")).strip()
imagem_2 = str(st.session_state.get("moby_image_path_2", "")).strip()
footer_view = str(st.session_state.get("moby_footer_view", "images"))

# Quando a ilustração é dispensada, apenas a faixa dos controles permanece;
# o espaço liberado volta ao palco.
if footer_view == "none":
    st.markdown(
        """
        <style>
        .st-key-moby_stage_scroll {
            height: 525px; min-height: 525px; max-height: 525px;
        }
        .st-key-moby_footer_zone {
            height: 40px; min-height: 40px; max-height: 40px; padding-bottom: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

with st.container(key="moby_footer_zone", border=False):
    with st.container(key="moby_footer_controls", border=False):
        c1, c2, c3 = st.columns(3, gap="small")

        with c1:
            with st.popover("Copiar", help="copiar texto", use_container_width=True):
                st.code(ypoema_html_to_text(poema_html), language=None, wrap_lines=True)

        with c2:
            st.button("Imagem", key="moby_image", width="stretch", on_click=toggle_image)

        with c3:
            st.button("Retrato", key="moby_portrait", width="stretch", on_click=prepare_portrait)

    if footer_view == "portrait" and st.session_state.get("moby_portrait_png", b""):
        portrait_png = st.session_state.get("moby_portrait_png", b"")
        with st.container(key="moby_portrait_stage", border=False):
            portrait_view, portrait_actions = st.columns([2.25, 1.0], gap="small")
            with portrait_view:
                st.image(portrait_png, width="content")
            with portrait_actions:
                if st.button(
                    "Ampliar",
                    key="moby_portrait_ampliar",
                    help="ampliar",
                    width="stretch",
                ):
                    ampliar_retrato_moby(portrait_png)
                st.download_button(
                    "Salvar",
                    data=portrait_png,
                    file_name=f"{st.session_state.get('moby_portrait_name', 'retrato')}.png",
                    mime="image/png",
                    key="moby_portrait_save",
                    help="salvar",
                    width="stretch",
                )

    elif footer_view != "none":
        st.session_state.moby_footer_view = "images"
        st.session_state.moby_image_visible = True
        with st.container(key="moby_images_stage", border=False):
            imagem_1_html = (
                f'<img class="moby-footer-image" src="{image_path_to_data_uri(imagem_1)}" alt="">'
                if imagem_1 and Path(imagem_1).is_file() else ""
            )
            imagem_2_html = (
                f'<img class="moby-footer-image" src="{image_path_to_data_uri(imagem_2)}" alt="">'
                if imagem_2 and Path(imagem_2).is_file() else ""
            )
            st.markdown(
                '<div class="moby-footer-images-flex">'
                '<div></div>'
                f'<div class="moby-footer-image-cell">{imagem_1_html}</div>'
                '<div></div>'
                f'<div class="moby-footer-image-cell">{imagem_2_html}</div>'
                '<div></div>'
                '</div>',
                unsafe_allow_html=True,
            )
