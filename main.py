import os
import re
import time
import random
import base64
import socket
import streamlit as st
import extra_streamlit_components as stx
from datetime import datetime
from lay_2_ypo import gera_poema

# =================================================================
# 1. SETTINGS & INTERFACE (CORREÇÃO DE LAYOUT)
# =================================================================

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="expanded",
)

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False

if have_internet():
    try:
        from deep_translator import GoogleTranslator
        from gtts import gTTS
    except ImportError:
        pass

st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .main .block-container {
        max-width: 900px;
        padding-top: 1.5rem;
    }
    [data-testid="stSidebar"] {
        min-width: 310px;
        max-width: 310px;
    }
    .logo-text {
        font-weight: 400;
        font-size: 20px;
        font-family: 'IBM Plex Sans', serif;
        color: #000000;
        line-height: 1.6;
    }
    .logo-img {
        float: right;
        margin-left: 20px;
        max-width: 280px;
        border-radius: 4px;
    }
    </style> """,
    unsafe_allow_html=True,
)

# =================================================================
# 2. SESSION STATE (PRESERVAÇÃO TOTAL)
# =================================================================

if "lang" not in st.session_state: st.session_state.lang = "pt"
if "book" not in st.session_state: st.session_state.book = "livro vivo"
if "take" not in st.session_state: st.session_state.take = 0
if "tema" not in st.session_state: st.session_state.tema = "Fatos"
if "visy" not in st.session_state: st.session_state.visy = True
if "draw" not in st.session_state: st.session_state.draw = True
if "talk" not in st.session_state: st.session_state.talk = False
if "vydo" not in st.session_state: st.session_state.vydo = False
if "arts" not in st.session_state: st.session_state.arts = []

# =================================================================
# 3. MOTORES E UTILITÁRIOS
# =================================================================

def translate(input_text):
    if st.session_state.lang == "pt" or not have_internet():
        return input_text
    try:
        return GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
    except:
        return input_text

def load_temas(book):
    try:
        path = os.path.join("./base/rol_" + book + ".txt")
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip().replace(" ", "") for line in f if line.strip()]
    except:
        return ["Fatos"]

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE=None):
    img_html = ""
    if LOGO_IMAGE and os.path.exists(LOGO_IMAGE):
        try:
            with open(LOGO_IMAGE, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode()
            img_html = f"<img class='logo-img' src='data:image/jpg;base64,{img_base64}'>"
        except: pass
    st.markdown(f"<div class='container'>{img_html}<p class='logo-text'>{LOGO_TEXTO}</p></div>", unsafe_allow_html=True)

# =================================================================
# 4. SIDEBAR (CONTEÚDO ORIGINAL)
# =================================================================

def draw_sidebar():
    with st.sidebar:
        st.title("Machina")
        
        # Seleção de Idioma
        cols = st.columns(5)
        langs = ["pt", "en", "es", "it", "fr"]
        for i, l in enumerate(langs):
            if cols[i].button(l.upper()):
                st.session_state.lang = l
                st.rerun()
        
        st.write("---")
        
        # Biblioteca
        livros = ["livro vivo", "clássicos", "experimental"]
        st.session_state.book = st.selectbox("Biblioteca", livros, index=livros.index(st.session_state.book))
        
        st.write("---")
        
        # Toggles
        st.session_state.draw = st.toggle("Imagem", st.session_state.draw)
        st.session_state.talk = st.toggle("Áudio", st.session_state.talk)
        st.session_state.vydo = st.toggle("Vídeo", st.session_state.vydo)
        
        st.write("---")
        st.caption(f"Status: Online | IP: {socket.gethostbyname(socket.gethostname())}")
        st.caption("Máquina de Fazer Poesia © 2026")

# =================================================================
# 5. PÁGINAS DO PALCO (DEFINIDAS)
# =================================================================

def page_mini():
    st.subheader("Pílula Poética")
    temas = load_temas("todos os temas")
    if st.button("✻ Girar"):
        st.session_state.take = random.randint(0, len(temas)-1)
    
    st.session_state.tema = temas[st.session_state.take % len(temas)]
    poema = "<br>".join(gera_poema(st.session_state.tema, "mini"))
    write_ypoema(translate(poema))

def page_ypoemas():
    temas = load_temas(st.session_state.book)
    c1, c2, c3 = st.columns([1, 4, 1])
    if c1.button("◄"): st.session_state.take -= 1
    if c3.button("►"): st.session_state.take += 1
    
    st.session_state.take %= len(temas)
    st.session_state.tema = temas[st.session_state.take]
    
    st.markdown(f"### {st.session_state.tema}")
    poema = "<br>".join(gera_poema(st.session_state.tema, "full"))
    write_ypoema(translate(poema))

def page_eureka():
    st.subheader("Busca Eureka")
    mote = st.text_input("Insira o mote da descoberta:")
    if mote:
        poema = "<br>".join(gera_poema(mote, "eureka"))
        write_ypoema(translate(poema))

# =================================================================
# 6. MAIN (ROTEAMENTO)
# =================================================================

def main():
    draw_sidebar()

    # Correção do TypeError e SyntaxError anterior
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
    ], default="2")

    if chosen_id == "1":
        page_mini()
    elif chosen_id == "2":
        page_ypoemas()
    elif chosen_id == "3":
        page_eureka()

if __name__ == "__main__":
    main()
