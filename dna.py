"""DNA ÚNICO — autoridade cadastral da Machina.

Este módulo NÃO calcula poesia nem altera .ypo/.new.
Ele lê o cadastro base/DNA.TXT e oferece consultas aos consumidores.

Autoridades:
- DNA.TXT: cadastro do tema e banco temático.
- rol_<livro>.txt: pertencimento e ordem autoral dos livros.
- rol_estudos.txt: ordem autoral do ambiente de estudo.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

DNA_HEADER = (
    "tema", "ativo", "livro", "banco_tematico",
    "versos", "verbetes_no_texto", "verbetes_do_tema", "total_de_itimos",
    "qtd_de_variacoes", "qtd_cientifica",
)

DNA_HEADER_LEGACY_CODIGO = (
    "codigo", "tema", "ativo", "livro", "banco_tematico",
    "versos", "verbetes_no_texto", "verbetes_do_tema", "total_de_itimos",
    "qtd_de_variacoes", "qtd_cientifica",
)

DNA_HEADER_LEGACY_CODIGO_ORDEM = (
    "codigo", "tema", "ativo", "ordem", "livro", "banco_tematico",
    "versos", "verbetes_no_texto", "verbetes_do_tema", "total_de_itimos",
    "qtd_de_variacoes", "qtd_cientifica",
)

DNA_STATUS = {"N", "T", "S"}

DNA_DEFAULTS_NOVO_TEMA = {
    "ativo": "T",
    "livro": "estudo",
    "banco_tematico": "machina",
}


class DNAError(RuntimeError):
    pass


def dna_path(base_dir: str | Path = "./base") -> Path:
    return Path(base_dir) / "DNA.TXT"


def _normaliza_tema(valor: str) -> str:
    return str(valor or "").strip().casefold()


def _read_simple_list(path: Path) -> list[str]:
    if not path.is_file():
        return []
    return [
        raw.strip()
        for raw in path.read_text(encoding="utf-8-sig").splitlines()
        if raw.strip()
    ]


def ler(base_dir: str | Path = "./base") -> list[dict[str, str]]:
    """Lê DNA atual ou legado; em memória, remove o campo legado 'ordem'."""
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
                header_tuple = tuple(header)
                if header_tuple not in {DNA_HEADER, DNA_HEADER_LEGACY_CODIGO, DNA_HEADER_LEGACY_CODIGO_ORDEM}:
                    raise DNAError(
                        "Cabeçalho DNA divergente.\n"
                        f"esperado atual: {'|'.join(DNA_HEADER)}\n"
                        f"encontrado: {'|'.join(header)}"
                    )
                continue

            if len(fields) != len(header):
                raise DNAError(
                    f"DNA linha {numero}: {len(fields)} campos; esperado {len(header)}"
                )

            row = dict(zip(header, fields))
            row.pop("ordem", None)
            row.pop("codigo", None)
            rows.append(row)

    return rows


def validar(
    rows: Iterable[dict[str, str]],
    *,
    exigir_completos: bool = True,
) -> list[str]:
    """Valida responsabilidades cadastrais do DNA; ordem não pertence aqui."""
    erros: list[str] = []
    vistos_tema: set[str] = set()

    for n, row in enumerate(rows, start=1):
        tema = str(row.get("tema", "")).strip()
        ativo = str(row.get("ativo", "")).strip().upper()
        chave = _normaliza_tema(tema)

        if exigir_completos:
            obrigatorios = (
                "tema", "ativo", "banco_tematico",
                "versos", "verbetes_no_texto", "verbetes_do_tema",
                "total_de_itimos", "qtd_de_variacoes", "qtd_cientifica",
            )
            vazios = [
                campo
                for campo in obrigatorios
                if not str(row.get(campo, "")).strip()
            ]
            if vazios:
                erros.append(
                    f"{tema or '#'+str(n)}: campo(s) obrigatório(s) vazio(s): "
                    + ", ".join(vazios)
                )

        if not tema:
            erros.append(f"registro {n}: tema vazio")
        elif chave in vistos_tema:
            erros.append(f"tema duplicado: {tema}")
        vistos_tema.add(chave)


        if ativo and ativo not in DNA_STATUS:
            erros.append(f"{tema}: ativo inválido {ativo!r}; use N/T/S")

    return erros


def get_registro(
    tema: str,
    base_dir: str | Path = "./base",
) -> dict[str, str]:
    """Retorna o cadastro de um tema; {} quando não encontrado."""
    alvo = _normaliza_tema(tema)
    for row in ler(base_dir):
        if _normaliza_tema(row.get("tema", "")) == alvo:
            return row
    return {}


def get_banco_tema(
    tema: str,
    base_dir: str | Path = "./base",
    *,
    include_testes: bool = True,
) -> str:
    """Retorna exclusivamente do DNA o banco temático associado ao tema."""
    row = get_registro(tema, base_dir)
    if not row:
        return ""

    ativo = str(row.get("ativo", "")).strip().upper()
    permitidos = {"S", "T"} if include_testes else {"S"}
    if ativo not in permitidos:
        return ""

    return str(row.get("banco_tematico", "")).strip()


def _status_visivel(include_testes: bool) -> set[str]:
    return {"S", "T"} if include_testes else {"S"}


def _rol_path(livro: str, base_dir: str | Path) -> Path:
    nome = str(livro or "").strip()
    base = Path(base_dir)

    if nome.casefold() == "estudo":
        return base / "rol_estudos.txt"

    return base / f"rol_{nome}.txt"


def _nome_fisico_tema(tema: str, base_dir: str | Path = "./base") -> str:
    """Resolve a KEY no ./data e devolve a grafia física/autoral do .ypo."""
    wanted = _normaliza_tema(tema)
    if not wanted:
        return ""
    data_dir = Path(base_dir).resolve().parent / "data"
    if data_dir.is_dir():
        for path in data_dir.iterdir():
            if path.is_file() and path.suffix.casefold() == ".ypo" and _normaliza_tema(path.stem) == wanted:
                return path.stem
    return str(tema or "").strip()


def get_temas_livro(
    livro: str,
    base_dir: str | Path = "./base",
    *,
    include_testes: bool = True,
) -> list[str]:
    """Entrega temas na ordem do rol; DNA apenas valida cadastro/status."""
    rol = _rol_path(livro, base_dir)
    if not rol.is_file():
        return []

    permitidos = _status_visivel(include_testes)
    cadastro = {
        _normaliza_tema(row.get("tema", "")): row
        for row in ler(base_dir)
    }

    result: list[str] = []
    vistos: set[str] = set()

    for nome in _read_simple_list(rol):
        chave = _normaliza_tema(nome)
        if not chave or chave in vistos:
            continue

        row = cadastro.get(chave)
        if not row:
            continue

        if str(row.get("ativo", "")).strip().upper() not in permitidos:
            continue

        tema = _nome_fisico_tema(str(row.get("tema", "")).strip(), base_dir)
        if tema:
            result.append(tema)
            vistos.add(chave)

    return result


def mapa_bancos(
    base_dir: str | Path = "./base",
    *,
    include_testes: bool = True,
) -> dict[str, str]:
    permitidos = _status_visivel(include_testes)
    out: dict[str, str] = {}

    for row in ler(base_dir):
        if str(row.get("ativo", "")).strip().upper() not in permitidos:
            continue
        tema = str(row.get("tema", "")).strip()
        banco = str(row.get("banco_tematico", "")).strip()
        if tema and banco:
            out[tema.casefold()] = banco

    return out


def bancos(
    base_dir: str | Path = "./base",
    *,
    include_testes: bool = True,
) -> list[str]:
    valores = {
        v
        for v in mapa_bancos(base_dir, include_testes=include_testes).values()
        if v
    }
    return sorted(valores, key=str.casefold)


def linhas_images_compat(
    base_dir: str | Path = "./base",
    *,
    include_testes: bool = True,
) -> list[str]:
    """Compatibilidade transitória sem devolver autoridade a images.txt."""
    mapa = mapa_bancos(base_dir, include_testes=include_testes)
    return [
        f"{row['tema']} : {mapa[row['tema'].casefold()]}\n"
        for row in ler(base_dir)
        if row.get("tema", "").casefold() in mapa
    ]


__all__ = [
    "DNAError",
    "DNA_HEADER",
    "DNA_STATUS",
    "DNA_DEFAULTS_NOVO_TEMA",
    "dna_path",
    "ler",
    "validar",
    "get_registro",
    "get_banco_tema",
    "get_temas_livro",
    "mapa_bancos",
    "bancos",
    "linhas_images_compat",
]
