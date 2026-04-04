import streamlit as st
import random
import time
import os
import base64
import socket
from gtts import gTTS
from deep_translator import GoogleTranslator

# --- 1. MOTOR DE 1983 ---
from lay_2_ypo import gera_poema

# --- 2. GÊNESE E CONFIGURAÇÃO ---
st.set_page_config(page_title="Machina 1983", layout="wide")
IPAddres = "sessao"

# Inicialização de Estados (Crucial para a Navegação)
if 'page' not in st.session_state: st.session_state.page = "mini"
if 'tema' not in st.session_state: st.session_state.tema = ""
if 'lang' not in st.session_state: st.session_state.lang = "pt"
if 'book' not in st.session_state: st.session_state.book = "todos os temas"
if 'draw' not in st.session_state: st.session_state.draw = True
if 'talk' not in st.session_state: st.session_state.talk = False
if 'take' not in st.session_state: st.session_state.take = 0

# --- 3. AS ENGRENAGENS (FUNÇÕES) ---

def translate(text):
    if st.session_state.lang == "pt": return text
    try:
        res = GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=text)
        return res.replace("<br>>", "<br>").replace("< br>", "<br>")
    except: return text

def write_ypoema(texto, img_path):
    st.markdown("""
        <style>
        .machina-container { display: flex; justify-content: space-between; align-items: flex-start; }
        .ypoema-text { font-family: 'IBM Plex Sans'; font-size: 1.3rem; line-height: 1.6; color: #333; width: 55%; }
        .ypoema-img { max-width: 40%; border: 1px solid #ddd; border-radius: 4px; }
        </style>
    """, unsafe_allow_html=True)
    
    html = "<div class='machina-container'>"
    html += f"<div class='ypoema-text'>{texto}</div>"
    if img_path and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        html += f"<img src='data:image/jpg;base64,{b64}' class='ypoema-img'>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def load_poema(tema):
    script = gera_poema(tema, "")
    path = f"./temp/LYPO_{IPAddres}"
    if not os.path.exists("./temp"): os.makedirs("./temp")
    texto_br = ""
    with open(path, "w", encoding="utf-8") as f:
        f.write(tema + "\n")
        for line in script:
            f.write(line + "\n")
            texto_br += line + "<br>"
    return texto_br

def load_temas_list():
    path = f"./base/rol_{st.session_state.book}.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip()]
    return ["ERRO_CARGA"]

# --- 4. SIDEBAR (NAVEGAÇÃO GLOBAL - O ALICERCE) ---
with st.sidebar:
    st.title("Machina 1983")
    st.write("---")
    if st.button("Página Mini", use_container_width=True): st.session_state.page = "mini"
    if st.button("Página yPoemas", use_container_width=True): st.session_state.page = "ypoemas"
    st.write("---")
    st.session_state.draw = st.toggle("Exibir Imagens", value=st.session_state.draw)
    st.session_state.talk = st.toggle("Ativar Voz", value=st.session_state.talk)
    
    idiomas = {"Português": "pt", "English": "en", "Español": "es"}
    escolha = st.selectbox("Idioma de Leitura", list(idiomas.keys()))
    st.session_state.lang = idiomas[escolha]

# --- 5. O PALCO (MINI) ---
def page_mini():
    temas = load_temas_list()
    
    # PONTE DE COMANDO (Navegação Interna)
    f1, b_more, b_rand, b_help, f2 = st.columns([3, 1, 1, 1, 3])
    
    clique_more = b_more.button("✚", help="Novos versos")
    clique_rand = b_rand.button("✻", help="Sortear Tema")
    clique_help = b_help.button("?", help="Manual")

    # Lógica de Sorteio e Geração
    if clique_rand or not st.session_state.tema:
        st.session_state.tema = random.choice(temas)
        st.session_state.current_text = load_poema(st.session_state.tema)
    elif clique_more:
        st.session_state.current_text = load_poema(st.session_state.tema)

    # Identidade do Expander
    label = f"⚫ {st.session_state.lang.upper()} | MINI | {st.session_state.tema.upper()}"
    
    with st.expander(label, expanded=True):
        final_text = translate(st.session_state.current_text)
        
        # A imagem agora só vem se for convidada (st.session_state.draw)
        img_convidada = None
        if st.session_state.draw:
            # Lógica de busca de imagem baseada no tema
            img_convidada = f"./images/machina/{st.session_state.tema.lower()}.jpg"

        write_ypoema(final_text, img_convidada)

    if clique_help:
        st.info("MANUAL MINI: Use ✻ para mudar o tema. Use ✚ para manter o tema e mudar os versos.")

# --- 6. O PALCO (YPOEMAS) ---
def page_ypoemas():
    st.title("yPoemas - Estação de Leitura")
    st.write("Em desenvolvimento...")

# --- DISPARO ---
if st.session_state.page == "mini":
    page_mini()
else:
    page_ypoemas()
