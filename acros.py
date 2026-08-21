# acros.py
# ACROS — aparição da Machina
#
# O código não cria verbetes.
# As listas .txt mnemônicas são a autoridade.
# O módulo apenas consulta, sorteia, evita repetição e monta a saída.

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random
import unicodedata


class AcrosError(Exception):
    """Erro base do ACROS."""


class AcrosFonteAusenteError(AcrosError):
    """A fonte .txt pedida não existe."""


class AcrosFonteLeituraError(AcrosError):
    """A fonte foi localizada, mas não pôde ser lida."""


class AcrosEntradaVaziaError(AcrosError):
    """Nenhuma sequência foi informada pelo leitor."""


@dataclass(frozen=True)
class AcrosLinha:
    entrada: str
    verbete: str | None
    markdown: str


@dataclass(frozen=True)
class AcrosResultado:
    entrada: str
    modo: str
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


_MODO = {
    "BEM": "bem",
    "MAL": "mal",
}

_GENERO = {
    "M": "M",
    "MASCULINO": "M",
    "F": "F",
    "FEMININO": "F",
}


def _sem_acento(texto: str) -> str:
    """Normaliza apenas para busca; nunca altera a entrada exibida."""
    decomposed = unicodedata.normalize("NFD", str(texto or ""))
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def _chave_letra(ch: str) -> str:
    normal = _sem_acento(ch).upper()
    return normal[:1]


def _normaliza_modo(modo: str) -> str:
    key = str(modo or "").strip().upper()
    if key not in _MODO:
        raise AcrosError("Modo inválido. Use Bem ou Mal.")
    return _MODO[key]


def _normaliza_genero(genero: str) -> str:
    key = str(genero or "").strip().upper()
    if key not in _GENERO:
        raise AcrosError("Gênero inválido. Use Masculino ou Feminino.")
    return _GENERO[key]


def nome_fonte(modo: str, genero: str) -> str:
    """
    Nome canônico da fonte.

    O SPEC atual usa quatro fontes .txt mnemônicas:
    Bem/Mal x Feminino/Masculino.
    """
    m = _normaliza_modo(modo)
    g = _normaliza_genero(genero)
    return f"acros_{m}_{g}.txt"


def localizar_fonte(base_dir: str | Path, modo: str, genero: str) -> Path:
    """Localiza a fonte .txt mnemônica sem depender de caixa do nome do arquivo."""
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

    endereco = pasta.resolve()
    raise AcrosFonteAusenteError(
        "ACROS não encontrou a fonte.\n"
        f"arquivo: {esperado}\n"
        f"caminho esperado: {endereco / esperado}\n"
        f"pasta: {endereco}"
    )

def carregar_verbetes(path: str | Path) -> tuple[str, ...]:
    """
    Lê a fonte ACROS em UTF-8.

    Se a codificação histórica impedir a leitura, pede ao Builders a
    normalização canônica daquele arquivo, relê e segue. Reparo bem-sucedido
    não gera mensagem para o leitor.
    """
    fonte = Path(path).resolve()

    def _ler_utf8():
        verbetes = []
        with fonte.open("r", encoding="utf-8-sig") as file:
            for raw in file:
                verbete = raw.rstrip("\r\n")
                if verbete.strip():
                    verbetes.append(verbete.strip())
        return tuple(verbetes)

    try:
        return _ler_utf8()
    except UnicodeDecodeError as primeiro_erro:
        try:
            from builders import normalizar_utf8_arquivo
            normalizar_utf8_arquivo(fonte)
            return _ler_utf8()
        except Exception as reparo_erro:
            raise AcrosFonteLeituraError(
                "ERRO UTF-8 — ACROS não conseguiu reparar a fonte.\n"
                f"arquivo: {fonte.name}\n"
                f"caminho: {fonte}\n"
                f"posição: {primeiro_erro.start}\n"
                f"byte: 0x{primeiro_erro.object[primeiro_erro.start]:02x}\n"
                f"reparo: {type(reparo_erro).__name__}: {reparo_erro}"
            ) from reparo_erro
    except OSError as exc:
        raise AcrosFonteLeituraError(
            "ERRO DE LEITURA — ACROS não pôde abrir a fonte.\n"
            f"arquivo: {fonte.name}\n"
            f"caminho: {fonte}\n"
            f"detalhe: {exc}"
        ) from exc


def indexar_por_letra(verbetes: tuple[str, ...]) -> dict[str, tuple[str, ...]]:
    """Índice por primeira letra normalizada. Á procura em A, É em E etc."""
    indice: dict[str, list[str]] = {}

    for verbete in verbetes:
        if not verbete:
            continue
        chave = _chave_letra(verbete[0])
        if not chave:
            continue
        indice.setdefault(chave, []).append(verbete)

    return {k: tuple(v) for k, v in indice.items()}


def _mensagem_sem_verbete(ch: str) -> str:
    return f'Nenhum verbete digno da sua entrada para a letra "{ch}".'


def _monta_markdown(ch_entrada: str, verbete: str) -> str:
    """
    Mantém a letra realmente digitada pelo leitor e usa o restante
    do verbete sorteado.
    """
    restante = verbete[1:] if len(verbete) > 1 else ""
    return f"**{ch_entrada}**{restante}"


def gerar_acros(
    entrada: str,
    modo: str = "Bem",
    genero: str = "Feminino",
    base_dir: str | Path = "./data/acros",
    rng: random.Random | None = None,
) -> AcrosResultado:
    """
    Gera uma leitura acróstica.

    Regras:
    - entrada livre;
    - acentos são normalizados somente para a busca;
    - espaços, hífens e demais acidentes são preservados as-is;
    - escolha RANDOM;
    - verbetes já usados não são repetidos;
    - o código nunca cria verbetes;
    - se uma letra não puder ser atendida, usa a mensagem canônica.
    """
    texto = str(entrada or "")
    if not texto:
        raise AcrosEntradaVaziaError("Informe uma sequência para o ACROS.")

    fonte = localizar_fonte(base_dir, modo, genero)
    verbetes = carregar_verbetes(fonte)
    indice = indexar_por_letra(verbetes)
    sorteio = rng if rng is not None else random.Random()

    usados: set[str] = set()
    linhas: list[AcrosLinha] = []

    for ch in texto:
        chave = _chave_letra(ch)

        if not chave.isalpha():
            linhas.append(AcrosLinha(
                entrada=ch,
                verbete=None,
                markdown=ch,
            ))
            continue

        candidatos = [
            verbete
            for verbete in indice.get(chave, ())
            if verbete.casefold() not in usados
        ]

        if not candidatos:
            linhas.append(AcrosLinha(
                entrada=ch,
                verbete=None,
                markdown=_mensagem_sem_verbete(ch),
            ))
            continue

        escolhido = sorteio.choice(candidatos)
        usados.add(escolhido.casefold())

        linhas.append(AcrosLinha(
            entrada=ch,
            verbete=escolhido,
            markdown=_monta_markdown(ch, escolhido),
        ))

    return AcrosResultado(
        entrada=texto,
        modo=_normaliza_modo(modo),
        genero=_normaliza_genero(genero),
        fonte=str(fonte),
        linhas=tuple(linhas),
    )


__all__ = [
    "AcrosError",
    "AcrosFonteAusenteError",
    "AcrosFonteLeituraError",
    "AcrosEntradaVaziaError",
    "AcrosLinha",
    "AcrosResultado",
    "nome_fonte",
    "localizar_fonte",
    "carregar_verbetes",
    "indexar_por_letra",
    "gerar_acros",
]
