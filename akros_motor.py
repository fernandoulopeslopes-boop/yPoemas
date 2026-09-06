# akros_motor.py — ARKOS / leitura Poético
# Cada letra escolhe RANDOM um verbete da mesma inicial e uma frase da fonte.

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import random
import unicodedata

class AkrosError(Exception):
    """Erro base da leitura Poético."""

class AkrosFonteAusenteError(AkrosError):
    """A fonte Poético pedida não existe."""

class AkrosFonteFormatoError(AkrosError):
    """A fonte Poético não obedece ao formato esperado."""

class AkrosEntradaVaziaError(AkrosError):
    """Nenhuma sequência foi informada pelo visitante."""

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

_GENERO = {"M": "M", "MASCULINO": "M", "F": "F", "FEMININO": "F"}

def _sem_acento(texto: str) -> str:
    decomposed = unicodedata.normalize("NFD", str(texto or ""))
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")

def _chave_letra(ch: str) -> str:
    return _sem_acento(ch).upper()[:1]

def _normaliza_genero(genero: str) -> str:
    key = str(genero or "").strip().upper()
    if key not in _GENERO:
        raise AkrosError("Gênero inválido. Use Masculino ou Feminino.")
    return _GENERO[key]

def nome_fonte(genero: str) -> str:
    return f"akros_bem_{_normaliza_genero(genero)}.txt"

def localizar_fonte(base_dir: str | Path, genero: str) -> Path:
    pasta = Path(base_dir)
    esperado = nome_fonte(genero)
    direto = pasta / esperado
    if direto.is_file():
        return direto
    if pasta.is_dir():
        alvo = esperado.casefold()
        for item in pasta.iterdir():
            if item.is_file() and item.name.casefold() == alvo:
                return item
    raise AkrosFonteAusenteError(
        "ARKOS não encontrou a fonte Poético.\n"
        f"pasta: {pasta.resolve()}\nprocurado: {esperado}"
    )

def carregar_registros(path: str | Path) -> tuple[AkrosRegistro, ...]:
    fonte = Path(path)
    registros: list[AkrosRegistro] = []
    try:
        conteudo = fonte.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise AkrosError(f"ARKOS não pôde abrir a fonte: {fonte.name}: {exc}") from exc

    for numero, raw in enumerate(conteudo.splitlines(), start=1):
        if not raw.strip():
            continue
        partes = raw.split("|")
        if partes and not partes[0].strip(): partes = partes[1:]
        if partes and not partes[-1].strip(): partes = partes[:-1]
        partes = [parte.strip() for parte in partes]
        if not partes or not partes[0]:
            raise AkrosFonteFormatoError(f"ARKOS — verbete ausente na linha {numero}: {fonte.name}")
        verbete = partes[0]
        frases = tuple(frase for frase in partes[1:] if frase)
        if not 3 <= len(frases) <= 6:
            raise AkrosFonteFormatoError(
                "ARKOS — fonte fora do padrão.\n"
                f"arquivo: {fonte.name}\nlinha: {numero}\n"
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
    return f'Nenhum verbete digno da sua entrada para a letra "{ch}".'

def gerar_akros(
    entrada: str,
    genero: str = "Masculino",
    base_dir: str | Path = "./data",
    rng: random.Random | None = None,
) -> AkrosResultado:
    texto = str(entrada or "")
    if not texto:
        raise AkrosEntradaVaziaError("Informe um nome.")

    fonte = localizar_fonte(base_dir, genero)
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
        candidatos = [r for r in indice.get(chave, ()) if r.verbete.casefold() not in usados]
        if not candidatos:
            linhas.append(AkrosLinha(entrada=ch, verbete=None, markdown=_mensagem_sem_verbete(ch)))
            continue
        escolhido = sorteio.choice(candidatos)
        usados.add(escolhido.verbete.casefold())
        frase = sorteio.choice(escolhido.frases)
        linha_poetica = escolhido.verbete + " " + frase
        restante = linha_poetica[1:] if len(linha_poetica) > 1 else ""
        linhas.append(AkrosLinha(
            entrada=ch,
            verbete=linha_poetica,
            markdown=f"**{ch.upper()}** {restante}",
        ))

    return AkrosResultado(
        entrada=texto,
        genero=_normaliza_genero(genero),
        fonte=str(fonte),
        linhas=tuple(linhas),
    )

__all__ = [
    "AkrosError", "AkrosFonteAusenteError", "AkrosFonteFormatoError",
    "AkrosEntradaVaziaError", "AkrosRegistro", "AkrosLinha", "AkrosResultado",
    "nome_fonte", "localizar_fonte", "carregar_registros", "indexar_por_letra", "gerar_akros",
]
