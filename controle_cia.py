import os
import re
import random

import streamlit as st

from lay_2_ypo import gera_poema


_translate = lambda text: text
_load_typo = None
_write_ypoema = None
_ip_address = ""


def configure_cia(translate_func, load_typo_func, write_ypoema_func, ip_address):
    """Recebe da Machina as funções de apoio que a CIA precisa usar."""
    global _translate, _load_typo, _write_ypoema, _ip_address
    _translate = translate_func
    _load_typo = load_typo_func
    _write_ypoema = write_ypoema_func
    _ip_address = ip_address


CIA_MOODS = [
    "Sintática",
    "Sintética",
    "Formal",
    "Reduzida",
    "Completa",
    "Index",
]


REGRA_ZERO_CIA = """
REGRA_ZERO_CIA

Conduta comum a todos os moods:
- posição flexível;
- função crítica respeitada;
- consulta obrigatória às listas funcionais;
- random apenas entre candidatos plausíveis;
- nenhuma fórmula pode mentir sobre a função do FORTE_CANDIDATO;
- nenhuma figura de análise deve ser nomeada sem constatação clara no texto;
- repetição de trecho é ponto de fuga, não padrão.

A primeira linha e o último verso continuam candidatos fortes, mas não são
obrigações automáticas. O FECHO real recebe atenção especial porque, na
arquitetura dos yPoemas, costuma carregar reverberação, resumo da ópera,
estranheza produtiva ou convite à releitura.

Hierarquia interna:
1. regras fixas;
2. regras variáveis adequadas ao texto;
3. cartas na manga, com parcimônia, quando não houver encaixe seguro.
"""

CIA_OPERACOES_CRITICAS = [
    "deslocamento",
    "virada",
    "ponto de inflexão",
    "mudança de eixo",
    "transição",
    "passagem",
]

CIA_VERBOS_SURGIMENTO = ["surge", "aparece", "desponta"]

CIA_APOIOS_LEITURA = [
    "onde pousar",
    "uma âncora",
    "um porto seguro",
    "algum apoio",
    "uma referência",
    "um ponto de apoio",
    "um rumo de leitura",
    "um chão mínimo",
    "um eixo de sustentação",
    "um gancho",
]

CIA_TERMOS_SINTATICOS = [
    "verbo",
    "sujeito",
    "predicado",
    "advérbio",
    "pronome",
    "complemento",
    "oração",
    "coordenação",
    "subordinação",
    "elipse",
    "enumeração",
    "inciso",
    "conectivo",
    "regência",
    "pontuação",
    "reticências",
    "anáfora",
    "paralelismo",
    "sintaxe",
]


def _cia_count_sintatic_terms(text):
    """Conta termos acadêmicos reais em negrito para regular a Sintática."""
    clean = str(text or "").lower()
    total = 0
    for termo in CIA_TERMOS_SINTATICOS:
        total += len(re.findall(r"\*\*" + re.escape(termo) + r"\*\*", clean))
    return total


CIA_VERBOS_EXPLICITOS_COMUNS = {
    "sou", "és", "é", "somos", "são", "era", "eram", "será", "serão",
    "estou", "estás", "está", "estamos", "estão", "estive", "esteve", "estiveram", "estava", "estavam",
    "tenho", "tens", "tem", "têm", "tinha", "tinham", "teve", "tiveram",
    "vou", "vai", "vão", "fui", "foi", "foram",
    "vejo", "veem", "imagino", "busco", "buscar", "sabe", "sabem",
    "sonhar", "viver", "descobrirá", "saberá", "pousem", "livrá-las",
    "enquadra", "oferece", "recolhe", "condensa", "organiza", "prepara",
}

CIA_NAO_VERBOS = {
    "quando", "onde", "que", "se", "porque", "embora", "mas", "ou", "e",
    "como", "para", "por", "sem", "com", "num", "numa", "de", "do", "da",
    "carência", "lembrança", "certeza", "dúvida", "coisas", "coisa",
    "apenas", "nem", "só", "pouco", "bom", "senso",
    "assembleia", "doutora", "auditora", "vitalícia", "abnp",
    "bondade", "juventude", "carinho", "euforia", "cafuné",
    "bem-querer", "bombril-febrileto", "alcol-gentilito", "senil-butileto",
}

CIA_FALSOS_VERBOS_SUFFIX = (
    "ência", "ança", "eza", "dade", "ção", "ções", "são", "mento", "mentos",
)


def _cia_is_false_verb_token(token):
    token = str(token or "").lower().strip()
    return token in CIA_NAO_VERBOS or token.endswith(CIA_FALSOS_VERBOS_SUFFIX)


def _cia_token_has_nominal_context(line, token):
    """Evita transformar matéria nominal em verbo só por terminação.

    Ex.: “de mono-sulfito de bem-querer” ou “da Assembleia...”
    pode conter palavras que lembram ação, mas funcionam como nome, título,
    matéria afetiva, entidade ou composição inventada.
    """
    token = str(token or "").lower().strip()
    clean = str(line or "").lower()
    if not token:
        return False
    if token in CIA_NAO_VERBOS:
        return True
    if "-" in token and re.search(r"\b(de|do|da|dos|das)\s+(?:um\s+tal\s+|uma\s+tal\s+|algum\s+|alguma\s+)?[\wÀ-ÿ-]*" + re.escape(token) + r"\b", clean):
        return True
    if re.search(r"\b(de|do|da|dos|das)\s+(?:assembleia|bondade|carência|lembrança|certeza|dúvida|juventude|carinho|euforia|cafuné)\b", clean):
        return True
    return False


def _cia_tokens_lower(line):
    return [
        token.strip("“”\"'()[]{}.,;:!?…-").lower()
        for token in re.findall(r"[\wÀ-ÿ-]+", str(line or ""))
        if token.strip("“”\"'()[]{}.,;:!?…-")
    ]


def _cia_has_explicit_verb(line):
    """Heurística conservadora: só autoriza 'verbo' quando há forma verbal plausível."""
    tokens = _cia_tokens_lower(line)
    if not tokens:
        return False
    for token in tokens:
        if _cia_is_false_verb_token(token) or _cia_token_has_nominal_context(line, token):
            continue
        if token in CIA_VERBOS_EXPLICITOS_COMUNS:
            return True
        # Infinitivos e formas conjugadas comuns; evita marcar nomes curtos por acaso.
        if len(token) >= 5 and re.search(
            r"(ar|er|ir|ou|ei|ava|avam|ia|iam|ará|erá|irá|arei|erei|irei|asse|esse|isse|ando|endo|indo)$",
            token,
        ):
            return True
    return False


def _cia_first_explicit_verb(line):
    tokens = _cia_tokens_lower(line)
    for token in tokens:
        if _cia_is_false_verb_token(token) or _cia_token_has_nominal_context(line, token):
            continue
        if token in CIA_VERBOS_EXPLICITOS_COMUNS:
            return token
        if len(token) >= 5 and re.search(
            r"(ar|er|ir|ou|ei|ava|avam|ia|iam|ará|erá|irá|arei|erei|irei|asse|esse|isse|ando|endo|indo)$",
            token,
        ):
            return token
    return ""


def _cia_verbo_label(verbo):
    """Evita lematização mecânica do tipo está -> estár."""
    verbo = str(verbo or "").strip()
    if verbo.lower() in {"estou", "estás", "está", "estamos", "estão", "estive", "esteve", "estiveram", "estava", "estavam"}:
        return f'a forma verbal “{verbo}” (estar)'
    return f'o **verbo** “{verbo}”'


def _cia_find_nearby_explicit_verb(poema_lines, line, radius=2):
    idx = _cia_line_index(poema_lines, line)
    if idx < 0:
        return "", ""
    for dist in range(1, radius + 1):
        for j in (idx - dist, idx + dist):
            if 0 <= j < len(poema_lines):
                verbo = _cia_first_explicit_verb(poema_lines[j])
                if verbo:
                    return verbo, poema_lines[j]
    return "", ""


def _cia_has_clear_subject(line):
    clean = str(line or "").lower()
    return bool(re.search(r"\b(eu|tu|ele|ela|nós|vós|eles|elas|algo|alguém|ninguém|quem|o que|a gente|as gentes|os momentos)\b", clean))


def _cia_is_nominal_or_prepositional(line):
    clean = str(line or "").strip().lower()
    return bool(clean) and not _cia_has_explicit_verb(clean)


def _cia_subordinacao_kind(line):
    clean = str(line or "").lower()
    if re.search(r"\bquando\b", clean):
        return "tempo"
    if re.search(r"\bse\b", clean):
        return "condição"
    if re.search(r"\bembora\b", clean):
        return "concessão"
    if re.search(r"\bporque\b", clean):
        return "explicação"
    if re.search(r"\bque\b", clean):
        return "complementação ou retomada"
    if re.search(r"\bonde\b", clean):
        return "lugar ou origem"
    return ""


def _cia_carta_na_manga():
    return random.choice([
        "a impressão que fica é que o texto abre uma possibilidade de leitura sem obrigar uma explicação única.",
        "aparentemente, o texto insinua uma passagem lateral e deixa ao leitor outras leituras possíveis.",
        "o texto parece oferecer outros caminhos de leitura, sem entregar todos os seus vínculos de forma direta.",
        "há caminhos quase ocultos para outros pontos do poema; a leitura avança por aproximação, não por prova única.",
    ])


def _cia_is_monoverso(poema_lines):
    return len(poema_lines or []) == 1


def _cia_is_poema_curto(poema_lines):
    return 1 <= len(poema_lines or []) <= 3


def _cia_is_micropercurso(poema_lines):
    return len(poema_lines or []) == 3


def _cia_analise_monoverso(poema_lines):
    line = poema_lines[0]
    clip = _cia_clip(line)
    return _cia_join([
        f"Em “{clip}”, o texto funciona como inscrição conceitual: mais do que desenvolver uma cena, nomeia um campo de leitura.",
        f"A força da linha está na própria fórmula verbal e imagética: o verso oferece uma chave de entrada sem precisar simular percurso.",
        f"A leitura se concentra nesse núcleo único; o poema não se alonga, mas abre um horizonte de aproximação.",
    ])


def _cia_abertura_micro(poema_lines):
    clip = _cia_clip(poema_lines[0])
    return random.choice([
        f"Em “{clip}”, o texto arma seu primeiro impulso e oferece ao leitor uma referência de aproximação.",
        f"“{clip}” instala a entrada do poema: a imagem inicial dá direção à pequena sequência.",
        f"Desde “{clip}”, a leitura encontra o primeiro apoio do texto, ainda aberto ao deslocamento seguinte.",
    ])


def _cia_miolo_micro(poema_lines):
    line = poema_lines[1] if len(poema_lines) > 1 else poema_lines[0]
    clip = _cia_clip(line)
    return random.choice([
        f"“{clip}” funciona como passagem intermediária: a imagem desloca o primeiro impulso antes da saída final.",
        f"Em “{clip}”, a pequena sequência muda de temperatura; o verso comenta o impulso inicial sem fingir percurso longo.",
        f"“{clip}” abre o meio do poema: não amplia demais o caminho, mas altera a direção antes do fecho.",
    ])


def _cia_fecho_micro(poema_lines):
    clip = _cia_clip(poema_lines[-1])
    return random.choice([
        f"No fecho, “{clip}” recolhe a pequena sequência sem esgotá-la; a última linha oferece ressonâncias pelo poema.",
        f"Em “{clip}”, a saída final preserva abertura: o verso conclui sem transformar a imagem em resposta única.",
        f"No último verso, “{clip}” concentra a chegada do micropercurso e deixa o texto respirando depois da linha final.",
    ])


def _cia_mapa_previo(poema_lines):
    """Cartas abertas na mesa: candidatos dirigidos antes da redação."""
    if not poema_lines:
        return {"abertura": [], "miolo": [], "fecho": [], "chave": [], "coringas": [], "cartas": []}
    total = len(poema_lines)
    chaves = _cia_linhas_perola(poema_lines)
    first, last = poema_lines[0], poema_lines[-1]
    middle = poema_lines[total // 2]
    fortes = _cia_forte_candidatos(poema_lines)
    if total == 1:
        return {"abertura": [first], "miolo": [first], "fecho": [first], "chave": [first], "coringas": [first], "cartas": []}
    if total == 2:
        return {"abertura": [first], "miolo": _cia_unique(chaves + [first, last]), "fecho": [last], "chave": _cia_unique(chaves + fortes), "coringas": fortes, "cartas": []}
    if total == 3:
        return {"abertura": [first], "miolo": [poema_lines[1]], "fecho": [last], "chave": _cia_unique(chaves + fortes), "coringas": fortes, "cartas": []}
    perguntas = [line for line in fortes if "?" in line]
    suspensos = [line for line in fortes if "..." in line or "…" in line]
    marcados = [line for line in fortes if line.count(",") >= 1 or "(" in line or ")" in line]
    return {
        "abertura": _cia_unique([first] + perguntas + suspensos + chaves + fortes + [last]),
        "miolo": _cia_unique(chaves + marcados + fortes + [middle, first, last]),
        "fecho": _cia_unique([last] + suspensos + perguntas + chaves + fortes + [first]),
        "chave": _cia_unique(chaves + fortes),
        "coringas": _cia_unique(fortes + chaves),
        "cartas": [],
    }


CIA_PEROLA_LEXICO = {
    "paz", "silêncio", "destino", "tempo", "sonho", "sonhar", "saudade",
    "mistério", "mistérios", "deuses", "lamúrias", "certeza", "falácias",
    "felizes", "improviso", "vida", "morte", "rota", "caminho",
}


def _cia_score_linha_perola(line, idx, total):
    """Pontua linha-pérola: fotografia, mapa da mina, chave-mestra, bússola."""
    clean = str(line or "").strip()
    lower = clean.lower()
    words = _cia_tokens_lower(clean)
    score = 0

    if not clean:
        return 0
    if 3 <= len(words) <= 8:
        score += 2
    if "..." in clean or "…" in clean:
        score += 2
    if "?" in clean:
        score += 1
    if idx not in (0, total - 1):
        score += 2
    if total > 3 and 1 < idx < total - 2:
        score += 1
    if any(w in CIA_PEROLA_LEXICO for w in words):
        score += 2
    if re.search(r"\b(cotoco|quase|nunca|sempre|além|sem|resto|deuses|lamúrias|falácias)\b", lower):
        score += 2
    if re.search(r"\b(paz|certeza|destino|tempo|sonhar|improviso)\b", lower):
        score += 1
    return score


def _cia_linhas_perola(poema_lines, min_score=5):
    """Detecta linhas que funcionam como fotografia/mapa da mina do poema."""
    total = len(poema_lines)
    scored = []
    for idx, line in enumerate(poema_lines):
        score = _cia_score_linha_perola(line, idx, total)
        if score >= min_score:
            scored.append((score, idx, line))
    return [line for score, idx, line in sorted(scored, key=lambda item: (-item[0], item[1]))]


def _cia_is_linha_perola(poema_lines, line):
    return line in _cia_linhas_perola(poema_lines, min_score=5)


def _cia_comentario_linha_perola(poema_lines, line):
    clip = _cia_clip(line)
    imagem = random.choice(["fotografia", "mapa da mina", "chave-mestra", "bússola"])
    return random.choice([
        f"“{clip}” funciona como {imagem} do poema: a linha condensa o percurso e oferece ao leitor outro ângulo de leitura.",
        f"Em “{clip}”, o texto encontra uma {imagem}: a imagem concentra o caminho e muda o peso do que veio antes e depois.",
        f"“{clip}” atua como linha-chave: mais do que passagem intermediária, oferece um rumo para reler o poema inteiro.",
        f"Em “{clip}”, a leitura encontra uma fotografia do conjunto: o verso mostra, em pouco espaço, uma direção possível para atravessar o texto.",
    ])


def _cia_bloco_sintatico_reforco(poema_lines, used_lines):
    """Garante lastro sintático sem nomear figura que o trecho não sustenta."""
    line = _cia_pick_role_by_zones(
        poema_lines,
        "miolo",
        used_lines,
        poema_lines[len(poema_lines) // 2],
        allowed_zones={"miolo", "inicial_proxima", "tardia"},
    )
    clip = _cia_clip(line)
    if _cia_has_explicit_verb(line):
        verbo = _cia_first_explicit_verb(line)
        return random.choice([
            f"Em “{clip}”, o **verbo** “{verbo}” põe a imagem em movimento e dá direção à **sintaxe** do verso.",
            f"Em “{clip}”, a presença verbal de “{verbo}” sustenta a **oração** e organiza o avanço da leitura.",
        ])
    nearby_verb, nearby_line = _cia_find_nearby_explicit_verb(poema_lines, line)
    if nearby_verb:
        return (
            f"Em “{clip}”, não há **verbo** explícito no trecho citado; "
            f"o verso funciona como **complemento** da ação indicada por “{nearby_verb}” em “{_cia_clip(nearby_line)}”."
        )
    return random.choice([
        f"Em “{clip}”, a construção nominal dispensa **verbo** explícito e sustenta a imagem por justaposição.",
        f"Em “{clip}”, a leitura se apoia em sintagma nominal ou preposicional: a frase não age por **verbo**, mas por aproximação de imagens.",
        f"Em “{clip}”, {_cia_carta_na_manga()}",
    ])


def ensure_cia_name(force=False):
    """Compatibilidade: o cabeçalho da CIA agora vem do tema Cia.ypo."""
    if force or not st.session_state.get("cia_name"):
        st.session_state["cia_name"] = "Cia"


def generate_poema_preview(nome_tema, seed_eureka=""):
    """Gera um poema inline sem sobrescrever o LYPO em disco."""
    try:
        script = gera_poema(nome_tema, seed_eureka)
    except Exception:
        return nome_tema

    text_lines = [nome_tema]
    for line in script:
        if line == "\n":
            text_lines.append("")
        else:
            text_lines.append(line)
    return "<br>".join(text_lines)


def build_cia_header():
    """Descrição poética da CIA, gerada pela própria Machina via Cia.ypo."""
    header = generate_poema_preview("Cia", "")
    if st.session_state.lang != "pt":
        header = _translate(header)
        typo_user = "TYPO_" + _ip_address
        with open(os.path.join("./temp/" + typo_user), "w", encoding="utf-8") as save_typo:
            save_typo.write(header)
        header = _load_typo()

    parts = [part.strip() for part in header.replace("<br/>", "<br>").split("<br>")]
    body_parts = [part for part in parts[1:] if part] if len(parts) > 1 else [part for part in parts if part]
    return "<br>".join(body_parts)


def _cia_first_token(line):
    token = line.strip().split(" ")[0] if line.strip() else ""
    return token.strip("“”\"'()[]{}.,;:!?…-").lower()


def _cia_first_two_tokens(line):
    parts = [p.strip("“”\"'()[]{}.,;:!?…-").lower() for p in line.strip().split()[:2]]
    return " ".join([p for p in parts if p])


def _cia_poema_lines(curr_ypoema):
    """Extrai linhas reais do yPoema, preservando apenas o corpo do texto."""
    raw_parts = [part.strip() for part in curr_ypoema.replace("<br/>", "<br>").split("<br>")]
    lines = [part for part in raw_parts if part]
    return lines[1:] if len(lines) > 1 else []


def _cia_clip(line, limit=62):
    """Mantém o trecho legível no palco, sem deixar a citação dominar o parágrafo."""
    clean = re.sub(r"\s+", " ", str(line or "")).strip()
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + "..."


def _cia_join(blocks):
    """Une blocos sem trailing spaces visuais; o HTML da CIA cuida dos parágrafos."""
    return "\n\n".join([str(block).strip() for block in blocks if str(block).strip()])


def _cia_pick_unused(candidates, used_lines, fallback=""):
    """Escolhe um verso ainda não mobilizado e o registra como usado."""
    for line in candidates:
        if line and line not in used_lines:
            used_lines.add(line)
            return line
    if fallback and fallback not in used_lines:
        used_lines.add(fallback)
        return fallback
    return ""


def _cia_destaques(poema_lines):
    """Trechos com maior probabilidade de rendimento crítico, sem transformar isso em fórmula."""
    marked = [line for line in poema_lines if "..." in line or "…" in line or "?" in line or line.count(",") >= 1]
    inner_caps = []
    for line in poema_lines:
        words = line.split()
        if len(words) > 1 and any(w.strip("“”\"'()[]{}.,;:!?…-")[:1].isupper() for w in words[1:]):
            inner_caps.append(line)
    curtas_fortes = [line for line in poema_lines if 2 <= len(line.split()) <= 6]
    return marked + inner_caps + curtas_fortes + poema_lines


def _cia_unique(lines):
    """Preserva a ordem e elimina repetições vazias."""
    seen = set()
    out = []
    for line in lines:
        clean = str(line or "").strip()
        if clean and clean not in seen:
            seen.add(clean)
            out.append(clean)
    return out


def _cia_score_candidate(line, idx, total):
    """Pontua um FORTE_CANDIDATO sem prender a análise à ordem linear do poema."""
    score = 0
    words = line.split()
    n_words = len(words)

    if idx == 0:
        score += 2
    if idx == total - 1:
        score += 2
    if total > 2 and idx not in (0, total - 1):
        score += 1
    if "?" in line:
        score += 3
    if "..." in line or "…" in line:
        score += 3
    if line.count(",") >= 1:
        score += 2
    if line.count(",") >= 2:
        score += 1
    if "(" in line or ")" in line:
        score += 2
    if 2 <= n_words <= 7:
        score += 2
    elif 8 <= n_words <= 13:
        score += 1
    if any(w.strip("“”\"'()[]{}.,;:!?…-")[:1].isupper() for w in words[1:]):
        score += 1
    if re.search(r"\b(se|quando|embora|porque|que|mas|ou|e)\b", line.lower()):
        score += 1
    score += _cia_score_linha_perola(line, idx, total)

    return score


def _cia_line_index(poema_lines, line):
    """Retorna a posição do verso no poema, sem quebrar se houver repetição."""
    try:
        return poema_lines.index(line)
    except ValueError:
        return -1


def _cia_line_zone(poema_lines, line):
    """Classifica a posição material do candidato para evitar fórmula mentirosa."""
    total = len(poema_lines)
    idx = _cia_line_index(poema_lines, line)
    if idx < 0 or total <= 0:
        return "indefinida"
    if idx == 0:
        return "inicial"
    if idx == total - 1:
        return "final"
    if idx >= max(1, total - 2):
        return "tardia"
    if idx <= 1:
        return "inicial_proxima"
    return "miolo"


def _cia_regra_zero_abertura(poema_lines, line):
    """ABERTURA: escolhe formulação conforme posição/função real do candidato."""
    clip = _cia_clip(line)
    if _cia_is_monoverso(poema_lines):
        return random.choice([
            f"Em “{clip}”, o texto funciona como inscrição conceitual: mais do que desenvolver uma cena, nomeia um campo de leitura.",
            f"“{clip}” oferece uma chave de entrada em estado concentrado; a linha não simula percurso, abre um horizonte.",
            f"Em “{clip}”, a leitura começa pelo núcleo único do poema, onde a imagem já nasce condensada.",
        ])
    zone = _cia_line_zone(poema_lines, line)
    if zone == "final":
        return random.choice([
            f"No fecho real, “{clip}” recolhe parte do percurso e permite perceber como o texto vinha preparando sua reverberação.",
            f"No último verso, “{clip}” concentra a chegada do poema e reorganiza retrospectivamente seu campo de forças.",
            f"Em “{clip}”, o texto chega ao seu ponto de recolhimento: a leitura volta sobre o percurso sem forçar uma abertura artificial.",
        ])
    if zone == "tardia":
        return random.choice([
            f"Lido retroativamente, “{clip}” recolhe parte do percurso e permite perceber como o texto vinha preparando sua reverberação.",
            f"Quase no fecho, “{clip}” funciona como ponto de inflexão; dali o percurso anterior ganha outro rumo de leitura.",
            f"Em “{clip}”, a tensão se condensa: o verso não inaugura o texto, mas reorganiza retrospectivamente seu campo de forças.",
            f"“{clip}” concentra uma força tardia do poema e permite reler o caminho anterior sem forçar uma abertura artificial.",
        ])
    if zone == "miolo":
        op = random.choice(CIA_OPERACOES_CRITICAS)
        verbo = random.choice(CIA_VERBOS_SURGIMENTO)
        return random.choice([
            f"Em “{clip}”, a leitura encontra um {op}: o verso {verbo} como ponto de orientação sem depender da ordem linear do texto.",
            f"“{clip}” oferece um rumo de leitura pelo centro do poema; a partir daí, o percurso ganha outra organização.",
            f"Quando “{clip}” {verbo} no percurso, o texto se deixa ler por uma passagem interna, não apenas pelo primeiro verso.",
        ])
    return random.choice([
        f"“{clip}” abre um campo de forças e oferece um caminho de aproximação para o leitor.",
        f"Desde “{clip}”, o poema encontra um portal de entrada: a leitura começa por ali e ganha direção.",
        f"“{clip}” funciona como entrada crítica do poema; dali a leitura encontra seu primeiro ponto de apoio.",
        f"Em “{clip}”, o texto arma seu gesto inicial e oferece ao leitor uma referência de aproximação.",
    ])


def _cia_regra_zero_miolo(poema_lines, line):
    """MIOLO: comenta desenvolvimento/tensão sem presumir posição intermediária falsa."""
    clip = _cia_clip(line)
    zone = _cia_line_zone(poema_lines, line)
    if _cia_is_micropercurso(poema_lines):
        if zone == "inicial":
            return random.choice([
                f"Retomado como primeiro impulso, “{clip}” ilumina a pequena sequência sem precisar fingir desenvolvimento longo.",
                f"“{clip}” volta como apoio inicial: o verso orienta o micropercurso sem ocupar o lugar do fecho.",
            ])
        if zone == "final":
            return _cia_fecho_micro(poema_lines)
        return _cia_miolo_micro(poema_lines)
    if _cia_is_linha_perola(poema_lines, line):
        return _cia_comentario_linha_perola(poema_lines, line)
    if zone == "inicial":
        return random.choice([
            f"Retomado no desenvolvimento, “{clip}” deixa de ser apenas entrada e passa a sustentar a direção crítica da leitura.",
            f"Quando volta ao desenvolvimento, “{clip}” funciona como eixo de leitura: o início passa a iluminar o percurso.",
            f"No desenvolvimento, “{clip}” ganha outra função: não abre de novo o poema, mas ajuda a organizar sua tensão interna.",
        ])
    if zone == "final":
        return random.choice([
            f"No último verso, “{clip}” já é o fecho real do poema: a imagem concentra a tensão que o percurso vinha preparando.",
            f"Como fecho real, “{clip}” recolhe o movimento anterior e faz o desenvolvimento chegar à sua reverberação.",
            f"Em “{clip}”, o desenvolvimento encontra seu ponto de chegada: o verso não aproxima o fecho; ele concentra o próprio encerramento.",
        ])
    if zone == "tardia":
        return random.choice([
            f"Quase no fim, “{clip}” adensa o percurso e prepara a reverberação que a leitura ainda precisa atravessar.",
            f"“{clip}” aparece como zona de passagem para o encerramento, mudando o peso do que vinha sendo lido.",
            f"Nessa passagem tardia, “{clip}” concentra uma tensão que o fecho poderá recolher sem parecer imposto.",
        ])
    op = random.choice(CIA_OPERACOES_CRITICAS)
    verbo = random.choice(CIA_VERBOS_SURGIMENTO)
    return random.choice([
        f"Em “{clip}”, a linguagem ganha densidade: o verso concentra imagem, tensão e atmosfera sem dissolver o mistério.",
        f"Quando “{clip}” {verbo} no desenvolvimento, a leitura encontra um {op} que altera o peso do percurso.",
        f"O centro de força passa por “{clip}”; ali o poema ganha espessura e evita seguir por caminho óbvio.",
        f"Há em “{clip}” uma condensação de leitura: o texto se mostra breve na superfície e mais largo por dentro.",
    ])


def _cia_regra_zero_fecho(poema_lines, line):
    """FECHO: preserva reverberação e dá atenção especial ao fecho real."""
    clip = _cia_clip(line)
    if _cia_is_monoverso(poema_lines):
        return random.choice([
            f"A linha única, “{clip}”, conclui sem encerrar: sua força está em concentrar a leitura numa fórmula aberta.",
            f"Em “{clip}”, o fecho coincide com a própria inscrição; o texto termina no mesmo ponto em que abre seu horizonte.",
        ])
    if _cia_is_micropercurso(poema_lines) and line == poema_lines[-1]:
        return _cia_fecho_micro(poema_lines)
    zone = _cia_line_zone(poema_lines, line)
    if zone == "final":
        return random.choice([
            f"No fecho, “{clip}” recolhe o percurso sem esgotá-lo; a última linha concentra a pressão e oferece ressonâncias pelo poema.",
            f"No fecho, “{clip}” recolhe o percurso sem esgotá-lo; a última linha concentra a pressão e cria ressonâncias pelo texto.",
            f"No fecho, “{clip}” recolhe o percurso sem esgotá-lo; a última linha concentra a pressão e distribui ecos pelo percurso.",
            f"A chegada a “{clip}” dá ao poema seu ponto de recolhimento: não fecha o sentido, mas organiza o eco do que veio antes.",
            f"Em “{clip}”, o poema encontra uma saída que ainda preserva atrito. O final recolhe a leitura sem transformar a tensão em resposta única.",
            f"O último verso, “{clip}”, funciona como resumo da ópera: conserva estranheza e convida a leitura a voltar sobre o percurso.",
        ])
    if zone == "inicial":
        return random.choice([
            f"O encerramento crítico pode retornar a “{clip}”: o começo reaparece como eco e dá outro peso ao percurso.",
            f"Ao retomar “{clip}”, a leitura fecha em <u>da capo</u>: o primeiro verso volta como chave de reverberação.",
            f"No retorno a “{clip}”, a abertura reaparece como eco; o primeiro gesto passa a iluminar o fim.",
        ])
    op = random.choice(CIA_OPERACOES_CRITICAS)
    verbo = random.choice(CIA_VERBOS_SURGIMENTO)
    return random.choice([
        f"A reverberação pode voltar a “{clip}”: esse ponto reorganiza o percurso e faz o final ser lido por outra direção.",
        f"O encerramento crítico se apoia em “{clip}” porque essa imagem aponta para a tensão que o final recolhe.",
        f"Mesmo fora da última linha, “{clip}” funciona como zona de eco: a análise retorna a esse ponto para deixar o poema vibrando.",
        f"Na {op}, “{clip}” {verbo} como reverberação possível sem apagar o impacto do último verso.",
    ])

def _cia_forte_candidatos(poema_lines, min_count=2, max_count=5):
    """Mapeia 2 a 5 FORTE_CANDIDATO para uso móvel na CIA.

    A primeira e a última linha continuam candidatas, mas deixam de ser obrigações.
    O acaso escolhe entre possibilidades plausíveis; não chuta comentários.
    """
    if not poema_lines:
        return []

    scored = []
    total = len(poema_lines)
    for idx, line in enumerate(poema_lines):
        scored.append((_cia_score_candidate(line, idx, total), idx, line))

    # Prioriza força crítica; usa a posição apenas como desempate estável.
    ranked = [line for score, idx, line in sorted(scored, key=lambda item: (-item[0], item[1]))]

    # Garante eixo mínimo para poemas maiores, sem fixar função.
    anchors = [poema_lines[0]]
    if total > 2:
        anchors.append(poema_lines[total // 2])
    if total > 1:
        anchors.append(poema_lines[-1])

    candidatos = _cia_unique(ranked + anchors)
    target = min(max_count, max(min_count, min(len(candidatos), max_count)))
    return candidatos[:target]


def _cia_candidate_pools(poema_lines):
    """Cria listas funcionais já mapeadas antes da redação.

    As cartas ficam abertas na mesa: ABERTURA, MIOLO, FECHO, CHAVE,
    CORINGAS e CARTAS_NA_MANGA. Os moods consultam esse mapa em vez de
    escrever a partir de blocos isolados.
    """
    mapa = _cia_mapa_previo(poema_lines)
    return {
        "abertura": mapa.get("abertura", []),
        "miolo": mapa.get("miolo", []),
        "fecho": mapa.get("fecho", []),
        "chave": mapa.get("chave", []),
        "coringas": mapa.get("coringas", []),
        "cartas": mapa.get("cartas", []),
    }


def _cia_pick_role(poema_lines, role, used_lines, fallback=""):
    """Escolhe um candidato funcional, embaralhando apenas opções plausíveis.

    REGRA_ZERO_CIA: no FECHO, o último verso recebe atenção especial, sem virar
    obrigação absoluta. A variação não pode atropelar impacto.
    """
    pools = _cia_candidate_pools(poema_lines)
    pool = pools.get(role, [])[:]

    if role == "fecho" and poema_lines:
        last = poema_lines[-1]
        if last in pool and last not in used_lines and random.random() < 0.82:
            used_lines.add(last)
            return last

    random.shuffle(pool)
    chosen = _cia_pick_unused(pool, used_lines, fallback)
    if chosen:
        return chosen

    # Se o poema é curto ou todos já foram usados, reabre a lista sem repetir por vício.
    pool = pools.get(role, [])[:]
    random.shuffle(pool)
    return pool[0] if pool else fallback


def _cia_pick_role_by_zones(poema_lines, role, used_lines, fallback="", allowed_zones=None):
    """Escolhe candidato por função, mas respeita zonas permitidas para moods mais curtos.

    Usado principalmente na Reduzida e em pontos sensíveis da Completa para evitar
    que o último verso vire 'entrada' ou que a primeira linha vire 'fecho' sem
    operação de eco/retomada explicitamente nomeada.
    """
    allowed_zones = set(allowed_zones or [])
    pool = _cia_candidate_pools(poema_lines).get(role, [])[:]
    filtered = [line for line in pool if _cia_line_zone(poema_lines, line) in allowed_zones]
    random.shuffle(filtered)
    chosen = _cia_pick_unused(filtered, used_lines, "")
    if chosen:
        return chosen
    return fallback


def _cia_critico_abertura(poema_lines, used_lines):
    """Primeiro bloco: portal, inflexão ou entrada retroativa, conforme REGRA_ZERO_CIA."""
    abertura = _cia_pick_role(poema_lines, "abertura", used_lines, poema_lines[0])
    return _cia_regra_zero_abertura(poema_lines, abertura)


def _cia_critico_fecho(poema_lines, used_lines, prefer_specific=True):
    """Último bloco: melhor reverberação final entre candidatos plausíveis."""
    if prefer_specific and poema_lines:
        last = poema_lines[-1]
        # Em poemas curtos, o fecho real costuma carregar a chave de recolhimento.
        if len(poema_lines) <= 5 and last not in used_lines:
            used_lines.add(last)
            return _cia_regra_zero_fecho(poema_lines, last)
    fecho = _cia_pick_role(poema_lines, "fecho", used_lines, poema_lines[-1])
    if prefer_specific and fecho:
        return _cia_regra_zero_fecho(poema_lines, fecho)
    return random.choice([
        "O fechamento recolhe as linhas de força sem reduzir o poema a uma resposta. A leitura termina com eco, não com explicação.",
        "O percurso crítico se encerra onde o poema preserva sua zona de ressonância: o sentido se organiza, mas não se deixa domesticar.",
        "Ao fim, permanece uma tensão produtiva. O poema não pede solução; pede que a leitura conserve o que nele ficou em movimento.",
    ])


def _cia_filter_candidates(candidates, used_lines, target_count, min_count=1):
    """Seleciona blocos intermediários evitando repetir trechos já mobilizados."""
    shuffled = candidates[:]
    random.shuffle(shuffled)
    chosen = []
    for item in shuffled:
        item_lines = set(item.get("lines", []))
        if item_lines and item_lines & used_lines:
            continue
        chosen.append(item)
        used_lines.update(item_lines)
        if len(chosen) >= target_count:
            break
    return chosen


def _cia_sintatica_reticencias(poema_lines, line):
    """Lê reticências conforme a posição: abertura não suspende fechamento."""
    clip = _cia_clip(line)
    zone = _cia_line_zone(poema_lines, line)
    apoio = random.choice(CIA_APOIOS_LEITURA)
    if zone in ("inicial", "inicial_proxima"):
        return random.choice([
            f"As **reticências** de “{clip}” deixam a abertura em suspensão: a **pontuação** prolonga a enumeração e puxa a leitura adiante.",
            f"Em “{clip}”, as **reticências** não suspendem o fechamento; elas abrem expectativa e fazem a **oração** continuar para além da linha.",
            f"A **pontuação** em “{clip}” instala uma entrada incompleta: o verso começa por falta, acúmulo e continuidade.",
        ])
    if zone in ("final", "tardia"):
        return random.choice([
            f"As **reticências** de “{clip}” suspendem o fechamento e deixam a frase continuar fora da linha, como se o sentido ainda estivesse procurando {apoio}.",
            f"Em “{clip}”, a **pontuação** final preserva uma sobra de sentido: o verso recolhe o percurso sem encerrar sua reverberação.",
            f"As **reticências** em “{clip}” fazem o fecho respirar para fora da linha; a leitura termina sem perder o resto de tensão.",
        ])
    return random.choice([
        f"As **reticências** de “{clip}” abrem uma zona de passagem: a **pontuação** interrompe a frase e muda o ritmo da leitura.",
        f"Em “{clip}”, a **pontuação** cria suspensão no desenvolvimento; o verso interrompe o fluxo e desloca o eixo da frase.",
        f"As **reticências** em “{clip}” deixam a **oração** incompleta por escolha: a leitura precisa atravessar o intervalo.",
    ])

def _cia_sintatica_abertura_academica(poema_lines):
    """ABERTURA da Sintática: cartilha estável, sem random estrutural."""
    line = poema_lines[0]
    clip = _cia_clip(line)
    lower = line.lower()
    if "..." in line or "…" in line:
        return (
            f"Na abertura, “{clip}” instala uma entrada em suspensão: "
            f"as **reticências** funcionam como **pontuação** de continuidade e fazem a **oração** avançar para além da linha."
        )
    if "?" in line:
        return (
            f"Na abertura, “{clip}” arma uma pergunta de entrada: "
            f"a **pontuação** interrogativa reorganiza a **sintaxe** e coloca o leitor diante de uma tensão inicial."
        )
    if line.count(",") >= 2:
        return (
            f"Na abertura, “{clip}” apresenta uma **enumeração** inicial: "
            f"a **sintaxe** cresce por acúmulo e oferece ao leitor o primeiro rumo de leitura."
        )
    if re.search(r"\b(eu|me|meu|minha|nós|nosso|nossa)\b", lower):
        return (
            f"Na abertura, “{clip}” organiza a entrada por uma marca de pessoa: "
            f"o **sujeito** se insinua no enunciado e dá ao **verbo** um gesto de aproximação."
        )
    if _cia_has_explicit_verb(line):
        verbo = _cia_first_explicit_verb(line)
        return (
            f"Na abertura, “{clip}” firma o primeiro movimento verbal do poema: "
            f"o **verbo** “{verbo}” dá ação ao enunciado e organiza a entrada da **sintaxe**."
        )
    return (
        f"Na abertura, “{clip}” funciona como construção nominal de entrada: "
        f"a **sintaxe** ainda não age por **verbo** explícito, mas por nomeação, título e enquadramento."
    )


def _cia_sintatica_fecho_academico(poema_lines):
    """FECHO da Sintática: cartilha estável, com atenção ao último verso real."""
    line = poema_lines[-1]
    clip = _cia_clip(line)
    if "..." in line or "…" in line:
        return (
            f"No fecho, “{clip}” preserva uma sobra de sentido: "
            f"as **reticências** atuam como **pontuação** de reverberação, deixando a frase respirar depois da última linha."
        )
    if "?" in line:
        return (
            f"No fecho, “{clip}” encerra por pergunta: "
            f"a **pontuação** desloca a resposta e mantém a **oração** aberta à releitura."
        )
    if line.count(",") >= 2:
        return (
            f"No fecho, “{clip}” recolhe o percurso por **enumeração**: "
            f"a **sintaxe** concentra o acúmulo final sem transformar a tensão em explicação única."
        )
    return (
        f"No fecho, “{clip}” recolhe o movimento do poema: "
        f"a **sintaxe** final organiza o **predicado** da leitura e deixa o sentido em estado de reverberação."
    )


def _cia_sintatica_bloco_generico(poema_lines, used_lines):
    """MIOLO de segurança para a Sintática acadêmica real."""
    line = _cia_pick_unused([poema_lines[len(poema_lines) // 2]] + poema_lines, used_lines, poema_lines[len(poema_lines) // 2])
    if line:
        used_lines.add(line)
    clip = _cia_clip(line)
    return (
        f"No desenvolvimento, “{clip}” sustenta a engrenagem interna do poema: "
        f"a **oração** não apenas comunica uma imagem, mas distribui pausas, cortes e retomadas dentro da **sintaxe**."
    )

CIA_SINTATICA_GRUPOS = {
    "basico": ["sujeito", "verbo", "pronome", "predicado"],
    "articulacao": ["oração", "complemento", "conectivo", "coordenação", "subordinação"],
    "expressivo": ["elipse", "enumeração", "inciso", "regência", "pontuação", "reticências"],
    "ritmo": ["anáfora", "paralelismo", "repetição", "deslocamento"],
}


def _cia_sintatica_grupos_presentes(text):
    """Indica quais grupos da Sintática já apareceram no comentário."""
    clean = str(text or "").lower()
    presentes = set()
    for grupo, termos in CIA_SINTATICA_GRUPOS.items():
        for termo in termos:
            if re.search(r"\*\*" + re.escape(termo) + r"\*\*", clean):
                presentes.add(grupo)
                break
    return presentes


def _cia_sintatica_add_candidate(candidates, grupo, lines_used, text):
    cleaned = [line for line in lines_used if line]
    candidates.append({"grupo": grupo, "lines": cleaned, "text": text})


def _cia_sintatica_candidatos_balanceados(poema_lines, used_lines):
    """Cria blocos de MIOLO por constatação clara e repetição controlada.

    Regra interna:
    - figura técnica só entra quando o trecho a sustenta;
    - candidato usado entra no bloqueio;
    - repetição é ponto de fuga, não padrão.
    """
    inner = poema_lines[1:-1] if len(poema_lines) > 2 else poema_lines[:]
    candidates = []

    # 1. Básico: verbo/sujeito/predicado apenas com constatação clara.
    verbais = [line for line in inner if _cia_has_explicit_verb(line)]
    if verbais:
        line = verbais[0]
        verbo = _cia_first_explicit_verb(line)
        verbo_label = _cia_verbo_label(verbo)
        if _cia_has_clear_subject(line):
            texto = random.choice([
                f"Em “{_cia_clip(line)}”, {verbo_label} encontra apoio em um **sujeito** perceptível no próprio enunciado, organizando o gesto da frase.",
                f"Quando {verbo_label} movimenta o verso, a **sintaxe** avança por ação concreta e cria apoio para o enunciado.",
            ])
        else:
            texto = random.choice([
                f"Em “{_cia_clip(line)}”, {verbo_label} movimenta o verso; a **sintaxe** avança pela ação verbal, não por comentário abstrato.",
                f"Quando {verbo_label} organiza o movimento do verso, a **sintaxe** avança por ação concreta, não por comentário abstrato.",
            ])
        _cia_sintatica_add_candidate(candidates, "basico", [line], texto)
    else:
        nominais = [line for line in inner if _cia_is_nominal_or_prepositional(line)]
        if nominais:
            line = nominais[0]
            nearby_verb, nearby_line = _cia_find_nearby_explicit_verb(poema_lines, line)
            if nearby_verb:
                texto = (
                    f"Em “{_cia_clip(line)}”, não há **verbo** explícito no trecho citado; "
                    f"a construção funciona como **complemento** da ação indicada por “{nearby_verb}” em “{_cia_clip(nearby_line)}”."
                )
            else:
                texto = f"Em “{_cia_clip(line)}”, a construção nominal dispensa **verbo** explícito e sustenta a imagem por aproximação sintática."
            _cia_sintatica_add_candidate(candidates, "basico", [line], texto)

    # 2. Articulação: só nomeia subordinação/conectivo quando o marcador existe.
    articulacoes = [line for line in inner if _cia_subordinacao_kind(line)]
    coordenadas = [line for line in inner if re.search(r"\b(e|ou|mas)\b", line.lower())]
    if articulacoes:
        line = articulacoes[0]
        kind = _cia_subordinacao_kind(line)
        if "onde" in line.lower():
            texto = f"Em “{_cia_clip(line)}”, o marcador “onde” abre uma **oração** de lugar ou origem; a articulação depende do que o período desenvolve ao redor."
        elif "que" in line.lower() and not re.search(r"\b(se|quando|embora|porque)\b", line.lower()):
            texto = f"Em “{_cia_clip(line)}”, o **conectivo** “que” cria dependência de complementação ou retomada; a **oração** não funciona como frase solta."
        else:
            texto = f"Em “{_cia_clip(line)}”, a **subordinação** cria dependência interna de {kind}; a **oração** avança por vínculo sintático claro."
        _cia_sintatica_add_candidate(candidates, "articulacao", [line], texto)
    elif coordenadas:
        line = coordenadas[0]
        _cia_sintatica_add_candidate(
            candidates,
            "articulacao",
            [line],
            f"Em “{_cia_clip(line)}”, o **conectivo** articula a passagem entre partes da frase; a **coordenação** aproxima segmentos sem fundi-los por completo."
        )

    # 3. Expressivo: pontuação/inciso/enumeração apenas quando há sinal claro.
    reticencias = [line for line in inner if "..." in line or "…" in line]
    perguntas = [line for line in inner if "?" in line]
    incisos = [line for line in inner if "(" in line or ")" in line or re.search(r",\s*por dizer\s*,", line.lower())]
    enumeracoes = [line for line in inner if line.count(",") >= 2]
    if reticencias:
        line = reticencias[0]
        _cia_sintatica_add_candidate(
            candidates,
            "expressivo",
            [line],
            f"Em “{_cia_clip(line)}”, as **reticências** alongam a frase: a **pontuação** cria uma suspensão expressiva sem abandonar a direção sintática."
        )
    elif perguntas:
        line = perguntas[0]
        _cia_sintatica_add_candidate(
            candidates,
            "expressivo",
            [line],
            f"Em “{_cia_clip(line)}”, a **pontuação** interrogativa muda a pressão da **oração** e abre uma tensão de leitura."
        )
    elif incisos:
        line = incisos[0]
        _cia_sintatica_add_candidate(
            candidates,
            "expressivo",
            [line],
            f"O **inciso** em “{_cia_clip(line)}” cria uma dobra interna: a frase se desvia por um instante e retorna com outra respiração."
        )
    elif enumeracoes:
        line = enumeracoes[0]
        _cia_sintatica_add_candidate(
            candidates,
            "expressivo",
            [line],
            f"A **enumeração** em “{_cia_clip(line)}” trabalha por acúmulo: o verso amplia a frase sem perder o eixo sintático."
        )

    # 4. Desenho e ritmo: anáfora/paralelismo/deslocamento com bloqueio posterior.
    first_tokens = {}
    first_two = {}
    for line in inner:
        t1 = _cia_first_token(line)
        t2 = _cia_first_two_tokens(line)
        if t1:
            first_tokens.setdefault(t1, []).append(line)
        if t2:
            first_two.setdefault(t2, []).append(line)
    parallel_key = next((k for k, v in first_two.items() if len(v) >= 2 and len(k.split()) == 2), None)
    anafora_key = next((k for k, v in first_tokens.items() if len(v) >= 2), None)
    if parallel_key:
        exemplos = first_two[parallel_key][:2]
        _cia_sintatica_add_candidate(
            candidates,
            "ritmo",
            exemplos,
            f"O **paralelismo** entre “{_cia_clip(exemplos[0])}” e “{_cia_clip(exemplos[1])}” organiza a cadência: a estrutura retorna, mas cada volta altera a pressão da leitura."
        )
    elif anafora_key:
        exemplos = first_tokens[anafora_key][:2]
        _cia_sintatica_add_candidate(
            candidates,
            "ritmo",
            exemplos,
            f"A **anáfora** entre “{_cia_clip(exemplos[0])}” e “{_cia_clip(exemplos[1])}” firma um eixo de **repetição** e dá cadência ao percurso."
        )
    else:
        cortes = []
        for i, line in enumerate(poema_lines[1:-2], start=1):
            nxt = poema_lines[i + 1]
            if line and line[-1] not in ".?!:;…)" and (nxt[:1].islower() or len(line.split()) <= 4):
                cortes.append((line, nxt))
        if cortes:
            l1, l2 = cortes[0]
            _cia_sintatica_add_candidate(
                candidates,
                "ritmo",
                [l1, l2],
                f"Na passagem entre “{_cia_clip(l1)}” e “{_cia_clip(l2)}”, há **deslocamento** de ritmo: o corte faz a frase atravessar a linha antes de encontrar novo apoio."
            )
        elif inner:
            line = inner[min(len(inner) - 1, len(inner) // 2)]
            _cia_sintatica_add_candidate(
                candidates,
                "ritmo",
                [line],
                f"Em “{_cia_clip(line)}”, o desenho do verso cria **deslocamento**: a leitura muda de eixo sem romper a unidade do período."
            )

    # Pré-filtro contra versos já reservados e grupos repetidos.
    filtered = []
    grupos = set()
    for item in candidates:
        item_lines = set(item.get("lines", []))
        if item_lines and item_lines & used_lines:
            continue
        if item.get("grupo") in grupos:
            continue
        filtered.append(item)
        grupos.add(item.get("grupo"))
    return filtered


def _cia_sintatica_escolhe_miolos_balanceados(poema_lines, used_lines, abertura, fecho):
    """Seleciona miolos suficientes para dar lastro acadêmico visível."""
    blocos = [abertura]
    termo_min = 4
    termo_max = 8
    grupos_alvo = {"basico", "articulacao", "expressivo", "ritmo"}
    candidatos = _cia_sintatica_candidatos_balanceados(poema_lines, used_lines)

    for item in candidatos:
        item_lines = set(item.get("lines", []))
        if item_lines and item_lines & used_lines:
            continue
        teste = _cia_join(blocos + [item["text"], fecho])
        if _cia_count_sintatic_terms(teste) > termo_max:
            # Se passar muito do teto, ainda aceita quando faltar grupo essencial.
            presentes = _cia_sintatica_grupos_presentes(_cia_join(blocos + [fecho]))
            if item.get("grupo") in presentes:
                continue
        blocos.append(item["text"])
        used_lines.update(item.get("lines", []))
        presentes = _cia_sintatica_grupos_presentes(_cia_join(blocos + [fecho]))
        if grupos_alvo.issubset(presentes) and _cia_count_sintatic_terms(_cia_join(blocos + [fecho])) >= termo_min:
            break

    if len(blocos) == 1:
        blocos.append(_cia_sintatica_bloco_generico(poema_lines, used_lines))

    blocos.append(fecho)

    # Se ainda estiver pobre, acrescenta reforço antes do fecho.
    if _cia_count_sintatic_terms(_cia_join(blocos)) < termo_min:
        blocos.insert(-1, _cia_bloco_sintatico_reforco(poema_lines, used_lines))

    return blocos


def _cia_completa_bloco_sintatico(poema_lines, used_lines):
    """Camada sintática leve para a análise Completa fazer jus ao nome."""
    candidatos = _cia_sintatica_candidatos_balanceados(poema_lines, used_lines)
    for alvo in ("expressivo", "articulacao", "ritmo", "basico"):
        item = next((c for c in candidatos if c.get("grupo") == alvo), None)
        if item:
            used_lines.update(item.get("lines", []))
            return "Na camada sintática, " + item["text"][0].lower() + item["text"][1:]
    return _cia_bloco_sintatico_reforco(poema_lines, used_lines)


def build_cia_analysis(curr_ypoema):
    """Sintática acadêmica real: papéis bem distribuídos e cartilha ABERTURA-MIOLO-FECHO."""
    poema_lines = _cia_poema_lines(curr_ypoema)
    tema = st.session_state.get("tema", "")

    if not poema_lines:
        st.session_state["_cia_used_lines"] = []
        return "**requer apuração manual**"

    if _cia_is_monoverso(poema_lines):
        st.session_state["_cia_used_lines"] = list(poema_lines)
        return _cia_analise_monoverso(poema_lines)

    used_lines = set()

    # Cartilha fixa da Sintática: abertura = primeira linha real; fecho = último verso real.
    abertura = _cia_sintatica_abertura_academica(poema_lines)
    fecho = _cia_sintatica_fecho_academico(poema_lines)
    used_lines.add(poema_lines[0])
    used_lines.add(poema_lines[-1])

    # Regra interna: lastro sintático visível, com balanceamento por papéis.
    # Não é quantidade por quantidade: a análise tenta contemplar básico,
    # articulação, expressivo e desenho/ritmo quando houver pertinência e espaço.
    blocos = _cia_sintatica_escolhe_miolos_balanceados(poema_lines, used_lines, abertura, fecho)

    st.session_state.tema_last_analise = tema
    st.session_state["_cia_used_lines"] = list(used_lines)
    return _cia_join(blocos)

def build_cia_analysis_free(curr_ypoema):
    """Outro ângulo: leitura de contraste, sem repetir trechos por comodidade."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "Sem texto em foco para leitura."

    used = set(st.session_state.get("_cia_used_lines", []))
    local_used = set(used)

    abertura_line = _cia_pick_role_by_zones(
        poema_lines,
        "abertura",
        local_used,
        "",
        allowed_zones={"inicial", "inicial_proxima", "miolo"},
    )
    if abertura_line:
        local_used.add(abertura_line)
    destaque_line = _cia_pick_role_by_zones(
        poema_lines,
        "miolo",
        local_used,
        "",
        allowed_zones={"miolo", "inicial_proxima", "tardia"},
    )
    if destaque_line:
        local_used.add(destaque_line)

    # Outro ângulo não repete trecho já usado na análise principal, salvo falta real de alternativa.
    fecho_line = poema_lines[-1] if poema_lines and poema_lines[-1] not in local_used else ""

    if _cia_is_poema_curto(poema_lines) and len(local_used) >= len(poema_lines):
        return _cia_join([
            "Por outro caminho, a leitura pode observar o modo como o texto condensa sua energia em poucas linhas, sem precisar repetir os mesmos pontos já vistos.",
            "A força do conjunto está na passagem entre imagem, matéria verbal e saída final: cada linha trabalha uma função diferente dentro da pequena sequência.",
            "O poema ganha fôlego justamente porque não explica demais; concentra, desloca e deixa uma última ressonância.",
        ])

    if abertura_line:
        abertura = _cia_regra_zero_abertura(poema_lines, abertura_line)
    else:
        abertura = random.choice([
            "Outro ângulo surge pela organização interna do poema: a leitura muda quando acompanha as passagens, não apenas os versos isolados.",
            "Por outro caminho, o poema revela uma temperatura própria. O texto começa a pesar menos pelo enunciado e mais pelo modo como distribui sua tensão.",
            "Há uma entrada crítica possível pela circulação do próprio texto: o poema respira por retomadas, desvios e zonas de adensamento.",
        ])

    if destaque_line:
        desenvolvimento = _cia_regra_zero_miolo(poema_lines, destaque_line)
    else:
        desenvolvimento = random.choice([
            "No corpo do poema, a energia se distribui por passagens sucessivas. A leitura avança porque o texto desloca sua pressão de um ponto a outro.",
            "A zona de maior força não precisa se concentrar em uma única citação: ela nasce do encadeamento entre imagem, ritmo e desvio.",
            "A linguagem ganha espessura no conjunto. O poema cria densidade sem depender de um único ponto de apoio.",
        ])

    if fecho_line:
        fecho = _cia_regra_zero_fecho(poema_lines, fecho_line)
    else:
        fecho = random.choice([
            "O encerramento recolhe a tensão sem resolver tudo. O poema termina preservando uma zona de eco.",
            "Ao final, a leitura não encontra uma explicação única, mas um resto de intensidade que continua trabalhando.",
            "O final não domestica o percurso: apenas concentra sua última reverberação.",
        ])

    return _cia_join([abertura, desenvolvimento, fecho])


def build_cia_analysis_sintetica(curr_ypoema):
    """Sintética: núcleo de tensão com atmosfera, sem virar resumo banal."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "**requer apuração manual**"

    if _cia_is_monoverso(poema_lines):
        return _cia_analise_monoverso(poema_lines)
    if _cia_is_micropercurso(poema_lines):
        return _cia_join([_cia_abertura_micro(poema_lines), _cia_miolo_micro(poema_lines), _cia_fecho_micro(poema_lines)])

    used_lines = set()
    abertura_line = _cia_pick_role(poema_lines, "abertura", used_lines, poema_lines[0])
    destaque_line = _cia_pick_role(poema_lines, "miolo", used_lines, poema_lines[len(poema_lines) // 2])

    abertura = _cia_regra_zero_abertura(poema_lines, abertura_line)
    desenvolvimento = _cia_regra_zero_miolo(poema_lines, destaque_line)

    fecho = _cia_critico_fecho(poema_lines, used_lines, prefer_specific=True)
    return _cia_join([abertura, desenvolvimento, fecho])


def build_cia_analysis_formal(curr_ypoema):
    """Formal: arquitetura visível do poema, sem repetir o padrão da Sintética ou da Reduzida."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "**requer apuração manual**"

    raw_lines = curr_ypoema.replace("<br/>", "<br>").split("<br>")
    raw_poem = raw_lines[1:] if len(raw_lines) > 1 else []
    qtd_linhas = len(poema_lines)
    blocos = max(
        1,
        sum(
            1
            for i, line in enumerate(raw_poem)
            if line.strip() and (i == 0 or not raw_poem[i - 1].strip())
        ),
    )

    curtas = sum(1 for line in poema_lines if len(line.split()) <= 4)
    longas = sum(1 for line in poema_lines if len(line.split()) >= 7)
    medias = max(0, qtd_linhas - curtas - longas)
    reticencias = [line for line in poema_lines if "..." in line or "…" in line]
    perguntas = [line for line in poema_lines if "?" in line]

    repeticoes_iniciais = {}
    for line in poema_lines:
        first = line.split()[0].strip("“”\"'()[]{}.,;:!?…-").lower() if line.split() else ""
        if first:
            repeticoes_iniciais[first] = repeticoes_iniciais.get(first, 0) + 1
    repetido = next((k for k, v in repeticoes_iniciais.items() if v >= 2), None)

    if qtd_linhas == 14 and blocos == 4:
        abertura = random.choice([
            "A primeira presença do poema é o seu desenho: **14 linhas** em **4 blocos** desenham uma forma reconhecível de **soneto**, ainda que a Machina o faça respirar em chave própria.",
            "O poema se apresenta como arquitetura visível: **14 linhas** distribuídas em **4 blocos** aproximam o texto do **soneto**, antes mesmo de qualquer interpretação.",
            "Antes do sentido se explicar, a forma já se anuncia: **14 linhas** em **4 blocos** acionam a memória do **soneto** e organizam o fôlego inicial da leitura.",
        ])
    else:
        abertura = random.choice([
            f"A primeira presença do poema é o seu desenho: **{qtd_linhas} linhas** em **{blocos} bloco{'s' if blocos != 1 else ''}** dão ao texto uma forma de chegada antes mesmo da interpretação.",
            f"O poema se apresenta como arquitetura visível: **{qtd_linhas} linhas** e **{blocos} bloco{'s' if blocos != 1 else ''}** regulam o modo como a leitura entra no texto.",
            f"Antes do sentido se explicar, há uma forma em cena: **{qtd_linhas} linhas** distribuídas em **{blocos} bloco{'s' if blocos != 1 else ''}** organizam o fôlego inicial da leitura.",
        ])

    desenvolvimento = []

    def _rotulo_qtd(qtd, singular, plural):
        return f"**{qtd} {singular if qtd == 1 else plural}**"

    extensoes = []
    if curtas:
        extensoes.append(_rotulo_qtd(curtas, "linha breve", "linhas breves"))
    if medias:
        extensoes.append(_rotulo_qtd(medias, "linha média", "linhas médias"))
    if longas:
        extensoes.append(_rotulo_qtd(longas, "linha mais longa", "linhas mais longas"))

    if len(extensoes) >= 2:
        extensoes_texto = ", ".join(extensoes[:-1]) + " e " + extensoes[-1]
    elif extensoes:
        extensoes_texto = extensoes[0]
    else:
        extensoes_texto = ""

    if extensoes_texto:
        verbo_criar = "cria" if (curtas + medias + longas) == 1 else "criam"
        verbo_fazer = "faz" if (curtas + medias + longas) == 1 else "fazem"
        desenvolvimento.append(random.choice([
            f"A alternância de extensão também trabalha: {extensoes_texto} {verbo_criar} variação de fôlego, evitando que o poema avance em linha reta demais.",
            f"O ritmo nasce da medida dos versos: {extensoes_texto} {verbo_fazer} a leitura acelerar, conter-se ou respirar conforme o desenho pede.",
            f"A diferença entre versos de extensão distinta não é ornamento gráfico; ela distribui pausas e pressões dentro do próprio corpo do poema.",
        ]))

    if repetido:
        desenvolvimento.append(random.choice([
            f"A recorrência inicial de “{_cia_clip(repetido)}” atua como marca de coesão. O poema ganha reconhecimento pelo retorno, não por simples repetição.",
            f"O retorno de “{_cia_clip(repetido)}” no começo de versos cria uma coluna interna: a forma passa a insistir antes mesmo do argumento.",
            f"Quando “{_cia_clip(repetido)}” reaparece em posição inicial, o poema firma uma pequena ossatura de repetição e reconhecimento.",
        ]))

    if reticencias or perguntas:
        mark = reticencias[0] if reticencias else perguntas[0]
        desenvolvimento.append(random.choice([
            f"A pontuação em “{_cia_clip(mark)}” interfere no desenho do tempo: o verso não apenas diz, ele regula a demora da leitura.",
            f"Em “{_cia_clip(mark)}”, a pontuação vira gesto formal. Ela cria pausa, suspensão ou pressão dentro da superfície do poema.",
            f"O sinal gráfico em “{_cia_clip(mark)}” participa da arquitetura: muda o modo como o verso se oferece ao olhar e à escuta.",
        ]))

    if len(desenvolvimento) > 2:
        random.shuffle(desenvolvimento)
        desenvolvimento = desenvolvimento[:2]

    fecho = random.choice([
        "O resultado é uma forma que não apenas abriga o poema, mas participa de sua força: linhas, pausas e retornos dão ao texto uma presença própria.",
        "A forma recolhe a leitura sem precisar explicar o poema: o desenho visível organiza o percurso e deixa uma última impressão de arquitetura viva.",
        "Ao final, o que permanece não é só o que foi dito, mas o modo como o texto ocupou o espaço e conduziu o olhar até o seu repouso.",
    ])

    return _cia_join([abertura] + desenvolvimento + [fecho])


def build_cia_analysis_resumida(curr_ypoema):
    """Reduzida: leitura curta, objetiva e distinta da Sintética.

    Na Reduzida, a brevidade aumenta o risco de inversão funcional.
    Por isso, a REGRA_ZERO_CIA é aplicada com zonas mais rígidas:
    abertura não usa último verso; fecho privilegia o fecho real.
    """
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "**requer apuração manual**"

    if _cia_is_monoverso(poema_lines):
        return _cia_analise_monoverso(poema_lines)
    if _cia_is_micropercurso(poema_lines):
        return _cia_join([_cia_abertura_micro(poema_lines), _cia_miolo_micro(poema_lines), _cia_fecho_micro(poema_lines)])

    used_lines = set()
    abertura_line = _cia_pick_role_by_zones(
        poema_lines,
        "abertura",
        used_lines,
        poema_lines[0],
        allowed_zones={"inicial", "inicial_proxima"},
    )
    if abertura_line:
        used_lines.add(abertura_line)

    destaque_line = _cia_pick_role_by_zones(
        poema_lines,
        "miolo",
        used_lines,
        poema_lines[len(poema_lines) // 2],
        allowed_zones={"miolo", "inicial_proxima", "tardia"},
    )
    if destaque_line:
        used_lines.add(destaque_line)

    abertura = _cia_regra_zero_abertura(poema_lines, abertura_line)
    desenvolvimento = _cia_regra_zero_miolo(poema_lines, destaque_line)

    fecho_line = poema_lines[-1]
    fecho = _cia_regra_zero_fecho(poema_lines, fecho_line)
    return _cia_join([abertura, desenvolvimento, fecho])

def build_cia_analysis_completa(curr_ypoema):
    """Completa: leitura ampla com imagem, forma, tensão, camada sintática e fecho."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "**requer apuração manual**"

    if _cia_is_monoverso(poema_lines):
        return _cia_analise_monoverso(poema_lines)
    if _cia_is_micropercurso(poema_lines):
        qtd_linhas = len(poema_lines)
        forma_curta = random.choice([
            f"O desenho visível em **{qtd_linhas} linhas** participa do efeito: as quebras organizam uma pequena sequência de entrada, passagem e saída.",
            f"A forma curta não é suporte neutro: em **{qtd_linhas} linhas**, o poema regula o fôlego e concentra sua invenção.",
        ])
        return _cia_join([_cia_abertura_micro(poema_lines), _cia_miolo_micro(poema_lines), forma_curta, _cia_fecho_micro(poema_lines)])

    used_lines = set()
    qtd_linhas = len(poema_lines)
    abertura_line = _cia_pick_role(poema_lines, "abertura", used_lines, poema_lines[0])
    destaque_line = _cia_pick_role_by_zones(
        poema_lines,
        "miolo",
        used_lines,
        poema_lines[len(poema_lines) // 2],
        allowed_zones={"miolo", "inicial_proxima", "tardia"},
    )

    abertura = _cia_regra_zero_abertura(poema_lines, abertura_line)
    nucleo = _cia_regra_zero_miolo(poema_lines, destaque_line)

    forma = random.choice([
        f"A distribuição em **{qtd_linhas} linhas** participa do efeito do poema: pausas e cortes regulam o ritmo de aparição do sentido.",
        f"O desenho visível do texto — suas **{qtd_linhas} linhas**, pausas e quebras — atua como arquitetura, não como suporte neutro.",
        f"Também a forma pesa: as **{qtd_linhas} linhas** organizam o fôlego e modulam a intensidade do percurso.",
    ])

    camada_sintatica = _cia_completa_bloco_sintatico(poema_lines, used_lines)

    ampliacao = random.choice([
        "O poema vale não só pelo que nomeia, mas pelo modo como organiza pressão, intervalo, reaparição e eco.",
        "A força do texto está no modo como regula sua intensidade e a devolve ao leitor em camadas.",
        "O texto conduz, interrompe, reaperta e libera o próprio movimento sem reduzir-se a uma explicação única.",
    ])

    # A Completa articula o conjunto: não é Sintática expandida, mas inclui uma parte sintática.
    meio = [nucleo, forma, camada_sintatica, ampliacao]
    random.shuffle(meio)
    fecho = _cia_critico_fecho(poema_lines, used_lines, prefer_specific=True)
    return _cia_join([abertura] + meio + [fecho])


def _cia_index_unique(seq):
    seen = set()
    out = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _cia_index_find_ypo_file(nome_tema):
    """Localiza o .ypo do tema em foco. Leitura apenas."""
    safe = str(nome_tema or "").strip()
    if not safe:
        return ""

    candidates = [
        safe,
        safe.replace(" ", "_"),
        safe.replace("_", " "),
        safe.capitalize(),
        safe.title(),
    ]

    folders = ["./DATA", "./data", ".DATA", ".data", "./base", "."]
    for folder in folders:
        for name in _cia_index_unique(candidates):
            path = os.path.join(folder, name + ".ypo")
            if os.path.exists(path):
                return path

    for folder in folders:
        if os.path.isdir(folder):
            try:
                for fname in os.listdir(folder):
                    if fname.lower() == (safe.lower() + ".ypo"):
                        return os.path.join(folder, fname)
            except Exception:
                pass
    return ""


def _cia_index_all_ypo_files():
    """Lista os .ypo disponíveis para medir a grandeza da Machina. Leitura apenas."""
    folders = ["./DATA", "./data", ".DATA", ".data", "./base", "."]
    paths = []
    seen = set()

    for folder in folders:
        if not os.path.isdir(folder):
            continue
        try:
            for fname in os.listdir(folder):
                if not fname.lower().endswith(".ypo"):
                    continue
                path = os.path.join(folder, fname)
                key = os.path.abspath(path).lower()
                if key in seen:
                    continue
                seen.add(key)
                paths.append(path)
        except Exception:
            pass

    return sorted(paths, key=lambda p: os.path.basename(p).lower())


def _cia_index_norm_unique(value):
    return re.sub(r"\s+", " ", str(value or "").strip()).casefold()


def _cia_index_totais_machina():
    """Totais reais e únicos de verbetes e ítimos em todos os .ypo encontrados."""
    itimos_real = 0
    itimos_unicos = set()
    verbetes_real = 0
    verbetes_unicos = set()

    for ypo_file in _cia_index_all_ypo_files():
        try:
            with open(ypo_file, "r", encoding="utf-8", errors="replace") as f:
                for raw in f:
                    line = raw.strip()
                    if not line or not line.startswith("|"):
                        continue
                    itens = _cia_index_itimos_from_pipe(line.split("|"))
                    for item in itens:
                        clean_item = str(item or "").strip()
                        if not clean_item:
                            continue
                        itimos_real += 1
                        itimos_unicos.add(_cia_index_norm_unique(clean_item))

                        palavras = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:[-'][A-Za-zÀ-ÖØ-öø-ÿ0-9]+)*", clean_item)
                        verbetes_real += len(palavras)
                        for palavra in palavras:
                            verbetes_unicos.add(_cia_index_norm_unique(palavra))
        except Exception:
            pass

    return {
        "verbetes_real": verbetes_real,
        "verbetes_unicos": len([v for v in verbetes_unicos if v]),
        "itimos_real": itimos_real,
        "itimos_unicos": len([v for v in itimos_unicos if v]),
    }


def _cia_index_parse_int(value):
    try:
        return int(str(value).strip())
    except Exception:
        return 0


def _cia_index_itimos_from_pipe(pipe):
    """Extrai ítimos reais de uma linha .ypo, preservando formatos históricos."""
    if len(pipe) >= 8:
        partes_barra = [p.strip() for p in pipe[7:] if p.strip()]
        if len(partes_barra) > 1:
            return partes_barra
        if len(partes_barra) == 1:
            tail = partes_barra[0]
        else:
            tail = ""
    elif len(pipe) >= 7:
        tail = pipe[6].strip()
    else:
        tail = ""

    if not tail:
        return []

    return [item.strip() for item in re.split(r"\s+", tail) if item.strip()]


def _cia_index_formata_milhar(value):
    try:
        return f"{int(value):,}".replace(",", ".")
    except Exception:
        return str(value)


def _cia_index_formata_cientifica(value):
    try:
        valor = int(value)
        if valor == 0:
            return "0,000e+00"
        return f"{valor:.3e}".replace(".", ",")
    except Exception:
        return ""


def _cia_index_linha_index(tema, variacoes):
    return f"{tema} : {_cia_index_formata_milhar(variacoes)}"


def _cia_index_linha_index_cientifica(tema, variacoes):
    inteiro = _cia_index_formata_milhar(variacoes)
    cientifica = _cia_index_formata_cientifica(variacoes)
    return f"{tema} : {inteiro} = {cientifica}"


def _cia_index_file_path():
    candidates = [
        os.path.join("./base", "index"),
        os.path.join("./base", "index.txt"),
        os.path.join("./base", "INDEX.txt"),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return candidates[0]


def _cia_index_parse_index_line(clean):
    clean = str(clean or "").strip()
    if not clean or clean.startswith("#"):
        return "", ""

    if clean.startswith("|"):
        parts = [p.strip() for p in clean.split("|") if p.strip()]
        if len(parts) >= 2:
            return parts[0], parts[1]

    part_line = clean.partition(" : ")
    if part_line[1]:
        return part_line[0].strip(), part_line[2].strip()

    match = re.match(r"^(.+?)\s*[:=]\s*(.+)$", clean)
    if match:
        return match.group(1).strip(), match.group(2).strip()

    return "", ""


def _cia_index_find_index_line(nome_tema):
    path = _cia_index_file_path()
    tema_key = str(nome_tema or "").strip().upper()
    if not os.path.exists(path):
        return path, ""

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                parsed_tema, _parsed_value = _cia_index_parse_index_line(line.strip())
                if parsed_tema.upper() == tema_key:
                    return path, line.rstrip("\n")
    except Exception:
        pass

    return path, ""


def _cia_index_numeros_tema(nome_tema):
    """Recalcula o INDEX do tema em foco. Não é estimativa; é produto combinatório lido do .ypo."""
    tema = str(nome_tema or "").strip()
    ypo_file = _cia_index_find_ypo_file(tema)

    linhas = 0
    qtd_itimos = 0
    qtd_itimos_declarados = 0
    variacoes = 1
    itimos_lista = []
    divergencias = 0

    if ypo_file:
        try:
            with open(ypo_file, "r", encoding="utf-8", errors="replace") as f:
                for raw in f:
                    line = raw.strip()
                    if not line or not line.startswith("|"):
                        continue
                    pipe = line.split("|")
                    itens = _cia_index_itimos_from_pipe(pipe)
                    qtd_real_linha = len(itens)
                    qtd_declarada_linha = _cia_index_parse_int(pipe[5]) if len(pipe) > 5 else 0
                    qtd_para_variacao = qtd_real_linha or qtd_declarada_linha

                    if qtd_para_variacao <= 0:
                        continue

                    linhas += 1
                    variacoes *= qtd_para_variacao
                    qtd_itimos += qtd_para_variacao
                    qtd_itimos_declarados += qtd_declarada_linha
                    itimos_lista.extend(itens)

                    if qtd_declarada_linha and qtd_real_linha and qtd_declarada_linha != qtd_real_linha:
                        divergencias += 1
        except Exception:
            ypo_file = ""

    if linhas == 0:
        variacoes = 0

    palavras = []
    for item in itimos_lista:
        palavras.extend(re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:[-'][A-Za-zÀ-ÖØ-öø-ÿ0-9]+)*", item))

    status = "OK"
    if not ypo_file:
        status = "SEM_ARQUIVO"
    elif linhas == 0:
        status = "SEM_LINHAS"
    elif divergencias:
        status = "CONFERIR_QTD_ITIMOS"

    index_path, index_line = _cia_index_find_index_line(tema)

    return {
        "tema": tema,
        "arquivo": ypo_file,
        "index_path": index_path,
        "index_line": index_line,
        "variacoes": variacoes,
        "linhas": linhas,
        "itimos": qtd_itimos,
        "itimos_declarados": qtd_itimos_declarados,
        "palavras": len(palavras),
        "status": status,
    }


def build_cia_index_html(curr_ypoema):
    """Lente Index: informação exata do tema em foco para o leitor."""
    tema = (
        st.session_state.get("tema_atual_para_analise")
        or st.session_state.get("tema_em_analise")
        or st.session_state.get("tema")
        or ""
    )
    row = _cia_index_numeros_tema(tema)
    versos = len(_cia_poema_lines(curr_ypoema))
    totais = _cia_index_totais_machina()

    return f"""
        <p>Linhas: {row['linhas']}<br>
        Versos: {versos}<br>
        Ítimos: {row['itimos']}<br>
        Palavras: {row['palavras']}</p>

        <p>Total de verbetes na Machina: {_cia_index_formata_milhar(totais['verbetes_real'])} reais / {_cia_index_formata_milhar(totais['verbetes_unicos'])} únicos<br>
        Total de ítimos na Machina: {_cia_index_formata_milhar(totais['itimos_real'])} reais / {_cia_index_formata_milhar(totais['itimos_unicos'])} únicos</p>

        <p>Variações possíveis: {_cia_index_formata_milhar(row['variacoes'])}<br>
        Notação científica: {_cia_index_formata_cientifica(row['variacoes'])}</p>
    """

def render_cia_stage(curr_ypoema):
    """Renderiza a análise da CIA; traduz o conteúdo quando o leitor troca de idioma."""
    cia_offset = int(st.session_state.get("cia_line0_offset_px", 0))
    cia_font = st.session_state.get("cia_font", "Trebuchet MS")
    cia_size = int(st.session_state.get("cia_size", 18))
    mood = st.session_state.get("cia_mood", CIA_MOODS[0])

    def _translate_analysis(markdown_text):
        return _translate(str(markdown_text).strip())

    def _to_html_block(markdown_text, underline_strong=False):
        html = _translate_analysis(markdown_text)
        while "**" in html:
            html = html.replace("**", "<strong>", 1)
            html = html.replace("**", "</strong>", 1)
        if underline_strong:
            html = html.replace("<strong>", "<strong><u>")
            html = html.replace("</strong>", "</u></strong>")
        html = html.replace("  \n", "\n")
        html = html.replace("\r\n", "\n")
        html = re.sub(r"\n{3,}", "\n\n", html)
        paragraphs = [p.strip() for p in html.split("\n\n") if p.strip()]
        return "".join(f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paragraphs)

    st.markdown(
        f"<div class='cia-stage-box' style='margin-top:{cia_offset}px;'>",
        unsafe_allow_html=True,
    )
    _write_ypoema(build_cia_header(), None)
    st.markdown("&nbsp;", unsafe_allow_html=True)

    if mood == "Sintética":
        analysis_html = _to_html_block(build_cia_analysis_sintetica(curr_ypoema))
        content = analysis_html
    elif mood == "Sintática":
        analysis_html = _to_html_block(build_cia_analysis(curr_ypoema), underline_strong=True)
        analysis_free_html = _to_html_block(build_cia_analysis_free(curr_ypoema))
        outro_angulo = _translate("Outro ângulo")
        content = f"""{analysis_html}
            <div class='cia-stage-sep'><strong>{outro_angulo}</strong></div>
            {analysis_free_html}"""
    elif mood == "Formal":
        analysis_html = _to_html_block(build_cia_analysis_formal(curr_ypoema))
        content = analysis_html
    elif mood in ("Reduzida", "Resumida"):
        analysis_html = _to_html_block(build_cia_analysis_resumida(curr_ypoema))
        content = analysis_html
    elif mood == "Completa":
        analysis_html = _to_html_block(build_cia_analysis_completa(curr_ypoema))
        content = analysis_html
    elif mood == "Index":
        content = build_cia_index_html(curr_ypoema)
    else:
        analysis_html = _to_html_block("Este mood ainda não entrou em operação na CIA.")
        content = analysis_html

    st.markdown(
        f"""
        <style>
        .cia-stage-box .cia-stage-text p {{
            margin: 0 0 1.15em 0;
        }}
        .cia-stage-box .cia-stage-text p:last-child {{
            margin-bottom: 0;
        }}
        .cia-stage-box .cia-stage-sep {{
            margin: 1.25em 0 1em 0;
            padding-top: 0.8em;
            border-top: 1px solid rgba(0,0,0,0.12);
            opacity: 0.95;
        }}
        </style>
        <div class='cia-stage-text' style="font-family:{cia_font}; font-size:{cia_size}px; line-height:1.42;">
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_cia_sidebar():
    """Renderiza os moods da CIA em desenho compacto 2x2 + centro."""
    current_mood = st.session_state.get("cia_mood", CIA_MOODS[0])
    if current_mood not in CIA_MOODS:
        current_mood = CIA_MOODS[0]
        st.session_state.cia_mood = current_mood

    rows = [("Sintática", "Sintética"), ("Formal", "Reduzida")]
    for left_mood, right_mood in rows:
        col_left, col_right = st.sidebar.columns(2)
        with col_left:
            label = f"• {left_mood}" if current_mood == left_mood else left_mood
            if st.button(label, key=f"cia_mood_btn_{left_mood}", use_container_width=True):
                st.session_state.cia_mood = left_mood
        with col_right:
            label = f"• {right_mood}" if current_mood == right_mood else right_mood
            if st.button(label, key=f"cia_mood_btn_{right_mood}", use_container_width=True):
                st.session_state.cia_mood = right_mood

    col_l, col_c, col_r = st.sidebar.columns([0.5, 1.0, 0.5])
    with col_c:
        label = "• Completa" if current_mood == "Completa" else "Completa"
        if st.button(label, key="cia_mood_btn_Completa", use_container_width=True):
            st.session_state.cia_mood = "Completa"


def draw_sidebar_panel_buttons(chosen_id):
    """Alterna entre Machina e CIA com botões horizontais, apenas em yPoemas."""
    if chosen_id != "2":
        st.session_state["sidebar_panel"] = "Machina"
        return

    col_mach, col_cia = st.sidebar.columns([1, 1])
    with col_mach:
        if st.button("Machina", key="sidebar_panel_machina", use_container_width=True):
            st.session_state["sidebar_panel"] = "Machina"
    with col_cia:
        if st.button("CIA", key="sidebar_panel_cia", use_container_width=True):
            st.session_state["sidebar_panel"] = "CIA"
