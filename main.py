import os
import re
import time
import random
import base64
import socket
import streamlit as st

from extra_streamlit_components import TabBar as stx
from datetime import datetime
from lay_2_ypo import gera_poema

### bof: settings

# the User IPAddress for LYPO, TYPO
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

def have_internet():
    try:
        # Tenta conectar ao IP da Cloudflare na porta 80 (HTTP)
        socket.create_connection(("1.1.1.1", 80), timeout=3)
        return True
    except OSError:
        return False
        
st.set_page_config(
    page_title="a Machina de fazer Poesia - yPoemas",
    page_icon="★",
    layout="centered",
    initial_sidebar_state="expanded",
)

if have_internet():
    try:
        from deep_translator import GoogleTranslator
        from gtts import gTTS
    except ImportError:
        st.warning("Dependências ausentes no requirements.txt")
else:
    st.warning("Internet não conectada. Traduções não disponíveis no momento.")

# --- BLOCO ÚNICO DE CSS (Otimizado) ---
st.markdown(
    """
    <style>
    /* 1. Respiro no topo: Ajustado para o ponto ideal */
    .block-container {
        padding-top: 2rem !important; 
        margin-top: 0px !important;
    }

    /* 2. Sidebar e Botão de Colapso (>>) */
    [data-testid="stSidebar"] {
        width: 310px !important;
        min-width: 310px !important;
    }

    [data-testid="stSidebarCollapseButton"] {
        left: 310px !important;
        z-index: 999999;
    }

    /* 3. Estética do Poema */
    mark { background-color: powderblue; color: black; }
    .logo-text {
        font-weight: 600;
        font-size: 16px;
        font-family: 'IBM Plex Sans';
        color: #000000;
        padding-left: 5px;
    }
    header { visibility: hidden; height: 0px; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

### eof: settings

# Initialize SessionState

if "lang" not in st.session_state:
    st.session_state.lang = "pt"
if "last_lang" not in st.session_state:
    st.session_state.last_lang = "pt"

if "book" not in st.session_state:  #  index for books_list
    st.session_state.book = "livro vivo"
if "take" not in st.session_state:  #  index for selected tema in books_list
    st.session_state.take = 0
if "mini" not in st.session_state:  #  index for selected tema in page_mini
    st.session_state.mini = 0
if "tema" not in st.session_state:  #  selected tema for all pages
    st.session_state.tema = "Fatos"

if "off_book" not in st.session_state:  #  index for off_books_list
    st.session_state.off_book = 0
if "off_take" not in st.session_state:  #  index for selected book in off_books_list
    st.session_state.off_take = 0

if "eureka" not in st.session_state:  #  index for random tema in page_eureka
    st.session_state.eureka = 0

if "poly_lang" not in st.session_state:
    st.session_state.poly_lang = "ca"
if "poly_name" not in st.session_state:
    st.session_state.poly_name = "català"
if "poly_take" not in st.session_state:
    st.session_state.poly_take = 12
if "poly_file" not in st.session_state:
    st.session_state.poly_file = "poly_pt.txt"

if "visy" not in st.session_state:
    st.session_state.visy = True
if "nany_visy" not in st.session_state:
    st.session_state.nany_visy = 0

if "draw" not in st.session_state:
    st.session_state.draw = False
if "talk" not in st.session_state:
    st.session_state.talk = False
if "vydo" not in st.session_state:
    st.session_state.vydo = False
if "arts" not in st.session_state:
    st.session_state.arts = []
if "auto" not in st.session_state:
    st.session_state.auto = False
if "rand" not in st.session_state:
    st.session_state.rand = False

### eof: settings


### bof: tools


def pick_lang():  # define idioma de forma horizontal na sidebar
    with st.sidebar:
        cols = st.columns([1, 1, 1, 1, 1, 1])
        
        btn_pt = cols[0].button("pt", help="Português")
        btn_es = cols[1].button("es", help="Español")
        btn_it = cols[2].button("it", help="Italiano")
        btn_fr = cols[3].button("fr", help="Français")
        btn_en = cols[4].button("en", help="English")
        btn_xy = cols[5].button("⚒️", help="ca")

        if btn_pt:
            st.session_state.lang = "pt"
            st.session_state.poly_file = "poly_pt.txt"
        elif btn_es:
            st.session_state.lang = "es"
            st.session_state.poly_file = "poly_es.txt"
        elif btn_it:
            st.session_state.lang = "it"
            st.session_state.poly_file = "poly_it.txt"
        elif btn_fr:
            st.session_state.lang = "fr"
            st.session_state.poly_file = "poly_fr.txt"
        elif btn_en:
            st.session_state.lang = "en"
            st.session_state.poly_file = "poly_en.txt"
        elif btn_xy:
            st.session_state.last_lang = st.session_state.lang
            st.session_state.lang = st.session_state.poly_lang

# ... [Mantenha as funções translate, load_help, etc.] ...

def translate(input_text):
    if st.session_state.lang == "pt":  # don't need translations here
        return input_text

    if not have_internet():
        st.session_state.lang = "pt"
        return input_text

    try:
        output_text = GoogleTranslator(
            source="pt", target=st.session_state.lang
        ).translate(text=input_text)

        output_text = output_text.replace("<br>>", "<br>")
        output_text = output_text.replace("< br>", "<br>")
        output_text = output_text.replace("<br >", "<br>")
        output_text = output_text.replace("<br ", "<br>")
        output_text = output_text.replace(" br>", "<br>")
        return output_text
    except:
        return translate("Arquivo muito grande para ser traduzido.")


pick_lang()


def load_help_tips():
    help_list = []
    with open(os.path.join("./base/helpers.txt"), encoding="utf-8") as file:
        for line in file:
            help_list.append(line)
    file.close()

    return help_list


def load_help():
    returns = []
    returns.append(translate("anterior"))
    returns.append(translate("escolhe tema ao acaso"))
    returns.append(translate("próximo"))
    returns.append(translate("mais lidos..."))
    returns.append(translate("gera novo yPoema"))
    returns.append(translate("imagem"))
    returns.append(translate("audio"))
    return returns


def draw_check_buttons():
    draw_text, talk_text = st.sidebar.columns([3.2, 3.8])
    help_tips = load_help()
    help_draw = help_tips[5]
    help_talk = help_tips[6]
    st.session_state.draw = draw_text.checkbox(
        help_draw, st.session_state.draw, key="draw_machina"
    )
    st.session_state.talk = talk_text.checkbox(
        help_talk, st.session_state.talk, key="talk_machina"
    )

def load_md_file(file):  # Open files for about's
    try:
        with open(os.path.join("./md_files/" + file), encoding="utf-8") as file_to_open:
            file_text = file_to_open.read()

        if not "rol_" in file.lower():  # do not translate theme
            file_text = translate(file_text)
    except:
        file_text = translate("ooops... arquivo ( " + file + " ) não pode ser aberto.")
        st.session_state.lang = "pt"

    return file_text


def main():
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

    draw_check_buttons()

    # Correção das vírgulas nas atribuições de magy
    if chosen_id == "1":
        st.sidebar.info(load_md_file("INFO_MINI.md"))
        magy = "./images/img_mini.jpg"
        page_mini()
    elif chosen_id == "2":
        st.sidebar.info(load_md_file("INFO_YPOEMAS.md"))
        magy = "./images/img_ypoemas.jpg"
        page_ypoemas()
    elif chosen_id == "3":
        st.sidebar.info(load_md_file("INFO_EUREKA.md"))
        magy = "./images/img_eureka.jpg"
        page_eureka()
    elif chosen_id == "4":
        st.sidebar.info(load_md_file("INFO_OFF-MACHINA.md"))
        magy = "./images/img_off-machina.jpg"
        page_off_machina()
    elif chosen_id == "5":
        st.sidebar.info(load_md_file("INFO_BOOKS.md"))
        magy = "./images/img_books.jpg"
        page_books()
    elif chosen_id == "6":
        st.sidebar.info(load_md_file("INFO_POLY.md"))
        magy = "./images/img_poly.jpg"
        page_polys()
    elif chosen_id == "7":
        st.sidebar.info(load_md_file("INFO_ABOUT.md"))
        magy = "./images/img_about.jpg"
        page_abouts()

    with st.sidebar:
        # Só tenta carregar se magy for uma string válida
        if 'magy' in locals() and isinstance(magy, str):
            st.image(magy)

    show_icons()

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy_ypoemas = len(temas_list) - 1
    if (
        st.session_state.take > maxy_ypoemas or st.session_state.take < 0
    ):  # just in case
        st.session_state.take = 0

    foo1, more, last, rand, nest, manu, foo2 = st.columns([3, 1, 1, 1, 1, 1, 3])

    help_tips = load_help(st.session_state.lang)
    help_last = help_tips[0]
    help_rand = help_tips[1]
    help_nest = help_tips[2]
    help_more = help_tips[4]

    more = more.button("✚", help=help_more)
    last = last.button("◀", help=help_last)
    rand = rand.button("✻", help=help_rand)
    nest = nest.button("▶", help=help_nest)
    manu = manu.button("?", help="help !!!")

    if last:
        st.session_state.take -= 1
        if st.session_state.take < 0:
            st.session_state.take = maxy_ypoemas

    if rand:
        st.session_state.take = random.randrange(0, maxy_ypoemas)

    if nest:
        st.session_state.take += 1
        if st.session_state.take > maxy_ypoemas:
            st.session_state.take = 0

    if not st.session_state.draw:
        options = list(range(len(temas_list)))
        sobrios = "↓  " + translate("lista de Temas")
        opt_take = st.selectbox(
            sobrios,
            options,
            index=st.session_state.take,
            format_func=lambda z: temas_list[z],
            key="opt_take",
        )

        if opt_take != st.session_state.take:
            st.session_state.take = opt_take

    st.session_state.tema = temas_list[st.session_state.take]

    lnew = True
    if manu:
        st.subheader(load_md_file("MANUAL_YPOEMAS.md"))

    if st.session_state.vydo:
        lnew = False
        show_video("ypoemas")
        update_readings("video_ypoemas")
        st.session_state.vydo = False

    if lnew:
        what_book = (
            "⚫  "
            + st.session_state.lang
            + " ( "
            + st.session_state.book
            + " ) ( "
            + str(st.session_state.take + 1)
            + " / "
            + str(len(temas_list))
            + " )"
        )

        ypoemas_expander = st.expander(what_book, expanded=True)
        with ypoemas_expander:
            if st.session_state.lang != st.session_state.last_lang:
                curr_ypoema = load_lypo()  # changes in lang, keep LYPO
            else:
                curr_ypoema = load_poema(st.session_state.tema, "")
                curr_ypoema = load_lypo()

            if st.session_state.lang != "pt":  # translate if idioma <> pt
                curr_ypoema = translate(curr_ypoema)
                typo_user = "TYPO_" + IPAddres
                with open(
                    os.path.join("./temp/" + typo_user), "w", encoding="utf-8"
                ) as save_typo:
                    save_typo.write(curr_ypoema)
                    save_typo.close()
                curr_ypoema = load_typo()  # to normalize line breaks in text

            update_readings(st.session_state.tema)
            LOGO_TEXTO = curr_ypoema
            LOGO_IMAGE = None
            if st.session_state.draw:
                LOGO_IMAGE = load_arts(st.session_state.tema)

            write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

            if manu:
                LOGO_TEXTO = load_info(st.session_state.tema)
                if st.session_state.lang != "pt":  # translate if idioma <> pt
                    LOGO_TEXTO = translate(LOGO_TEXTO)

                LOGO_IMAGE = (
                    "./images/matrix/" + st.session_state.tema.capitalize() + ".jpg"
                )
                write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

        if st.session_state.talk:
            talk(curr_ypoema)

        # st.markdown(get_binary_file_downloader_html('./temp/'+'LYPO_' + IPAddres, '➪ '+st.session_state.tema), unsafe_allow_html=True)


def page_eureka():
    help_tips = load_help(st.session_state.lang)
    help_rand = help_tips[1]
    help_more = help_tips[4]

    seed, more, rand, manu, occurrences = st.columns([2.5, 1.5, 1.5, 0.7, 4])

    with seed:
        find_what = st.text_input(
            label=translate("digite algo para buscar..."),
        )

    with more:
        more = more.button("✚", help=help_more)

    with rand:
        rand = rand.button("✻", help=help_rand)

    with manu:
        manu = manu.button("?", help="help !!!")

    if manu:
        st.subheader(load_md_file("MANUAL_EUREKA.md"))

    if len(find_what) < 3:
        st.warning(translate("digite pelo menos 3 letras..."))
    else:
        seed_list = []
        soma_tema = []

        eureka_list = load_eureka(find_what)
        for line in eureka_list:
            this_line = line.strip("\n")
            part_line = this_line.partition(" : ")
            palas = part_line[0]
            fonte = part_line[2]
            seed_tema = fonte[0:-5]
            if (palas is None) or (fonte is None):
                continue
            else:
                seed_list.append(palas + " ➪ " + fonte)
                if not seed_tema in soma_tema:
                    soma_tema.append(seed_tema)

        if (not more) and (not manu):
            st.session_state.eureka = 0

        if len(seed_list) == 0:
            st.warning(
                translate(
                    'nenhuma ocorrência das letras " '
                    + find_what
                    + ' " foi encontrada...'
                )
            )
        elif len(seed_list) >= 1:
            seed_list.sort()
            if len(seed_list) == 1:
                info_find = translate('ocorrência de "')
            else:
                info_find = translate('ocorrências de "')

            info_find += find_what
            if len(soma_tema) > 1:
                info_find += translate('" em ' + str(len(soma_tema)) + " temas")

            if rand:
                st.session_state.eureka = random.randrange(0, len(seed_list))

            with occurrences:
                options = list(range(len(seed_list)))
                opt_ocur = st.selectbox(
                    "↓  " + str(len(seed_list)) + " " + info_find,
                    options,
                    index=st.session_state.eureka,
                    format_func=lambda y: seed_list[y],
                    key="opt_ocur",
                )

            st.session_state.eureka = opt_ocur
            this_seed = seed_list[st.session_state.eureka]
            part_line = this_seed.partition(" ➪ ")
            nome_tema = part_line[2]
            seed_tema = nome_tema[0:-5]

            st.session_state.tema = seed_tema

            if st.session_state.lang != st.session_state.last_lang:
                curr_ypoema = load_lypo()  # changes in lang, keep LYPO
            else:
                curr_ypoema = load_poema(seed_tema, this_seed)
                curr_ypoema = load_lypo()

            if st.session_state.lang != "pt":  # translate if idioma <> pt
                curr_ypoema = translate(curr_ypoema)
                typo_user = "TYPO_" + IPAddres
                with open(
                    os.path.join("./temp/" + typo_user), "w", encoding="utf-8"
                ) as save_typo:
                    save_typo.write(curr_ypoema)
                    save_typo.close()
                curr_ypoema = load_typo()  # to normalize line breaks in text

            lnew = True
            if st.session_state.vydo:
                lnew = False
                show_video("eureka")
                update_readings("video_eureka")
                st.session_state.vydo = False

            if lnew:
                eureka_expander = st.expander("", expanded=True)
                with eureka_expander:
                    LOGO_TEXTO = curr_ypoema
                    LOGO_IMAGE = None
                    if st.session_state.draw:
                        LOGO_IMAGE = load_arts(seed_tema)

                    write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
                    update_readings(seed_tema)

                if st.session_state.talk:
                    talk(curr_ypoema)
            if manu:
                lnew = False
                LOGO_TEXTO = load_info(seed_tema)
                if st.session_state.lang != "pt":  # translate if idioma <> pt
                    LOGO_TEXTO = translate(LOGO_TEXTO)

                LOGO_IMAGE = "./images/matrix/" + seed_tema.capitalize() + ".jpg"
                write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

        else:
            st.warning(
                translate(
                    "nenhum verbete encontrado com essas letras ---> " + find_what
                )
            )


def page_off_machina():  # available off_machina_books
    off_books_list = load_all_offs()
    options = list(range(len(off_books_list)))
    sobrios = "↓  " + translate("lista de Livros")
    opt_off_book = st.selectbox(
        sobrios,
        options,
        index=st.session_state.off_book,
        format_func=lambda x: off_books_list[x],
        key="opt_off_book",
    )

    if opt_off_book != st.session_state.off_book:
        st.session_state.off_book = opt_off_book
        st.session_state.off_take = 0

    off_book_name = off_books_list[st.session_state.off_book]

    help_tips = load_help(st.session_state.lang)
    help_last = help_tips[0]
    help_rand = help_tips[1]
    help_nest = help_tips[2]
    help_love = help_tips[3]

    foo1, last, rand, nest, love, manu, foo2 = st.columns([2.5, 1, 1, 1, 1, 1, 2.5])
    last = last.button("◀", help=help_last)
    rand = rand.button("✻", help=help_rand)
    nest = nest.button("▶", help=help_nest)
    love = love.button("❤", help=help_love)
    manu = manu.button("?", help="help !!!")

    this_off_book = load_off_book(off_book_name)
    off_book_pagys = load_book_pages(this_off_book)
    maxy_off_machina = len(off_book_pagys) - 1

    if last:
        st.session_state.off_take -= 1
        if st.session_state.off_take < 0:
            st.session_state.off_take = maxy_off_machina

    if rand:
        st.session_state.off_take = random.randrange(0, maxy_off_machina)

    if nest:
        st.session_state.off_take += 1
        if st.session_state.off_take > maxy_off_machina:
            st.session_state.off_take = 0

    if st.session_state.off_take > maxy_off_machina:  # just in case...
        st.session_state.off_take = 0

    if not st.session_state.draw:
        options = list(range(len(off_book_pagys)))
        sobrios = "↓  " + translate("lista de Títulos")
        opt_off_take = st.selectbox(
            sobrios,
            options,
            index=st.session_state.off_take,
            format_func=lambda x: off_book_pagys[x],
            key="opt_off_take",
        )

        if opt_off_take != st.session_state.off_take:
            st.session_state.off_take = opt_off_take

    lnew = True
    if manu:
        lnew = False
        st.subheader(load_md_file("MANUAL_OFF-MACHINA.md"))

    if love:
        lnew = False
        list_readings()
        st.markdown(
            get_binary_file_downloader_html("./temp/read_list.txt", "views"),
            unsafe_allow_html=True,
        )

    if st.session_state.vydo:
        lnew = False
        show_video("off-machina")
        update_readings("video_off-machina")
        st.session_state.vydo = False

    if lnew:
        what_book = (
            "⚫  "
            + st.session_state.lang
            + " ( "
            + str(st.session_state.off_take + 1)
            + "/"
            + str(len(off_book_pagys))
            + " )"
        )

        off_machina_expander = st.expander(what_book, True)
        with off_machina_expander:
            off_book_text = ""
            pipe_line = this_off_book[st.session_state.off_take].split("|")
            if "@ " in pipe_line[1]:
                if st.session_state.lang != st.session_state.last_lang:
                    off_book_text = load_lypo()  # changes in lang, keep LYPO
                else:
                    nome_tema = pipe_line[1].replace("@ ", "")
                    off_book_text = load_poema(nome_tema, "")  # no seed_eureka
                    off_book_text = "<br>" + load_lypo()
            else:
                for text in pipe_line:
                    off_book_text += text + "<br>"

            capo = st.session_state.off_take == 0

            if capo:
                capa, isbn = st.columns([2.5, 7.5])
                with capa:
                    if off_book_name == "livro_vivo":
                        LOGO_CAPA = load_arts("livro_vivo")
                        st.image(LOGO_CAPA, use_column_width=True)
                    else:
                        st.image(
                            "./off_machina/capa_" + off_book_name + ".jpg",
                            use_column_width=True,
                        )
                with isbn:
                    st.markdown(
                        off_book_text, unsafe_allow_html=True
                    )  # finally... write it
            else:
                if st.session_state.lang != "pt":
                    off_book_text = translate(off_book_text)

                LOGO_TEXTO = off_book_text
                LOGO_IMAGE = None
                if st.session_state.draw:
                    LOGO_IMAGE = load_arts(off_book_name)

                write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
                update_readings(off_book_name)

        if st.session_state.talk:
            talk(off_book_text)


def page_books():  # available books
    books, ok = st.columns([9.3, 0.7])
    with books:
        books_list = [
            "livro vivo",
            "poemas",
            "jocosos",
            "ensaios",
            "variações",
            "metalinguagem",
            "sociais",
            "todos os temas",
            "outros autores",
            "signos_fem",
            "signos_mas",
            "todos os signos",
        ]

        options = list(range(len(books_list)))
        sobrios = "↓  " + translate("lista de Livros")
        opt_book = st.selectbox(
            sobrios,
            options,
            index=books_list.index(st.session_state.book),
            format_func=lambda x: books_list[x],
            key="opt_book",
        )

        with ok:
            doit = st.button("✔", help="confirm ?")

        lnew = True
        if st.session_state.vydo:
            lnew = False
            show_video("books")
            update_readings("video_books")
            st.session_state.vydo = False

        if lnew:
            list_book = ""
            temas_list = load_temas(books_list[opt_book])
            for line in temas_list:
                list_book += line.strip() + ", "
            st.write(list_book[:-2] + " ▶ " + str(int(len(temas_list))) + " páginas")

            books_expander = st.expander("", True)
            with books_expander:
                st.subheader(load_md_file("MANUAL_BOOKS.md"))

            if doit:
                st.session_state.take = 0
                st.session_state.book = books_list[opt_book]


def page_polys():  # available languages
    polys, ok = st.columns([9.3, 0.7])
    with polys:
        poly_list = []
        poly_pais = []
        poly_ling = []
        with open(
            os.path.join("./base/" + st.session_state.poly_file), encoding="utf-8"
        ) as poly:
            for line in poly:
                poly_list.append(line)
                this_line = line.strip("\n")
                part_line = this_line.partition(" : ")
                poly_pais.append(translate(part_line[0]))
                poly_ling.append(part_line[2])
        poly.close()

        options = list(range(len(poly_list)))
        opt_poly = st.selectbox(
            "↓  lista: " + str(len(poly_list)) + " idiomas",
            options,
            index=st.session_state.poly_take,
            format_func=lambda x: poly_list[x],
            key="opt_poly",
        )

    with ok:
        doit = st.button("✔", help="confirm ?")

    lnew = True
    if st.session_state.vydo:
        lnew = False
        show_video("poly")
        update_readings("video_poly")
        st.session_state.vydo = False

    if doit:
        poly_pais = poly_pais[opt_poly]
        poly_ling = poly_ling[opt_poly]
        st.session_state.poly_name = translate(poly_pais)
        st.session_state.poly_lang = poly_ling
        st.session_state.poly_take = opt_poly

        st.session_state.last_lang = st.session_state.lang
        st.session_state.lang = st.session_state.poly_lang

    if lnew:
        poly_expander = st.expander("", True)
        with poly_expander:
            st.subheader(load_md_file("MANUAL_POLY.md"))


def page_abouts():
    abouts_list = [
        "comments",
        "prefácio",
        "machina",
        "off-machina",
        "outros",
        "traduttore",
        "bibliografia",
        "imagens",
        "samizdát",
        "notes",
        "license",
        "index",
    ]


    options = list(range(len(abouts_list)))
    sobrios = "↓  " + translate("sobre")
    opt_abouts = st.selectbox(
        sobrios,
        options,
        format_func=lambda x: abouts_list[x],
        key="opt_abouts",
    )

    lnew = True
    if st.session_state.vydo:
        lnew = False
        show_video("about")
        update_readings("video_about")
        st.session_state.vydo = False

    if lnew:
        choice = abouts_list[opt_abouts].upper()
        about_expander = st.expander("", True)
        with about_expander:
            if choice == "MACHINA":
                st.subheader(load_md_file("ABOUT_MACHINA_A.md"))
                LOGO_TEXTO = load_info(st.session_state.tema)
                LOGO_IMAGE = "./images/matrix/" + st.session_state.tema + ".jpg"
                write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
                st.subheader(load_md_file("ABOUT_MACHINA_D.md"))
            else:
                st.subheader(load_md_file("ABOUT_" + choice + ".md"))


### eof: pages

if __name__ == "__main__":
    main()
