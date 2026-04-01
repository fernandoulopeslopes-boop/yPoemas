import os
import re
import time
import random
import base64
import streamlit as st
from lay_2_ypo import gera_poema

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="yPoemas", layout="wide")

# --- CSS RADICAL (A "CARA DE HTML") ---
st.markdown(
    """ <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400&display=swap');

    /* Remove o estilo 'app' do Streamlit */
    .stApp { background-color: #e0e0e0; }
    header, footer { visibility: hidden !important; }
    .block-container { padding: 2rem !important; }

    /* O PALCO: Construção de Objeto Único */
    .palco-moldura {
        background-color: #ffffff;
        border: 2px solid #000;
        padding: 60px 80px;
        margin: 0 auto;
        max-width: 900px;
        min-height: 750px;
        box-shadow: 40px 40px 0px #bcbcbc; /* Sombra bruta */
        position: relative;
    }

    .poema-texto {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 300;
        font-size: 30px;
        color: #111;
        line-height: 1.3; /* Mais apertado = mais literário */
        white-space: pre-wrap;
    }

    .arte-tema {
        float: right;
        width: 340px;
        margin-left: 40px;
        margin-bottom: 20px;
        border: 2px solid #000;
        filter: grayscale(100%);
    }

    /* BOTÕES: Teclado de Máquina */
    .stButton>button {
        font-family: 'IBM Plex Mono', monospace !important;
        border-radius: 0px !important;
        border: 2px solid #000 !important;
        background: #fff !important;
        height: 65px !important;
        width: 90px !important;
        font-size: 26px !important;
        transition: 0.1s;
    }
    .stButton>button:hover { background: #000 !important; color: #fff !important; }
    .stButton>button:active { transform: translate(4px, 4px); }

    /* SIDEBAR PRETO ABSOLUTO */
    [data-testid="stSidebar"] { background-color: #000 !important; border-right: 5px solid #222; }
    [data-testid="stSidebar"] * { color: white !important; font-family: 'IBM Plex Mono'; }
    </style> """,
    unsafe_allow_html=True,
)

# --- LOGICA ---
if "poema_html" not in st.session_state:
    st.session_state.poema_html = ""

def get_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def montar_palco(tema, seed=""):
    linhas = gera_poema(tema, str(seed))
    corpo = "<br>".join(linhas)
    
    img_tag = ""
    img_b64 = get_b64(f"./arts/{tema.lower()}.jpg")
    if img_b64:
        img_tag = f'<img src="data:image/jpg;base64,{img_b64}" class="arte-tema">'
    
    st.session_state.poema_html = f"""
    <div class="palco-moldura">
        {img_tag}
        <div class="poema-texto">{corpo}</div>
    </div>
    """

# --- UI INTERFACE ---
with st.sidebar:
    st.title("MACHINA")
    st.selectbox("LIVRO", ["livro vivo", "arquivo morto"], key="book")
    st.toggle("Artes", value=True, key="draw")

# Navegação Centralizada
_, c1, c2, c3, c4, c5, _ = st.columns([2, 1, 1, 1, 1, 1, 2])
with c1: st.button("+")
with c2: st.button("<")
with c3: 
    if st.button("*"): montar_palco("Fatos") # Teste rápido
with c4: st.button(">")
with c5: st.button("⚒️")

st.markdown("---")

# Input de comando rápido
col_in, col_go = st.columns([5, 1])
tema_input = col_in.selectbox("Gatilho:", ["Fatos", "Tempo", "Anjos"], label_visibility="collapsed")
if col_go.button("GO"): 
    montar_palco(tema_input)

# --- RENDER FINAL ---
if st.session_state.poema_html:
    st.markdown(st.session_state.poema_html, unsafe_allow_html=True)
