r"""

yPoemas is an app that randomly collects words and phrases
from specific databases and organizes them
in different new poems or poetic texts.

All texts are unique and will only be repeated  
after they are sold out the thourekasands  
of combinations possible to each theme.

[Epitaph]
Passei boa parte da minha vida escrevendo a "machina".
A leitura fica para os amanhãs.
Não vivo no meu tempo.

º¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°

ツpoemas

AlfaBetaAção == C:\WINDOWS\new.ini
config.toml  == C:\Users\dkvece\.streamlit

share : https://share.streamlit.io/
deploy: https://share.streamlit.io/nandoulopes/ypoemas/main/ypo.py
runnin: https://nandoulopes-ypoemas-ypo-gf4z3l.streamlitapp.com/
config: chrome://settings/content/siteDetails?site=https%3A%2F%2Fauth.streamlit.io
github: https://github.com/NandouLopes/yPoemas
instag: https://www.instagram.com/maquina_de_fazer_ypoemas/
youtub: https://youtu.be/uL6T3roTtAs
google: https://console.cloud.google.com/welcome?project=ypoemas&cloudshell=false
prosas: https://prosas.com.br/dashboards/my-proposals
bairro: https://www.superbairro.com.br/joseense-cria-maquina-de-produzir-poemas-2/

para novos temas:
- incluir novo_tema em \ypo\base\ativos.txt
- incluir novo_tema em \ypo\base\images.txt
- incluir novo_tema em \ypo\temp\readings.txt
- incluir novo_tema em \base\rol_*.txt
- atualizar ABOUT_NOTES.md se necessário...

VISY == New Visitor
NANY_VISY == Number of Visitors
LYPO == Last YPOema created from curr_ypoema
TYPO == Translated YPOema from LYPO
POLY == Poliglot Idiom == Changed on Catalán

"""
# =================================================================
# 🚀 BLOCO DE IGNIÇÃO: MACHINA DE FAZER POESIA (ABNP)
# =================================================================
import streamlit as st
import os
import re
import random
import time
from datetime import datetime
from PIL import Image
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64

# 1. CONFIGURAÇÃO DE INTERFACE (DEVE SER O PRIMEIRO COMANDO ST)
st.set_page_config(
    page_title="Machina de fazer Poesia",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INICIALIZAÇÃO DO ESTADO (PROTEÇÃO CONTRA "BAD MESSAGE FORMAT")
if 'initialized' not in st.session_state:
    # Estados de Identidade
    st.session_state.lang = 'pt'
    st.session_state.last_lang = 'pt'
    st.session_state.tema = 'lazer'
    
    # Estados de Navegação
    st.session_state.eureka = 0
    st.session_state.show_eureka = True
    
    # Estados de Percepção (Toggle Switches)
    st.session_state.talk = False
    st.session_state.draw = True
    st.session_state.vydo = False
    
    # Trava de Segurança
    st.session_state.initialized = True

# 3. CARREGAMENTO DO LÉXICO (41.291 VERBETES EM CACHE)
@st.cache_resource
def load_eureka_database():
    caminho_lexico = os.path.join("base", "lexico.pt")
    if os.path.exists(caminho_lexico):
        try:
            with open(caminho_lexico, "r", encoding="utf-8") as f:
                # Carrega e limpa, ignorando linhas vazias
                return [linha.strip() for linha in f if " : " in linha]
        except Exception:
            return []
    return []

# 4. CARREGAMENTO DE TRADUÇÕES E AJUDA (CACHE DE DADOS)
@st.cache_data
def load_help_system(lang):
    help_list = []
    with open(os.path.join("./base/helpers.txt"), encoding="utf-8") as file:
        for line in file:
            help_list.append(line)
    file.close()

    return help_list
    pass

# =================================================================
# 🛠️ FIM DO BLOCO OBRIGATÓRIO - O CÓDIGO SEGUE ABAIXO
# =================================================================        

# --- TRATAMENTO DE ÁUDIO E MULTIMÍDIA ---
import pygame           # Para o controle fino de áudio (Mixer)
import edge_tts         # Para vozes neurais de alta qualidade
import asyncio          # Necessário para rodar o edge-tts (que é assíncrono)

# --- COMUNICAÇÃO E SISTEMA ---
import requests         # Para buscar dados externos ou APIs
import json             # Para manipular arquivos de configuração ou Rols
import glob             # Para localizar arquivos de imagem/poema nas pastas
import shutil           # Para limpeza de arquivos temporários na pasta /temp/

# --- GRÁFICOS E COMPONENTES DE INTERFACE ---
import matplotlib.pyplot as plt # Se for usar visualização de dados do léxico
import extra_streamlit_components as stx # Para os componentes extras (seletor de abas, etc.)
from PIL import Image, ImageDraw, ImageFont # Para manipulação avançada de artes

# --- GESTÃO DE REDE (IP) ---
import socket           # Útil para gerar o ID temporário (IPAddres) que você usa

def main():
    if "book_list" not in st.session_state:
        
        # 1. Carrega o Rol Vivo
        book_list = []
        caminho_rol = "./base/rol_livro vivo.txt"
        
        if os.path.exists(caminho_rol):
            with open(caminho_rol, "r", encoding="utf-8") as file:
                for line in file:
                    tema_limpo = line.replace(" ", "").strip()
                    if tema_limpo:
                        book_list.append(tema_limpo)
            st.session_state.book_list = book_list
        else:
            # Caso o arquivo não seja encontrado
            st.session_state.book_list = ["Fatos", "Saudades", "Oficio"]

        # 2. Define o Tema Inicial Aleatório
        if "tema" not in st.session_state:
            st.session_state.tema = random.choice(st.session_state.book_list)

        # 3. Enche o tanque com o primeiro yPoema
        if "curr_ypoema" not in st.session_state:
            st.session_state.curr_ypoema = load_poema(st.session_state.tema, "")
            st.session_state.trad_ypoema = "" # Tanque de tradução limpo

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
    except ImportError:
        st.warning("Google Translator não encontrado no ambiente...")
    
    try:
        import edge_tts
        import asyncio
        # O gTTS não é mais estritamente necessário se usarmos o Edge, 
        # mas se quiser mantê-lo como "plano B", pode deixar aqui.
    except ImportError:
        st.warning("Motor de voz neural (edge-tts) não conectado.")
else:
    st.warning("Internet não conectada. Traduções e Vozes Neurais indisponíveis.")
    
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
# --- INÍCIO DO BLOCO REPARADO ---
# --- COPIE EXATAMENTE DAQUI ---
st.markdown("""
<style>
.logo-text {
    font-weight: 600;
    font-size: 18px;
    font-family: 'IBM Plex Sans', sans-serif;
    color: #000000;
    padding-left: 15px;
    text-align: left;
    display: block;
    line-height: 1.6;
    white-space: pre-wrap !important;
}
.logo-img {
    float: right;
    max-width: 300px;
    margin-left: 15px;
}
</style>
""", unsafe_allow_html=True)
# --- ATÉ AQUI ---# Initialize SessionState

if "lang" not in st.session_state:
    st.session_state.lang = "pt"
if "last_lang" not in st.session_state:
    st.session_state.last_lang = "pt"

if "curr_ypoema" not in st.session_state:
    st.session_state.curr_ypoema = ""      # O Original (Matriz)
if "trad_ypoema" not in st.session_state:
    st.session_state.trad_ypoema = ""      # O Traduzido (Reserva)
    
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

if "eureka" not in st.session_state:  #  index for random tema in 
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
        return translate("Arquivo muito grande para ser traduzido.")


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


@st.cache_data(show_spinner=False)
def update_visy():  # count one more visitor
    with open(os.path.join("./temp/visitors.txt"), "r", encoding="utf-8") as visitors:
        tots = int(visitors.read())
        tots = tots + 1
        st.session_state.nany_visy = tots

    with open(os.path.join("./temp/visitors.txt"), "w", encoding="utf-8") as visitors:
        visitors.write(str(tots))

    visitors.close()


@st.cache_data(show_spinner=False)
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


@st.cache_data(show_spinner=False)
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


@st.cache_data(show_spinner=False)
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


@st.cache_data(show_spinner=False)
def load_temas(book):  # List of themes inside a Book
    book_list = []
    with open(
        os.path.join("./base/rol_" + book + ".txt"), "r", encoding="utf-8"
    ) as file:
        for line in file:
            line = line.replace(" ", "")
            book_list.append(line.strip("\n"))

    return book_list


@st.cache_data(show_spinner=False)
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


@st.cache_data(show_spinner=False)
def load_index():  # Load indexes numbers for all themes
    index_list = []
    with open(os.path.join("./md_files/ABOUT_INDEX.md"), encoding="utf-8") as lista:
        for line in lista:
            index_list.append(line)

    return index_list


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
    
    # 1. Transformamos a lista de versos em um texto único com quebras de linha
    novo_ypoema = "\n".join(script)
    
    # 2. Debug para o Comandante ver que o combustível está saindo
    # st.write(f"Debug Interno: {nome_tema} - Gerado com Sucesso!") 

    # 3. A PEÇA CHAVE: Retornar o texto para a memória (st.session_state)
    return novo_ypoema
    
@st.cache_data(show_spinner=False)
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

        
def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    # Garante que o texto nunca seja None para o Markdown
    texto_final = LOGO_TEXTO if LOGO_TEXTO else "Gerando versos..."
    
    if LOGO_IMAGE is None or not os.path.exists(LOGO_IMAGE):
        # Saída apenas texto se a imagem falhar ou não existir
        st.markdown(f"<div class='container'><p class='logo-text'>{texto_final}</p></div>", unsafe_allow_html=True)
    else:
        try:
            with open(LOGO_IMAGE, "rb") as img_file:
                img_b64 = base64.b64encode(img_file.read()).decode()
            st.markdown(
                f"""
                <div class='container'>
                    <img class='logo-img' src='data:image/jpg;base64,{img_b64}'>
                    <p class='logo-text'>{texto_final}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception:
            # Fallback total: se até o base64 der erro, mostra só o texto
            st.markdown(f"<p class='logo-text'>{texto_final}</p>", unsafe_allow_html=True)


def talk(text):
    # Limpeza para a voz não ler tags
    text_clean = text.replace("<br>", " ").replace("< br>", "").replace("<br >", "").replace("<br/>", " ")
    
    # Mapeamento de vozes neurais de alta qualidade
    voices = {
        "pt": "pt-BR-FranciscaNeural",
        "en": "en-US-GuyNeural",
        "es": "es-ES-AlvaroNeural",
        "fr": "fr-FR-RemyNeural",
        "it": "it-IT-DiegoNeural"
    }
    selected_voice = voices.get(st.session_state.lang, "pt-BR-AntonioNeural")

    async def generate_audio():
        communicate = edge_tts.Communicate(text_clean, selected_voice)
        audio_bytes = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes += chunk["data"]
        return audio_bytes

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_output = loop.run_until_complete(generate_audio())
        st.audio(audio_output, format="audio/mp3")
    except Exception as e:
        st.error(f"Erro na voz neural: {e}")
        
    
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

    if st.session_state.mini >= maxy_mini: 
        st.session_state.mini = 0

    foo1, more_col, rand_col, auto_col, foo2 = st.columns([4, 1, 1, 1, 4])

    help_tips = load_help(st.session_state.lang)
    help_rand = help_tips[1]
    help_more = help_tips[4]
    
    btn_rand = rand_col.button("✻", help=help_rand)
    st.session_state.auto = auto_col.checkbox("auto")

    if st.session_state.auto:
        st.session_state.talk = False
        st.session_state.vydo = False
        with st.sidebar:
            wait_time = st.slider(translate("tempo de exibição (em segundos): "), 5, 60)

    if btn_rand:
        st.session_state.rand = True
        st.session_state.mini = random.randrange(0, maxy_mini)
    else:
        st.session_state.rand = False

    st.session_state.tema = temas_list[st.session_state.mini]
    analise = say_number(st.session_state.tema)
    btn_more = more_col.button("✚", help=help_more + " • " + analise)

    if btn_more:
        st.session_state.rand = False

    # --- LÓGICA DE GERAÇÃO DO POEMA ---
    # Só carregamos se for novo ou se mudou o idioma
    if st.session_state.lang != st.session_state.last_lang:
        curr_ypoema = load_poema(st.session_state.tema, "")
    else:
        curr_ypoema = load_poema(st.session_state.tema, "")

    # Tradução se necessário
    if st.session_state.lang != "pt":
        curr_ypoema = translate(curr_ypoema)

    # --- NORMALIZAÇÃO DAS QUEBRAS DE LINHA (A solução do osso duro!) ---
    if curr_ypoema:
        linhas = [l.strip() for l in curr_ypoema.split('\n')]
        LOGO_TEXTO = "  \n".join(linhas) # Dois espaços para o Markdown
    else:
        LOGO_TEXTO = "Gerando versos..."

    # --- ARTE / IMAGEM ---
    LOGO_IMAGE = None
    if st.session_state.draw:
        LOGO_IMAGE = load_arts(st.session_state.tema)

    # --- EXIBIÇÃO ---
    mini_place_holder = st.empty()
    
    if not st.session_state.auto:
        with mini_place_holder:
            write_ypoema(LOGO_TEXTO, LOGO_IMAGE)
        if st.session_state.talk:
            talk(curr_ypoema)
    else:
        # Loop do Modo Auto (Simplificado)
        while st.session_state.auto:
            st.session_state.mini = random.randrange(0, maxy_mini)
            st.session_state.tema = temas_list[st.session_state.mini]
            
            p_auto = load_poema(st.session_state.tema, "")
            if st.session_state.lang != "pt":
                p_auto = translate(p_auto)
            
            texto_auto = "  \n".join([l.strip() for l in p_auto.split('\n')])
            img_auto = load_arts(st.session_state.tema) if st.session_state.draw else None
            
            with mini_place_holder:
                write_ypoema(texto_auto, img_auto)
            
            time.sleep(wait_time)
            st.rerun() # Para atualizar o tema na próxima rodada

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy_ypoemas = len(temas_list) - 1
    if (st.session_state.take > maxy_ypoemas or st.session_state.take < 0):
        st.session_state.take = 0

    foo1, more, last, rand, nest, manu, foo2 = st.columns([3, 1, 1, 1, 1, 1, 3])

    help_tips = load_help(st.session_state.lang)
    help_last, help_rand, help_nest = help_tips[0], help_tips[1], help_tips[2]
    help_more = help_tips[4]

# Botões com IDs únicos para a página Ypoemas
    more_btn = more.button("✚", help=help_more, key="btn_more_ypo")
    last_btn = last.button("◀", help=help_last, key="btn_last_ypo")
    rand_btn = rand.button("✻", help=help_rand, key="btn_rand_ypo")
    nest_btn = nest.button("▶", help=help_nest, key="btn_nest_ypo")
    manu_btn = manu.button("?", help="help !!!", key="btn_manu_ypo")

    # Agora ajuste os "ifs" logo abaixo para usar os novos nomes:
    if last:
        st.session_state.take -= 1
        if st.session_state.take < 0: st.session_state.take = maxy_ypoemas
        st.rerun()

    if rand_btn:
        st.session_state.take = random.randrange(0, maxy_ypoemas)
        st.rerun()

    if nest_btn:
        st.session_state.take += 1
        if st.session_state.take > maxy_ypoemas: st.session_state.take = 0
        st.rerun()

    if rand_btn:
        st.session_state.take = random.randrange(0, maxy_ypoemas)
        st.rerun()

    if not st.session_state.draw:
        options = list(range(len(temas_list)))
        opt_take = st.selectbox("↓ " + translate("lista de Temas"), options, index=st.session_state.take, format_func=lambda z: temas_list[z])
        if opt_take != st.session_state.take:
            st.session_state.take = opt_take
            st.rerun()

    st.session_state.tema = temas_list[st.session_state.take]
    lnew = True

    if manu_btn:
        st.subheader(load_md_file("MANUAL_YPOEMAS.md"))

    if st.session_state.vydo:
        lnew = False
        show_video("ypoemas")
        update_readings("video_ypoemas")
        st.session_state.vydo = False

    if lnew:
        what_book = f"⚫ {st.session_state.lang} ( {st.session_state.book} ) ( {st.session_state.take + 1} / {len(temas_list)} )"
        
        with st.expander(what_book, expanded=True):
            if st.session_state.lang != st.session_state.last_lang:
                raw_text = translate(st.session_state.curr_ypoema)
            else:
                raw_text = load_poema(str(st.session_state.tema), "")
                st.session_state.curr_ypoema = raw_text

            update_readings(st.session_state.tema)

            if raw_text:
                linhas_formatadas = []
                for l in raw_text.split('\n'):
                    linha_limpa = l.lstrip().strip()
                    if not linha_limpa:
                        linhas_formatadas.append("&nbsp;")
                    else:
                        linhas_formatadas.append(linha_limpa)
                texto_formatado = "<br>".join(linhas_formatadas)
            else:
                texto_formatado = "Gerando versos..."

            imagem_carregada = load_arts(st.session_state.tema) if st.session_state.draw else None
            write_ypoema(texto_formatado, imagem_carregada)

            if st.session_state.talk:
                talk(raw_text)
            
            if manu_btn:
                info_txt = load_info(st.session_state.tema)
                st.info(translate(info_txt) if st.session_state.lang != "pt" else info_txt)

# --- FIM DA YPOEMAS / INÍCIO DA EUREKA ---

import streamlit as st
import re

def page_eureka():
    # 1. SETUP DE DICAS E COLUNAS (Layout Original)
    help_tips = load_help(st.session_state.lang)
    seed_col, more_col, rand_col, manu_col, occurrences_col = st.columns([2.5, 1.5, 1.5, 0.7, 4])

    with seed_col:
        find_what = st.text_input(label=translate("digite algo para buscar..."), label_visibility="collapsed")

    with more_col: more = st.button("✚", help=help_tips[4])
    with rand_col: rand = st.button("✻", help=help_tips[1])
    with manu_col: manu = st.button("?", help="help !!!")

    if len(find_what) < 3:
        st.warning(translate("digite pelo menos 3 letras..."))
        return

    # 2. MOTOR DE BUSCA E PROCESSAMENTO
    eureka_list = load_eureka(find_what)
    seed_list = []
    soma_tema = []

    for line in eureka_list:
        part_line = line.strip().partition(" : ")
        palas, fonte = part_line[0], part_line[2]
        if palas and fonte:
            seed_list.append(f"{palas} ➪ {fonte}")
            tema_nome = fonte[0:-5]
            if tema_nome not in soma_tema:
                soma_tema.append(tema_nome)

    if not seed_list:
        st.warning(translate(f'nenhuma ocorrência de "{find_what}" encontrada...'))
        return

    seed_list.sort()
    if rand:
        st.session_state.eureka = random.randrange(0, len(seed_list))

    # 3. SELETOR DE OCORRÊNCIAS (Topo Direito)
    with occurrences_col:
        info_find = f"{len(seed_list)} ocorrências de '{find_what}' em {len(soma_tema)} temas"
        opt_ocur = st.selectbox(
            "↓ " + translate(info_find),
            range(len(seed_list)),
            index=st.session_state.eureka if st.session_state.eureka < len(seed_list) else 0,
            format_func=lambda y: seed_list[y],
            key="opt_ocur"
        )
        st.session_state.eureka = opt_ocur

    # 4. CARGA DO TEXTO
    this_seed = seed_list[st.session_state.eureka]
    seed_tema = this_seed.partition(" ➪ ")[2][0:-5]
    st.session_state.tema = seed_tema
    
    # Carrega o poema bruto (PT)
    curr_ypoema = load_poema(seed_tema, this_seed)

    # 5. APRESENTAÇÃO CORRIGIDA (O Ponto da Crítica)
    # Título do yPoema no topo esquerdo da área de texto
    st.write(f"### {this_seed}") 
    
    # Expander para Hide/Show (com a setinha à direita)
    with st.expander("", expanded=True):
        # Tradução e Normalização de Fonte (Bloco Único)
        if st.session_state.lang != "pt":
            curr_ypoema = translate(curr_ypoema) # Aqui gera o TYPO
        
        # APLICANDO O UNDERLINE (HTML puro para garantir o destaque)
        # Substituímos a semente por ela mesma dentro de <u></u>
        # Usamos flags=re.IGNORECASE para pegar "Amor" e "amor"
        texto_final = re.sub(f"({re.escape(find_what)})", r"<u>\1</u>", curr_ypoema, flags=re.IGNORECASE)

        # Exibição com fonte única (definida no write_ypoema ou markdown direto)
        # O unsafe_allow_html=True é essencial para o <u> funcionar
        st.markdown(f'<div style="font-family: monospace; font-size: 1.1em;">{texto_final}</div>', unsafe_allow_html=True)
        
        # Arte e Voz
        if st.session_state.draw:
            st.image(load_arts(seed_tema))
        if st.session_state.talk:
            talk(curr_ypoema)
            
# --- FIM DA EUREKA --- INÍCIO DA OFF_MACHINA

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
        "dát",
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

    pick_lang()
    draw_check_buttons()

    if chosen_id == "1":
        st.sidebar.info(load_md_file("INFO_MINI.md"))
        magy = "img_mini.jpg"
        page_mini()
    elif chosen_id == "2":
        st.sidebar.info(load_md_file("INFO_YPOEMAS.md"))
        magy = "img_ypoemas.jpg"
        page_ypoemas()
    elif chosen_id == "3":
        st.sidebar.info(load_md_file("INFO_EUREKA.md"))
        magy = "img_eureka.jpg"
        page_eureka()
    elif chosen_id == "4":
        st.sidebar.info(load_md_file("INFO_OFF-MACHINA.md"))
        magy = "img_off-machina.jpg"
        page_off_machina()
    elif chosen_id == "5":
        st.sidebar.info(load_md_file("INFO_BOOKS.md"))
        magy = "img_books.jpg"
        page_books()
    elif chosen_id == "6":
        st.sidebar.info(load_md_file("INFO_POLY.md"))
        magy = "img_poly.jpg"
        page_polys()
    elif chosen_id == "7":
        st.sidebar.info(load_md_file("INFO_ABOUT.md"))
        magy = "img_about.jpg"
        page_abouts()
        ##$ page_docs()

    with st.sidebar:
        st.image(magy)

    show_icons()
    ##$ st.sidebar.state = True


if __name__ == "__main__":
    main()

