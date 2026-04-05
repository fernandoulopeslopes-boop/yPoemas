import os
import re
import time
import random
import base64
import socket
import streamlit as st

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


# hide Streamlit Menu and Footer
st.markdown(
    """ <style>
    /*#MainMenu {visibility: hidden;}*/
    footer {visibility: hidden;}
    </style> """,
    unsafe_allow_html=True,
)


# change padding between components
st.markdown(
    """ <style>
    .reportview-container .main .block-container{
        padding-top: 0rem;
        padding-right: 0rem;
        padding-left: 0rem;
        padding-bottom: 0rem;
    } </style> """,
    unsafe_allow_html=True,
)


# change sidebar width
st.markdown(
    """ 
    <style>
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 310px;
    }
    </style> """,
    unsafe_allow_html=True,
)


# load_poema settings
st.markdown(
    """
    <style>
    mark {
      background-color: powderblue;
      color: black;
    }
    .container {
        display: flex;
        /* justify-content: center; */
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
    </style> """,
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
    b_pt = btn_pt.button("pt", key=1, help="Português")
    b_es = btn_es.button("es", key=2, help="Español")
    b_it = btn_it.button("it", key=3, help="Italiano")
    b_fr = btn_fr.button("fr", key=4, help="Français")
    b_en = btn_en.button("en", key=5, help="English")
    b_xy = btn_xy.button("⚒️", key=6, help=st.session_state.poly_name)

    if b_pt:
        st.session_state.lang = "pt"
        st.session_state.poly_file = "poly_pt.txt"
    elif b_es:
        st.session_state.lang = "es"
        st.session_state.poly_file = "poly_es.txt"
    elif b_it:
        st.session_state.lang = "it"
        st.session_state.poly_file = "poly_it.txt"
    elif b_fr:
        st.session_state.lang = "fr"
        st.session_state.poly_file = "poly_fr.txt"
    elif b_en:
        st.session_state.lang = "en"
        st.session_state.poly_file = "poly_en.txt"
    elif b_xy:
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


@st.cache_data
def load_help_tips():
    help_list = []
    with open(os.path.join("./base/helpers.txt"), encoding="utf-8") as file:
        for line in file:
            help_list.append(line)
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


def get_binary_file_downloader_html(bin_file, file_label="File"):
    with open(bin_file, "rb") as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">download {file_label}</a>'

    return href


def atoi(text):  # human reading number functions for sorting
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r"(\d+)", text)]


### eof: tools
### bof: update themes readings


def update_visy():  # count one more visitor
    path = os.path.join("./temp/visitors.txt")
    if not os.path.exists(path):
        with open(path, "w") as f: f.write("0")
    
    with open(path, "r", encoding="utf-8") as visitors:
        tots = int(visitors.read())
        tots = tots + 1
        st.session_state.nany_visy = tots

    with open(path, "w", encoding="utf-8") as visitors:
        visitors.write(str(tots))


def load_readings():
    readers_list = []
    path = os.path.join("./temp/read_list.txt")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as reader:
            for line in reader:
                readers_list.append(line)
    return readers_list


def update_readings(tema):
    read_changes = []
    readings = load_readings()
    found = False
    for line in readings:
        pipe_line = line.split("|")
        if len(pipe_line) > 1:
            name = pipe_line[1]
            if name == tema:
                qtds = int(pipe_line[2]) + 1
                new_line = "|" + name + "|" + str(qtds) + "|\n"
                read_changes.append(new_line)
                found = True
            else:
                read_changes.append(line)
    
    if not found:
        read_changes.append(f"|{tema}|1|\n")

    with open(os.path.join("./temp/read_list.txt"), "w", encoding="utf-8") as new_reader:
        for line in read_changes:
            new_reader.write(line)


def list_readings():
    sum_all_days = 0
    read_days = []  # days
    readings = load_readings()
    for line in readings:
        pipe_line = line.split("|")
        if len(pipe_line) > 2:
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
    days_of_runs = abs((begining_day - currrent_day).days)
    views_by_day = total_viewes / max(1, days_of_runs)
    reads_by_day = sum_all_days / max(1, total_viewes)

    options = list(range(len(read_days)))
    if options:
        st.selectbox(
            f"↓ {len(read_days)} temas, {sum_all_days} leituras por {total_viewes} visitantes ({int(views_by_day)} / {reads_by_day:.2})",
            options,
            format_func=lambda x: read_days[x],
            key="opt_readings",
        )


### eof: update themes readings
### bof: loaders


@st.cache_data
def load_md_file(file):  # Open files for about's
    try:
        with open(os.path.join("./md_files/" + file), encoding="utf-8") as file_to_open:
            file_text = file_to_open.read()
        if not "rol_" in file.lower():
            file_text = translate(file_text)
    except:
        file_text = "ooops... arquivo ( " + file + " ) não pode ser aberto."
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


@st.cache_data
def load_temas(book):  # List of themes inside a Book
    book_list = []
    with open(os.path.join("./base/rol_" + book + ".txt"), "r", encoding="utf-8") as file:
        for line in file:
            line = line.replace(" ", "")
            book_list.append(line.strip("\n"))
    return book_list


@st.cache_data
def load_info(nome_tema):
    with open(os.path.join("./base/info.txt"), "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("|"):
                pipe = line.split("|")
                if pipe[1].upper() == nome_tema.upper():
                    res = f"<br><br><br>Titulo: {nome_tema}<br>Gênero: {pipe[2]}<br>Imagem: {pipe[3]}<br>"
                    res += f"Versos: {pipe[4]}<br>Verbetes no texto: {pipe[5]}<br>Verbetes do Tema: {pipe[6]}<br>"
                    res += f"• Banco de Ítimos: {pipe[7]}<br>Análise: {pipe[8]}<br>Notação Científica: {pipe[9]}<br>"
                    return res
    return "nonono"


@st.cache_data
def load_index():  # Load indexes numbers for all themes
    index_list = []
    with open(os.path.join("./md_files/ABOUT_INDEX.md"), encoding="utf-8") as lista:
        for line in lista:
            index_list.append(line)
    return index_list


def load_lypo():
    lypo_text = ""
    lypo_user = "LYPO_" + IPAddres
    path = os.path.join("./temp/" + lypo_user)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as script:
            for line in script:
                lypo_text += line.strip() + "<br>"
    return lypo_text


def load_typo():
    typo_text = ""
    typo_user = "TYPO_" + IPAddres
    path = os.path.join("./temp/" + typo_user)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as script:
            for line in script:
                line = line.strip().replace(" >", "\n").replace("< ", "\n")
                line = line.replace(" br", "\n").replace("br ", "\n")
                line = line.replace("< <", ">").replace("> >", ">")
                typo_text += line + "<br>"
    return typo_text


def load_all_offs():
    return ["a_torre_de_papel", "linguafiada", "livro_vivo", "faz_de_conto", "um_romance", "quase_que_eu_Poesia", "segredo_público"]


def load_off_book(book):
    book_full = []
    full_name = os.path.join("./off_machina/", book) + ".Pip"
    if os.path.exists(full_name):
        with open(full_name, encoding="utf-8") as file:
            for line in file:
                if line.startswith("|"): book_full.append(line)
    return book_full


def load_book_pages(book):
    book_pages = []
    for line in book:
        if line.startswith("<EOF>"): break
        if line.startswith("|"):
            pipe_line = line.split("|")
            book_pages.append(pipe_line[1])
    return book_pages


def load_poema(nome_tema, seed_eureka):
    script = gera_poema(nome_tema, seed_eureka)
    novo_ypoema = ""
    lypo_user = "LYPO_" + IPAddres
    if not os.path.exists("./temp"): os.makedirs("./temp")
    with open(os.path.join("./temp/" + lypo_user), "w", encoding="utf-8") as save_lypo:
        save_lypo.write(nome_tema + "\n")
        for line in script:
            if line == "\n":
                save_lypo.write("\n")
                novo_ypoema += "<br>"
            else:
                save_lypo.write(line + "\n")
                novo_ypoema += line + "<br>"
    return novo_ypoema


@st.cache_data
def load_images():
    images_list = []
    with open(os.path.join("./base/images.txt"), encoding="utf-8") as lista:
        for line in lista: images_list.append(line)
    return images_list


def load_arts(nome_tema):
    path = "./images/machina/"
    path_list = load_images()
    for line in path_list:
        if line.startswith(nome_tema):
            part_line = line.strip().partition(" : ")
            if nome_tema == part_line[0]:
                path = "./images/" + part_line[2] + "/"
                break
    
    arts_list = [f for f in os.listdir(path) if f.endswith(".jpg")]
    if not arts_list: return None
    
    image = random.choice(arts_list)
    if image in st.session_state.arts:
        image = random.choice(arts_list)
    
    st.session_state.arts.append(image)
    if len(st.session_state.arts) > 36: del st.session_state.arts[0]
    return path + image


### eof: loaders
### bof: functions

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    if LOGO_IMAGE == None:
        st.markdown(f"<div class='container'><p class='logo-text'>{LOGO_TEXTO}</p></div>", unsafe_allow_html=True)
    else:
        with open(LOGO_IMAGE, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""<div class='container'>
                <img class='logo-img' src='data:image/jpg;base64,{data}'>
                <p class='logo-text'>{LOGO_TEXTO}</p>
            </div>""", unsafe_allow_html=True)


def talk(text):
    text = text.replace("<br>", "\n").replace("< br>", "").replace("<br >", "")
    tts = gTTS(text=text, lang=st.session_state.lang, slow=False)
    file_name = os.path.join(f"./temp/audio{random.randint(1, 20000000)}.mp3")
    tts.save(file_name)
    with open(file_name, "rb") as f:
        st.audio(f.read(), format="audio/ogg")
    os.remove(file_name)


def show_video(pagina):
    st.sidebar.info(load_md_file("INFO_VYDE.md"))
    video_name = os.path.join("./base/" + "video_" + pagina + ".webm")
    if os.path.exists(video_name):
        with open(video_name, "rb") as f:
            st.video(f.read(), format="webm")


def say_number(tema):
    indexes = load_index()
    for line in indexes:
        if line.startswith(tema):
            return translate(line.strip().partition(" : ")[2])
    return "nonono"

### eof: functions
### bof: pages

if st.session_state.visy:
    update_visy()
    temas_l = load_temas(st.session_state.book)
    st.session_state.take = random.randrange(0, len(temas_l))
    st.session_state.mini = random.randrange(0, len(load_temas("todos os temas")))
    st.success(translate("bem vindo à **máquina de fazer Poesia...**"))
    st.session_state.draw = True
    st.session_state.visy = False

st.session_state.last_lang = st.session_state.lang

def page_mini():
    temas_list = load_temas("todos os temas")
    maxy_mini = len(temas_list)
    if st.session_state.mini >= maxy_mini: st.session_state.mini = 0

    foo1, more, rand_btn, auto_chk, foo2 = st.columns([4, 1, 1, 1, 4])
    tips = load_help(st.session_state.lang)
    r_pressed = rand_btn.button("✻", help=tips[1])
    st.session_state.auto = auto_chk.checkbox("auto")

    if st.session_state.auto:
        st.session_state.talk = st.session_state.vydo = False
        wait_time = st.sidebar.slider(translate("tempo de exibição (em segundos): "), 5, 60)

    if r_pressed:
        st.session_state.rand = True
        st.session_state.mini = random.randrange(0, maxy_mini)
    else:
        st.session_state.rand = False

    st.session_state.tema = temas_list[st.session_state.mini]
    analise = say_number(st.session_state.tema)
    m_pressed = more.button("✚", help=tips[4] + " • " + analise)

    if m_pressed: st.session_state.rand = False

    lnew = True
    if st.session_state.vydo:
        lnew = False
        show_video("mini")
        update_readings("video_mini")
        st.session_state.vydo = False

    if lnew or st.session_state.auto:
        mini_placeholder = st.empty()
        
        while True:
            if st.session_state.rand:
                st.session_state.mini = random.randrange(0, maxy_mini)
                st.session_state.tema = temas_list[st.session_state.mini]

            if st.session_state.lang != st.session_state.last_lang:
                curr_ypoema = load_lypo()
            else:
                load_poema(st.session_state.tema, "")
                curr_ypoema = load_lypo()

            if st.session_state.lang != "pt":
                curr_ypoema = translate(curr_ypoema)
                with open(os.path.join(f"./temp/TYPO_{IPAddres}"), "w", encoding="utf-8") as f:
                    f.write(curr_ypoema)
                curr_ypoema = load_typo()

            update_readings(st.session_state.tema)
            img = load_arts(st.session_state.tema) if st.session_state.draw else None
            
            with mini_placeholder.container():
                write_ypoema(curr_ypoema, img)
            
            if st.session_state.talk: talk(curr_ypoema)
            
            if not st.session_state.auto: break
            time.sleep(wait_time)

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list) - 1
    if st.session_state.take > maxy: st.session_state.take = 0

    f1, more, last, rand, nest, manu, f2 = st.columns([3, 1, 1, 1, 1, 1, 3])
    tips = load_help(st.session_state.lang)
    
    if more.button("✚", help=tips[4]): pass
    if last.button("◀", help=tips[0]):
        st.session_state.take = maxy if st.session_state.take <= 0 else st.session_state.take - 1
    if rand.button("✻", help=tips[1]):
        st.session_state.take = random.randrange(0, maxy)
    if nest.button("▶", help=tips[2]):
        st.session_state.take = 0 if st.session_state.take >= maxy else st.session_state.take + 1
    m_clicked = manu.button("?", help="help !!!")

    if not st.session_state.draw:
        st.session_state.take = st.selectbox("↓ " + translate("lista de Temas"), range(len(temas_list)), index=st.session_state.take, format_func=lambda z: temas_list[z])

    st.session_state.tema = temas_list[st.session_state.take]
    
    if m_clicked: st.subheader(load_md_file("MANUAL_YPOEMAS.md"))
    if st.session_state.vydo:
        show_video("ypoemas")
        update_readings("video_ypoemas")
        st.session_state.vydo = False

    with st.expander(f"⚫ {st.session_state.lang} ({st.session_state.book}) ({st.session_state.take + 1}/{len(temas_list)})", expanded=True):
        if st.session_state.lang != st.session_state.last_lang:
            curr = load_lypo()
        else:
            load_poema(st.session_state.tema, "")
            curr = load_lypo()
        
        if st.session_state.lang != "pt":
            curr = translate(curr)
            with open(os.path.join(f"./temp/TYPO_{IPAddres}"), "w", encoding="utf-8") as f: f.write(curr)
            curr = load_typo()

        update_readings(st.session_state.tema)
        img = load_arts(st.session_state.tema) if st.session_state.draw else None
        write_ypoema(curr, img)

        if m_clicked:
            info = load_info(st.session_state.tema)
            if st.session_state.lang != "pt": info = translate(info)
            write_ypoema(info, f"./images/matrix/{st.session_state.tema.capitalize()}.jpg")

    if st.session_state.talk: talk(curr)

def page_eureka():
    tips = load_help(st.session_state.lang)
    seed_col, more_col, rand_col, manu_col, occ_col = st.columns([2.5, 1.5, 1.5, 0.7, 4])
    find_what = seed_col.text_input(label=translate("digite algo para buscar..."))
    m_p = more_col.button("✚", help=tips[4])
    r_p = rand_col.button("✻", help=tips[1])
    h_p = manu_col.button("?", help="help !!!")

    if h_p: st.subheader(load_md_file("MANUAL_EUREKA.md"))
    if len(find_what) < 3:
        st.warning(translate("digite pelo menos 3 letras..."))
    else:
        eureka_list = load_eureka(find_what)
        seed_list = [line.strip().partition(" : ")[0] + " ➪ " + line.strip().partition(" : ")[2] for line in eureka_list]
        
        if not (m_p or h_p): st.session_state.eureka = 0
        if not seed_list:
            st.warning(translate(f'nenhuma ocorrência de "{find_what}" encontrada...'))
        else:
            seed_list.sort()
            if r_p: st.session_state.eureka = random.randrange(0, len(seed_list))
            st.session_state.eureka = occ_col.selectbox(f"↓ {len(seed_list)} ocorrências", range(len(seed_list)), index=st.session_state.eureka, format_func=lambda y: seed_list[y])
            
            st.session_state.tema = seed_list[st.session_state.eureka].partition(" ➪ ")[2][:-5]
            # ... resto da lógica segue o padrão de exibição
