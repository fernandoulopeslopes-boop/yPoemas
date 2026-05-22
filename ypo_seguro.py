# -*- coding: utf-8 -*-
"""
ypo_seguro.py

Página ABOUT da Machina.

Padrão dos arquivos MD:
    ABOUT_nome_da_informacao.md

Regras:
    - "ABOUT_" é a chave geral.
    - o nome depois de ABOUT_ vira o título do menu em lower.
    - ABOUT_machina_A.md e ABOUT_machina_D.md são inseparáveis.
      Onde aparece A, D é carregado junto.
    - fonte/corpo são escolha do leitor e valem para todos os ABOUTs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import streamlit as st


# -----------------------------------------------------------------------------
# CONFIGURAÇÃO BÁSICA
# -----------------------------------------------------------------------------

ABOUT_PREFIX = "ABOUT_"
ABOUT_EXT = ".md"

# Ajuste aqui, se seus ABOUTs estiverem em outra pasta.
# A função abaixo também procura automaticamente em pastas comuns.
ABOUT_DIR_CANDIDATES = [
    Path("."),
    Path("about"),
    Path("abouts"),
    Path("ABOUTS"),
    Path("md"),
    Path("MD_FILES"),
    Path("data"),
    Path("docs"),
]

FONTES = {
    "serif": "Georgia, 'Times New Roman', serif",
    "sans": "Arial, Helvetica, sans-serif",
    "mono": "'Courier New', Courier, monospace",
}

CORPOS = {
    "pequeno": 16,
    "normal": 18,
    "grande": 20,
    "maior": 22,
}


# -----------------------------------------------------------------------------
# DESCOBERTA DOS ABOUTS
# -----------------------------------------------------------------------------

def find_about_dir() -> Path:
    """Retorna a primeira pasta que contém arquivos ABOUT_*.md."""
    for folder in ABOUT_DIR_CANDIDATES:
        if folder.exists() and any(folder.glob(f"{ABOUT_PREFIX}*{ABOUT_EXT}")):
            return folder
    return Path(".")


def about_key(path: Path) -> str:
    """
    Transforma ABOUT_nome_da_informacao.md em nome_da_informacao.
    Mantém apenas a chave interna, sem prefixo e sem extensão.
    """
    name = path.stem
    if name.startswith(ABOUT_PREFIX):
        name = name[len(ABOUT_PREFIX):]
    return name


def about_title_from_key(key: str) -> str:
    """
    Título que aparece no menu da página About.
    Regra combinada: lower.
    """
    return key.lower().replace("_", " ")


def load_about_files(about_dir: Path) -> Dict[str, Path]:
    """Carrega todos os ABOUT_*.md encontrados."""
    files = sorted(about_dir.glob(f"{ABOUT_PREFIX}*{ABOUT_EXT}"))
    return {about_key(path): path for path in files}


def build_about_menu(about_files: Dict[str, Path]) -> List[Tuple[str, List[Path]]]:
    """
    Cria o menu de ABOUTs.

    Caso especial:
        ABOUT_machina_A.md + ABOUT_machina_D.md aparecem como um único item:
            machina
        e são renderizados juntos, A depois D.
    """
    menu: List[Tuple[str, List[Path]]] = []
    used = set()

    lower_map = {key.lower(): key for key in about_files.keys()}

    machina_a_key = lower_map.get("machina_a")
    machina_d_key = lower_map.get("machina_d")

    if machina_a_key and machina_d_key:
        menu.append(("machina", [about_files[machina_a_key], about_files[machina_d_key]]))
        used.add(machina_a_key)
        used.add(machina_d_key)

    for key in sorted(about_files.keys(), key=lambda value: value.lower()):
        if key in used:
            continue
        menu.append((about_title_from_key(key), [about_files[key]]))

    return menu


# -----------------------------------------------------------------------------
# LEITURA / RENDERIZAÇÃO
# -----------------------------------------------------------------------------

def read_md(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def inject_about_css(font_family: str, font_size: int) -> None:
    """Aplica fonte/corpo apenas à área dos ABOUTs."""
    line_height = round(font_size * 1.72, 2)

    st.markdown(
        f"""
        <style>
            .machina-about {{
                max-width: 880px;
                margin: 0 auto;
                font-family: {font_family};
                font-size: {font_size}px;
                line-height: {line_height}px;
            }}
            .machina-about blockquote {{
                margin-left: 1.15rem;
                padding-left: 1rem;
                border-left: 3px solid rgba(120, 120, 120, 0.28);
            }}
            .machina-about hr {{
                margin: 1.6rem 0;
                opacity: 0.35;
            }}
            .machina-about p {{
                margin-bottom: 0.86rem;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_md_in_about_container(md_text: str) -> None:
    """
    Renderiza o markdown dentro de uma div própria.
    Mantém o markdown original e aplica CSS externo.
    """
    st.markdown('<div class="machina-about">', unsafe_allow_html=True)
    st.markdown(md_text)
    st.markdown('</div>', unsafe_allow_html=True)


def render_about_page() -> None:
    """Página ABOUT completa."""
    about_dir = find_about_dir()
    about_files = load_about_files(about_dir)

    st.sidebar.markdown("### leitura")

    fonte_label = st.sidebar.selectbox(
        "fonte",
        options=list(FONTES.keys()),
        index=0,
        key="about_fonte",
    )

    corpo_label = st.sidebar.selectbox(
        "corpo",
        options=list(CORPOS.keys()),
        index=1,
        key="about_corpo",
    )

    inject_about_css(
        font_family=FONTES[fonte_label],
        font_size=CORPOS[corpo_label],
    )

    if not about_files:
        st.warning(f"Nenhum arquivo {ABOUT_PREFIX}*{ABOUT_EXT} encontrado.")
        st.caption(f"Pasta verificada: {about_dir.resolve()}")
        return

    menu = build_about_menu(about_files)
    menu_titles = [title for title, _paths in menu]

    st.sidebar.markdown("### about")
    selected_title = st.sidebar.radio(
        "",
        options=menu_titles,
        index=0,
        label_visibility="collapsed",
        key="about_selected",
    )

    selected_paths = dict(menu)[selected_title]

    for index, path in enumerate(selected_paths):
        if index > 0:
            st.markdown("---")
        render_md_in_about_container(read_md(path))


# -----------------------------------------------------------------------------
# EXECUÇÃO DIRETA
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    st.set_page_config(
        page_title="yPoemas @ Machina de Fazer Poesia",
        layout="wide",
    )
    render_about_page()
