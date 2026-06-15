#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
build_ficha_tecnica_limpa_de_verdade.py

Varrre a lista de temas da Machina e gera uma lista de divergências da ficha
tecnica do rodapé dos .ypo.

Também pode corrigir, em lote controlado, apenas as linhas técnicas do rodapé:
- Versos
- Verbetes usados / Verbetes no texto
- Verbetes do Tema
- Banco de Ítimos
- Análise combinatória

Contrato:
- não altera versos/ítimos/conteúdo poético;
- não mexe no motor;
- correção opcional cria backup antes;
- relatório registra exatamente o que foi alterado.
"""

import os
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, getcontext

BASE_DIR = "./base"
DATA_DIR = "./data"
BACKUP_DIR = "./backup_ficha_tecnica_ypo"
OUTPUT_FILE = os.path.join(BASE_DIR, "lista_ficha_tecnica_divergencias.txt")
REPORT_FILE = os.path.join(BASE_DIR, "relatorio_ficha_tecnica_corrigida.txt")

ROL_CANDIDATES = [
    os.path.join(BASE_DIR, "todos os temas.rol"),
    os.path.join(BASE_DIR, "todos_os_temas.rol"),
    os.path.join(BASE_DIR, "rol_todos os temas.txt"),
    os.path.join(BASE_DIR, "rol_todos_os_temas.txt"),
    os.path.join(BASE_DIR, "ativos.txt"),
]

IGNORE_PREFIXES = ("#", "//", "--")
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9_]+", re.UNICODE)


@dataclass
class TemaStats:
    tema: str
    versos: int
    verbetes_usados: int
    verbetes_tema: int
    banco_itimos: int
    analise: int


@dataclass
class Divergence:
    campo: str
    antigo: int | None
    novo: int


def clean_theme_name(value):
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

    if os.path.isdir(DATA_DIR):
        temas = sorted(
            os.path.splitext(name)[0]
            for name in os.listdir(DATA_DIR)
            if name.endswith(".ypo")
        )
        return temas, DATA_DIR

    return [], ""


def _data_lines(path):
    lines = []
    with open(path, encoding="utf-8", errors="replace") as file:
        for line in file:
            if line.startswith("|"):
                lines.append(line.rstrip("\r\n"))
    return lines


def _split_ypo_line(line):
    parts = line.split("|")
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return parts


def choices_from_ypo_line(line):
    parts = _split_ypo_line(line)
    choices = [part.strip() for part in parts[7:] if part.strip()]

    # Marcador histórico de tabulação/indentação; acompanha a lógica do motor.
    if choices and "$" in choices[0]:
        choices = choices[1:]

    if choices:
        return choices

    try:
        qtd = max(1, int(parts[5].strip()))
    except Exception:
        qtd = 1

    return [""] * qtd


def _current_choice_from_line(line):
    parts = _split_ypo_line(line)
    choices = choices_from_ypo_line(line)

    if not choices:
        return ""

    try:
        atual = int(parts[6].strip())
    except Exception:
        atual = 0

    if atual < 0:
        atual = 0
    if atual >= len(choices):
        atual = len(choices) - 1

    return choices[atual]


def _count_words(text):
    return len([word for word in WORD_RE.findall(str(text)) if len(word) > 0])


def _norm_itimo(value):
    return " ".join(str(value).split()).casefold()


def calculate_stats(tema):
    path = os.path.join(DATA_DIR, tema + ".ypo")
    if not os.path.exists(path):
        raise FileNotFoundError(f"arquivo .ypo não encontrado: {tema}")

    lines = _data_lines(path)
    if not lines:
        raise ValueError(f"sem linhas válidas: {tema}")

    line_ids = []
    verbetes_tema = 0
    analise = 1
    banco = set()
    verbetes_usados = 0

    for line in lines:
        parts = _split_ypo_line(line)
        if len(parts) > 1 and parts[1].strip():
            line_id = parts[1].strip()
            if line_id not in line_ids:
                line_ids.append(line_id)

        choices = choices_from_ypo_line(line)
        qtd = max(1, len(choices))
        verbetes_tema += qtd
        analise *= qtd

        for choice in choices:
            norm = _norm_itimo(choice)
            if norm:
                banco.add(norm)

        verbetes_usados += _count_words(_current_choice_from_line(line))

    versos = len(line_ids) if line_ids else len(lines)

    return TemaStats(
        tema=tema,
        versos=versos,
        verbetes_usados=verbetes_usados,
        verbetes_tema=verbetes_tema,
        banco_itimos=len(banco),
        analise=analise,
    )


def _digits_to_int(text):
    digits = "".join(re.findall(r"\d+", str(text).split("(", 1)[0]))
    if not digits:
        return None
    try:
        return int(digits)
    except Exception:
        return None


def read_footer_values(tema):
    path = os.path.join(DATA_DIR, tema + ".ypo")
    if not os.path.exists(path):
        raise FileNotFoundError(f"arquivo .ypo não encontrado: {tema}")

    values = {
        "versos": None,
        "verbetes_usados": None,
        "verbetes_tema": None,
        "banco_itimos": None,
        "analise": None,
    }

    patterns = {
        "versos": re.compile(r"\bVersos\s*:\s*(.+)$", re.IGNORECASE),
        "verbetes_usados": re.compile(r"\bVerbetes\s+(?:usados|no\s+texto)\s*:\s*(.+)$", re.IGNORECASE),
        "verbetes_tema": re.compile(r"\bVerbetes\s+do\s+Tema\s*:\s*(.+)$", re.IGNORECASE),
        "banco_itimos": re.compile(r"\bBanco\s+de\s+[ÍI]timos\s*:\s*(.+)$", re.IGNORECASE),
        "analise": re.compile(r"\bAn[aá]lise\s+combinat[oó]ria\s*:\s*(.+)$", re.IGNORECASE),
    }

    with open(path, encoding="utf-8", errors="replace") as file:
        for raw_line in file:
            for key, pattern in patterns.items():
                match = pattern.search(raw_line)
                if match:
                    values[key] = _digits_to_int(match.group(1).strip())

    return values


def stats_as_dict(stats):
    return {
        "versos": stats.versos,
        "verbetes_usados": stats.verbetes_usados,
        "verbetes_tema": stats.verbetes_tema,
        "banco_itimos": stats.banco_itimos,
        "analise": stats.analise,
    }


def field_label(field):
    return {
        "versos": "Versos",
        "verbetes_usados": "Verbetes no texto",
        "verbetes_tema": "Verbetes do Tema",
        "banco_itimos": "Banco de Ítimos",
        "analise": "Análise combinatória",
    }.get(field, field)


def format_big_int(number):
    if number is None:
        return "não encontrado"
    return f"{int(number):,}".replace(",", ".")


def scientific(number):
    if number is None:
        return ""
    getcontext().prec = 8
    return f"{Decimal(number):.6E}".replace(".", ",")


def _compare_theme(tema):
    old_values = read_footer_values(tema)
    new_stats = calculate_stats(tema)
    new_values = stats_as_dict(new_stats)
    divergences = []

    for key, new_value in new_values.items():
        old_value = old_values.get(key)
        if old_value != new_value:
            divergences.append(Divergence(key, old_value, new_value))

    return old_values, new_stats, divergences


def build_lista_ficha_tecnica_divergencias():
    temas, source = load_all_themes()
    resultados = []
    problemas = []

    for tema in temas:
        try:
            _old, _new, divergences = _compare_theme(tema)
            if divergences:
                resultados.append((tema, divergences))
        except Exception as exc:
            problemas.append((tema, str(exc)))

    os.makedirs(os.path.dirname(OUTPUT_FILE) or ".", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("lista_ficha_tecnica_divergencias.txt\n")
        out.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y_%H:%M')}\n")
        out.write(f"Fonte de temas: {source}\n")
        out.write(f"Temas lidos: {len(temas)}\n")
        out.write(f"Temas com divergência: {len(resultados)}\n")
        out.write(f"Problemas: {len(problemas)}\n")
        out.write("\n")

        out.write("Observação: 'Verbetes no texto' é uma medida de amostra técnica,\n")
        out.write("calculada a partir do ítimo atual de cada linha. Não é leitura absoluta do tema.\n\n")

        if resultados:
            out.write("=== DIVERGÊNCIAS DA FICHA TÉCNICA ===\n\n")
            for tema, divergences in resultados:
                out.write(f"Tema: {tema}\n")
                for div in divergences:
                    label = field_label(div.campo)
                    out.write(f"{label}: antigo {format_big_int(div.antigo)} | novo {format_big_int(div.novo)}\n")
                    if div.campo == "analise":
                        out.write(f"Notação nova: {scientific(div.novo)}\n")
                out.write("\n")
        else:
            out.write("Nenhuma divergência encontrada.\n\n")

        if problemas:
            out.write("=== PROBLEMAS DE LEITURA ===\n\n")
            for tema, erro in problemas:
                out.write(f"{tema}: {erro}\n")

    print(f"Temas lidos: {len(temas)}")
    print(f"Temas com divergência: {len(resultados)}")
    print(f"Problemas: {len(problemas)}")
    print(f"Arquivo gerado: {OUTPUT_FILE}")

    return resultados, problemas


def _replace_number_after_colon(line, new_value, keep_suffix=True):
    prefix, sep, rest = line.partition(":")
    if not sep:
        return line

    newline = "\n" if line.endswith("\n") else ""
    rest_no_newline = rest.rstrip("\r\n")
    suffix = ""

    if keep_suffix and "(" in rest_no_newline:
        suffix = " " + rest_no_newline[rest_no_newline.find("("):].strip()

    return f"{prefix}:{' '}{format_big_int(new_value)}{suffix}{newline}"


def _update_footer_lines(lines, stats):
    new_values = stats_as_dict(stats)
    changed = []

    patterns = {
        "versos": re.compile(r"\bVersos\s*:", re.IGNORECASE),
        "verbetes_usados": re.compile(r"\bVerbetes\s+(?:usados|no\s+texto)\s*:", re.IGNORECASE),
        "verbetes_tema": re.compile(r"\bVerbetes\s+do\s+Tema\s*:", re.IGNORECASE),
        "banco_itimos": re.compile(r"\bBanco\s+de\s+[ÍI]timos\s*:", re.IGNORECASE),
        "analise": re.compile(r"\bAn[aá]lise\s+combinat[oó]ria\s*:", re.IGNORECASE),
    }

    updated = []
    seen = set()

    for line in lines:
        new_line = line
        for key, pattern in patterns.items():
            if pattern.search(line):
                old = _digits_to_int(line.partition(":")[2])
                new = new_values[key]
                if old != new:
                    new_line = _replace_number_after_colon(line, new, keep_suffix=(key == "analise"))
                    changed.append((key, old, new))
                seen.add(key)
                break
        updated.append(new_line)

    return updated, changed, seen


def corrigir_rodapes_ficha_tecnica():
    temas, source = load_all_themes()
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(BASE_DIR, exist_ok=True)

    corrigidos = []
    sem_mudanca = []
    problemas = []

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for tema in temas:
        path = os.path.join(DATA_DIR, tema + ".ypo")
        if not os.path.exists(path):
            problemas.append((tema, "arquivo .ypo não encontrado"))
            continue

        try:
            stats = calculate_stats(tema)
            with open(path, encoding="utf-8", errors="replace") as file:
                lines = file.readlines()

            updated, changed, seen = _update_footer_lines(lines, stats)

            missing = [field_label(key) for key in stats_as_dict(stats).keys() if key not in seen]
            if missing:
                problemas.append((tema, "campos de rodapé não encontrados: " + ", ".join(missing)))

            if changed:
                backup_name = f"{tema}.{stamp}.bak"
                backup_path = os.path.join(BACKUP_DIR, backup_name)
                shutil.copy2(path, backup_path)

                tmp_path = path + ".tmp"
                with open(tmp_path, "w", encoding="utf-8", newline="") as file:
                    file.writelines(updated)
                os.replace(tmp_path, path)

                corrigidos.append((tema, changed, backup_path))
            else:
                sem_mudanca.append(tema)

        except Exception as exc:
            problemas.append((tema, str(exc)))

    with open(REPORT_FILE, "w", encoding="utf-8") as out:
        out.write("relatorio_ficha_tecnica_corrigida.txt\n")
        out.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y_%H:%M')}\n")
        out.write(f"Fonte de temas: {source}\n")
        out.write(f"Temas lidos: {len(temas)}\n")
        out.write(f"Temas corrigidos: {len(corrigidos)}\n")
        out.write(f"Sem mudança: {len(sem_mudanca)}\n")
        out.write(f"Problemas: {len(problemas)}\n")
        out.write(f"Backups: {BACKUP_DIR}\n\n")

        if corrigidos:
            out.write("=== CORRIGIDOS ===\n\n")
            for tema, changed, backup_path in corrigidos:
                out.write(f"Tema: {tema}\n")
                out.write(f"Backup: {backup_path}\n")
                for key, old, new in changed:
                    out.write(f"{field_label(key)}: antigo {format_big_int(old)} | novo {format_big_int(new)}\n")
                    if key == "analise":
                        out.write(f"Notação nova: {scientific(new)}\n")
                out.write("\n")

        if problemas:
            out.write("=== PROBLEMAS / AVISOS ===\n\n")
            for tema, erro in problemas:
                out.write(f"{tema}: {erro}\n")

    print(f"Temas corrigidos: {len(corrigidos)}")
    print(f"Problemas: {len(problemas)}")
    print(f"Relatório gerado: {REPORT_FILE}")

    return corrigidos, problemas


# Compatibilidade com o botão antigo, se algum main ainda chamar o nome anterior.
def build_lista_novas_analises():
    return build_lista_ficha_tecnica_divergencias()


if __name__ == "__main__":
    build_lista_ficha_tecnica_divergencias()
