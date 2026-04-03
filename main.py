import streamlit as st
import random
import time
import os
import base64
import socket
from gtts import gTTS
from deep_translator import GoogleTranslator

# --- MOTOR DE 1983 ---
from lay_2_ypo import gera_poema

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="yPoemas 1983", layout="wide")
IPAddres = "sessao"

# --- GÊNESE (ESTADOS DE SESSÃO) ---
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

# --- AS ENGRENAGENS (FUNÇÕES) ---

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False

def translate(input_text):
    if st.session_state.lang == "pt": return input_text
    if not have_internet():
        st.session_state.lang = "pt"
        return input_text
    try:
        output_text = GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
        for tag in ["<br>>", "< br>", "<br >", "<br ", " br>"]:
            output_text = output_text.replace(tag, "<br>")
        return output_text
    except:
        return input_text

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
                line = line.strip().replace(" >", "\n").replace("< ", "\n")
                typo_text += line + "<br>"
    return typo_text

def load_images():
    with open("./base/images.txt", encoding="utf-8") as f: return f.readlines()

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
    st.markdown(html, unsafe_allow_html=True)

def load_md_file(file):
    try:
        with open(os.path.join("./md_files/" + file), encoding="utf-8") as f:
            text = f.read()
        return translate(text) if "rol_" not in file.lower() else text
    except:
        return "Erro ao abrir arquivo MD."

def load_info(nome_tema):
    with open("./base/info.txt", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("|"):
                p = line.split("|")
                if p[1].upper() == nome_tema.upper():
                    return f"<br>Titulo: {nome_tema}<br>Gênero: {p[2]}<br>Versos: {p[4]}<br>Análise: {p[8]}"
    return "nonono"

def load_help(idiom):
    tips = ["Anterior", "Sorteio", "Próximo", "Mais lidos", "Novo Poema", "Imagem", "Áudio", "Vídeo"]
    return [translate(t) for t in tips]

def load_readings():
    if not os.path.exists("./temp/read_list.txt"): return []
    with open("./temp/read_list.txt", encoding="utf-8") as f: return f.readlines()

def update_readings(tema):
    readings = load_readings()
    new_data = []
    found = False
    for line in readings:
        p = line.split("|")
        if len(p) > 1 and p[1] == tema:
            new_data.append(f"|{p[1]}|{int(p[2])+1}|\n")
            found = True
        else: new_data.append(line)
    if not found: new_data.append(f"|{tema}|1|\n")
    if not os.path.exists("./temp"): os.makedirs("./temp")
    with open("./temp/read_list.txt", "w", encoding="utf-8") as f: f.writelines(new_data)

def show_video(pagina):
    video_path = f"./base/video_{pagina}.webm"
    if os.path.exists(video_path):
        with open(video_path, "rb") as f: st.video(f.read(), format="webm")

# --- AS PÁGINAS ---

def page_mini():
    temas = load_temas(st.session_state.book)
    c1, c2, c3 = st.columns([1,1,1])
    if c2.button("✻"):
        st.session_state.tema = random.choice(temas)
    if st.session_state.tema:
        poema = load_poema(st.session_state.tema, "")
        if st.session_state.lang != "pt": poema = translate(poema)
        img = load_arts(st.session_state.tema) if st.session_state.draw else None
        write_ypoema(poema, img)
        update_readings(st.session_state.tema)

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list) - 1
    f1, more, last, rand, nest, manu, f2 = st.columns([3, 1, 1, 1, 1, 1, 3])
    if last.button("◀"): st.session_state.take = (st.session_state.take - 1) % maxy
    if rand.button("✻"): st.session_state.take = random.randint(0, maxy)
    if nest.button("▶"): st.session_state.take = (st.session_state.take + 1) % maxy
    st.session_state.tema = temas_list[st.session_state.take]
    poema = load_poema(st.session_state.tema, "")
    img = load_arts(st.session_state.tema) if st.session_state.draw else None
    write_ypoema(poema, img)

# --- EXECUÇÃO ---
if st.session_state.page == "mini":
    page_mini()
elif st.session_state.page == "ypoemas":
    page_ypoemas()
