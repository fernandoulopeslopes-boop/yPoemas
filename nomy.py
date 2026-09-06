# nomy.py — NOMY 1.0 / primeira arquitetura visual mobile
from __future__ import annotations

from pathlib import Path
from io import BytesIO
import html
import random
import re
import unicodedata

import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps

from acros import gerar_acros, AcrosError
from akros_motor import gerar_akros, AkrosError

ROOT = Path(__file__).resolve().parent
BASE_DIR = ROOT / "data" / "acros"
IMAGES_ROOT = ROOT / "images"

st.set_page_config(
    page_title="NOMY",
    page_icon="🍒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

FONTES = {
    "OpenDyslexic": ('"OpenDyslexic", sans-serif', "OpenDyslexic"),
    "MV Boli": ('"MV Boli", "Segoe Print", cursive', "MV Boli"),
    "Source Code SemiBold": ('"Source Code Pro", Consolas, "Courier New", monospace', "Source Code Pro"),
    "Comic Relief": ('"Comic Relief", "Comic Sans MS", cursive', "Comic Relief"),
    "JetBrains Mono": ('"JetBrains Mono", Consolas, "Courier New", monospace', "JetBrains Mono"),
    "Ubuntu Condensed": ('"Ubuntu Condensed", "Arial Narrow", Arial, sans-serif', "Ubuntu Condensed"),
}
ESTILOS = ("normal", "itálico", "bold", "bold itálico")
CORPOS = tuple(range(16, 37))
RETRATO_FONTE_AJUSTE_DEFAULT = 1.60
RETRATO_IMAGEM_PCT = 34
RETRATO_COMPACTACAO = 100


def _init_state():
    defaults = {
        "nomy_nome": "",
        "nomy_genero": "Feminino",
        "nomy_leitura": "Simples",
        "nomy_fonte": "Comic Relief",
        "nomy_estilo": "normal",
        "nomy_corpo": 20,
        "nomy_resultado": None,
        "nomy_nome_ativo": "",
        "nomy_genero_ativo": "Feminino",
        "nomy_leitura_ativa": "Simples",
        "nomy_fonte_ativa": "Comic Relief",
        "nomy_estilo_ativo": "normal",
        "nomy_corpo_ativo": 20,
        "nomy_retrato": None,
        "nomy_retrato_assinatura": None,
        "nomy_palco_view": "texto",
        "nomy_retrato_imagem": "",
        "nomy_retrato_fator": RETRATO_FONTE_AJUSTE_DEFAULT,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()



def _toggle_palco_view():
    atual = st.session_state.get("nomy_palco_view", "texto")
    st.session_state["nomy_palco_view"] = "texto" if atual == "imagem" else "imagem"



def _retrato_valido() -> bool:
    png = st.session_state.get("nomy_retrato")
    return (
        png is not None
        and st.session_state.get("nomy_retrato_assinatura") == _assinatura_retrato()
    )


def _atualizar_retrato(*, preservar_imagem: bool) -> bool:
    png = _criar_retrato_png(preservar_imagem=preservar_imagem)
    if not png:
        return False

    st.session_state["nomy_retrato"] = png
    st.session_state["nomy_retrato_assinatura"] = _assinatura_retrato()
    return True


def _sincronizar_retrato_do_palco():
    """Se o palco está em imagem, atualiza o PNG sem trocar o estado."""
    if st.session_state.get("nomy_palco_view", "texto") != "imagem":
        return
    if st.session_state.get("nomy_resultado") is None:
        return
    if _retrato_valido():
        return

    # Fonte/estilo/corpo: preserva a imagem escolhida.
    if not _atualizar_retrato(preservar_imagem=True):
        # Falha técnica não autoriza cruzar o estado silenciosamente.
        st.session_state["nomy_retrato"] = None
        st.session_state["nomy_retrato_assinatura"] = None


def _gerar(nome: str, genero: str, leitura: str):
    if leitura == "Poético":
        return gerar_akros(entrada=nome, genero=genero, base_dir=BASE_DIR)
    return gerar_acros(entrada=nome, genero=genero, base_dir=BASE_DIR)


def _resultado_html(resultado) -> str:
    linhas_html = []
    for linha in resultado.linhas:
        if linha.verbete is None:
            linhas_html.append(
                "<div class='nomy-linha nomy-linha-sem-verbete'>"
                f"<span class='nomy-inicial'></span><span class='nomy-resto'>{html.escape(linha.markdown)}</span>"
                "</div>"
            )
            continue
        primeira = html.escape(str(linha.entrada or "")[:1].upper())
        resto = linha.verbete[1:] if len(linha.verbete) > 1 else ""
        linhas_html.append(
            "<div class='nomy-linha'>"
            f"<strong class='nomy-inicial'>{primeira}</strong>"
            f"<span class='nomy-resto'>{html.escape(resto)}</span>"
            "</div>"
        )
    return "<div class='nomy-texto-bloco'>" + "".join(linhas_html) + "</div>"


def _assinatura_retrato():
    resultado = st.session_state.get("nomy_resultado")
    if resultado is None:
        return None
    return (
        str(
            st.session_state.get("nomy_nome")
            or st.session_state.get("nomy_nome_ativo")
            or ""
        ).strip(),
        st.session_state.get("nomy_genero_ativo", ""),
        st.session_state.get("nomy_leitura_ativa", ""),
        st.session_state.get("nomy_fonte", ""),
        st.session_state.get("nomy_estilo", ""),
        int(st.session_state.get("nomy_corpo", 20)),
        float(st.session_state.get("nomy_retrato_fator", RETRATO_FONTE_AJUSTE_DEFAULT)),
        tuple((l.entrada, l.verbete, l.markdown) for l in resultado.linhas),
    )


def _font_key(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value or "")).casefold()
    return "".join(ch for ch in value if ch.isalnum() and not unicodedata.combining(ch))


def _font_path(fonte_nome: str, estilo: str) -> str | None:
    _, family = FONTES[fonte_nome]
    fonts_dir = ROOT / "fonts"
    aliases = {
        "sourcecodepro": {"sourcecodepro", "sourcecodesemibold"},
        "mvboli": {"mvboli"},
        "comicrelief": {"comicrelief"},
        "jetbrainsmono": {"jetbrainsmono"},
        "ubuntucondensed": {"ubuntucondensed"},
        "opendyslexic": {"opendyslexic"},
    }
    wanted = _font_key(family)
    targets = aliases.get(wanted, {wanted})

    candidatos = []
    if fonts_dir.is_dir():
        for path in sorted(fonts_dir.iterdir()):
            if not path.is_file() or path.suffix.casefold() not in {".ttf", ".otf"}:
                continue
            key = _font_key(path.stem)
            if any(target and target in key for target in targets):
                candidatos.append(path)

    estilo_key = _font_key(estilo)
    quer_bold = "bold" in estilo_key
    quer_italico = "italico" in estilo_key

    def flags(path: Path):
        key = _font_key(path.stem)
        is_bold = any(k in key for k in ("bold", "semibold", "demibold"))
        is_italic = any(k in key for k in ("italic", "ital", "oblique"))
        return is_bold, is_italic

    if candidatos:
        # Primeiro: variante exata solicitada.
        exatos = [
            p for p in candidatos
            if flags(p) == (quer_bold, quer_italico)
        ]
        if exatos:
            return str(exatos[0])

        # Depois: aproximações previsíveis, sem trocar estilo ao acaso.
        if quer_bold and quer_italico:
            aprox = [p for p in candidatos if all(flags(p))]
            if aprox:
                return str(aprox[0])
        elif quer_bold:
            aprox = [p for p in candidatos if flags(p)[0]]
            if aprox:
                return str(aprox[0])
        elif quer_italico:
            aprox = [p for p in candidatos if flags(p)[1]]
            if aprox:
                return str(aprox[0])

        # Regular como último recurso dentro da família.
        regulares = [p for p in candidatos if flags(p) == (False, False)]
        if regulares:
            return str(regulares[0])
        return str(candidatos[0])

    if family == "MV Boli":
        win = Path("C:/Windows/Fonts/mvboli.ttf")
        if win.is_file():
            return str(win)
    return None


def _pil_font(size: int, fonte_nome: str, estilo: str):
    path = _font_path(fonte_nome, estilo)
    if path:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            pass

    estilo_key = _font_key(estilo)
    quer_bold = "bold" in estilo_key
    quer_italico = "italico" in estilo_key

    if quer_bold and quer_italico:
        fallback_candidates = [
            "C:/Windows/Fonts/arialbi.ttf",
            "C:/Windows/Fonts/calibriz.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-BoldItalic.ttf",
        ]
    elif quer_bold:
        fallback_candidates = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        ]
    elif quer_italico:
        fallback_candidates = [
            "C:/Windows/Fonts/ariali.ttf",
            "C:/Windows/Fonts/calibrii.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Italic.ttf",
        ]
    else:
        fallback_candidates = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        ]

    # Fallback sempre escalável; regular só depois da variante solicitada.
    fallback_candidates += [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]

    for candidato in fallback_candidates:
        if Path(candidato).is_file():
            try:
                return ImageFont.truetype(candidato, size=size)
            except OSError:
                pass

    return ImageFont.load_default()


def _wrap_text(draw, texto: str, font, max_width: int):
    palavras = texto.split()
    if not palavras:
        return [""]
    linhas, atual = [], palavras[0]
    for palavra in palavras[1:]:
        teste = atual + " " + palavra
        box = draw.textbbox((0, 0), teste, font=font)
        if box[2] - box[0] <= max_width:
            atual = teste
        else:
            linhas.append(atual)
            atual = palavra
    linhas.append(atual)
    return linhas


def _escolher_imagem_retrato(genero: str) -> Path | None:
    pasta = IMAGES_ROOT / ("persona" if genero == "Feminino" else "machina")
    if not pasta.is_dir():
        return None
    arquivos = [
        p for p in pasta.iterdir()
        if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")
    ]
    return random.choice(arquivos) if arquivos else None


def _criar_retrato_png(*, preservar_imagem: bool = False) -> bytes | None:
    resultado = st.session_state.get("nomy_resultado")
    if resultado is None:
        return None

    nome = str(
        st.session_state.get("nomy_nome")
        or st.session_state.get("nomy_nome_ativo")
        or ""
    ).strip()
    genero = st.session_state.get("nomy_genero_ativo", "Feminino")
    leitura = st.session_state.get("nomy_leitura_ativa", "Simples")
    fonte_nome = st.session_state.get("nomy_fonte", "Comic Relief")
    estilo = st.session_state.get("nomy_estilo", "normal")
    corpo = int(st.session_state.get("nomy_corpo", 20))

    escala = 2
    fator_retrato = float(
        st.session_state.get("nomy_retrato_fator", RETRATO_FONTE_AJUSTE_DEFAULT)
    )
    img_pct = RETRATO_IMAGEM_PCT
    compactacao = RETRATO_COMPACTACAO

    tamanho_retrato = max(1, round(corpo * escala * fator_retrato))
    font = _pil_font(tamanho_retrato, fonte_nome, estilo)

    width = 1080
    margin_x = 78
    margin_y = 72
    gap = 58

    inner_w = width - (margin_x * 2)
    image_box_w = max(220, round(inner_w * (img_pct / 100.0)))
    image_box_h = round(image_box_w * 1.5)
    text_w = max(290, inner_w - image_box_w - gap)

    probe = Image.new("RGB", (width, 100), "white")
    probe_draw = ImageDraw.Draw(probe)

    blocos = []
    for linha in resultado.linhas:
        if linha.verbete is None:
            texto = linha.markdown
        else:
            primeira = str(linha.entrada or "")[:1].upper()
            resto = linha.verbete[1:] if len(linha.verbete) > 1 else ""
            texto = primeira + " " + resto
        blocos.extend(_wrap_text(probe_draw, texto, font, text_w))
        blocos.append("")

    if blocos and blocos[-1] == "":
        blocos.pop()

    line_h_base = max(tamanho_retrato + 16, 46)
    line_h = max(30, round(line_h_base * (compactacao / 100.0)))
    blank_gap = max(8, round(line_h * 0.42))

    text_h = sum(blank_gap if item == "" else line_h for item in blocos)
    text_h = max(line_h, text_h)

    content_h = max(image_box_h, text_h)
    height = max(1350, content_h + (margin_y * 2)) if leitura == "Poético" else 1350

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    block_w = image_box_w + gap + text_w
    block_h = max(image_box_h, text_h)
    block_x = max(margin_x, (width - block_w) // 2)
    block_y = max(margin_y, (height - block_h) // 2)

    image_x = block_x
    image_y = block_y + max(0, (block_h - image_box_h) // 2)
    text_x = block_x + image_box_w + gap
    text_y = block_y + max(0, (block_h - text_h) // 2)

    imagem_path = None
    if preservar_imagem:
        atual = str(st.session_state.get("nomy_retrato_imagem", "")).strip()
        if atual and Path(atual).is_file():
            imagem_path = Path(atual)
    if imagem_path is None:
        imagem_path = _escolher_imagem_retrato(genero)

    if imagem_path:
        try:
            with Image.open(imagem_path) as original:
                foto = ImageOps.exif_transpose(original).convert("RGB")
                foto = ImageOps.fit(
                    foto,
                    (image_box_w, image_box_h),
                    method=Image.Resampling.LANCZOS,
                )
                img.paste(foto, (image_x, image_y))
                st.session_state["nomy_retrato_imagem"] = str(imagem_path)
        except OSError:
            st.session_state["nomy_retrato_imagem"] = ""
    else:
        st.session_state["nomy_retrato_imagem"] = ""

    y = text_y
    for item in blocos:
        if item == "":
            y += blank_gap
        else:
            draw.text((text_x, y), item, fill="black", font=font)
            y += line_h

    bio = BytesIO()
    img.save(bio, format="PNG", optimize=True)
    return bio.getvalue()


_init_state()

resultado = st.session_state.get("nomy_resultado")
fonte_ativa = st.session_state.get("nomy_fonte", "Comic Relief")
estilo_ativo = st.session_state.get("nomy_estilo", "normal")
corpo_ativo = int(st.session_state.get("nomy_corpo", 20))
fonte_css = FONTES[fonte_ativa][0]
estilo_key = str(estilo_ativo).casefold()
estilo_css = "italic" if "itálico" in estilo_key else "normal"
peso_css = 700 if "bold" in estilo_key else 400

st.markdown(
    f"""
    <style>
    #MainMenu, footer, header {{
        display:none !important;
        visibility:hidden !important;
        height:0 !important;
        min-height:0 !important;
        margin:0 !important;
        padding:0 !important;
    }}
    section[data-testid="stSidebar"] {{ display:none !important; }}

    .block-container,
    div[data-testid="stMainBlockContainer"] {{
        width:calc(100vw - 24px) !important;
        max-width:430px !important;
        margin:0 auto !important;
        padding:12px !important;
        background:white !important;
        border:1px solid rgba(0,0,0,.18) !important;
        border-radius:28px !important;
        box-shadow:0 10px 35px rgba(0,0,0,.10) !important;
        height:auto !important;
        min-height:0 !important;
        max-height:none !important;
        overflow:visible !important;
        box-sizing:border-box !important;
    }}

    div[data-testid="stVerticalBlock"] {{ gap:.48rem; }}
    div[data-testid="stHorizontalBlock"] {{
        flex-wrap:nowrap !important;
        gap:.28rem !important;
    }}
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {{
        min-width:0 !important;
        width:auto !important;
    }}

    div[data-testid="stButton"] button,
    div[data-testid="stDownloadButton"] button {{
        min-height:38px !important;
        height:38px !important;
        border-radius:9px !important;
        padding-left:.18rem !important;
        padding-right:.18rem !important;
        font-size:.88rem !important;
    }}

    div[data-testid="stSelectbox"] label {{ display:none !important; }}
    div[data-testid="stTextInput"] label {{ display:none !important; }}

    .nomy-palco {{
        height:525px;
        min-height:525px;
        max-height:525px;
        overflow-y:auto;
        overflow-x:hidden;
        margin-top:2px;
        padding:10px 7px 12px 7px;
        box-sizing:border-box;
        font-family:{fonte_css};
        font-style:{estilo_css};
        font-weight:{peso_css};
        font-size:{corpo_ativo}px;
        line-height:1.35;
        overflow-wrap:anywhere;
    }}
    .nomy-texto-bloco {{
        width:fit-content;
        max-width:100%;
        margin:0 auto;
    }}
    .nomy-linha {{
        display:grid;
        grid-template-columns:1.15em minmax(0, auto);
        column-gap:.42em;
        align-items:baseline;
        margin:.18rem 0;
    }}
    .nomy-inicial {{
        font-weight:700;
        text-align:center;
    }}
    .nomy-resto {{
        min-width:0;
    }}

    .st-key-nomy_retrato_palco {{
        height:525px !important;
        min-height:525px !important;
        max-height:525px !important;
        overflow:hidden !important;
        display:flex !important;
        align-items:center !important;
        justify-content:center !important;
        margin-top:2px !important;
        padding:8px !important;
        box-sizing:border-box !important;
    }}
    .st-key-nomy_retrato_palco > div,
    .st-key-nomy_retrato_palco div[data-testid="stVerticalBlock"],
    .st-key-nomy_retrato_palco div[data-testid="stImage"] {{
        width:100% !important;
        height:100% !important;
        display:flex !important;
        align-items:center !important;
        justify-content:center !important;
    }}
    .st-key-nomy_retrato_palco img {{
        width:auto !important;
        max-width:96% !important;
        height:auto !important;
        max-height:505px !important;
        margin:0 auto !important;
        object-fit:contain !important;
    }}

    @media (max-width:600px) {{
        .block-container,
        div[data-testid="stMainBlockContainer"] {{
            width:calc(100vw - 24px) !important;
            max-width:430px !important;
            padding:12px !important;
            border-radius:20px !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# O estado do palco é autoridade.
# Se fonte/estilo/corpo/layout mudaram durante um Retrato,
# recompõe o PNG antes de calcular botões e palco.
_sincronizar_retrato_do_palco()

with st.container(key="nomy_controles", border=False):
    # A primeira faixa usa a mesma malha da faixa inferior:
    # input ocupa exatamente as duas primeiras unidades (F + S).
    c_nome, c_formato = st.columns([1.64, 2.80], gap="small")

    with c_nome:
        st.text_input(
            "nome para o acróstico",
            key="nomy_nome",
            placeholder="nome",
            label_visibility="collapsed",
        )

    with c_formato:
        c_fonte, c_estilo, c_corpo = st.columns([1.75, 1.20, 0.72], gap="small")
        with c_fonte:
            st.selectbox("fonte", tuple(FONTES), key="nomy_fonte", label_visibility="collapsed")
        with c_estilo:
            st.selectbox("estilo", ESTILOS, key="nomy_estilo", label_visibility="collapsed")
        with c_corpo:
            st.selectbox("corpo", CORPOS, key="nomy_corpo", label_visibility="collapsed")

    c_gen, c_leitura, c_criar, c_retrato = st.columns([0.82, 0.82, 1.40, 1.40], gap="small")

    with c_gen:
        clic_f = st.button(
            "F", key="nomy_f", width="stretch",
            type="primary" if st.session_state["nomy_genero"] == "Feminino" else "secondary",
        )
        clic_m = st.button(
            "M", key="nomy_m", width="stretch",
            type="primary" if st.session_state["nomy_genero"] == "Masculino" else "secondary",
        )

    with c_leitura:
        clic_s = st.button(
            "S", key="nomy_s", width="stretch",
            type="primary" if st.session_state["nomy_leitura"] == "Simples" else "secondary",
        )
        clic_p = st.button(
            "P", key="nomy_p", width="stretch",
            type="primary" if st.session_state["nomy_leitura"] == "Poético" else "secondary",
        )

    retrato_png = st.session_state.get("nomy_retrato")
    retrato_valido = _retrato_valido()

    with c_criar:
        # O rótulo indica a AÇÃO: "Imagem" mostra o PNG; "Texto" volta ao acróstico.
        view_label = "Texto" if st.session_state.get("nomy_palco_view") == "imagem" else "Imagem"
        imagem_swap = st.button(
            view_label,
            key="nomy_imagem_swap",
            width="stretch",
            disabled=not retrato_valido,
            on_click=_toggle_palco_view,
        )
        criar = st.button("Criar", key="nomy_criar", width="stretch")

    with c_retrato:
        if retrato_valido:
            safe = re.sub(
                r"[^A-Za-z0-9_-]+", "_", st.session_state.get("nomy_nome_ativo", "")
            ).strip("_") or "nomy"
            st.download_button(
                "Salvar",
                data=retrato_png,
                file_name=f"NOMY_{safe}.png",
                mime="image/png",
                key="nomy_salvar",
                width="stretch",
            )
        else:
            st.button("Salvar", key="nomy_salvar_vazio", width="stretch", disabled=True)

        retrato = st.button(
            "Retrato", key="nomy_retrato_btn", width="stretch", disabled=resultado is None
        )

st.divider()

def _swap_resultado(*, genero=None, leitura=None):
    view_atual = st.session_state.get("nomy_palco_view", "texto")

    genero_anterior = st.session_state.get("nomy_genero")
    if genero is not None:
        st.session_state["nomy_genero"] = genero
    if leitura is not None:
        st.session_state["nomy_leitura"] = leitura

    resultado_atual = st.session_state.get("nomy_resultado")
    nome = str(
        st.session_state.get("nomy_nome_ativo")
        or st.session_state.get("nomy_nome")
        or ""
    ).strip()

    # Antes do primeiro Criar, troca apenas a seleção.
    if resultado_atual is None or not nome:
        _rerun()

    try:
        novo = _gerar(
            nome,
            st.session_state["nomy_genero"],
            st.session_state["nomy_leitura"],
        )
    except (AcrosError, AkrosError) as exc:
        st.error(str(exc))
        return

    st.session_state["nomy_resultado"] = novo
    st.session_state["nomy_nome_ativo"] = nome
    st.session_state["nomy_genero_ativo"] = st.session_state["nomy_genero"]
    st.session_state["nomy_leitura_ativa"] = st.session_state["nomy_leitura"]

    # O conteúdo muda; o estado do palco não.
    if view_atual == "imagem":
        mudou_genero = (
            genero is not None
            and st.session_state["nomy_genero"] != genero_anterior
        )
        # F/M pode mudar a família de imagens; S/P preserva a imagem.
        ok = _atualizar_retrato(preservar_imagem=not mudou_genero)
        if not ok:
            st.session_state["nomy_retrato"] = None
            st.session_state["nomy_retrato_assinatura"] = None

    st.session_state["nomy_palco_view"] = view_atual
    _rerun()


if clic_f:
    _swap_resultado(genero="Feminino")
if clic_m:
    _swap_resultado(genero="Masculino")
if clic_s:
    _swap_resultado(leitura="Simples")
if clic_p:
    _swap_resultado(leitura="Poético")

if criar:
    view_atual = st.session_state.get("nomy_palco_view", "texto")
    nome = str(st.session_state.get("nomy_nome", "")).strip()

    if not nome:
        st.error("digite um nome ou palavra")
    else:
        try:
            novo = _gerar(
                nome,
                st.session_state["nomy_genero"],
                st.session_state["nomy_leitura"],
            )
        except (AcrosError, AkrosError) as exc:
            st.error(str(exc))
        else:
            st.session_state["nomy_resultado"] = novo
            st.session_state["nomy_nome_ativo"] = nome
            st.session_state["nomy_genero_ativo"] = st.session_state["nomy_genero"]
            st.session_state["nomy_leitura_ativa"] = st.session_state["nomy_leitura"]
            st.session_state["nomy_fonte_ativa"] = st.session_state["nomy_fonte"]
            st.session_state["nomy_estilo_ativo"] = st.session_state["nomy_estilo"]
            st.session_state["nomy_corpo_ativo"] = int(st.session_state["nomy_corpo"])

            if view_atual == "imagem":
                # Novo resultado: novo Retrato; não atravessa para Texto.
                if not _atualizar_retrato(preservar_imagem=False):
                    st.session_state["nomy_retrato"] = None
                    st.session_state["nomy_retrato_assinatura"] = None

            st.session_state["nomy_palco_view"] = view_atual
            _rerun()

if retrato:
    if _atualizar_retrato(preservar_imagem=False):
        st.session_state["nomy_palco_view"] = "imagem"
        _rerun()

resultado = st.session_state.get("nomy_resultado")
if resultado is not None:
    if st.session_state.get("nomy_palco_view", "texto") == "imagem":
        if _retrato_valido():
            with st.container(key="nomy_retrato_palco", border=False):
                st.image(st.session_state["nomy_retrato"], width="stretch")
        else:
            # Estado continua IMAGEM; não mostra Texto como tela intermediária.
            st.markdown("<div class='nomy-palco'></div>", unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div class='nomy-palco'>{_resultado_html(resultado)}</div>",
            unsafe_allow_html=True,
        )
else:
    st.markdown("<div class='nomy-palco'></div>", unsafe_allow_html=True)
