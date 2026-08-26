"""Estrutura canônica dos arquivos .ypo da Machina.

ÚNICA autoridade para:
- reconhecer comandos estruturais;
- validar registros de conteúdo;
- separar Header / corpo / <EOF> / rodapé;
- expor os ítimos sem destruir NULL;
- diagnosticar com motivo e linha exatos.

Este módulo não conhece Streamlit, Builders, DNA ou poesia.
Ele não altera conteúdo autoral. A correção de fronteira, quando
explicitamente autorizada, exige callback de backup fornecido pelo chamador.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Callable


@dataclass(frozen=True)
class YpoRecord:
    raw: str
    fields: tuple[str, ...]
    line_number: int | None = None

    @property
    def is_blank_command(self) -> bool:
        return len(self.fields) == 4 and self.fields[2] == "00"

    @property
    def is_spacing_command(self) -> bool:
        return re.fullmatch(r"\|\$+\|", self.raw) is not None

    @property
    def is_content(self) -> bool:
        return not self.is_blank_command and not self.is_spacing_command

    @property
    def line_id(self) -> str:
        return self.fields[1].strip() if len(self.fields) > 1 else ""

    @property
    def idea_id(self) -> str:
        return self.fields[2].strip() if len(self.fields) > 2 else ""

    @property
    def source(self) -> str:
        return self.fields[3].strip() if len(self.fields) > 3 else ""

    @property
    def random_mode(self) -> str:
        return self.fields[4].strip() if len(self.fields) > 4 else ""

    @property
    def declared_total(self) -> int:
        if not self.is_content:
            raise ValueError(f"comando estrutural não possui quantidade: {self.raw}")
        try:
            value = int(self.fields[5].strip())
        except (ValueError, TypeError, IndexError) as exc:
            raise ValueError(f"quantidade de ítimos inválida: {self.raw}") from exc
        if value < 0:
            raise ValueError(f"quantidade de ítimos negativa: {self.raw}")
        return value

    @property
    def current_index(self) -> int:
        if not self.is_content:
            raise ValueError(f"comando estrutural não possui itimos_atual: {self.raw}")
        try:
            return int(self.fields[6].strip())
        except (ValueError, TypeError, IndexError) as exc:
            raise ValueError(f"itimos_atual inválido: {self.raw}") from exc

    @property
    def itimos(self) -> tuple[str, ...]:
        if not self.is_content:
            return tuple()
        return tuple(payload_itimos(self.fields))


@dataclass(frozen=True)
class YpoDocument:
    path: str
    header_lines: tuple[str, ...]
    body_lines: tuple[str, ...]
    footer_lines: tuple[str, ...]
    newline: str
    body_start_line: int

    @property
    def records(self) -> tuple[YpoRecord, ...]:
        return tuple(
            parse_record(
                line,
                self.path,
                line_number=self.body_start_line + offset,
            )
            for offset, line in enumerate(self.body_lines)
        )


def _prefix(line_number: int | None) -> str:
    return f"linha {line_number}: " if line_number is not None else ""


def is_spacing_line(raw: str) -> bool:
    """Qualquer | + N sinais de $ + | é comando estrutural válido, N>=1."""
    return re.fullmatch(r"\|\$+\|", str(raw or "")) is not None


def is_blank_fields(fields) -> bool:
    """|NN|00| é comando estrutural válido de linha em branco."""
    try:
        return len(fields) == 4 and str(fields[2]).strip() == "00"
    except Exception:
        return False


def payload_itimos(fields) -> list[str]:
    """Ítimos reais: preserva NULL e remove só o marcador estrutural $ x N."""
    fields = list(fields)
    if len(fields) < 9:
        return []
    payload = list(fields[7:-1])
    if payload and re.fullmatch(r"\$+", payload[0] or ""):
        payload = payload[1:]
    # NÃO filtrar "". O vazio entre pipes é ítimo NULL válido.
    return payload


def parse_record(
    line: str,
    path: str | Path = "",
    *,
    line_number: int | None = None,
) -> YpoRecord:
    """Valida uma linha do corpo e devolve diagnóstico específico."""
    raw = str(line).rstrip("\r\n")
    prefix = _prefix(line_number)
    where = f" [{path}]" if str(path) else ""

    if not raw.startswith("|"):
        raise ValueError(
            f"{prefix}registro não inicia com '|': {raw!r}{where}"
        )
    if not raw.endswith("|"):
        raise ValueError(
            f"{prefix}registro sem pipe final '|': {raw!r}{where}"
        )

    fields = tuple(raw.split("|"))

    # Comando estrutural compacto: |$|, |$$|, ... qualquer N>=1.
    if is_spacing_line(raw):
        return YpoRecord(raw=raw, fields=fields, line_number=line_number)

    # Comando estrutural de linha em branco: |NN|00|
    if is_blank_fields(fields):
        return YpoRecord(raw=raw, fields=fields, line_number=line_number)

    # Registro de conteúdo:
    # |linha|ideia|fonte|T/F/K|qtd_itimos|itimos_atual|ítimo...|
    if len(fields) < 9:
        internos = max(0, len(fields) - 2)
        raise ValueError(
            f"{prefix}estrutura não reconhecida: {internos} campo(s) interno(s); "
            "esperado |NN|00|, |$...$| ou "
            "|linha|ideia|fonte|T/F/K|qtd_itimos|itimos_atual|ítimo...|; "
            f"conteúdo={raw!r}{where}"
        )

    mode = fields[4].strip()
    if mode not in {"T", "F", "K"}:
        raise ValueError(
            f"{prefix}modo T/F/K inválido: {mode!r}; conteúdo={raw!r}{where}"
        )

    try:
        declared = int(fields[5].strip())
    except (ValueError, TypeError, IndexError) as exc:
        valor = fields[5] if len(fields) > 5 else ""
        raise ValueError(
            f"{prefix}quantidade de ítimos inválida: {valor!r}; "
            f"conteúdo={raw!r}{where}"
        ) from exc
    if declared < 0:
        raise ValueError(
            f"{prefix}quantidade de ítimos negativa: {declared}; "
            f"conteúdo={raw!r}{where}"
        )

    try:
        int(fields[6].strip())
    except (ValueError, TypeError, IndexError) as exc:
        valor = fields[6] if len(fields) > 6 else ""
        raise ValueError(
            f"{prefix}itimos_atual inválido: {valor!r}; "
            f"conteúdo={raw!r}{where}"
        ) from exc

    return YpoRecord(raw=raw, fields=fields, line_number=line_number)


def _read_text(path: str | Path) -> tuple[str, str, list[str]]:
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"UTF-8 inválido em {path}: byte/posição {exc.start}"
        ) from exc
    newline = "\r\n" if "\r\n" in text else "\n"
    return text, newline, text.splitlines()


def validate_boundary(
    path: str | Path,
    corrigir: bool = False,
    *,
    backup_callback: Callable[[str | Path], object] | None = None,
) -> int:
    """Valida a fronteira corpo/<EOF>; nunca corrige sem backup explícito."""
    path = Path(path)
    text, newline, lines = _read_text(path)

    eof_positions = [
        i for i, line in enumerate(lines)
        if line.strip() == "<EOF>"
    ]
    if not eof_positions:
        if not corrigir:
            raise ValueError(f"<EOF> ausente: {path}")
        if backup_callback is None:
            raise RuntimeError(
                "correção de <EOF> bloqueada: callback de backup obrigatório"
            )
        # Regra autoral do Atelier: quando <EOF> falta, inseri-lo
        # imediatamente após o último registro completo delimitado por pipes.
        last_record = None
        for index in range(len(lines) - 1, -1, -1):
            line = lines[index]
            if line.startswith("|") and line.endswith("|"):
                last_record = index
                break
        if last_record is None:
            raise ValueError(
                f"<EOF> ausente e nenhum registro completo terminado em '|' foi encontrado: {path}"
            )
        backup_callback(path)
        new_lines = lines[:last_record + 1] + ["<EOF>"] + lines[last_record + 1:]
        new_text = newline.join(new_lines)
        if text.endswith(("\n", "\r")):
            new_text += newline
        path.write_text(new_text, encoding="utf-8", newline="")
        return 1
    if len(eof_positions) > 1:
        numeros = ", ".join(str(i + 1) for i in eof_positions)
        raise ValueError(
            f"<EOF> duplicado em {path}; linhas: {numeros}"
        )

    eof_index = eof_positions[0]
    # Fronteira não interpreta a estrutura interna do registro.
    # Basta localizar a última linha que se apresenta como registro (inicia por |).
    # Se ela própria estiver malformada, parse_record dará o diagnóstico exato.
    last_record = None
    for index in range(eof_index - 1, -1, -1):
        line = lines[index]
        if line.startswith("|"):
            last_record = index
            break

    # Sem nenhuma linha iniciada por |, deixamos read_document/parse_record
    # diagnosticar a primeira linha real do corpo com precisão.
    if last_record is None:
        return 0

    if last_record + 1 == eof_index:
        return 0

    between = lines[last_record + 1:eof_index]
    first_number = last_record + 2
    first_text = between[0] if between else ""

    if not corrigir:
        raise ValueError(
            f"linha {first_number}: conteúdo entre o último registro e <EOF>: "
            f"{first_text!r} [{path}]"
        )

    if backup_callback is None:
        raise RuntimeError(
            "correção de fronteira bloqueada: callback de backup obrigatório"
        )

    backup_callback(path)
    new_lines = lines[:last_record + 1] + lines[eof_index:]
    new_text = newline.join(new_lines)
    if text.endswith(("\n", "\r")):
        new_text += newline
    path.write_text(new_text, encoding="utf-8", newline="")

    # CAE local da própria correção.
    _, _, confirmed = _read_text(path)
    confirmed_eof = [
        i for i, line in enumerate(confirmed)
        if line.strip() == "<EOF>"
    ]
    if len(confirmed_eof) != 1:
        raise RuntimeError(f"correção da fronteira falhou: {path}")
    pos = confirmed_eof[0]
    if pos < 1 or not confirmed[pos - 1].startswith("|"):
        raise RuntimeError(
            f"fronteira continua inválida após correção: {path}"
        )
    return len(between)


def read_document(
    path: str | Path,
    corrigir_fronteira: bool = False,
    *,
    backup_callback: Callable[[str | Path], object] | None = None,
) -> YpoDocument:
    """Lê Header, corpo e rodapé e valida TODO o corpo pela regra única."""
    path = Path(path)
    validate_boundary(
        path,
        corrigir=bool(corrigir_fronteira),
        backup_callback=backup_callback,
    )

    _, newline, lines = _read_text(path)
    if not lines:
        raise ValueError(f".ypo vazio: {path}")

    eof_index = next(
        i for i, line in enumerate(lines)
        if line.strip() == "<EOF>"
    )

    header_end = 0
    while header_end < eof_index and lines[header_end].startswith("*"):
        header_end += 1

    if header_end == 0:
        raise ValueError(f"Header ausente ou inválido: {path}")

    header = tuple(lines[:header_end])
    body = tuple(lines[header_end:eof_index])
    footer = tuple(lines[eof_index + 1:])

    if not body:
        raise ValueError(f"corpo .ypo vazio: {path}")

    body_start_line = header_end + 1
    for offset, line in enumerate(body):
        parse_record(
            line,
            path,
            line_number=body_start_line + offset,
        )

    return YpoDocument(
        path=str(path),
        header_lines=header,
        body_lines=body,
        footer_lines=footer,
        newline=newline,
        body_start_line=body_start_line,
    )


def read_records(
    path: str | Path,
    *,
    include_spacing: bool = True,
) -> list[YpoRecord]:
    """Todos os registros válidos; opcionalmente omite apenas |$...$|."""
    records = list(read_document(path).records)
    if include_spacing:
        return records
    return [record for record in records if not record.is_spacing_command]


__all__ = [
    "YpoRecord",
    "YpoDocument",
    "is_spacing_line",
    "is_blank_fields",
    "payload_itimos",
    "parse_record",
    "validate_boundary",
    "read_document",
    "read_records",
]
