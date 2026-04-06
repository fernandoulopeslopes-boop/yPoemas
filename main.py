import streamlit as st
import streamlit_antd_components as sac
import extra_streamlit_components as stx
import random
import time
import os

# [Lógica de inicialização de estados e funções auxiliares]

# MOVIDO: Definição da função antes da chamada para evitar NameError
def update_visy():
    # Insira aqui a lógica original da sua função update_visy
    pass

if 'visy' not in st.session_state:
    st.session_state.visy = True

if st.session_state.visy:
    update_visy() # Agora a função já existe no escopo
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
        rand_btn = rand.button("✻", help=help_tips[1], key="btn_rand_mini")
        st.session_state.auto = auto.checkbox("auto", key="chk_auto_mini")

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
        more_btn = more.button("✚", help=help_tips[4] + " • " + analise, key="btn_more_mini")

        if more_btn:
            st.session_state.rand = False

        lnew = True
        if st.session_state.vydo:
            lnew = False
            show_video("mini")
            update_readings("video_mini")
            st.session_state.vydo = False

        if lnew or st.session_state.auto:
            curr_ypoema = load_poema(st.session_state.tema, "")
            update_readings(st.session_state.tema)
            LOGO_TEXTO = curr_ypoema
            LOGO_IMAGE = load_arts(st.session_state.tema) if st.session_state.draw else None

            mini_place_holder = st.empty()
            if not st.session_state.auto:
                with mini_place_holder:
                    write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
                if st.session_state.talk:
                    talk(curr_ypoema)
            else:
                while st.session_state.auto:
                    with mini_place_holder:
                        mini_place_holder.empty()
                        write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
                        time.sleep(wait_time)

def main():
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
        with st.container():
            func()
        with st.sidebar:
            st.image(img)

    show_icons()

if __name__ == "__main__":
    main()
