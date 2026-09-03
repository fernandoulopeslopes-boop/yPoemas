"""Builders da Machina.

Casa dos construtores e da manutenção dos bastidores da Machina.

``build_utf8`` normaliza, sob autorização explícita, arquivos textuais
da pasta escolhida. A lista editável ``base/build_utf8.txt`` determina
as extensões que podem ser tocadas.
"""

from pathlib import Path
import shutil
import time
import re
from ypo_structure import (
    is_blank_fields as _ypo_is_blank_fields,
    payload_itimos as _ypo_payload_itimos,
    read_records as _ypo_read_records,
)


PROJECT_ROOT = Path(__file__).resolve().parent


def _project_path(*parts):
    """Monta um caminho interno da Machina a partir da raiz do projeto."""
    return PROJECT_ROOT.joinpath(*parts)


def _theme_name(tema):
    """Nome canônico do tema: .ypo é a assinatura da Machina."""
    valor = str(tema or "").strip()
    if not valor:
        return ""
    nome = Path(valor).name
    ext = Path(nome).suffix
    if not ext:
        return nome
    if ext.casefold() == ".ypo":
        return Path(nome).stem
    raise ValueError(
        f"assinatura inválida para tema da Machina: {nome}. "
        "A assinatura oficial é .ypo; confirmação explícita é necessária para outra extensão."
    )


def _resolve_ypo_path(tema):
    """Localiza Design ou Design.ypo sem duplicar a assinatura oficial."""
    tema_nome = _theme_name(tema)
    data_dir = _project_path("data")
    candidatos = (
        data_dir / (tema_nome + ".ypo"),
        data_dir / (tema_nome + ".YPO"),
    )
    for path in candidatos:
        if path.exists():
            return path

    key = tema_nome.casefold()
    if data_dir.is_dir():
        for path in data_dir.iterdir():
            if path.is_file() and path.suffix.casefold() == ".ypo" and path.stem.casefold() == key:
                return path
    return candidatos[0]


def _build_utf8_extensions_path():
    return _project_path("base", "build_utf8.txt")


def _build_utf8_load_extensions():
    """Lê a autoridade editável de extensões permitidas."""
    path = _build_utf8_extensions_path()
    if not path.is_file():
        raise FileNotFoundError(f"lista de extensões não encontrada: {path}")

    extensoes = []
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        item = raw.strip()
        if not item or item.startswith("#"):
            continue
        if not item.startswith("."):
            item = "." + item
        item = item.casefold()
        if item not in extensoes:
            extensoes.append(item)

    if not extensoes:
        raise ValueError(f"lista de extensões vazia: {path}")

    return tuple(extensoes)


def _build_utf8_old_path(path):
    return path.with_name(path.stem + "_old" + path.suffix)


def _build_utf8_decode(raw, path):
    """Decodifica apenas formatos textuais conhecidos para normalização."""
    try:
        return raw.decode("utf-8-sig"), "utf-8"
    except UnicodeDecodeError:
        pass

    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        try:
            return raw.decode("utf-16"), "utf-16"
        except UnicodeDecodeError as exc:
            raise UnicodeError(f"UTF-16 inválido: {path}: {exc}") from exc

    if b"\x00" in raw:
        raise UnicodeError(f"arquivo textual suspeito (NUL sem BOM): {path}")

    try:
        return raw.decode("cp1252"), "cp1252"
    except UnicodeDecodeError as exc:
        raise UnicodeError(
            f"codificação não reconhecida com segurança: {path}: {exc}"
        ) from exc


def build_utf8(pasta, progress_callback=None, status_callback=None):
    """
    Normaliza para UTF-8 somente os arquivos autorizados da pasta escolhida.

    Regras:
    - NÃO percorre subpastas;
    - a autoridade é base/build_utf8.txt;
    - arquivo já UTF-8 permanece intocado;
    - arquivo *_old.ext é ignorado;
    - antes da conversão, o original é preservado byte a byte como *_old.ext;
    - se *_old.ext já existe, a operação é bloqueada antes de qualquer gravação;
    - nenhuma pasta é criada, movida ou reorganizada.
    """
    start_time = time.time()
    pasta = Path(str(pasta or "").strip()).expanduser()
    if not pasta.is_absolute():
        pasta = (PROJECT_ROOT / pasta).resolve()
    else:
        pasta = pasta.resolve()

    if not pasta.is_dir():
        raise FileNotFoundError(f"pasta não encontrada: {pasta}")

    extensoes = _build_utf8_load_extensions()

    candidatos = []
    for path in sorted(pasta.iterdir(), key=lambda p: p.name.casefold()):
        if not path.is_file():
            continue
        if path.stem.casefold().endswith("_old"):
            continue
        if path.suffix.casefold() not in extensoes:
            continue
        candidatos.append(path)

    if not candidatos:
        return (
            f"build_utf-8: nenhum arquivo autorizado em {pasta}.\n"
            f"Extensões: {', '.join(extensoes)}\n"
            f"Runtime: {time.time() - start_time:.2f}s"
        )

    plano = []
    ja_utf8 = []
    erros = []
    total = len(candidatos)

    # PRE-FLIGHT: nenhuma gravação antes de validar tudo.
    for indice, path in enumerate(candidatos, start=1):
        if status_callback:
            status_callback(f"checando {indice}/{total}: {path.name}")
        try:
            raw = path.read_bytes()
            texto, origem = _build_utf8_decode(raw, path)
        except (OSError, UnicodeError) as exc:
            erros.append(str(exc))
            continue

        if origem == "utf-8":
            ja_utf8.append(path)
            continue

        old_path = _build_utf8_old_path(path)
        if old_path.exists():
            erros.append(
                f"bloqueado: {old_path.name} já existe; {path.name} não foi tocado"
            )
            continue

        novo = texto.encode("utf-8")
        if novo.decode("utf-8") != texto:
            erros.append(f"{path.name}: falha de round-trip UTF-8")
            continue

        plano.append((path, old_path, raw, novo, origem, texto))

    if erros:
        raise RuntimeError(
            "build_utf-8 PRE-FLIGHT bloqueado; nenhum arquivo foi modificado.\n"
            + "\n".join(erros)
        )

    convertidos = []
    total_plano = len(plano)

    for indice, (path, old_path, raw, novo, origem, texto) in enumerate(plano, start=1):
        if status_callback:
            status_callback(
                f"normalizando {indice}/{total_plano}: {path.name} ({origem} → UTF-8)"
            )

        # Preserva primeiro o original no próprio território.
        shutil.copy2(path, old_path)
        if old_path.read_bytes() != raw:
            raise RuntimeError(f"cópia _old não confere byte a byte: {old_path}")

        try:
            path.write_bytes(novo)
            conferido = path.read_bytes().decode("utf-8")
            if conferido != texto:
                raise RuntimeError(f"conteúdo UTF-8 não confere: {path}")
        except Exception:
            shutil.copy2(old_path, path)
            raise

        convertidos.append((path, origem))
        if progress_callback:
            progress_callback(indice, max(1, total_plano))

    if progress_callback and not plano:
        progress_callback(1, 1)

    linhas = [
        f"build_utf-8: {pasta}",
        f"autorizados verificados: {len(candidatos)}",
        f"já UTF-8: {len(ja_utf8)}",
        f"normalizados: {len(convertidos)}",
        f"extensões: {', '.join(extensoes)}",
    ]
    for path, origem in convertidos:
        linhas.append(
            f"OK: {path.name} ({origem} → UTF-8); original: {_build_utf8_old_path(path).name}"
        )
    linhas.append(f"Runtime: {time.time() - start_time:.2f}s")
    return "\n".join(linhas)


def _words_from_itimo(itimo):
    """Extrai unidades lexicais, preservando formas hifenizadas."""
    text = str(itimo or "").casefold()
    return re.findall(r"[^\W_]+(?:-[^\W_]+)*", text, flags=re.UNICODE)


def build_lexico():
    """Constrói o mapa da Eureka e a lista autoral completa de verbetes."""
    start_time = time.time()
    eureka_pairs = set()
    all_unique_words = set()
    errors = []
    themes_read = 0

    for theme, path in _active_themes():
        if not Path(path).exists():
            errors.append(f"{theme}: arquivo não encontrado: {path}")
            continue

        try:
            records = _read_ypo_records(path)
            themes_read += 1
        except Exception as exc:
            errors.append(f"{theme}: {exc}")
            continue

        for line_number, fields in records:
            if _ypo_is_blank_fields(fields):
                continue
            source_id = str(fields[3]).strip()
            if not source_id:
                errors.append(f"{theme}: linha {line_number}: ID de origem vazio")
                continue

            for itimo in _payload_itimos(fields):
                for word in _words_from_itimo(itimo):
                    all_unique_words.add(word)
                    if len(word) >= 3:
                        eureka_pairs.add((word, source_id))

    if errors:
        raise RuntimeError(
            "Build_Léxico STOP; lexico_pt.txt e verbetes.txt vigentes preservados.\n"
            + "\n".join(errors)
        )

    eureka_lines = [
        f"{word} : {source_id}"
        for word, source_id in sorted(
            eureka_pairs,
            key=lambda item: (item[0], item[1]),
        )
    ]
    verbetes_lines = sorted(all_unique_words)

    base_dir = _project_path("base")
    lexicon_path = base_dir / "lexico_pt.txt"
    verbetes_path = base_dir / "verbetes.txt"

    _write_derived_text(
        lexicon_path,
        "\n".join(eureka_lines) + ("\n" if eureka_lines else ""),
    )
    _write_derived_text(
        verbetes_path,
        "\n".join(verbetes_lines) + ("\n" if verbetes_lines else ""),
    )

    return (
        f"Build_Léxico: {themes_read} tema(s); "
        f"{len(eureka_lines)} relação(ões) Eureka; "
        f"{len(verbetes_lines)} verbete(s) único(s) para curadoria. "
        f"Saídas: {lexicon_path}; {verbetes_path}. "
        f"Runtime: {time.time() - start_time:.2f}s"
    )


BUILD_INDEXY_FILE = "ABOUT_index.MD"

BUILD_ESCALA = [
    "unidade",
    "mil",
    "milhão",
    "bilhão",
    "trilhão",
    "quatrilhão",
    "quintilhão",
    "sextilhão",
    "setilhão",
    "octilhão",
    "nonilhão",
    "decilhão",
    "undecilhão",
    "dodecilhão",
    "tredecilhão",
    "quatordecilhão",
    "quindecilhão",
    "sedecilhão",
    "septendecilhão",
]


def _backup_derived_file(path):
    """Cria backup antes de substituir um arquivo derivado existente."""
    path = Path(path)
    if not path.exists():
        return None

    backup_dir = _project_path("backups", "local_builders")
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    destination = backup_dir / f"{stamp}_{path.name}"
    destination.write_bytes(path.read_bytes())
    return destination


def _write_derived_text(path, text):
    """Grava arquivo derivado em UTF-8, preservando uma cópia anterior."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    _backup_derived_file(path)
    path.write_text(text, encoding="utf-8")


def _read_dna_rows():
    """Lê os registros do DNA sem inferir ou corrigir dados."""
    path = _project_path("base", "DNA.TXT")
    if not path.exists():
        return []

    header = []
    rows = []
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if line == "<EOF>":
            break
        if not line.startswith("|"):
            continue

        fields = [field.strip() for field in line.split("|")[1:-1]]
        if not header:
            header = fields
        elif len(fields) == len(header):
            rows.append(dict(zip(header, fields)))

    return rows


def _active_themes():
    """Temas públicos na ordem autoral de rol_todos os temas.txt; cadastro/status vêm do DNA."""
    dna_rows = _read_dna_rows()
    if dna_rows:
        by_key = {
            str(row.get("tema", "")).strip().casefold(): row
            for row in dna_rows if str(row.get("tema", "")).strip()
        }
        themes = []
        rol_path = _project_path("base", "rol_todos os temas.txt")
        for raw in _read_simple_list(rol_path):
            theme_key = raw.strip().casefold()
            row = by_key.get(theme_key)
            if not row or str(row.get("ativo", "")).strip().upper() != "S":
                continue
            theme = str(row.get("tema", "")).strip()
            if theme:
                themes.append((theme, _resolve_ypo_path(theme)))
        return themes

    # Bootstrap legado somente enquanto ainda não existe DNA utilizável.
    ativos_path = _project_path("base", "ativos.txt")
    themes = []
    if ativos_path.exists():
        for raw in ativos_path.read_text(encoding="utf-8-sig").splitlines():
            theme = raw.strip().partition(" : ")[0].strip()
            if theme:
                themes.append((theme, _resolve_ypo_path(theme)))
    return themes



def _read_ypo_records(path):
    """Compatibilidade interna: registros validados pela autoridade ypo_structure."""
    return [
        (record.line_number, list(record.fields))
        for record in _ypo_read_records(path, include_spacing=False)
    ]


def _payload_itimos(fields):
    """Compatibilidade interna: payload canônico; preserva NULL."""
    return list(_ypo_payload_itimos(fields))


def _theme_possibilities(path):
    """Calcula as possibilidades do tema usando os ítimos reais do .ypo."""
    sources = []
    correction = 1
    quantities = []

    for line_number, fields in _read_ypo_records(path):
        if _ypo_is_blank_fields(fields):
            continue
        source = fields[3]
        total_itimos = len(_payload_itimos(fields))

        if total_itimos <= 0:
            raise ValueError(f"linha {line_number}: nenhum ítimo real")

        if source not in sources:
            sources.append(source)
            quantities.append(total_itimos)
        else:
            index = sources.index(source)
            remaining = quantities[index] - correction
            if remaining == 0:
                remaining = 1
            sources.append(source)
            quantities.append(remaining)
            correction += 1

    possibilities = 1
    for quantity in quantities:
        possibilities *= quantity

    return abs(possibilities)


def _power_name(value):
    """Nome legível da ordem decimal usada no retrato da Machina."""
    grouped = f"{int(value):,}"
    index = grouped.count(",")
    if 0 <= index < len(BUILD_ESCALA):
        return BUILD_ESCALA[index]
    return "nonono"


def build_indexy():
    """Gera o retrato do tamanho da Machina: possibilidades de cada tema e total."""
    start_time = time.time()
    index_lines = []
    errors = []
    total_possibilities = 0

    for theme, path in _active_themes():
        try:
            possibilities = _theme_possibilities(path)
            total_possibilities += possibilities
            index_lines.append(
                f"{theme} : {possibilities:,} ({_power_name(possibilities)})"
            )
        except Exception as exc:
            errors.append(f"{theme}: {exc}")

    if errors:
        raise RuntimeError(
            "Build_Indexy STOP; ABOUT_index.MD vigente preservado.\n"
            + "\n".join(errors)
        )

    output = _project_path("md_files", BUILD_INDEXY_FILE)
    lines = [
        "variações para cada tema:  ",
        "___  ",
    ]
    lines.extend(line.replace(",", ".") + "  " for line in index_lines)
    lines.extend([
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
        (
            f"Total de variações: {total_possibilities:,} "
            f"({_power_name(total_possibilities)})"
        ).replace(",", "."),
        "",
    ])

    _write_derived_text(output, "\n".join(lines))

    return (
        f"Build_Indexy: {len(index_lines)} tema(s). "
        f"Saída: {output}. "
        f"Runtime: {time.time() - start_time:.2f}s"
    )



def _update_keyed_derived_line(path, key, new_line):
    """Atualiza uma única linha de arquivo derivado, preservando as demais."""
    path = Path(path)
    existing = []
    if path.exists():
        existing = path.read_text(encoding="utf-8-sig").splitlines()

    key_norm = str(key).casefold().strip()
    output = []
    replaced = False

    for line in existing:
        line_key = line.partition(" : ")[0].casefold().strip()
        if line_key == key_norm:
            if not replaced:
                output.append(str(new_line).strip())
                replaced = True
            continue
        output.append(line)

    if not replaced:
        output.append(str(new_line).strip())

    _write_derived_text(path, "\n".join(output).rstrip() + "\n")


def _matrix_one_theme(theme, path):
    """Calcula versos e ítimos reais e gera a imagem Matrix 3D do tema."""
    try:
        import numpy as np
        import matplotlib.pyplot as plt
    except Exception as exc:
        raise RuntimeError(f"dependência ausente ou indisponível: {exc}")

    table_name = str(theme).capitalize()
    matrix_dir = _project_path("images", "matrix")
    matrix_dir.mkdir(parents=True, exist_ok=True)

    current_line = "01"
    line_index = 1
    total_itimos = 0

    x_pos = np.array([])
    y_pos = np.array([])
    z_pos = np.array([])
    z_val = np.array([])

    for line_number, fields in _read_ypo_records(path):
        try:
            new_column = int(fields[2])
        except (TypeError, ValueError):
            raise ValueError(
                f"linha {line_number}: coluna estrutural inválida: {fields[2]!r}"
            )

        if fields[1] != current_line:
            line_index += 1
            current_line = fields[1]

        if new_column == 0:
            x_pos = np.append(x_pos, line_index)
            y_pos = np.append(y_pos, 0)
            z_pos = np.append(z_pos, 0)
            z_val = np.append(z_val, 0)
            continue

        actual_itimos = len(_payload_itimos(fields))
        total_itimos += actual_itimos

        x_pos = np.append(x_pos, line_index - 1)
        y_pos = np.append(y_pos, new_column - 1)
        z_pos = np.append(z_pos, 0)
        z_val = np.append(z_val, actual_itimos)

    x_val = np.ones(len(x_pos))
    y_val = np.ones(len(y_pos))
    z_base = np.ones(len(z_pos))

    if len(x_val) > 0:
        figure = plt.figure(figsize=(7, 7))
        axis = figure.add_subplot(111, projection="3d")
        axis.set_xlabel("x ➪ linhas", fontsize=14)
        axis.set_ylabel("y ➪ versos", fontsize=14)
        axis.set_zlabel("z ➪ ítimos", fontsize=14)
        axis.view_init(elev=30, azim=-30)
        axis.bar3d(
            x_pos,
            y_pos,
            z_base,
            x_val,
            y_val,
            z_val,
            color="#00ccaa",
            alpha=0.85,
            edgecolor="k",
        )
        image_path = matrix_dir / f"{table_name}.jpg"
        if image_path.exists():
            _backup_derived_file(image_path)
        figure.savefig(image_path, dpi=50)
        plt.close(figure)

    return table_name, line_index, total_itimos


def build_matrix(theme_only=None):
    """Constrói Matrix 3D, itimos.txt e versos.txt a partir dos .ypo reais.

    PRE-FLIGHT global: qualquer tema inválido interrompe antes da primeira
    Matrix/itimos.txt/versos.txt ser publicada.
    """
    start_time = time.time()
    themes = _active_themes()

    if theme_only:
        themes = [
            (theme, path)
            for theme, path in themes
            if theme.strip().casefold() == str(theme_only).strip().casefold()
        ]

    # PRE-FLIGHT: valida a leitura/estrutura de todos os alvos antes de gerar saída.
    preflight_errors = []
    for theme, path in themes:
        if not Path(path).exists():
            preflight_errors.append(f"{theme}: arquivo não encontrado: {path}")
            continue
        try:
            records = _read_ypo_records(path)
            for line_number, fields in records:
                if _ypo_is_blank_fields(fields):
                    continue
                int(fields[2])
                _payload_itimos(fields)
        except Exception as exc:
            preflight_errors.append(f"{theme}: {exc}")

    if preflight_errors:
        raise RuntimeError(
            "Build_Matrix STOP no PRE-FLIGHT; derivados vigentes preservados.\n"
            + "\n".join(preflight_errors)
        )

    itimos_lines = []
    versos_lines = []
    errors = []

    for theme, path in themes:
        if not Path(path).exists():
            errors.append(f"{theme}: arquivo não encontrado: {path}")
            continue

        try:
            table, verses, itimos = _matrix_one_theme(theme, path)
        except Exception as exc:
            errors.append(f"{theme}: {exc}")
            continue

        versos_lines.append(f"{table} : {verses}")
        itimos_lines.append(f"{table} : {itimos}")

    base_dir = _project_path("base")
    itimos_path = base_dir / "itimos.txt"
    versos_path = base_dir / "versos.txt"

    if theme_only:
        for line in itimos_lines:
            key = line.partition(" : ")[0]
            _update_keyed_derived_line(itimos_path, key, line)
        for line in versos_lines:
            key = line.partition(" : ")[0]
            _update_keyed_derived_line(versos_path, key, line)
    else:
        _write_derived_text(
            itimos_path,
            "\n".join(itimos_lines).rstrip() + ("\n" if itimos_lines else ""),
        )
        _write_derived_text(
            versos_path,
            "\n".join(versos_lines).rstrip() + ("\n" if versos_lines else ""),
        )

    mode = f"tema {theme_only}" if theme_only else "todos os temas"
    if errors:
        raise RuntimeError(
            "Build_Matrix STOP durante a geração.\n" + "\n".join(errors)
        )

    return (
        f"Build_Matrix: {mode}; "
        f"{len(itimos_lines)} Matrix 3D gerada(s)/atualizada(s). "
        f"Runtime: {time.time() - start_time:.2f}s"
    )


DNA_HEADER = [
    "tema", "ativo", "livro", "banco_tematico",
    "versos", "verbetes_no_texto", "verbetes_do_tema", "total_de_itimos",
    "qtd_de_variacoes", "qtd_cientifica",
]

DNA_LIVROS_PRINCIPAIS = [
    "livro vivo", "poemas", "jocosos", "ensaios", "variações",
    "metalinguagem", "sociais", "outros autores", "signos_fem", "signos_mas",
]


def _read_simple_list(path):
    path = Path(path)
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def _read_pair_map(path):
    output = {}
    for raw in _read_simple_list(path):
        name, separator, value = raw.partition(" : ")
        if separator and name.strip():
            output[name.strip().casefold()] = value.strip()
    return output


def _read_existing_dna_any_header():
    path = _project_path("base", "DNA.TXT")
    if not path.exists():
        return {}
    header = []
    output = {}
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if line == "<EOF>":
            break
        if not line.startswith("|"):
            continue
        fields = [x.strip() for x in line.split("|")[1:-1]]
        if not header:
            header = fields
            continue
        if len(fields) != len(header):
            continue
        row = dict(zip(header, fields))
        tema = row.get("tema", "").strip()
        if tema:
            row.pop("ordem", None)
            output[tema.casefold()] = row
    return output


def _books_by_theme():
    """Lê pertencimento autoral dos livros; a posição permanece somente no rol."""
    output = {}
    for book in DNA_LIVROS_PRINCIPAIS:
        path = _project_path("base", f"rol_{book}.txt")
        for theme in _read_simple_list(path):
            key = theme.strip().casefold()
            output.setdefault(key, []).append(book)
    return output


def _discover_theme_files():
    """Autoridade material do DNA: somente ./data/*.ypo."""
    data_dir = _project_path("data")
    found = {}
    collisions = []
    if not data_dir.is_dir():
        return found, [f"pasta data não encontrada: {data_dir}"]
    for path in sorted(data_dir.iterdir(), key=lambda p: p.name.casefold()):
        if not path.is_file() or path.suffix.casefold() != ".ypo":
            continue
        key = path.stem.casefold()
        if key in found:
            collisions.append(
                f"{path.stem}: duplicidade lógica .ypo: {found[key].name} + {path.name}"
            )
            continue
        found[key] = path
    return found, collisions


def _dna_footer():
    return [
        "LEGENDA",
        "tema = nome autoral do tema; existência material oficial vem somente de data/*.ypo.",
        "ativo = circulação: S quando presente em rol_todos os temas; N quando fora dele.",
        "livro = livro(s) aos quais o tema pertence; a ORDEM pertence exclusivamente ao rol_<livro>.txt.",
        "banco_tematico = banco visual associado ao tema.",
        "imagem = escolha RANDOM do banco_tematico; não integra o DNA.",
        "versos = quantidade de versos do yPoema.",
        "verbetes_no_texto = quantidade de registros estruturais do tema.",
        "verbetes_do_tema = quantidade de verbetes únicos disponíveis no tema.",
        "total_de_itimos = quantidade total de ítimos disponíveis no tema.",
        "qtd_de_variacoes = quantidade total de variações possíveis do tema.",
        "qtd_cientifica = qtd_de_variacoes em notação científica.",
    ]


def _theme_metrics(path):
    records = _read_ypo_records(path)
    verse_ids, unique_words = [], set()
    structural_rows = total_itimos = 0
    for line_number, fields in records:
        if _ypo_is_blank_fields(fields):
            continue
        structural_rows += 1
        verse_id = str(fields[1]).strip()
        if verse_id and verse_id not in verse_ids:
            verse_ids.append(verse_id)
        payload = _payload_itimos(fields)
        total_itimos += len(payload)
        for itimo in payload:
            unique_words.update(_words_from_itimo(itimo))
    variations = _theme_possibilities(path)
    return {
        "versos": str(len(verse_ids)),
        "verbetes_no_texto": str(structural_rows),
        "verbetes_do_tema": str(len(unique_words)),
        "total_de_itimos": str(total_itimos),
        "qtd_de_variacoes": str(variations),
        "qtd_cientifica": f"{variations:.2e}",
    }


def build_dna():
    """Reconstrói DNA.TXT do zero a partir de ./data/*.ypo.

    DNA anterior nunca é fonte. Permanece apenas como versão vigente até
    a nova fotografia passar integralmente pela validação.
    """
    start_time = time.time()
    theme_files, errors = _discover_theme_files()
    image_map = _read_pair_map(_project_path("base", "images.txt"))
    books = _books_by_theme()

    rol_todos_path = _project_path("base", "rol_todos os temas.txt")
    rol_todos_atual = _read_simple_list(rol_todos_path)
    rol_todos_keys = {
        str(item).strip().casefold()
        for item in rol_todos_atual
        if str(item).strip()
    }

    rows = []
    sem_livro = []
    sem_banco = []
    ordered = sorted(theme_files.items(), key=lambda item: item[1].stem.casefold())

    for indice, (key, path) in enumerate(ordered, start=1):
        theme = path.stem
        try:
            metrics = _theme_metrics(path)
        except Exception as exc:
            errors.append(f"{theme}: {exc}")
            continue

        theme_key_rol = theme.strip().casefold()
        ativo = "S" if theme_key_rol in rol_todos_keys else "N"
        theme_books = books.get(theme_key_rol, [])
        if theme_books:
            livro = ";".join(theme_books)
        elif ativo == "S":
            livro = "todos os temas"
        else:
            livro = ""
            sem_livro.append(theme)

        # Banco temático é um ECHO de images.txt, não autoridade sobre o tema.
        # A presença física de data/*.ypo preserva o tema autoral, mas NÃO o
        # reinsere no ambiente. Somente novo_tema/ROLs podem reativá-lo.
        banco = image_map.get(theme.casefold(), "")
        if not banco:
            sem_banco.append(theme)

        rows.append({
            "tema": theme,
            "ativo": ativo,
            "livro": livro,
            "banco_tematico": banco,
            **metrics,
        })

    audit_path = _project_path("base", "DNA_AUDITORIA.TXT")
    if errors:
        audit_lines = [
            f"temas_ypo={len(theme_files)}",
            f"temas_processados={len(rows)}",
            f"erros={len(errors)}",
            "",
            "ERROS",
            *errors,
            "",
        ]
        _write_derived_text(audit_path, "\n".join(audit_lines))
        raise RuntimeError(
            "Build_DNA STOP; DNA.TXT vigente preservado.\n"
            f"Erros: {len(errors)}.\n"
            f"Consulte {audit_path}.\n"
            f"Runtime: {time.time() - start_time:.2f}s"
        )

    # Cada um no seu quadrado:
    # Build_DNA fotografa; não cadastra nem ressuscita tema removido.
    # A reintegração ao ambiente pertence exclusivamente a novo_tema.
    inativos_fora_rol = sorted(
        (row["tema"] for row in rows if str(row.get("ativo", "")).upper() != "S"),
        key=str.casefold,
    )

    dna_lines = ["|" + "|".join(DNA_HEADER) + "|"]
    for row in rows:
        dna_lines.append("|" + "|".join(str(row.get(field, "")) for field in DNA_HEADER) + "|")
    dna_lines += ["<EOF>", ""] + _dna_footer() + [""]

    dna_path = _project_path("base", "DNA.TXT")
    audit_lines = [
        f"temas_ypo={len(rows)}",
        "erros=0",
        "inseridos_em_rol_todos=0",
        f"inativos_fora_rol_todos={len(inativos_fora_rol)}",
        f"banco_tematico_ausente={len(sem_banco)}",
        "",
    ]
    _write_derived_text(dna_path, "\n".join(dna_lines))
    _write_derived_text(audit_path, "\n".join(audit_lines))

    return (
        f"Build_DNA: {len(rows)} tema(s) .ypo; "
        "DNA reconstruído do zero; "
        "inseridos em rol_todos os temas=0; "
        f"inativos fora de rol_todos os temas={len(inativos_fora_rol)}; "
        f"banco temático ausente={len(sem_banco)} (não bloqueante); "
        f"saídas: {dna_path}; {audit_path}. "
        f"Runtime: {time.time() - start_time:.2f}s"
    )
