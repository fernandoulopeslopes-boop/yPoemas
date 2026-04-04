def main():
    # 1. SETUP DE SESSÃO & IDENTIDADE
    # (Garante que IPAddres e estados iniciais estejam prontos)
    init_session() 

    # 2. CABEÇALHO DE CONTROLE (O PAINEL ÚNICO)
    # Criamos uma linha horizontal simétrica acima de tudo
    # Sequência: more / last / rand / nest / help / love
    f1, b_more, b_last, b_rand, b_nest, b_help, b_love, f2 = st.columns([2, 1, 1, 1, 1, 1, 1, 2])
    
    help_tips = load_help(st.session_state.lang)

    with b_more:
        # ✚ - Informações extras / Eureka detail
        btn_more = st.button("✚", help=help_tips[4])
    with b_last:
        # ◀ - Voltar tema / Voltar página
        btn_last = st.button("◀", help=help_tips[0])
    with b_rand:
        # ✻ - Sorteio universal
        btn_rand = st.button("✻", help=help_tips[1])
    with b_nest:
        # ▶ - Avançar tema / Próxima página
        btn_nest = st.button("▶", help=help_tips[2])
    with b_help:
        # ? - Manual contextual (.md)
        btn_help = st.button("?", help="help !!!")
    with b_love:
        # ❤ - Lista de leituras (Views)
        btn_love = st.button("❤", help=help_tips[3])

    st.divider() # Uma linha sutil para separar o comando da navegação

    # 3. NAVEGAÇÃO DE CONTEXTO (TAB BAR)
    # Fica logo abaixo dos botões, definindo a "estrada"
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="mini", description=""),
        stx.TabBarItemData(id=2, title="yPoemas", description=""),
        stx.TabBarItemData(id=3, title="eureka", description=""),
        stx.TabBarItemData(id=4, title="off-machina", description=""),
        stx.TabBarItemData(id=5, title="books", description=""),
        stx.TabBarItemData(id=6, title="poly", description=""),
        stx.TabBarItemData(id=7, title="about", description=""),
    ], default=2)

    # 4. TRATAMENTO DAS EXCEÇÕES & LOGA DE ESTADO
    # Aqui, os cliques nos botões do topo alimentam as variáveis de estado
    # que as páginas usarão. Ex: btn_rand no topo altera st.session_state.take
    handle_global_logic(btn_more, btn_last, btn_rand, btn_nest, btn_help, btn_love)

    # 5. O PALCO (CONTEÚDO)
    # Renderiza apenas a arte, sem botões internos de navegação
    render_palco(chosen_id)
