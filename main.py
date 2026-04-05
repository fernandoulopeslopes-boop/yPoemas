import os
import re
import time
import random
import base64
import socket
import streamlit as st

from extra_streamlit_components import TabBar as stx
from datetime import datetime
from lay_2_ypo import gera_poema

### bof: settings

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# PROTOCOLO DE LAYOUT: CSS INTEGRADO (Proteção contra encavalamento e Palco Central)
st.markdown(
    """
    <style>
    /* Estabilização da Sidebar */
    [data-testid="stSidebar"] {
        min-width: 310px;
        max-width: 310px;
    }
    
    /* Centralização e Respiro do Palco Principal */
    .main .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 2rem;
        margin: auto;
    }
    
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    mark {
      background-color: powderblue;
      color: black;
    }
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .logo-text {
        font-weight: 600;
        font-size: 20px;
        font-family: 'IBM Plex Sans', sans-serif;
        color: #1E1E1E;
        line-height: 1.6;
        text-align: center;
    }
    .logo-img {
        margin-bottom: 20px;
        max-width: 100%;
        height: auto;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False

# Initialize SessionState (Completo conforme Backup)
if "lang" not in st.session_state: st.session_state.lang = "pt"
if "book" not in st.session_state: st.session_state.book = "livro vivo"
if "take" not in st.session_state: st.session_state.take = 0
if "tema" not in st.session_state: st.session_state.tema = "Fatos"
if "draw" not in st.session_state: st.session_state.draw = True
if "talk" not in st.session_state: st.session_state.talk = False
if "vydo" not in st.session_state: st.session_state.vydo = False
if "arts" not in st.session_state: st.session_state.arts = []

hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

### bof: Protocolo de Funções Fixas

def translate(input_text):
    if st.session_state.lang == "pt" or not have_internet():
        return input_text
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
    except:
        return input_text

def pick_lang():
    st.sidebar.write("🌐 Idioma")
    cols = st.sidebar.columns(6)
    langs = ["pt", "es", "it", "fr", "en", "ca"]
    for i, l in enumerate(langs):
        if cols[i].button(l, key=f"btn_{l}"):
            st.session_state.lang = l

def draw_check_buttons():
    st.sidebar.write("🛠️ Ferramentas")
    c1, c2, c3 = st.sidebar.columns(3)
    st.session_state.draw = c1.checkbox("Imagem", value=st.session_state.draw)
    st.session_state.talk = c2.checkbox("Áudio", value=st.session_state.talk)
    st.session_state.vydo = c3.checkbox("Vídeo", value=st.session_state.vydo)

def load_temas(book_name):
    # Garante o formato correto para o arquivo rol_
    filename = f"./base/rol_{book_name.replace(' ', '_')}.txt"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["Fatos"]

def write_ypoema(text, img_path=None):
    if img_path and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"""<div class='container'><img class='logo-img' src='data:image/jpg;base64,{data}'><p class='logo-text'>{text}</p></div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class='container'><p class='logo-text'>{text}</p></div>""", unsafe_allow_html=True)

### bof: Interface Principal (Sidebar + Palco)

with st.sidebar:
    st.header("Machina")
    pick_lang()
    st.write("---")
    
    # Carregamento do seletor de livros
    books = ["livro vivo", "linguafiada", "faz de conto", "todos os temas"]
    selected_book = st.selectbox("Selecione o Livro", books, index=books.index(st.session_state.book))
    if selected_book != st.session_state.book:
        st.session_state.book = selected_book
        st.session_state.take = 0
        st.rerun()

    draw_check_buttons()
    st.write("---")
    
    # Navegação Secundária na Sidebar
    temas_disponiveis = load_temas(st.session_state.book)
    st.session_state.take = st.number_input("Índice", 0, len(temas_disponiveis)-1, value=st.session_state.take)
    st.session_state.tema = temas_disponiveis[st.session_state.take]

# Palco Principal
def run_machina():
    # Botões de controle no topo do palco
    col1, col2, col3 = st.columns([1, 2, 1])
    if col1.button("◀ Anterior"): 
        st.session_state.take -= 1
        st.rerun()
    if col2.button("✻ ALEATÓRIO"): 
        temas = load_temas(st.session_state.book)
        st.session_state.take = random.randint(0, len(temas)-1)
        st.rerun()
    if col3.button("Próximo ▶"): 
        st.session_state.take += 1
        st.rerun()

    # Proteção de índice
    temas = load_temas(st.session_state.book)
    st.session_state.take %= len(temas)
    st.session_state.tema = temas[st.session_state.take]

    # Geração do Poema (Passando o nome do tema limpo para o lay_2_ypo)
    try:
        script = gera_poema(st.session_state.tema, "")
        poema_html = "<br>".join(script)
        
        if st.session_state.lang != "pt":
            poema_html = translate(poema_html)
            
        # Lógica de Imagem
        img_file = None
        if st.session_state.draw:
            # Busca simples de imagem (ajuste conforme seu diretório real)
            img_dir = f"./images/matrix/{st.session_state.tema.capitalize()}.jpg"
            if os.path.exists(img_dir):
                img_file = img_dir

        write_ypoema(poema_html, img_file)
        
        if st.session_state.talk and have_internet():
            from gtts import gTTS
            tts = gTTS(text=poema_html.replace("<br>", "\n"), lang=st.session_state.lang)
            tts.save("temp_audio.mp3")
            st.audio("temp_audio.mp3")

    except Exception as e:
        st.error(f"Erro ao processar o tema '{st.session_state.tema}': {e}")
        st.info("Verifique se o arquivo .Pip correspondente existe na pasta base.")

if __name__ == "__main__":
    run_machina()
