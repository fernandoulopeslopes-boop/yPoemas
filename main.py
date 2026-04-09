import streamlit as st
import extra_streamlit_components as stx
import os
import random

# CRONOLOGIA ATIVA: X=10 (v1.3 - Cockpit Sync & HTML Linebreaks)

try:
    from streamlit_autorefresh import st_autorefresh
    HAS_AUTO = True
except ImportError:
    HAS_AUTO = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- MOTOR ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(t, s=""): return f"Erro: Motor não localizado.\nTema: {t}"

# --- DADOS ---
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
            div[data-testid="column"] { display: flex; justify-content: center; align-items: center; }
            .stButton > button { 
                border-radius: 50% !important; width: 42px !important; height: 42px !important; 
                border: 1px solid #eee !important; background: white !important; color: #555 !important;
            }
            div[data-testid="stSelectbox"] { width: fit-content !important; min-width: 250px !important; margin: 0 auto !important; }
            div[data-baseweb="select"] { border: none !important; background: transparent !important; font-family: serif !important; font-size: 1.4em !important; font-weight: bold !important; }
            .poema-box { 
                font-family: serif; 
                font-size: 1.6em; 
                line-height: 1.7; 
                color: #1a1a1a; 
                margin-top: 2rem; 
                padding: 10px;
                text-align: left;
            }
        </style>
    """, unsafe_allow_html=True)

MAPA_BOOKS = {
    "todos os temas": "rol_todos os temas.txt", "livro vivo": "rol_livro_vivo.txt", 
    "ensaios": "rol_ensaios.txt", "jocosos": "rol_jocosos.txt", "variações": "rol_variações.txt", 
    "metalinguagem": "rol_metalinguagem.txt", "sociais": "rol_sociais.txt", 
    "outros autores": "rol_outros autores.txt", "todos os signos": "rol_todos os signos.txt", 
    "temas mini": "rol_temas_mini.txt"
}

def main():
    st.set_page_config(layout="wide", page_title="yPoemas")
    aplicar_estetica_machina()

    # --- ESTADOS ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 0 
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = 'todos os temas'
    if 'tema_idx_por_book' not in st.session_state: st.session_state.tema_idx_por_book = {b: 0 for b in MAPA_BOOKS}
    if 'com_imagem' not in st.session_state: st.session_state.com_imagem = True
    if 'show_config' not in st.session_state: st.session_state.show_config = False
    if 'seed_mutante' not in st.session_state: st.session_state.seed_mutante =
