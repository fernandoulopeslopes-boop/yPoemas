import os
import re
import time


def _project_path(*parts):
    """Resolve caminho tanto pelo diretório de execução quanto pelo diretório do .py."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(os.getcwd(), *parts),
        os.path.join(here, *parts),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return candidates[0]


def _tools_resolve_ypo_path(tema):
    tema = str(tema or "").strip()
    candidatos = [
        _project_path("data", tema + ".ypo"),
        _project_path("data", tema + ".YPO"),
    ]
    for path in candidatos:
        if os.path.exists(path):
            return path
    return candidatos[0]


def build_tools_utf8_temas():
    """Verifica UTF-8 em base/ativos.txt e em todos os temas ativos, sem alterar arquivos."""
    start_time = time.time()
    problemas = []
    verificados = 0

    ativos_path = _project_path("base", "ativos.txt")
    try:
        with open(ativos_path, encoding="utf-8") as file:
            ativos_linhas = file.read().splitlines()
    except UnicodeDecodeError as exc:
        return (
            "UTF-8 temas: falha em ./base/ativos.txt\n"
            f"arquivo: {ativos_path}\n"
            f"posição: {exc.start}\n"
            f"erro: {exc}"
        )

    for raw in ativos_linhas:
        linha = raw.strip()
        if not linha:
            continue
        tema = linha.partition(" : ")[0].strip()
        if not tema:
            continue
        path = _tools_resolve_ypo_path(tema)
        if not os.path.exists(path):
            problemas.append(f"não encontrado: {path}")
            continue
        try:
            with open(path, encoding="utf-8") as file:
                file.read()
            verificados += 1
        except UnicodeDecodeError as exc:
            problemas.append(
                f"UTF-8 inválido: {path} | posição {exc.start} | {exc}"
            )

    if problemas:
        return (
            f"UTF-8 temas: {len(problemas)} problema(s) encontrado(s).\n"
            + "\n".join(problemas)
            + f"\nRuntime: {time.time() - start_time:.2f}s"
        )

    return f"UTF-8 temas: OK. {verificados} tema(s) ativo(s) verificado(s). Runtime: {time.time() - start_time:.2f}s"

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


def _tools_temas_ativos():
    temas = []
    ativos_path = _project_path("base", "ativos.txt")
    with open(ativos_path, encoding="utf-8") as file:
        for raw in file:
            linha = raw.strip("\n")
            if not linha.strip():
                continue
            tema = linha.partition(" : ")[0].strip()
            if tema:
                temas.append((tema, _tools_resolve_ypo_path(tema)))
    return temas


def _tools_linhas_ypo(path):
    """Lê linhas estruturais do .YPO em UTF-8 estrito, informando arquivo se falhar."""
    try:
        with open(path, encoding="utf-8") as file:
            for line in file:
                if line.startswith("|"):
                    yield line.rstrip("\n").split("|")
    except UnicodeDecodeError as exc:
        raise UnicodeDecodeError(
            exc.encoding,
            exc.object,
            exc.start,
            exc.end,
            f"{exc.reason} em {path}"
        ) from exc


def _tools_payload_itimos(campos):
    """Retorna apenas os ítimos autorais da linha estrutural."""
    if len(campos) <= 8:
        return []
    return [item for item in campos[7:-1] if item != ""]


def _tools_palavras_de_itimo(itimo, minimo=1):
    """Separa verbetes, preservando formas hifenizadas como manda-se."""
    texto = str(itimo or "").casefold()
    palavras = re.findall(r"[^\W_]+(?:-[^\W_]+)*", texto, flags=re.UNICODE)
    return [palavra for palavra in palavras if len(palavra) >= int(minimo)]


def build_tools_lexico():
    """Regera léxico textual a partir dos temas, sem alterar .ypo."""
    start_time = time.time()
    linhas_lexico = []
    vistos_lexico = set()
    verbetes = []
    vistos_verbetes = set()

    for tema, path in _tools_temas_ativos():
        if not os.path.exists(path):
            continue
        for campos in _tools_linhas_ypo(path):
            if len(campos) < 8:
                continue
            fonte = campos[3]
            for itimo in _tools_payload_itimos(campos):
                for palavra in _tools_palavras_de_itimo(itimo, minimo=3):
                    chave = palavra + " : " + fonte
                    if chave not in vistos_lexico:
                        vistos_lexico.add(chave)
                        linhas_lexico.append(chave)
                    if palavra not in vistos_verbetes:
                        vistos_verbetes.add(palavra)
                        verbetes.append(palavra)

    base_dir = _project_path("base")
    texto_lexico = "\n".join(sorted(linhas_lexico)) + "\n"
    texto_verbetes = "\n".join(sorted(verbetes)) + "\n"
    _tools_write_text(os.path.join(base_dir, "lexico_pt.txt"), texto_lexico)
    _tools_write_text(os.path.join(base_dir, "verbetes.txt"), texto_verbetes)
    return (
        f"Build_Léxico: {len(linhas_lexico)} verbete(s)-fonte; "
        f"{len(verbetes)} verbete(s) únicos. "
        f"Runtime: {time.time() - start_time:.2f}s"
    )

BUILD_INDEXY_FILE = "ABOUT_index.MD"
BUILD_ESCALA = [
    "mil", "milhões", "bilhões", "trilhões", "quatrilhões", "quintilhões",
    "sextilhões", "setilhões", "octilhões", "nonilhões", "decilhões",
    "undecilhões", "dodecilhões", "tredecilhões", "quatuordecilhões",
    "quindecilhões", "sedecilhões", "septendecilhões",
]


def _tools_potencia_nome(valor):
    num = f"{int(valor):,}"
    pontos = num.count(",") - 1
    if 0 <= pontos < len(BUILD_ESCALA):
        return BUILD_ESCALA[pontos]
    return "nonono"


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


def build_tools_indexy():
    start_time = time.time()
    temas = _tools_temas_ativos()
    index_list = []
    error_list = []
    acm_variatio = 0
    for tema, path in temas:
        try:
            qtd_variatio = _tools_calcular_variacoes_tema(path)
            acm_variatio += qtd_variatio
            index_list.append(f"{tema} : {qtd_variatio:,} ({_tools_potencia_nome(qtd_variatio)})")
        except Exception as exc:
            error_list.append(f"{tema}: {exc}")

    md_dir = _project_path("md_files")
    about_index = os.path.join(md_dir, BUILD_INDEXY_FILE)
    linhas = []
    linhas.append("variações para cada tema:  ")
    linhas.append("___  ")
    for linha in index_list:
        linhas.append(linha.replace(",", ".") + "  ")
    linhas.extend([
        "___",
        "[escala dos nomes das potências de 10]  ",
        "  ",
        "> mil=1.000|10e3|  ",
        "> milhão=1.000.000|10e6|  ",
        "> bilhão=1.000.000.000|10e9|  ",
        "> trilhão=1.000.000.000.000|10e12|  ",
        "> quatrilhão=1.000.000.000.000.000|10e15|  ",
        "> quintilhão=1.000.000.000.000.000.000|10e18|  ",
        "> sextilhão=1.000.000.000.000.000.000.000|10e21|  ",
        "> setilhão=1.000.000.000.000.000.000.000.000|10e24|  ",
        "> octilhão=1.000.000.000.000.000.000.000.000.000|10e27|  ",
        "> nonilhão=1.000.000.000.000.000.000.000.000.000.000|10e30|  ",
        "> decilhão=1.000.000.000.000.000.000.000.000.000.000.000|10e33|  ",
        "> undecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000|10e36|  ",
        "> dodecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000|10e39|  ",
        "> tredecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000.000|10e42|  ",
        "> quatordecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000|10e45|  ",
        "> quindecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000|10e48|  ",
        "> sedecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000|10e51|  ",
        "> septendecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000|10e54|  ",
        "> googol=dez duotrigintilhões|10e100|  ",
        "> googolplexo=quanto dá isso?|10e googol|  ",
        "> googolplexiano=por enquanto, o maior número com nome|10e googolplexo|  ",
        "  ",
        "[fonte dos dados](http://www.fisica-interessante.com/matematica-divertida-ordens-classes-multiplos.html)  ",
        "___",
        "Copyright © 1983-2022 Nando Lopes - **yPoemas @ máquina de fazer Poesia**  ",
        "",
        f"Total de variações: {acm_variatio:,} ({_tools_potencia_nome(acm_variatio)})".replace(",", "."),
        "",
    ])
    _tools_write_text(about_index, "\n".join(linhas))
    extra = f" Erros: {len(error_list)}." if error_list else ""
    return f"Build_Indexy: {len(index_list)} tema(s). Saída: {about_index}.{extra} Runtime: {time.time() - start_time:.2f}s"

