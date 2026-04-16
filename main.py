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
config.toml == C:\Users\dkvece\.streamlit

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

One more test...
"""

import re
import time
import random
import base64
import socket
import streamlit as st
from pathlib import Path
from random import randrange
from datetime import datetime

### bof: settings

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- [ PATHS SEGUROS ] ---
BASE_DIR = Path(__file__).parent
BASE = BASE_DIR / "base"
DATA = BASE_DIR / "data"
TEMP = BASE_DIR / "temp"
MD_FILES = BASE_DIR / "md_files"
IMAGES = BASE_DIR / "images"
OFF_MACHINA = BASE_DIR / "off_machina"

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
.reportview-container.main.block-container{{
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
### bof: MACHINA - GERADOR DE POEMA

@st.cache_data
def abre(nome_do_tema):
    """
    :param nome_do_tema
    :return: lista do arquivo
    """
    full_name = DATA / f"{nome_do_tema}.ypo"
    lista = []
    try:
        with open(full_name, encoding="utf-8") as file:
            for line in file:
                lista.append(line)
    except (FileNotFoundError, UnicodeDecodeError) as e:
        st.error(f"Arquivo {full_name} não encontrado ou com erro de encoding: {e}")
    return lista

@st.cache_data
def load_babel():
    lista = []
    try:
        with open(BASE / "babel.txt", "r", encoding="utf-8") as babel:
            for line in babel:
                lista.append(line.strip())
    except FileNotFoundError:
        st.warning("babel.txt não encontrado")
    return lista

@st.cache_data
def load_cidades():
    cidades = []
    try:
        with open(BASE / "fatos_cidades.txt", encoding="utf8") as file:
            for line in file:
                if line.strip():
                    cidades.append(line.strip())
    except FileNotFoundError:
        st.warning("fatos_cidades.txt não encontrado")
    return cidades

@st.cache_data
def load_abnp():
    lista = []
    full_name = BASE / "abnp.txt"
    try:
        with open(full_name, encoding="utf-8") as file:
            for line in file:
                alinhas = line.split("|")
                for item in alinhas:
                    item = item.strip()
                    if item:
                        lista.append(item)
    except FileNotFoundError:
        st.warning("abnp.txt não encontrado")
    return lista

def novo_babel(swap_pala):
    """
    :param swap_pala: quantas palavras por linhas no poema: 0 = rand; n = n-1 palavras
    :return: poema aleatório
    """
    lista_silabas = load_babel()
    sinais_ini = [".", ",", ":", "!", "?", "...", " "]
    sinais_end = [".", "!", "?", "..."]

    min_versos = 5
    max_versos = 15
    qtd_versos = random.randrange(min_versos, max_versos)

    sinal = "."
    novo_poema = []
    for nQtdLin in range(qtd_versos):
        novo_verso_babel = ""
        if swap_pala == 0:
            qtd_palas = random.randrange(3, 7)
        else:
            qtd_palas = swap_pala

        for nova_frase in range(qtd_palas):
            nova_pala = ""
            qtd_silabas = random.randrange(2, 4)
            for palavra in range(qtd_silabas):
                if lista_silabas:
                    njump = random.randrange(len(lista_silabas))
                    nova_silaba = str(lista_silabas[njump])
                    nova_pala += nova_silaba.strip()
            nova = nova_pala.replace("aa", "a")
            nova = nova.replace("ee", "e")
            nova = nova.replace("ii", "i")
            nova = nova.replace("uu", "u")
            novo_verso_babel += nova.strip() + " "

        if nQtdLin == 0:
            njump = random.randrange(len(sinais_ini))
            sinal = sinais_ini[njump]
            novo_poema.append("")
            novo_poema.append(novo_verso_babel.strip() + sinal)
        else:
            nany = random.randrange(100)
            if nany <= 50:
                njump = random.randrange(len(sinais_ini))
                sinal = sinais_ini[njump]
                novo_verso_babel = novo_verso_babel.rstrip() + sinal
            novo_poema.append(novo_verso_babel.strip())
            if nany <= 50:
                if ","!= sinal:
                    novo_poema.append("")

    if novo_poema:
        last = novo_poema[-1]
        njump = random.randrange(len(sinais_end))
        sinal = sinais_end[njump]

        if len(last) > 1 and not last[-1] in sinais_ini:
            if "," == last or ":" == last:
                novo_poema[-1] += sinal
            else:
                novo_poema[-1] += "."

    return novo_poema

def fala_cidade_fato():
    cidades = load_cidades()
    if not cidades:
        return "CidadeDesconhecida"
    return random.choice(cidades)

def fala_cidade_oficio():
    cidades = load_cidades()
    if not cidades:
        return "CidadeDesconhecida"
    return random.choice(cidades)

def fala_celsius():
    ini = randrange(1, 50)
    fim = randrange(1, 50)
    if ini > fim:
        ini, fim = fim, ini
    else:
        ini -= 1
    return str(ini) + "º e " + str(fim) + "º"

def fala_umidade():
    ini = randrange(1, 99)
    return str(ini) + "%"

def fala_data(dref):
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
    ]
    dia = dref.day
    mes = dref.month
    if mes > 0 and mes < 13:
        mes -= 1
    else:
        mes = 5
    mestxt = meses[mes]
    ano = dref.year
    return f"{dia} de {mestxt} de {ano}"

def fala_norma_abnp():
    hoje = datetime.now().date()
    rand = randrange(0, hoje.year * 30)
    ontem = hoje - datetime.timedelta(days=rand)
    return f"{ontem.day}/{ontem.year}"

def fala_abnp():
    lista = load_abnp()
    if not lista:
        return "ABNP"
    nany = randrange(len(lista))
    return lista[nany]

def acerto_final(texto):
    if "." in texto:
        texto = texto.replace(".", ".")
    if "," in texto:
        texto = texto.replace(",", ",")
    if "?" in texto:
        texto = texto.replace("?", "?")
    if "!" in texto:
        texto = texto.replace("!", "!")
    if " :" in texto:
        texto = texto.replace(" :", ":")
    if "..." in texto:
        texto = texto.replace("...", "...")
    if " -" in texto:
        texto = texto.replace(" -", "-")
    if "- " in texto:
        texto = texto.replace("- ", "-")
    if " #" in texto:
        texto = texto.replace(" #", "")
    if "#" in texto:
        texto = texto.replace("#", "")
    if "< pCity >" in texto:
        texto = texto.replace("< pCity >", fala_cidade_fato())
    if "< pCidadeOficio >" in texto:
        texto = texto.replace("< pCidadeOficio >", fala_cidade_oficio())
    if "< gCelcius >" in texto:
        texto = texto.replace("< gCelcius >", fala_celsius())
    if "< pUmido >" in texto:
        texto = texto.replace("< pUmido >", fala_umidade())
    if "< pAbnp >" in texto:
        texto = texto.replace("< pAbnp >", fala_abnp())
    if "< dNormas >" in texto:
        texto = texto.replace("< dNormas >", fala_norma_abnp())
    if "< dPublic >" in texto:
        hoje = datetime.now().date()
        rand = randrange(0, hoje.year * 30)
        ontem = hoje - datetime.timedelta(days=rand)
        texto = texto.replace("< dPublic >", fala_data(ontem))
    if "< dOficio >" in texto:
        hoje = datetime.now().date()
        rand = randrange(0, hoje.year * 30)
        demain = hoje + datetime.timedelta(days=rand)
        texto = texto.replace("< dOficio >", fala_data(demain))
    return texto

def gera_poema(nome_tema, seed_eureka):
    lista_header = []
    lista_linhas = []
    lista_finais = []
    lista_change = []
    lista_duplos = []
    lista_errata = []
    lista_unicos = []

    this_seed = ""
    find_coords = ""
    look_for_seed = False

    if seed_eureka!= "":
        look_for_seed = True
        part_string = seed_eureka.partition(" ➪ ")
        this_seed = part_string[0]
        find_coords = part_string[2]

    nome_tema = nome_tema.strip("\n")

    try:
        if nome_tema == "Babel":
            novo_poema = novo_babel(0)
            return novo_poema
        else:
            tema = abre(nome_tema)
            for line in tema:
                if line.startswith("*", 0, 1):
                    lista_header.append(line)
                elif line.startswith("|", 0, 1):
                    lista_linhas.append(line)
                else:
                    lista_finais.append(line)
    except UnicodeDecodeError:
        lista_errata.append(nome_tema)
        pass

    novo_poema = []
    novo_verso = ""
    muda_linha = "00"
    pula_linha = "no"
    find_eureka = ""

    for line in lista_linhas:
        alinhas = line.split("|")

        if len(alinhas) == 0:
            continue
        if len(alinhas) < 2:
            lista_errata.append(nome_tema)
            continue
        if alinhas[2] == "00":
            pula_linha = "si"
            lista_change.append(line)
            continue

        if len(alinhas) >= 7:
            numero_linea = alinhas[1]
            ideia_numero = alinhas[2]
            fonte_itimos = alinhas[3]
            se_randomico = alinhas[4]
            total_itimos = int(alinhas[5])
            itimos_atual = int(alinhas[6])
            array_itimos = alinhas[7 : len(alinhas) - 1]

            tabs = array_itimos[0].count('$') if array_itimos else 0
            if tabs > 0:
                array_itimos = array_itimos[1 : len(array_itimos)]

            find_eureka = nome_tema + "_" + numero_linea + ideia_numero

            if itimos_atual > len(array_itimos):
                itimos_atual = len(array_itimos)
            if total_itimos!= len
