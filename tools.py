"""Tools — central local de ferramentas e garantias da Machina.


Carregado exclusivamente por ypo_tools.py. O executável público ypo_mobile.py
permanece independente deste módulo.
"""
import os
import re
import time
import random
import string
import unicodedata
import base64
import html
import io
import json
import csv
from dataclasses import dataclass
import builders
import streamlit as st
# Constantes próprias das ferramentas locais da Machina.
# Permanecem neste módulo para que novo_tema/update_tema não dependam
# de definições incidentais do arquivo hospedeiro.
BUILD_RIMAS_WORD_RE = re.compile(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", re.UNICODE)
BUILD_RIMAS_CLITIC_PRONOUNS = {
    "me", "te", "se", "nos", "vos",
    "o", "a", "os", "as",
    "lo", "la", "los", "las",
    "no", "na", "nas",
    "lhe", "lhes",
}
BUILD_RIMAS_WEAK_SUFFIXES = {
    "da", "de", "do",
    "me", "se", "te",
    "lhe", "nte",
}
BUILD_RIMAS_RICH_SUFFIXES = {
    "ão", "ões",
    "ais", "eis", "éis", "ois", "óis", "ous",
    "ado", "ada", "ido", "ida",
    "oso", "osa", "esa", "eza",
    "ante", "ente", "inte", "onte", "unto",
    "al", "el", "il", "ol", "ul",
}
BUILD_AMBIENTE_LEXICO = "--- Ambiente Léxico da Machina"
BUILD_INDEXY_FILE = "ABOUT_index.MD"
BUILD_ESCALA = [
    "mil", "milhões", "bilhões", "trilhões", "quatrilhões", "quintilhões",
    "sextilhões", "setilhões", "octilhões", "nonilhões", "decilhões",
    "undecilhões", "dodecilhões", "tredecilhões", "quatuordecilhões",
    "quindecilhões", "sedecilhões", "septendecilhões",
]
try:
    import make_ola_tools
except Exception:
    make_ola_tools = None

def _bind_host(host_globals):
    """Disponibiliza à página Tools as funções comuns da base ypo_mobile."""
    if not host_globals:
        return
    for name, value in host_globals.items():
        if not name.startswith("__"):
            globals()[name] = value
@dataclass(frozen=True)
class YpoRecord:
    raw: str
    fields: tuple

    @property
    def is_blank_command(self):
        return len(self.fields) == 4 and self.fields[2] == "00"

    @property
    def is_spacing_command(self):
        return re.fullmatch(r"\|\$+\|", self.raw) is not None

    @property
    def is_content(self):
        return not self.is_blank_command and not self.is_spacing_command

    @property
    def line_id(self):
        return self.fields[1].strip() if len(self.fields) > 1 else ""

    @property
    def idea_id(self):
        return self.fields[2].strip() if len(self.fields) > 2 else ""

    @property
    def source(self):
        return self.fields[3].strip() if len(self.fields) > 3 else ""

    @property
    def random_mode(self):
        return self.fields[4].strip() if len(self.fields) > 4 else ""

    @property
    def declared_total(self):
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
    def current_index(self):
        if not self.is_content:
            raise ValueError(f"comando estrutural não possui itimos_atual: {self.raw}")
        try:
            return int(self.fields[6].strip())
        except (ValueError, TypeError, IndexError) as exc:
            raise ValueError(f"itimos_atual inválido: {self.raw}") from exc

    @property
    def itimos(self):
        if not self.is_content:
            return tuple()
        payload = list(self.fields[7:-1])
        if payload and re.fullmatch(r"\$+", payload[0] or ""):
            payload = payload[1:]
        return tuple(payload)

@dataclass(frozen=True)

class YpoDocument:
    path: str
    header_lines: tuple
    body_lines: tuple
    footer_lines: tuple
    newline: str
    @property
    def records(self):
        return tuple(_tools_parse_record(line, self.path) for line in self.body_lines)

def _tools_parse_record(line, path=""):
    """Valida uma linha do bloco 2 sem reinterpretar o conteúdo autoral."""
    raw = str(line).rstrip("\r\n")
    if not raw.startswith("|") or not raw.endswith("|"):
        raise ValueError(f"registro .ypo sem pipes de borda em {path}: {raw}")
    fields = tuple(raw.split("|"))

    # Comandos estruturais válidos e independentes dos registros de conteúdo.
    if re.fullmatch(r"\|\$+\|", raw):
        return YpoRecord(raw=raw, fields=fields)
    if len(fields) == 4 and fields[2] == "00":
        return YpoRecord(raw=raw, fields=fields)

    # |linha|ideia|fonte|T/F/K|total|atual|ítimo...|
    if len(fields) < 9:
        raise ValueError(f"registro .ypo incompleto em {path}: {raw}")
    if fields[4] not in {"T", "F", "K"}:
        raise ValueError(f"modo T/F/K inválido em {path}: {raw}")
    record = YpoRecord(raw=raw, fields=fields)
    _ = record.declared_total
    _ = record.current_index
    return record


def _tools_validar_fronteira_ypo(path, corrigir=False):
    """Valida a fronteira canônica entre o corpo autoral e <EOF>.

    Regra: a linha imediatamente anterior a <EOF> deve ser o último registro
    do corpo e terminar em ``|``. Quando ``corrigir=True``, remove somente as
    linhas indevidas entre esse último registro e <EOF>, preservando Header,
    corpo autoral e todo o rodapé posterior a <EOF>.
    """
    with open(path, "r", encoding="utf-8", newline="") as file:
        texto = file.read()
    newline = "\r\n" if "\r\n" in texto else "\n"
    linhas = texto.splitlines()
    eof_positions = [i for i, linha in enumerate(linhas) if linha.strip() == "<EOF>"]
    if len(eof_positions) != 1:
        raise ValueError(f".ypo deve conter exatamente um <EOF>: {path}")
    eof_index = eof_positions[0]
    ultimo_registro = None
    for index in range(eof_index - 1, -1, -1):
        linha = linhas[index]
        if linha.startswith("|") and linha.endswith("|"):
            ultimo_registro = index
            break
    if ultimo_registro is None:
        raise ValueError(f"nenhum registro válido antes de <EOF>: {path}")
    if ultimo_registro + 1 == eof_index:
        return 0
    intervalo = linhas[ultimo_registro + 1:eof_index]
    if not corrigir:
        detalhe = intervalo[0] if intervalo else ""
        raise ValueError(
            f"fronteira inválida antes de <EOF> em {path}: {detalhe}"
        )
    novas_linhas = linhas[:ultimo_registro + 1] + linhas[eof_index:]
    novo_texto = newline.join(novas_linhas) + (newline if texto.endswith(("\n", "\r")) else "")
    _tools_backup_path(path)
    with open(path, "w", encoding="utf-8", newline="") as file:
        file.write(novo_texto)
    with open(path, "r", encoding="utf-8", newline="") as file:
        confirmado = file.read().splitlines()
    eof_confirmado = [i for i, linha in enumerate(confirmado) if linha.strip() == "<EOF>"]
    if len(eof_confirmado) != 1:
        raise ValueError(f"correção da fronteira falhou em {path}")
    pos = eof_confirmado[0]
    if pos < 1 or not confirmado[pos - 1].startswith("|") or not confirmado[pos - 1].endswith("|"):
        raise ValueError(f"fronteira continua inválida após correção em {path}")
    return len(intervalo)


def ypo_ler(path, corrigir_fronteira=False):
    """Separa e valida os três blocos canônicos do .ypo.

    Bloco 1: Header inicial, composto apenas por linhas iniciadas por '*'.
    Bloco 2: registros iniciados por '|', até a linha imediatamente anterior a <EOF>.
    Bloco 3: ficha técnica após <EOF>.
    """
    _tools_validar_fronteira_ypo(path, corrigir=bool(corrigir_fronteira))
    with open(path, "r", encoding="utf-8", newline="") as file:
        text = file.read()
    newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines()
    if not lines:
        raise ValueError(f".ypo vazio: {path}")
    eof_positions = [i for i, line in enumerate(lines) if line.strip() == "<EOF>"]
    if len(eof_positions) != 1:
        raise ValueError(f".ypo deve conter exatamente um <EOF>: {path}")
    eof_index = eof_positions[0]
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
    for line in body:
        if not line.startswith("|"):
            raise ValueError(f"linha estranha entre Header e <EOF> em {path}: {line}")
        _tools_parse_record(line, path)
    return YpoDocument(
        path=str(path),
        header_lines=header,
        body_lines=body,
        footer_lines=footer,
        newline=newline,
    )

def _tools_body_signature(document, ignore_current_index=False):
    """Assinatura do corpo; opcionalmente ignora apenas o campo itimos_atual."""
    normalized = []
    for record in document.records:
        fields = list(record.fields)
        if ignore_current_index and len(fields) > 6 and fields[2] != "00":
            fields[6] = "<ITIMOS_ATUAL>"
        normalized.append("|".join(fields))
    return "\n".join(normalized)

def ypo_validar_corpo_preservado(original, novo, permitir_itimos_atual=False):
    """Prova que nenhum Build alterou o corpo autoral.

    `permitir_itimos_atual=True` é reservado ao motor lay_2_ypo.py.
    """
    left = _tools_body_signature(original, ignore_current_index=permitir_itimos_atual)
    right = _tools_body_signature(novo, ignore_current_index=permitir_itimos_atual)
    if left != right:
        raise ValueError("bloco 2 alterado fora do contrato")

def _tools_compor_ypo(document, footer_lines):
    lines = list(document.header_lines)
    lines.extend(document.body_lines)
    lines.append("<EOF>")
    lines.extend(str(line).rstrip("\r\n") for line in footer_lines)
    return document.newline.join(lines) + document.newline

def _tools_write_ypo_certificado(path, original_document, novo_texto):
    """Grava .ypo só após validar candidato; restaura backup se a releitura falhar."""
    tmp_path = str(path) + ".tools.tmp"
    backup_path = ""
    with open(tmp_path, "w", encoding="utf-8", newline="") as file:
        file.write(novo_texto)
    try:
        candidate = ypo_ler(tmp_path, corrigir_fronteira=False)
        ypo_validar_corpo_preservado(original_document, candidate, permitir_itimos_atual=False)
        backup_path = _tools_backup_path(path)
        with open(tmp_path, "rb") as src, open(path, "wb") as dst:
            dst.write(src.read())
        persisted = ypo_ler(path, corrigir_fronteira=False)
        ypo_validar_corpo_preservado(original_document, persisted, permitir_itimos_atual=False)
    except Exception:
        if backup_path and os.path.exists(backup_path):
            with open(backup_path, "rb") as src, open(path, "wb") as dst:
                dst.write(src.read())
        raise
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def _tools_fmt_int(valor):
    return f"{int(valor):,}".replace(",", ".")

def _tools_potencia_nome(valor):
    num = f"{int(valor):,}"
    pontos = num.count(",") - 1
    if 0 <= pontos < len(BUILD_ESCALA):
        return BUILD_ESCALA[pontos]
    return "nonono"

def _tools_backup_path(path):
    """Cria backup local antes de qualquer gravação derivada/cadastral."""
    if not os.path.exists(path):
        return ""
    backup_dir = _project_path("backups", "local_tools")
    os.makedirs(backup_dir, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    base = os.path.basename(path)
    dst = os.path.join(backup_dir, f"{stamp}_{base}")
    with open(path, "rb") as src, open(dst, "wb") as out:
        out.write(src.read())
    return dst

def _tools_write_text(path, texto):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    _tools_backup_path(path)
    with open(path, "w", encoding="utf-8") as file:
        file.write(texto)

def _tools_add_unique_line(path, line, key):
    """Adiciona linha única sem criar linhas em branco incidentais."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    line = str(line).rstrip("\n")
    key = str(key).casefold().strip()
    linhas = []
    texto_atual = ""
    if os.path.exists(path):
        with open(path, encoding="utf-8-sig") as file:
            texto_atual = file.read()
        linhas = texto_atual.splitlines()
    for raw in linhas:
        raw_strip = raw.strip()
        if raw_strip.startswith("|"):
            campos = raw_strip.split("|")
            parte = campos[1].strip().casefold() if len(campos) > 1 else ""
        else:
            parte = raw_strip.partition(" : ")[0].strip().casefold()
        if parte == key or raw_strip.casefold() == key:
            return False
    _tools_backup_path(path)
    with open(path, "a", encoding="utf-8") as file:
        if texto_atual and not texto_atual.endswith(("\n", "\r")):
            file.write("\n")
        file.write(line + "\n")
    return True


def _tools_add_ativo_line(path, line, key, livro):
    """Inclui tema em ativos.txt preservando o bloco final canônico dos 24 signos."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    linhas = []
    if os.path.exists(path):
        with open(path, encoding="utf-8-sig") as file:
            linhas = file.read().splitlines()
    key_norm = str(key or "").strip().casefold()
    for raw in linhas:
        nome = raw.strip().partition(" : ")[0].strip().casefold()
        if nome == key_norm:
            return False

    nova = str(line).strip()
    if str(livro or "").strip() in {"signos_fem", "signos_mas"}:
        insert_at = len(linhas)
    else:
        nonblank_positions = [i for i, raw in enumerate(linhas) if raw.strip()]
        insert_at = nonblank_positions[-24] if len(nonblank_positions) >= 24 else len(linhas)
    linhas.insert(insert_at, nova)
    _tools_write_text(path, "\n".join(linhas).rstrip() + "\n")
    return True


def _tools_resolve_ypo_path(tema):
    """Resolve o arquivo sem rebatizar uma extensão informada pelo autor.

    Um nome sem extensão continua sob o contrato histórico ``tema -> tema.ypo``.
    Quando o nome já traz uma extensão (por exemplo ``Design.new``), essa
    assinatura é preservada integralmente e nunca vira ``Design.new.ypo``.
    """
    tema = str(tema or "").strip()
    nome = tema.replace("\\", "/").rsplit("/", 1)[-1]
    extensao_explicita = bool(os.path.splitext(nome)[1])

    if extensao_explicita:
        candidatos = [_project_path("data", nome)]
    else:
        candidatos = [
            _project_path("data", nome + ".ypo"),
            _project_path("data", nome + ".YPO"),
        ]

    for path in candidatos:
        if os.path.exists(path):
            return path

    # Windows não distingue caixa; este fallback conserva a mesma autoridade
    # também em ambientes case-sensitive usados no CAE/deploy.
    data_dir = _project_path("data")
    if os.path.isdir(data_dir):
        nomes_esperados = {os.path.basename(path).casefold() for path in candidatos}
        for existente in os.listdir(data_dir):
            if existente.casefold() in nomes_esperados:
                return os.path.join(data_dir, existente)

    return candidatos[0]


DNA_HEADER = [
    "codigo", "tema", "ativo", "ordem", "livro", "banco_tematico",
    "versos", "verbetes_no_texto", "verbetes_do_tema", "total_de_itimos",
    "qtd_de_variacoes", "qtd_cientifica",
]
DNA_LIVROS_PRINCIPAIS = [
    "livro vivo", "poemas", "jocosos", "ensaios", "variações",
    "metalinguagem", "sociais", "outros autores", "signos_fem", "signos_mas",
]


def _tools_dna_path():
    return _project_path("base", "DNA.TXT")


def _tools_dna_ler():
    path = _tools_dna_path()
    if not os.path.exists(path):
        return []
    header, rows = [], []
    with open(path, encoding="utf-8-sig") as f:
        for raw in f:
            line = raw.strip()
            if line == "<EOF>":
                break
            if not line.startswith("|"):
                continue
            fields = [x.strip() for x in line.split("|")[1:-1]]
            if not header:
                header = fields
            elif len(fields) == len(header):
                rows.append(dict(zip(header, fields)))
    return rows


def _tools_dna_registro(tema):
    alvo = str(tema or "").strip().casefold()
    for row in _tools_dna_ler():
        if str(row.get("tema", "")).strip().casefold() == alvo:
            return row
    return {}


def _tools_lista_simples(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig") as f:
        return [raw.strip() for raw in f if raw.strip()]


def _tools_mapa_pares(path):
    out = {}
    for raw in _tools_lista_simples(path):
        nome, sep, valor = raw.partition(" : ")
        if sep and nome.strip():
            out[nome.strip().casefold()] = valor.strip()
    return out




def _tools_livros_por_tema():
    out = {}
    for livro in DNA_LIVROS_PRINCIPAIS:
        path = _project_path("base", "rol_" + livro + ".txt")
        for tema in _tools_lista_simples(path):
            chave = tema.replace(" ", "").casefold()
            out.setdefault(chave, []).append(livro)
    return out


def _tools_dna_footer():
    return [
        "LEGENDA",
        "codigo = identificador interno e estável do tema.",
        "tema = nome autoral do tema.",
        "ativo = autorização de circulação no palco.",
        "ordem = posição canônica de circulação; preserva o bloco final dos 24 signos.",
        "livro = livro(s) da Machina ao qual o tema pertence.",
        "banco_tematico = banco visual associado ao tema.",
        "imagem = escolha RANDOM do banco_tematico; não integra o DNA.",
        "versos = quantidade de versos do yPoema.",
        "verbetes_no_texto = quantidade de verbetes no texto.",
        "verbetes_do_tema = quantidade total de verbetes disponíveis no tema.ypo.",
        "total_de_itimos = quantidade total de ítimos disponíveis no tema.ypo.",
        "qtd_de_variacoes = quantidade total de variações possíveis do tema.",
        "qtd_cientifica = quantidade de variações em notação científica.",
    ]



def _tools_temas_ativos():
    """Temas ativos vêm sempre da autoridade base/ativos.txt."""
    temas = []
    vistos = set()
    ativos_path = _project_path("base", "ativos.txt")
    if not os.path.exists(ativos_path):
        raise FileNotFoundError(f"autoridade de temas não encontrada: {ativos_path}")
    with open(ativos_path, encoding="utf-8-sig") as file:
        for raw in file:
            linha = raw.strip()
            if not linha:
                continue
            tema = linha.partition(" : ")[0].strip()
            chave = tema.casefold()
            if chave in vistos:
                raise ValueError(f"tema duplicado em ativos.txt: {tema}")
            vistos.add(chave)
            temas.append((tema, _tools_resolve_ypo_path(tema)))
    return temas


def _tools_temas_para_remover():
    """Lista temas em circulação, usando as mesmas listas vistas pelos yPoemas.

    A remoção precisa enxergar temas que aparecem em rol_*.txt mesmo que
    alguma lista cadastral esteja desencontrada.
    """
    nomes = []
    def add(nome):
        nome = str(nome or "").strip()
        if nome and nome not in nomes:
            nomes.append(nome)
    # 1) Lista canônica usada pelo livro "todos os temas" no palco.
    try:
        for nome in load_temas("todos os temas"):
            add(nome)
    except Exception:
        pass
    # 2) Todos os rol_*.txt, para capturar livros específicos.
    base_dir = _project_path("base")
    if os.path.isdir(base_dir):
        for file_name in sorted(os.listdir(base_dir)):
            if not (file_name.lower().startswith("rol_") and file_name.lower().endswith(".txt")):
                continue
            try:
                with open(os.path.join(base_dir, file_name), encoding="utf-8") as file:
                    for raw in file:
                        add(raw.replace(" ", "").strip())
            except Exception:
                pass
    # 3) Ativos, caso algum tema esteja cadastrado mas fora dos livros.
    try:
        for tema, path in _tools_temas_ativos():
            add(tema)
    except Exception:
        pass
    # 4) Arquivos em ./data, para permitir remover clone recém-criado mesmo
    #    quando as listas ficaram desencontradas.
    data_dir = _project_path("data")
    if os.path.isdir(data_dir):
        for file_name in sorted(os.listdir(data_dir), key=natural_keys):
            if file_name.lower().endswith(".ypo"):
                add(os.path.splitext(file_name)[0])
    return sorted(nomes, key=natural_keys)

def _tools_corrigir_quantidades_declaradas(path):
    """Reconcilia apenas o campo quantidade com os ítimos reais do próprio .ypo.

    O payload autoral é a autoridade. Nenhum ítimo, Header ou rodapé é alterado.
    """
    with open(path, "r", encoding="utf-8", newline="") as file:
        texto = file.read()
    newline = "\r\n" if "\r\n" in texto else "\n"
    linhas = texto.splitlines()
    alterou = False
    dentro_corpo = True
    saida = []
    for linha in linhas:
        if linha.strip() == "<EOF>":
            dentro_corpo = False
            saida.append(linha)
            continue
        if dentro_corpo and linha.startswith("|") and linha.endswith("|"):
            campos = linha.split("|")
            if len(campos) >= 8 and campos[2] != "00":
                real = len([item for item in campos[7:-1] if item != ""])
                try:
                    declarado = int(str(campos[5]).strip())
                except Exception:
                    declarado = None
                if declarado != real:
                    campos[5] = str(real)
                    linha = "|".join(campos)
                    alterou = True
        saida.append(linha)
    if alterou:
        _tools_write_text(path, newline.join(saida) + newline)
    return alterou


def _tools_linhas_ypo(path):
    """Entrega somente registros de conteúdo; comandos estruturais ficam preservados no documento."""
    document = ypo_ler(path, corrigir_fronteira=False)
    for record in document.records:
        if record.is_content:
            yield list(record.fields)


def _tools_payload_itimos(campos):
    """Ítimos reais: preserva NULL e remove somente o marcador estrutural $ x N."""
    if len(campos) < 9:
        return []
    payload = list(campos[7:-1])
    if payload and re.fullmatch(r"\$+", payload[0] or ""):
        payload = payload[1:]
    return payload


def _tools_qtd_itimos_declarada(campos):
    """Quantidade declarada; valor inválido é erro, nunca zero silencioso."""
    try:
        value = int(str(campos[5]).strip())
    except (ValueError, TypeError, IndexError) as exc:
        raise ValueError(f"quantidade de ítimos inválida: {campos}") from exc
    if value < 0:
        raise ValueError(f"quantidade de ítimos negativa: {campos}")
    return value

def _tools_normaliza_unico(texto):
    return re.sub(r"\s+", " ", str(texto or "").strip().casefold())

def _tools_palavras_de_itimo(itimo, minimo=1):
    """Separa verbetes, preservando formas hifenizadas como manda-se.

    A contagem técnica do tema aceita verbetes de qualquer tamanho.
    O Build_Léxico chama esta função com minimo=3, pois a Eureka só busca
    sementes com três ou mais letras.
    """
    texto = str(itimo or "").casefold()
    palavras = re.findall(r"[^\W_]+(?:-[^\W_]+)*", texto, flags=re.UNICODE)
    return [palavra for palavra in palavras if len(palavra) >= int(minimo)]

def _tools_calcular_variacoes_tema(path):
    fontes_list = []
    corrige_qtd = 1
    qtd_itimos_list = []
    for campos in _tools_linhas_ypo(path):
        if len(campos) >= 8:
            nova_fonte = campos[3]
            total_itimos = len(_tools_payload_itimos(campos))
            if nova_fonte not in fontes_list:
                fontes_list.append(nova_fonte)
                qtd_itimos_list.append(total_itimos)
            else:
                index = fontes_list.index(nova_fonte)
                saldo_itimos = qtd_itimos_list[index] - corrige_qtd
                if saldo_itimos == 0:
                    saldo_itimos = 1
                fontes_list.append(nova_fonte)
                qtd_itimos_list.append(saldo_itimos)
                corrige_qtd += 1
    qtd_variatio = 1
    for qtd in qtd_itimos_list:
        qtd_variatio = +(qtd_variatio * qtd)
    return abs(qtd_variatio)







def build_ficha_lexica():
    start_time = time.time()
    temas = _tools_temas_ativos()
    total_itimos = 0
    itimos_unicos = set()
    total_verbetes = 0
    verbetes_unicos = set()
    for tema, path in temas:
        if not os.path.exists(path):
            raise FileNotFoundError(f"{tema}: arquivo não encontrado ({path})")
        for campos in _tools_linhas_ypo(path):
            payload = _tools_payload_itimos(campos)
            total_itimos += len(payload)
            for itimo in payload:
                itimos_unicos.add(_tools_normaliza_unico(itimo))
                palavras = _tools_palavras_de_itimo(itimo, minimo=1)
                total_verbetes += len(palavras)
                verbetes_unicos.update(palavras)
    try:
        total_temas_ficha = len([tema for tema in load_temas("todos os temas") if str(tema).strip()])
    except Exception:
        total_temas_ficha = len(temas)
    bloco = (
        f"{BUILD_AMBIENTE_LEXICO}\n\n"
        f"Total de Verbetes: {_tools_fmt_int(total_verbetes)}\n"
        f"Total de Verbetes únicos: {_tools_fmt_int(len(verbetes_unicos))}\n\n"
        f"Total de Ítimos: {_tools_fmt_int(total_itimos)}\n"
        f"Total de Ítimos únicos: {_tools_fmt_int(len(itimos_unicos))}\n\n"
        f"Total de Temas: {_tools_fmt_int(total_temas_ficha)}\n"
    )
    md_dir = _project_path("md_files")
    index_path = os.path.join(md_dir, "INDEX.txt")
    texto = ""
    if os.path.exists(index_path):
        with open(index_path, encoding="utf-8") as file:
            texto = file.read()
    pos = texto.find(BUILD_AMBIENTE_LEXICO)
    if pos >= 0:
        texto = texto[:pos].rstrip() + "\n\n" + bloco
    else:
        texto = (texto.rstrip() + "\n\n" + bloco) if texto.strip() else bloco
    _tools_write_text(index_path, texto)
    return f"Ficha Léxica atualizada em {index_path}. Runtime: {time.time() - start_time:.2f}s\n\n{bloco}"


def _tools_imagem_tema(tema):
    # return _tools_imagem_tema_legacy(tema)  # <CHG>
    return str(_tools_dna_registro(tema).get("banco_tematico", "") or "").strip()


def _tools_dados_rodape_ypo(path):
    """Recalcula a Ficha Técnica diretamente do corpo atual do .ypo."""
    document = ypo_ler(path, corrigir_fronteira=False)
    verbetes_no_texto = 0
    total_itimos = 0
    verbetes_unicos = set()
    for record in document.records:
        if not record.is_content:
            continue
        campos = list(record.fields)
        verbetes_no_texto += 1
        payload = _tools_payload_itimos(campos)
        total_itimos += len(payload)
        for itimo in payload:
            verbetes_unicos.update(_tools_palavras_de_itimo(itimo, minimo=1))
    qtd_variacoes = _tools_calcular_variacoes_tema(path)
    return {
        "verbetes_no_texto": verbetes_no_texto,
        "total_itimos": total_itimos,
        "total_verbetes": len(verbetes_unicos),
        "qtd_variacoes": qtd_variacoes,
    }


def _tools_linhas_rodape_ypo(path):
    dados = _tools_dados_rodape_ypo(path)
    variacoes = dados["qtd_variacoes"]
    return [
        f"Verbetes no Texto = {dados['verbetes_no_texto']}",
        f"  Total de ítimos = {dados['total_itimos']}",
        f"Total de verbetes = {dados['total_verbetes']}",
        f"Qtd. de Variações = {_tools_fmt_int(variacoes)} ({_tools_potencia_nome(variacoes)})",
    ]


def _tools_eh_build_by(linha):
    chave = str(linha or "").strip().casefold()
    return chave.startswith("build_by") or chave.startswith("build by")


def _tools_normalizar_nota_rodape(linha):
    texto = str(linha or "").strip()
    if not texto:
        return ""
    for prefixo in ("#-", "*-", "# -", "* -"):
        if texto.startswith(prefixo):
            texto = texto[len(prefixo):].strip()
            break
    return "#- " + texto if texto else ""


def _tools_notas_apos_build_by(footer_lines):
    """Preserva somente a memória de oficina posterior ao último Build By."""
    build_idx = None
    for idx, linha in enumerate(footer_lines):
        if _tools_eh_build_by(linha):
            build_idx = idx
    if build_idx is None:
        return []
    notas = []
    for linha in footer_lines[build_idx + 1:]:
        nota = _tools_normalizar_nota_rodape(linha)
        if nota:
            notas.append(nota)
    return notas


def _tools_build_line_existente(footer_lines):
    for linha in reversed(footer_lines):
        if _tools_eh_build_by(linha):
            return str(linha).strip()
    return ""


def _tools_update_rodape_um_tema(tema, path):
    """Reconstrói a Ficha Técnica; Header e corpo ficam byte-a-byte em suas linhas."""
    document = ypo_ler(path, corrigir_fronteira=False)
    technical = _tools_linhas_rodape_ypo(path)
    build_line = _tools_build_line_existente(document.footer_lines)
    if not build_line:
        build_line = time.strftime("build_by update_rodape em %d/%m/%Y - %H:%M")
    notas = _tools_notas_apos_build_by(document.footer_lines)
    footer = technical + [build_line, ""] + notas
    novo_texto = _tools_compor_ypo(document, footer)
    atual = _tools_compor_ypo(document, document.footer_lines)
    if atual == novo_texto:
        return f"{tema}: sem alteração"
    _tools_write_ypo_certificado(path, document, novo_texto)
    return f"{tema}: Ficha Técnica atualizada"


def update_rodape(tema_unico=None):
    """Reescreve Ficha Técnica; faz PRE-FLIGHT de todos os temas antes da primeira gravação."""
    start_time = time.time()
    temas = _tools_temas_ativos()
    if tema_unico:
        tema_norm = str(tema_unico).strip().casefold()
        temas = [(tema, path) for tema, path in temas if tema.casefold() == tema_norm]
        if not temas:
            path = _tools_resolve_ypo_path(tema_unico)
            if os.path.exists(path):
                temas = [(str(tema_unico).strip(), path)]
            else:
                raise ValueError(f"update_rodape: tema não encontrado: {tema_unico}")

    # PRE-FLIGHT: nenhum .ypo é gravado enquanto houver um tema inválido.
    for tema, path in temas:
        if not os.path.exists(path):
            raise FileNotFoundError(f"{tema}: arquivo não encontrado ({path})")
        document = ypo_ler(path, corrigir_fronteira=False)
        _ = _tools_linhas_rodape_ypo(path)
        _ = _tools_notas_apos_build_by(document.footer_lines)

    resultados = [_tools_update_rodape_um_tema(tema, path) for tema, path in temas]
    try:
        st.cache_data.clear()
    except Exception:
        pass
    alvo = f"tema {tema_unico}" if tema_unico else "todos os temas"
    return f"update_rodape: {alvo}; {len(resultados)} tema(s). Runtime: {time.time() - start_time:.2f}s\n" + "\n".join(resultados)


def _tools_validar_quantidades_tema(path):
    """Confere real == declarado nos registros de conteúdo, sem alterar o .ypo."""
    document = ypo_ler(path, corrigir_fronteira=False)
    divergencias = []
    for record in document.records:
        if not record.is_content:
            continue
        campos = list(record.fields)
        declarado = _tools_qtd_itimos_declarada(campos)
        real = len(_tools_payload_itimos(campos))
        if real != declarado:
            linha_id = "|".join(campos[1:4])
            divergencias.append(f"{linha_id}: declarado={declarado}; real={real}")
    if divergencias:
        raise ValueError("quantidade de ítimos divergente; operação bloqueada:\n" + "\n".join(divergencias))
    return document


def _tools_natural_key(value):
    return [int(part) if part.isdigit() else part.casefold() for part in re.split(r"(\d+)", str(value))]


def _tools_add_unique_sorted_line(path, line, key=None):
    """Inclui uma linha única e mantém a ordem canônica da lista.

    Em rol_todos os temas.txt, a lista é formada por dois blocos:
    1) temas comuns em ordem alfabética;
    2) temas do Zodíaco (nomes terminados em =f ou =m) em ordem alfabética.
    
    A identificação do Zodíaco é estrutural pelo sufixo, sem depender de uma
    quantidade fixa nem do nome do signo. Assim Sagitari=f/m entra no bloco
    correto e qualquer grafia antiga não é corrigida silenciosamente.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    existentes = []
    if os.path.exists(path):
        with open(path, encoding="utf-8-sig") as file:
            existentes = [raw.strip() for raw in file if raw.strip()]

    original = list(existentes)
    chave = str(key if key is not None else line).strip().casefold()
    ja_existe = False
    for raw in existentes:
        raw_key = raw.partition(" : ")[0].strip().casefold()
        if raw_key == chave or raw.strip().casefold() == chave:
            ja_existe = True
            break

    if not ja_existe:
        existentes.append(str(line).strip())

    if os.path.basename(path).casefold() == "rol_todos os temas.txt":
        temas = []
        zodiacos = []
        for raw in existentes:
            nome = raw.partition(" : ")[0].strip()
            if re.search(r"=(?:f|m)$", nome, flags=re.IGNORECASE):
                zodiacos.append(raw)
            else:
                temas.append(raw)
        temas.sort(key=_tools_natural_key)
        zodiacos.sort(key=_tools_natural_key)
        ordenadas = temas + zodiacos
    else:
        ordenadas = sorted(existentes, key=_tools_natural_key)

    if ordenadas == original:
        return False

    _tools_write_text(path, "\n".join(ordenadas) + "\n")
    return True


TOOLS_BOOKS = [
    "livro vivo", "poemas", "jocosos", "ensaios", "variações",
    "metalinguagem", "sociais", "outros autores", "signos_fem", "signos_mas",
]


def _tools_bancos_tematicos():
    valores = {"Machina"}
    path = _project_path("base", "images.txt")
    if os.path.exists(path):
        with open(path, encoding="utf-8-sig") as file:
            for raw in file:
                _, sep, valor = raw.strip().partition(" : ")
                if sep and valor.strip():
                    valores.add(valor.strip())
    return sorted(valores, key=_tools_natural_key)


def _tools_resultado_falhou(resultado):
    texto = str(resultado or "").casefold()
    marcadores = (
        "não gravou", "erros:", " stop", "stop;", " falhou", "falha ",
        "problema(s) encontrado(s)", "arquivo não encontrado", "não encontrado:",
    )
    return any(m in texto for m in marcadores)


def _tools_executar(nome, func, *args):
    resultado = func(*args)
    if _tools_resultado_falhou(resultado):
        raise RuntimeError(f"{nome}: {resultado}")
    return str(resultado)


def _tools_tentar_derivado(nome, func, *args):
    """Novo/remove não são bloqueados por erro estrutural de OUTRO tema."""
    try:
        return _tools_executar(nome, func, *args)
    except Exception as exc:
        return f"PENDÊNCIA DERIVADA — {nome}: {exc}"


def update_tema(tema):
    """Valida um tema existente e atualiza derivados sem tocar no corpo .ypo."""
    tema = str(tema or "").strip()
    path = _tools_resolve_ypo_path(tema)
    if not tema or not os.path.exists(path):
        raise ValueError(f"update_tema: tema/arquivo não encontrado: {tema}")
    original = ypo_ler(path, corrigir_fronteira=False)
    _tools_validar_quantidades_tema(path)
    resultados = [f"update_tema: {tema} validado"]
    resultados.append(_tools_executar("Matrix", builders.build_matrix, tema))
    resultados.append(_tools_executar("Léxico", builders.build_lexico))
    resultados.append(_tools_executar("Indexy", builders.build_indexy))
    resultados.append(_tools_executar("DNA", builders.build_dna))
    resultados.append(update_rodape(tema))
    persistido = ypo_ler(path, corrigir_fronteira=False)
    ypo_validar_corpo_preservado(original, persistido, permitir_itimos_atual=False)
    try:
        st.cache_data.clear()
    except Exception:
        pass
    return "\n\n".join(resultados)


def novo_tema(tema, livro, banco_tematico="Machina"):
    """Cadastra tema autoral; erro em outro .ypo não desfaz o cadastro do alvo válido."""
    tema = str(tema or "").strip()
    livro = str(livro or "").strip()
    banco_tematico = str(banco_tematico or "Machina").strip() or "Machina"
    if not tema:
        raise ValueError("novo_tema: informe o nome do tema")
    if any(sep in tema for sep in ("/", "\\", ":", "*", "?", '"', "<", ">", "|")):
        raise ValueError("novo_tema: nome contém caractere inválido para arquivo")
    if livro not in TOOLS_BOOKS:
        raise ValueError(f"novo_tema: livro inválido: {livro}")
    ypo_path = _tools_resolve_ypo_path(tema)
    if not os.path.exists(ypo_path):
        raise FileNotFoundError(f"novo_tema: crie antes ./data/{tema}.ypo")
    original = _tools_validar_quantidades_tema(ypo_path)
    alteracoes = []
    if _tools_add_ativo_line(_project_path("base", "ativos.txt"), f"{tema} : {livro}", tema, livro):
        alteracoes.append("base/ativos.txt")
    if _tools_add_unique_line(_project_path("base", "images.txt"), f"{tema} : {banco_tematico}", tema):
        alteracoes.append("base/images.txt")
    if _tools_add_unique_line(_project_path("temp", "read_list.txt"), f"|{tema}|0|", tema):
        alteracoes.append("temp/read_list.txt")
    if _tools_add_unique_sorted_line(_project_path("base", "rol_todos os temas.txt"), tema, tema):
        alteracoes.append("base/rol_todos os temas.txt")
    if _tools_add_unique_sorted_line(_project_path("base", f"rol_{livro}.txt"), tema, tema):
        alteracoes.append(f"base/rol_{livro}.txt")

    resultados = [
        f"novo_tema: {tema} cadastrado",
        f"livro={livro}; banco_tematico={banco_tematico}",
        "alterados: " + (", ".join(alteracoes) if alteracoes else "nenhum; cadastro já existia"),
    ]
    resultados.append(_tools_tentar_derivado("Matrix", builders.build_matrix, tema))
    resultados.append(_tools_tentar_derivado("DNA", builders.build_dna))
    resultados.append(_tools_tentar_derivado("Léxico", builders.build_lexico))
    resultados.append(_tools_tentar_derivado("Indexy", builders.build_indexy))
    persistido = ypo_ler(ypo_path, corrigir_fronteira=False)
    ypo_validar_corpo_preservado(original, persistido, permitir_itimos_atual=False)
    try:
        st.cache_data.clear()
    except Exception:
        pass
    return "\n\n".join(resultados)


def _tools_remove_linhas_por_tema(path, tema):
    """Remove referências do tema de uma lista, com backup."""
    tema_norm = str(tema or "").strip().casefold()
    if not tema_norm or not os.path.exists(path):
        return 0
    with open(path, encoding="utf-8-sig") as file:
        linhas = file.read().splitlines()
    saida, removidas = [], 0
    for raw in linhas:
        raw_strip = raw.strip()
        chave = raw_strip.partition(" : ")[0].strip().casefold()
        if raw_strip.startswith("|"):
            campos = raw_strip.split("|")
            if len(campos) > 1:
                chave = campos[1].strip().casefold()
        if chave == tema_norm or raw_strip.casefold() == tema_norm:
            removidas += 1
        else:
            saida.append(raw)
    if removidas:
        _tools_write_text(path, "\n".join(saida).rstrip() + ("\n" if saida else ""))
    return removidas


def _tools_remover_arquivo_derivado(path):
    if path and os.path.isfile(path):
        _tools_backup_path(path)
        os.remove(path)
        return True
    return False


def remove_tema(tema):
    """Retira o tema do ambiente; nunca apaga o .ypo e não trava por erro de outro tema."""
    tema = str(tema or "").strip()
    if not tema:
        raise ValueError("remove_tema: escolha um tema")
    removidos = []
    arquivos_lista = [
        _project_path("base", "ativos.txt"),
        _project_path("base", "images.txt"),
        _project_path("temp", "read_list.txt"),
        _project_path("temp", "readings.txt"),  # legado: limpa se existir; não recebe novas gravações
        _project_path("base", "itimos.txt"),
        _project_path("base", "versos.txt"),
    ]
    base_dir = _project_path("base")
    if os.path.isdir(base_dir):
        for name in sorted(os.listdir(base_dir)):
            if name.lower().startswith("rol_") and name.lower().endswith(".txt"):
                arquivos_lista.append(os.path.join(base_dir, name))
    for path in dict.fromkeys(arquivos_lista):
        qtd = _tools_remove_linhas_por_tema(path, tema)
        if qtd:
            removidos.append(f"{os.path.relpath(path, _project_path())}: {qtd} linha(s)")
    matrix_dir = _project_path("images", "matrix")
    for nome in {tema + ".jpg", tema.capitalize() + ".jpg", tema + ".JPG", tema.capitalize() + ".JPG"}:
        candidate = os.path.join(matrix_dir, nome)
        if _tools_remover_arquivo_derivado(candidate):
            removidos.append(f"{os.path.relpath(candidate, _project_path())}: removido")
    resultados = [f"remove_tema: {tema}", "Alterações:\n" + ("\n".join(removidos) if removidos else "nenhuma")]
    resultados.append("Arquivo autoral .ypo preservado.")
    resultados.append(_tools_tentar_derivado("DNA", builders.build_dna))
    resultados.append(_tools_tentar_derivado("Léxico", builders.build_lexico))
    resultados.append(_tools_tentar_derivado("Indexy", builders.build_indexy))
    try:
        st.cache_data.clear()
    except Exception:
        pass
    return "\n\n".join(resultados)


def build_off_lex():
    start_time = time.time()
    off_dir = _project_path("off_machina")
    if not os.path.isdir(off_dir):
        return "Build_Off_Lex: pasta ./off_machina não encontrada."
    list_lexico = []
    list_verbet = []
    for name in sorted(os.listdir(off_dir)):
        if not name.lower().endswith(".pip"):
            continue
        script = os.path.join(off_dir, name)
        with open(script, encoding="utf-8") as file:
            for line in file:
                if not line.startswith("|"):
                    continue
                alinhas = line.split("|")
                if len(alinhas) < 3:
                    continue
                fonte = alinhas[1]
                if "Dados de Catalogação" in fonte or "copyrights" in fonte:
                    continue
                for itimo in alinhas[2:len(alinhas)-1]:
                    for word in itimo.split(" "):
                        if "-" not in word:
                            for c in string.punctuation:
                                word = word.replace(c, "")
                        word = word.strip().lower()
                        if len(word) >= 3:
                            if word not in list_verbet:
                                list_verbet.append(word)
                            chave = word + "|" + fonte
                            if chave not in list_lexico:
                                list_lexico.append(chave)
    _tools_write_text(os.path.join(off_dir, "off_lexico.txt"), "".join("|" + line + "|\n" for line in list_lexico))
    _tools_write_text(os.path.join(off_dir, "off_verbet.txt"), "".join(line + "\n" for line in list_verbet))
    return f"Build_Off_Lex: {len(list_lexico)} ocorrência(s); {len(list_verbet)} verbete(s). Runtime: {time.time() - start_time:.2f}s"


def build_all():
    """Executa a fila consolidada; STOP imediato na primeira falha."""
    tarefas = [
        ("build_dna", builders.build_dna, ()),
        ("build_matrix", builders.build_matrix, ()),
        ("build_lexico", builders.build_lexico, ()),
        ("build_indexy", builders.build_indexy, ()),
        ("update_rodape", update_rodape, ()),
    ]
    barra = st.progress(0)
    status = st.empty()
    resultados = []
    total = len(tarefas)
    for indice, (nome, func, args) in enumerate(tarefas, start=1):
        status.text(f"{indice}/{total}  {nome}")
        try:
            resultado = _tools_executar(nome, func, *args)
        except Exception as exc:
            status.error(f"STOP em {nome}: {exc}")
            raise RuntimeError(f"build_all STOP em {nome}: {exc}") from exc
        resultados.append(resultado)
        barra.progress(int(indice * 100 / total))
    status.success(f"{total}/{total} tarefas concluídas")
    try:
        st.cache_data.clear()
    except Exception:
        pass
    return "\n\n".join(resultados)

def _tools_run_button(label, func, *args):
    if st.button(label, use_container_width=True):
        with st.spinner(label + "..."):
            try:
                resultado = func(*args)
                st.success(label + " concluído.")
                st.text(resultado)
            except Exception as exc:
                st.error(f"{label} falhou: {exc}")

def _build_rimas_strip_accents(text):
    """Chave de ordenação sem acentos, preservando a palavra original na saída."""
    normalized = unicodedata.normalize("NFD", str(text or "").casefold())
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")

def _build_rimas_normalize_word(word, mode):
    word = str(word or "").strip("-'")
    if mode == "upper":
        return word.upper()
    if mode == "preserve":
        return word
    return word.casefold()

def _build_rimas_verb_to_infinitive(word):
    clean = _build_rimas_strip_accents(word)
    if clean.endswith("ando"):
        return clean[:-4] + "ar"
    if clean.endswith("endo"):
        return clean[:-4] + "er"
    if clean.endswith("indo"):
        return clean[:-4] + "ir"
    if clean.endswith(("ar", "er", "ir", "or")):
        return clean
    if clean.endswith("a"):
        return clean + "r"
    if clean.endswith("e"):
        return clean + "r"
    return clean

def _build_rimas_expand_token(token):
    parts = [part for part in str(token or "").split("-") if part]
    if len(parts) <= 1:
        return parts
    last_part = _build_rimas_strip_accents(parts[-1])
    if last_part in BUILD_RIMAS_CLITIC_PRONOUNS:
        return [_build_rimas_verb_to_infinitive(parts[0])]
    return parts

def _build_rimas_extract_words(text, mode="lower", min_len=2):
    words = []
    for match in BUILD_RIMAS_WORD_RE.finditer(str(text or "")):
        for token in _build_rimas_expand_token(match.group(0)):
            word = _build_rimas_normalize_word(token, mode)
            if len(word) >= int(min_len):
                words.append(word)
    return words

def _build_rimas_sorted_words(words):
    return sorted(set(words), key=lambda value: (_build_rimas_strip_accents(value), value))

def _build_rimas_group_by_suffix(words, min_size=2, max_size=6):
    """
    Agrupa do maior sufixo para o menor.

    Cada verbete é retirado da lista de disponíveis assim que entra
    em um grupo válido; portanto não reaparece em grupos menores.
    """
    min_size = max(1, int(min_size))
    max_size = max(min_size, int(max_size))
    palavras = _build_rimas_sorted_words(words)
    disponiveis = set(palavras)
    result = {}
    for size in range(max_size, min_size - 1, -1):
        grupos_do_tamanho = {}
        for word in palavras:
            if word not in disponiveis or len(word) <= size:
                continue
            suffix = word[-size:]
            suffix_key = _build_rimas_strip_accents(suffix)
            weak_keys = {_build_rimas_strip_accents(item) for item in BUILD_RIMAS_WEAK_SUFFIXES}
            if suffix_key in weak_keys:
                continue
            # A chave ignora acentos apenas para aproximar grafias equivalentes;
            # as palavras originais permanecem intactas na saída.
            grupos_do_tamanho.setdefault(suffix_key, []).append(word)
        grupos_validos = [
            (suffix, _build_rimas_sorted_words(values))
            for suffix, values in grupos_do_tamanho.items()
            if len(values) >= 2
        ]
        grupos_validos.sort(
            key=lambda item: (_build_rimas_strip_accents(item[0]), item[0])
        )
        for suffix, values in grupos_validos:
            values = [word for word in values if word in disponiveis]
            if len(values) < 2:
                continue
            result[suffix] = values
            disponiveis.difference_update(values)
    return result

def _build_rimas_split_groups(groups):
    rich = {}
    support = {}
    ordered = sorted(
        groups.items(),
        key=lambda item: (-len(item[0]), _build_rimas_strip_accents(item[0]), item[0]),
    )
    for suffix, words in ordered:
        rich_keys = {_build_rimas_strip_accents(item) for item in BUILD_RIMAS_RICH_SUFFIXES}
        if _build_rimas_strip_accents(suffix) in rich_keys:
            rich[suffix] = words
        else:
            support[suffix] = words
    return rich, support

def _build_rimas_sorted_by_suffix(words):
    return sorted(
        set(words),
        key=lambda word: (_build_rimas_strip_accents(word)[::-1], _build_rimas_strip_accents(word), word),
    )

def _build_rimas_render_list(lines):
    return "\n".join(lines) if lines else "(nenhum)"

def _build_rimas_render_groups(groups, marker="-"):
    parts = []
    for key, words in groups.items():
        label = f"[ {key} ]" if marker == "-" else f"[ {key}{marker} ]"
        parts.append(f"{label}\n{_build_rimas_render_list(words)}")
    return "\n\n".join(parts) if parts else "(nenhum grupo com 2 ou mais palavras)"

def build_rimas_texto(text, mode="lower", min_len=2, min_suffix=2, max_suffix=6):
    """Gera mapa lexical/rimas a partir de texto bruto. Não altera arquivos da Machina."""
    all_words = _build_rimas_extract_words(text, mode=mode, min_len=max(1, int(min_len)))
    unique_words = _build_rimas_sorted_words(all_words)
    suffix_groups = _build_rimas_group_by_suffix(unique_words, min_size=min_suffix, max_size=max_suffix)
    rich_groups, support_groups = _build_rimas_split_groups(suffix_groups)
    rich_words = {word for words in rich_groups.values() for word in words}
    support_words = {word for words in support_groups.values() for word in words}
    overlap = rich_words & support_words
    if overlap:
        raise RuntimeError(
            "Build_rimas encontrou verbetes repetidos entre RIMAS RICAS e RIMAS DE APOIO: "
            + ", ".join(_build_rimas_sorted_words(overlap))
        )
    mapped_words = rich_words | support_words
    outside_words = _build_rimas_sorted_by_suffix(set(unique_words) - mapped_words)
    final_words = list(rich_words) + list(support_words) + list(outside_words)
    final_unique_words = set(final_words)
    if len(final_words) != len(final_unique_words):
        raise RuntimeError("Build_rimas encontrou verbetes repetidos no arquivo final.")
    missing_words = set(unique_words) - final_unique_words
    extra_words = final_unique_words - set(unique_words)
    if missing_words or extra_words or len(final_words) != len(unique_words):
        detalhes = []
        if missing_words:
            detalhes.append("faltando: " + ", ".join(_build_rimas_sorted_words(missing_words)))
        if extra_words:
            detalhes.append("extras: " + ", ".join(_build_rimas_sorted_words(extra_words)))
        raise RuntimeError(
            "Build_rimas não preservou a quantidade exata de verbetes"
            + (": " + " | ".join(detalhes) if detalhes else ".")
        )
    return "\n\n".join(
        [
            "Build_rimas",
            "___",
            f"Total de ocorrências: {len(all_words)}",
            f"Verbetes únicos do texto inicial: {len(unique_words)}",
            f"Verbetes no arquivo final: {len(final_words)}",
            f"Palavras em rimas ricas: {len(rich_words)}",
            f"Palavras em rimas de apoio: {len(support_words)}",
            f"Palavras fora do mapa: {len(outside_words)}",
            "___",
            "RIMAS RICAS",
            _build_rimas_render_groups(rich_groups, "-"),
            "___",
            "RIMAS DE APOIO",
            _build_rimas_render_groups(support_groups, "-"),
            "___",
            "FORA DO MAPA",
            _build_rimas_render_list(outside_words),
            "___",
            "EOF()",
        ]
    )

def _texto_externo_decodificar(dados):
    """Tradutor-padrão: somente para material externo à Machina."""
    dados = bytes(dados or b"")
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return dados.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise ValueError("não foi possível reconhecer a codificação do texto externo.")


def _build_rimas_decode_uploaded(uploaded_file):
    texto, _encoding = _texto_externo_decodificar(uploaded_file.getvalue())
    return texto

def build_unicos_texto(text, mode="lower", min_len=1):
    """Devolve lista alfabética de verbetes únicos a partir de texto colado."""
    words = _build_rimas_extract_words(text, mode=mode, min_len=max(1, int(min_len)))
    return _build_rimas_render_list(_build_rimas_sorted_words(words))


def make_pip_texto(text):
    linhas = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if linhas and linhas[-1] == "":
        linhas.pop()
    return "|" + "|".join(linhas) + "|"


def render_make_pip_tool():
    st.markdown("### make_pip")
    st.caption("Converte texto externo em tema .pip e grava diretamente em ./off_machina.")
    texto_colado = st.text_area(
        "colar texto / área de descarte",
        height=220,
        key="make_pip_pasted_text",
        placeholder="Ctrl+V aqui basta para carregar o texto...",
    )
    uploaded = st.file_uploader(
        "tema.txt",
        type=["txt", "md", "markdown"],
        key="make_pip_upload",
    )
    texto_colado = str(texto_colado or "")
    if texto_colado.strip():
        texto = texto_colado
        nome_base = st.text_input(
            "nome do tema",
            value="novo_tema",
            key="make_pip_nome_colado",
        ).strip() or "novo_tema"
        encoding = "unicode"
        if uploaded is not None:
            st.caption("Fonte ativa: texto colado. Para usar o arquivo, limpe a área de descarte.")
    elif uploaded is not None:
        texto, encoding = _texto_externo_decodificar(uploaded.getvalue())
        nome_base = os.path.splitext(os.path.basename(uploaded.name))[0] or "novo_tema"
    else:
        st.info("Cole o texto ou escolha um arquivo textual.")
        return
    nome_base = os.path.basename(nome_base)
    nome = nome_base + ".pip"
    st.caption("saída: ./off_machina/" + nome)
    if encoding not in {"unicode", "utf-8", "utf-8-sig"}:
        st.caption("entrada externa convertida de " + encoding + " para UTF-8")
    if st.button("make_pip", use_container_width=True, key="make_pip_button"):
        resultado = make_pip_texto(texto)
        destino = _project_path("off_machina", nome)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino, "w", encoding="utf-8", newline="\n") as arquivo:
            arquivo.write(resultado + "\n")
        st.success(f"make_pip concluído: off_machina/{nome}")
        st.code(resultado, language=None)

def render_build_unicos_tool():
    """Ferramenta local da Off Sina para extrair verbetes únicos."""
    st.markdown("### Build_unicos")
    st.caption("Off Sina: recebe arquivo ou texto colado; devolve verbetes únicos em ordem alfabética.")
    pasted_text = st.text_area(
        "colar texto / área de descarte",
        value=st.session_state.get("build_unicos_pasted_text", ""),
        height=220,
        key="build_unicos_pasted_text",
        placeholder="Ctrl+V aqui basta para carregar o texto...",
    )
    uploaded = st.file_uploader(
        "arquivo .txt / .md / .doc",
        type=["txt", "md", "markdown", "doc"],
        key="build_unicos_upload",
    )
    case_mode = st.selectbox(
        "caixa",
        ["lower", "upper", "preserve"],
        index=0,
        key="build_unicos_case",
    )
    pasted_text = str(pasted_text or "")
    if pasted_text.strip():
        texto_fonte = pasted_text
        fonte = "texto colado"
        if uploaded is not None:
            st.caption("Fonte ativa: texto colado. Para usar o arquivo, limpe a área de descarte.")
    elif uploaded is not None:
        texto_fonte = _build_rimas_decode_uploaded(uploaded)
        fonte = uploaded.name
    else:
        st.info("Cole um texto ou escolha um arquivo textual.")
        return
    if st.button("Build_unicos", use_container_width=True):
        lista = build_unicos_texto(texto_fonte, mode=case_mode, min_len=1)
        st.session_state["build_unicos_result"] = lista
        st.session_state["build_unicos_fonte"] = fonte
        st.success("Build_unicos concluído.")
    resultado = st.session_state.get("build_unicos_result", "")
    if resultado:
        fonte_resultado = st.session_state.get("build_unicos_fonte", "")
        if fonte_resultado:
            st.caption("fonte: " + str(fonte_resultado))
        total = 0 if resultado == "(nenhum)" else len([line for line in resultado.splitlines() if line.strip()])
        st.caption(f"verbetes únicos: {total}")
        st.text_area(
            "lista_unicos.txt",
            value=resultado,
            height=420,
            key="build_unicos_textarea",
        )
        st.download_button(
            "baixar lista_unicos.txt",
            data=resultado + "\n",
            file_name="lista_unicos.txt",
            mime="text/plain",
            use_container_width=True,
        )

def render_build_rimas_tool():
    """Ferramenta local da Off Sina para mineração lexical/rimas."""
    st.markdown("### Build_rimas")
    st.caption("Off Sina: lê arquivo ou texto colado, organiza palavras únicas e monta mapa de rimas para curadoria.")
    pasted_text = st.text_area(
        "colar texto / área de descarte",
        value=st.session_state.get("build_rimas_pasted_text", ""),
        height=180,
        key="build_rimas_pasted_text",
        placeholder="Ctrl+V aqui basta para carregar o texto...",
    )
    uploaded = st.file_uploader(
        "arquivo .txt / .md / .doc",
        type=["txt", "md", "markdown", "doc"],
        key="build_rimas_upload",
    )
    upload_signature = None
    if uploaded is not None:
        upload_signature = (
            str(getattr(uploaded, "name", "")),
            int(getattr(uploaded, "size", 0) or 0),
        )
    previous_signature = st.session_state.get("build_rimas_upload_signature")
    if upload_signature != previous_signature:
        st.session_state["build_rimas_upload_signature"] = upload_signature
        for key in (
            "build_rimas_result",
            "build_rimas_download_name",
            "build_rimas_source_label",
        ):
            st.session_state.pop(key, None)
    col_case, col_min, col_suf = st.columns([1.2, 1.0, 1.4])
    with col_case:
        case_mode = st.selectbox(
            "caixa",
            ["lower", "upper", "preserve"],
            index=0,
            key="build_rimas_case",
        )
    with col_min:
        min_suffix = st.selectbox(
            "mínimo",
            list(range(1, 8)),
            index=1,
            key="build_rimas_min_suffix",
        )
    with col_suf:
        max_suffix = st.selectbox(
            "sufixo máx.",
            list(range(3, 9)),
            index=3,
            key="build_rimas_max_suffix",
        )
    pasted_text = str(pasted_text or "")
    has_paste = bool(pasted_text.strip())
    has_upload = uploaded is not None
    if has_paste:
        source_stem = "texto_colado"
        fonte_label = "texto colado"
    elif has_upload:
        source_stem = os.path.splitext(os.path.basename(uploaded.name))[0]
        fonte_label = uploaded.name
    else:
        source_stem = "build_rimas"
        fonte_label = ""
    output_name = f"rimas_{source_stem}.txt"
    st.caption("arquivo de saída: " + output_name)
    if not has_paste and not has_upload:
        st.info("Cole um texto com Ctrl+V na área de descarte ou escolha um arquivo .txt/.md/.doc.")
        return
    if has_paste and has_upload:
        st.caption("Fonte ativa: texto colado. Para usar o arquivo, limpe a área de descarte.")
    if st.button("Build_rimas", use_container_width=True):
        texto_fonte = pasted_text if has_paste else _build_rimas_decode_uploaded(uploaded)
        mapa = build_rimas_texto(
            texto_fonte,
            mode=case_mode,
            min_len=min_suffix,
            min_suffix=min_suffix,
            max_suffix=max_suffix,
        )
        st.session_state["build_rimas_result"] = mapa
        st.session_state["build_rimas_download_name"] = output_name
        st.session_state["build_rimas_source_label"] = fonte_label
        st.success("Build_rimas concluído.")
    resultado = st.session_state.get("build_rimas_result", "")
    download_name = st.session_state.get("build_rimas_download_name", output_name)
    source_label = st.session_state.get("build_rimas_source_label", "")
    if resultado:
        if source_label:
            st.caption("fonte: " + str(source_label))
        st.text_area(
            "mapa lexical",
            value=resultado,
            height=420,
            key="build_rimas_textarea",
        )
        st.download_button(
            "baixar " + download_name,
            data=resultado + "\n",
            file_name=download_name,
            mime="text/plain",
            use_container_width=True,
        )
_ATELIER_POS_LABELS = {
    "VERB": "Verbos",
    "AUX": "Verbos auxiliares",
    "NOUN": "Substantivos",
    "PROPN": "Nomes próprios",
    "ADJ": "Adjetivos",
    "ADV": "Advérbios",
    "PRON": "Pronomes",
    "ADP": "Preposições",
    "DET": "Determinantes e artigos",
    "CCONJ": "Conjunções coordenativas",
    "SCONJ": "Conjunções subordinativas",
    "NUM": "Números",
    "INTJ": "Interjeições",
    "PART": "Partículas",
    "X": "Outros",
}

def _atelier_load_nlp():
    """Carrega spaCy somente quando o Atelier é usado.

    Assim, a página Tools continua abrindo mesmo em ambientes nos quais
    spaCy ou o modelo português ainda não estejam instalados.
    """
    try:
        import spacy
    except Exception as exc:
        raise RuntimeError(
            "spaCy não está instalado. Execute: pip install spacy"
        ) from exc
    try:
        return spacy.load("pt_core_news_sm")
    except Exception as exc:
        raise RuntimeError(
            "modelo pt_core_news_sm não encontrado. Execute: "
            "python -m spacy download pt_core_news_sm"
        ) from exc

def _atelier_classificar_palavras(texto, usar_lema=True, mode="lower", min_len=1):
    """Classifica verbetes do texto por classe gramatical, sem repetições."""
    nlp = _atelier_load_nlp()
    doc = nlp(str(texto or ""))
    grupos = {}
    for token in doc:
        if not token.is_alpha:
            continue
        palavra = token.lemma_ if usar_lema and token.lemma_ else token.text
        palavra = _build_rimas_normalize_word(palavra, mode)
        palavra = str(palavra or "").strip()
        if len(palavra) < max(1, int(min_len)):
            continue
        classe = _ATELIER_POS_LABELS.get(token.pos_, f"Outros ({token.pos_ or 'X'})")
        grupos.setdefault(classe, set()).add(palavra)
    return {
        classe: _build_rimas_sorted_words(palavras)
        for classe, palavras in sorted(grupos.items(), key=lambda item: item[0].casefold())
    }

def _atelier_render_classificacao(classificacao):
    partes = ["CLASSIFICAÇÃO GRAMATICAL", "___"]
    if not classificacao:
        partes.append("(nenhum verbete classificado)")
    else:
        for classe, palavras in classificacao.items():
            partes.extend([
                f"{classe} ({len(palavras)})",
                _build_rimas_render_list(palavras),
                "",
            ])
    return "\n".join(partes).rstrip()

def _atelier_normalizar_escrita(texto):
    normalized = unicodedata.normalize("NFD", str(texto or "").casefold())
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")

def _atelier_normalizar_som(palavra):
    valor = _atelier_normalizar_escrita(palavra)
    valor = re.sub(r"[szxh]", "s", valor)
    valor = re.sub(r"[gk]", "c", valor)
    valor = re.sub(r"[dt]", "t", valor)
    valor = valor.replace("v", "f").replace("m", "n")
    return valor

def _atelier_agrupar_rimas(palavras, tamanho=3, por_som=False):
    grupos = {}
    tamanho = max(1, int(tamanho))
    for palavra in palavras:
        base = _atelier_normalizar_som(palavra) if por_som else _atelier_normalizar_escrita(palavra)
        chave = base[-tamanho:] if len(base) >= tamanho else base
        grupos.setdefault(chave, set()).add(palavra)
    return {
        chave: _build_rimas_sorted_words(valores)
        for chave, valores in sorted(grupos.items())
        if len(valores) > 1
    }

def _atelier_render_rimas(titulo, grupos):
    partes = [titulo, "___"]
    if not grupos:
        partes.append("(nenhuma rima encontrada)")
    else:
        for chave, palavras in grupos.items():
            partes.append(f"[{chave}]\n" + "\n".join(palavras))
    return "\n\n".join(partes)

def build_atelier_texto(
    text,
    usar_lema=True,
    mode="lower",
    min_len=2,
    min_suffix=2,
    max_suffix=6,
    tipo_rima="ambas",
    tamanho_rima=3,
):
    """Classificação gramatical e rimas por escrita/som para curadoria."""
    texto = str(text or "")
    if not texto.strip():
        raise ValueError("o texto do Atelier está vazio.")
    classificacao = _atelier_classificar_palavras(
        texto, usar_lema=bool(usar_lema), mode=mode, min_len=min_len
    )
    palavras = _build_rimas_sorted_words(
        palavra for grupo in classificacao.values() for palavra in grupo
    )
    rimas_escrita = {}
    rimas_som = {}
    if tipo_rima in {"escrita", "ambas"}:
        rimas_escrita = _atelier_agrupar_rimas(palavras, tamanho_rima, por_som=False)
    if tipo_rima in {"som", "ambas"}:
        rimas_som = _atelier_agrupar_rimas(palavras, tamanho_rima, por_som=True)
    partes = ["Atelier", "___", _atelier_render_classificacao(classificacao)]
    if tipo_rima in {"escrita", "ambas"}:
        partes.extend(["___", _atelier_render_rimas("RIMAS POR ESCRITA", rimas_escrita)])
    if tipo_rima in {"som", "ambas"}:
        partes.extend(["___", _atelier_render_rimas("RIMAS POR SOM", rimas_som)])
    return {
        "classificacao_gramatical": classificacao,
        "rimas_por_escrita": rimas_escrita,
        "rimas_por_som": rimas_som,
        "texto": "\n\n".join(partes),
    }

def _atelier_json(resultado):
    return json.dumps(
        {
            "build": "Build_Atelier",
            "classificacao_gramatical": resultado["classificacao_gramatical"],
            "rimas_por_escrita": resultado.get("rimas_por_escrita", {}),
            "rimas_por_som": resultado.get("rimas_por_som", {}),
            "relatorio_texto": resultado["texto"],
        },
        ensure_ascii=False,
        indent=2,
    ) + "\n"

def _atelier_csv(resultado):
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=";")
    writer.writerow(["Classe gramatical", "Palavra"])
    for classe, palavras in resultado["classificacao_gramatical"].items():
        for palavra in palavras:
            writer.writerow([classe, palavra])
    for tipo, grupos in (
        ("Rima por escrita", resultado.get("rimas_por_escrita", {})),
        ("Rima por som", resultado.get("rimas_por_som", {})),
    ):
        for terminacao, palavras in grupos.items():
            writer.writerow([tipo + " [" + terminacao + "]", ", ".join(palavras)])
    return buffer.getvalue()

def render_build_atelier_tool():
    """Interface local do Build_Atelier."""
    st.markdown("### Atelier")
    st.caption(
        "Classifica verbetes por classe gramatical e monta o mapa de rimas. "
        "Não altera arquivos da Machina."
    )
    pasted_text = st.text_area(
        "colar texto / área de descarte",
        value=st.session_state.get("build_atelier_pasted_text", ""),
        height=220,
        key="build_atelier_pasted_text",
        placeholder="Ctrl+V aqui basta para carregar o texto...",
    )
    uploaded = st.file_uploader(
        "arquivo textual",
        type=["txt", "md", "markdown", "doc"],
        key="build_atelier_upload",
    )
    col_lema, col_case, col_min = st.columns([1.1, 1.0, 1.0])
    with col_lema:
        usar_lema = st.checkbox("usar lema", value=True, key="build_atelier_lema")
    with col_case:
        case_mode = st.selectbox(
            "caixa", ["lower", "upper", "preserve"], index=0,
            key="build_atelier_case",
        )
    with col_min:
        min_len = st.selectbox(
            "mín. letras", list(range(1, 8)), index=1,
            key="build_atelier_min_len",
        )
    col_tipo, col_tamanho = st.columns(2)
    with col_tipo:
        tipo_rima = st.selectbox(
            "rimas", ["ambas", "escrita", "som", "nenhuma"], index=0,
            key="atelier_tipo_rima",
        )
    with col_tamanho:
        tamanho_rima = st.selectbox(
            "terminação", [2, 3], index=1, key="atelier_tamanho_rima"
        )
    min_suffix = 2
    max_suffix = 6
    texto_colado = str(pasted_text or "")
    if texto_colado.strip():
        texto_fonte = texto_colado
        source_stem = "texto_colado"
    elif uploaded is not None:
        texto_fonte = _build_rimas_decode_uploaded(uploaded)
        source_stem = os.path.splitext(os.path.basename(uploaded.name))[0] or "atelier"
    else:
        st.info("Cole um texto ou escolha um arquivo textual.")
        return
    if st.button("Build_Atelier", use_container_width=True):
        try:
            resultado = build_atelier_texto(
                texto_fonte,
                usar_lema=usar_lema,
                mode=case_mode,
                min_len=min_len,
                min_suffix=min_suffix,
                max_suffix=max_suffix,
                tipo_rima=tipo_rima,
                tamanho_rima=tamanho_rima,
            )
            st.session_state["build_atelier_result"] = resultado
            st.session_state["build_atelier_stem"] = source_stem
            st.success("Atelier concluído.")
        except Exception as exc:
            st.error(f"Atelier falhou: {exc}")
    resultado = st.session_state.get("build_atelier_result")
    if not resultado:
        return
    stem = st.session_state.get("build_atelier_stem", source_stem)
    st.text_area(
        "relatório do Atelier",
        value=resultado["texto"],
        height=520,
        key="build_atelier_textarea",
    )
    col_txt, col_json, col_csv = st.columns(3)
    with col_txt:
        st.download_button(
            "baixar TXT",
            data=resultado["texto"] + "\n",
            file_name=f"atelier_{stem}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col_json:
        st.download_button(
            "baixar JSON",
            data=_atelier_json(resultado),
            file_name=f"atelier_{stem}.json",
            mime="application/json",
            use_container_width=True,
        )
    with col_csv:
        st.download_button(
            "baixar CSV",
            data=_atelier_csv(resultado),
            file_name=f"atelier_{stem}.csv",
            mime="text/csv",
            use_container_width=True,
        )

def _make_md_validar_limites(chr_minimo, chr_maximo):
    """Valida os limites de comprimento usados pelo make_md."""
    try:
        minimo = int(chr_minimo)
        maximo = int(chr_maximo)
    except (TypeError, ValueError) as exc:
        raise ValueError("chr_minimo e chr_maximo devem ser números inteiros.") from exc
    if minimo < 1:
        raise ValueError("chr_minimo deve ser maior ou igual a 1.")
    if maximo < minimo:
        raise ValueError("chr_maximo deve ser maior ou igual a chr_minimo.")
    return minimo, maximo

def _make_md_prefixo_estrutural(linha):
    """Separa prefixos Markdown que devem ser preservados nas linhas derivadas."""
    texto = str(linha or "")
    padroes = [
        r"^(\s*>\s+)",                       # citação
        r"^(\s*[-+*]\s+)",                  # lista não ordenada
        r"^(\s*\d+[.)]\s+)",               # lista ordenada
        r"^(\s*#{1,6}\s+)",                 # título Markdown
    ]
    for padrao in padroes:
        match = re.match(padrao, texto)
        if match:
            return match.group(1), texto[match.end():]
    match = re.match(r"^(\s*)", texto)
    prefixo = match.group(1) if match else ""
    return prefixo, texto[len(prefixo):]

def _make_md_linha_estrutural(linha):
    """Identifica linhas que não devem ser fundidas com o parágrafo vizinho."""
    texto = str(linha or "").strip()
    if not texto:
        return True
    if re.match(r"^(```|~~~)", texto):
        return True
    if re.match(r"^(?:___+|---+|\*\*\*+)$", texto):
        return True
    if re.match(r"^#{1,6}\s+", texto):
        return True
    if re.match(r"^(?:[-+*]|\d+[.)])\s+", texto):
        return True
    if texto.startswith(">"):
        return True
    if "|" in texto and texto.count("|") >= 2:
        return True
    return False

def _make_md_quebrar_texto(texto, prefixo, chr_minimo, chr_maximo):
    """Distribui palavras dentro dos limites, sem cortar palavras."""
    palavras = re.findall(r"\S+", str(texto or "").strip())
    if not palavras:
        return [prefixo.rstrip()]
    # Linhas seguintes mantêm apenas a indentação do prefixo estrutural.
    indent_match = re.match(r"^\s*", prefixo)
    indentacao = indent_match.group(0) if indent_match else ""
    prefixos = [prefixo, indentacao]
    blocos = []
    atual = []
    prefixo_atual = prefixos[0]
    for palavra in palavras:
        candidato = " ".join(atual + [palavra])
        tamanho = len(prefixo_atual + candidato)
        if atual and tamanho > chr_maximo:
            blocos.append((prefixo_atual, atual))
            atual = [palavra]
            prefixo_atual = prefixos[1]
        else:
            atual.append(palavra)
    if atual:
        blocos.append((prefixo_atual, atual))
    # Balanceia a última linha para aproximá-la do mínimo quando possível.
    if len(blocos) >= 2:
        pref_ant, anterior = blocos[-2]
        pref_ult, ultima = blocos[-1]
        while len(pref_ult + " ".join(ultima)) < chr_minimo and len(anterior) > 1:
            candidata = anterior[-1]
            nova_anterior = anterior[:-1]
            nova_ultima = [candidata] + ultima
            tam_anterior = len(pref_ant + " ".join(nova_anterior))
            tam_ultima = len(pref_ult + " ".join(nova_ultima))
            if tam_anterior < chr_minimo or tam_ultima > chr_maximo:
                break
            anterior[:] = nova_anterior
            ultima[:] = nova_ultima
    return [pref + " ".join(palavras_bloco) for pref, palavras_bloco in blocos]

def _make_md_quebrar_linha(linha, chr_minimo, chr_maximo):
    """Reformata uma linha isolada, preservando seu prefixo Markdown."""
    linha = str(linha or "").rstrip(" \t")
    if not linha:
        return [""]
    prefixo, corpo = _make_md_prefixo_estrutural(linha)
    return _make_md_quebrar_texto(corpo, prefixo, chr_minimo, chr_maximo)

def _make_md_refluir_linhas(linhas_origem, chr_minimo, chr_maximo):
    """Une linhas curtas de prosa e redistribui os parágrafos nos limites.

    Linhas vazias e estruturas Markdown permanecem como fronteiras. Itens de
    lista, citações, títulos, tabelas e separadores não são fundidos com texto
    vizinho, mas podem ser quebrados internamente quando excedem o máximo.
    """
    saida = []
    paragrafo = []
    em_codigo = False
    def descarregar_paragrafo():
        nonlocal paragrafo
        if not paragrafo:
            return
        texto = " ".join(parte.strip() for parte in paragrafo if parte.strip())
        saida.extend(_make_md_quebrar_texto(texto, "", chr_minimo, chr_maximo))
        paragrafo = []
    for linha_original in linhas_origem:
        linha = str(linha_original or "").rstrip(" \t")
        limpa = linha.strip()
        if re.match(r"^(```|~~~)", limpa):
            descarregar_paragrafo()
            saida.append(linha)
            em_codigo = not em_codigo
            continue
        if em_codigo:
            saida.append(linha)
            continue
        if not limpa:
            descarregar_paragrafo()
            saida.append("")
            continue
        if _make_md_linha_estrutural(linha):
            descarregar_paragrafo()
            saida.extend(_make_md_quebrar_linha(linha, chr_minimo, chr_maximo))
            continue
        paragrafo.append(linha)
    descarregar_paragrafo()
    return saida

def _make_md_texto_utf8(raw_bytes, chr_minimo, chr_maximo):
    """Decodifica UTF-8, reflui parágrafos e aplica o padrão Markdown.

    Cada linha de saída termina com exatamente dois espaços antes da quebra.
    O conteúdo não é traduzido, corrigido, resumido nem reescrito.
    """
    minimo, maximo = _make_md_validar_limites(chr_minimo, chr_maximo)
    try:
        texto = bytes(raw_bytes or b"").decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("O arquivo não é texto UTF-8. Nenhuma conversão foi feita.") from exc
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    linhas_origem = texto.split("\n")
    termina_com_quebra = texto.endswith("\n")
    if termina_com_quebra and linhas_origem:
        linhas_origem = linhas_origem[:-1]
    linhas_saida = _make_md_refluir_linhas(linhas_origem, minimo, maximo)
    resultado = "\n".join(linha.rstrip(" \t") + "  " for linha in linhas_saida)
    if linhas_saida or termina_com_quebra:
        resultado += "\n"
    return resultado

def _make_md_output_path(uploaded_name):
    """Define ./md_files/arquivo.md; usa arquivo_new.md quando necessário."""
    base = os.path.splitext(os.path.basename(str(uploaded_name or "arquivo")))[0].strip()
    base = base or "arquivo"
    md_dir = _project_path("md_files")
    os.makedirs(md_dir, exist_ok=True)
    destino = os.path.join(md_dir, base + ".md")
    if os.path.exists(destino):
        destino = os.path.join(md_dir, base + "_new.md")
    return destino

def render_make_md_tool():
    """Converte texto externo em Markdown dentro dos limites escolhidos."""
    st.markdown("### make_md")
    st.caption(
        "Ajusta as linhas entre chr_minimo e chr_maximo e acrescenta "
        "dois espaços ao fim de cada linha."
    )
    col_min, col_max = st.columns(2)
    with col_min:
        chr_minimo = st.number_input(
            "chr_minimo",
            min_value=1,
            max_value=1000,
            value=60,
            step=1,
            key="make_md_chr_minimo",
        )
    with col_max:
        chr_maximo = st.number_input(
            "chr_maximo",
            min_value=1,
            max_value=1000,
            value=80,
            step=1,
            key="make_md_chr_maximo",
        )
    texto_colado = st.text_area(
        "colar texto / área de descarte",
        height=260,
        key="make_md_pasted_text",
        placeholder="Ctrl+V aqui basta para carregar o texto...",
    )
    uploaded = st.file_uploader(
        "arquivo.ext — qualquer extensão textual",
        type=None,
        key="make_md_upload",
    )
    texto_colado = str(texto_colado or "")
    if texto_colado.strip():
        texto = texto_colado
        nome_base = st.text_input(
            "nome do arquivo",
            value="arquivo",
            key="make_md_nome_colado",
        ).strip() or "arquivo"
        nome_origem = os.path.basename(nome_base) + ".txt"
        encoding = "unicode"
        if uploaded is not None:
            st.caption("Fonte ativa: texto colado. Para usar o arquivo, limpe a área de descarte.")
    elif uploaded is not None:
        texto, encoding = _texto_externo_decodificar(uploaded.getvalue())
        nome_origem = uploaded.name
        nome_base = os.path.splitext(os.path.basename(uploaded.name))[0] or "arquivo"
    else:
        st.info("Cole o texto ou escolha um arquivo textual.")
        return
    st.caption("saída: ./md_files/" + nome_base + ".md")
    if encoding not in {"unicode", "utf-8", "utf-8-sig"}:
        st.caption("entrada externa convertida de " + encoding + " para UTF-8")
    if st.button("make_md", use_container_width=True):
        try:
            resultado = _make_md_texto_utf8(
                texto.encode("utf-8"),
                chr_minimo=chr_minimo,
                chr_maximo=chr_maximo,
            )
            destino = _make_md_output_path(nome_origem)
            with open(destino, "w", encoding="utf-8", newline="\n") as file:
                file.write(resultado)
            st.success("make_md concluído.")
            st.text(os.path.relpath(destino, _project_path()).replace("\\", "/"))
        except Exception as exc:
            st.error(f"make_md falhou: {exc}")

def _resize_images_validar_dimensoes(largura, altura):
    try:
        largura = int(largura)
        altura = int(altura)
    except (TypeError, ValueError) as exc:
        raise ValueError("largura e altura devem ser números inteiros.") from exc
    if largura < 1 or altura < 1:
        raise ValueError("largura e altura devem ser maiores que zero.")
    return largura, altura

def _resize_images_remover_rodape_branco(imagem, tolerancia=245, minimo_branco=0.97):
    """Remove somente a faixa branca contígua encostada no rodapé.

    A leitura sobe linha a linha enquanto quase todos os pixels forem brancos.
    Não procura branco no interior da imagem e não recorta topo ou laterais.
    """
    from PIL import Image
    rgb = imagem.convert("RGB")
    largura, altura = rgb.size
    if largura < 1 or altura < 2:
        return imagem, 0
    pixels = rgb.load()
    limite_brancos = max(1, int(largura * float(minimo_branco)))
    corte = altura
    for y in range(altura - 1, -1, -1):
        brancos = 0
        for x in range(largura):
            r, g, b = pixels[x, y]
            if r >= tolerancia and g >= tolerancia and b >= tolerancia:
                brancos += 1
        if brancos >= limite_brancos:
            corte = y
        else:
            break
    removidos = altura - corte
    # Evita eliminar uma imagem inteira ou uma grande área branca autoral.
    limite_seguro = max(1, min(40, altura // 8))
    if removidos < 1 or removidos > limite_seguro or corte < 2:
        return imagem, 0
    return imagem.crop((0, 0, largura, corte)), removidos

def _resize_images_processar(origem, destino, largura=240, altura=360, fundo="white"):
    """Remove rodapé branco e ajusta a altura sem cortar laterais.

    Primeiro elimina somente a faixa branca contígua encostada no rodapé.
    Depois normaliza a largura, se necessário, e altera apenas a altura até o
    tamanho escolhido. Os originais nunca são apagados ou sobrescritos.
    """
    try:
        from PIL import Image, ImageOps
    except Exception as exc:
        raise RuntimeError(f"Pillow não está disponível: {exc}") from exc
    largura, altura = _resize_images_validar_dimensoes(largura, altura)
    origem = os.path.abspath(str(origem or "").strip())
    destino = os.path.abspath(str(destino or "").strip())
    if not os.path.isdir(origem):
        raise FileNotFoundError(f"pasta de origem não encontrada: {origem}")
    if origem == destino:
        raise ValueError("a pasta de destino deve ser diferente da pasta de origem.")
    os.makedirs(destino, exist_ok=True)
    extensoes = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
    arquivos = [
        nome for nome in sorted(os.listdir(origem), key=natural_keys)
        if os.path.isfile(os.path.join(origem, nome))
        and os.path.splitext(nome)[1].casefold() in extensoes
    ]
    if not arquivos:
        raise ValueError("nenhuma imagem compatível foi encontrada na pasta de origem.")
    processadas = []
    falhas = []
    for nome in arquivos:
        entrada = os.path.join(origem, nome)
        saida = os.path.join(destino, nome)
        try:
            with Image.open(entrada) as imagem:
                imagem = ImageOps.exif_transpose(imagem)
                if imagem.mode not in ("RGB", "RGBA"):
                    imagem = imagem.convert("RGBA" if "transparency" in imagem.info else "RGB")
                cor_fundo = fundo
                if imagem.mode == "RGBA" and os.path.splitext(saida)[1].casefold() in {".jpg", ".jpeg"}:
                    base = Image.new("RGB", imagem.size, cor_fundo)
                    base.paste(imagem, mask=imagem.getchannel("A"))
                    imagem = base
                imagem, rodape_removido = _resize_images_remover_rodape_branco(imagem)
                # A largura é apenas normalizada quando necessário.
                # A etapa final altera a altura diretamente: sem fit, pad ou crop lateral.
                if imagem.width != largura:
                    altura_proporcional = max(1, round(imagem.height * largura / imagem.width))
                    imagem = imagem.resize(
                        (largura, altura_proporcional),
                        Image.Resampling.LANCZOS,
                    )
                nova = imagem.resize(
                    (largura, altura),
                    Image.Resampling.LANCZOS,
                )
                parametros = {}
                if os.path.splitext(saida)[1].casefold() in {".jpg", ".jpeg"}:
                    if nova.mode != "RGB":
                        nova = nova.convert("RGB")
                    parametros = {"quality": 95, "optimize": True}
                nova.save(saida, **parametros)
                processadas.append((nome, rodape_removido))
        except Exception as exc:
            falhas.append((nome, str(exc)))
    return processadas, falhas

def render_resize_images_tool():
    """Interface local para padronizar lotes de imagens."""
    st.markdown("### resize_images")
    st.caption(
        "Remove faixa branca contígua do rodapé e ajusta a altura. "
        "Não usa fit, pad ou corte lateral. Os originais não são apagados."
    )
    col_largura, col_altura = st.columns(2)
    with col_largura:
        largura = st.number_input(
            "largura", min_value=1, max_value=10000, value=240, step=1,
            key="resize_images_largura",
        )
    with col_altura:
        altura = st.number_input(
            "altura", min_value=1, max_value=10000, value=360, step=1,
            key="resize_images_altura",
        )
    origem_rel = st.text_input(
        "pasta de origem",
        value="images/#garimpo",
        key="resize_images_origem",
    )
    destino_rel = st.text_input(
        "pasta de destino",
        value="images/#resized",
        key="resize_images_destino",
    )
    fundo = st.text_input(
        "cor do fundo",
        value="white",
        key="resize_images_fundo",
    )
    origem = origem_rel if os.path.isabs(origem_rel) else _project_path(*origem_rel.replace("\\", "/").split("/"))
    destino = destino_rel if os.path.isabs(destino_rel) else _project_path(*destino_rel.replace("\\", "/").split("/"))
    st.caption("origem: " + origem)
    st.caption("destino: " + destino)
    if st.button("resize_images", use_container_width=True):
        try:
            processadas, falhas = _resize_images_processar(
                origem, destino, largura=largura, altura=altura, fundo=fundo
            )
            st.success(f"resize_images concluído: {len(processadas)} imagem(ns).")
            removidos = [(nome, px) for nome, px in processadas if px]
            st.text(os.path.relpath(destino, _project_path()).replace("\\", "/"))
            if removidos:
                st.caption("rodapés removidos: " + ", ".join(f"{nome} ({px}px)" for nome, px in removidos))
            if falhas:
                st.warning(f"{len(falhas)} arquivo(s) não foram processados.")
                st.text("\n".join(f"{nome}: {erro}" for nome, erro in falhas))
        except Exception as exc:
            st.error(f"resize_images falhou: {exc}")

def _tools_help_text():
    return """help_? — Tools da Machina

novo_tema
  Cadastra um tema autoral já existente em ./data. Exige livro e banco temático,
  valida real == declarado antes de qualquer cadastro e nunca altera o corpo .ypo.

remove_tema
  Retira o tema do ambiente local e reconstrói derivados. O arquivo autoral .ypo
  é sempre preservado; somente referências cadastrais e Matrix derivada são removidas.

update_tema
  Valida real == declarado, atualiza Matrix, léxico, Indexy e DNA e depois chama
  update_rodape. O corpo do .ypo precisa permanecer integralmente preservado.

update_rodape
  Recalcula e reescreve toda a Ficha Técnica. Preserva a linha Build By existente
  e tudo que estiver abaixo dela como nota de oficina com assinatura '#- '.

build_indexy
  Atualiza ./md_files/ABOUT_index.MD com as variações combinatórias por tema.

build_lexico
  Regera ./base/lexico_pt.txt e ./base/verbetes.txt.

build_off-lex
  Regera ./off_machina/off_lexico.txt e ./off_machina/off_verbet.txt.

build_rimas
  Off Sina: extrai palavras únicas e gera mapa de rimas para curadoria.

atelier
  Classifica verbetes por classe gramatical e usa o mapa de rimas da Machina.

build_matrix
  Gera Matrix 3D e atualiza ./base/itimos.txt e ./base/versos.txt.

build_dna
  Constrói ./base/DNA.TXT sem depender de info.txt.

build_all
  Executor da fila consolidada. Mostra barra de andamento e dá STOP no primeiro erro.

ficha_lexico
  Atualiza o bloco “Ambiente Léxico da Machina” em ./md_files/INDEX.txt.

build_utf-8
  Normaliza os arquivos autorizados da pasta escolhida para UTF-8.
  A autoridade de extensões é ./base/build_utf8.txt. Não percorre subpastas.
  O original fica ao lado como arquivo_old.ext; a estrutura permanece AS IS.

make_md
  Converte arquivo textual UTF-8 para Markdown de duas quebras.

make_pip
  Converte tema.txt em off_machina/tema.pip.

make_ola
  Envia um arquivo textual UTF-8 para uma análise sintática da OLA.

resize_images
  Padroniza imagens sem cortar/deformar e sem sobrescrever originais.
"""

def _build_utf8_extensoes_exibicao():
    """Mostra a autoridade de extensões do build_utf-8."""
    path = os.path.join("./base", "build_utf8.txt")
    try:
        with open(path, encoding="utf-8-sig") as file:
            itens = []
            for raw in file:
                item = raw.strip()
                if not item or item.startswith("#"):
                    continue
                if not item.startswith("."):
                    item = "." + item
                if item.casefold() not in [x.casefold() for x in itens]:
                    itens.append(item)
            return itens
    except OSError:
        return []


def render_build_utf8_tool():
    """Interface LOCAL da família build_utf-8."""
    st.caption("pasta escolhida • extensões autorizadas • estrutura AS IS")

    pasta = st.text_input(
        "pasta",
        value="./data/acros",
        key="build_utf8_pasta",
        help="Somente os arquivos desta pasta. Subpastas não são percorridas.",
    )

    extensoes = _build_utf8_extensoes_exibicao()
    if extensoes:
        st.caption("autorizadas: " + "  ".join(extensoes))
    else:
        st.warning("Lista ./base/build_utf8.txt ausente ou vazia.")

    if not st.button("build_utf-8", use_container_width=True):
        return

    progress = st.progress(0, text="pre-flight...")
    status = st.empty()

    def progress_callback(indice, total):
        pct = 100 if total <= 0 else int(indice * 100 / total)
        progress.progress(
            min(100, pct),
            text=f"{min(100, pct)}%  •  {indice}/{total}",
        )

    def status_callback(mensagem):
        status.text(mensagem)

    try:
        resultado = builders.build_utf8(
            pasta,
            progress_callback=progress_callback,
            status_callback=status_callback,
        )
    except Exception as exc:
        status.error(f"build_utf-8 STOP: {exc}")
        return

    progress.progress(100, text="100%  •  DONE")
    status.success("build_utf-8 concluído")
    st.text(resultado)


def page_tools():
    st.subheader("Tools")
#    st.caption("LOCAL. Lista funcional simples. Lê temas; não altera poesia.")
    tools_items = [
        "novo_tema",
        "remove_tema",
        "update_rodape",
        "update_tema",
        "---",
        "atelier",
        "build_rimas",
        "build_unicos",
        "make_md",
        "make_ola",
        "make_pip",
        "resize_images",
        "---",
        "build_all",
        "build_dna",
        "build_indexy",
        "build_lexico",
        "build_matrix",
        "build_off-lex",
        "build_utf-8",
        "ficha_lexico",
        "---",
        "help_?",
    ]
    try:
        temas_local = [tema for tema, path in _tools_temas_ativos()]
    except Exception:
        temas_local = []
    try:
        temas_remocao = _tools_temas_para_remover()
    except Exception:
        temas_remocao = temas_local
    escolha = st.selectbox(
        "tools",
        tools_items,
        index=tools_items.index("help_?"),
        key="tools_lista_funcional",
    )
    if escolha == "---":
        st.info("separador")
        return
    tema_update = None
    tema_remove = None
    tema_rodape = None
    novo_tema_nome = ""
    novo_tema_livro = TOOLS_BOOKS[0]
    novo_tema_banco = "Machina"
    if escolha == "update_tema":
        if temas_local:
            tema_update = st.selectbox(
                "tema",
                temas_local,
                key="tools_lista_update_tema",
            )
        else:
            st.warning("Nenhum tema encontrado em ./base/ativos.txt.")
            return
    elif escolha == "remove_tema":
        if temas_remocao:
            tema_remove = st.selectbox(
                "tema",
                temas_remocao,
                key="tools_lista_remove_tema",
            )
        else:
            st.warning("Nenhum tema encontrado nas listas dos yPoemas ou em ./data.")
            return
    elif escolha == "update_rodape":
        opcoes_rodape = ["todos os temas"] + temas_local
        tema_rodape = st.selectbox(
            "tema",
            opcoes_rodape,
            key="tools_lista_rodape_ypo",
        )
        if tema_rodape == "todos os temas":
            tema_rodape = None
    elif escolha == "novo_tema":
        novo_tema_nome = st.text_input(
            "novo tema já existente em ./data",
            key="tools_lista_novo_tema",
        )
        novo_tema_livro = st.selectbox(
            "livro", TOOLS_BOOKS, key="tools_novo_tema_livro"
        )
        bancos = _tools_bancos_tematicos()
        novo_tema_banco = st.selectbox(
            "banco temático", bancos,
            index=bancos.index("Machina") if "Machina" in bancos else 0,
            key="tools_novo_tema_banco",
        )
    if escolha == "build_rimas":
        render_build_rimas_tool()
        return
    if escolha == "make_pip":
        render_make_pip_tool()
        return
    if escolha == "atelier":
        render_build_atelier_tool()
        return
    if escolha == "build_unicos":
        render_build_unicos_tool()
        return
    if escolha == "make_md":
        render_make_md_tool()
        return
    if escolha == "make_ola":
        if make_ola_tools is None:
            st.error("make_ola_tools.py não pôde ser carregado.")
            return
        make_ola_tools.render_make_ola_tool()
        return
    if escolha == "resize_images":
        render_resize_images_tool()
        return
    if escolha == "build_utf-8":
        render_build_utf8_tool()
        return
    if escolha == "help_?":
        st.text(_tools_help_text())
        return
    mapa = {
        "novo_tema": (novo_tema, (novo_tema_nome, novo_tema_livro, novo_tema_banco)),
        "remove_tema": (remove_tema, (tema_remove,)),
        "update_tema": (update_tema, (tema_update,)),
        "update_rodape": (update_rodape, (tema_rodape,)),
        "build_indexy": (builders.build_indexy, ()),
        "build_lexico": (builders.build_lexico, ()),
        "build_off-lex": (build_off_lex, ()),
        "build_matrix": (builders.build_matrix, ()),
        "build_dna": (builders.build_dna, ()),
        "build_all": (build_all, ()),
        "ficha_lexico": (build_ficha_lexica, ()),
    }
    func, args = mapa[escolha]
    if st.button(escolha, use_container_width=True):
        with st.spinner(escolha + "..."):
            try:
                resultado = func(*args)
                st.success(escolha + " concluído.")
                st.text(resultado)
            except Exception as exc:
                st.error(f"{escolha} falhou: {exc}")

def show_tools(host_globals=None):
    """Entrada pública canônica chamada por basico.py no Atelier LOCAL."""
    _bind_host(host_globals)
    return page_tools()


def render_page(host_globals=None):
    """Compatibilidade histórica; delega para a entrada pública canônica."""
    return show_tools(host_globals)
