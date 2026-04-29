import streamlit as st
import extra_streamlit_components as stx
import os
import random

# --- CONFIGURAÇÃO E ESTADO INICIAL ---
def init_session():
    defaults = {
        "lang": "pt",
        "last_lang": "pt",
        "eureka": 0,
        "tema": "geral",
        "off_book": 0,
        "off_take": 0,
        "book": "livro vivo",
        "poly_take": 0,
        "poly_file": "poly.txt",  # Lista oficial de idiomas
        "draw": True,
        "talk": False,
        "poly_name": "Português",
        "poly_lang": "pt"
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

# --- PÁGINAS DO SISTEMA ---

def page_eureka():
    help_tips = load_help(st.session_state.lang)
    help_rand, help_more = help_tips[1], help_tips[4]

    seed, more_col, rand_col, manu_col, occurrences = st.columns([2.5, 1.5, 1.5, 0.7, 4])

    with seed:
        find_what = st.text_input(label=translate("digite algo para buscar..."))

    btn_more = more_col.button("✚", help=help_more)
    btn_rand = rand_col.button("✻", help=help_rand)
    btn_manu = manu_col.button("?", help="help !!!")

    if btn_manu:
        st.subheader(load_md_file("MANUAL_EUREKA.md"))

    if len(find_what) < 3:
        st.warning(translate("digite pelo menos 3 letras..."))
        return

    seed_list = []
    soma_tema = []
    eureka_list = load_eureka(find_what)

    for line in eureka_list:
        this_line = line.strip("\n")
        palas, _, fonte = this_line.partition(" : ")
        if not palas or not fonte:
            continue
        seed_list.append(f"{palas} ➪ {fonte}")
        seed_tema = fonte[0:-5]
        if seed_tema not in soma_tema:
            soma_tema.append(seed_tema)

    if not btn_more and not btn_manu:
        st.session_state.eureka = 0

    if not seed_list:
        st.warning(translate(f'nenhuma ocorrência de "{find_what}" encontrada...'))
        return

    seed_list.sort()
    
    if btn_rand:
        st.session_state.eureka = random.randrange(0, len(seed_list))

    with occurrences:
        info_find = translate('ocorrência de "') if len(seed_list) == 1 else translate('ocorrências de "')
        label = f"↓ {len(seed_list)} {info_find}{find_what}"
        if len(soma_tema) > 1:
            label += f"\" em {len(soma_tema)} temas"

        opt_ocur = st.selectbox(
            label,
            range(len(seed_list)),
            index=st.session_state.eureka,
            format_func=lambda y: seed_list[y],
            key="sb_eureka"
        )
        st.session_state.eureka = opt_ocur

    this_seed = seed_list[st.session_state.eureka]
    _, _, nome_tema = this_seed.partition(" ➪ ")
    seed_tema = nome_tema[0:-5]
    st.session_state.tema = seed_tema

    if st.session_state.lang != st.session_state.last_lang:
        curr_ypoema = load_lypo()
    else:
        load_poema(seed_tema, this_seed)
        curr_ypoema = load_lypo()

    if st.session_state.lang != "pt":
        curr_ypoema = translate(curr_ypoema)
        curr_ypoema = curr_ypoema.replace('\r\n', '\n')

    with st.expander("", expanded=True):
        img = load_arts(seed_tema) if st.session_state.draw else None
        write_ypoema(curr_ypoema, img)
        update_readings(seed_tema)

    if st.session_state.talk:
        talk(curr_ypoema)


def page_off_machina():
    off_books_list = load_all_offs()
    sobrios = "↓ " + translate("lista de Livros")
    opt_off_book = st.selectbox(
        sobrios,
        range(len(off_books_list)),
        index=st.session_state.off_book,
        format_func=lambda x: off_books_list[x],
        key="sb_off_book"
    )

    if opt_off_book != st.session_state.off_book:
        st.session_state.off_book = opt_off_book
        st.session_state.off_take = 0

    off_book_name = off_books_list[st.session_state.off_book]
    help_tips = load_help(st.session_state.lang)
    
    col_nav, col_manu = st.columns([8, 2])
    with col_nav:
        f1, btn_l, btn_r, btn_n, btn_v, f2 = st.columns([1, 1, 1, 1, 1, 1])
        last = btn_l.button("◀", help=help_tips[0])
        rand = btn_r.button("✻", help=help_tips[1])
        nest = btn_n.button("▶", help=help_tips[2])
        love = btn_v.button("❤", help=help_tips[3])
    
    manu = col_manu.button("?", help="help !!!")

    this_off_book = load_off_book(off_book_name)
    off_book_pagys = load_book_pages(this_off_book)
    maxy = len(off_book_pagys) - 1

    if last:
        st.session_state.off_take = maxy if st.session_state.off_take <= 0 else st.session_state.off_take - 1
    if rand:
        st.session_state.off_take = random.randrange(0, maxy + 1)
    if nest:
        st.session_state.off_take = 0 if st.session_state.off_take >= maxy else st.session_state.off_take + 1

    if not st.session_state.draw:
        st.session_state.off_take = st.selectbox(
            "↓ " + translate("lista de Títulos"),
            range(len(off_book_pagys)),
            index=st.session_state.off_take,
            format_func=lambda x: off_book_pagys[x]
        )

    if manu:
        st.subheader(load_md_file("MANUAL_OFF-MACHINA.md"))
    elif love:
        list_readings()
        st.markdown(get_binary_file_downloader_html("./temp/read_list.txt", "views"), unsafe_allow_html=True)
    else:
        header = f"⚫ {st.session_state.lang} ( {st.session_state.off_take + 1}/{len(off_book_pagys)} )"
        with st.expander(header, expanded=True):
            pipe_line = this_off_book[st.session_state.off_take].split("|")
            
            if "@ " in pipe_line[1]:
                if st.session_state.lang == st.session_state.last_lang:
                    nome_tema = pipe_line[1].replace("@ ", "")
                    load_poema(nome_tema, "")
                off_book_text = "<br>" + load_lypo()
            else:
                off_book_text = "<br>".join(pipe_line)

            if st.session_state.off_take == 0:
                c1, c2 = st.columns([2.5, 7.5])
                with c1:
                    img_path = load_arts("livro_vivo") if off_book_name == "livro_vivo" else f"./off_machina/capa_{off_book_name}.jpg"
                    st.image(img_path, use_column_width=True)
                with c2:
                    st.markdown(off_book_text, unsafe_allow_html=True)
            else:
                if st.session_state.lang != "pt":
                    off_book_text = translate(off_book_text)
                img = load_arts(off_book_name) if st.session_state.draw else None
                write_ypoema(off_book_text, img)
                update_readings(off_book_name)

        if st.session_state.talk:
            talk(off_book_text)


def page_polys():
    polys_col, ok_col = st.columns([9.3, 0.7])
    with polys_col:
        poly_list = []
        poly_data = []
        path_poly = os.path.join("./base/", st.session_state.poly_file)
        
        if os.path.exists(path_poly):
            with open(path_poly, "r", encoding="utf-8") as f:
                for line in f:
                    if " : " in line:
                        this_line = line.strip()
                        pais, _, ling = this_line.partition(" : ")
                        poly_list.append(this_line)
                        poly_data.append((pais, ling))
        
        if not poly_list:
            st.error("Erro: poly.txt não encontrado em ./base/")
            return

        opt_poly = st.selectbox(
            f"↓ lista: {len(poly_list)} idiomas",
            range(len(poly_list)),
            index=st.session_state.poly_take,
            format_func=lambda x: poly_list[x],
            key="sb_poly"
        )

    with ok_col:
        doit = st.button("✔", help="confirmar?")

    if doit:
        selecionado = poly_data[opt_poly]
        st.session_state.poly_name = translate(selecionado[0])
        st.session_state.poly_lang = selecionado[1]
        st.session_state.poly_take = opt_poly
        st.session_state.last_lang = st.session_state.lang
        st.session_state.lang = selecionado[1]
        st.rerun()

    with st.expander("", expanded=True):
        st.subheader(load_md_file("MANUAL_POLY.md"))


def page_books():
    books_list = ["livro vivo", "poemas", "jocosos", "ensaios", "variações", "metalinguagem", "sociais", "todos os temas", "outros autores", "signos_fem", "signos_mas", "todos os signos"]
    books_col, ok_col = st.columns([9.3, 0.7])
    
    with books_col:
        opt_book = st.selectbox("↓ " + translate("lista de Livros"), range(len(books_list)), index=books_list.index(st.session_state.book))
    
    with ok_col:
        doit = st.button("✔", key="btn_book_ok")

    temas_list = load_temas(books_list[opt_book])
    st.write(", ".join([line.strip() for line in temas_list]) + f" ▶ {len(temas_list)} páginas")

    with st.expander("", expanded=True):
        st.subheader(load_md_file("MANUAL_BOOKS.md"))

    if doit:
        st.session_state.take = 0
        st.session_state.book = books_list[opt_book]


def page_abouts():
    abouts_list = ["comments", "prefácio", "machina", "off-machina", "outros", "traduttore", "bibliografia", "imagens", "samizdát", "notes", "license", "index"]
    opt_abouts = st.selectbox("↓ " + translate("sobre"), range(len(abouts_list)), format_func=lambda x: abouts_list[x])
    
    choice = abouts_list[opt_abouts].upper()
    with st.expander("", expanded=True):
        if choice == "MACHINA":
            st.subheader(load_md_file("ABOUT_MACHINA_A.md"))
            txt = load_info(st.session_state.tema)
            img = f"./images/matrix/{st.session_state.tema}.jpg"
            write_ypoema(txt, img)
            st.subheader(load_md_file("ABOUT_MACHINA_D.md"))
        else:
            st.subheader(load_md_file(f"ABOUT_{choice}.md"))

# --- MAPEAMENTO DE NAVEGAÇÃO ---

PAGES = {
    "1": {"func": page_mini, "img": "img_mini.jpg", "info": "INFO_MINI.md"},
    "2": {"func": page_ypoemas, "img": "img_ypoemas.jpg", "info": "INFO_YPOEMAS.md"},
    "3": {"func": page_eureka, "img": "img_eureka.jpg", "info": "INFO_EUREKA.md"},
    "4": {"func": page_off_machina, "img": "img_off-machina.jpg", "info": "INFO_OFF-MACHINA.md"},
    "5": {"func": page_books, "img": "img_books.jpg", "info": "INFO_BOOKS.md"},
    "6": {"func": page_polys, "img": "img_poly.jpg", "info": "INFO_POLY.md"},
    "7": {"func": page_abouts, "img": "img_about.jpg", "info": "INFO_ABOUT.md"},
}

def main():
    init_session()

    chosen_id = stx.tab_bar(
        data=[
            stx.TabBarItemData(id=1, title="mini", description=""),
            stx.TabBarItemData(id=2, title="yPoemas", description=""),
            stx.TabBarItemData(id=3, title="eureka", description=""),
            stx.TabBarItemData(id=4, title="off-machina", description=""),
            stx.TabBarItemData(id=5, title="books", description=""),
            stx.TabBarItemData(id=6, title="poly", description=""),
            stx.TabBarItemData(id=7, title="about", description=""),
        ],
        default=2,
    )

    pick_lang()
    draw_check_buttons()

    page_data = PAGES.get(str(chosen_id))
    if page_data:
        st.sidebar.info(load_md_file(page_data["info"]))
        with st.sidebar:
            st.image(page_data["img"])
        page_data["func"]()

    show_icons()

if __name__ == "__main__":
    main()
