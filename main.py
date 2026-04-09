import streamlit as st
import extra_streamlit_components as stx
try:
    from streamlit_autorefresh import st_autorefresh
    HAS_AUTO = True
except ImportError:
    HAS_AUTO = False

from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import os
import random

# --- CONFIGURAÇÃO DE AMBIENTE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- [PROTOCOL] MOTOR SOBERANO ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(t, s=""): return f"Erro: Motor não localizado.\nTema: {t}"

# --- CACHE & LOGICA DE DADOS ---
@st.cache_data
def carregar_temas_cached(arquivo_nome):
    caminho = os.path.join(BASE_DIR, "base", arquivo_nome)
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip() and not l.startswith("[")]
        except: pass
    return ["Fatos"]

@st.cache_data
def load_images_list_cached():
    caminho = os.path.join(BASE_DIR, "base", "images.txt")
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return f.readlines()
        except: pass
    return []

def load_arts(nome_tema):
    path = "./images/machina/"
    path_list = load_images_list_cached()
    for line in path_list:
        if line.startswith(nome_tema):
            this_line = line.strip("\n")
            part_line = this_line.partition(" : ")
            if nome_tema == part_line[0]:
                path = "./images/" + part_line[2] + "/"
                break
    if not os.path.exists(path): return None
    arts_list = [f for f in os.listdir(path) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
    if not arts_list: return None
    if 'arts' not in st.session_state: st.session_state.arts = []
    image = random.choice(arts_list)
    intentos = 0
    while image in st.session_state.arts and intentos < 10:
        image = random.choice(arts_list)
        intentos += 1
    st.session_state.arts.append(image)
    if len(st.session_state.arts) > 36: del st.session_state.arts[0]
    return path + image

def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            .block-container { padding-top: 1rem !important; max-width: 100% !important; }
            
            /* Sequência Sagrada Centralizada */
            .stButton > button { 
                border-radius: 50% !important; width: 42px !important; height: 42px !important; 
                border: 1px solid #eee !important; background: white !important; color: #555 !important;
            }
            
            /* Lista de Temas Light e Centralizada */
            div[data-testid="stSelectbox"] {
                width: fit-content !important;
                min-width: 150px !important;
                margin: 0 auto !important;
            }
            div[data-baseweb="select"] { 
                border: none !important; background: transparent !important; 
                font-family: serif !important; font-size: 1.1em !important; font-weight: bold !important;
            }
            
            /* Tipografia do Poema */
            .titulo-
