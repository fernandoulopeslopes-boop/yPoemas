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
config: chrome://settings/content/siteDetails?site=https%3A%2Fauth.streamlit.io
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
from extra_streamlit_components import TabBar as stx
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
        st.warning(translate("Google Translator não conectado"))
    try:
        from gtts import gTTS
    except ImportError as ex:
        st.warning(translate("Google TTS não conectado"))
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
    with open(BASE / "babel.txt", "r", encoding="utf-8") as babel:
        for line in babel:
            lista.append(line.strip())
    return lista

@st.cache_data
def load_cidades():
    cidades = []
    with open(BASE / "fatos_cidades.txt", encoding="utf8") as file:
        for line in file:
            if line.strip():
                cidades.append(line.strip())
    return cidades

@st.cache_data
def load_abnp():
    lista = []
    full_name = BASE / "abnp.txt"
    with open(full_name, encoding="utf-8") as file:
        for line in file:
            alinhas = line.split("|")
            for item in alinhas:
                item = item.strip()
                if item:
                    lista.append(item)
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
    for nQtdLin in range(qtd_versos): # corrigido: era range(1, qtd_versos)
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
    """
    :return: alguma cidade do arquivo fatos_cidades.txt
    """
    cidades = load_cidades()
    if not cidades:
        return "CidadeDesconhecida"
    return random.choice(cidades)

def fala_cidade_oficio():
    """
    :return: alguma cidade do arquivo cidade_país.txt
    """
    cidades = load_cidades()
    if not cidades:
        return "CidadeDesconhecida"
    return random.choice(cidades)

def fala_celsius():
    """
    :return: temperatura randômica entre 1 e 50 graus celcius - Meteoro
    """
    ini = randrange(1, 50)
    fim = randrange(1, 50)
    if ini > fim:
        ini, fim = fim, ini
    else:
        ini -= 1
    return str(ini) + "º e " + str(fim) + "º"

def fala_umidade():
    """
    :return: umidade randômica entre 1 e 99% - Meteoro
    """
    ini = randrange(1, 99)
    return str(ini) + "%"

def fala_data(dref):
    """
    :param data de referência
    :return: data genérica: dia + mês_extenso + ano
    """
    meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
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
    """
    :return: data randômicamente 'anterior' à data atual
    """
    hoje = datetime.now().date()
    rand = randrange(0, hoje.year * 30)
    ontem = hoje - datetime.timedelta(days=rand)
    return f"{ontem.day}/{ontem.year}"

def fala_abnp():
    lista = load_abnp()
    if not lista:
        return "ABNP"
    nany = randrange(len(lista))
    return lista[nany] # CORRIGIDO: retornava a lista inteira

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

def gera_poema(nome_tema, seed_eureka): # abrir um script.ypo e gerar um novo yPoema
    """
    :param = script, tema
         numero_linea = '01' # linha
         ideia_numero = '01' # ideia
         fonte_itimos = nome_tema + '_' + numero_linea + ideia_numero
         se_randomico = 'F' # se_random
         total_itimos = N # qtd_itimos
         itimos_atual = 1 # itimos_atual
         array_itimos = [] # array com todos os itimos da ideia na linha
    return: novo_poema
    """

    lista_header = []
    lista_linhas = []
    lista_finais = []
    lista_change = []
    lista_duplos = []
    lista_errata = []
    lista_unicos = []

    conta_palavra = 0

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
                if line.startswith("*", 0, 1): # observações e cabeçalho
                    lista_header.append(line)
                elif line.startswith("|", 0, 1): # ideias & itimos
                    lista_linhas.append(line)
                else: # <eof> + análise + build_date
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

            if total_itimos!= len(array_itimos): # just in case...
                total_itimos = len(array_itimos) # real lenght...

            if total_itimos == 1: # just in case...
                se_randomico = "F"

            tentativas = 0
            while True: # seleciona próximo ítimo válido
                if 1!= total_itimos: # mais de hum ítimo
                    if se_randomico == "F":
                        itimos_atual -= 1 # pega ítimo anterior
                        if itimos_atual < 0:
                            itimos_atual = ( total_itimos - 1) # because matrix começa em zero
                    else:
                        if total_itimos >= 1:
                            itimos_atual = randrange(total_itimos) # CORRIGIDO: era randrange(0, total_itimos - 1)
                        else:
                            itimos_atual = 0 # just in case
                else: # apenas hum ítimo
                    itimos_atual = 0

                # CORRIGIDO: era <=, agora é < pra evitar IndexError
                if itimos_atual >= 0 and itimos_atual < len(array_itimos):
                    itimo_escolhido = array_itimos[itimos_atual] # escolheu ítimo
                else:
                    st.warning(
                        "Algo deu errado em "
                        + fonte_itimos
                        + ". Se puder, entre em contato com o '[autor](mailto:lopes.fernando@hotmail.com)'"
                    )
                    itimo_escolhido = "_Erro_"

                if ( find_eureka == find_coords ): # marcar palavra/semente em eureka parameter
                    if look_for_seed: # not changed yet...
                        for itimo in array_itimos:
                            if this_seed.lower() in itimo.lower(): # CORRIGIDO: linha estava quebrada
                                itimo_escolhido = itimo
                                lista_unicos.append(
                                    itimo_escolhido.upper()
                                ) # no repeated words...
                                itimo_escolhido = itimo_escolhido.replace(
                                    this_seed, "<mark>" + this_seed + "</mark>"
                                ) # markdown text
                                look_for_seed = False

                # verifica se ítimo ainda não foi escolhido
                temp_random = se_randomico
                if (
                    not itimo_escolhido.upper() # Elimina duplicidaders óbvias...
                    in "_E_A_AS_O_OS_NO_NOS_NA_NAS_ME_DE_SE_QUE_NÃO_SO_SEM_NEM_EM_UM_UMA_POR_MEU_VE_TE_TÃO_DA_SER_TER_PRA_PARA_QUANDO_..._._,_:_!_?"
                ):
                    if (
                        itimo_escolhido.upper() not in lista_unicos
                    ): # check if not yet used...
                        lista_unicos.append(itimo_escolhido.upper())
                        break
                    else:
                        tentativas += 1
                        if (
                            tentativas > total_itimos
                        ): # tentativas > que total de ítimos: pega o próximo sequencial
                            if temp_random == "T":
                                tentativas = 0 # Da Capo
                                temp_random = "F"
                            else:
                                lista_unicos.append(itimo_escolhido.upper())
                                lista_duplos.append(itimo_escolhido.upper())
                                break

                        if (
                            itimo_escolhido.upper() in lista_duplos
                        ): # para não repetir verbetes/ítimos usados em mais de uma ideia/linha
                            if len(itimo_escolhido) > 3:
                                continue

                        if tentativas > 30:
                            break
                else:
                    break

            if numero_linea!= muda_linha: # check new line in script
                if novo_verso:
                    novo_verso = acerto_final(novo_verso)
                    novo_poema.append(novo_verso)
                novo_verso = ""
                muda_linha = numero_linea

            novo_verso += itimo_escolhido + " "
            if tabs > 0:
                novo_verso = tabs*'&emsp;' + novo_verso
                tabs = 0

            if "si" == pula_linha:
                novo_poema.append("\n")
                pula_linha = "no"

            changed_line = (
                "|" + numero_linea + "|" + ideia_numero + "|" + fonte_itimos + "|"
            )

            if itimos_atual < 1: # sequencial = -1
                if total_itimos == 1:
                    itimos_atual = 1
                else:
                    itimos_atual = total_itimos

            if se_randomico == "T":
                changed_line += "T"
            else:
                changed_line += "F"

            changed_line += "|" + str(total_itimos) + "|" + str(itimos_atual)

            for v in alinhas[7 : len(alinhas) - 1]:
                changed_line += "|" + v
            changed_line += "|\n"
            lista_change.append(changed_line)

        # endif len(alinhas) >= 7:
    # end for... line in lista_linhas

    if novo_verso:
        novo_poema.append(acerto_final(novo_verso))

    if nome_tema == "Nós":
        novo_poema.append("\n")
        novo_poema.append(
            '<a href="https://thispersondoesnotexist.com/" target="_blank">... quem será essa pessoa que não existe?</a>'
        )

    if len(lista_errata) > 0:
        st.warning(
            "Algo deu errado com o tema "
            + nome_tema.upper()
            + ". Se puder, entre em contato com o '[autor](mailto:lopes.fernando@hotmail.com)'"
        )
    # BLOCO DE REESCRITA DESATIVADO - era a causa do race condition
    # with open(DATA / f"{nome_tema}.ypo", "w", encoding="utf-8") as file:
    # for linha in lista_header:
    # file.write(linha)
    # for linha in lista_change:
    # file.write(linha)
    # for linha in lista_finais:
    # file.write(linha)

    return novo_poema

### eof: MACHINA
### bof: tools

def translate(input_text):
    if st.session_state.lang == "pt": # don't need translations here
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

def pick_lang(): # define idioma
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

    if st.session_state.lang!= st.session_state.last_lang:
        st.success(translate("idioma atual") + " ➪ " + st.session_state.lang)

def show_icons(): # https://api.whatsapp.com/
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
    with open(BASE / "helpers.txt", encoding="utf-8") as file:
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

def atoi(text): # human reading number functions for sorting
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split(r"(\d+)", text)]

### eof: tools
### bof: update themes readings

def update_visy(): # count one more visitor
    with open(TEMP / "visitors.txt", "r", encoding="utf-8") as visitors:
        tots = int(visitors.read())
        tots = tots + 1
        st.session_state.nany_visy = tots

    with open(TEMP / "visitors.txt", "w", encoding="utf-8") as visitors:
        visitors.write(str(tots))

@st.cache_data
def load_readings():
    readers_list = []
    with open(TEMP / "read_list.txt", encoding="utf-8") as reader:
        for line in reader:
            readers_list.append(line)
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

    with open(TEMP / "read_list.txt", "w", encoding="utf-8") as new_reader:
        for line in read_changes:
            new_reader.write(line)

def list_readings():
    sum_all_days = 0
    read_days = [] # days
    readings = load_readings()
    for line in readings:
        pipe_line = line.split("|")
        name = pipe_line[1]
        qtds = pipe_line[2]
        sum_all_days += int(qtds)
        if qtds!= "0":
            new_line = str(qtds) + " - " + name + "\n"
            read_days.append(new_line)

    read_days.sort(key=natural_keys, reverse=True)

    total_viewes = st.session_state.nany_visy
    currrent_day = datetime.now()
    begining_day = datetime(2021, 7, 6)
    days_of_runs = begining_day - currrent_day
    days_of_runs = abs(days_of_runs.days)
    views_by_day = total_viewes / days_of_runs if days_of_runs > 0 else 0
    reads_by_day = sum_all_days / total_viewes if total_viewes > 0 else 0

    options = list(range(len(read_days)))
    st.selectbox(
        "↓ "
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

@st.cache_data
def load_md_file(file): # Open files for about's
    try:
        with open(MD_FILES / file, encoding="utf-8") as file_to_open:
            file_text = file_to_open.read()

        if not "rol_" in file.lower(): # do not translate theme
            file_text = translate(file_text)
    except:
        file_text = translate("ooops... arquivo ( " + file + " ) não pode ser aberto.")
        st.session_state.lang = "pt"

    return file_text

@st.cache_data
def load_eureka(part_of_word):
    lexico_list = []
    with open(BASE / "lexico_pt.txt", encoding="utf-8") as lista:
        for line in lista:
            this_line = line.strip("\n")
            part_line = this_line.partition(" : ")
            palas = part_line[0]
            if part_of_word.lower() in palas.lower():
                lexico_list.append(line)

    return lexico_list

@st.cache_data
def load_temas(book): # List of themes inside a Book
    book_list = []
    try:
        with open(BASE / f"rol_{book}.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    book_list.append(line)
    except FileNotFoundError:
        st.warning(f"Arquivo rol_{book}.txt não encontrado")
    return book_list

@st.cache_data
def load_info(nome_tema):
    with open(BASE / "info.txt", "r", encoding="utf-8") as file:
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
                    result
