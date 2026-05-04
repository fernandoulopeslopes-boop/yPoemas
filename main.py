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

### eof: update themes readings
### bof: loaders


# @st.cache(allow_output_mutation=True)
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


# @st.cache(allow_output_mutation=True)
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


# @st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_temas(book):  # List of themes inside a Book
    book_list = []
    with open(
        os.path.join("./base/rol_" + book + ".txt"), "r", encoding="utf-8"
    ) as file:
        for line in file:
            line = line.replace(" ", "")
            book_list.append(line.strip("\n"))

    return book_list


# @st.cache(allow_output_mutation=True)
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


# @st.cache(allow_output_mutation=True)
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
        "quase_que_eu_Poesia",
        "faz_de_conto",
        "um_romance",
        "linguafiada",
        "livro_vivo",
        "desvoto",
        "ensaio",
        "urbano",
        "essencial",
        "secreto",
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
