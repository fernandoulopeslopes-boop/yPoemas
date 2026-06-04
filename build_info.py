"""build_info.py

Atualiza ./base/info.txt a partir dos arquivos gerados pela família Builds.

Contrato usado pelo ypo_seguro.py / tools_Machina:
    from build_info import gera_info
    gera_info()

Este módulo não depende de tools.py e não altera arquivos .ypo.
"""

import os
import re
import time
from decimal import Decimal, InvalidOperation


BASE_DIR = "./base"
DATA_DIR = "./data"
MD_DIR = "./md_files"


def _read_lines(path):
    """Lê arquivo de texto com fallback seguro."""
    if not os.path.exists(path):
        return []

    with open(path, encoding="utf-8", errors="replace") as file:
        return [line.rstrip("\n") for line in file]


def _save_file(path, filename, lines):
    """Salva lista de linhas, criando a pasta se necessário."""
    os.makedirs(path, exist_ok=True)
    full_path = os.path.join(path, filename)

    with open(full_path, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(str(line).rstrip("\n") + "\n")


def _clean_theme_name(value):
    """Preserva o nome curatorial do tema; não usa capitalize."""
    value = str(value).replace("\ufeff", "").strip()

    if value.endswith(".ypo"):
        value = os.path.splitext(os.path.basename(value))[0]

    return value.strip()


def _parse_mapping_line(line):
    """Interpreta linhas no formato 'tema : valor'."""
    line = str(line).strip()
    if not line:
        return "", ""

    if " : " in line:
        key, _, value = line.partition(" : ")
    elif ":" in line:
        key, _, value = line.partition(":")
    else:
        return _clean_theme_name(line), ""

    return _clean_theme_name(key), value.strip()


def load_temas_ativos():
    """Lê ./base/ativos.txt preservando o formato tema/gênero.

    Retorna lista de tuplas:
        [(tema, genero), ...]

    Fallback:
        usa ./base/rol_todos os temas.txt ou arquivos .ypo em ./data.
    """
    ativos_path = os.path.join(BASE_DIR, "ativos.txt")
    temas = []

    for line in _read_lines(ativos_path):
        raw = line.strip()
        if not raw or raw.startswith(("#", "//", "--")):
            continue

        tema, genero = _parse_mapping_line(raw)
        if tema:
            temas.append((tema, genero))

    if temas:
        return temas

    for rol_name in ("rol_todos os temas.txt", "rol_todos_os_temas.txt"):
        rol_path = os.path.join(BASE_DIR, rol_name)
        for line in _read_lines(rol_path):
            raw = line.strip()
            if not raw or raw.startswith(("#", "//", "--")):
                continue
            tema = _clean_theme_name(raw.replace(" ", ""))
            if tema:
                temas.append((tema, "ativo"))

        if temas:
            return temas

    if os.path.isdir(DATA_DIR):
        for filename in sorted(os.listdir(DATA_DIR), key=str.casefold):
            if filename.endswith(".ypo"):
                temas.append((_clean_theme_name(filename), "ativo"))

    return temas


def _lookup_mapping_file(filename, tema, default="0"):
    """Procura tema em arquivo de mapeamento 'tema : valor'."""
    tema = _clean_theme_name(tema)
    path = os.path.join(BASE_DIR, filename)

    for line in _read_lines(path):
        key, value = _parse_mapping_line(line)
        if key.casefold() == tema.casefold():
            return value if value != "" else default

    return default


def say_imagem(tema):
    """Retorna a pasta/imagem associada ao tema em ./base/images.txt."""
    return _lookup_mapping_file("images.txt", tema, default="")


def say_versos(tema):
    """Retorna quantidade de versos gerada por build_matrix."""
    return _lookup_mapping_file("versos.txt", tema, default="0")


def say_itimos(tema):
    """Retorna quantidade de ítimos gerada por build_matrix."""
    return _lookup_mapping_file("itimos.txt", tema, default="0")


def _fonte_matches_tema(fonte, tema):
    """Confere se a fonte do lexico_pt pertence ao tema, preservando nomes exatos."""
    fonte = str(fonte).strip()
    tema = _clean_theme_name(tema)

    return (
        fonte == tema
        or fonte.startswith(tema + "_")
        or fonte.casefold() == tema.casefold()
        or fonte.casefold().startswith(tema.casefold() + "_")
    )


def _lexico_stats_from_lexico_pt(tema):
    """Calcula wordin e winlex a partir de ./base/lexico_pt.txt."""
    tema = _clean_theme_name(tema)
    wordin = 0
    unique_words = set()

    for line in _read_lines(os.path.join(BASE_DIR, "lexico_pt.txt")):
        if " : " not in line:
            continue

        word, _, fonte = line.partition(" : ")
        word = word.strip()
        fonte = fonte.strip()

        if not word or not fonte:
            continue

        if _fonte_matches_tema(fonte, tema):
            wordin += 1
            unique_words.add(word.casefold())

    return wordin, len(unique_words)


def say_wordin(tema):
    """Retorna verbetes no texto.

    Preferência:
    1. ./base/wordin.txt, se existir;
    2. cálculo por ./base/lexico_pt.txt.
    """
    mapped = _lookup_mapping_file("wordin.txt", tema, default=None)
    if mapped is not None:
        return mapped

    wordin, _winlex = _lexico_stats_from_lexico_pt(tema)
    return str(wordin)


def say_winlex(tema):
    """Retorna verbetes únicos do tema.

    Preferência:
    1. ./base/winlex.txt, se existir;
    2. cálculo por ./base/lexico_pt.txt.
    """
    mapped = _lookup_mapping_file("winlex.txt", tema, default=None)
    if mapped is not None:
        return mapped

    _wordin, winlex = _lexico_stats_from_lexico_pt(tema)
    return str(winlex)


def say_number(tema):
    """Retorna análise combinatória em ABOUT_index/ABOUT_INDEX."""
    tema = _clean_theme_name(tema)

    candidates = [
        os.path.join(MD_DIR, "ABOUT_index.md"),
        os.path.join(MD_DIR, "ABOUT_INDEX.md"),
    ]

    for path in candidates:
        for line in _read_lines(path):
            key, value = _parse_mapping_line(line)
            if key.casefold() == tema.casefold():
                return value if value else "0"

    return "0"


def _scientific_from_analysis(value):
    """Gera notação científica segura a partir do texto de análise."""
    text = str(value)

    # Se build_indexy gravou "inteiro | 1.234E+56", usa a parte inteira.
    if "|" in text:
        text = text.split("|", 1)[0]

    digits = "".join(ch for ch in text if ch.isdigit())

    if not digits:
        return "0"

    try:
        number = Decimal(digits)
    except (InvalidOperation, ValueError):
        return "0"

    scientific = f"{number:.3E}"
    scientific = scientific.replace(".", ",")
    scientific = scientific.replace("E+", " e+")
    scientific = scientific.replace("E-", " e-")
    return scientific


def gera_info():
    """Gera ./base/info.txt."""
    start_time = time.time()
    info = []

    info.append("|nome_tema|genero|imagem|versos|words_in|lexico|ítimos|analise|notação|")
    info.append("|   [0]   |  [1] |  [2] |  [3] |   [4]  |  [5] |  [6] |  [7]  |  [8]  |")
    info.append("")

    list_ativos = load_temas_ativos()

    for tema, txt_genero in list_ativos:
        txt_imagem = say_imagem(tema)
        qtd_versos = say_versos(tema)
        qtd_wordin = say_wordin(tema)
        qtd_lexico = say_winlex(tema)
        qtd_itimos = say_itimos(tema)
        qtd_analiz = say_number(tema)
        qtd_scient = _scientific_from_analysis(qtd_analiz)

        text = ""
        text += "|" + tema
        text += "|" + txt_genero
        text += "|" + txt_imagem
        text += "|" + qtd_versos
        text += "|" + qtd_wordin
        text += "|" + qtd_lexico
        text += "|" + qtd_itimos
        text += "|" + qtd_analiz
        text += "|" + qtd_scient
        text += "|"

        info.append(text)
        print(tema)

    _save_file(BASE_DIR, "info.txt", info)

    print("Runtime:", time.time() - start_time)
    return info


def main():
    gera_info()


if __name__ == "__main__":
    main()
