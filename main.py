import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime
from deep_translator import GoogleTranslator
from gtts import gTTS

# --- 1. CONFIGURAÇÃO DE HARDWARE VIRTUAL (Rigor Geométrico) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon="ツ",
    layout="centered",
    initial_sidebar_state="auto",
)

st.markdown("""
    <style>
    /* SIDEBAR: Largura fixa de 320px conforme pactuado */
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }
    
    /* PALCO: Container de 800px centralizado para esmero visual */
    .main .block-container { max-width: 800px !important; padding-top: 2rem; }
    
    /* BOTÕES: Rosa, Circulares, 65px - Identidade Machina */
    div.stButton > button {
        background-color: #ff4b4b; color: white; border-radius: 50% !important;
        width: 65px !important; height: 65px !important; border: none;
        font-weight: bold; font-size: 24px; transition: 0.3s;
        display: flex; align-items: center; justify-content: center;
        margin: auto; box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    div.stButton > button:hover { background-color: #d33; transform: scale(1.1) rotate(5deg); }
    
    /* SELECTBOX: Estilo minimalista/collapsed */
    .stSelectbox label { display: none; }
    
    /* DIVISOR: O 'fio de navalha' em gradiente */
    hr { border: 0; height: 1px; background: linear-gradient(to right, transparent, #ff4b4b, transparent); margin: 2rem 0; }
    
    /* POESIA: Renderização do Subheader (Georgia Serif) */
    .stSubheader { font-family: 'Georgia', serif; font-weight: 400; text-align: center; color: #1a1a1a; line-height: 1.6; }
    
    /* IMAGEM: Estilo da logo-img do ypo_seguro */
    .logo-img { float: right; border-radius: 8px; margin-left: 20px; max-width: 300px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. MOTOR TÉCNICO (O Coração do ypo_seguro) ---

# Pacto de Idiomas: Apenas alfabeto ocidental
LISTA_IDIOMAS_OCIDENTAIS = [
    "Português", "English", "Español", "Français", "Italiano", "Deutsch", 
    "Nederlands", "Polski", "Dansk", "Svenska", "Norsk", "Suomi", "Română"
]

@st.cache_data
def motor_v32(tema):
    try:
        caminho = f"data/{tema}.ypo"
        if not os.path.exists(caminho): return ["Palco não encontrado."]
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = f.read().splitlines()
        poema = []
        for l in linhas:
            t = l.strip()
            # Filtro de metadados e marcas de build (F, _, números)
            if (not t or t.startswith(("#", "*-", "<EOF>")) or t == "F" or t.isdigit() or "_" in t):
                continue
            poema.append(random.choice(t.split("|")) if "|" in t else t)
        return poema
    except: return ["Erro no motor."]

def traduzir_machina(versos, destino):
    if destino == "Português": return versos
    try:
        texto_full = "\n".join(versos)
        traduzido = GoogleTranslator(source='auto', target=destino.lower()).translate(texto_full)
        return traduzido.split("\n")
    except: return versos

def write_ypoema_v32(texto_versos, img_path=None):
    # Reconstrução da lógica write_ypoema do ypo_seguro com esmero visual
    img_html = ""
    if img_path and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()
        img_html = f"<img class='logo-img' src='data:image/jpg;base64,{img_base64}'>"
    
    poema_html = "".join([f"<div class='stSubheader'>{v}</div>" for v in texto_versos])
    st.markdown(f"<div class='container'>{img_html}{poema_html}</div>", unsafe_allow_html=True)

# --- 3. GESTÃO DE ESTADO E SIDEBAR ---

if "tema" not in st.session_state: st.session_state.tema = "Fatos"
if "lang" not in st.session_state: st.session_state.lang = "Português"
if "draw" not in st.session_state: st.session_state.draw = True

with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>ツ Machina</h1>", unsafe_allow_html=True)
    
    # Seletor de Idiomas (O Pacto)
    st.session_state.lang = st.selectbox("Idioma", LISTA_IDIOMAS_OCIDENTAIS, index=0)
    
    st.markdown("---")
    
    # Seletor de Palcos
    arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
    st.session_state.tema = st.selectbox("Palco", arquivos, index=0)
    
    st.markdown("---")
    # Botões de Ação do ypo_seguro
    col_a, col_b = st.columns(2)
    talk_btn = col_a.button("Talk", key="tk")
    arte_btn = col_b.button("Arte", key="art")
    st.session_state.draw = st.checkbox("Exibir Arte", value=st.session_state.draw)

# --- 4. NAVEGAÇÃO E PALCO ---

# Menu Superior de 5 Colunas
nav = st.columns(5)
btns = ["+", "<", "*", ">", "?"]
for i, col in enumerate(nav):
    with col: st.button(btns[i], key=f"nav_{i}")

st.markdown("<hr>", unsafe_allow_html=True)

# Execução do Ciclo Poético
versos_raw = motor_v32(st.session_state.tema)
versos_traduzidos = traduzir_machina(versos_raw, st.session_state.lang)

# Busca de Imagem (Lógica load_arts simplificada para v.32)
img_final = None
if st.session_state.draw:
    # Simulação da busca de imagem por tema
    img_final = f"./images/matrix/{st.session_state.tema}.jpg" 

write_ypoema_v32(versos_traduzidos, img_final)

st.markdown("<hr>", unsafe_allow_html=True)
