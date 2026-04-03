import streamlit as st
import random
import time
import os

# ---import streamlit as st
import random
import time
import os
import base64
import socket
from gtts import gTTS
from deep_translator import GoogleTranslator

# --- 1. O MOTOR DE 1983 ---
from lay_2_ypo import gera_poema

# --- 2. GÊNESE (ESTADOS & CONFIGURAÇÕES) ---
st.set_page_config(page_title="yPoemas 1983", layout="wide")

IPAddres = "sessao"

if 'page' not in st.session_state: st.session_state.page = "mini"
if 'book' not in st.session_state: st.session_state.book = "todos os temas"
if 'take' not in st.session_state: st.session_state.take = 0
if 'tema' not in st.session_state: st.session_state.tema = ""
if 'lang' not in st.session_state: st.session_state.lang = "pt"
if 'last_lang' not in st.session_state: st.session_state.last_lang = "pt"
if 'arts' not in st.session_state: st.session_state.arts = []
if 'draw' not in st.session_state: st.session_state.draw = True
if 'talk' not in st.session_state: st.session_state.talk = False
if 'vydo' not in st.session_state: st.session_state.vydo = False

# --- 3. AS ENGRENAGENS (FUNÇÕES UNIVERSAIS) ---

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def translate(input_text):
    if st.session_state.lang == "pt": return input_text
    if not have_internet():
        st.session_state.lang = "pt"
        return input_text
    try:
        output_text = GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
        # Limpeza de tags do tradutor
        for tag in ["<br>>", "< br>", "<br >", "<br ", " br>"]:
            output_text = output_text.replace(tag, "<br>")
        return output_text
    except:
        return "Erro na tradução / File too large."

def talk(text):
    text = text.replace("<br>", "\n").replace("< br>", "").replace("<br >", "")
    tts = gTTS(text=text, lang=st.session_state.lang, slow=False)
    nany_file = random.randint(1, 20000000)
    file_name = os.path.join("./temp/audio" + str(nany_file) + ".mp3")
    if not os.path.exists("./temp"): os.makedirs("./temp")
    tts.save(file_name)
    with open(file_name, "rb") as f:
        st.audio(f.read(), format="audio/ogg")
    os.remove(file_name)

def load_temas(book):
    book_list = []
    path = os.path.join("./base/rol_" + book + ".txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                book_list.append(line.replace(" ", "").strip("\n"))
    return book_list

def load_poema(nome_tema, seed_eureka):
    script = gera_poema(nome_tema, seed_eureka)
    novo_ypoema = ""
    lypo_user = "LYPO_" + IPAddres
    path_lypo = os.path.join("./temp/", lypo_user)
    if not os.path.exists("./temp"): os.makedirs("./temp")
    with open(path_lypo, "w", encoding="utf-8") as save_lypo:
        save_lypo.write(nome_tema + "\n")
        for line in script:
            save_lypo.write(line + ("\n" if line == "\n" else ""))
            novo_ypoema += line + ("<br>" if line != "\n" else "")
    return novo_ypoema

def load_lypo():
    lypo_text = ""
    path = os.path.join("./temp/LYPO_" + IPAddres)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as script:
            for line in script:
                lypo_text += line.strip() + "<br>"
    return lypo_text

def load_typo():
    typo_text = ""
    path = os.path.join("./temp/TYPO_" + IPAddres)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as script:
            for line in script:
                line = line.strip()
                # Normalização de bugs de tradução
                line = line.replace(" >", "\n").replace("< ", "\n").replace(" br ", "\n")
                typo_text += line + "<br>"
    return typo_text

def load_arts(nome_tema):
    path = "./images/machina/"
    images_db = load_images()
    for line in images_db:
        if line.startswith(nome_tema):
            part_line = line.strip().partition(" : ")
            path = "./images/" + part_line[2] + "/"
            break
    
    arts_list = [f for f in os.listdir(path) if f.endswith(".jpg")]
    if not arts_list: return None
    
    image = random.choice(arts_list)
    while image in st.session_state.arts and len(arts_list) > 1:
        image = random.choice(arts_list)
    
    st.session_state.arts.append(image)
    if len(st.session_state.arts) > 36: del st.session_state.arts[0]
    return path + image

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    st.markdown("""
        <style>
        .container { display: flex; align-items: flex-start; justify-content: space-between; }
        .logo-text { font-family: 'IBM Plex Sans'; font-weight: 600; font-size: 1.2rem; padding-left: 15px; }
        .logo-img { float: right; max-width: 40%; border-radius: 5px; }
        mark { background-color: powderblue; color: black; }
        </style>
    """, unsafe_allow_html=True)
    
    if LOGO_IMAGE:
        img_b64 = base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()
        html = f"<div class='container'><p class='logo-text'><mark>{LOGO_TEXTO}</mark></p><img class='logo-img' src='data:image/jpg;base64,{img_b64}'></div>"
    else:
        html = f"<div class='container'><p class='logo-text'><mark>{LOGO_TEXTO}</mark></p></div>"
    st. 1. GÊNESE (ESTADOS) ---
# Aqui garantimos que o st.session_state não quebre
if 'page' not in st.session_state: st.session_state.page = "mini"
if 'mini' not in st.session_state: st.session_state.mini = 0
if 'auto' not in st.session_state: st.session_state.auto = False
if 'lang' not in st.session_state: st.session_state.lang = "pt"
if 'last_lang' not in st.session_state: st.session_state.last_lang = "pt"

# --- 2. AS ENGRENAGENS (FUNÇÕES QUE O PALCO CHAMA) ---
# Elas PRECISAM estar aqui, antes de serem usadas.

def load_temas(book):
    book_list = []
    # Usando o caminho que você enviou do ypo_old
    path = os.path.join("./base/rol_" + book + ".txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.replace(" ", "")
                book_list.append(line.strip("\n"))
    return book_list

def load_help(lang):
    # Simulação do seu dicionário de ajuda (mande o real se preferir)
    return {1: "sortear", 4: "mais"}

def translate(texto):
    # Sua lógica de tradução (ou apenas retorna o texto por enquanto)
    return texto

def say_number(tema):
    return "1.0"

# --- 3. O PALCO (PÁGINA MINI) ---

def page_mini():
    # Agora o Python já leu 'load_temas' acima, então não haverá NameError
    temas_list = load_temas("todos os temas")
    maxy_mini = len(temas_list)

    if st.session_state.mini >= maxy_mini:
        st.session_state.mini = 0

    foo1, more_col, rand_col, auto_col, foo2 = st.columns([4, 1, 1, 1, 4])
    
    help_tips = load_help(st.session_state.lang)
    
    # ... resto da lógica que você me enviou ...
    st.write(f"Māchina ativa: {st.session_state.tema}")

# --- 4. EXECUÇÃO PRINCIPAL ---

if st.session_state.page == "mini":
    page_mini()
