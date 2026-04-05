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

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)


def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        return False


if have_internet():
    try:
        from deep_translator import GoogleTranslator
    except ImportError as ex:
        st.warning("Google Translator não conectado")
    try:
        from gtts import gTTS
    except ImportError as ex:
        st.warning("Google TTS não conectado")
else:
    st.warning("Internet não conectada. Traduções não disponíveis no momento.")


# the User IPAddres for LYPO, TYPO
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)


# AJUSTE DE LAYOUT: SEPARAÇÃO E PALCO CENTRADO (Protocolo de Correção de Encavalamento)
st.markdown(
    """
    <style>
    /* 1. SEPARAÇÃO E LARGURA DA SIDEBAR */
    [data-testid="stSidebar"] {
        min-width: 310px;
        max-width: 310px;
    }

    /* 2. CENTRALIZAÇÃO DO PALCO E PREVENÇÃO DE SOBREPOSIÇÃO */
    .main .block-container {
        max-width: 850px;
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
        margin: auto;
    }

    /* 3. OCULTAR MENUS E RODAPÉ */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* 4. ESTILOS DE TEXTO E IMAGEM (MARK) */
    mark {
      background-color: powderblue;
      color: black;
    }
    .container {
        display: flex;
    }
    .header {
        text-align:center;
    }
    .logo-text {
        font-weight: 600;
        font-size: 18px;
        font-family: 'IBM Plex Sans';
        color: #000000;
        padding-top: 0px;
        padding-left: 15px;
    }
    .logo-img {
        float:right;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


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
        return "Arquivo muito grande para ser traduzido."


def pick_lang():  # define idioma
    btn_pt, btn_es, btn_it, btn_fr, btn_en, btn_xy = st.sidebar.columns(
        [1.1, 1.13, 1.04, 1.04, 1.17, 1.25]
    )
    btn_pt = btn_pt.button("pt", key=1, help="Português")
    btn_es = btn_es.button("es", key=2, help="Español")
    btn_it = btn_it.button("it", key=3, help="Italiano")
    btn_fr = btn_fr.button("fr", key=4, help="Français")
    btn_en = btn_en.button("en", key=5, help="English")
    btn_xy = btn_xy.button("⚒️", key=6, help=st.session_state.poly_name)

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

    if st.session_state.lang != st.session_state.last_lang:
        st.success(translate("idioma atual") + " ➪ " + st.session_state.lang)


def show_icons():  # https://api.whatsapp.com/
    with st.sidebar:
        st.sidebar.markdown(
            f"""
            <nav>
            <a href='https://www.facebook.com/nandoulopes' target='_blank'>• facebook</a> |
            <a href='mailto:lopes.fernando@hotmail.com' target='_blank'>e-mail</a> |
            <a href='https://www.instagram.com/fernando.lopes.942/' target='_blank'>instagram</a> |
            <a href='https://web.whatsapp.com/send?phone=+5512991368181' target='_blank'>whatsapp</a>
            </nav>
            """,
            unsafe_allow_html=True,
        )


def load_help_tips():
    help_list = []
    with open(os.path.join("./base/helpers.txt"), encoding="utf-8") as file:
        for line in file:
            help_list.append(line)
    file.close()

    return help_list


def load_help(idiom):
    returns = []
    if idiom in "_pt_es_it_fr_en":
        helpers = load_help_tips()
        for line in helpers:
            pipe_line = line.split("|")
            if pipe_line[1].startswith(idiom + "_"):
                text = pipe_line[2]
                returns.append(text)
    else:
        returns.append(translate("anterior"))
        returns.append(translate("escolhe tema ao acaso"))
        returns.append(translate("próximo"))
        returns.append(translate("mais lidos..."))
        returns.append(translate("gera novo yPoema"))
        returns.append(translate("imagem"))
        returns.append(translate("áudio"))
        returns.append(translate("vídeo"))

    return returns


def draw_check_buttons():
    draw_text, talk_text, vyde_text = st.sidebar.columns([3.8, 3.2, 3])
    help_tips = load_help(st.session_state.lang)
    help_draw = help_tips[5]
    help_talk = help_tips[6]
    help_vyde = help_tips[7]
    st.session_state.draw = draw_text.checkbox(
        help_draw, st.session_state.draw, key="draw_machina"
    )
    st.session_state.talk = talk_text.checkbox(
        help_talk, st.session_state.talk, key="talk_machina"
    )
    st.session_state.vydo = vyde_text.checkbox(
        help_vyde, st.session_state.vydo, key="vyde_machina"
    )


def atoi(text):  # human reading number functions for sorting
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r"(\d+)", text)]


### eof: tools
### bof: update themes readings


def update_visy():  # count one more visitor
    with open(os.path.join("./temp/visitors.txt"), "r", encoding="utf-8") as visitors:
        tots = int(visitors.read())
        tots = tots + 1
        st.session_state.nany_visy = tots

    with open(os.path.join("./temp/visitors.txt"), "w", encoding="utf-8") as visitors:
        visitors.write(str(tots))

    visitors.close()


def load_readings():
    readers_list = []
    with open(os.path.join("./temp/read_list.txt"), encoding="utf-8") as reader:
        for line in reader:
            readers_list.append(line)
    reader.close()

    return readers_list


def update_readings(tema):
    read_changes = []
    readings = load_readings()
    for line in readings:
        pipe_line = line.split("|")
        name = pipe_line[1]
        if name == tema:
            qtds = int(pipe_line[2]) + 1
            new_line = "|" + name + "|" + str(qtds) + "|\n"
            read_changes.append(new_line)
        else:
            read_changes.append(line)

    with open(
        os.path.join("./temp/read_list.txt"), "w", encoding="utf-8"
    ) as new_reader:
        for line in read_changes:
            new_reader.write(line)
    new_reader.close()


def list_readings():
    sum_all_days = 0
    read_days = []  # days
    readings = load_readings()
    for line in readings:
        pipe_line = line.split("|")
        name = pipe_line[1]
        qtds = pipe_line[2]
        sum_all_days += int(qtds)
        if qtds != "0":
            new_line = str(qtds) + " - " + name + "\n"
            read_days.append(new_line)

    read_days.sort(key=natural_keys, reverse=True)

    total_viewes = st.session_state.nany_visy
    currrent_day = datetime.now()
    begining_day = datetime(2021, 7, 6)
    days_of_runs = begining_day - currrent_day
    days_of_runs = abs(days_of_runs.days)
    views_by_day = total_viewes / days_of_runs
    reads_by_day = sum_all_days / total_viewes

    options = list(range(len(read_days)))
    st.selectbox(
        "↓  "
        + str(len(read_days))
        + " temas, "
        + str(sum_all_days)
        + " leituras por "
        + str(total_viewes)
        + " visitantes ( "
        + str(int(views_by_day))
        + " / "
        + f"{reads_by_day:.2}"
        + " )",
        options,
        format_func=lambda x: read_days[x],
        key="opt_readings",
    )


### eof: update themes readings
### bof: loaders


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


def load_eureka(part_of_word):
    lexico_list = []
    with open(os.path.join("./base/lexico_pt.txt"), encoding="utf-8") as lista:
        for line in lista:
            this_line = line.strip("\n")
            part_line = this_line.partition(" : ")
            palas = part_line[0]
            if part_of_word.lower() in palas.lower():
                lexico_list.append(line)

    return lexico_list


def load_temas(book):  # List of themes inside a Book
    book_list = []
    with open(
        os.path.join("./base/rol_" + book + ".txt"), "r", encoding="utf-8"
    ) as file:
        for line in file:
            line = line.replace(" ", "")
            book_list.append(line.strip("\n"))

    return book_list


def load_info(nome_tema):
    with open(os.path.join("./base/" + "info.txt"), "r", encoding="utf-8") as file:
        result = "nonono"
        for line in file:
            if line.startswith("|"):
                pipe = line.split("|")
                if pipe[1].upper() == nome_tema.upper():
                    genero = pipe[2]
                    imagem = pipe[3]
                    qtd_versos = pipe[4]
                    qtd_wordin = pipe[5]
                    qtd_lexico = pipe[6]
                    qtd_itimos = pipe[7]
                    qtd_analiz = pipe[8]
                    qtd_cienti = pipe[9]
                    result = "<br>"
                    result += "<br>"
                    result += "<br>"
                    result += "Titulo: " + nome_tema + "<br>"
                    result += "Gênero: " + genero + "  " + "<br>"
                    result += "Imagem: " + imagem + "  " + "<br>"
                    result += "Versos: " + qtd_versos + "  " + "<br>"
                    result += "Verbetes no texto: " + qtd_wordin + "  " + "<br>"
                    result += "Verbetes  do Tema: " + qtd_lexico + "  " + "<br>"
                    result += "• Banco de Ítimos: " + qtd_itimos + "  " + "<br>"
                    result += "Análise : " + qtd_analiz + "  " + "<br>"
                    result += "Notação Científica: " + qtd_cienti + "  " + "<br>"
                    result += "<br>"

        return result


def load_index():  # Load indexes numbers for all themes
    index_list = []
    with open(os.path.join("./md_files/ABOUT_INDEX.md"), encoding="utf-8") as lista:
        for line in lista:
            index_list.append(line)

    return index_list


def load_lypo():  # Load last yPoema & replace '\n' with '<br>' for translator returned text
    lypo_text = ""
    lypo_user = "LYPO_" + IPAddres
    with open(os.path.join("./temp/" + lypo_user), encoding="utf-8") as script:
        for line in script:
            line = line.strip()
            lypo_text += line + "<br>"

    return lypo_text


def load_typo():  # Load translated yPoema & clean translator returned bugs in text
    typo_text = ""
    typo_user = "TYPO_" + IPAddres
    with open(os.path.join("./temp/" + typo_user), encoding="utf-8") as script:
        for line in script:  # just 1 line
            line = line.strip()
            if " >" in line:
                line = line.replace(" >", "\n")
            elif "< " in line:
                line = line.replace("< ", "\n")
            elif " br " in line:
                line = line.replace(" br", "\n")
            elif "br " in line:
                line = line.replace("br ", "\n")
            elif " br" in line:
                line = line.replace(" br", "\n")
            line = line.replace("< <", ">")
            line = line.replace("> >", ">")
            typo_text += line + "<br>"

    return typo_text


def load_all_offs():
    all_books_off = [
        "a_torre_de_papel",
        "linguafiada",
        "livro_vivo",
        "faz_de_conto",
        "um_romance",
        "quase_que_eu_Poesia",
        "segredo_público",
    ]

    return all_books_off


def load_off_book(book):  # Load selected off_book
    book_full = []
    full_name = os.path.join("./off_machina/", book) + ".Pip"
    with open(full_name, encoding="utf-8") as file:
        for line in file:
            if line.startswith("|"):
                book_full.append(line)

    return book_full


def load_book_pages(book):  # Load Book pages for off_book
    book_pages = []
    for line in book:
        if line.startswith("<EOF>"):
            break

        if line.startswith("|"):  # only valid lines in PIP
            pipe_line = line.split("|")
            book_pages.append(pipe_line[1])

    return book_pages


def load_poema(nome_tema, seed_eureka):  # generate new yPoema
    script = gera_poema(nome_tema, seed_eureka)
    novo_ypoema = ""
    lypo_user = "LYPO_" + IPAddres

    with open(os.path.join("./temp/" + lypo_user), "w", encoding="utf-8") as save_lypo:
        save_lypo.write(
            nome_tema
        )  # include title of yPoema in first line for translations
        save_lypo.write("\n")

        for line in script:
            if line == "\n":
                save_lypo.write("\n")
                novo_ypoema += "<br>"
            else:
                save_lypo.write(line + "\n")
                novo_ypoema += line + "<br>"

    save_lypo.close()  # save last generated in LYPO

    return novo_ypoema


def load_images():
    images_list = []
    with open(os.path.join("./base/images.txt"), encoding="utf-8") as lista:
        for line in lista:
            images_list.append(line)

    return images_list


def load_arts(nome_tema):  # Select image for arts
    path = "./images/machina/"
    path_list = load_images()
    for line in path_list:
        if line.startswith(nome_tema):
            this_line = line.strip("\n")
            part_line = this_line.partition(" : ")
            if nome_tema == part_line[0]:
                path = "./images/" + part_line[2] + "/"
                break

    arts_list = []
    for file in os.listdir(path):
        if file.endswith(".jpg"):
            arts_list.append(file)

    sorte = random.randrange(0, len(arts_list))
    image = arts_list[sorte]

    if image in st.session_state.arts:  # insert new image
        while image in st.session_state.arts:
            sorte = random.randrange(0, len(arts_list))
            image = arts_list[sorte]
        st.session_state.arts.append(image)
        image = st.session_state.arts[-1]
    else:
        st.session_state.arts.append(image)

    if len(st.session_state.arts) > 36:  # remove first
        del st.session_state.arts[0]

    logo = path + image

    return logo


### eof: loaders
### bof: functions

        
def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):  # ver save_img.py
    if LOGO_IMAGE == None:
        st.markdown(
            f"""
            <div class='container'>
                <p class='logo-text'>{LOGO_TEXTO}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class='container'>
                <img class='logo-img' src='data:image/jpg;base64,{base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()}'>
                <p class='logo-text'>{LOGO_TEXTO}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def talk(text):  # text to speech( in session_state.lang )
    text = text.replace("<br>", "\n")
    text = text.replace("< br>", "")
    text = text.replace("<br >", "")

    tts = gTTS(text=text, lang=st.session_state.lang, slow=False)
    nany_file = random.randint(1, 20000000)
    file_name = os.path.join("./temp/" + "audio" + str(nany_file) + ".mp3")
    tts.save(file_name)
    audio_file = open(file_name, "rb")
    audio_byts = audio_file.read()
    st.audio(audio_byts, format="audio/ogg")
    audio_file.close()
    os.remove(file_name)


def show_video(pagina):  # vídeo-tutorial da página
    st.sidebar.info(load_md_file("INFO_VYDE.md"))
    video_name = os.path.join("./base/" + "video_" + pagina + ".webm")
    video_file = open(video_name, "rb")
    video_byts = video_file.read()
    st.video(video_byts, format="webm")
    video_file.close()


def say_number(tema):  # search index title for eureka
    analise = "nonono"
    indexes = load_index()
    for line in indexes:
        if line.startswith(tema):
            this_line = line.strip("\n")
            part_line = this_line.partition(" : ")
            analise = part_line[2]
            break

    return translate(analise)


### eof: functions
### bof: pages


if st.session_state.visy:  # check visitor once; rand initial temas
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

    if st.session_state.mini > maxy_mini:  # just in case
        st.session_state.mini = 0

    foo1, more, rand, auto, foo2 = st.columns([4, 1, 1, 1, 4])

    help_tips = load_help(st.session_state.lang)
    help_rand = help_tips[1]
    help_more = help_tips[4]
    rand = rand.button("✻", help=help_rand)
    st.session_state.auto = auto.checkbox("auto")

    if st.session_state.auto:
        st.session_state.talk = False
        st.session_state.vydo = False
        with st.sidebar:
            wait_time = st.slider(translate("tempo de exibição (em segundos): "), 5, 60)

    if rand:
        st.session_state.rand = True
        st.session_state.mini = random.randrange(0, maxy_mini)
    else:
        st.session_state.rand = False

    st.session_state.tema = temas_list[st.session_state.mini]
    analise = say_number(st.session_state.tema)
    more = more.button("✚", help=help_more + " • " + analise)

    if more:
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

        mini_place_holder = st.empty()
        mini_place_holder.empty()
        st.write("")

        if st.session_state.auto == False:
            with mini_place_holder:
                write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

            if st.session_state.talk:
                talk(curr_ypoema)

        else:
            while st.session_state.auto:
                if st.session_state.rand:
                    st.session_state.mini = random.randrange(0, maxy_mini)
                    st.session_state.tema = temas_list[st.session_state.mini]

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

                with mini_place_holder:
                    mini_place_holder.empty()
                    write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
                    secs = wait_time
                    while secs >= 0:
                        time.sleep(1)
                        secs -= 1


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


# Chamada da Interface
page_ypoemas()
