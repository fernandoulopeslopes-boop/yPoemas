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
"""

import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime
from lay_2_ypo import gera_poema
from extra_streamlit_components import TabBar as stx

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- CONSTANTES ---
BASE_DIR = os.path.dirname(__file__)
BASE = os.path.join(BASE_DIR, "base")
TEMP = os.path.join(BASE_DIR, "temp")
MD_FILES = os.path.join(BASE_DIR, "md_files")
IMAGES = os.path.join(BASE_DIR, "images")
OFF_MACHINA = os.path.join(BASE_DIR, "off_machina")
IPAddres = socket.gethostbyname(socket.gethostname())
LYPO_FILE = os.path.join(TEMP, f"LYPO_{IPAddres}")
TYPO_FILE = os.path.join(TEMP, f"TYPO_{IPAddres}")
os.makedirs(TEMP, exist_ok=True)

# --- CSS ÚNICO: remove faixa branca e junta tudo ---
st.markdown(
    """
    <style>
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {height: 0rem;}
    div[data-testid="stToolbar"] {display: none;}
    div[data-testid="stDecoration"] {display: none;}
   .reportview-container.main.block-container{
        padding-top: 0rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 0rem;
    }
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 310px;
    }
    /* Remove margem do TabBar que causa faixa branca */
    div[data-testid="stVerticalBlock"] > div:first-child {
        margin-top: -1rem;
    }
    mark {background-color: powderblue; color: black;}
   .container {display: flex;}
   .logo-text {
        font-weight: 600; font-size: 18px; font-family: 'IBM Plex Sans';
        color: #000000; padding-top: 0px; padding-left: 15px;
    }
   .logo-img {float:right;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SESSION STATE: loop único ---
DEFAULTS = {
    "lang": "pt", "last_lang": "pt", "book": "livro vivo", "take": 0, "mini": 0,
    "tema": "Fatos", "off_book": 0, "off_take": 0, "eureka": 0, "poly_lang": "ca",
    "poly_name": "català", "poly_take": 12, "poly_file": "poly_pt.txt",
    "visy": True, "nany_visy": 0, "draw": False, "talk": False, "vydo": False,
    "arts": [], "auto": False, "rand": False, "gerar": False,
    "internet": None, "translator": None, "gtts": None
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- INTERNET + IMPORTS PESADOS: checa 1x só ---
@st.cache_resource
def check_deps():
    def have_net(host="8.8.8.8", port=53, timeout=2):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except:
            return False

    internet = have_net()
    translator = gtts = None
    if internet:
        try:
            from deep_translator import GoogleTranslator
            translator = GoogleTranslator
        except: pass
        try:
            from gtts import gTTS
            gtts = gTTS
        except: pass
    return internet, translator, gtts

st.session_state.internet, st.session_state.translator, st.session_state.gtts = check_deps()
if not st.session_state.internet:
    st.warning("Internet não conectada. Traduções não disponíveis no momento.")

# --- FUNÇÕES GENÉRICAS ---
@st.cache_data
def load_list(path):
    try:
        with open(path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def load_file_temp(name):
    try:
        with open(os.path.join(TEMP, name), encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def save_file_temp(name, content):
    with open(os.path.join(TEMP, name), "w", encoding="utf-8") as f:
        f.write(content)

def translate(txt):
    if st.session_state.lang == "pt" or not st.session_state.translator:
        return txt
    try:
        out = st.session_state.translator(source="pt", target=st.session_state.lang).translate(text=txt)
        return re.sub(r"<\s*br\s*>", "<br>", out)
    except:
        return "Arquivo muito grande para ser traduzido."

def load_md_file(file):
    try:
        txt = open(os.path.join(MD_FILES, file), encoding="utf-8").read()
        return txt if "rol_" in file.lower() else translate(txt)
    except:
        st.session_state.lang = "pt"
        return translate(f"ooops... arquivo ( {file} ) não pode ser aberto.")

def load_arts(nome_tema):
    path = os.path.join(IMAGES, "machina")
    for line in load_list(os.path.join(BASE, "images.txt")):
        if line.startswith(nome_tema + " :"):
            path = os.path.join(IMAGES, line.split(" : ")[1])
            break
    try:
        arts = [f for f in os.listdir(path) if f.endswith(".jpg")]
        if not arts: return None
        img = random.choice([a for a in arts if a not in st.session_state.arts] or arts)
        st.session_state.arts.append(img)
        if len(st.session_state.arts) > 36: del st.session_state.arts[0]
        return os.path.join(path, img)
    except:
        return None

def load_poema(nome_tema, seed_eureka=""):
    script = gera_poema(nome_tema, seed_eureka)
    novo = []
    muda, verso = "00", ""
    for line in script:
        if line.startswith("|"):
            p = line.split("|")
            if len(p) < 9: continue
            num, itimos = p[1], p[8:-1] if p[-1] == "\n" else p[8:]
            if not itimos: continue
            escolhido = random.choice(itimos)
            if num!= muda:
                if verso: novo.append(verso.strip())
                verso, muda = "", num
            verso += escolhido + " "
    if verso: novo.append(verso.strip())

    save_file_temp(f"LYPO_{IPAddres}", nome_tema + "\n" + "\n".join(novo))
    return "<br>".join(novo)

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    if LOGO_IMAGE:
        st.markdown(
            f"""<div class='container'>
            <img class='logo-img' src='data:image/jpg;base64,{base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()}'>
            <p class='logo-text'>{LOGO_TEXTO}</p></div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(f"<div class='container'><p class='logo-text'>{LOGO_TEXTO}</p></div>", unsafe_allow_html=True)

def talk(text):
    if not st.session_state.gtts: return
    text = re.sub(r"<br>", "\n", text)
    tts = st.session_state.gtts(text=text, lang=st.session_state.lang, slow=False)
    file = os.path.join(TEMP, f"audio{random.randint(1, 2e7)}.mp3")
    tts.save(file)
    st.audio(open(file, "rb").read(), format="audio/ogg")
    os.remove(file)

# --- UI ---
def pick_lang():
    cols = st.sidebar.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
    langs = ["pt", "es", "it", "fr", "en"]
    for i, (c, l) in enumerate(zip(cols, langs + ["⚒️"])):
        if c.button(l, key=i+1, help=st.session_state.poly_name if l=="⚒️" else l):
            if l == "⚒️":
                st.session_state.last_lang = st.session_state.lang
                st.session_state.lang = st.session_state.poly_lang
            else:
                st.session_state.lang = l
                st.session_state.poly_file = f"poly_{l}.txt"
    if st.session_state.lang!= st.session_state.last_lang:
        st.success(translate("idioma atual") + " ➪ " + st.session_state.lang)

def draw_check_buttons():
    c1, c2, c3 = st.sidebar.columns([3.8, 3.2, 3])
    st.session_state.draw = c1.checkbox("imagem", st.session_state.draw, key="draw")
    st.session_state.talk = c2.checkbox("áudio", st.session_state.talk, key="talk")
    st.session_state.vydo = c3.checkbox("vídeo", st.session_state.vydo, key="vydo")

def show_icons():
    st.sidebar.markdown(
        f"""<nav>
        <a href='https://www.facebook.com/nandoulopes' target='_blank'>• facebook</a> |
        <a href='mailto:lopes.fernando@hotmail.com' target='_blank'>e-mail</a> |
        <a href='https://www.instagram.com/fernando.lopes.942/' target='_blank'>instagram</a> |
        <a href='https://web.whatsapp.com/send?phone=+5512991368181' target='_blank'>whatsapp</a>
        </nav>""", unsafe_allow_html=True,
    )

# --- VISITOR COUNT 1x ---
if st.session_state.visy:
    try:
        v = int(load_file_temp("visitors.txt") or "0") + 1
        st.session_state.nany_visy = v
        save_file_temp("visitors.txt", str(v))
    except: pass
    temas = load_list(os.path.join(BASE, f"rol_{st.session_state.book}.txt"))
    st.session_state.take = random.randrange(len(temas)) if temas else 0
    st.success(translate("bem vindo à **máquina de fazer Poesia...**"))
    st.session_state.draw = True
    st.session_state.visy = False

st.session_state.last_lang = st.session_state.lang

# --- PÁGINAS: só yPoemas como exemplo, resto igual mas chama funções otimizadas ---
def page_ypoemas():
    temas_list = load_list(os.path.join(BASE, f"rol_{st.session_state.book}.txt")) or ["Fatos"]
    maxy = len(temas_list) - 1
    st.session_state.take = max(0, min(st.session_state.take, maxy))

    _, more, last, rand, nest, manu, _ = st.columns([3, 1, 1, 1, 1, 1, 3])
    if last.button("◀", help="anterior"):
        st.session_state.take = maxy if st.session_state.take == 0 else st.session_state.take - 1
    if rand.button("✻", help="ao acaso"):
        st.session_state.take = random.randrange(maxy + 1)
    if nest.button("▶", help="próximo"):
        st.session_state.take = 0 if st.session_state.take == maxy else st.session_state.take + 1
    more.clicked = more.button("✚", help="mais lidos...")
    manu.clicked = manu.button("?", help="help!!!")

    if not st.session_state.draw:
        opt = st.selectbox("↓ lista de Temas", range(len(temas_list)),
                          index=st.session_state.take, format_func=lambda x: temas_list[x])
        st.session_state.take = opt

    st.session_state.tema = temas_list[st.session_state.take]

    if manu.clicked:
        st.subheader(load_md_file("MANUAL_YPOEMAS.md"))

    if st.session_state.vydo:
        st.sidebar.info(load_md_file("INFO_VYDE.md"))
        v = os.path.join(BASE, "video_ypoemas.webm")
        if os.path.exists(v): st.video(open(v, "rb").read(), format="webm")
        st.session_state.vydo = False
    else:
        what = f"⚫ {st.session_state.lang} ( {st.session_state.book} ) ( {st.session_state.take+1} / {len(temas_list)} )"
        with st.expander(what, True):
            curr = load_file_temp(f"LYPO_{IPAddres}") if st.session_state.lang!= st.session_state.last_lang else ""
            if not curr:
                curr = load_poema(st.session_state.tema)
                curr = load_file_temp(f"LYPO_{IPAddres}")
            if st.session_state.lang!= "pt":
                curr = translate(curr)
                save_file_temp(f"TYPO_{IPAddres}", curr)
                curr = load_file_temp(f"TYPO_{IPAddres}")

            LOGO_TEXTO = curr
            LOGO_IMAGE = load_arts(st.session_state.tema) if st.session_state.draw else None
            write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

            if manu.clicked:
                info = translate(load_file_temp(os.path.join(BASE, "info.txt")) or "")
                img = os.path.join(IMAGES, "matrix", st.session_state.tema.capitalize() + ".jpg")
                write_ypoema(info, img if os.path.exists(img) else None)

        if st.session_state.talk: talk(curr)

# --- MAIN ---
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

    pages = {2: page_ypoemas} # adiciona as outras: 1: page_mini, etc
    pages.get(int(chosen_id), page_ypoemas)()

    st.sidebar.image("img_ypoemas.jpg") # muda conforme chosen_id se quiser
    show_icons()

if __name__ == "__main__":
    main()
