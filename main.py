import os
import io
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime
from lay_2_ypo import gera_poema

# --- Settings ---

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

@st.cache_data
def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

if have_internet():
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        pass
    try:
        from gtts import gTTS
    except ImportError:
        pass
else:
    st.warning("Internet não conectada.")

hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

st.markdown(
    """ <style>
    footer {visibility: hidden;}
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 300px;
    }
    .reportview-container .main .block-container{
        padding: 0rem;
    }
    mark {
      background-color: powderblue;
      color: black;
    }
    .container {
        display: flex;
    }
    .logo-text {
        font-weight: 600;
        font-size: 18px;
        font-family: 'IBM Plex Sans';
        color: #000000;
        padding-left: 15px;
    }
    .logo-img {
        float:right;
    }
    </style> """,
    unsafe_allow_html=True,
)

# --- Session State ---

if "lang" not in st.session_state: st.session_state.lang = "pt"
if "book" not in st.session_state: st.session_state.book = "livro vivo"
if "take" not in st.session_state: st.session_state.take = 0
if "mini" not in st.session_state: st.session_state.mini = 0
if "tema" not in st.session_state: st.session_state.tema = "Fatos"
if "eureka" not in st.session_state: st.session_state.eureka = 0
if "find_eureka" not in st.session_state: st.session_state.find_eureka = "amar"
if "draw" not in st.session_state: st.session_state.draw = False
if "talk" not in st.session_state: st.session_state.talk = False

# --- Tools ---

def translate(input_text):
    if st.session_state.lang == "pt" or not have_internet():
        return input_text
    try:
        output_text = GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
        return output_text.replace("<br>>", "<br>").replace("< br>", "<br>").replace("<br >", "<br>")
    except:
        return input_text

def pick_lang():
    btn_pt, btn_es, btn_it, btn_fr, btn_en, btn_xy = st.sidebar.columns([1, 1, 1, 1, 1, 1])
    if btn_pt.button("pt", key=1): st.session_state.lang = "pt"
    if btn_es.button("es", key=2): st.session_state.lang = "es"
    if btn_it.button("it", key=3): st.session_state.lang = "it"
    if btn_fr.button("fr", key=4): st.session_state.lang = "fr"
    if btn_en.button("en", key=5): st.session_state.lang = "en"

def draw_check_buttons():
    draw_col, talk_col = st.sidebar.columns(2)
    st.session_state.draw = draw_col.checkbox("🎨 Art", st.session_state.draw)
    st.session_state.talk = talk_col.checkbox("🔊 Talk", st.session_state.talk)

@st.cache_data
def load_temas(book):
    with open(f"./base/rol_{book}.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f]

def load_eureka(part_of_word):
    lexico_list = []
    with open("./base/lexico_pt.txt", "r", encoding="utf-8") as f:
        for line in f:
            if part_of_word.lower() in line.lower():
                lexico_list.append(line.strip())
    return lexico_list

def load_poema(nome_tema, seed_eureka):
    script = gera_poema(nome_tema, seed_eureka)
    return "<br>".join(script)

def load_arts(nome_tema):
    path = "./images/machina/"
    # Lógica de seleção de imagem simplificada
    arts_list = [f for f in os.listdir(path) if f.endswith(".jpg")]
    image = random.choice(arts_list)
    return path + image

def write_ypoema(LOGO_TEXT, LOGO_IMAGE):
    if LOGO_IMAGE:
        img_b64 = base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()
        st.markdown(f"<div class='container'><img class='logo-img' src='data:image/jpg;base64,{img_b64}'><p class='logo-text'>{LOGO_TEXT}</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='container'><p class='logo-text'>{LOGO_TEXT}</p></div>", unsafe_allow_html=True)

def talk(text):
    if have_internet():
        clean_text = text.replace("<br>", "\n")
        tts = gTTS(text=clean_text, lang=st.session_state.lang)
        filename = f"./temp/audio_{random.randint(1,1000)}.mp3"
        tts.save(filename)
        st.audio(open(filename, "rb").read(), format="audio/mpeg")
        os.remove(filename)

# --- Pages ---

def page_mini():
    temas_list = load_temas("todos os temas")
    st.session_state.tema = temas_list[st.session_state.mini]
    curr_ypoema = load_poema(st.session_state.tema, "")
    if st.session_state.lang != "pt": curr_ypoema = translate(curr_ypoema)
    LOGO_IMAGE = load_arts(st.session_state.tema) if st.session_state.draw else None
    write_ypoema(curr_ypoema, LOGO_IMAGE)
    if st.session_state.talk: talk(curr_ypoema)

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    st.session_state.tema = temas_list[st.session_state.take]
    curr_ypoema = load_poema(st.session_state.tema, "")
    if st.session_state.lang != "pt": curr_ypoema = translate(curr_ypoema)
    LOGO_IMAGE = load_arts(st.session_state.tema) if st.session_state.draw else None
    write_ypoema(curr_ypoema, LOGO_IMAGE)
    if st.session_state.talk: talk(curr_ypoema)

def page_eureka():
    find_what = st.text_input("Busca Eureka", value=st.session_state.find_eureka)
    if len(find_what) >= 3:
        results = load_eureka(find_what)
        seed_list = [line.partition(" : ")[0] for line in results if " : " in line]
        if seed_list:
            st.selectbox("Sementes:", seed_list)
        else:
            st.info("Nada encontrado.")

# --- Main ---

def main():
    with st.sidebar:
        st.write("### yPoemas")
        pick_lang()
        st.divider()
        page = st.radio("Menu", ["Mini", "yPoemas", "Eureka"])
        st.divider()
        draw_check_buttons()

    if page == "Mini": page_mini()
    elif page == "yPoemas": page_ypoemas()
    elif page == "Eureka": page_eureka()

if __name__ == "__main__":
    main()
