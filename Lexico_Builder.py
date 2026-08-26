from __future__ import annotations

import argparse
import re
import unicodedata
from collections import defaultdict
from pathlib import Path


WORD_RE = re.compile(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", re.UNICODE)

DEFAULT_SUFFIX_MIN = 2
DEFAULT_SUFFIX_MAX = 6
RICH_SUFFIXES = {
    "ão", "ões",
    "ais", "eis", "éis", "ois", "óis", "ous",
    "ado", "ada", "ido", "ida",
    "oso", "osa", "esa", "eza",
    "ante", "ente", "inte", "onte", "unto",
    "al", "el", "il", "ol", "ul",
}
WEAK_SUFFIXES = {
    "da", "de", "do",
    "me", "se", "te",
    "lhe",
    "nte",
}
CLITIC_PRONOUNS = {
    "me", "te", "se", "nos", "vos",
    "o", "a", "os", "as",
    "lo", "la", "los", "las",
    "no", "na", "nos", "nas",
    "lhe", "lhes",
}
PREFERRED_SHORT_SUFFIXES = {
    "ar", "er", "ir", "or",
    "as", "es", "is", "os",
    "ão", "õe", "am", "em", "ou", "ei",
    "al", "el", "il", "ol",
    "ante", "ente", "inte", "onte", "unto",
    "ões", "ais", "eis", "ous",
    "ado", "ada", "ido", "ida",
    "oso", "osa", "esa", "eza",
    "ul",
}


def strip_accents(text: str) -> str:
    """Return a lowercase sort key that ignores accents."""
    normalized = unicodedata.normalize("NFD", text.casefold())
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


def normalize_word(word: str, mode: str) -> str:
    word = word.strip("-'")
    if mode == "upper":
        return word.upper()
    if mode == "preserve":
        return word
    return word.casefold()


def verb_to_infinitive(word: str) -> str:
    clean = strip_accents(word)
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


def expand_token(token: str) -> list[str]:
    parts = [part for part in token.split("-") if part]
    if len(parts) <= 1:
        return parts

    last_part = strip_accents(parts[-1])
    if last_part in CLITIC_PRONOUNS:
        return [verb_to_infinitive(parts[0])]

    return parts


def extract_words(text: str, mode: str, min_len: int) -> list[str]:
    words = []
    for match in WORD_RE.finditer(text):
        for token in expand_token(match.group(0)):
            word = normalize_word(token, mode)
            if len(word) >= min_len:
                words.append(word)
    return words


def sorted_words(words: set[str]) -> list[str]:
    return sorted(words, key=lambda value: (strip_accents(value), value))


def group_by_suffix(
    words: list[str],
    min_size: int = DEFAULT_SUFFIX_MIN,
    max_size: int = DEFAULT_SUFFIX_MAX,
) -> dict[str, list[str]]:
    groups: dict[str, set[str]] = defaultdict(set)

    for word in words:
        for size in range(min_size, max_size + 1):
            if len(word) <= size:
                continue
            groups[word[-size:]].add(word)

    candidates = []
    for suffix, values in groups.items():
        if len(values) >= 2 and strip_accents(suffix) not in WEAK_SUFFIXES:
            sorted_values = sorted_words(values)
            candidates.append((suffix, sorted_values))

    def is_preferred(suffix: str) -> bool:
        return suffix.casefold() in PREFERRED_SHORT_SUFFIXES

    def suffix_score(suffix: str) -> tuple[int, int, str, str]:
        clean = strip_accents(suffix)
        if suffix.casefold() in RICH_SUFFIXES:
            return (0, len(suffix), clean, suffix)
        if is_preferred(suffix):
            return (1, len(suffix), clean, suffix)
        return (2, abs(5 - len(suffix)), clean, suffix)

    candidates.sort(key=lambda item: suffix_score(item[0]))

    result: dict[str, list[str]] = {}
    seen_sets: set[tuple[str, ...]] = set()
    for suffix, sorted_values in candidates:
        signature = tuple(sorted_values)
        if signature in seen_sets:
            continue
        if any(
            suffix.endswith(selected_suffix) and set(sorted_values).issubset(selected_words)
            for selected_suffix, selected_words in result.items()
        ):
            continue
        if not is_preferred(suffix):
            covered_words: set[str] = set()
            for selected_suffix, selected_words in result.items():
                if selected_suffix.endswith(suffix):
                    covered_words.update(selected_words)
            if set(sorted_values).issubset(covered_words):
                continue
        seen_sets.add(signature)
        result[suffix] = sorted_values

    return dict(sorted(result.items(), key=lambda item: (len(item[0]), strip_accents(item[0]), item[0])))


def split_rhyme_groups(groups: dict[str, list[str]]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    rich = {}
    support = {}
    for suffix, words in groups.items():
        if suffix.casefold() in RICH_SUFFIXES:
            rich[suffix] = words
        else:
            support[suffix] = words
    return rich, support


def render_list(lines: list[str]) -> str:
    return "\n".join(lines) if lines else "(nenhum)"


def sorted_by_suffix(words: set[str]) -> list[str]:
    return sorted(
        words,
        key=lambda word: (strip_accents(word)[::-1], strip_accents(word), word),
    )


def render_groups(groups: dict[str, list[str]], marker: str) -> str:
    parts = []
    for key, words in groups.items():
        label = f"[ {key} ]" if marker == "-" else f"[ {key}{marker} ]"
        parts.append(f"{label}\n{render_list(words)}")
    return "\n\n".join(parts) if parts else "(nenhum grupo com 2 ou mais palavras)"


def build_lexical_map(text: str, mode: str, min_len: int) -> str:
    all_words = extract_words(text, mode=mode, min_len=min_len)
    unique_words = sorted_words(set(all_words))

    suffix_groups = group_by_suffix(unique_words)
    rich_groups, _support_groups = split_rhyme_groups(suffix_groups)
    mapped_words = {word for words in rich_groups.values() for word in words}
    outside_words = sorted_by_suffix(set(unique_words) - mapped_words)

    return "\n\n".join(
        [
            "Lexico Builder",
            "___",
            f"Total de ocorrencias: {len(all_words)}",
            f"Palavras unicas: {len(unique_words)}",
            f"Palavras em rimas ricas: {len(mapped_words)}",
            f"Palavras fora do mapa: {len(outside_words)}",
            "___",
            "RIMAS RICAS",
            render_groups(rich_groups, "-"),
            "___",
            "FORA DO MAPA",
            render_list(outside_words),
            "___",
            "EOF()",
        ]
    )


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extrai vocabulario bruto de um .txt e gera mapa lexical para curadoria."
    )
    parser.add_argument("entrada", help="Arquivo .txt de entrada.")
    parser.add_argument(
        "-o",
        "--saida",
        help="Arquivo .txt de saida. Padrao: <entrada>_lexico.txt",
    )
    parser.add_argument(
        "--case",
        choices=("lower", "upper", "preserve"),
        default="lower",
        help="Normalizacao das palavras. Padrao: lower.",
    )
    parser.add_argument(
        "--min-len",
        type=int,
        default=2,
        help="Comprimento minimo das palavras. Padrao: 2.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.entrada)
    if not input_path.exists():
        raise SystemExit(f"Arquivo de entrada nao encontrado: {input_path}")

    output_path = Path(args.saida) if args.saida else input_path.with_name(input_path.stem + "_lexico.txt")

    text = read_text(input_path)
    lexical_map = build_lexical_map(text, mode=args.case, min_len=max(1, args.min_len))
    output_path.write_text(lexical_map + "\n", encoding="utf-8")

    print(f"Mapa lexical gerado: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
