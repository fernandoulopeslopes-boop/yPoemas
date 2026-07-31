"""Página Utils local da Machina.

Este módulo contém apenas o código específico da página Utils. Ele é carregado
exclusivamente por ypo_utils.py. A base do aplicativo permanece em ypo_mobile.py.
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
import streamlit as st
import builders

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
    """Disponibiliza à página Utils as funções comuns da base ypo_mobile."""
    if not host_globals:
        return
    for name, value in host_globals.items():
        if not name.startswith("__"):
            globals()[name] = value

def _utils_fmt_int(valor):
    return f"{int(valor):,}".replace(",", ".")

def _utils_potencia_nome(valor):
    num = f"{int(valor):,}"
    pontos = num.count(",") - 1
    if 0 <= pontos < len(BUILD_ESCALA):
        return BUILD_ESCALA[pontos]
    return "nonono"

def _utils_backup_path(path):
    """Cria backup local antes de qualquer gravação derivada/cadastral."""
    if not os.path.exists(path):
        return ""
    backup_dir = _project_path("backups", "local_utils")
    os.makedirs(backup_dir, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    base = os.path.basename(path)
    dst = os.path.join(backup_dir, f"{stamp}_{base}")
    with open(path, "rb") as src, open(dst, "wb") as out:
        out.write(src.read())
    return dst

def _utils_write_text(path, texto):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    _utils_backup_path(path)
    with open(path, "w", encoding="utf-8") as file:
        file.write(texto)

def _utils_insert_rol_tema_alfabetico(path, tema, zodiac_count=24):
    """Insere um tema no índice alfabético, preservando o subíndice final do Zodíaco."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tema = str(tema or "").strip()
    if not tema:
        return False

    def chave_alfabetica(nome):
        nome = unicodedata.normalize("NFKD", str(nome).strip().casefold())
        return "".join(ch for ch in nome if not unicodedata.combining(ch))

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", newline="") as file:
            linhas = file.readlines()
    else:
        linhas = []

    tema_key = tema.casefold()
    linhas_com_tema = [i for i, raw in enumerate(linhas) if raw.strip()]
    for i in linhas_com_tema:
        if linhas[i].strip().casefold() == tema_key:
            return False

    if len(linhas_com_tema) >= zodiac_count:
        inicio_zodiaco = linhas_com_tema[-zodiac_count]
    else:
        inicio_zodiaco = len(linhas)

    posicao = inicio_zodiaco
    nova_chave = chave_alfabetica(tema)
    for i in linhas_com_tema:
        if i >= inicio_zodiaco:
            break
        if chave_alfabetica(linhas[i]) > nova_chave:
            posicao = i
            break

    quebra = "\n"
    for raw in linhas:
        if raw.endswith("\r\n"):
            quebra = "\r\n"
            break
        if raw.endswith("\n"):
            quebra = "\n"
            break

    if posicao > 0 and linhas and not linhas[posicao - 1].endswith(("\n", "\r")):
        linhas[posicao - 1] += quebra

    linhas.insert(posicao, tema + quebra)
    _utils_backup_path(path)
    with open(path, "w", encoding="utf-8", newline="") as file:
        file.writelines(linhas)
    return True

def _utils_add_unique_line(path, line, key):
    """Adiciona linha se a chave ainda não existir. Preserva o arquivo fora disso."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    line = str(line).rstrip("\n")
    key = str(key).casefold().strip()
    linhas = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as file:
            linhas = file.read().splitlines()

    for raw in linhas:
        parte = raw.partition(" : ")[0].strip().casefold()
        if not parte and raw.startswith("|"):
            campos = raw.split("|")
            if len(campos) > 1:
                parte = campos[1].strip().casefold()
        if parte == key or raw.strip().casefold() == key:
            return False

    _utils_backup_path(path)
    with open(path, "a", encoding="utf-8") as file:
        if linhas and linhas[-1] != "":
            file.write("\n")
        file.write(line + "\n")
    return True

def _utils_resolve_ypo_path(tema):
    tema = str(tema or "").strip()
    candidatos = [
        _project_path("data", tema + ".ypo"),
        _project_path("data", tema + ".YPO"),
    ]
    for path in candidatos:
        if os.path.exists(path):
            return path
    return candidatos[0]

def _utils_temas_ativos():
    temas = []
    ativos_path = _project_path("base", "ativos.txt")
    with open(ativos_path, encoding="utf-8") as file:
        for raw in file:
            linha = raw.strip("\n")
            if not linha.strip():
                continue
            tema = linha.partition(" : ")[0].strip()
            if tema:
                temas.append((tema, _utils_resolve_ypo_path(tema)))
    return temas

def _utils_temas_para_remover():
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
        for tema, path in _utils_temas_ativos():
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

def _utils_linhas_ypo(path):
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

def _utils_payload_itimos(campos):
    """Retorna apenas os ítimos autorais da linha estrutural.

    Após o split por |, campos[5] é a quantidade declarada de ítimos e
    campos[6] é metadado histórico. O conteúdo autoral começa em campos[7].
    """
    if len(campos) <= 8:
        return []
    return [item for item in campos[7:-1] if item != ""]

def _utils_qtd_itimos_declarada(campos):
    """Quantidade de ítimos da linha: elemento #5 do registro .ypo."""
    try:
        return max(0, int(str(campos[5]).strip()))
    except Exception:
        return 0

def _utils_normaliza_unico(texto):
    return re.sub(r"\s+", " ", str(texto or "").strip().casefold())

def _utils_palavras_de_itimo(itimo, minimo=1):
    """Separa verbetes, preservando formas hifenizadas como manda-se.

    A contagem técnica do tema aceita verbetes de qualquer tamanho.
    O Build_Léxico chama esta função com minimo=3, pois a Eureka só busca
    sementes com três ou mais letras.
    """
    texto = str(itimo or "").casefold()
    palavras = re.findall(r"[^\W_]+(?:-[^\W_]+)*", texto, flags=re.UNICODE)
    return [palavra for palavra in palavras if len(palavra) >= int(minimo)]

def _utils_calcular_variacoes_tema(path):
    fontes_list = []
    corrige_qtd = 1
    qtd_itimos_list = []
    for campos in _utils_linhas_ypo(path):
        if len(campos) >= 8:
            nova_fonte = campos[3]
            total_itimos = len(_utils_payload_itimos(campos))
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

def _utils_matrix_um_tema(tema, path):
    try:
        import numpy as np
        import matplotlib.pyplot as plt
    except Exception as exc:
        raise RuntimeError(f"dependência ausente ou indisponível: {exc}")

    tabela = tema.capitalize()  # comportamento histórico do Build_Matrix.
    matrix_dir = _project_path("images", "matrix")
    os.makedirs(matrix_dir, exist_ok=True)
    curlin = "01"
    linini = 1
    itimos_acm = 0
    x_pos = np.array([]); y_pos = np.array([]); z_pos = np.array([]); z_val = np.array([])

    with open(path, encoding="utf-8") as file:
        for line in file:
            if line.startswith("|", 0, 1):
                campos = line.split("|")
                if len(campos) < 6:
                    continue
                newcol = int(campos[2])
                if campos[1] != curlin:
                    linini += 1
                    curlin = campos[1]
                if newcol == 0:
                    x_pos = np.append(x_pos, linini); y_pos = np.append(y_pos, 0); z_pos = np.append(z_pos, 0); z_val = np.append(z_val, 0)
                else:
                    itimos = int(campos[5])
                    itimos_acm += itimos
                    x_pos = np.append(x_pos, linini - 1); y_pos = np.append(y_pos, newcol - 1); z_pos = np.append(z_pos, 0); z_val = np.append(z_val, itimos)

    x_val = np.ones(len(x_pos)); y_val = np.ones(len(y_pos)); z_pos = np.ones(len(z_pos))
    if len(x_val) > 0:
        fg = plt.figure(figsize=(7, 7))
        ax = fg.add_subplot(111, projection="3d")
        ax.set_xlabel("x ➪ linhas", fontsize=14)
        ax.set_ylabel("y ➪ versos", fontsize=14)
        ax.set_zlabel("z ➪ ítimos", fontsize=14)
        ax.view_init(elev=30, azim=-30)
        ax.bar3d(x_pos, y_pos, z_pos, x_val, y_val, z_val, color="#00ccaa", alpha=0.85, edgecolor="k")
        plt.savefig(os.path.join(matrix_dir, tabela + ".jpg"), dpi=50)
        plt.close(fg)
    return tabela, linini, itimos_acm

def _utils_atualizar_linha_chave(path, chave, nova_linha):
    linhas = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as file:
            linhas = file.read().splitlines()
    chave_norm = str(chave).casefold().strip()
    nova_linha = str(nova_linha).strip()
    saida = []
    alterou = False
    for linha in linhas:
        parte = linha.partition(" : ")[0].strip().casefold()
        if parte == chave_norm:
            if not alterou:
                saida.append(nova_linha)
                alterou = True
            continue
        saida.append(linha)
    if not alterou:
        saida.append(nova_linha)
    _utils_write_text(path, "\n".join(saida).rstrip() + "\n")

def build_matrix(tema_unico=None):
    start_time = time.time()
    temas = _utils_temas_ativos()
    if tema_unico:
        temas = [(tema, path) for tema, path in temas if tema == tema_unico]
    lista_itimos = []
    lista_versos = []
    for tema, path in temas:
        if not os.path.exists(path):
            continue
        tabela, versos, itimos = _utils_matrix_um_tema(tema, path)
        lista_versos.append(f"{tabela} : {versos}")
        lista_itimos.append(f"{tabela} : {itimos}")

    base_dir = _project_path("base")
    if tema_unico:
        for linha in lista_itimos:
            chave = linha.partition(" : ")[0]
            _utils_atualizar_linha_chave(os.path.join(base_dir, "itimos.txt"), chave, linha)
        for linha in lista_versos:
            chave = linha.partition(" : ")[0]
            _utils_atualizar_linha_chave(os.path.join(base_dir, "versos.txt"), chave, linha)
    else:
        _utils_write_text(os.path.join(base_dir, "itimos.txt"), "\n".join(lista_itimos).rstrip() + "\n")
        _utils_write_text(os.path.join(base_dir, "versos.txt"), "\n".join(lista_versos).rstrip() + "\n")
    modo = f"tema {tema_unico}" if tema_unico else "todos os temas"
    return f"Build_Matrix: {modo}; {len(lista_itimos)} Matrix 3D gerada(s)/atualizada(s). Runtime: {time.time() - start_time:.2f}s"

def build_ficha_lexica():
    start_time = time.time()
    temas = _utils_temas_ativos()
    total_itimos = 0
    itimos_unicos = set()
    total_verbetes = 0
    verbetes_unicos = set()
    for tema, path in temas:
        if not os.path.exists(path):
            continue
        for campos in _utils_linhas_ypo(path):
            total_itimos += _utils_qtd_itimos_declarada(campos)
            for itimo in _utils_payload_itimos(campos):
                itimos_unicos.add(_utils_normaliza_unico(itimo))
                palavras = _utils_palavras_de_itimo(itimo, minimo=1)
                total_verbetes += len(palavras)
                verbetes_unicos.update(palavras)
    try:
        total_temas_ficha = len([tema for tema in load_temas("todos os temas") if str(tema).strip()])
    except Exception:
        total_temas_ficha = len(temas)

    bloco = (
        f"{BUILD_AMBIENTE_LEXICO}\n\n"
        f"Total de Verbetes: {_utils_fmt_int(total_verbetes)}\n"
        f"Total de Verbetes únicos: {_utils_fmt_int(len(verbetes_unicos))}\n\n"
        f"Total de Ítimos: {_utils_fmt_int(total_itimos)}\n"
        f"Total de Ítimos únicos: {_utils_fmt_int(len(itimos_unicos))}\n\n"
        f"Total de Temas: {_utils_fmt_int(total_temas_ficha)}\n"
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
    _utils_write_text(index_path, texto)
    return f"Ficha Léxica atualizada em {index_path}. Runtime: {time.time() - start_time:.2f}s\n\n{bloco}"

def _utils_imagem_tema(tema):
    """Busca o grupo de imagem do tema em ./base/images.txt, sem depender de módulos externos."""
    tema_norm = str(tema or "").strip().casefold()
    images_path = _project_path("base", "images.txt")
    if os.path.exists(images_path):
        with open(images_path, encoding="utf-8") as file:
            for raw in file:
                linha = raw.strip()
                if not linha:
                    continue
                nome, sep, resto = linha.partition(" : ")
                if nome.strip().casefold() == tema_norm and sep:
                    return resto.strip() or "Machina"
    return "Machina"

def _utils_info_tema(tema, path):
    """Calcula a linha técnica de ./base/info.txt para um tema ativo.

    Fonte única dos temas: ./base/ativos.txt.
    Não importa build_info.py nem tools.py.
    Não altera .YPO; apenas lê estrutura e escreve documentação derivada.
    """
    genero = "Machina"
    imagem = _utils_imagem_tema(tema)
    versos = 0
    qtd_itimos = 0
    verbetes_tema = set()
    verbetes_no_texto = 0

    curlin = ""
    for campos in _utils_linhas_ypo(path):
        if len(campos) < 8:
            continue

        # Cada linha estrutural oferece uma escolha ao texto gerado.
        verbetes_no_texto += 1

        linha_id = campos[1].strip() if len(campos) > 1 else ""
        if linha_id and linha_id != curlin:
            versos += 1
            curlin = linha_id

        # Total de ítimos: soma cega do elemento #5 de todas as linhas.
        qtd_itimos += _utils_qtd_itimos_declarada(campos)

        # Verbetes do Tema: lista única das palavras contidas nos ítimos.
        # Artigos e palavras curtas contam aqui; formas hifenizadas não se partem.
        for itimo in _utils_payload_itimos(campos):
            verbetes_tema.update(_utils_palavras_de_itimo(itimo, minimo=1))

    qtd_wordin = verbetes_no_texto
    qtd_lexico = len(verbetes_tema)
    qtd_variatio = _utils_calcular_variacoes_tema(path)
    qtd_cienti = f"{qtd_variatio:.2e}"

    return (
        f"|{tema}|{genero}|{imagem}|{versos}|{qtd_wordin}|"
        f"{qtd_lexico}|{qtd_itimos}|{qtd_variatio}|{qtd_cienti}|"
    )

def _utils_dados_rodape_ypo(path):
    """Calcula apenas o rodapé informativo do .YPO, sem alterar corpo poético."""
    verbetes_no_texto = 0
    total_itimos = 0
    verbetes_tema = set()

    for campos in _utils_linhas_ypo(path):
        if len(campos) < 8:
            continue
        verbetes_no_texto += 1
        total_itimos += _utils_qtd_itimos_declarada(campos)
        for itimo in _utils_payload_itimos(campos):
            verbetes_tema.update(_utils_palavras_de_itimo(itimo, minimo=1))

    total_verbetes = len(verbetes_tema)
    qtd_variacoes = _utils_calcular_variacoes_tema(path)
    return {
        "verbetes_no_texto": verbetes_no_texto,
        "total_itimos": total_itimos,
        "total_verbetes": total_verbetes,
        "qtd_variacoes": qtd_variacoes,
    }

def _utils_linhas_rodape_ypo(path):
    dados = _utils_dados_rodape_ypo(path)
    variacoes = dados["qtd_variacoes"]
    return [
        f"Verbetes no Texto = {dados['verbetes_no_texto']}",
        f"  Total de ítimos = {dados['total_itimos']}",
        f"Total de verbetes = {dados['total_verbetes']}",
        f"Qtd. de Variações = {_utils_fmt_int(variacoes)} ({_utils_potencia_nome(variacoes)})",
    ]

def _utils_atualizar_rodape_ypo_um_tema(tema, path):
    """Preserva integralmente o .ypo e substitui somente sua última linha de build."""
    with open(path, encoding="utf-8") as file:
        linhas = file.read().splitlines()
    if not linhas:
        return f"{tema}: arquivo vazio"

    ultima = linhas[-1].strip()
    chave = ultima.casefold()
    if not (chave.startswith("build_by_lay_2_ypo") or chave.startswith("build_by lay_2_ypo")):
        return f"{tema}: última linha de build não encontrada"

    nova = time.strftime("build_by lay_2_ypo em %d/%m/%Y - %H:%M")
    if linhas[-1] == nova:
        return f"{tema}: sem alteração"
    linhas[-1] = nova
    _utils_write_text(path, "\n".join(linhas) + "\n")
    return f"{tema}: atualizado"


def build_atualizar_rodape_ypo(tema_unico=None):
    """Atualiza rodapé informativo dos .YPO sob demanda, localmente."""
    start_time = time.time()
    temas = _utils_temas_ativos()
    if tema_unico:
        temas = [(tema, path) for tema, path in temas if tema == tema_unico]
        if not temas:
            return f"atualizar_rodape_ypo: tema não encontrado em ./base/ativos.txt: {tema_unico}"

    resultados = []
    erros = []
    for tema, path in temas:
        if not os.path.exists(path):
            erros.append(f"{tema}: arquivo não encontrado ({path})")
            continue
        try:
            resultados.append(_utils_atualizar_rodape_ypo_um_tema(tema, path))
        except Exception as exc:
            erros.append(f"{tema}: {exc}")

    try:
        st.cache_data.clear()
    except Exception:
        pass

    alvo = f"tema {tema_unico}" if tema_unico else "todos os temas ativos"
    msg = f"atualizar_rodape_ypo: {alvo}; {len(resultados)} tema(s). Runtime: {time.time() - start_time:.2f}s"
    if resultados:
        msg += "\n" + "\n".join(resultados)
    if erros:
        msg += "\nErros:\n" + "\n".join(erros)
    return msg

def build_info():
    """Atualiza ./base/info.txt pela Central local, lendo diretamente ./base/ativos.txt."""
    start_time = time.time()
    linhas = []
    erros = []

    for tema, path in _utils_temas_ativos():
        if not os.path.exists(path):
            erros.append(f"{tema}: arquivo não encontrado ({path})")
            continue
        try:
            linhas.append(_utils_info_tema(tema, path))
        except Exception as exc:
            erros.append(f"{tema}: {exc}")

    info_path = _project_path("base", "info.txt")
    _utils_write_text(info_path, "\n".join(linhas).rstrip() + "\n")

    msg = f"Build_Info: {len(linhas)} tema(s) em ./base/info.txt. Runtime: {time.time() - start_time:.2f}s"
    if erros:
        msg += "\nErros:\n" + "\n".join(erros)
    return msg

def build_update(tema):
    """Atualiza derivados de tema já existente."""
    tema = str(tema or "").strip()
    temas = dict(_utils_temas_ativos())
    if tema not in temas:
        return "Build_update: tema não encontrado em ./base/ativos.txt."
    if not os.path.exists(temas[tema]):
        return f"Build_update: arquivo do tema não encontrado: {temas[tema]}"
    resultados = [
        builders.build_lexico(),
        build_matrix(tema),
        build_atualizar_rodape_ypo(tema),
        builders.build_indexy(),
        build_ficha_lexica(),
        build_info(),
    ]
    try:
        st.cache_data.clear()
    except Exception:
        pass
    return "\n\n".join(resultados)

def build_novo_tema(tema):
    """Cadastro técnico de novo tema já criado pelo autor em ./data.

    Fonte única para ativação e grupo de imagens: ./base/ativos.txt.
    """
    tema = str(tema or "").strip()
    if not tema:
        return "Build_Novo_Tema: informe o nome do tema."
    if any(sep in tema for sep in ("/", "\\", ":", "*", "?", '"', "<", ">", "|")):
        return "Build_Novo_Tema: nome de tema contém caractere inválido para arquivo."
    ypo_path = _utils_resolve_ypo_path(tema)
    if not os.path.exists(ypo_path):
        return f"Build_Novo_Tema: crie antes o arquivo autoral em ./data/{tema}.YPO ou ./data/{tema}.ypo. Nada foi cadastrado."

    alteracoes = []
    if _utils_add_unique_line(_project_path("base", "ativos.txt"), f"{tema} : Machina", tema):
        alteracoes.append("base/ativos.txt")
    if _utils_add_unique_line(_project_path("temp", "readings.txt"), f"|{tema}|0|", tema):
        alteracoes.append("temp/readings.txt")
    if _utils_insert_rol_tema_alfabetico(
        _project_path("base", "rol_todos os temas.txt"), tema
    ):
        alteracoes.append("base/rol_todos os temas.txt")

    resultados = [
        "Build_Novo_Tema: cadastro técnico verificado.",
        "Arquivos cadastrais alterados: " + (", ".join(alteracoes) if alteracoes else "nenhum; tema já estava cadastrado"),
        build_update(tema),
    ]
    return "\n\n".join(resultados)

def _utils_remove_linhas_por_tema(path, tema):
    """Remove linhas cadastrais/derivadas relacionadas a um tema. Retorna qtd removida."""
    tema_norm = str(tema or "").strip().casefold()
    if not tema_norm or not os.path.exists(path):
        return 0

    with open(path, encoding="utf-8") as file:
        linhas = file.read().splitlines()

    saida = []
    removidas = 0
    for raw in linhas:
        raw_strip = raw.strip()
        chave = raw_strip.partition(" : ")[0].strip().casefold()

        if raw_strip.startswith("|"):
            campos = raw_strip.split("|")
            if len(campos) > 1:
                chave = campos[1].strip().casefold()

        remove = False
        if chave == tema_norm:
            remove = True
        elif raw_strip.casefold() == tema_norm:
            remove = True

        if remove:
            removidas += 1
        else:
            saida.append(raw)

    if removidas:
        _utils_write_text(path, "\n".join(saida).rstrip() + ("\n" if saida else ""))
    return removidas

def _utils_remover_arquivo(path):
    """Remove arquivo se existir. Retorna True/False."""
    if path and os.path.exists(path) and os.path.isfile(path):
        os.remove(path)
        return True
    return False

def build_remove_tema(tema):
    """Remove tecnicamente um tema do ambiente local e atualiza derivados."""
    tema = str(tema or "").strip()
    if not tema:
        return "remove_tema: escolha um tema."

    ypo_path = _utils_resolve_ypo_path(tema)
    removidos = []

    # Listas cadastrais e derivadas simples.
    arquivos_lista = [
        _project_path("base", "ativos.txt"),
        _project_path("temp", "readings.txt"),
        _project_path("base", "itimos.txt"),
        _project_path("base", "versos.txt"),
    ]

    base_dir = _project_path("base")
    if os.path.isdir(base_dir):
        for name in sorted(os.listdir(base_dir)):
            if name.lower().startswith("rol_") and name.lower().endswith(".txt"):
                arquivos_lista.append(os.path.join(base_dir, name))

    vistos = set()
    for path in arquivos_lista:
        if path in vistos:
            continue
        vistos.add(path)
        qtd = _utils_remove_linhas_por_tema(path, tema)
        if qtd:
            removidos.append(f"{os.path.relpath(path, _project_path())}: {qtd} linha(s)")

    # Imagem Matrix derivada do tema, se existir.
    matrix_dir = _project_path("images", "matrix")
    matrix_candidates = {
        os.path.join(matrix_dir, tema + ".jpg"),
        os.path.join(matrix_dir, tema.capitalize() + ".jpg"),
        os.path.join(matrix_dir, tema + ".JPG"),
        os.path.join(matrix_dir, tema.capitalize() + ".JPG"),
    }
    for candidate in sorted(matrix_candidates):
        if _utils_remover_arquivo(candidate):
            removidos.append(f"{os.path.relpath(candidate, _project_path())}: removido")

    # Arquivo autoral do tema. remove_tema é ação explícita do usuário.
    ypo_removido = False
    for candidate in [ypo_path, _project_path("data", tema + ".ypo"), _project_path("data", tema + ".YPO")]:
        if _utils_remover_arquivo(candidate):
            removidos.append(f"{os.path.relpath(candidate, _project_path())}: removido")
            ypo_removido = True

    resultados = [
        f"remove_tema: {tema}",
        "Alterações: " + ("\n" + "\n".join(removidos) if removidos else "nenhuma ocorrência encontrada"),
    ]

    # Recria derivados que dependem do conjunto ativo restante.
    resultados.extend([
        builders.build_lexico(),
        builders.build_indexy(),
        build_ficha_lexica(),
        build_info(),
    ])

    try:
        st.cache_data.clear()
    except Exception:
        pass

    if not ypo_removido:
        resultados.insert(2, "Arquivo .YPO/.ypo não encontrado em ./data; listas/derivados foram tratados mesmo assim.")

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
    _utils_write_text(os.path.join(off_dir, "off_lexico.txt"), "".join("|" + line + "|\n" for line in list_lexico))
    _utils_write_text(os.path.join(off_dir, "off_verbet.txt"), "".join(line + "\n" for line in list_verbet))
    return f"Build_Off_Lex: {len(list_lexico)} ocorrência(s); {len(list_verbet)} verbete(s). Runtime: {time.time() - start_time:.2f}s"

def build_all():
    """Reconstrói todos os derivados da Machina, inclusive rodapés dos temas."""
    resultados = [
        builders.build_lexico(),
        build_matrix(),
        build_atualizar_rodape_ypo(),
        builders.build_indexy(),
        build_ficha_lexica(),
        build_info(),
    ]
    try:
        st.cache_data.clear()
    except Exception:
        pass
    return "\n\n".join(resultados)

def _utils_run_button(label, func, *args):
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

def _build_rimas_decode_uploaded(uploaded_file):
    data = uploaded_file.getvalue()
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")

def build_unicos_texto(text, mode="lower", min_len=1):
    """Devolve lista alfabética de verbetes únicos a partir de texto colado."""
    words = _build_rimas_extract_words(text, mode=mode, min_len=max(1, int(min_len)))
    return _build_rimas_render_list(_build_rimas_sorted_words(words))

def render_build_unicos_tool():
    """Ferramenta local da Off Sina para extrair verbetes únicos."""
    st.markdown("### Build_unicos")
    st.caption("Off Sina: cole um texto; recebe uma lista alfabética de verbetes únicos.")

    pasted_text = st.text_area(
        "colar texto / área de descarte",
        value=st.session_state.get("build_unicos_pasted_text", ""),
        height=220,
        key="build_unicos_pasted_text",
        placeholder="Ctrl+V aqui basta para carregar o texto...",
    )

    case_mode = st.selectbox(
        "caixa",
        ["lower", "upper", "preserve"],
        index=0,
        key="build_unicos_case",
    )

    pasted_text = str(pasted_text or "")
    if not pasted_text.strip():
        st.info("Cole um texto com Ctrl+V na área de descarte.")
        return

    if st.button("Build_unicos", use_container_width=True):
        lista = build_unicos_texto(pasted_text, mode=case_mode, min_len=1)
        st.session_state["build_unicos_result"] = lista
        st.success("Build_unicos concluído.")

    resultado = st.session_state.get("build_unicos_result", "")
    if resultado:
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


def build_atelier_texto(
    text,
    usar_lema=True,
    mode="lower",
    min_len=2,
    min_suffix=2,
    max_suffix=6,
):
    """Análise lexical integrada: gramática + mapa de rimas da Machina.

    Não altera arquivos, listas, temas ou poesia. O resultado é material de
    atelier para conferência e curadoria do autor.
    """
    texto = str(text or "")
    if not texto.strip():
        raise ValueError("o texto do Atelier está vazio.")

    classificacao = _atelier_classificar_palavras(
        texto,
        usar_lema=bool(usar_lema),
        mode=mode,
        min_len=min_len,
    )
    mapa_rimas = build_rimas_texto(
        texto,
        mode=mode,
        min_len=min_len,
        min_suffix=min_suffix,
        max_suffix=max_suffix,
    )

    texto_final = "\n\n".join([
        "Build_Atelier",
        "___",
        _atelier_render_classificacao(classificacao),
        "___",
        mapa_rimas,
    ])
    return {
        "classificacao_gramatical": classificacao,
        "texto": texto_final,
    }


def _atelier_json(resultado):
    return json.dumps(
        {
            "build": "Build_Atelier",
            "classificacao_gramatical": resultado["classificacao_gramatical"],
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
    return buffer.getvalue()


def render_build_atelier_tool():
    """Interface local do Build_Atelier."""
    st.markdown("### Build_Atelier")
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

    col_suf_min, col_suf_max = st.columns(2)
    with col_suf_min:
        min_suffix = st.selectbox(
            "sufixo mínimo", list(range(1, 8)), index=1,
            key="build_atelier_min_suffix",
        )
    with col_suf_max:
        max_suffix = st.selectbox(
            "sufixo máximo", list(range(3, 9)), index=3,
            key="build_atelier_max_suffix",
        )

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
            )
            st.session_state["build_atelier_result"] = resultado
            st.session_state["build_atelier_stem"] = source_stem
            st.success("Build_Atelier concluído.")
        except Exception as exc:
            st.error(f"Build_Atelier falhou: {exc}")

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
    """Converte texto UTF-8 em Markdown dentro dos limites escolhidos."""
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

    uploaded = st.file_uploader(
        "arquivo.ext — qualquer extensão textual em UTF-8",
        type=None,
        key="make_md_upload",
    )

    if uploaded is None:
        st.info("Escolha um arquivo textual UTF-8.")
        return

    nome_base = os.path.splitext(os.path.basename(uploaded.name))[0] or "arquivo"
    st.caption("saída: ./md_files/" + nome_base + ".md")

    if st.button("make_md", use_container_width=True):
        try:
            resultado = _make_md_texto_utf8(
                uploaded.getvalue(),
                chr_minimo=chr_minimo,
                chr_maximo=chr_maximo,
            )
            destino = _make_md_output_path(uploaded.name)
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


def _utils_help_text():
    return """help_? — Utils locais da Machina

novo_tema
  Cadastra tecnicamente um tema novo que já existe em ./data como .YPO/.ypo.
  Atualiza arquivos cadastrais necessários e depois roda update_tema.

remove_tema
  Remove tecnicamente um tema do ambiente local. A lista de remoção vem dos
  yPoemas/rol_*.txt, ativos e ./data para capturar listas desencontradas.
  Remove listas cadastrais, rol_*.txt, arquivo .YPO/.ypo e Matrix derivada,
  depois atualiza os derivados.

update_tema
  Atualiza derivados de um tema já existente em ./base/ativos.txt.
  Roda léxico, matrix do tema, rodapé informativo do .ypo, indexy, ficha_lexico e info.

atualizar_rodape_ypo
  Atualiza sob demanda as 4 linhas informativas do rodapé dos .ypo.
  Mantém a linha Build_By_Lay_2_Ipo como está.

build_indexy
  Atualiza ./md_files/ABOUT_index.MD com as variações combinatórias por tema.

build_lexico
  Regera ./base/lexico_pt.txt e ./base/verbetes.txt com verbetes de 3 ou mais letras, preservando formas hifenizadas.

build_off-lex
  Regera ./off_machina/off_lexico.txt e ./off_machina/off_verbet.txt.
  Base futura da eureka_off_machina.

build_rimas
  Off Sina: lê um .txt/.md/.doc em texto UTF-8, extrai palavras únicas e gera mapa de rimas
  para curadoria. Não altera .ypo, base, md_files nem poesia.

build_atelier
  Classifica os verbetes por classe gramatical com spaCy e usa o mapa de rimas
  da Machina. Gera saídas TXT, JSON e CSV sem alterar arquivos do ambiente.

build_matrix
  Gera as imagens Matrix 3D XYZ e atualiza ./base/itimos.txt e ./base/versos.txt.
  Requer numpy + matplotlib no ambiente local.

build_info
  Atualiza ./base/info.txt pela própria Central local, lendo diretamente ./base/ativos.txt.

build_all
  Reconstrução geral dos derivados principais: léxico, matrix, indexy, ficha_lexico e info.

ficha_lexico
  Atualiza o bloco final “Ambiente Léxico da Machina” em ./md_files/INDEX.txt.

chk_utf-8
  Verifica ./base/ativos.txt e todos os temas ativos em UTF-8 estrito.
  Não converte nem altera arquivos.

make_md
  Lê qualquer arquivo textual UTF-8, qualquer que seja a extensão, e acrescenta
  dois espaços ao fim de cada linha. Salva em ./md_files como arquivo.md;
  se o nome já existir, salva como arquivo_new.md. Arquivo binário não é convertido.

make_ola
  Envia um arquivo textual UTF-8 para uma única análise sintática da OLA.

resize_images
  Padroniza todas as imagens de uma pasta nas dimensões escolhidas, sem cortar
  nem deformar. Centraliza a imagem inteira sobre fundo configurável e salva em
  outra pasta. Os arquivos originais não são apagados nem sobrescritos.
"""

def page_local_utils():
    st.subheader("ypo_utils")
#    st.caption("LOCAL. Lista funcional simples. Lê temas; não altera poesia.")

    tools_items = [
        "novo_tema",
        "remove_tema",
        "update_tema",
        "atualizar_rodape_ypo",
        "---",
        "build_indexy",
        "build_lexico",
        "build_off-lex",
        "build_rimas",
        "build_atelier",
        "build_unicos",
        "build_matrix",
        "build_info",
        "build_all",
        "---",
        "ficha_lexico",
        "chk_utf-8",
        "make_md",
        "make_ola",
        "resize_images",
        "---",
        "help_?",
    ]

    try:
        temas_local = [tema for tema, path in _utils_temas_ativos()]
    except Exception:
        temas_local = []

    try:
        temas_remocao = _utils_temas_para_remover()
    except Exception:
        temas_remocao = temas_local

    escolha = st.selectbox(
        "utils",
        tools_items,
        index=tools_items.index("help_?"),
        key="utils_lista_funcional",
    )

    if escolha == "---":
        st.info("separador")
        return

    tema_update = None
    tema_remove = None
    tema_rodape = None
    novo_tema = ""

    if escolha == "update_tema":
        if temas_local:
            tema_update = st.selectbox(
                "tema",
                temas_local,
                key="utils_lista_update_tema",
            )
        else:
            st.warning("Nenhum tema encontrado em ./base/ativos.txt.")
            return

    elif escolha == "remove_tema":
        if temas_remocao:
            tema_remove = st.selectbox(
                "tema",
                temas_remocao,
                key="utils_lista_remove_tema",
            )
        else:
            st.warning("Nenhum tema encontrado nas listas dos yPoemas ou em ./data.")
            return

    elif escolha == "atualizar_rodape_ypo":
        opcoes_rodape = ["todos os temas"] + temas_local
        tema_rodape = st.selectbox(
            "tema",
            opcoes_rodape,
            key="utils_lista_rodape_ypo",
        )
        if tema_rodape == "todos os temas":
            tema_rodape = None

    elif escolha == "novo_tema":
        novo_tema = st.text_input(
            "novo tema já existente em ./data",
            key="utils_lista_novo_tema",
        )

    if escolha == "build_rimas":
        render_build_rimas_tool()
        return

    if escolha == "build_atelier":
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

    if escolha == "help_?":
        st.text(_utils_help_text())
        return

    mapa = {
        "novo_tema": (build_novo_tema, (novo_tema,)),
        "remove_tema": (build_remove_tema, (tema_remove,)),
        "update_tema": (build_update, (tema_update,)),
        "atualizar_rodape_ypo": (build_atualizar_rodape_ypo, (tema_rodape,)),
        "build_indexy": (builders.build_indexy, ()),
        "build_lexico": (builders.build_lexico, ()),
        "build_off-lex": (build_off_lex, ()),
        "build_matrix": (build_matrix, ()),
        "build_info": (build_info, ()),
        "build_all": (build_all, ()),
        "ficha_lexico": (build_ficha_lexica, ()),
        "chk_utf-8": (builders.build_utf8_temas, ()),
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

def render_page(host_globals=None):
    """Entrada pública chamada apenas por ypo_utils.py."""
    _bind_host(host_globals)
    return page_local_utils()
