# ARKOS 1.0 — ACROS SIMPLES — fontes: acros_bem_F.txt / acros_bem_M.txt
# acros.py — ARKOS / leitura Simples
# O código não cria verbetes. As listas TXT canônicas em data/acros são a autoridade.

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import random
import unicodedata

class AcrosError(Exception):
    """Erro base da leitura Simples."""

class AcrosFonteAusenteError(AcrosError):
    """A fonte TXT pedida não existe."""

class AcrosEntradaVaziaError(AcrosError):
    """Nenhuma sequência foi informada pelo visitante."""

@dataclass(frozen=True)
class AcrosLinha:
    entrada: str
    verbete: str | None
    markdown: str

@dataclass(frozen=True)
class AcrosResultado:
    entrada: str
    genero: str
    fonte: str
    linhas: tuple[AcrosLinha, ...]

    @property
    def markdown(self) -> str:
        return "\n\n".join(linha.markdown for linha in self.linhas)

    @property
    def texto(self) -> str:
        saida = []
        for linha in self.linhas:
            if linha.verbete is None:
                saida.append(linha.entrada)
            else:
                saida.append(linha.entrada + linha.verbete[1:])
        return "\n".join(saida)

_GENERO = {"M": "M", "MASCULINO": "M", "F": "F", "FEMININO": "F"}

def _sem_acento(texto: str) -> str:
    decomposed = unicodedata.normalize("NFD", str(texto or ""))
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")

def _chave_letra(ch: str) -> str:
    return _sem_acento(ch).upper()[:1]

def _normaliza_genero(genero: str) -> str:
    key = str(genero or "").strip().upper()
    if key not in _GENERO:
        raise AcrosError("Gênero inválido. Use Masculino ou Feminino.")
    return _GENERO[key]

def nome_fonte(genero: str) -> str:
    return f"acros_bem_{_normaliza_genero(genero)}.txt"

def localizar_fonte(base_dir: str | Path, genero: str) -> Path:
    pasta = Path(base_dir)

    # ARKOS passa a raiz /data; as fontes canônicas moram em /data/acros.
    pasta_acros = pasta / "acros"
    if pasta_acros.is_dir():
        pasta = pasta_acros

    esperado = nome_fonte(genero)
    direto = pasta / esperado
    if direto.is_file():
        return direto
    if pasta.is_dir():
        alvo = esperado.casefold()
        for item in pasta.iterdir():
            if item.is_file() and item.name.casefold() == alvo:
                return item
    raise AcrosFonteAusenteError(f"Fonte Simples não encontrada: {esperado}")

def carregar_verbetes(path: str | Path) -> tuple[str, ...]:
    fonte = Path(path)
    verbetes = []
    with fonte.open("r", encoding="utf-8-sig") as file:
        for raw in file:
            verbete = raw.rstrip("\r\n")
            if verbete.strip():
                verbetes.append(verbete.strip())
    return tuple(verbetes)

def indexar_por_letra(verbetes: tuple[str, ...]) -> dict[str, tuple[str, ...]]:
    indice: dict[str, list[str]] = {}
    for verbete in verbetes:
        if not verbete:
            continue
        chave = _chave_letra(verbete[0])
        if chave:
            indice.setdefault(chave, []).append(verbete)
    return {k: tuple(v) for k, v in indice.items()}

def _mensagem_sem_verbete(ch: str) -> str:
    return f'Nenhum verbete digno da sua entrada para a letra "{ch}".'

def _monta_markdown(ch_entrada: str, verbete: str) -> str:
    restante = verbete[1:] if len(verbete) > 1 else ""
    return f"**{ch_entrada}** {restante}"

def gerar_acros(
    entrada: str,
    genero: str = "Masculino",
    base_dir: str | Path = "./data",
    rng: random.Random | None = None,
) -> AcrosResultado:
    texto = str(entrada or "")
    if not texto:
        raise AcrosEntradaVaziaError("Informe um nome.")

    fonte = localizar_fonte(base_dir, genero)
    verbetes = carregar_verbetes(fonte)
    indice = indexar_por_letra(verbetes)
    sorteio = rng if rng is not None else random.Random()
    usados: set[str] = set()
    linhas: list[AcrosLinha] = []

    for ch in texto:
        chave = _chave_letra(ch)
        if not chave.isalpha():
            linhas.append(AcrosLinha(entrada=ch, verbete=None, markdown=ch))
            continue
        candidatos = [v for v in indice.get(chave, ()) if v.casefold() not in usados]
        if not candidatos:
            linhas.append(AcrosLinha(entrada=ch, verbete=None, markdown=_mensagem_sem_verbete(ch)))
            continue
        escolhido = sorteio.choice(candidatos)
        usados.add(escolhido.casefold())
        linhas.append(AcrosLinha(entrada=ch, verbete=escolhido, markdown=_monta_markdown(ch, escolhido)))

    return AcrosResultado(
        entrada=texto,
        genero=_normaliza_genero(genero),
        fonte=str(fonte),
        linhas=tuple(linhas),
    )

__all__ = [
    "AcrosError", "AcrosFonteAusenteError", "AcrosEntradaVaziaError",
    "AcrosLinha", "AcrosResultado", "nome_fonte", "localizar_fonte",
    "carregar_verbetes", "indexar_por_letra", "gerar_acros",
]
