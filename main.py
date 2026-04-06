import streamlit as st
import streamlit_antd_components as sac
import streamlit_selection_bar as stx
import random
import time
import os

# [Lógica de inicialização e estados mantida conforme original]

if st.session_state.visy:
    update_visy()
    temas_list = load_temas(st.session_state.book)
    maxy_ypoemas = len(temas_list)
    st.session_state.take = random.randrange(0, maxy_ypoemas)
    temas_list = load_temas("todos os temas")
    maxy_mini = len(temas_list)
    st.session_state.mini = random.randrange(0, maxy_mini)
    st.success(translate("bem vindo à **máquina de fazer Poesia...**"))
    st.session_state.draw = True
    st.session_state.visy = False

st.session_state.last_lang = st.session_state.lang

def page_mini():
    temas_list = load_temas("todos os temas")
    maxy_mini = len(temas_list)
    if st.session_state.mini > maxy_mini:
        st.session_state.mini = 0

    with st.container():
        foo1, more, rand, auto, foo2 = st.columns([1, 1, 1, 1, 1])
        help_tips = load_help(st.session_state.lang)
        rand_btn = rand.button("✻", help=help_tips[1])
        st.session_state.auto = auto.checkbox("auto")

        if st.session_state.auto:
            st.session_state.talk = False
            st.session_state.vydo = False
            with st.sidebar:
                wait_time = st.slider(translate("tempo de exibição (em segundos): "), 5, 60)

        if rand_btn:
            st.session_state.rand = True
            st.session_state.mini = random.randrange(0, maxy_mini)
        else:
            st.session_state.rand = False

        st.session_state.tema = temas_list[st.session_state.mini]
        analise = say_number(st.session_state.tema)
        more_btn = more.button("✚", help=help_tips[4] + " • " + analise)

        if more_btn:
            st.session_state.rand = False

        lnew = True
        if st.session_state.vydo:
            lnew = False
            show_video("mini")
            update_readings("video_mini")
            st.session_state.vydo = False

        if lnew or st.session_state.auto:
            if st.session_state.rand:
                st.session_state.mini = random.randrange(0, maxy_mini)
                st.session_state.tema = temas_list[st.session_state.mini]

            if st.session_state.lang != st.session_state.last_lang:
                curr_ypoema = load_lypo()
            else:
                curr_ypoema = load_poema(st.session_state.tema, "")
                curr_ypoema = load_lypo()

            if st.session_state.lang != "pt":
                curr_ypoema = translate(curr_ypoema)
                typo_user = "TYPO_" + IPAddres
                with open(os.path.join("./temp/" + typo_user), "w", encoding="utf-8") as save_typo:
                    save_typo.write(curr_ypoema)
                curr_ypoema = load_typo()

            update_readings(st.session_state.tema)
            LOGO_TEXTO = curr_ypoema
            LOGO_IMAGE = None
            if st.session_state.draw:
                LOGO_IMAGE = load_arts(st.session_state.tema)

            mini_place_holder = st.empty()
            st.write("")

            if not st.session_state.auto:
                with mini_place_holder:
                    write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
                if st.session_state.talk:
                    talk(curr_ypoema)
            else:
                while st.session_state.auto:
                    # [Lógica auto repetida do bloco anterior]
                    with mini_place_holder:
                        mini_place_holder.empty()
                        write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
                        time.sleep(wait_time)

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy_ypoemas = len(temas_list) - 1
    if st.session_state.take > maxy_ypoemas or st.session_state.take < 0:
        st.session_state.take = 0

    with st.container():
        foo1, more, last, rand, nest, manu, foo2 = st.columns([1, 1, 1, 1, 1, 1, 1])
        help_tips = load_help(st.session_state.lang)
        
        btn_more = more.button("✚", help=help_tips[4])
        btn_last = last.button("◀", help=help_tips[0])
        btn_rand = rand.button("✻", help=help_tips[1])
        btn_nest = nest.button("▶", help=help_tips[2])
        btn_manu = manu.button("?", help="help !!!")

        if btn_last:
            st.session_state.take -= 1
            if st.session_state.take < 0: st.session_state.take = maxy_ypoemas
        if btn_rand:
            st.session_state.take = random.randrange(0, maxy_ypoemas)
        if btn_nest:
            st.session_state.take += 1
            if st.session_state.take > maxy_ypoemas: st.session_state.take = 0

        if not st.session_state.draw:
            options = list(range(len(temas_list)))
            opt_take = st.selectbox("↓ " + translate("lista de Temas"), options, index=st.session_state.take, format_func=lambda z: temas_list[z])
            if opt_take != st.session_state.take: st.session_state.take = opt_take

        st.session_state.tema = temas_list[st.session_state.take]
        # [Exibição do yPoema no container]
        ypoemas_expander = st.expander("", expanded=True)
        with ypoemas_expander:
            # [Lógica de carregamento e escrita original]
            pass

def page_eureka():
    with st.container():
        seed, more, rand, manu, occurrences = st.columns([4, 1, 1, 1, 4])
        # [Restante da lógica eureka mantida no container]

def page_off_machina():
    with st.container():
        foo1, last, rand, nest, love, manu, foo2 = st.columns([1, 1, 1, 1, 1, 1, 1])
        # [Restante da lógica off-machina mantida no container]

def main():
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="mini", description=""),
        stx.TabBarItemData(id=2, title="yPoemas", description=""),
        stx.TabBarItemData(id=3, title="eureka", description=""),
        stx.TabBarItemData(id=4, title="off-machina", description=""),
        stx.TabBarItemData(id=5, title="books", description=""),
        stx.TabBarItemData(id=6, title="poly", description=""),
        stx.TabBarItemData(id=7, title="about", description=""),
    ], default=2)

    pick_lang()
    draw_check_buttons()

    pages = {
        "1": (page_mini, "INFO_MINI.md", "img_mini.jpg"),
        "2": (page_ypoemas, "INFO_YPOEMAS.md", "img_ypoemas.jpg"),
        "3": (page_eureka, "INFO_EUREKA.md", "img_eureka.jpg"),
        "4": (page_off_machina, "INFO_OFF-MACHINA.md", "img_off-machina.jpg"),
        "5": (page_books, "INFO_BOOKS.md", "img_books.jpg"),
        "6": (page_polys, "INFO_POLY.md", "img_poly.jpg"),
        "7": (page_abouts, "INFO_ABOUT.md", "img_about.jpg"),
    }

    if chosen_id in pages:
        func, info, img = pages[chosen_id]
        st.sidebar.info(load_md_file(info))
        magy = img
        # Chamada protegida por container para evitar sobreposição da sidebar
        with st.container():
            func()

    with st.sidebar:
        st.image(magy)
    show_icons()

if __name__ == "__main__":
    main()
