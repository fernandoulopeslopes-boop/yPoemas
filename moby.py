# moby.py
# Etapa 035: sincroniza livros/temas + retorno da sidebar ao palco.
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
    page_icon="🌀",
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


VOICES_EDGE_TTS = {
    "pt": "pt-BR-AntonioNeural", "es": "es-ES-AlvaroNeural",
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


def _moby_font(size, bold=False):
    candidates = [
        Path("./fonts/OpenDyslexic-Bold.otf" if bold else "./fonts/OpenDyslexic-Regular.otf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
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
    body_font = _moby_font(28)
    footer_font = _moby_font(17)
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
        "label": "E-mail",
        "url": "mailto:lopes.fernando@hotmail.com",
        "icon": "https://cdn.simpleicons.org/microsoftoutlook/0078D4",
        "kind": "email",
    },
    {
        "label": "Buy Me a Coffee",
        "url": "https://www.buymeacoffee.com/yPoemas",
        "icon": "https://cdn.simpleicons.org/buymeacoffee/FFDD00",
        "kind": "coffee",
    },
    {
        "label": "WhatsApp / Pix",
        "url": "https://api.whatsapp.com/send?phone=+5512991368181",
        "icon": "https://cdn.simpleicons.org/whatsapp/25D366",
        "icon_2": "https://cdn.simpleicons.org/pix/32BCAD",
        "kind": "whatsapp wide",
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
        "<div class='moby-social-title'>Conecte-se com a Machina</div>"
        "<div class='moby-social-subtitle'>presença, contato e apoio</div>"
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
    voice = VOICES_EDGE_TTS.get(st.session_state.get("moby_lang", "pt"), "pt-BR-AntonioNeural")
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
    """A ordem autoral vive nos rol_*.txt; DNA valida pertencimento/atividade."""
    alvo = str(livro or "").strip().casefold()
    ativos = {}
    for row in rows:
        if str(row.get("ativo", "")).strip().upper() != "S":
            continue
        livros = [item.strip().casefold() for item in str(row.get("livro", "")).split(";") if item.strip()]
        tema = str(row.get("tema", "")).strip()
        if tema and alvo in livros:
            ativos[nome_normalizado(tema)] = tema

    ordem = _rol_temas(livro)
    if ordem:
        vistos = set()
        saida = []
        for tema_rol in ordem:
            chave = nome_normalizado(tema_rol)
            tema = ativos.get(chave)
            if tema and chave not in vistos:
                saida.append(tema)
                vistos.add(chave)
        return saida

    return list(ativos.values())


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
    """A Machina escolhe, de surpresa, uma das duas imagens atuais para o Retrato."""
    dismiss_help()
    update_real_image()
    candidates = [
        path for path in (
            str(st.session_state.get("moby_image_path", "")),
            str(st.session_state.get("moby_image_path_2", "")),
        )
        if path and Path(path).is_file()
    ]
    if not candidates:
        return
    chosen = random.choice(candidates)
    st.session_state.moby_portrait_image = chosen
    title = st.session_state.get("moby_current_title", "retrato")
    poem_html = st.session_state.get("moby_current_poem_html", "")
    png = create_moby_portrait_png(poem_html, chosen, title)
    if png:
        st.session_state.moby_portrait_png = png
        safe = re.sub(r"[^A-Za-z0-9_-]+", "_", str(title or "retrato")).strip("_") or "retrato"
        st.session_state.moby_portrait_name = safe


def update_real_poem():
    """Gera e congela o yPoema real da leitura atual no palco do Moby."""
    tema = current_theme()
    assinatura = (tema, int(st.session_state.get("moby_reading_n", 1)))

    if st.session_state.get("moby_poem_signature") == assinatura:
        return

    try:
        script = gera_poema(tema, "")
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
            # O recuo autoral já vem resolvido pelo lay_2_ypo como &emsp;.
            # Converte apenas essa entidade histórica em espaço Unicode antes
            # de escapar o restante: o palco não interpreta HTML do yPoema.
            texto_linha = texto_linha.replace("&emsp;", "\u2003")
            linhas.append(html.escape(texto_linha))

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
    invalidate_real_image()


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
        invalidate_real_image()


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
        invalidate_real_image()


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
    invalidate_real_image()


def book_changed():
    escolha = str(st.session_state.get("moby_book_pick", st.session_state.get("moby_book", MOBY_DEFAULT_BOOK)))
    if escolha in MOBY_BOOKS:
        st.session_state.moby_book = escolha
    st.session_state.moby_theme_index = 0
    st.session_state.moby_reading_n = 1
    st.session_state.pop("moby_theme_pick", None)
    invalidate_real_poem()
    invalidate_real_image()


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

    .moby-social-card.wide {
        grid-column: 1 / -1;
        min-height: 62px;
        flex-direction: row;
        gap: .65rem;
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

    div[data-testid="stButton"] button {
        min-height: 38px;
        border-radius: 9px;
        padding-left: .35rem !important;
        padding-right: .35rem !important;
        font-size: .88rem !important;
    }



    /* Copiar pertence à mesma família visual de Imagem/Retrato. */
    div[data-testid="stPopover"] > button,
    div[data-testid="stPopover"] button {
        width: 100% !important;
        min-height: 38px !important;
        border-radius: 9px !important;
        font-size: .88rem !important;
    }

    /* O controle nativo de expansão do Retrato precisa aparecer. */
    button[title="Fullscreen"],
    button[aria-label="Fullscreen"],
    button[title="View fullscreen"],
    button[aria-label="View fullscreen"] {
        opacity: 1 !important;
        visibility: visible !important;
        filter: none !important;
        background: rgba(255,255,255,.94) !important;
        border: 1px solid rgba(0,0,0,.24) !important;
        color: #222 !important;
    }


    #MainMenu, footer, header { visibility: hidden; }

    section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* Moby em celular vertical: as barras continuam barras, não pilhas. */
    @media (max-width: 600px) {
        .block-container {
            width: calc(100vw - 12px) !important;
            max-width: 430px !important;
            margin: 6px auto 24px auto !important;
            padding: 12px 12px 18px 12px !important;
            height: auto !important;
            min-height: 820px !important;
            max-height: none !important;
            overflow: visible !important;
            border-radius: 20px;
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
    # Idiomas passam a ocupar o topo da sidebar.
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
            "Fontes & Letras", fonte_labels, index=fonte_labels.index(fonte_atual),
            key="moby_font_pick", on_change=sidebar_font_changed,
        )
    with corpo_col:
        corpo_escolhido = st.selectbox(
            "Corpo", CORPOS_MOBY, index=CORPOS_MOBY.index(corpo_atual),
            key="moby_size_pick", on_change=sidebar_size_changed,
        )
    st.session_state.moby_font_family = fonte_lookup.get(fonte_escolhida, st.session_state.moby_font_family)
    st.session_state.moby_font_size = int(corpo_escolhido)

    about_col, links_col = st.columns([4.4, 1.35], gap="small")
    with about_col:
        st.button("ABOUT", key="moby_sidebar_about", width="stretch", on_click=sidebar_show_about)
    with links_col:
        st.button("links", key="moby_sidebar_links", width="stretch", on_click=sidebar_show_links)

    if st.session_state.get("moby_sidebar_panel", "about") == "links":
        render_social_links()
    else:
        current_about = str(st.session_state.get("moby_about_pick", "machina"))
        if current_about not in ABOUTS_LIST:
            current_about = "machina"
        about_choice = st.selectbox(
            "sobre",
            ABOUTS_LIST,
            index=ABOUTS_LIST.index(current_about),
            key="moby_about_pick",
        )
        st.markdown(load_about_text(about_choice))

    st.button(
        "yPoemas",
        key="moby_close_sidebar",
        width="stretch",
        on_click=sidebar_return_to_stage,
    )

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
        livro_off = st.selectbox(f"livros: {idx_off + 1} / {len(nomes_off)}", nomes_off, index=idx_off, key="moby_off_book_pick")
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
        titulo_off = st.selectbox(f"temas: {st.session_state.moby_off_take + 1} / {len(titulos_off)}", titulos_off, key="moby_off_page_pick")
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

    livro_atual_idx = MOBY_BOOKS.index(st.session_state.moby_book) if st.session_state.moby_book in MOBY_BOOKS else 0
    tema_atual_idx = int(st.session_state.get("moby_theme_index", 0)) % len(temas)
    col_book, col_ola, col_theme = st.columns([3, 1.25, 3], gap="small")
    with col_book:
        st.selectbox(
            f"livros: {livro_atual_idx + 1} / {len(MOBY_BOOKS)}",
            MOBY_BOOKS,
            index=livro_atual_idx,
            key="moby_book_pick",
            on_change=book_changed,
        )
    with col_ola:
        st.markdown("<div style='height:1.45rem'></div>", unsafe_allow_html=True)
        st.button("OLA", key="moby_ola_focus", width="stretch", on_click=request_ola)
    with col_theme:
        current = current_theme()
        if st.session_state.get("moby_theme_pick") not in temas:
            st.session_state["moby_theme_pick"] = current
        st.selectbox(
            f"temas: {tema_atual_idx + 1} / {len(temas)}",
            temas,
            index=temas.index(current),
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


if st.session_state.moby_help_open:
    st.markdown(
        """
        <div class="moby-help">
        <ul>
          <li><b>*</b> tema ao acaso</li>
          <li><b>&lt;</b> tema anterior</li>
          <li><b>+</b> nova leitura do tema</li>
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
limite_palco = 315 if st.session_state.moby_image_visible else 520

if st.session_state.get("moby_mode") == "Off-Machina":
    titulo_palco, corpo_off = current_off_page()
    poema_html = html.escape(str(corpo_off)).replace("\n", "<br>")
else:
    update_real_poem()
    titulo_palco = current_theme()
    poema_html = st.session_state.get("moby_poem_html", "")

poema_html_original = str(poema_html)
poema_html = translate_poem_html(poema_html_original)
st.session_state.moby_current_title = str(titulo_palco)
st.session_state.moby_current_poem_html = str(poema_html)

# Troca justa: o Som ocupa o lugar do título; o yPoema permanece onde estava.
if st.session_state.get("moby_sound_open", False):
    render_sound_player(update_sound_audio(titulo_palco, poema_html))
else:
    # Aspas simples no atributo: as pilhas CSS contêm aspas duplas nos nomes das fontes.
    st.markdown(
        f"<div class='poem-title' style='font-family:{fonte_css}; font-size:{corpo_palco}px;'>"
        f"{html.escape(str(titulo_palco))}</div>",
        unsafe_allow_html=True,
    )

analise_ola = update_ola_analysis(titulo_palco, poema_html_original)
ola_html = ""
if analise_ola:
    ola_html = (
        "<div class='moby-ola-inline'>"
        "<div class='moby-ola-inline-title'>OLA</div>"
        + html.escape(str(analise_ola)).replace("\n", "<br>")
        + "</div>"
    )

st.markdown(
    f"<div class='ypoema' style='font-family:{fonte_css}; font-size:{corpo_palco}px; max-height:{limite_palco}px;'>"
    f"{poema_html}{ola_html}</div>",
    unsafe_allow_html=True,
)

st.markdown('<div class="end-rule"></div>', unsafe_allow_html=True)


# =============================================================================
# AÇÕES FINAIS
# =============================================================================
c1, c2, c3 = st.columns(3, gap="small")

with c1:
    # Comportamento original: abre o texto; o ícone do bloco faz a cópia real.
    with st.popover("Copiar", help="copiar texto", use_container_width=True):
        st.code(ypoema_html_to_text(poema_html), language=None, wrap_lines=True)

with c2:
    st.button("Imagem", key="moby_image", width="stretch", on_click=toggle_image)

with c3:
    st.button("Retrato", key="moby_portrait", width="stretch", on_click=prepare_portrait)

portrait_png = st.session_state.get("moby_portrait_png", b"")
if portrait_png:
    st.image(portrait_png, width="stretch")
    save_left, save_center, save_right = st.columns([1.2, 1, 1.2])
    with save_center:
        st.download_button(
            "salvar...",
            data=portrait_png,
            file_name=f"{st.session_state.get('moby_portrait_name', 'retrato')}.png",
            mime="image/png",
            key="moby_portrait_save",
            width="stretch",
        )

# Duas imagens distintas do mesmo banco temático no rodapé — apenas FIT.
update_real_image()
imagem_1 = str(st.session_state.get("moby_image_path", "")).strip()
imagem_2 = str(st.session_state.get("moby_image_path_2", "")).strip()

if st.session_state.moby_image_visible:
    # As imagens pertencem ao palco visual, mas não precisam de HTML artesanal.
    # st.image preserva a proporção (FIT, sem crop) e elimina a possibilidade
    # de o código do contêiner vazar como texto para o palco.
    img_col_1, img_col_2 = st.columns(2, gap="small")

    with img_col_1:
        if imagem_1 and Path(imagem_1).is_file():
            st.image(imagem_1, width=187)

    with img_col_2:
        if imagem_2 and Path(imagem_2).is_file():
            st.image(imagem_2, width=187)
