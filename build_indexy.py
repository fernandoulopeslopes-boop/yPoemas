#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
build_indexy.py

Gera o índice combinatório dos temas da Machina para uso no ABOUT_index.md.

Contrato usado pelo ypo_seguro.py / tools_Machina:
    from build_indexy import gera_indexy
    gera_indexy()

Este módulo não depende de tools.py e não altera arquivos .ypo.
"""

import os
import sys
from decimal import Decimal, getcontext


BASE_DIR = "./base"
DATA_DIR = "./data"
MD_DIR = "./md_files"

_IGNORE_PREFIXES = ("#", "//", "--")


def _clean_theme_name(value):
    """Preserva o nome curatorial do tema; não usa capitalize."""
    value = str(value).replace("\ufeff", "").strip()

    if value.endswith(".ypo"):
        value = os.path.splitext(os.path.basename(value))[0]

    return value.strip()


def _read_theme_list_from_file(path):
    """Lê nomes de temas de um arquivo de lista da Machina."""
    temas = []

    if not os.path.exists(path):
        return temas

    with open(path, encoding="utf-8", errors="replace") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or line.startswith(_IGNORE_PREFIXES):
                continue

            if "|" in line:
                parts = [part.strip() for part in line.split("|") if part.strip()]
                if parts:
                    line = parts[0]
            elif " : " in line:
                line = line.partition(" : ")[0]
            elif ":" in line:
                line = line.partition(":")[0]

            tema = _clean_theme_name(line.replace(" ", ""))
            if tema and tema not in temas:
                temas.append(tema)

    return temas


def load_temas_ativos():
    """Retorna os temas ativos sem depender de tools.py."""
    candidates = [
        os.path.join(BASE_DIR, "ativos.txt"),
        os.path.join(BASE_DIR, "rol_todos os temas.txt"),
        os.path.join(BASE_DIR, "rol_todos_os_temas.txt"),
    ]

    temas = []
    for candidate in candidates:
        temas = _read_theme_list_from_file(candidate)
        if temas:
            break

    if not temas and os.path.isdir(DATA_DIR):
        temas = sorted(
            os.path.splitext(file_name)[0]
            for file_name in os.listdir(DATA_DIR)
            if file_name.endswith(".ypo")
        )

    return {tema: "ativo" for tema in temas}


def _choices_from_ypo_line(line):
    """Conta opções de ítimos em uma linha .ypo válida."""
    parts = line.rstrip("\n").split("|")

    # Padrão:
    # |linha|ideia|fonte|F|qtd_itimos|itimos_atual| itimo 1 | itimo 2 | ... |
    if len(parts) >= 8:
        choices = [part.strip() for part in parts[7:] if part.strip()]
        if choices:
            return len(choices)

    return 1


def _format_number(number):
    """Formata número inteiro e notação científica sem depender de bibliotecas externas."""
    if not isinstance(number, int):
        return str(number)

    digits = len(str(number))
    if digits <= 18:
        return str(number)

    getcontext().prec = 8
    scientific = f"{Decimal(number):.6E}"
    return f"{number}  |  {scientific}"


def zay_number(tema):
    """Calcula a combinatória aproximada de um tema .ypo."""
    tema = _clean_theme_name(tema)
    file_path = os.path.join(DATA_DIR, tema + ".ypo")

    if not os.path.exists(file_path):
        return "arquivo .ypo não encontrado"

    total = 1
    valid_lines = 0

    with open(file_path, encoding="utf-8", errors="replace") as ypo_file:
        for line in ypo_file:
            if not line.startswith("|"):
                continue

            total *= max(1, _choices_from_ypo_line(line))
            valid_lines += 1

    if valid_lines == 0:
        return "sem linhas válidas"

    return _format_number(total)


def gera_indexy():
    """Gera ABOUT_index.md e ABOUT_INDEX.md para compatibilidade histórica."""
    lista_ativos = load_temas_ativos()
    os.makedirs(MD_DIR, exist_ok=True)

    linhas = []
    for tema in sorted(lista_ativos.keys(), key=str.casefold):
        numero = zay_number(tema)
        linhas.append(f"{tema} : {numero}\n")

    outputs = [
        os.path.join(MD_DIR, "ABOUT_index.md"),
        os.path.join(MD_DIR, "ABOUT_INDEX.md"),
    ]

    for output in outputs:
        with open(output, "w", encoding="utf-8") as file:
            file.writelines(linhas)

    print(f"ABOUT_index gerado: {len(linhas)} temas")
    return linhas


def main():
    lista_ativos = load_temas_ativos()

    if len(sys.argv) < 2:
        print("Uso: python build_indexy.py <tema>")
        print("ou:  python build_indexy.py --all")
        print("Temas disponíveis:")
        for tema, tipo in lista_ativos.items():
            print(f" {tema} : {tipo}")
        return

    tema = sys.argv[1]

    if tema == "--all":
        gera_indexy()
        return

    if tema not in lista_ativos:
        print(f"Erro: tema '{tema}' não encontrado na lista de ativos")
        return

    numero = zay_number(tema)
    tipo = lista_ativos[tema]

    print(f"Tema: {tema}")
    print(f"Tipo: {tipo}")
    print(f"Número: {numero}")


if __name__ == "__main__":
    main()
