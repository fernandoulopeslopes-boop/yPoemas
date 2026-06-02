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
    if fallback:
        used_lines.add(fallback)
        return fallback
    for line in candidates:
        if line:
            used_lines.add(line)
            return line
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


def _cia_critico_abertura(poema_lines, used_lines):
    """Primeiro bloco fixo: cria eixo de leitura sem virar fórmula."""
    abertura = _cia_pick_unused([poema_lines[0]], used_lines, poema_lines[0])
    return random.choice([
        f"Desde **“{_cia_clip(abertura)}”**, o poema estabelece um campo de tensão que orienta a leitura sem entregar tudo de saída.",
        f"A entrada em **“{_cia_clip(abertura)}”** já define um modo de aproximação: o poema começa como gesto, não apenas como enunciado.",
        f"Logo em **“{_cia_clip(abertura)}”**, o texto escolhe seu passo e prepara a pressão que irá circular pelos versos.",
        f"**“{_cia_clip(abertura)}”** funciona como porta de entrada do poema: abre o percurso e já deixa uma tensão em suspensão.",
    ])


def _cia_critico_fecho(poema_lines, used_lines, prefer_specific=True):
    """Último bloco fixo: recolhe a leitura sem fechar o poema."""
    fecho = poema_lines[-1]
    if prefer_specific and fecho not in used_lines:
        used_lines.add(fecho)
        return random.choice([
            f"No fecho, **“{_cia_clip(fecho)}”** recolhe o percurso sem esgotá-lo; a última linha concentra a pressão e deixa o poema ainda reverberando.",
            f"A chegada a **“{_cia_clip(fecho)}”** dá ao poema seu ponto de recolhimento: não fecha o sentido, mas organiza o eco do que veio antes.",
            f"Em **“{_cia_clip(fecho)}”**, o poema encontra uma saída que ainda preserva atrito. O fim recolhe a leitura sem transformar a tensão em resposta única.",
            f"O verso final — **“{_cia_clip(fecho)}”** — funciona como mar da leitura: para ali converge o percurso, mas o texto continua vibrando depois da chegada.",
        ])
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
    if len(chosen) < min_count:
        for item in shuffled:
            if item in chosen:
                continue
            item_lines = set(item.get("lines", []))
            # repetição só como último recurso, quando há pouco material no poema
            chosen.append(item)
            used_lines.update(item_lines)
            if len(chosen) >= min_count:
                break
    return chosen


def build_cia_analysis(curr_ypoema):
    """Leitura sintática com fluxo fixo: abertura, desenvolvimento e fecho."""
    poema_lines = _cia_poema_lines(curr_ypoema)
    tema = st.session_state.get("tema", "")

    if not poema_lines:
        st.session_state["_cia_used_lines"] = []
        return "**requer apuração manual**"

    candidates = []

    def add(lines_used, text):
        cleaned = [line for line in lines_used if line]
        candidates.append({"lines": cleaned, "text": text})

    perguntas = [line for line in poema_lines if "?" in line]
    if perguntas:
        line = perguntas[0]
        add([line],
            f"Em **“{_cia_clip(line)}”** a interrogação não funciona como simples pergunta: ela instala uma zona de instabilidade e obriga o poema a respirar pelo intervalo da dúvida."
        )

    reticencias = [line for line in poema_lines if "..." in line or "…" in line]
    if reticencias:
        line = reticencias[0]
        add([line],
            f"As reticências de **“{_cia_clip(line)}”** suspendem o fechamento e deixam a frase continuar fora da linha, como se o sentido ainda estivesse procurando onde pousar."
        )

    incisos = [line for line in poema_lines if "(" in line or ")" in line]
    if incisos:
        line = incisos[0]
        add([line],
            f"O inciso em **“{_cia_clip(line)}”** cria uma dobra interna: o verso se desvia por um instante e volta ao poema com outra respiração."
        )

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
        add(exemplos,
            f"O paralelismo entre **“{_cia_clip(exemplos[0])}”** e **“{_cia_clip(exemplos[1])}”** dá cadência ao poema: a estrutura retorna, mas não repete simplesmente a mesma intensidade."
        )
    elif anafora_key:
        exemplos = first_tokens[anafora_key][:2]
        add(exemplos,
            f"A repetição inicial em **“{_cia_clip(exemplos[0])}”** e **“{_cia_clip(exemplos[1])}”** cria anáfora. O retorno do mesmo arranque firma um eixo verbal para o percurso."
        )

    enumeracoes = [line for line in poema_lines if line.count(",") >= 2]
    if enumeracoes:
        line = enumeracoes[0]
        add([line],
            f"A enumeração em **“{_cia_clip(line)}”** trabalha por acúmulo. O verso não se limita a listar: ele engrossa o campo de forças do poema."
        )

    subordinadas = [line for line in poema_lines if re.search(r"\b(se|quando|embora|porque|que)\b", line.lower())]
    coordenadas = [line for line in poema_lines if re.search(r"\b(e|ou|mas)\b", line.lower()) and "," in line]

    if subordinadas:
        line = subordinadas[0]
        add([line],
            f"Em **“{_cia_clip(line)}”**, a subordinação cria dependência interna: a frase avança por condição, tempo ou explicação, e não por simples sequência."
        )
    elif coordenadas:
        line = coordenadas[0]
        add([line],
            f"A coordenação em **“{_cia_clip(line)}”** aproxima segmentos sem fundi-los por completo. O verso ganha soma, contraste ou desvio lateral."
        )

    cortes = []
    for i, line in enumerate(poema_lines[:-1]):
        nxt = poema_lines[i + 1]
        if line and line[-1] not in ".?!:;…)" and (nxt[:1].islower() or len(line.split()) <= 4):
            cortes.append((line, nxt))
    if cortes:
        l1, l2 = cortes[0]
        add([l1, l2],
            f"No corte entre **“{_cia_clip(l1)}”** e **“{_cia_clip(l2)}”**, a sintaxe atravessa a linha. A leitura é empurrada para diante antes de encontrar repouso."
        )

    used_lines = set()
    abertura = _cia_critico_abertura(poema_lines, used_lines)

    if candidates:
        max_figures = min(4, len(candidates))
        min_figures = min(2, len(candidates))
        target_count = max_figures if max_figures <= 2 else random.randint(min_figures, max_figures)
        chosen = _cia_filter_candidates(candidates, used_lines, target_count, min_figures)
        desenvolvimento = [item["text"] for item in chosen]
    else:
        desenvolvimento = [random.choice([
            "A construção verbal do poema trabalha menos por explicação do que por pressão acumulada: cada linha desloca um pouco o eixo da leitura.",
            "Mesmo sem uma figura dominante imediatamente nomeável, o poema sustenta seu efeito pela distribuição de cortes, pausas e retomadas.",
            "A sintaxe opera como corrente subterrânea: o sentido avança por pequenas tensões, não por declaração direta.",
        ])]

    fecho = _cia_critico_fecho(poema_lines, used_lines, prefer_specific=True)

    st.session_state.tema_last_analise = tema
    st.session_state["_cia_used_lines"] = list(used_lines)
    return _cia_join([abertura] + desenvolvimento + [fecho])


def build_cia_analysis_free(curr_ypoema):
    """Outro ângulo: leitura de contraste, sem mencionar método e sem repetir trechos por comodidade."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "Sem texto em foco para leitura."

    used = set(st.session_state.get("_cia_used_lines", []))
    local_used = set(used)

    abertura_line = _cia_pick_unused([poema_lines[0]], local_used, poema_lines[0])
    destaque_line = _cia_pick_unused(_cia_destaques(poema_lines), local_used, poema_lines[len(poema_lines) // 2])
    fecho_line = _cia_pick_unused([poema_lines[-1]], local_used, poema_lines[-1])

    abertura = random.choice([
        f"Outro ângulo surge já em **“{_cia_clip(abertura_line)}”**: o verso não apenas inicia o texto, mas define uma temperatura de leitura.",
        f"Por outro caminho, **“{_cia_clip(abertura_line)}”** abre uma zona de expectativa. O poema começa antes de se explicar.",
        f"Há uma entrada discreta, mas decisiva, em **“{_cia_clip(abertura_line)}”**: dali o texto já escolhe o seu modo de respirar.",
    ])

    desenvolvimento = random.choice([
        f"No corpo do poema, **“{_cia_clip(destaque_line)}”** concentra uma energia própria. A formulação desloca a linguagem do uso comum e cria densidade.",
        f"O ponto de maior pressão aparece em **“{_cia_clip(destaque_line)}”**. O verso não apenas comunica: cria uma zona de sentido ao redor de si.",
        f"Em **“{_cia_clip(destaque_line)}”**, a linguagem ganha espessura. Há ali uma pequena torção que impede a leitura de seguir por caminho óbvio.",
    ])

    if fecho_line in {abertura_line, destaque_line} and len(poema_lines) > 2:
        fecho = random.choice([
            "O encerramento recolhe essa tensão sem resolver tudo. O poema termina preservando uma zona de eco.",
            "Ao final, a leitura não encontra uma explicação única, mas um resto de intensidade que continua trabalhando.",
            "O fim não domestica o percurso: apenas concentra sua última reverberação.",
        ])
    else:
        fecho = random.choice([
            f"No encerramento, **“{_cia_clip(fecho_line)}”** recolhe a tensão anterior e devolve o poema com outro peso.",
            f"A chegada a **“{_cia_clip(fecho_line)}”** desloca retrospectivamente o que veio antes e deixa o texto em estado de eco.",
            f"Quando chega a **“{_cia_clip(fecho_line)}”**, o poema muda de temperatura e conserva uma pressão residual depois do fim.",
        ])

    return _cia_join([abertura, desenvolvimento, fecho])


def build_cia_analysis_sintetica(curr_ypoema):
    """Sintética: núcleo de tensão com atmosfera, sem virar resumo banal."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "**requer apuração manual**"

    used_lines = set()
    abertura_line = _cia_pick_unused([poema_lines[0]], used_lines, poema_lines[0])
    destaque_line = _cia_pick_unused(_cia_destaques(poema_lines), used_lines, poema_lines[len(poema_lines) // 2])

    abertura = random.choice([
        f"Desde **“{_cia_clip(abertura_line)}”**, o poema se apresenta como concentração: pouco se espalha, muito se adensa.",
        f"A entrada em **“{_cia_clip(abertura_line)}”** já arma o núcleo do texto, com uma pressão que prefere sugerir a explicar.",
        f"Em **“{_cia_clip(abertura_line)}”**, o poema encontra seu primeiro eixo e começa a trabalhar por condensação.",
    ])

    desenvolvimento = random.choice([
        f"O centro de força passa por **“{_cia_clip(destaque_line)}”**. A formulação concentra imagem, tensão e atmosfera sem dissolver o mistério.",
        f"Em **“{_cia_clip(destaque_line)}”**, a linguagem ganha densidade: o verso parece reunir o que o poema tem de mais vivo.",
        f"Há em **“{_cia_clip(destaque_line)}”** uma medula verbal. O poema se mostra breve na superfície e mais largo por dentro.",
    ])

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
            f"A recorrência inicial de **“{_cia_clip(repetido)}”** atua como marca de coesão. O poema ganha reconhecimento pelo retorno, não por simples repetição.",
            f"O retorno de **“{_cia_clip(repetido)}”** no começo de versos cria uma coluna interna: a forma passa a insistir antes mesmo do argumento.",
            f"Quando **“{_cia_clip(repetido)}”** reaparece em posição inicial, o poema firma uma pequena ossatura de repetição e reconhecimento.",
        ]))

    if reticencias or perguntas:
        mark = reticencias[0] if reticencias else perguntas[0]
        desenvolvimento.append(random.choice([
            f"A pontuação em **“{_cia_clip(mark)}”** interfere no desenho do tempo: o verso não apenas diz, ele regula a demora da leitura.",
            f"Em **“{_cia_clip(mark)}”**, a pontuação vira gesto formal. Ela cria pausa, suspensão ou pressão dentro da superfície do poema.",
            f"O sinal gráfico em **“{_cia_clip(mark)}”** participa da arquitetura: muda o modo como o verso se oferece ao olhar e à escuta.",
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
    abertura_line = _cia_pick_unused([poema_lines[0]], used_lines, poema_lines[0])
    destaque_line = _cia_pick_unused(_cia_destaques(poema_lines), used_lines, poema_lines[len(poema_lines) // 2])

    abertura = random.choice([
        f"O percurso se abre em **“{_cia_clip(abertura_line)}”** e já define o eixo mínimo da leitura.",
        f"A entrada em **“{_cia_clip(abertura_line)}”** fixa o primeiro movimento do poema.",
        f"Logo em **“{_cia_clip(abertura_line)}”**, o texto indica sua direção principal.",
    ])

    desenvolvimento = random.choice([
        f"O ponto de maior concentração aparece em **“{_cia_clip(destaque_line)}”**: ali o poema reúne sua tensão mais visível.",
        f"Em **“{_cia_clip(destaque_line)}”**, a leitura encontra o núcleo mais direto do texto.",
        f"**“{_cia_clip(destaque_line)}”** resume a pressão central sem esgotar o poema.",
    ])

    fecho = _cia_critico_fecho(poema_lines, used_lines, prefer_specific=True)
    return _cia_join([abertura, desenvolvimento, fecho])

def build_cia_analysis_completa(curr_ypoema):
    """Completa: cartografia articulada com abertura, desenvolvimento e fecho fixos."""
    poema_lines = _cia_poema_lines(curr_ypoema)

    if not poema_lines:
        return "**requer apuração manual**"

    used_lines = set()
    qtd_linhas = len(poema_lines)
    abertura_line = _cia_pick_unused([poema_lines[0]], used_lines, poema_lines[0])
    destaque_line = _cia_pick_unused(_cia_destaques(poema_lines), used_lines, poema_lines[len(poema_lines) // 2])

    abertura = random.choice([
        f"Desde **“{_cia_clip(abertura_line)}”**, o poema arma um campo de leitura que não se limita ao enunciado: a entrada instala direção, tom e tensão.",
        f"Logo em **“{_cia_clip(abertura_line)}”**, o texto fixa um eixo. O começo já orienta o modo como o poema quer ser acompanhado.",
        f"Em **“{_cia_clip(abertura_line)}”**, a abertura pesa como gesto inaugural; o que vem depois parece nascer sob essa primeira pressão verbal.",
    ])

    nucleo = random.choice([
        f"No corpo do texto, **“{_cia_clip(destaque_line)}”** concentra parte decisiva da força verbal. A imagem ou tensão ali ganha espessura.",
        f"Há um centro de gravidade em **“{_cia_clip(destaque_line)}”**. O poema reúne ali uma de suas zonas de maior densidade.",
        f"Em **“{_cia_clip(destaque_line)}”**, o texto adensa seu movimento: a linguagem deixa de apenas conduzir e passa a pesar mais diretamente.",
    ])

    forma = random.choice([
        f"A distribuição em **{qtd_linhas} linhas** participa do efeito do poema: pausas e cortes regulam o ritmo de aparição do sentido.",
        f"O desenho visível do texto — suas **{qtd_linhas} linhas**, pausas e quebras — atua como arquitetura, não como suporte neutro.",
        f"Também a forma pesa: as **{qtd_linhas} linhas** organizam o fôlego e modulam a intensidade do percurso.",
    ])

    ampliacao = random.choice([
        "O poema vale não só pelo que nomeia, mas pelo modo como organiza pressão, intervalo, reaparição e eco.",
        "A força do texto está no modo como regula sua intensidade e a devolve ao leitor em camadas.",
        "O texto conduz, interrompe, reaperta e libera o próprio movimento sem reduzir-se a uma explicação única.",
    ])

    meio = [nucleo, forma, ampliacao]
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
