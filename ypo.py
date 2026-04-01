import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime
from lay_2_ypo import gera_poema

# Nota: Removi a linha 'from extra_streamlit_components import TabBar as stx' 
# para evitar o erro de deploy que vimos nos logs.

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
    f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {0}rem;
        padding-right: {0}rem;
        padding-left: {0}rem;
        padding-bottom: {0}rem;
    }} </style> """,
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
if "book" not in st.session_state:
    st.session_state.book = "livro vivo"
if "take" not in st.session_state:
    st.session_state.take = 0
if "mini" not in st.session_state:
    st.session_state.mini = 0
if "tema" not in st.session_state:
    st.session_state.tema = "Fatos"
if "off_book" not in st.session_state:
    st.session_state.off_book = 0
if "off_take" not in st.session_state:
    st.session_state.off_take = 0
if "eureka" not in st.session_state:
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
    if st.session_state.lang == "pt":
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
        return "Erro na tradução."

def pick_lang():
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
    elif btn_es:
        st.session_state.lang = "es"
    elif btn_it:
        st.session_state.lang = "it"
    elif btn_fr:
        st.session_state.lang = "fr"
    elif btn_en:
        st.session_state.lang = "en"
    elif btn_xy:
        st.session_state.lang = st.session_state.poly_lang

def show_icons():
    with st.sidebar:
        st.sidebar.markdown(
            f"""
            <nav>
            <a href='https://facebook.com' target='_blank'>facebook</a> |
            <a href='mailto:lopes.fernando@hotmail.com' target='_blank'>e-mail</a> |
            <a href='https://instagram.com' target='_blank'>instagram</a>
            </nav>
            """,
            unsafe_allow_html=True,
        )

@st.cache(allow_output_mutation=True)
def load_help_tips():
    help_list = []
    with open("./base/helpers.txt", encoding="utf-8") as file:
        for line in file:
            help_list.append(line)
    return help_list

def load_help(idiom):
    returns = []
    helpers = load_help_tips()
    for line in helpers:
        pipe_line = line.split("|")
        if pipe_line[1].startswith(idiom + "_"):
            returns.append(pipe_line[2])
    return returns

def draw_check_buttons():
    draw_text, talk_text, vyde_text = st.sidebar.columns([3.8, 3.2, 3])
    st.session_state.draw = draw_text.checkbox("imagem", st.session_state.draw)
    st.session_state.talk = talk_text.checkbox("áudio", st.session_state.talk)
    st.session_state.vydo = vyde_text.checkbox("vídeo", st.session_state.vydo)

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split(r"(\d+)", text)]

### bof: update themes readings

def update_visy():
    try:
        with open("./temp/visitors.txt", "r", encoding="utf-8") as visitors:
            tots = int(visitors.read()) + 1
        st.session_state.nany_visy = tots
        with open("./temp/visitors.txt", "w", encoding="utf-8") as visitors:
            visitors.write(str(tots))
    except:
        pass

def load_readings():
    readers_list = []
    with open("./temp/read_list.txt", encoding="utf-8") as reader:
        for line in reader:
            readers_list.append(line)
    return readers_list

def update_readings(tema):
    readings = load_readings()
    with open("./temp/read_list.txt", "w", encoding="utf-8") as new_reader:
        for line in readings:
            pipe_line = line.split("|")
            if pipe_line[1] == tema:
                qtds = int(pipe_line[2]) + 1
                new_reader.write(f"|{tema}|{qtds}|\n")
            else:
                new_reader.write(line)

### bof: loaders

def load_md_file(file):
    try:
        with open(f"./md_files/{file}", encoding="utf-8") as f:
            return f.read()
    except:
        return "Erro ao carregar arquivo."

def load_temas(book):
    book_list = []
    with open(f"./base/rol_{book}.txt", "r", encoding="utf-8") as file:
        for line in file:
            book_list.append(line.replace(" ", "").strip("\n"))
    return book_list

def load_lypo():
    lypo_text = ""
    lypo_user = f"LYPO_{IPAddres}"
    with open(f"./temp/{lypo_user}", encoding="utf-8") as script:
        for line in script:
            lypo_text += line.strip() + "<br>"
    return lypo_text

def load_poema(nome_tema, seed_eureka):
    script = gera_poema(nome_tema, seed_eureka)
    novo_ypoema = ""
    lypo_user = f"LYPO_{IPAddres}"
    with open(f"./temp/{lypo_user}", "w", encoding="utf-8") as save_lypo:
        save_lypo.write(nome_tema + "\n")
        for line in script:
            save_lypo.write(line + "\n")
            novo_ypoema += (line if line != "\n" else "") + "<br>"
    return novo_ypoema

def load_arts(nome_tema):
    # Lógica simplificada de seleção de imagem
    return "./images/default.jpg"

### bof: functions

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    if LOGO_IMAGE == None:
        st.markdown(f"<div class='container'><p class='logo-text'>{LOGO_TEXTO}</p></div>", unsafe_allow_html=True)
    else:
        img_data = base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()
        st.markdown(
            f"<div class='container'><img class='logo-img' src='data:image/jpg;base64,{img_data}'><p class='logo-text'>{LOGO_TEXTO}</p></div>",
            unsafe_allow_html=True
        )

def talk(text):
    if have_internet():
        clean_text = text.replace("<br>", "\n")
        tts = gTTS(text=clean_text, lang=st.session_state.lang)
        tts.save("./temp/speech.mp3")
        st.audio("./temp/speech.mp3")

### Paginação simplificada para teste de Deploy
def page_mini():
    st.title("LYPO - Mini")
    st.write(st.session_state.tema)
    if st.button("Gerar Poema"):
        poema = load_poema(st.session_state.tema, "")
        write_ypoema(poema, None)

# Navegação lateral simples (Substituindo a TabBar que causava erro)
pagina = st.sidebar.selectbox("Menu", ["Mini", "yPoemas", "Eureka"])

if pagina == "Mini":
    page_mini()
else:
    st.write("Em construção...")
    
