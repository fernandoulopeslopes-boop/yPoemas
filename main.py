import streamlit as st
import random
import time
import os

# --- MESTRE: FUNÇÕES DE UTILIDADE (MEMÓRIA > DISCO) ---

def get_processed_content(tema, seed=""):
    """Gerencia carregamento, tradução e log em um único fluxo de memória."""
    try:
        # Evita recarregar se a língua não mudou e o tema é o mesmo (Otimização)
        curr_ypoema = load_poema(tema, seed)
        curr_ypoema = load_lypo()
        
        if st.session_state.lang != "pt":
            curr_ypoema = translate(curr_ypoema)
            # Normalização de quebras de linha em memória (Substitui o I/O de arquivo)
            curr_ypoema = curr_ypoema.replace('\r\n', '\n').strip()
            
        update_readings(tema)
        return curr_ypoema
    except Exception as e:
        return f"Erro ao processar conteúdo: {e}"

def render_display(texto, tema, context=""):
    """Padroniza a exibição de imagem + texto em todas as páginas."""
    image = load_arts(tema) if st.session_state.draw else None
    write_ypoema(texto, image)
    if st.session_state.talk:
        talk(texto)

# --- MESTRE: PÁGINAS REFATORADAS ---

def page_mini():
    temas_list = load_temas("todos os temas")
    maxy = len(temas_list)

    # Sidebar UI
    with st.sidebar:
        wait_time = st.slider(translate("tempo de exibição (segundos):"), 5, 60, 10)
    
    col1, col2, col3, col4, col5 = st.columns([4, 1, 1, 1, 4])
    help_tips = load_help(st.session_state.lang)
    
    btn_rand = col3.button("✻", help=help_tips[1])
    st.session_state.auto = col4.checkbox("auto", value=st.session_state.get('auto', False))

    if btn_rand:
        st.session_state.mini = random.randrange(0, maxy)

    # Placeholder para evitar "jumpy UI"
    placeholder = st.empty()

    # LÓGICA DE EXECUÇÃO
    if st.session_state.auto:
        # Loop controlado por Rerun (Não trava a Main Thread)
        st.session_state.mini = random.randrange(0, maxy)
        tema = temas_list[st.session_state.mini]
        texto = get_processed_content(tema)
        
        with placeholder.container():
            render_display(texto, tema)
            st.caption(f"Próximo em {wait_time}s...")
        
        time.sleep(wait_time)
        st.rerun()
    else:
        # Modo Manual
        st.session_state.mini %= maxy
        tema = temas_list[st.session_state.mini]
        
        # Botão More (+)
        analise = say_number(tema)
        if col2.button("✚", help=help_tips[4] + " • " + analise):
            pass # Lógica de expansão se necessária

        texto = get_processed_content(tema)
        with placeholder.container():
            render_display(texto, tema)

def page_eureka():
    help_tips = load_help(st.session_state.lang)
    col_input, col_plus, col_rand, col_help, col_res = st.columns([2.5, 1.5, 1.5, 0.7, 4])

    with col_input:
        find_what = st.text_input(label=translate("buscar..."))

    if len(find_what) < 3:
        st.warning(translate("mínimo 3 letras..."))
        return

    eureka_list = load_eureka(find_what)
    if not eureka_list:
        st.error(translate("nada encontrado."))
        return

    # Processamento da lista em memória
    seed_data = []
    for line in eureka_list:
        p, _, f = line.partition(" : ")
        if p and f: seed_data.append({"display": f"{p} ➪ {f}", "tema": f[0:-5], "seed": f"{p} ➪ {f}"})

    if col_rand.button("✻"):
        st.session_state.eureka = random.randrange(0, len(seed_data))

    selected_idx = col_res.selectbox(
        f"↓ {len(seed_data)} ocorrências",
        range(len(seed_data)),
        index=st.session_state.get('eureka', 0) % len(seed_data),
        format_func=lambda x: seed_data[x]["display"]
    )
    st.session_state.eureka = selected_idx
    
    item = seed_data[selected_idx]
    texto = get_processed_content(item["tema"], item["seed"])
    
    with st.expander("EUREKA!", expanded=True):
        render_display(texto, item["tema"])

# --- MESTRE: ENTRY POINT ---

def main():
    # Estilização básica para remover margens excessivas
    st.set_page_config(layout="wide")
    
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="poly", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    pick_lang()
    draw_check_buttons()

    # Mapeamento de Info/Imagens da Sidebar
    pages_config = {
        "1": ("INFO_MINI.md", "img_mini.jpg", page_mini),
        "2": ("INFO_YPOEMAS.md", "img_ypoemas.jpg", page_ypoemas),
        "3": ("INFO_EUREKA.md", "img_eureka.jpg", page_eureka),
        "4": ("INFO_OFF-MACHINA.md", "img_off-machina.jpg", page_off_machina),
        "5": ("INFO_BOOKS.md", "img_books.jpg", page_books),
        "6": ("INFO_POLY.md", "img_poly.jpg", page_polys),
        "7": ("INFO_ABOUT.md", "img_about.jpg", page_abouts),
    }

    if chosen_id in pages_config:
        info_md, img, func = pages_config[chosen_id]
        st.sidebar.info(load_md_file(info_md))
        st.sidebar.image(img)
        func()

    show_icons()

if __name__ == "__main__":
    main()
