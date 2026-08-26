# akros_motor.py
# AKROS — versão Poético da aparição ACROS
#
# O motor histórico lay_2_ypo não é alterado.
# Cada letra escolhe RANDOM um verbete da mesma inicial;
# o verbete escolhido oferece de 3 a 6 frases e uma delas é sorteada.

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random
import unicodedata


class AkrosError(Exception):
    """Erro base do AKROS."""


class AkrosFonteAusenteError(AkrosError):
    """A fonte AKROS pedida não existe."""


class AkrosFonteFormatoError(AkrosError):
    """A fonte AKROS não obedece ao formato esperado."""


class AkrosEntradaVaziaError(AkrosError):
    """Nenhuma sequência foi informada pelo leitor."""


@dataclass(frozen=True)
class AkrosRegistro:
    verbete: str
    frases: tuple[str, ...]


@dataclass(frozen=True)
class AkrosLinha:
    entrada: str
    verbete: str | None
    markdown: str


@dataclass(frozen=True)
class AkrosResultado:
    entrada: str
    modo: str
    genero: str
    fonte: str
    linhas: tuple[AkrosLinha, ...]

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
                saida.append(linha.entrada.upper() + linha.verbete[1:])
        return "\n".join(saida)


_MODO = {"BEM": "bem", "MAL": "mal", "NEM TANTO": "mix", "NEM_TANTO": "mix"}
_GENERO = {"M": "M", "MASCULINO": "M", "F": "F", "FEMININO": "F", "MIX": "Mix"}


def _sem_acento(texto: str) -> str:
    decomposed = unicodedata.normalize("NFD", str(texto or ""))
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def _chave_letra(ch: str) -> str:
    return _sem_acento(ch).upper()[:1]


def _normaliza_modo(modo: str) -> str:
    key = str(modo or "").strip().upper()
    if key not in _MODO:
        raise AkrosError("Modo inválido. Use Bem, Mal ou nem tanto.")
    return _MODO[key]


def _normaliza_genero(genero: str) -> str:
    key = str(genero or "").strip().upper()
    if key not in _GENERO:
        raise AkrosError("Gênero inválido. Use Masculino, Feminino ou Mix.")
    return _GENERO[key]


def nome_fonte(modo: str, genero: str) -> str:
    m = _normaliza_modo(modo)
    g = _normaliza_genero(genero)
    if m == "mix" or g == "Mix":
        return "Akros_Mix.TXT"
    return f"akros_{m}_{g}.txt"


def localizar_fonte(base_dir: str | Path, modo: str, genero: str) -> Path:
    pasta = Path(base_dir)
    esperado = nome_fonte(modo, genero)
    direto = pasta / esperado
    if direto.is_file():
        return direto
    if pasta.is_dir():
        alvo = esperado.casefold()
        for item in pasta.iterdir():
            if item.is_file() and item.name.casefold() == alvo:
                return item
    raise AkrosFonteAusenteError(
        "AKROS não encontrou a fonte.\n"
        f"pasta: {pasta.resolve()}\n"
        f"procurado: {esperado}"
    )


def carregar_registros(path: str | Path) -> tuple[AkrosRegistro, ...]:
    fonte = Path(path)
    registros: list[AkrosRegistro] = []
    try:
        conteudo = fonte.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise AkrosError(
            "AKROS não pôde abrir a fonte.\n"
            f"arquivo: {fonte.name}\n"
            f"caminho: {fonte.resolve()}\n"
            f"detalhe: {exc}"
        ) from exc

    for numero, raw in enumerate(conteudo.splitlines(), start=1):
        if not raw.strip():
            continue
        partes = raw.split("|")
        if partes and not partes[0].strip():
            partes = partes[1:]
        if partes and not partes[-1].strip():
            partes = partes[:-1]
        partes = [parte.strip() for parte in partes]
        if not partes or not partes[0]:
            raise AkrosFonteFormatoError(
                f"AKROS — verbete ausente na linha {numero}: {fonte.name}"
            )
        verbete = partes[0]
        frases = tuple(frase for frase in partes[1:] if frase)
        if not 3 <= len(frases) <= 6:
            raise AkrosFonteFormatoError(
                "AKROS — fonte fora do padrão.\n"
                f"arquivo: {fonte.name}\n"
                f"linha: {numero}\n"
                f"frases encontradas: {len(frases)} (esperado: 3 a 6)"
            )
        registros.append(AkrosRegistro(verbete=verbete, frases=frases))

    return tuple(registros)


def indexar_por_letra(registros: tuple[AkrosRegistro, ...]) -> dict[str, tuple[AkrosRegistro, ...]]:
    indice: dict[str, list[AkrosRegistro]] = {}
    for registro in registros:
        chave = _chave_letra(registro.verbete[:1])
        if chave:
            indice.setdefault(chave, []).append(registro)
    return {chave: tuple(itens) for chave, itens in indice.items()}


def _mensagem_sem_verbete(ch: str) -> str:
    return f'Nenhum verbete digno na Machina para a letra "{ch}".'


def gerar_akros(
    entrada: str,
    modo: str = "Bem",
    genero: str = "Masculino",
    base_dir: str | Path = "./data/acros",
    rng: random.Random | None = None,
) -> AkrosResultado:
    texto = str(entrada or "")
    if not texto:
        raise AkrosEntradaVaziaError("Informe uma sequência para o AKROS.")

    fonte = localizar_fonte(base_dir, modo, genero)
    registros = carregar_registros(fonte)
    indice = indexar_por_letra(registros)
    sorteio = rng if rng is not None else random.Random()

    usados: set[str] = set()
    linhas: list[AkrosLinha] = []

    for ch in texto:
        chave = _chave_letra(ch)
        if not chave.isalpha():
            linhas.append(AkrosLinha(entrada=ch, verbete=None, markdown=ch))
            continue

        candidatos = [
            registro for registro in indice.get(chave, ())
            if registro.verbete.casefold() not in usados
        ]
        if not candidatos:
            linhas.append(AkrosLinha(
                entrada=ch,
                verbete=None,
                markdown=_mensagem_sem_verbete(ch),
            ))
            continue

        escolhido = sorteio.choice(candidatos)
        usados.add(escolhido.verbete.casefold())
        frase = sorteio.choice(escolhido.frases)
        linha_poetica = escolhido.verbete + ": " + frase
        linhas.append(AkrosLinha(
            entrada=ch,
            verbete=linha_poetica,
            markdown=f"**{ch.upper()}**{linha_poetica[1:]}",
        ))

    return AkrosResultado(
        entrada=texto,
        modo=_normaliza_modo(modo),
        genero=_normaliza_genero(genero),
        fonte=str(fonte),
        linhas=tuple(linhas),
    )


__all__ = [
    "AkrosError",
    "AkrosFonteAusenteError",
    "AkrosFonteFormatoError",
    "AkrosEntradaVaziaError",
    "AkrosRegistro",
    "AkrosLinha",
    "AkrosResultado",
    "nome_fonte",
    "localizar_fonte",
    "carregar_registros",
    "indexar_por_letra",
    "gerar_akros",
]
