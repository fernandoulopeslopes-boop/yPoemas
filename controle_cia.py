# controle_cia.py
# -----------------------------------------------------------------------------
# CIA — Câmara / Central de Inteligência Analítica
#
# Módulo separado do ypo_seguro.py para manter a Machina em seu quadrado:
# o ypo_seguro.py cuida do motor/palco; este arquivo cuida da presença,
# estado, sidebar e leitura da CIA.
# -----------------------------------------------------------------------------

import html
import re
import streamlit as st


_CB = {
    "translate": lambda texto: texto,
    "write_ypoema": None,
    "current_book": None,
    "say_number": None,
    "render_sidebar_for_page": None,
}


SIDEBAR_FILHOTE_WIDTH_PX = 64

CIA_MOOD_OPTIONS = [
    "Sintática",
    "Sintética",
    "Formal",
    "Completa",
    "Index",
]


def configure_cia(
    translate_func=None,
    load_typo_func=None,
    write_ypoema_func=None,
    ip_address=None,
    current_book_func=None,
    say_number_func=None,
    render_sidebar_for_page_func=None,
):
    """Recebe pequenos ganchos da Machina sem trazer a Machina para dentro da CIA."""
    if translate_func is not None:
        _CB["translate"] = translate_func
    if write_ypoema_func is not None:
        _CB["write_ypoema"] = write_ypoema_func
    if current_book_func is not None:
        _CB["current_book"] = current_book_func
    if say_number_func is not None:
        _CB["say_number"] = say_number_func
    if render_sidebar_for_page_func is not None:
        _CB["render_sidebar_for_page"] = render_sidebar_for_page_func

    _apply_cia_styles()


def _translate(texto):
    return _CB.get("translate", lambda x: x)(texto)


def _current_book():
    fn = _CB.get("current_book")
    if callable(fn):
        return fn()
    return st.session_state.get("book", "")


def _say_number(tema):
    fn = _CB.get("say_number")
    if callable(fn):
        return fn(tema)
    return "índice indisponível para este tema."


def _apply_cia_styles():
    """CSS da CIA fica no módulo da CIA, não no corpo da Machina."""
    st.markdown(
        """
        <style>
        .cia-stage-box {
            background: rgba(255, 255, 255, 0.58);
            border-radius: 16px;
            padding: 0.25rem 0.55rem 0.35rem 0.55rem;
            min-height: 1.4;
            box-sizing: border-box;
            overflow-x: hidden;
        }

        .cia-stage-body {
            line-height: 1.35;
        }

        .cia-stage-box .container {
            justify-content: center !important;
            text-align: center !important;
        }

        .cia-stage-box .logo-text {
            width: 100% !important;
            text-align: center !important;
            padding-left: 0 !important;
        }

        .cia-header-container {
            width: 100% !important;
            text-align: center !important;
            display: block !important;
        }

        .cia-header-text {
            width: 100% !important;
            text-align: center !important;
            padding-left: 0 !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        .cia-stage-title {
            text-align: center;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
            opacity: 0.88;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def guia_do_leitor_cia():
    """Guia curto do leitor para o modo CIA."""
    return """
### Guia do leitor da CIA

A **CIA** não substitui a leitura do leitor.  
Ela oferece lentes diferentes para observar o mesmo yPoema.

A regra principal é simples:

**mesmo yPoema → várias leituras → uma análise completa a outra**

Ao trocar o tipo de análise, o texto analisado permanece o mesmo.  
O que muda é a lente crítica.

**Sintática**  
Observa engrenagens da frase: forma verbal, sujeito, oração, pontuação, cortes e articulações internas.

**Sintética**  
Procura a tensão principal do yPoema, sem tentar explicar tudo.

**Formal**  
Lê o desenho visível: linhas, blocos, pausas, recorrências e arquitetura do texto.

**Completa**  
Amplia a leitura em camadas: imagem, forma, ritmo, tensão e fecho.

A comparação entre as análises é parte da experiência.  
Nenhuma lente encerra o poema; cada uma abre outro modo de entrada.
"""


def limpar_cia_palco():
    """A CIA nunca deixa rastros no palco da Machina."""
    for key, value in {
        "ypoema_atual_para_analise": "",
        "tema_atual_para_analise": "",
        "book_atual_para_analise": "",
        "take_atual_para_analise": -1,
        "lang_atual_para_analise": "",
        "ypoema_em_analise": "",
        "tema_em_analise": "",
        "book_em_analise": "",
        "take_em_analise": -1,
        "lang_em_analise": "",
        "cia_mood_changed": False,
        "cia_force_new_poema": False,
        "cia_freeze_book": "",
        "cia_freeze_take": -1,
        "cia_freeze_tema": "",
        "cia_last_action": "",
        "cia_reading_mode": False,
    }.items():
        st.session_state[key] = value


def _limpar_copias_palco():
    """Cópias pertencem ao tema que as gerou; ao entrar na CIA, somem do palco."""
    st.session_state["copy_bundle_text"] = ""
    st.session_state["copy_bundle_qtd"] = 0
    st.session_state["copy_bundle_token"] = 0


def _cia_objeto_analise_existe():
    """Objeto explícito de leitura da CIA: mesmo yPoema, várias lentes."""
    return bool(st.session_state.get("ypoema_atual_para_analise", ""))


def _cia_fixar_objeto_analise(curr_ypoema):
    """Fixa livro/take/tema/yPoema como objeto atual da análise."""
    st.session_state["book_atual_para_analise"] = _current_book()
    st.session_state["take_atual_para_analise"] = int(st.session_state.get("take", 0))
    st.session_state["tema_atual_para_analise"] = st.session_state.get("tema", "")
    st.session_state["ypoema_atual_para_analise"] = curr_ypoema
    st.session_state["lang_atual_para_analise"] = st.session_state.get("lang", "pt")

    # Compatibilidade com a camada anterior.
    st.session_state.ypoema_em_analise = curr_ypoema
    st.session_state.tema_em_analise = st.session_state.get("tema", "")
    st.session_state.book_em_analise = _current_book()
    st.session_state.take_em_analise = int(st.session_state.get("take", 0))
    st.session_state.lang_em_analise = st.session_state.get("lang", "pt")


def _cia_restaurar_identidade_objeto():
    """Recoloca o estado canônico no objeto que está sendo analisado."""
    if not _cia_objeto_analise_existe():
        return

    book = st.session_state.get("book_atual_para_analise", "")
    take = st.session_state.get("take_atual_para_analise", -1)
    tema = st.session_state.get("tema_atual_para_analise", "")

    if book:
        st.session_state.book = book

    try:
        take = int(take)
    except Exception:
        take = -1

    if take >= 0:
        st.session_state.take = take

    if tema:
        st.session_state.tema = tema


def _restore_cia_freeze_before_sync():
    """Troca de análise CIA não pode alterar livro/tema/take por gatilho lateral."""
    if not st.session_state.get("cia_mood_changed", False):
        return

    # Preferir o objeto explícito já fixado pela CIA.
    if _cia_objeto_analise_existe():
        _cia_restaurar_identidade_objeto()
        return

    frozen_book = st.session_state.get("cia_freeze_book", "")
    frozen_take = st.session_state.get("cia_freeze_take", -1)
    frozen_tema = st.session_state.get("cia_freeze_tema", "")

    if frozen_book:
        st.session_state.book = frozen_book

    if isinstance(frozen_take, int) and frozen_take >= 0:
        st.session_state.take = frozen_take

    if frozen_tema:
        st.session_state.tema = frozen_tema


def _limpar_html_texto(texto):
    texto = str(texto or "")
    texto = re.sub(r"<br\s*/?>", "\n", texto, flags=re.I)
    texto = re.sub(r"<[^>]+>", "", texto)
    texto = html.unescape(texto)
    return texto.strip()


def _linhas_ypoema(texto):
    return [ln.strip() for ln in _limpar_html_texto(texto).splitlines() if ln.strip()]


def _cia_analise_real_time(curr_ypoema, mood):
    """Leitura local, enxuta e em tempo real do yPoema visível."""
    linhas = _linhas_ypoema(curr_ypoema)
    tema = st.session_state.get("tema", "")

    if not linhas:
        return "A CIA não encontrou texto no palco para analisar."

    primeira = linhas[0]
    ultima = linhas[-1]
    interrogacoes = sum(ln.count("?") for ln in linhas)
    exclamacoes = sum(ln.count("!") for ln in linhas)
    reticencias = sum(ln.count("...") + ln.count("…") for ln in linhas)

    mood_norm = str(mood or "Sintática").lower()

    if mood_norm == "index":
        try:
            idx = _say_number(tema)
        except Exception:
            idx = "índice indisponível para este tema."
        return (
            f"Tema em foco: {tema}.\n\n"
            f"Linhas visíveis: {len(linhas)}.\n\n"
            f"INDEX: {idx}"
        )

    if mood_norm.startswith("sint") and "tica" in mood_norm:
        partes = [
            f"A leitura sintática observa o yPoema visível em {len(linhas)} linha(s).",
            f"A abertura fixa o primeiro enquadramento em: “{primeira}”.",
        ]
        if len(linhas) > 2:
            partes.append("O miolo sustenta a passagem entre a primeira imagem e o fecho, sem precisar explicar todo o percurso.")
        partes.append(f"O fecho concentra a última tensão em: “{ultima}”.")
        if interrogacoes:
            partes.append("A pergunta desloca a conclusão e mantém a leitura em suspensão.")
        if exclamacoes:
            partes.append("A exclamação aumenta a pressão da frase sem transformar a leitura em sentença.")
        if reticencias:
            partes.append("As reticências deixam uma sobra de sentido para o leitor completar.")
        return "\n\n".join(partes)

    if mood_norm.startswith("formal"):
        return "\n\n".join([
            f"Formalmente, o yPoema se organiza em {len(linhas)} linha(s).",
            "O desenho visível importa: cortes, pausas e distribuição das linhas orientam o ritmo antes mesmo da interpretação.",
            "A leitura deve considerar a arquitetura do texto no palco, não um tema abstrato fora dele.",
            f"O último bloco deixa o foco em: “{ultima}”.",
        ])

    if mood_norm.startswith("completa"):
        return "\n\n".join([
            f"Esta leitura parte do yPoema exibido agora, no tema {tema}.",
            f"A abertura apresenta o primeiro gesto: “{primeira}”.",
            "A forma conduz a atenção por aproximações sucessivas: imagem, pausa, deslocamento e retomada.",
            f"O fecho — “{ultima}” — não encerra definitivamente o poema; apenas mostra um modo de saída.",
            "A palavra final permanece sendo do leitor.",
        ])

    # Sintética
    return "\n\n".join([
        "A leitura sintética procura apenas a tensão principal do yPoema visível.",
        f"Entre a abertura “{primeira}” e o fecho “{ultima}”, o texto cria uma pequena travessia de sentido.",
        "O poema ganha força porque não precisa explicar tudo: mostra o suficiente para que o leitor complete o restante.",
    ])


def render_cia_stage(curr_ypoema):
    """Palco da CIA: presença, sub-header e análise em tempo real."""
    mood = st.session_state.get("cia_mood", "Sintática")

    write_header = _CB.get("write_ypoema")
    if callable(write_header):
        write_header("Central de Inteligência Analítica", None)
    else:
        st.markdown("### Central de Inteligência Analítica")

    analise = _cia_analise_real_time(curr_ypoema, mood)
    cia_font = st.session_state.get("cia_font", "Trebuchet MS")
    cia_size = int(st.session_state.get("cia_size", 18))
    texto_html = html.escape(analise).replace("\n", "<br>")

    st.markdown(
        f"""
        <div class='cia-real-time-stage' style="font-family:{cia_font}; font-size:{cia_size}px; line-height:1.55; text-align:left; margin:0 auto; max-width:42rem;">
            {texto_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def draw_sidebar_panel_buttons(chosen_id):
    """Botões de presença no palco: Machina / CIA."""
    if str(chosen_id) != "2":
        return

    with st.sidebar:
        cols = st.columns(2)

        if cols[0].button("Machina", key="sidebar_panel_machina", use_container_width=True):
            st.session_state["sidebar_panel"] = "Machina"
            limpar_cia_palco()

        if cols[1].button("CIA", key="sidebar_panel_cia", use_container_width=True):
            st.session_state["sidebar_panel"] = "CIA"
            _limpar_copias_palco()


def render_cia_mood_selectbox():
    """Lista da CIA sempre aberta: troca só a camada de análise."""
    current = st.session_state.get("cia_mood", "Sintática").strip()

    if current == "Reduzida":
        current = "Sintética"
        st.session_state["cia_mood"] = current
        st.session_state["cia_mood_select"] = current

    if current not in CIA_MOOD_OPTIONS:
        current = "Sintática"
        st.session_state["cia_mood"] = current
        st.session_state["cia_mood_select"] = current

    with st.sidebar.expander("↓  análises CIA", expanded=True):
        for mood in CIA_MOOD_OPTIONS:
            label = f"• {mood}" if mood == current else mood

            if st.button(label, key=f"cia_mood_list_{mood}", use_container_width=True):
                if mood != st.session_state.get("cia_mood", "Sintática"):
                    if _cia_objeto_analise_existe():
                        st.session_state["cia_freeze_book"] = st.session_state.get("book_atual_para_analise", "")
                        st.session_state["cia_freeze_take"] = int(st.session_state.get("take_atual_para_analise", -1))
                        st.session_state["cia_freeze_tema"] = st.session_state.get("tema_atual_para_analise", "")
                    else:
                        st.session_state["cia_freeze_book"] = st.session_state.get("book", "")
                        st.session_state["cia_freeze_take"] = int(st.session_state.get("take", -1))
                        st.session_state["cia_freeze_tema"] = st.session_state.get("tema", "")

                    st.session_state["cia_mood"] = mood
                    st.session_state["cia_mood_select"] = mood
                    st.session_state["cia_reading_mode"] = False
                    st.session_state["cia_last_action"] = "cia_mood"
                    st.session_state["cia_mood_changed"] = True


def _cia_sidebar_filha_active(chosen_id):
    """Mantém a sidebar CIA fixa; não recolhe para a coluna reduzida."""
    if str(chosen_id) != "2":
        st.session_state["sidebar_panel"] = "Machina"
        st.session_state["cia_reading_mode"] = False
    return False


def apply_sidebar_mae_filha_styles(chosen_id):
    """Alterna a largura visual da sidebar entre mãe e filha."""
    if _cia_sidebar_filha_active(chosen_id):
        width = SIDEBAR_FILHOTE_WIDTH_PX
        st.markdown(
            f"""
            <style>
            [data-testid='stSidebar'][aria-expanded='true'],
            section[data-testid='stSidebar'][aria-expanded='true'] {{
                width: {width}px !important;
                min-width: {width}px !important;
                max-width: {width}px !important;
            }}

            [data-testid='stSidebar'][aria-expanded='true'] > div:first-child,
            section[data-testid='stSidebar'][aria-expanded='true'] > div:first-child {{
                width: {width}px !important;
                min-width: {width}px !important;
                max-width: {width}px !important;
                padding-left: 0.20rem !important;
                padding-right: 0.20rem !important;
                overflow-x: hidden !important;
            }}

            [data-testid='stSidebar'] div[data-testid='stSidebarContent'] {{
                padding-left: 0.20rem !important;
                padding-right: 0.20rem !important;
            }}

            [data-testid='stSidebar'] .stButton button {{
                min-width: 100% !important;
                min-height: 3.0rem !important;
                font-size: 1.85rem !important;
                line-height: 1 !important;
                padding: 0 !important;
                border-radius: 14px !important;
            }}

            .machina-sidebar-filha-spacer {{
                height: 42vh;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
            [data-testid='stSidebar'][aria-expanded='true'],
            section[data-testid='stSidebar'][aria-expanded='true'] {
                width: 300px !important;
                min-width: 300px !important;
                max-width: 300px !important;
            }

            [data-testid='stSidebar'][aria-expanded='true'] > div:first-child,
            section[data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
                width: 300px !important;
                min-width: 300px !important;
                max-width: 300px !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


def render_sidebar_filha():
    """Compatibilidade: sidebar-filha desativada; a CIA permanece fixa."""
    st.session_state["sidebar_panel"] = "CIA"
    st.session_state["cia_reading_mode"] = False

    render_sidebar = _CB.get("render_sidebar_for_page")
    if callable(render_sidebar):
        render_sidebar("2")

    with st.sidebar:
        render_cia_mood_selectbox()
