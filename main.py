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

### 0. PROTOCOLO DE LAYOUT (Axioma Zero: Estabilização de Interface)
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

st.markdown(
    """
    <style>
    /* Estabiliza largura da Sidebar para evitar encavalamento */
    [data-testid="stSidebar"] {
        min-width: 310px;
        max-width: 310px;
    }
    /* Centraliza o Palco Principal e define respiro */
    .main .block-container {
        max-width: 850px;
        padding: 2rem 1rem;
        margin: auto;
    }
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    mark { background-color: powderblue; color: black; }
    .container { display: flex; flex-direction: column; }
    .logo-text {
        font-weight: 600;
        font-size: 19px;
        font-family: 'IBM Plex Sans', sans-serif;
        color: #1E1E1E;
        line-height: 1.5;
    }
    .logo-img { float: right; margin-bottom: 15px; border-radius: 4px; }
    </style>
    """,
    unsafe_allow_html=True,
)

### 1. NÚCLEO DE FUNÇÕES (Backup Confiável)

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False

def translate(input_text):
    if st.session_state.lang == "pt" or not have_internet():
        return input_text
    try:
        from deep_translator import GoogleTranslator
        out = GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
        return out.replace("<br>>", "<br>").replace("< br>", "<br>").replace("<br >", "<br>")
    except:
        return input_text

def write_ypoema(text, img=None):
    if img and os.path.exists(img):
        with open(img, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"<div class='container'><img class='logo-img' src='data:image/jpg;base64,{data}'><p class='logo-text'>{text}</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='container'><p class='logo-text'>{text}</p></div>", unsafe_allow_html=True)

### 2. SESSION STATE (Carga Completa)

states = {
    "lang": "pt", "book": "livro vivo", "take": 0, "tema": "Fatos",
    "draw": True, "talk": False, "vydo": False, "visy": True,
    "poly_lang": "ca", "poly_name": "català"
}
for key, val in states.items():
    if key not in st.session_state:
        st.session_state[key] = val

### 3. SIDEBAR (Componentes de Controle)

with st.sidebar:
    st.title("Machina")
    # Seleção de Idioma
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    if c1.button("pt"): st.session_state.lang = "pt"
    if c2.button("es"): st.session_state.lang = "es"
    if c3.button("it"): st.session_state.lang = "it"
    if c4.button("fr"): st.session_state.lang = "fr"
    if c5.button("en"): st.session_state.lang = "en"
    if c6.button("⚒️"): st.session_state.lang = st.session_state.poly_lang
    
    st.write("---")
    # Seleção de Livro e Ferramentas
    st.session_state.book = st.selectbox("Acervo", ["livro vivo", "linguafiada", "faz de conto", "todos os temas"])
    
    draw_col, talk_col = st.columns(2)
    st.session_state.draw = draw_col.checkbox("Imagem", st.session_state.draw)
    st.session_state.talk = talk_col.checkbox("Áudio", st.session_state.talk)
    st.session_state.vydo = st.checkbox("Vídeo Tutorial", st.session_state.vydo)

### 4. NAVEGAÇÃO DE PÁGINAS (stx TabBar)

chosen_id = stx(data=[
    stx.Item(id="yPoemas", title="yPoemas"),
    stx.Item(id="Mini", title="Mini"),
    stx.Item(id="Eureka", title="Eureka"),
    stx.Item(id="About", title="About"),
], default="yPoemas")

### 5. PÁGINA PRINCIPAL (yPoemas)

def page_ypoemas():
    # Carregamento de Temas (rol_)
    filename = f"./base/rol_{st.session_state.book.replace(' ', '_')}.txt"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            temas = [line.strip() for line in f if line.strip()]
    except:
        temas = ["Fatos"]
    
    maxy = len(temas) - 1
    st.session_state.take %= len(temas)
    
    # OS 5 BOTÕES DE NAVEGAÇÃO DO PALCO (Protocolo Restaurado)
    f1, b_more, b_back, b_rand, b_next, b_help, f2 = st.columns([2, 1, 1, 1, 1, 1, 2])
    
    if b_back.button("◀"): st.session_state.take = (st.session_state.take - 1) % (maxy + 1)
    if b_rand.button("✻"): st.session_state.take = random.randint(0, maxy)
    if b_next.button("▶"): st.session_state.take = (st.session_state.take + 1) % (maxy + 1)
    show_more = b_more.button("✚")
    show_help = b_help.button("?")

    st.session_state.tema = temas[st.session_state.take]

    # Renderização do Poema
    with st.expander(f"⚫ {st.session_state.tema.upper()} ({st.session_state.take + 1}/{maxy + 1})", expanded=True):
        script = gera_poema(st.session_state.tema, "")
        poema_txt = "<br>".join(script)
        if st.session_state.lang != "pt":
            poema_txt = translate(poema_txt)
        
        # Lógica de Imagem (Busca por matriz)
        img_path = f"./images/matrix/{st.session_state.tema.capitalize()}.jpg"
        write_ypoema(poema_txt, img_path if st.session_state.draw else None)

    # CONTEÚDO CONDICIONAL (Só aparece se acionado)
    if show_help:
        st.info("ℹ️ Modo Help: Dados de análise e gráfico 3D da estrutura do poema.")
        # Chame aqui a sua função de gráfico ou info específica
        
    if show_more:
        st.success(f"Mais detalhes sobre o tema: {st.session_state.tema}")

# Execução conforme a aba selecionada
if chosen_id == "yPoemas":
    page_ypoemas()
else:
    st.write(f"Página {chosen_id} em standby. Foco na consistência da página principal.")
