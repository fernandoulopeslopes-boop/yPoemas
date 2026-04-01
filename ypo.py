import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime
from lay_2_ypo import gera_poema

# --- CONFIGURAÇÃO DE PÁGINA ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS: O MOTOR VISUAL (PROPORÇÕES E HTML) ---
st.markdown(
    """ <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,600;1,300&display=swap');

    /* Reset de Margens Streamlit */
    .block-container { padding-top: 2rem; padding-bottom: 0rem; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* SIDEBAR: Largura Fixa e Estilo Escuro */
    [data-testid="stSidebar"] {
        background-color: #000;
        color: #fff;
        min-width: 310px !important; /* Resgatando a largura do seu fonte */
    }
    
    .sidebar-header-img {
        width: 100%;
        border-bottom: 2px solid #333;
        margin-bottom: 20px;
        filter: grayscale(100%);
    }

    /* O PALCO: A Geometria do Poema */
    .palco-container {
        display: flex;
        justify-content: center;
        width: 100%;
        padding: 20px;
    }

    .palco-moldura {
        background-color: #ffffff;
        border: 1px solid #111;
        padding: 50px 70px;
        width: 100%;
        max-width: 950px; /* Limita a largura para evitar desproporção */
        min-height: 600px;
        box-shadow: 35px 35px 0px #dcdcdc; /* Sombra sólida */
        position: relative;
        overflow: hidden;
    }

    .poema-texto {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 300;
        font-size: 28px;
        color: #111;
        line-height: 1.6;
        z-index: 2;
        position: relative;
    }

    /* ARTE: Posicionamento Orgânico */
    .arte-tema {
        float: right;
        width: 320px;
        height: auto;
        margin-left: 35px;
        margin-bottom: 20px;
        border: 1px solid #000;
        filter: grayscale(100%) contrast(105%);
        box-shadow: 10px 10px 0px #eee;
    }

    /* NAVEGAÇÃO: Simetria dos Botões (+ < * > ⚒️) */
    .nav-row {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-bottom: 40px;
    }

    .stButton>button {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 24px !important;
        font-weight: 600;
        border: 2px solid #000 !important;
        border-radius: 0px !important;
        background-color: #fff !important;
        color: #000 !important;
        height: 60px !important;
        width: 80px !important;
    }

    .stButton>button:hover {
        background-color: #000 !important;
        color: #fff !important;
        box-shadow: 5px 5px 0px #888;
    }

    /* Estilo de Inputs e Selects */
    .stSelectbox label, .stTextInput label { font-family: 'IBM Plex Mono'; color: #666; }
    </style> """,
    unsafe_allow_html=True,
)

# --- SESSION STATE ---
if "visy" not in st.session_state:
    st.session_state.update({
        "visy": True, "lang": "pt", "menu_nav": "Mini",
        "tema": "Fatos", "book": "livro vivo", "poema_html": "",
        "draw": True, "talk": False, "eureka_seed": ""
    })

# --- AUXILIARES ---
def get_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def processar_e_montar_html(tema, seed=""):
    # Gera o conteúdo bruto
    linhas = gera_poema(tema, str(seed))
    corpo_formatado = "<br>".join(linhas)
    
    # Busca imagem se 'draw' estiver ativo
    img_html = ""
    if st.session_state.draw:
        img_b64 = get_b64(f"./arts/{tema.lower()}.jpg")
        if img_b64:
            img_html = f'<img src="data:image/jpg;base64,{img_b64}" class="arte-tema">'
    
    # Monta a estrutura HTML que evita a "desproporcionalidade"
    st.session_state.poema_html = f"""
    <div class="palco-container">
        <div class="palco-moldura">
            {img_html}
            <div class="poema-texto">
                {corpo_formatado}
            </div>
        </div>
    </div>
    """

def carregar_rol(livro):
    slug = livro.replace(" ", "_")
    try:
        with open(f"./base/rol_{slug}.txt", "r", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip()]
    except: return ["Fatos", "Anjos", "Tempo", "Manifesto"]

# --- SIDEBAR FIXO ---
with st.sidebar:
    h_path = f"./assets/head_{st.session_state.menu_nav.lower()}.jpg"
    h_b64 = get_b64(h_path)
    if h_b64:
        st.markdown(f'<img src="data:image/jpg;base64,{h_b64}" class="sidebar-header-img">', unsafe_allow_html=True)
    
    st.session_state.book = st.selectbox("LIVRO ATIVO", ["livro vivo", "arquivo morto"])
    st.session_state.draw = st.toggle("Artes no Palco", st.session_state.draw)
    st.session_state.talk = st.toggle("Sintetizar Voz", st.session_state.talk)
    
    st.markdown("---")
    langs = {"Português": "pt", "English": "en", "Español": "es", "Italiano": "it"}
    st.session_state.lang = langs[st.selectbox("TRADUÇÃO", list(langs.keys()))]

# --- NAVEGAÇÃO DE FLUXO (+ < * > ⚒️) ---
# Usamos colunas centrais para manter a proporção dos botões
_, c1, c2, c3, c4, c5, _ = st.columns([2, 1, 1, 1, 1, 1, 2])
if c1.button("+"): st.session_state.menu_nav = "Mini"
if c2.button("<"): st.session_state.menu_nav = "yPoemas"
if c3.button("*"): 
    t_rand = random.choice(carregar_rol(st.session_state.book))
    processar_e_montar_html(t_rand)
if c4.button(">"): st.session_state.menu_nav = "Eureka"
if c5.button("⚒️"): st.session_state.menu_nav = "Config"

st.markdown("---")

# --- ÁREAS DE INTERAÇÃO ---
lista = carregar_rol(st.session_state.book)

if st.session_state.menu_nav == "Mini":
    col_m1, col_m2 = st.columns([5, 1])
    tema_m = col_m1.selectbox("Gatilho:", lista, label_visibility="collapsed")
    if col_m2.button("GO"): processar_e_montar_html(tema_m)

elif st.session_state.menu_nav == "yPoemas":
    tema_g = st.selectbox("Selecione o Tema da Galeria:", lista)
    if st.button("ABRIR ARQUIVO"): processar_e_montar_html(tema_g)

elif st.session_state.menu_nav == "Eureka":
    ce1, ce2 = st.columns([5, 1])
    st.session_state.eureka_seed = ce1.text_input("Chave Seed (Eurekas):", value=st.session_state.eureka_seed)
    tema_e = st.selectbox("Base de Garimpo:", lista)
    if st.button("GERAR"): processar_e_montar_html(tema_e, st.session_state.eureka_seed)

# --- RENDERIZAÇÃO DO PALCO (O PRODUTO FINAL) ---
if st.session_state.poema_html:
    st.markdown(st.session_state.poema_html, unsafe_allow_html=True)
