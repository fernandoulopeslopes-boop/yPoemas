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


CIA_WORD_1 = ["Informação", "Invenção", "Imaginação", "Imagética", "Injeção"]
CIA_WORD_2 = ["Analítica", "Artificial", "Analógica", "Afetiva", "Adicional", "Ampliada", "Avançada", "Acadêmica"]
CIA_MOODS = [
    "Sintática",
    "Sintética",
    "Formal",
    "Reduzida",
    "Completa",
]


REGRA_ZERO_CIA = """
REGRA_ZERO_CIA

Conduta comum a todos os moods:
- posição flexível;
- função crítica respeitada;
- consulta obrigatória às listas funcionais;
- random apenas entre candidatos plausíveis;
- nenhuma fórmula pode mentir sobre a função do FORTE_CANDIDATO.

A primeira linha e o último verso continuam candidatos fortes, mas não são
obrigações automáticas. O FECHO real recebe atenção especial porque, na
arquitetura dos yPoemas, costuma carregar reverberação, resumo da ópera,
estranheza produtiva ou convite à releitura.
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


def _cia_bloco_sintatico_reforco(poema_lines, used_lines):
    """Garante lastro sintático sem virar aula seca de gramática."""
    line = _cia_pick_role(poema_lines, "miolo", used_lines, poema_lines[len(poema_lines) // 2])
    clip = _cia_clip(line)
    return random.choice([
        f"Em “{clip}”, a **sintaxe** organiza o verso como movimento interno: o **verbo** não apenas informa, mas põe a imagem em ação.",
        f"Em “{clip}”, a **oração** ganha força pelo modo como distribui **sujeito**, **predicado** e pausa, deixando o sentido avançar por tensão.",
        f"Em “{clip}”, a **pontuação** interfere no ritmo da **oração** e regula a entrada do leitor no movimento sintático do poema.",
    ])


def ensure_cia_name(force=False):
    """Gera um nome mutável para a CIA e o preserva durante a sessão."""
    if force or not st.session_state.get("cia_name"):
        st.session_state["cia_name"] = (
            "Centro de "
            + random.choice(CIA_WORD_1)
            + " "
            + random.choice(CIA_WORD_2)
        )


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
    """Descrição poética da CIA, gerada pela própria Machina sem repetir o título."""
    ensure_cia_name()
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
    zone = _cia_line_zone(poema_lines, line)
    if zone in ("final", "tardia"):
        return random.choice([
            f"Tomado como entrada retroativa, “{clip}” recolhe parte do percurso e permite reler o que veio antes.",
            f"A leitura pode entrar pelo fim em “{clip}”: o verso não abre o poema, mas reorganiza retrospectivamente seu campo de forças.",
            f"Quase no fecho, “{clip}” funciona como ponto de inflexão; dali o percurso anterior ganha outro rumo de leitura.",
            f"“{clip}” oferece uma entrada pelo avesso: em vez de inaugurar o texto, condensa uma tensão que já vinha se formando.",
        ])
    if zone == "miolo":
        op = random.choice(CIA_OPERACOES_CRITICAS)
        verbo = random.choice(CIA_VERBOS_SURGIMENTO)
        return random.choice([
            f"Em “{clip}”, a leitura encontra um {op}: o verso {verbo} como ponto de entrada sem depender da ordem linear do texto.",
            f"“{clip}” oferece um rumo de leitura pelo centro do poema; a partir daí, o percurso ganha outra organização.",
            f"Quando “{clip}” {verbo} como ponto de entrada, o texto se deixa ler por uma passagem interna, não apenas pelo primeiro verso.",
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
    if zone == "inicial":
        return random.choice([
            f"Retomado no desenvolvimento, “{clip}” deixa de ser apenas entrada e passa a sustentar a direção crítica da leitura.",
            f"Quando volta ao desenvolvimento, “{clip}” funciona como eixo de leitura: o início passa a iluminar o percurso.",
            f"No desenvolvimento, “{clip}” ganha outra função: não abre de novo o poema, mas ajuda a organizar sua tensão interna.",
        ])
    if zone in ("final", "tardia"):
        return random.choice([
            f"No desenvolvimento crítico, “{clip}” atua como aproximação do fecho: a imagem concentra uma tensão que o fim recolhe.",
            f"“{clip}” aparece como zona de passagem para o encerramento, mudando o peso do que vinha sendo lido.",
            f"Quase no fim, “{clip}” adensa o percurso e prepara a reverberação que a leitura ainda precisa atravessar.",
        ])
    op = random.choice(CIA_OPERACOES_CRITICAS)
    verbo = random.choice(CIA_VERBOS_SURGIMENTO)
    return random.choice([
        f"Em “{clip}”, a linguagem ganha densidade: o verso concentra imagem, tensão e atmosfera sem dissolver o mistério.",
        f"Quando “{clip}” {verbo} no desenvolvimento, a leitura encontra um {op} que altera o peso do percurso.",
        f"O centro de força passa por “{clip}”; ali o poema ganha espessura e evita seguir por caminho óbvio.",
        f"Há em “{clip}” uma medula verbal: o texto se mostra breve na superfície e mais largo por dentro.",
    ])


def _cia_regra_zero_fecho(poema_lines, line):
    """FECHO: preserva reverberação e dá atenção especial ao fecho real."""
    clip = _cia_clip(line)
    zone = _cia_line_zone(poema_lines, line)
    if zone == "final":
        return random.choice([
            f"No fecho, “{clip}” recolhe o percurso sem esgotá-lo; a última linha concentra a pressão e deixa o poema ainda reverberando.",
            f"A chegada a “{clip}” dá ao poema seu ponto de recolhimento: não fecha o sentido, mas organiza o eco do que veio antes.",
            f"Em “{clip}”, o poema encontra uma saída que ainda preserva atrito. O fim recolhe a leitura sem transformar a tensão em resposta única.",
            f"O último verso, “{clip}”, funciona como resumo da ópera: conserva estranheza e convida a leitura a voltar sobre o percurso.",
        ])
    if zone == "inicial":
        return random.choice([
            f"O encerramento crítico pode retornar a “{clip}”: o começo reaparece como eco e dá outro peso ao percurso.",
            f"Ao voltar para “{clip}”, a leitura fecha por retomada: o início ganha função de reverberação, não de simples abertura.",
            f"O fecho da análise encontra em “{clip}” um gancho de retorno; o primeiro gesto passa a iluminar o fim.",
        ])
    op = random.choice(CIA_OPERACOES_CRITICAS)
    verbo = random.choice(CIA_VERBOS_SURGIMENTO)
    return random.choice([
        f"A reverberação pode voltar a “{clip}”: esse ponto reorganiza o percurso e faz o final ser lido por outra direção.",
        f"O encerramento crítico se apoia em “{clip}” porque essa imagem aponta para a tensão que o fim recolhe.",
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
    """Cria listas funcionais para ABERTURA, MIOLO e FECHO.

    Um mesmo FORTE_CANDIDATO pode aparecer em mais de uma lista.
    A ordem dos tratores não altera o viaduto: a posição depende da leitura.
    """
    fortes = _cia_forte_candidatos(poema_lines)
    if not fortes:
        return {"abertura": [], "miolo": [], "fecho": []}

    first = poema_lines[0]
    middle = poema_lines[len(poema_lines) // 2]
    last = poema_lines[-1]

    perguntas = [line for line in fortes if "?" in line]
    suspensos = [line for line in fortes if "..." in line or "…" in line]
    marcados = [line for line in fortes if line.count(",") >= 1 or "(" in line or ")" in line]

    lista_best_ABERTURA = _cia_unique([first] + perguntas + suspensos + fortes + [last])
    lista_best_MIOLO = _cia_unique(marcados + fortes + [middle, first, last])
    lista_best_FECHO = _cia_unique([last] + suspensos + perguntas + fortes + [first])

    return {
        "abertura": lista_best_ABERTURA,
        "miolo": lista_best_MIOLO,
        "fecho": lista_best_FECHO,
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
        if last in pool and last not in used_lines and random.random() < 0.62:
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


def _cia_critico_abertura(poema_lines, used_lines):
    """Primeiro bloco: portal, inflexão ou entrada retroativa, conforme REGRA_ZERO_CIA."""
    abertura = _cia_pick_role(poema_lines, "abertura", used_lines, poema_lines[0])
    return _cia_regra_zero_abertura(poema_lines, abertura)


def _cia_critico_fecho(poema_lines, used_lines, prefer_specific=True):
    """Último bloco: melhor reverberação final entre candidatos plausíveis."""
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
    return (
        f"Na abertura, “{clip}” firma o primeiro movimento verbal do poema: "
        f"a **sintaxe** distribui a imagem inicial e prepara o **predicado** crítico da leitura."
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
    """Cria blocos de MIOLO por grupos de 'ordem de nobreza'.

    Regra interna: não é quantidade por quantidade; é lastro sintático visível.
    A Sintática tenta contemplar básico, articulação, expressivo e desenho/ritmo
    quando houver pertinência e espaço.
    """
    inner = poema_lines[1:-1] if len(poema_lines) > 2 else poema_lines[:]
    candidates = []

    # 1. Básico: sujeito / verbo / pronome / predicado.
    pessoais = [line for line in inner if re.search(r"\b(eu|me|mim|meu|minha|nós|nosso|nossa|ele|ela|eles|elas|seu|sua)\b", line.lower())]
    line = pessoais[0] if pessoais else (inner[0] if inner else "")
    if line:
        _cia_sintatica_add_candidate(
            candidates,
            "basico",
            [line],
            f"Em “{_cia_clip(line)}”, a análise encontra uma base verbal: o **sujeito** se deixa perceber pelo enunciado e o **verbo** organiza o gesto da frase."
        )

    # 2. Articulação: oração / complemento / conectivo / coordenação / subordinação.
    subordinadas = [line for line in inner if re.search(r"\b(se|quando|embora|porque|que)\b", line.lower())]
    coordenadas = [line for line in inner if re.search(r"\b(e|ou|mas)\b", line.lower())]
    if subordinadas:
        line = subordinadas[0]
        _cia_sintatica_add_candidate(
            candidates,
            "articulacao",
            [line],
            f"Em “{_cia_clip(line)}”, a **subordinação** cria dependência interna: a **oração** avança por condição, tempo ou explicação, e não por simples sequência."
        )
    elif coordenadas:
        line = coordenadas[0]
        _cia_sintatica_add_candidate(
            candidates,
            "articulacao",
            [line],
            f"Em “{_cia_clip(line)}”, o **conectivo** articula a passagem entre partes da frase; a **coordenação** aproxima segmentos sem fundi-los por completo."
        )
    elif inner:
        line = inner[min(len(inner) - 1, len(inner) // 2)]
        _cia_sintatica_add_candidate(
            candidates,
            "articulacao",
            [line],
            f"Em “{_cia_clip(line)}”, a **oração** funciona como unidade de articulação: o verso distribui imagem e **complemento** sem perder a direção do período."
        )

    # 3. Expressivo: elipse / enumeração / inciso / regência / pontuação / reticências.
    reticencias = [line for line in inner if "..." in line or "…" in line]
    perguntas = [line for line in inner if "?" in line]
    incisos = [line for line in inner if "(" in line or ")" in line]
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
            f"Em “{_cia_clip(line)}”, a **pontuação** interrogativa não é ornamento: ela muda a pressão da **oração** e abre uma tensão de leitura."
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
            f"A **enumeração** em “{_cia_clip(line)}” trabalha por acúmulo: o verso amplia a frase sem perder o eixo do **predicado**."
        )
    elif inner:
        line = inner[-1]
        _cia_sintatica_add_candidate(
            candidates,
            "expressivo",
            [line],
            f"Em “{_cia_clip(line)}”, a **elipse** possível deixa uma falta trabalhando no verso; a frase sugere mais do que entrega."
        )

    # 4. Desenho e ritmo: anáfora / paralelismo / repetição / deslocamento.
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

    # Remove candidatos que usariam verso já reservado, preservando o grupo se possível.
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
    """Outro ângulo: leitura de contraste, sem mencionar método e sem repetir trechos por comodidade."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "Sem texto em foco para leitura."

    used = set(st.session_state.get("_cia_used_lines", []))
    local_used = set(used)

    abertura_line = _cia_pick_role(poema_lines, "abertura", local_used, "")
    destaque_line = _cia_pick_role(poema_lines, "miolo", local_used, "")
    fecho_line = _cia_pick_role(poema_lines, "fecho", local_used, "")

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

    if (not fecho_line) or (fecho_line in {abertura_line, destaque_line} and len(poema_lines) > 2):
        fecho = random.choice([
            "O encerramento recolhe a tensão sem resolver tudo. O poema termina preservando uma zona de eco.",
            "Ao final, a leitura não encontra uma explicação única, mas um resto de intensidade que continua trabalhando.",
            "O fim não domestica o percurso: apenas concentra sua última reverberação.",
        ])
    else:
        fecho = _cia_regra_zero_fecho(poema_lines, fecho_line)

    return _cia_join([abertura, desenvolvimento, fecho])


def build_cia_analysis_sintetica(curr_ypoema):
    """Sintética: núcleo de tensão com atmosfera, sem virar resumo banal."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "**requer apuração manual**"

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

    abertura = random.choice([
        f"A primeira presença do poema é o seu desenho: **{qtd_linhas} linhas** em **{blocos} bloco{'s' if blocos != 1 else ''}** dão ao texto uma forma de chegada antes mesmo da interpretação.",
        f"O poema se apresenta como arquitetura visível: **{qtd_linhas} linhas** e **{blocos} bloco{'s' if blocos != 1 else ''}** regulam o modo como a leitura entra no texto.",
        f"Antes do sentido se explicar, há uma forma em cena: **{qtd_linhas} linhas** distribuídas em **{blocos} bloco{'s' if blocos != 1 else ''}** organizam o fôlego inicial da leitura.",
    ])

    desenvolvimento = []

    extensoes = []
    if curtas:
        extensoes.append(f"**{curtas} linhas breves**")
    if medias:
        extensoes.append(f"**{medias} médias**")
    if longas:
        extensoes.append(f"**{longas} mais longas**")

    if len(extensoes) >= 2:
        extensoes_texto = ", ".join(extensoes[:-1]) + " e " + extensoes[-1]
    elif extensoes:
        extensoes_texto = extensoes[0]
    else:
        extensoes_texto = ""

    if extensoes_texto:
        desenvolvimento.append(random.choice([
            f"A alternância de extensão também trabalha: {extensoes_texto} criam variação de fôlego, evitando que o poema avance em linha reta demais.",
            f"O ritmo nasce da medida dos versos: {extensoes_texto} fazem a leitura acelerar, conter-se ou respirar conforme o desenho pede.",
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
    """Reduzida: leitura curta, objetiva e distinta da Sintética."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "**requer apuração manual**"

    used_lines = set()
    abertura_line = _cia_pick_role(poema_lines, "abertura", used_lines, poema_lines[0])
    destaque_line = _cia_pick_role(poema_lines, "miolo", used_lines, poema_lines[len(poema_lines) // 2])

    abertura = _cia_regra_zero_abertura(poema_lines, abertura_line)
    desenvolvimento = _cia_regra_zero_miolo(poema_lines, destaque_line)

    fecho = _cia_critico_fecho(poema_lines, used_lines, prefer_specific=True)
    return _cia_join([abertura, desenvolvimento, fecho])

def build_cia_analysis_completa(curr_ypoema):
    """Completa: leitura ampla com imagem, forma, tensão, camada sintática e fecho."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "**requer apuração manual**"

    used_lines = set()
    qtd_linhas = len(poema_lines)
    abertura_line = _cia_pick_role(poema_lines, "abertura", used_lines, poema_lines[0])
    destaque_line = _cia_pick_role(poema_lines, "miolo", used_lines, poema_lines[len(poema_lines) // 2])

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

def render_cia_stage(curr_ypoema):
    """Renderiza a análise da CIA; traduz o conteúdo quando o leitor troca de idioma."""
    cia_offset = int(st.session_state.get("cia_line0_offset_px", 0))
    cia_font = st.session_state.get("cia_font", "Trebuchet MS")
    cia_size = int(st.session_state.get("cia_size", 18))
    mood = st.session_state.get("cia_mood", CIA_MOODS[0])

    def _translate_analysis(markdown_text):
        return _translate(str(markdown_text).strip())

    def _to_html_block(markdown_text):
        html = _translate_analysis(markdown_text)
        while "**" in html:
            html = html.replace("**", "<strong>", 1)
            html = html.replace("**", "</strong>", 1)
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
        analysis_html = _to_html_block(build_cia_analysis(curr_ypoema))
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
