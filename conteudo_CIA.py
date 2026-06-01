import re
import random
from datetime import datetime

import streamlit as st

CIA_MOODS = ["Sintática", "Sintética", "Resumida", "Completa"]


def build_cia_stage_title():
    """Título objetivo da análise em foco."""
    mood = st.session_state.get("cia_mood", "Sintática")
    return f"Análise {mood}"


def _cia_first_token(line):
    token = line.strip().split(" ")[0] if line.strip() else ""
    return token.strip("“”\"'()[]{}.,;:!?…-").lower()


def _cia_first_two_tokens(line):
    parts = [p.strip("“”\"'()[]{}.,;:!?…-").lower() for p in line.strip().split()[:2]]
    return " ".join([p for p in parts if p])


def _cia_is_attribution_line(line):
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith("(") and stripped.endswith(")"):
        return True
    if stripped.startswith("（") and stripped.endswith("）"):
        return True
    return False


def _cia_clip(line, limit=45):
    """Normaliza espaços e corta trechos longos para caber melhor na coluna da CIA."""
    if not line:
        return ""
    clean = re.sub(r"\s+", " ", str(line)).strip()
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + "..."


def build_machina_reading(poema_lines, used_lines=None, avoid_fecho=False):
    """Pequena leitura viva do texto, sem repetir logo de saída versos já usados em outros blocos."""
    if not poema_lines:
        return ""

    used_lines = set(used_lines or [])
    current_year = datetime.now().year

    def available(lines, skip_fecho=False):
        pool = []
        fecho = poema_lines[-1] if poema_lines else ""
        for line in lines:
            if not line or line in used_lines:
                continue
            if skip_fecho and line == fecho:
                continue
            pool.append(line)
        return pool

    future_candidates = []
    for line in poema_lines:
        years = re.findall(r"\b(1[89]\d{2}|20\d{2}|21\d{2})\b", line)
        if any(int(y) > current_year for y in years):
            future_candidates.append(line)
    pool = available(future_candidates, skip_fecho=avoid_fecho)
    if pool:
        line = random.choice(pool)
        return random.choice([
            f"Há um deslocamento particularmente vivo em **“{_cia_clip(line)}”**: a data futura abre o poema para um tempo que ainda não chegou, mas já pesa dentro dele.",
            f"Em **“{_cia_clip(line)}”**, a projeção para o futuro não passa despercebida. Ela empurra o poema para fora do presente e lhe dá uma ousadia temporal muito própria.",
            f"A data futura em **“{_cia_clip(line)}”** muda o regime de leitura do texto: o poema deixa de falar só do agora e passa a respirar adiante.",
        ])

    ref_candidates = []
    for line in poema_lines:
        words = line.split()
        if len(words) > 1:
            inner_caps = [w.strip("“”\"'()[]{}.,;:!?…-") for w in words[1:] if w[:1].isupper()]
            if inner_caps:
                ref_candidates.append(line)
    pool = available(ref_candidates, skip_fecho=avoid_fecho)
    if pool:
        line = random.choice(pool)
        return random.choice([
            f"Há uma surpresa boa em **“{_cia_clip(line)}”**: a referência inesperada puxa o poema para fora do previsível e lhe dá um brilho próprio.",
            f"Em **“{_cia_clip(line)}”**, o texto ganha uma abertura particular. O nome ou referência que entra ali desloca o campo do poema e amplia a leitura.",
            f"Esse verso — **“{_cia_clip(line)}”** — chama atenção pela referência que carrega. Ela dá ao poema uma vida mais particular do que a leitura técnica, sozinha, daria conta de mostrar.",
        ])

    marked = [line for line in poema_lines if "..." in line or "?" in line or ":" in line or ";" in line]
    pool = available(marked, skip_fecho=avoid_fecho)
    if pool:
        line = random.choice(pool)
        return random.choice([
            f"Há algo de especialmente vivo em **“{_cia_clip(line)}”**. O verso foge do esperado e deixa uma impressão que não é só técnica.",
            f"**“{_cia_clip(line)}”** funciona como pequena pérola do texto: ali o poema parece ganhar uma temperatura própria, mais ousada ou mais inesperada.",
            f"Neste ponto — **“{_cia_clip(line)}”** — o poema oferece uma surpresa que vale por si mesma. É uma dessas linhas que pedem mais do que leitura mecânica.",
        ])

    fecho_pool = available([poema_lines[-1]] if poema_lines else [])
    if fecho_pool:
        fecho = fecho_pool[0]
        return random.choice([
            f"O fecho em **“{_cia_clip(fecho)}”** guarda uma qualidade difícil de reduzir a esquema. Há ali um resto de vida que ultrapassa a engrenagem da análise.",
            f"Também o verso final — **“{_cia_clip(fecho)}”** — merece um olhar menos técnico: ele concentra uma beleza ou um estranhamento que o poema soube guardar para o fim.",
            f"Em **“{_cia_clip(fecho)}”**, o poema deixa algo que não se esgota na análise. O verso final guarda um pequeno excesso de vida própria.",
        ])

    return ""


def build_cia_analysis(curr_ypoema):
    """Leitura sintática real no palco, com ordem variável, sem redundância interna e com 2 a 5 figuras."""
    raw_parts = [part.strip() for part in curr_ypoema.replace("<br/>", "<br>").split("<br>")]
    lines = [part for part in raw_parts if part]
    poema_lines = lines[1:] if len(lines) > 1 else []
    mood = st.session_state.get("cia_mood", CIA_MOODS[0])
    tema = st.session_state.get("tema", "")

    if mood != "Sintática":
        return "Este mood ainda não entrou em operação."

    if not poema_lines:
        return "**requer apuração manual**"

    candidates = []

    perguntas = [line for line in poema_lines if "?" in line]
    if perguntas:
        line = perguntas[0]
        candidates.append({"lines": [line], "text":
            f"Em **“{_cia_clip(line)}”** há **interrogação**. A frase abre o poema para a incerteza, para a provocação ou para a espera de resposta, em vez de afirmar de saída."
        })

    reticencias = [line for line in poema_lines if "..." in line or "…" in line]
    if reticencias:
        line = reticencias[0]
        candidates.append({"lines": [line], "text":
            f"As **reticências** de **“{_cia_clip(line)}”** funcionam como **suspensão sintática**: o verso retém o fechamento e espalha o sentido para além da linha."
        })

    first_tokens = {}
    first_two = {}
    for line in poema_lines:
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
        candidates.append({"lines": exemplos, "text":
            f"Há **paralelismo sintático** entre **“{_cia_clip(exemplos[0])}”** e **“{_cia_clip(exemplos[1])}”**. A estrutura reaparece em molde próximo e cria cadência com reforço de sentido."
        })
    elif anafora_key:
        exemplos = first_tokens[anafora_key][:2]
        candidates.append({"lines": exemplos, "text":
            f"A repetição inicial de **“{_cia_clip(exemplos[0])}”** e **“{_cia_clip(exemplos[1])}”** produz **anáfora**. O poema insiste no mesmo arranque frasal para firmar seu movimento."
        })

    enumeracoes = [line for line in poema_lines if line.count(",") >= 2]
    if enumeracoes:
        line = enumeracoes[0]
        candidates.append({"lines": [line], "text":
            f"Em **“{_cia_clip(line)}”** aparece **enumeração**. O acúmulo de termos organiza o pensamento por justaposição e amplia o campo semântico do verso."
        })

    subordinadas = [line for line in poema_lines if re.search(r"\b(se|quando|embora|porque|que)\b", line.lower())]
    coordenadas = [line for line in poema_lines if re.search(r"\b(e|ou|mas)\b", line.lower()) and "," in line]

    if subordinadas:
        line = subordinadas[0]
        candidates.append({"lines": [line], "text":
            f"Em **“{_cia_clip(line)}”** há **subordinação** visível. A frase depende de condição, tempo ou explicação para avançar, e isso articula o andamento do texto."
        })
    elif coordenadas:
        line = coordenadas[0]
        candidates.append({"lines": [line], "text":
            f"Em **“{_cia_clip(line)}”** há **coordenação** explícita. Os segmentos se articulam sem perder autonomia e o verso ganha soma ou contraste."
        })

    cortes = []
    for i, line in enumerate(poema_lines[:-1]):
        nxt = poema_lines[i + 1]
        if line and line[-1] not in ".?!:;…)" and (nxt[:1].islower() or len(line.split()) <= 4):
            cortes.append((line, nxt))
    if cortes:
        l1, l2 = cortes[0]
        candidates.append({"lines": [l1, l2], "text":
            f"O verso se encerra em **“{_cia_clip(l1)}”**, mas a frase prossegue em **“{_cia_clip(l2)}”**. A sintaxe atravessa a linha e empurra a leitura para diante."
        })

    if not candidates:
        st.session_state.tema_last_analise = tema
        return "**requer apuração manual**"

    repeated_theme = tema == st.session_state.get("tema_last_analise", "")
    max_figures = min(5, len(candidates))
    min_figures = min(2, len(candidates))
    target_count = max_figures if max_figures <= 3 else random.randint(min_figures, max_figures)

    shuffled = candidates[:]
    random.shuffle(shuffled)
    chosen_meta = shuffled[:target_count]

    used_lines = set()
    body = []
    for item in chosen_meta:
        body.append(item["text"])
        used_lines.update(item["lines"])

    machina_block = build_machina_reading(poema_lines, used_lines=used_lines, avoid_fecho=True)
    if machina_block:
        body.append(machina_block)

    fecho = poema_lines[-1]
    if fecho not in used_lines:
        body.append(random.choice([
            f"O fecho em **“{_cia_clip(fecho)}”** merece atenção porque concentra um último deslocamento do poema. Mesmo quando a figura central aparece antes, é ali que a leitura recolhe ou reabre o que ficou em tensão.",
            f"A última linha — **“{_cia_clip(fecho)}”** — pesa no conjunto porque ali o poema recolhe parte da pressão sintática que vinha distribuindo antes.",
            f"No fecho, **“{_cia_clip(fecho)}”** concentra ou desvia aquilo que a sintaxe foi armando ao longo das linhas.",
            f"Convém não perder de vista o fecho em **“{_cia_clip(fecho)}”**: a linha final recompõe, desloca ou reaperta a tensão do poema.",
            f"O verso final — **“{_cia_clip(fecho)}”** — não entra como sobra. Ele recolhe uma energia sintática que vinha se distribuindo nas linhas anteriores.",
            f"O fechamento em **“{_cia_clip(fecho)}”** pede leitura: é ali que o poema decide se recolhe, desloca ou reabre o seu impulso.",
        ]))

    body.append(random.choice([
        "A Sintática não resume o poema: ela nomeia o que aparece com nitidez e lê o efeito dessas escolhas na construção do sentido.",
        "Aqui a leitura sintática não procura resumir o poema, mas reconhecer figuras visíveis e medir o que elas fazem no andamento do texto.",
        "O foco desta leitura não é o tema em abstrato, mas a engrenagem verbal do poema: nomear o que aparece e ler o efeito de cada escolha.",
        "A leitura sintática se firma menos no assunto do poema do que nas formas que o fazem avançar, hesitar, insistir ou se fechar.",
        "O que interessa aqui não é resumir o poema, mas acompanhar como a construção verbal distribui força, pausa, dependência e corte.",
        "Esta leitura se ocupa menos de explicar o poema do que de perceber como a sintaxe sustenta, torce ou desloca o seu sentido.",
    ]))

    random.shuffle(body)
    if repeated_theme and len(body) > 2:
        random.shuffle(body)

    st.session_state.tema_last_analise = tema
    return "  \n\n".join(body)


def build_cia_analysis_free(curr_ypoema):
    """Leitura livre do mesmo texto em foco, sem usar o manual desta leitura."""
    raw_parts = [part.strip() for part in curr_ypoema.replace("<br/>", "<br>").split("<br>")]
    lines = [part for part in raw_parts if part]
    poema_lines = lines[1:] if len(lines) > 1 else []

    if not poema_lines:
        return "Sem texto em foco para a análise livre."

    abertura = poema_lines[0]
    fecho = poema_lines[-1]
    meio = poema_lines[len(poema_lines) // 2]
    longas = [line for line in poema_lines if "," in line or "..." in line or "?" in line]
    destaque = longas[0] if longas else meio

    p1_options = [
        f"A leitura deste poema começa por uma impressão mais direta: **“{_cia_clip(abertura)}”** não abre apenas o texto, abre também um modo de respirar o que vem depois.",
        f"Lido sem régua prévia, este poema se impõe primeiro por sua entrada: **“{_cia_clip(abertura)}”** já instala um clima verbal que pede atenção antes de qualquer classificação.",
        f"Numa leitura livre, **“{_cia_clip(abertura)}”** funciona menos como começo e mais como chave de acesso: dali o poema já decide o seu passo.",
    ]
    p2_options = [
        f"No corpo do texto, **“{_cia_clip(destaque)}”** chama atenção porque parece condensar a sua energia: há ali um empuxo de linguagem que não depende de nome técnico para ser percebido.",
        f"O miolo do poema ganha força em **“{_cia_clip(destaque)}”**. É o ponto em que a linguagem deixa de apenas dizer e passa a pressionar o leitor com mais densidade.",
        f"Há um centro de gravidade em **“{_cia_clip(destaque)}”**. Mesmo sem manual, percebe-se que alguma coisa ali reorganiza o modo de ler o restante do poema.",
    ]
    p3_options = [
        f"O fecho em **“{_cia_clip(fecho)}”** não chega como sobra. Ele recolhe a tensão anterior e devolve o poema ao leitor com outro peso.",
        f"Já o fechamento — **“{_cia_clip(fecho)}”** — parece decidir o destino do texto: não encerra só, também desloca o que veio antes.",
        f"Quando chega a **“{_cia_clip(fecho)}”**, o poema muda de temperatura. O verso final concentra uma última força e redefine o que ficou ecoando.",
    ]
    p4_options = [
        "O objetivo aqui não é provar nada, mas perceber como o poema vive mesmo antes de ser enquadrado por uma régua analítica.",
        "Esta leitura paralela serve de contraste, para mostrar o que o texto sustenta mesmo sem apoio prévio.",
        "O interesse desta leitura está justamente aí: ver o que o poema oferece quando é lido como acontecimento único, sem memória anterior de tema.",
    ]

    body = [
        random.choice(p1_options),
        random.choice(p2_options),
        random.choice(p3_options),
        random.choice(p4_options),
    ]
    return "  \n\n".join(body)


def build_cia_analysis_sintetica(curr_ypoema):
    """Leitura sintética: condensa o núcleo do poema sem virar comentário longo."""
    raw_parts = [part.strip() for part in curr_ypoema.replace("<br/>", "<br>").split("<br>")]
    lines = [part for part in raw_parts if part]
    poema_lines = lines[1:] if len(lines) > 1 else []

    if not poema_lines:
        return "**requer apuração manual**"

    abertura = poema_lines[0]
    fecho = poema_lines[-1]
    meio = poema_lines[len(poema_lines) // 2]
    destaque = next((line for line in poema_lines if "..." in line or "?" in line), meio)

    p1 = random.choice([
        f"O poema se organiza como uma travessia breve, mas densa: **“{_cia_clip(abertura)}”** já instala o seu campo de força e empurra a leitura para um centro de tensão.",
        f"Desde **“{_cia_clip(abertura)}”**, o poema abre um campo condensado de sentido. Ele não se espalha: concentra.",
        f"A entrada em **“{_cia_clip(abertura)}”** já sugere o núcleo do texto: um movimento que parece simples, mas guarda pressão por dentro.",
        f"Logo em **“{_cia_clip(abertura)}”**, o poema arma o seu eixo e evita dispersão. Tudo tende a convergir para esse impulso inicial.",
    ])

    p2 = random.choice([
        f"No miolo, **“{_cia_clip(destaque)}”** ajuda a perceber que o poema trabalha menos por explicação do que por concentração de imagem, gesto ou tensão verbal.",
        f"O centro do poema ganha nitidez em **“{_cia_clip(destaque)}”**. É ali que a linguagem deixa de apenas dizer e passa a condensar o que está em jogo.",
        f"Há um núcleo de força em **“{_cia_clip(destaque)}”**. O poema parece reunir ali o seu modo de existir: breve na forma, denso na carga.",
        f"Em **“{_cia_clip(destaque)}”**, o texto mostra seu procedimento mais forte: dizer pouco, mas deixar muito reverberando ao redor.",
    ])

    p3 = random.choice([
        f"O fecho em **“{_cia_clip(fecho)}”** recolhe essa pressão e devolve o poema em estado mais concentrado. A síntese não fecha tudo: deixa resto, eco, insistência.",
        f"Quando chega a **“{_cia_clip(fecho)}”**, o poema se concentra ainda mais. O verso final funciona como recolhimento do que vinha sendo armado.",
        f"O fechamento em **“{_cia_clip(fecho)}”** resume sem empobrecer. Ele condensa a energia do texto e a devolve com mais nitidez.",
        f"Em **“{_cia_clip(fecho)}”**, o poema não apenas termina: ele concentra o essencial e deixa a leitura reverberando depois do fim.",
    ])

    p4 = random.choice([
        "O foco aqui não está em nomear figuras, mas em entregar o núcleo do poema sem dissolver sua atmosfera.",
        "O texto condensa o que o poema põe em jogo, preservando seu clima e sua tensão.",
        "A síntese não funciona como atalho pobre, mas como concentração do que o poema tem de mais vivo.",
        "Trata-se de reduzir a dispersão e fazer aparecer o núcleo do poema sem apagar a sua vibração.",
    ])

    used_lines = {abertura, destaque}
    machina = build_machina_reading(poema_lines, used_lines=used_lines, avoid_fecho=True)
    body = [p1, p2, p3, machina, p4]
    body = [b for b in body if b]
    random.shuffle(body)
    return "  \n\n".join(body)


def build_cia_analysis_resumida(curr_ypoema):
    """Mapa ordenado do texto: figura principal + trecho, fiel ao que realmente aparece no poema."""
    raw_parts = [part.strip() for part in curr_ypoema.replace("<br/>", "<br>").split("<br>")]
    lines = [part for part in raw_parts if part]
    poema_lines = lines[1:] if len(lines) > 1 else []

    if not poema_lines:
        return "**requer apuração manual**"

    valid_lines = []
    for line in poema_lines:
        if _cia_is_attribution_line(line):
            continue
        if len(line.strip()) <= 3:
            continue
        valid_lines.append(line)

    if not valid_lines:
        return "**requer apuração manual**"

    first_tokens = {}
    first_two = {}
    for line in valid_lines:
        t1 = _cia_first_token(line)
        t2 = _cia_first_two_tokens(line)
        if t1:
            first_tokens.setdefault(t1, []).append(line)
        if t2:
            first_two.setdefault(t2, []).append(line)

    parallel_lines = set()
    for key, vals in first_two.items():
        if len(vals) >= 2 and len(key.split()) == 2:
            parallel_lines.update(vals)

    anafora_lines = set()
    for key, vals in first_tokens.items():
        if len(vals) >= 2:
            anafora_lines.update(vals)

    entries = []

    for idx, line in enumerate(valid_lines):
        lower = line.lower()
        stripped_words = [w.strip("“”\"'()[]{}.,;:!?…-") for w in line.split() if w.strip("“”\"'()[]{}.,;:!?…-")]
        initials = [w[0].lower() for w in stripped_words if w]
        vowels = ["".join(ch for ch in w.lower() if ch in "aeiouáéíóúâêôãõà")[:1] for w in stripped_words if w]

        candidates = []

        if line.count(",") >= 2:
            candidates.append("enumeração")

        if re.search(r"\b(se|quando|embora|porque|que)\b", lower):
            candidates.append("subordinação")

        if re.search(r"\b(mas|porém|contudo|todavia)\b", lower):
            candidates.append("contraste")
        elif re.search(r"\b(e|ou)\b", lower) and "," in line:
            candidates.append("coordenação")

        if line in parallel_lines:
            candidates.append("paralelismo sintático")

        if line in anafora_lines:
            candidates.append("anáfora / repetição inicial")

        if re.search(r"\b(entre|junto-me|junto)\b", lower):
            candidates.append("encadeamento sintático")

        if idx == len(valid_lines) - 1 and re.search(r"\b(esconjuro|recuso|nego|rejeito)\b", lower):
            candidates.append("fecho de recusa")

        if re.search(r"\b(sorte|bem|feliz|fontes|verdade|ouro|áureas|medidas)\b", lower) and line.endswith("."):
            candidates.append("síntese valorativa")

        if len(stripped_words) >= 3 and len(stripped_words) <= 7 and line.endswith((".", ":", "...", "…")):
            candidates.append("síntese imagética")

        if len(initials) >= 3 and len(set(initials[: min(4, len(initials))])) == 1:
            candidates.append("aliteração")

        if len(vowels) >= 3:
            vv = [v for v in vowels if v]
            if vv and len(set(vv[: min(4, len(vv))])) == 1:
                candidates.append("assonância")

        if "?" in line:
            candidates.append("interrogação")

        if "..." in line or "…" in line:
            candidates.append("suspensão sintática")

        if not candidates:
            continue

        priority = [
            "enumeração",
            "subordinação",
            "contraste",
            "paralelismo sintático",
            "anáfora / repetição inicial",
            "encadeamento sintático",
            "fecho de recusa",
            "síntese valorativa",
            "síntese imagética",
            "aliteração",
            "assonância",
            "interrogação",
            "suspensão sintática",
            "coordenação",
        ]

        figura = next((item for item in priority if item in candidates), candidates[0])
        entries.append((idx, figura, _cia_clip(line)))

    if not entries:
        return "**requer apuração manual**"

    compressed = []
    i = 0
    while i < len(entries):
        idx, figura, trecho = entries[i]
        j = i + 1
        group = [trecho]
        while j < len(entries) and entries[j][1] == figura and entries[j][0] == entries[j-1][0] + 1:
            group.append(entries[j][2])
            j += 1

        if figura == "interrogação" and len(group) >= 3:
            joined = _cia_clip(group[0] + " … " + group[-1], limit=45)
            compressed.append(("cadeia interrogativa", joined))
        elif figura == "suspensão sintática" and len(group) >= 2:
            joined = _cia_clip(group[0] + " … " + group[-1], limit=45)
            compressed.append(("suspensão recorrente", joined))
        else:
            for trecho_item in group:
                compressed.append((figura, trecho_item))
        i = j

    seen = set()
    ordered_blocks = []
    for figura, trecho in compressed:
        key = (figura, trecho)
        if key in seen:
            continue
        seen.add(key)
        ordered_blocks.append(f"**{figura}**  \n“{trecho}”")

    return "  \n\n".join(ordered_blocks)


def build_cia_analysis_completa(curr_ypoema):
    """Leitura completa: articula entrada, núcleo, forma e fecho sem virar aula."""
    raw_parts = [part.strip() for part in curr_ypoema.replace("<br/>", "<br>").split("<br>")]
    lines = [part for part in raw_parts if part]
    poema_lines = lines[1:] if len(lines) > 1 else []

    if not poema_lines:
        return "**requer apuração manual**"

    abertura = poema_lines[0]
    fecho = poema_lines[-1]
    meio = poema_lines[len(poema_lines) // 2]
    destaque = next((line for line in poema_lines if "..." in line or "?" in line), meio)
    qtd_linhas = len(poema_lines)

    entradas = [
        f"Desde **“{_cia_clip(abertura)}”**, o poema arma um campo de leitura que não se limita ao que diz literalmente: a entrada já instala direção, tom e tensão.",
        f"Logo em **“{_cia_clip(abertura)}”**, o texto fixa um eixo de leitura. O poema não começa apenas: ele já orienta o modo como quer ser acompanhado.",
        f"Em **“{_cia_clip(abertura)}”**, a abertura do poema já pesa como gesto inaugural. O que vem depois parece nascer sob essa primeira pressão verbal.",
        f"**“{_cia_clip(abertura)}”** funciona como porta de entrada e também como decisão de percurso: o poema já se declara no modo como começa.",
    ]

    nucleos = [
        f"No corpo do texto, **“{_cia_clip(destaque)}”** concentra parte importante da sua força. É ali que linguagem, imagem ou tensão verbal se tornam mais nítidas.",
        f"Há um centro de gravidade em **“{_cia_clip(destaque)}”**. O poema parece reunir ali o seu ponto de maior densidade e, a partir dele, irradiar sentido.",
        f"Em **“{_cia_clip(destaque)}”**, o texto adensa seu movimento. O que até ali vinha sendo sugerido ganha espessura e se oferece com mais nitidez.",
        f"O núcleo do poema se deixa perceber em **“{_cia_clip(destaque)}”**: a linguagem deixa de apenas conduzir e passa a pesar mais diretamente sobre a leitura.",
    ]

    formas = [
        f"Formalmente, o poema se sustenta em **{qtd_linhas} linhas** que trabalham menos por dispersão do que por concentração. O desenho visível acompanha esse adensamento.",
        f"O andamento formal não é neutro: a distribuição das **{qtd_linhas} linhas** participa do efeito do poema e regula seu ritmo de aparição.",
        f"A forma visível do texto — suas **{qtd_linhas} linhas**, pausas e cortes — ajuda a organizar a leitura como arquitetura, não como mero suporte.",
        f"Também o desenho do poema pesa na experiência de leitura: suas **{qtd_linhas} linhas** funcionam como moldura ativa do que se concentra no texto.",
    ]

    amplificacoes = [
        "Por isso a leitura não se esgota no tema declarado. O poema vale também pelo modo como organiza pressão, intervalo, reaparição e eco.",
        "O que fica não é só o assunto, mas a forma como o poema sustenta seu próprio clima e distribui suas forças ao longo do percurso.",
        "A força do texto não está apenas no que nomeia, mas no modo como regula sua intensidade e a devolve ao leitor em camadas.",
        "O poema não depende apenas do que afirma: depende de como conduz, interrompe, reaperta e libera o seu próprio movimento.",
    ]

    fechos = [
        f"No encerramento, **“{_cia_clip(fecho)}”** recolhe esse movimento e devolve o poema com outra concentração. O fecho não apaga o resto: o reorganiza.",
        f"O fecho em **“{_cia_clip(fecho)}”** pesa porque concentra o que vinha sendo distribuído. O poema termina, mas deixa uma pressão residual trabalhando.",
        f"Em **“{_cia_clip(fecho)}”**, o texto encontra sua última forma de intensidade. O final não serve só para concluir: ele redefine o conjunto.",
        f"A linha final — **“{_cia_clip(fecho)}”** — funciona como ponto de recolhimento. É ali que o poema devolve ao leitor a sua forma mais concentrada.",
    ]

    conclusoes = [
        "A análise completa tenta acompanhar esse conjunto sem transformar o poema em explicação. O objetivo é ler sua arquitetura viva: entrada, núcleo, forma, irradiação e fecho.",
        "O que importa aqui é sustentar uma leitura mais ampla sem esmagar o poema. A completude, neste caso, vem da articulação, não do excesso.",
        "Ler de modo completo não significa dizer tudo, mas acompanhar o máximo possível do que o poema faz com seus meios.",
        "A completude desta leitura está menos no volume do comentário do que na articulação das forças que o poema realmente põe em jogo.",
    ]

    body = [
        random.choice(entradas),
        random.choice(nucleos),
        random.choice(formas),
        random.choice(amplificacoes),
        random.choice(fechos),
        build_machina_reading(poema_lines, used_lines={abertura, destaque}, avoid_fecho=True),
        random.choice(conclusoes),
    ]
    body = [b for b in body if b]
    random.shuffle(body)
    return "  \n\n".join(body)


def render_cia_stage(curr_ypoema):
    """Renderiza a análise desta leitura; na Sintática, mantém o anexo comparativo."""
    cia_offset = int(st.session_state.get("cia_line0_offset_px", 0))
    cia_font = st.session_state.get("cia_font", "Trebuchet MS")
    cia_size = int(st.session_state.get("cia_size", 18))
    mood = st.session_state.get("cia_mood", CIA_MOODS[0])

    def _to_html_block(markdown_text):
        html = markdown_text
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
    st.markdown(f"**{build_cia_stage_title()}**")
    st.markdown("&nbsp;", unsafe_allow_html=True)

    if mood == "Sintática":
        analysis_html = _to_html_block(build_cia_analysis(curr_ypoema))
        analysis_free_html = _to_html_block(build_cia_analysis_free(curr_ypoema))
        content = f"""{analysis_html}
            <div class='cia-stage-sep'><strong>Análise da análise</strong></div>
            {analysis_free_html}"""
    elif mood == "Sintética":
        content = _to_html_block(build_cia_analysis_sintetica(curr_ypoema))
    elif mood == "Resumida":
        content = _to_html_block(build_cia_analysis_resumida(curr_ypoema))
    elif mood == "Completa":
        content = _to_html_block(build_cia_analysis_completa(curr_ypoema))
    else:
        content = _to_html_block("Este mood ainda não entrou em operação.")

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
    """Centro de Controle da Chave, exclusivo de yPoemas."""
    current_mood = st.session_state.get("cia_mood", CIA_MOODS[0])
    if current_mood not in CIA_MOODS:
        current_mood = CIA_MOODS[0]
        st.session_state.cia_mood = current_mood

    rows = [(0, 1), (2, 3)]
    for left_idx, right_idx in rows:
        col_left, col_right = st.sidebar.columns(2)
        with col_left:
            if st.button(CIA_MOODS[left_idx], key=f"cia_mood_btn_{left_idx}", use_container_width=True):
                st.session_state.cia_mood = CIA_MOODS[left_idx]
        with col_right:
            if st.button(CIA_MOODS[right_idx], key=f"cia_mood_btn_{right_idx}", use_container_width=True):
                st.session_state.cia_mood = CIA_MOODS[right_idx]


def draw_sidebar_panel_buttons(chosen_id, show_icons_callback=None):
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

    if show_icons_callback and st.session_state.get("sidebar_panel", "Machina") == "Machina":
        show_icons_callback()


__all__ = [
    "CIA_MOODS",
    "render_cia_stage",
    "render_cia_sidebar",
    "draw_sidebar_panel_buttons",
]
