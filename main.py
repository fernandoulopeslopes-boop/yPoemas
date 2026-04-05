import os
import random
import socket
import streamlit as st
from datetime import datetime

# --- 1. MOTOR: CONFIGURAÇÕES ---
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
    except socket.error:
        return False

if have_internet():
    try:
        from deep_translator import GoogleTranslator
        from gtts import gTTS
    except ImportError:
        pass

# --- 2. CONTEÚDO: CSS ---
st.markdown("""
    <style>
    footer {visibility: hidden;}
    [data-testid='stSidebar'] { overflow-x: hidden; }
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child { width: 310px; }
    div.stButton > button { padding: 2px 2px !important; font-size: 14px !important; width: 100% !important; white-space: nowrap !important; }
    [data-testid="column"] { padding: 0 2px !important; min-width: 0px !important; }
    .ypo_box {
        font-family: 'Courier New', Courier, monospace;
        background-color: #FAFAFA;
        padding: 25px; border: 1px solid #EEE;
        line-height: 1.5; font-size: 16px; color: #333;
    }
    .nav-links { font-family: 'Courier New', Courier, monospace; font-size: 14px; padding-bottom: 10px; text-align: center; }
    .nav-links a { color: #555; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONTEÚDO: SESSION STATE ---
if "lang" not in st.session_state: st.session_state.lang = "pt"
if "draw" not in st.session_state: st.session_state.draw = True
if "talk" not in st.session_state: st.session_state.talk = False
if "vydo" not in st.session_state: st.session_state.vydo = False
if "poly_lang" not in st.session_state: st.session_state.poly_lang = "ca"

# --- 4. MOTOR: MAPEAMENTO DE ARQUIVOS (RIGOROSO) ---
# Aqui o motor usa os nomes exatos que você enviou
MAPA_ARQUIVOS = {
    "Mini": "rol_mini.txt",
    "yPoemas": "rol_poemas.txt",
    "Eureka": "rol_jocosos.txt",
    "Biblioteca": "rol_outros autores.txt",
    "Livro Vivo": "rol_livro vivo.txt",
    "Ensaios": "rol_metalinguagem.txt",
    "Sobre": "info.txt"
}

@st.cache_data
def load_help(idiom):
    try:
        returns = []
        with open("./base/helpers.txt", encoding="utf-8") as file:
            for line in file:
                pipe = line.split("|")
                if pipe[1].strip().startswith(f"{idiom}_"):
                    returns.append(pipe[2].strip())
        return returns if len(returns) > 7 else ["ajuda"] * 10
    except: return ["..."] * 10

def get_ypoema(nome_aba, lang):
    f_name = MAPA_ARQUIVOS.get(nome_aba)
    if not f_name: return "ERRO: Aba não mapeada."
    
    f_path = os.path.join("base", f_name)
    
    if os.path.exists(f_path):
        with open(f_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        if not lines: return "ARQUIVO VAZIO."
        
        # Seleção aleatória do backup
        content = "\n".join(random.sample(lines, min(len(lines), 6)))
        
        if lang != "pt" and have_internet():
            try:
                return GoogleTranslator(source='pt', target=lang).translate(content)
            except: return content
        return content
    return f"ERRO: Arquivo {f_name} não encontrado."

# --- 5. SIDEBAR ---
st.sidebar.markdown('<div class="nav-links"><a href="https://github.com/NandouLopes/yPoemas">github</a> | <a href="https://youtu.be/uL6T3roTtAs">youtube</a></div>', unsafe_allow_html=True)

# Arte da Sidebar (Logo)
if os.path.exists("./images/logo.jpg"):
    st.sidebar.image("./images/logo.jpg", use_container_width=True)

with st.sidebar:
    # Idiomas
    c1, c2, c3, c4, c5, c6 = st.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
    if c1.button("pt"): st.session_state.lang = "pt"; st.rerun()
    if c2.button("es"): st.session_state.lang = "es"; st.rerun()
    if c3.button("it"): st.session_state.lang = "it"; st.rerun()
    if c4.button("fr"): st.session_state.lang = "fr"; st.rerun()
    if c5.button("en"): st.session_state.lang = "en"; st.rerun()
    if c6.button("⚒️"): st.session_state.lang = st.session_state.poly_lang; st.rerun()
    
    st.divider()
    
    # Sensores
    draw_text, talk_text, vyde_text = st.columns([3.8, 3.2, 3])
    help_tips = load_help(st.session_state.lang)
    st.session_state.draw = draw_text.checkbox(help_tips[5], st.session_state.draw)
    st.session_state.talk = talk_text.checkbox(help_tips[6], st.session_state.talk)
    st.session_state.vydo = vyde_text.checkbox(help_tips[7], st.session_state.vydo)

# --- 6. PALCO ---
paginas = ["Mini", "yPoemas", "Eureka", "Biblioteca", "Livro Vivo", "Ensaios", "Sobre"]
tabs = st.tabs([p.upper() for p in paginas])

for nome, tab in zip(paginas, tabs):
    with tab:
        conteudo = get_ypoema(nome, st.session_state.lang)
        col_txt, col_img = st.columns([2, 1])
        
        col_txt.markdown(f'<div class="ypo_box">{conteudo.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
        
        if st.session_state.talk and have_internet():
            try:
                tts = gTTS(text=conteudo, lang=st.session_state.lang)
                if not os.path.exists("temp"): os.makedirs("temp")
                tts.save("temp/voice.mp3")
                st.audio("temp/voice.mp3")
            except: pass

        if st.session_state.draw:
            # Busca a imagem correspondente à aba
            img_name = f"{nome.lower().replace(' ', '_')}.jpg"
            img_path = os.path.join("images", img_name)
            if os.path.exists(img_path):
                col_img.image(img_path, use_container_width=True)
