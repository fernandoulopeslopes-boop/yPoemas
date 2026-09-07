# nomy.py — NOMY 1.0 / primeira arquitetura visual mobile
from __future__ import annotations

from pathlib import Path
from io import BytesIO
import base64
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

CORPO_NOMY = 16
FONTES_NOMY_TXT = ROOT / "base" / "fontes_nomy.txt"
HELP_NOMY_MD = ROOT / "data" / "acros" / "help_nomy.md"


def _carregar_fontes_nomy() -> dict[str, str]:
    if not FONTES_NOMY_TXT.is_file():
        raise RuntimeError(f"NOMY: lista de fontes não encontrada: {FONTES_NOMY_TXT}")

    fontes: dict[str, str] = {}
    for linha in FONTES_NOMY_TXT.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        if "|" not in linha:
            continue

        nome, arquivo = (parte.strip() for parte in linha.split("|", 1))
        if nome and arquivo:
            fontes[nome] = arquivo

    if not fontes:
        raise RuntimeError(f"NOMY: nenhuma fonte válida em {FONTES_NOMY_TXT}")

    return fontes


FONTES_NOMY = _carregar_fontes_nomy()
FONTE_NOMY_DEFAULT = next(iter(FONTES_NOMY))
RETRATO_FONTE_AJUSTE_DEFAULT = 1.60
RETRATO_IMAGEM_PCT = 34
RETRATO_COMPACTACAO = 100


def _init_state():
    defaults = {
        "nomy_nome": "",
        "nomy_genero": "Feminino",
        "nomy_leitura": "Simples",
        "nomy_fonte": FONTE_NOMY_DEFAULT,
        "nomy_resultado": None,
        "nomy_nome_ativo": "",
        "nomy_genero_ativo": "Feminino",
        "nomy_leitura_ativa": "Simples",
        "nomy_retrato": None,
        "nomy_retrato_assinatura": None,
        "nomy_palco_view": "texto",
        "nomy_retrato_imagem": "",
        "nomy_retrato_fator": RETRATO_FONTE_AJUSTE_DEFAULT,
        "nomy_help": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()




def _abrir_help():
    st.session_state["nomy_help"] = True


def _limpar_help():
    st.session_state["nomy_help"] = False


def _ler_help_nomy() -> str:
    if not HELP_NOMY_MD.is_file():
        return "Help do NOMY não encontrado."
    return HELP_NOMY_MD.read_text(encoding="utf-8").strip()


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

    # Fonte: preserva a imagem escolhida.
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
        st.session_state.get("nomy_fonte", FONTE_NOMY_DEFAULT),
        CORPO_NOMY,
        float(st.session_state.get("nomy_retrato_fator", RETRATO_FONTE_AJUSTE_DEFAULT)),
        tuple((l.entrada, l.verbete, l.markdown) for l in resultado.linhas),
    )


def _font_path(fonte_nome: str) -> Path:
    arquivo = FONTES_NOMY[fonte_nome]
    path = ROOT / "fonts" / arquivo
    if not path.is_file():
        raise RuntimeError(f"NOMY: fonte não encontrada: {path}")
    return path


def _pil_font(size: int, fonte_nome: str):
    return ImageFont.truetype(str(_font_path(fonte_nome)), size=size)


def _font_face_css(fonte_nome: str) -> str:
    path = _font_path(fonte_nome)
    dados = base64.b64encode(path.read_bytes()).decode("ascii")
    formato = "truetype" if path.suffix.casefold() == ".ttf" else "opentype"
    mime = "font/ttf" if path.suffix.casefold() == ".ttf" else "font/otf"
    return (
        "@font-face {"
        "font-family:'NomySelecionada';"
        f"src:url(data:{mime};base64,{dados}) format('{formato}');"
        "font-style:normal;"
        "font-weight:400;"
        "}"
    )

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
    fonte_nome = st.session_state.get("nomy_fonte", FONTE_NOMY_DEFAULT)
    corpo = CORPO_NOMY

    escala = 2
    fator_retrato = float(
        st.session_state.get("nomy_retrato_fator", RETRATO_FONTE_AJUSTE_DEFAULT)
    )
    img_pct = RETRATO_IMAGEM_PCT
    compactacao = RETRATO_COMPACTACAO

    tamanho_retrato = max(1, round(corpo * escala * fator_retrato))
    font = _pil_font(tamanho_retrato, fonte_nome)

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
fonte_ativa = st.session_state.get("nomy_fonte", FONTE_NOMY_DEFAULT)
corpo_ativo = CORPO_NOMY
font_face_css = _font_face_css(fonte_ativa)
fonte_css = '"NomySelecionada", sans-serif'

st.markdown(
    f"""
    <style>
    {font_face_css}
    #MainMenu, footer {{
        display:none !important;
        visibility:hidden !important;
        height:0 !important;
        min-height:0 !important;
        margin:0 !important;
        padding:0 !important;
    }}

    /* Header global: não ocupa área útil.
       Não esconder <header> genericamente: o toolbar do elemento
       precisa continuar podendo expor o fullscreen do Retrato. */
    header[data-testid="stHeader"] {{
        height:0 !important;
        min-height:0 !important;
        background:transparent !important;
    }}

    div[data-testid="stAppViewContainer"],
    div[data-testid="stMain"],
    section.main {{
        padding-top:0 !important;
        margin-top:0 !important;
    }}

    section[data-testid="stSidebar"] {{ display:none !important; }}

    .stApp {{
        background:#ececec !important;
    }}

    .block-container,
    div[data-testid="stMainBlockContainer"] {{
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
        display:flex;
        align-items:center;
        justify-content:center;
        margin-top:2px;
        padding:10px 7px 12px 7px;
        box-sizing:border-box;
        font-family:{fonte_css};
        font-style:normal;
        font-weight:400;
        font-size:{corpo_ativo}px;
        line-height:1.35;
        overflow-wrap:anywhere;
    }}
    .nomy-texto-bloco {{
        width:fit-content;
        max-width:100%;
        min-width:0;
        margin:0 auto;
        box-sizing:border-box;
    }}

    .st-key-nomy_help_palco {{
        height:525px !important;
        min-height:525px !important;
        max-height:525px !important;
        overflow:auto !important;
        padding:18px 14px !important;
        box-sizing:border-box !important;
        font-family:{fonte_css};
        font-size:{corpo_ativo}px;
        line-height:1.45;
    }}
    .st-key-nomy_help_palco > div,
    .st-key-nomy_help_palco div[data-testid="stVerticalBlock"] {{
        width:100% !important;
        max-width:100% !important;
        min-width:0 !important;
        box-sizing:border-box !important;
    }}
    .nomy-linha {{
        display:grid;
        grid-template-columns:1.15em minmax(0, 1fr);
        width:100%;
        max-width:100%;
        min-width:0;
        column-gap:.42em;
        align-items:baseline;
        margin:.18rem 0;
        box-sizing:border-box;
    }}
    .nomy-inicial {{
        font-weight:700;
        text-align:center;
    }}
    .nomy-resto {{
        min-width:0;
        overflow-wrap:anywhere;
        word-break:break-word;
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
        max-width:100% !important;
        min-width:0 !important;
        height:100% !important;
        display:flex !important;
        align-items:center !important;
        justify-content:center !important;
        overflow:hidden !important;
        box-sizing:border-box !important;
    }}
    .st-key-nomy_retrato_palco * {{
        min-width:0 !important;
        max-width:100% !important;
        box-sizing:border-box !important;
    }}
    .st-key-nomy_retrato_palco div[data-testid="stImage"] > div {{
        width:100% !important;
        display:flex !important;
        justify-content:center !important;
        align-items:center !important;
        margin:0 auto !important;
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
# Se a fonte mudou durante um Retrato,
# recompõe o PNG antes de calcular botões e palco.
_sincronizar_retrato_do_palco()

with st.container(key="nomy_controles", border=False):
    c_nome, c_help, c_fonte = st.columns([1.64, 0.52, 2.28], gap="small")

    with c_nome:
        st.text_input(
            "nome para o acróstico",
            key="nomy_nome",
            placeholder="nome",
            label_visibility="collapsed",
        )

    with c_help:
        clic_help = st.button(
            "?",
            key="nomy_help_btn",
            width="stretch",
            on_click=_abrir_help,
        )

    with c_fonte:
        st.selectbox(
            "fonte",
            tuple(FONTES_NOMY),
            key="nomy_fonte",
            label_visibility="collapsed",
        )

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
            salvar = st.download_button(
                "Salvar",
                data=retrato_png,
                file_name=f"NOMY_{safe}.png",
                mime="image/png",
                key="nomy_salvar",
                width="stretch",
            )
        else:
            salvar = st.button(
                "Salvar", key="nomy_salvar_vazio", width="stretch", disabled=True
            )

        retrato = st.button(
            "Retrato", key="nomy_retrato_btn", width="stretch", disabled=resultado is None
        )


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


if any((clic_f, clic_m, clic_s, clic_p, imagem_swap, criar, salvar, retrato)):
    _limpar_help()

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

if st.session_state.get("nomy_help", False):
    with st.container(key="nomy_help_palco", border=False):
        st.markdown(_ler_help_nomy())
elif resultado is not None:
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
