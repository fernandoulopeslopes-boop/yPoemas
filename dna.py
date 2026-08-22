"""DNA ÚNICO — autoridade cadastral da Machina.

Este módulo NÃO calcula poesia nem altera .ypo.
Ele apenas lê, valida e oferece consultas do cadastro base/DNA.TXT.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

DNA_HEADER = (
    "codigo", "tema", "ativo", "ordem", "livro", "banco_tematico",
    "versos", "verbetes_no_texto", "verbetes_do_tema", "total_de_itimos",
    "qtd_de_variacoes", "qtd_cientifica",
)
DNA_STATUS = {"N", "T", "S"}
DNA_DEFAULTS_NOVO_TEMA = {
    "ativo": "T",
    "banco_tematico": "machina",
}

class DNAError(RuntimeError):
    pass


def dna_path(base_dir: str | Path = "./base") -> Path:
    return Path(base_dir) / "DNA.TXT"


def ler(base_dir: str | Path = "./base") -> list[dict[str, str]]:
    path = dna_path(base_dir)
    if not path.is_file():
        raise DNAError(f"DNA não encontrado: {path}")
    header: list[str] = []
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8-sig") as f:
        for numero, raw in enumerate(f, start=1):
            line = raw.strip()
            if line == "<EOF>":
                break
            if not line.startswith("|"):
                continue
            fields = [x.strip() for x in line.split("|")[1:-1]]
            if not header:
                header = fields
                if tuple(header) != DNA_HEADER:
                    raise DNAError(
                        "Cabeçalho DNA divergente.\n"
                        f"esperado: {'|'.join(DNA_HEADER)}\n"
                        f"encontrado: {'|'.join(header)}"
                    )
                continue
            if len(fields) != len(header):
                raise DNAError(f"DNA linha {numero}: {len(fields)} campos; esperado {len(header)}")
            rows.append(dict(zip(header, fields)))
    return rows


def validar(rows: Iterable[dict[str, str]], *, exigir_completos: bool = True) -> list[str]:
    erros: list[str] = []
    vistos_tema: set[str] = set()
    vistos_codigo: set[str] = set()
    vistos_ordem: set[str] = set()
    for n, row in enumerate(rows, start=1):
        tema = str(row.get("tema", "")).strip()
        codigo = str(row.get("codigo", "")).strip()
        ordem = str(row.get("ordem", "")).strip()
        ativo = str(row.get("ativo", "")).strip().upper()
        chave = tema.casefold()
        if exigir_completos:
            vazios = [campo for campo in DNA_HEADER if not str(row.get(campo, "")).strip()]
            if vazios:
                erros.append(f"{tema or '#'+str(n)}: campo(s) vazio(s): {', '.join(vazios)}")
        if not tema:
            erros.append(f"registro {n}: tema vazio")
        elif chave in vistos_tema:
            erros.append(f"tema duplicado: {tema}")
        vistos_tema.add(chave)
        if codigo:
            if codigo in vistos_codigo:
                erros.append(f"codigo duplicado: {codigo}")
            vistos_codigo.add(codigo)
        if ordem:
            if ordem in vistos_ordem:
                erros.append(f"ordem duplicada: {ordem}")
            vistos_ordem.add(ordem)
        if ativo and ativo not in DNA_STATUS:
            erros.append(f"{tema}: ativo inválido {ativo!r}; use N/T/S")
    return erros


def registro(tema: str, base_dir: str | Path = "./base") -> dict[str, str]:
    alvo = str(tema or "").strip().casefold()
    for row in ler(base_dir):
        if row.get("tema", "").strip().casefold() == alvo:
            return row
    return {}


def banco_do_tema(tema: str, base_dir: str | Path = "./base") -> str:
    """Retorna o banco temático cadastrado no DNA para um tema."""
    row = registro(tema, base_dir)
    return str(row.get("banco_tematico", "")).strip() if row else ""


def _status_visivel(include_testes: bool) -> set[str]:
    return {"S", "T"} if include_testes else {"S"}


def temas_do_livro(livro: str, base_dir: str | Path = "./base", *, include_testes: bool = True) -> list[str]:
    nome_livro = str(livro or "").strip().casefold()
    permitidos = _status_visivel(include_testes)
    result: list[tuple[int, str]] = []
    for row in ler(base_dir):
        if row.get("ativo", "").strip().upper() not in permitidos:
            continue
        livros = [x.strip().casefold() for x in row.get("livro", "").split(";") if x.strip()]
        if nome_livro == "todos os temas" or nome_livro in livros:
            try:
                ordem = int(row.get("ordem", ""))
            except Exception:
                ordem = 10**9
            result.append((ordem, row.get("tema", "").replace(" ", "").strip()))
    result.sort(key=lambda item: item[0])
    return [tema for _, tema in result]


def mapa_bancos(base_dir: str | Path = "./base", *, include_testes: bool = True) -> dict[str, str]:
    permitidos = _status_visivel(include_testes)
    out: dict[str, str] = {}
    for row in ler(base_dir):
        if row.get("ativo", "").strip().upper() not in permitidos:
            continue
        tema = row.get("tema", "").strip()
        banco = row.get("banco_tematico", "").strip()
        if tema and banco:
            out[tema.casefold()] = banco
    return out


def bancos(base_dir: str | Path = "./base", *, include_testes: bool = True) -> list[str]:
    valores = {v for v in mapa_bancos(base_dir, include_testes=include_testes).values() if v}
    return sorted(valores, key=str.casefold)


def linhas_images_compat(base_dir: str | Path = "./base", *, include_testes: bool = True) -> list[str]:
    """Compatibilidade transitória: oferece o conteúdo lógico de images.txt sem ler images.txt."""
    mapa = mapa_bancos(base_dir, include_testes=include_testes)
    return [f"{row['tema']} : {mapa[row['tema'].casefold()]}\n" for row in ler(base_dir)
            if row.get('tema','').casefold() in mapa]
