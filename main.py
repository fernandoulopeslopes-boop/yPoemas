import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime

# 1. TENTA IMPORTAR O MOTOR (Sem quebrar se o arquivo estiver ausente)
try:
    from lay_2_ypo import gera_poema
except ImportError:
    st.error("Erro Crítico: 'lay_2_ypo.py' não encontrado no diretório.")
    st.stop()

# 2. CONFIGURAÇÕES DE INTERFACE (Devem vir antes de qualquer desenho)
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered"
)

# 3. INICIALIZAÇÃO DO ESTADO (SESSION STATE)
# Isso garante que todas as variáveis existam antes das funções serem chamadas
if "lang" not in st.session_state: st.session_state.lang = "pt"
if "last_lang" not in st.session_state: st.session_state.last_lang = "pt"
if "book" not in st.session_state: st.session_state.book = "livro vivo"
if "take" not in st.session_state: st.session_state.take = 0
if "mini" not in st.session_state: st.session_state.mini = 0
if "tema" not in st.session_state: st.session_state.tema = "Fatos"
if "visy" not in st.session_state: st.session_state.visy = True
if "draw" not in st.session_state: st.session_state.draw = False
if "talk" not in st.session_state: st.session_state.talk = False
if "vydo" not in st.session_state: st.session_state.vydo = False
if "arts" not in st.session_state: st.session_state.arts = []
if "auto" not in st.session_state: st.session_state.auto = False
if "nany_visy" not in st.session_state: st.session_state.nany_visy = 0

# Endereço IP para logs locais
IPAddres = socket.gethostbyname(socket.gethostname())

# ---------------------------------------------------------
# 4. DEFINIÇÃO DE TODAS AS FUNÇÕES (Onde a lógica mora)
# ---------------------------------------------------------

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except: return False

def translate(input_text):
    if st.session_state.lang == "pt" or not have_internet():
        return input_text
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
    except: return input_text

def pick_lang():
    st.sidebar.write("Idioma:")
    cols = st.sidebar.columns(6)
    btns = ["pt", "es", "it", "fr", "en", "⚒️"]
    for i, l in enumerate(btns):
        if cols[i].button(l, key=f"btn_{l}"):
            st.session_state.lang = l if l != "⚒️" else "ca"
            st.rerun()

def draw_check_buttons():
    st.sidebar.markdown("---")
    st.session_state.draw = st.sidebar.checkbox("Imagem", st.session_state.draw)
    st.session_state.talk = st.sidebar.checkbox("Áudio", st.session_state.talk)
    st.session_state.vydo = st.sidebar.checkbox("Vídeo", st.session_state.vydo)

@st.cache_data
def load_temas(book):
    path = f"./base/rol_{book}.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return ["Fatos"]

def load_poema_local(nome_tema):
    script = gera_poema(nome_tema, "")
    novo_poema = "<br>".join(script)
    return novo_poema

def write_ypoema(texto, img_path=None):
    if img_path and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div style='display: flex; align-items: center;'>
                <img src='data:image/jpg;base64,{data}' style='width: 150px; margin-right: 20px;'>
                <div style='font-family: serif; font-size: 1.2em;'>{texto}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='font-family: serif; font-size: 1.2em;'>{texto}</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. PÁGINAS (Módulos de visualização)
# ---------------------------------------------------------

def page_ypoemas():
    temas = load_temas(st.session_state.book)
    st.session_state.tema = st.selectbox("Selecione o Tema", temas, index=st.session_state.take)
    
    if st.button("Gerar yPoema"):
        poema = load_poema_local(st.session_state.tema)
        write_ypoema(poema)

# ---------------------------------------------------------
# 6. O MAESTRO (Execução Final)
# ---------------------------------------------------------

def main():
    # Carrega Sidebar
    with st.sidebar:
        st.title("Máquina de Poesia")
        pick_lang()
        draw_check_buttons()

    # Boas-vindas (Executa apenas uma vez)
    if st.session_state.visy:
        st.toast("Bem-vindo à Máquina!")
        st.session_state.visy = False

    # Menu de Navegação
    menu = ["yPoemas", "Mini", "Eureka", "Leituras"]
    escolha = st.sidebar.radio("Navegar por:", menu)

    if escolha == "yPoemas":
        page_ypoemas()
    else:
        st.info(f"Módulo {escolha} pronto para integração.")

if __name__ == "__main__":
    main()
