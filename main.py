import streamlit as st
import random
import time
import os
import base64
import socket
from gtts import gTTS
from deep_translator import GoogleTranslator

# --- 1. MOTOR DE 1983 (O CORAÇÃO) ---
from lay_2_ypo import gera_poema

# --- 2. CONFIGURAÇÃO E ESTADOS (A GÊNESE) ---
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

# --- 3. AS ENGRENAGENS (FUNÇÕES SUPORTE) ---

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except: return False

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
    except: return input_text

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
    path_lypo = os.path.join("./temp/LYPO_" + IPAddres)
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
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, "r", encoding="utf-8") as script:
            next(script) # Pula o nome do tema no topo
            for line in script:
                lypo_text += line.strip() + "<br>"
    return lypo_text

def load_arts(nome_tema):
    images_db_path = "./base/images.txt"
    path_final = "./images/machina/"
    if os.path.exists(images_db_path):
        with open(images_db_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(nome_tema):
                    path_final = "./images/" + line.strip().partition(" : ")[2] + "/"
                    break
    if not os.path.exists(path_final): return None
    arts_list = [f for f in os.listdir(path_final) if f.endswith(".jpg")]
    if not arts_list: return None
    image = random.choice(arts_list)
    st.session_state.arts.append(image)
    if len(st.session_state.arts) > 36: del st.session_state.arts[0]
    return path_final + image

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    st.markdown("""
        <style>
        .container { display: flex; align-items: flex-start; justify-content: space-between; }
        .logo-text { font-family: 'IBM Plex Sans'; font-weight: 600; font-size: 1.2rem; padding-left: 15px; }
        .logo-img { float: right; max-width: 40%; border-radius: 5px; border: 1px solid #ccc; }
        mark { background-color: powderblue; color: black; padding: 2px 5px; }
        </style>
    """, unsafe_allow_html=True)
    if LOGO_IMAGE:
        with open(LOGO_IMAGE, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode()
        html = f"<div class='container'><p class='logo-text'><mark>{LOGO_TEXTO}</mark></p><img class='logo-img' src='data:image/jpg;base64,{img_b64}'></div>"
    else:
        html = f"<div class='container'><p class='logo-text'><mark>{LOGO_TEXTO}</mark></p></div>"
    st.markdown(html, unsafe_allow_html=True)

def load_help(idiom):
    tips = ["Anterior", "Sorteio", "Próximo", "Mais lidos", "Novo Poema", "Imagem", "Áudio", "Vídeo"]
    return [translate(t) for t in tips]

def update_readings(tema):
    path = "./temp/read_list.txt"
    readings = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f: readings = f.readlines()
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
    with open(path, "w", encoding="utf-8") as f: f.writelines(new_data)

# --- 4. O PALCO (AS PÁGINAS) ---

def page_mini():
    temas_list = load_temas(st.session_state.book)
    help_tips = load_help(st.session_state.lang)
    
    # A PONTE (Navegação Interna)
    f1, more, rand, manu, f2 = st.columns([3, 1, 1, 1, 3])
    btn_more = more.button("✚", help=help_tips[4])
    btn_rand = rand.button("✻", help=help_tips[1])
    btn_manu = manu.button("?", help="help !!!")

    if btn_rand or not st.session_state.tema:
        st.session_state.tema = random.choice(temas_list)
        curr_ypoema = load_poema(st.session_state.tema, "")
    elif btn_more:
        curr_ypoema = load_poema(st.session_state.tema, "")
    else:
        curr_ypoema = load_lypo()

    # Identidade e Moldura
    what_book = f"⚫ {st.session_state.lang} ( MINI ) ( {st.session_state.tema.upper()} )"
    with st.expander(what_book, expanded=True):
        if st.session_state.lang != "pt": curr_ypoema = translate(curr_ypoema)
        img = load_arts(st.session_state.tema) if st.session_state.draw else None
        write_ypoema(curr_ypoema, img)
        update_readings(st.session_state.tema)
    
    if st.session_state.talk: talk(curr_ypoema)

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list) - 1
    help_tips = load_help(st.session_state.lang)
    
    f1, more, last, rand, nest, manu, f2 = st.columns([3, 1, 1, 1, 1, 1, 3])
    if last.button("◀", help=help_tips[0]): st.session_state.take = (st.session_state.take - 1) % maxy
    if rand.button("✻", help=help_tips[1]): st.session_state.take = random.randint(0, maxy)
    if nest.button("▶", help=help_tips[2]): st.session_state.take = (st.session_state.take + 1) % maxy
    
    st.session_state.tema = temas_list[st.session_state.take]
    curr_ypoema = load_poema(st.session_state.tema, "")
    
    what_book = f"⚫ {st.session_state.lang} ( {st.session_state.book} ) ( {st.session_state.take + 1}/{len(temas_list)} )"
    with st.expander(what_book, expanded=True):
        if st.session_state.lang != "pt": curr_ypoema = translate(curr_ypoema)
        img = load_arts(st.session_state.tema) if st.session_state.draw else None
        write_ypoema(curr_ypoema, img)
        update_readings(st.session_state.tema)

# --- 5. O SOPRO FINAL (DISPARO) ---
if st.session_state.page == "mini":
    page_mini()
elif st.session_state.page == "ypoemas":
    page_ypoemas()
