#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
build_lista_novas_analises.py

Varrre a lista de temas da Machina e gera uma lista apenas com os temas cuja
Análise combinatória do rodapé do .ypo está diferente do valor calculado agora.

Uso:
    python build_lista_novas_analises.py

Saída padrão:
    ./base/lista_novas_analises.txt

Contrato:
- não altera arquivos .ypo;
- não mexe no motor;
- apenas lê todos os temas e aponta divergências para correção manual posterior.
"""

import os
import re
from datetime import datetime
from decimal import Decimal, getcontext

BASE_DIR = "./base"
DATA_DIR = "./data"
OUTPUT_FILE = os.path.join(BASE_DIR, "lista_novas_analises.txt")

ROL_CANDIDATES = [
    os.path.join(BASE_DIR, "todos os temas.rol"),
    os.path.join(BASE_DIR, "todos_os_temas.rol"),
    os.path.join(BASE_DIR, "rol_todos os temas.txt"),
    os.path.join(BASE_DIR, "rol_todos_os_temas.txt"),
    os.path.join(BASE_DIR, "ativos.txt"),
]

IGNORE_PREFIXES = ("#", "//", "--")


def clean_theme_name(value):
    """Preserva o nome curatorial do tema; não usa capitalize()."""
    value = str(value).replace("\ufeff", "").strip()

    if value.endswith(".ypo"):
        value = os.path.splitext(os.path.basename(value))[0]

    return value.strip()


def read_theme_list(path):
    temas = []

    if not os.path.exists(path):
        return temas

    with open(path, encoding="utf-8", errors="replace") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or line.startswith(IGNORE_PREFIXES):
                continue

            # Aceita formatos simples e formatos com separador.
            if "|" in line:
                line = line.split("|", 1)[0].strip()
            elif " : " in line:
                line = line.partition(" : ")[0].strip()
            elif ":" in line:
                line = line.partition(":")[0].strip()

            tema = clean_theme_name(line)
            if tema and tema not in temas:
                temas.append(tema)

    return temas


def load_all_themes():
    for candidate in ROL_CANDIDATES:
        temas = read_theme_list(candidate)
        if temas:
            return temas, candidate

    # Fallback: usa todos os .ypo encontrados.
    if os.path.isdir(DATA_DIR):
        temas = sorted(
            os.path.splitext(name)[0]
            for name in os.listdir(DATA_DIR)
            if name.endswith(".ypo")
        )
        return temas, DATA_DIR

    return [], ""


def choices_from_ypo_line(line):
    """
    Conta ítimos reais de uma linha .ypo.

    Estrutura esperada:
        |linha|ideia|fonte|F|qtd_itimos|itimos_atual| itimo1 | itimo2 | ... |

    Observação:
    - quando o primeiro campo dos ítimos contém '$', ele é marcador/indentação
      e é descartado, acompanhando a lógica do motor.
    """
    parts = line.rstrip("\r\n").split("|")

    # Remove campo vazio final quando a linha termina em "|".
    if parts and parts[-1] == "":
        parts = parts[:-1]

    choices = [part.strip() for part in parts[7:] if part.strip()]

    if choices and "$" in choices[0]:
        choices = choices[1:]

    if choices:
        return len(choices)

    # Fallback: usa o campo qtd_itimos, se existir.
    try:
        return max(1, int(parts[5].strip()))
    except Exception:
        return 1


def current_analysis_number(tema):
    path = os.path.join(DATA_DIR, tema + ".ypo")
    if not os.path.exists(path):
        return None, "arquivo .ypo não encontrado"

    total = 1
    valid_lines = 0

    with open(path, encoding="utf-8", errors="replace") as file:
        for line in file:
            if not line.startswith("|"):
                continue
            total *= max(1, choices_from_ypo_line(line))
            valid_lines += 1

    if valid_lines == 0:
        return None, "sem linhas válidas"

    return total, ""


def footer_analysis_number(tema):
    path = os.path.join(DATA_DIR, tema + ".ypo")
    if not os.path.exists(path):
        return None, "arquivo .ypo não encontrado"

    # Exemplo:
    # # Análise combinatória: 9.276.752... (nonilhões)
    pattern = re.compile(r"An[aá]lise combinat[oó]ria\s*:\s*(.+)$", re.IGNORECASE)

    with open(path, encoding="utf-8", errors="replace") as file:
        for raw_line in file:
            match = pattern.search(raw_line)
            if not match:
                continue

            value = match.group(1).strip()
            digits = "".join(re.findall(r"\d+", value.split("(", 1)[0]))
            if digits:
                return int(digits), ""
            return None, "rodapé encontrado, mas sem número legível"

    return None, "rodapé sem Análise combinatória"


def format_big_int(number):
    if number is None:
        return ""
    return f"{number:,}".replace(",", ".")


def scientific(number):
    if number is None:
        return ""
    getcontext().prec = 8
    return f"{Decimal(number):.6E}"


def build_lista_novas_analises():
    temas, source = load_all_themes()
    divergencias = []
    problemas = []

    for tema in temas:
        old_value, old_error = footer_analysis_number(tema)
        new_value, new_error = current_analysis_number(tema)

        if old_error or new_error:
            problemas.append((tema, old_error or new_error))
            continue

        if old_value != new_value:
            divergencias.append((tema, old_value, new_value))

    os.makedirs(os.path.dirname(OUTPUT_FILE) or ".", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("lista_novas_analises.txt\n")
        out.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y_%H:%M')}\n")
        out.write(f"Fonte de temas: {source}\n")
        out.write(f"Temas lidos: {len(temas)}\n")
        out.write(f"Divergências: {len(divergencias)}\n")
        out.write(f"Problemas: {len(problemas)}\n")
        out.write("\n")

        if divergencias:
            out.write("=== DIVERGÊNCIAS ===\n\n")
            for tema, old_value, new_value in divergencias:
                out.write(f"Tema: {tema}\n")
                out.write(f"Antiga: {format_big_int(old_value)}\n")
                out.write(f"Nova:   {format_big_int(new_value)}\n")
                out.write(f"Nova_notacao: {scientific(new_value)}\n")
                out.write("\n")
        else:
            out.write("Nenhuma divergência encontrada.\n\n")

        if problemas:
            out.write("=== PROBLEMAS DE LEITURA ===\n\n")
            for tema, erro in problemas:
                out.write(f"{tema}: {erro}\n")

    print(f"Temas lidos: {len(temas)}")
    print(f"Divergências: {len(divergencias)}")
    print(f"Problemas: {len(problemas)}")
    print(f"Arquivo gerado: {OUTPUT_FILE}")

    return divergencias, problemas


if __name__ == "__main__":
    build_lista_novas_analises()
