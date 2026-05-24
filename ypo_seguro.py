#!/usr/bin/env python3
"""
RAIO_X_DA_MACHINA.py

Curadoria interna da Machina.
AC/DC: Antes da Catástrofe / Depois da Catástrofe.

Unidade de medida:
    função = peça da Machina

Uso:
    python RAIO_X_DA_MACHINA.py
    python RAIO_X_DA_MACHINA.py caminho/para/ypo_seguro.py
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path


DOC_JSON = Path("CURADORIA_MACHINA_DOC.json")
OUT_JSON = Path("CURADORIA_MACHINA_DOC.json")
OUT_CSV = Path("CURADORIA_MACHINA.csv")
OUT_MD = Path("CURADORIA_MACHINA.md")


RISK_HINTS = {
    "main": 10,
    "init_session_state": 10,
    "page_ypoemas": 10,
    "load_poema": 10,
    "load_temas": 9,
    "load_lypo": 9,
    "page_eureka": 9,
    "page_off_machina": 9,
    "page_mini": 8,
    "pick_lang": 8,
    "pick_book_sidebar": 8,
    "write_ypoema": 8,
    "translate": 8,
    "load_typo": 8,
    "apply_styles": 7,
    "page_abouts": 7,
}


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def sha16(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def mnemonic(name: str) -> str:
    if len(name) <= 18:
        return name
    return name.replace("page_", "pg_").replace("session_state", "state")[:24]


def short_result(name: str) -> str:
    if name == "main":
        return "orquestra a Machina"
    if name.startswith("page_"):
        return "renderiza página/ambiente"
    if name.startswith("load_"):
        return "carrega dados/arquivo"
    if name.startswith("pick_"):
        return "controle de seleção"
    if name.startswith("update_"):
        return "atualiza estado/contador"
    if name.startswith("open_") or name.startswith("close_"):
        return "controle visual/layout"
    if name.startswith("write_"):
        return "renderiza conteúdo"
    if name.startswith("list_"):
        return "lista/relatório"
    if name.startswith("draw_"):
        return "controle visual"
    if name.startswith("show_"):
        return "exibe elemento visual"
    if name == "translate":
        return "traduz conteúdo"
    if name == "talk":
        return "voz/leitura"
    return "peça funcional"


def called_names(node: ast.AST) -> list[str]:
    names = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            fn = child.func
            if isinstance(fn, ast.Name):
                names.add(fn.id)
            elif isinstance(fn, ast.Attribute):
                names.add(fn.attr)
    return sorted(names)


def session_keys(source: str) -> list[str]:
    keys = set()
    for m in re.finditer(r"st\.session_state\.([A-Za-z_][A-Za-z0-9_]*)", source):
        keys.add(m.group(1))
    for m in re.finditer(r"st\.session_state\[['\"]([^'\"]+)['\"]\]", source):
        keys.add(m.group(1))
    return sorted(keys)


def risk_score(name: str, source: str, called_by_count: int, calls_count: int) -> int:
    if name in RISK_HINTS:
        return RISK_HINTS[name]

    risk = 2
    if name.startswith("page_"):
        risk += 4
    if "st.session_state" in source:
        risk += 3
    if "st." in source:
        risk += 2
    if "open(" in source or "os.path" in source:
        risk += 1
    if "translate(" in source:
        risk += 1
    if "load_poema(" in source or "gera_poema(" in source:
        risk += 3
    if called_by_count >= 3:
        risk += 2
    if calls_count >= 6:
        risk += 1
    return max(0, min(10, risk))


def load_previous() -> dict[str, dict]:
    if not DOC_JSON.exists():
        return {}
    try:
        data = json.loads(DOC_JSON.read_text(encoding="utf-8"))
        return {p["nome_funcao"]: p for p in data.get("pieces", [])}
    except Exception:
        return {}


def scan(py_path: Path) -> list[dict]:
    code = py_path.read_text(encoding="utf-8")
    tree = ast.parse(code)
    lines = code.splitlines()

    funcs = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    previous = load_previous()

    source_by_name = {}
    calls_by_name = {}

    for node in funcs:
        start = node.lineno
        end = getattr(node, "end_lineno", start)
        source = "\n".join(lines[start - 1:end])
        source_by_name[node.name] = source
        calls_by_name[node.name] = called_names(node)

    function_names = {n.name for n in funcs}
    called_by = {name: [] for name in function_names}
    for name, calls in calls_by_name.items():
        for call in calls:
            if call in function_names and call != name:
                called_by[call].append(name)

    now = now_iso()
    pieces = []

    for node in funcs:
        name = node.name
        start = node.lineno
        end = getattr(node, "end_lineno", start)
        source = source_by_name[name]
        fingerprint = sha16(source)

        prev = previous.get(name)
        if prev and prev.get("fingerprint") == fingerprint:
            last_update = prev.get("last_update", now)
            status = "sem_mudanca"
        elif prev:
            last_update = now
            status = "alterada"
        else:
            last_update = now
            status = "nova"

        calls = calls_by_name[name]
        callers = sorted(called_by.get(name, []))
        auto_risk = risk_score(name, source, len(callers), len(calls))
        risk = int(prev.get("risco", auto_risk)) if prev and str(prev.get("risco", "")).isdigit() else auto_risk

        pieces.append({
            "nome_funcao": name,
            "nome_mnemonico": prev.get("nome_mnemonico", mnemonic(name)) if prev else mnemonic(name),
            "resultado": prev.get("resultado", short_result(name)) if prev else short_result(name),
            "risco": risk,
            "last_update": last_update,
            "status": status,
            "fingerprint": fingerprint,
            "linha_inicio": start,
            "linha_fim": end,
            "linhas": end - start + 1,
            "chamado_por": callers,
            "chama_quem": calls,
            "session_state": session_keys(source),
            "mexer_com_cuidado": risk >= 8,
        })

    return pieces


def write_outputs(py_path: Path, pieces: list[dict]) -> None:
    generated_at = now_iso()
    doc = {
        "schema": "curadoria_machina_v1",
        "ac_dc": "Depois da Catástrofe",
        "generated_at": generated_at,
        "source_file": str(py_path),
        "total_pieces": len(pieces),
        "pieces": pieces,
    }

    OUT_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")

    fields = [
        "nome_funcao", "nome_mnemonico", "resultado", "risco", "last_update",
        "status", "linha_inicio", "linha_fim", "linhas", "mexer_com_cuidado",
        "session_state", "chamado_por", "chama_quem", "fingerprint",
    ]

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for p in pieces:
            row = dict(p)
            row["session_state"] = ", ".join(row["session_state"])
            row["chamado_por"] = ", ".join(row["chamado_por"])
            row["chama_quem"] = ", ".join(row["chama_quem"])
            writer.writerow({k: row[k] for k in fields})

    high = [p for p in pieces if p["risco"] >= 8]
    changed = [p for p in pieces if p["status"] != "sem_mudanca"]

    md = []
    md.append("# CURADORIA INTERNA DA MACHINA")
    md.append("")
    md.append("AC/DC: Antes da Catástrofe / Depois da Catástrofe.")
    md.append("")
    md.append(f"- gerado em: `{generated_at}`")
    md.append(f"- arquivo analisado: `{py_path}`")
    md.append(f"- peças/funções: **{len(pieces)}**")
    md.append(f"- peças de alto risco: **{len(high)}**")
    md.append(f"- peças novas/alteradas nesta varredura: **{len(changed)}**")
    md.append("")
    md.append("## Peças críticas")
    md.append("")
    md.append("| função | risco | resultado | last_update | status |")
    md.append("|---|---:|---|---|---|")
    for p in sorted(high, key=lambda x: (-x["risco"], x["nome_funcao"])):
        md.append(f"| `{p['nome_funcao']}` | {p['risco']} | {p['resultado']} | {p['last_update']} | {p['status']} |")

    md.append("")
    md.append("## Inventário completo")
    md.append("")
    md.append("| função | mnemônico | risco | linhas | last_update | status |")
    md.append("|---|---|---:|---:|---|---|")
    for p in pieces:
        md.append(f"| `{p['nome_funcao']}` | `{p['nome_mnemonico']}` | {p['risco']} | {p['linhas']} | {p['last_update']} | {p['status']} |")

    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")


def main() -> None:
    py_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("ypo_seguro.py")
    if not py_path.exists():
        raise SystemExit(f"Arquivo não encontrado: {py_path}")

    pieces = scan(py_path)
    write_outputs(py_path, pieces)

    print("RAIO_X_DA_MACHINA")
    print(f"arquivo: {py_path}")
    print(f"peças/funções: {len(pieces)}")
    print(f"alto risco: {sum(1 for p in pieces if p['risco'] >= 8)}")
    print(f"novas/alteradas: {sum(1 for p in pieces if p['status'] != 'sem_mudanca')}")
    print(f"gerados: {OUT_JSON}, {OUT_CSV}, {OUT_MD}")


if __name__ == "__main__":
    main()
