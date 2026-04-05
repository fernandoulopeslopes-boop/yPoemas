import os
import random
import socket
import base64
import streamlit as st
from datetime import datetime

# Tenta importar dependências externas com fallback de segurança
try:
    from deep_translator import GoogleTranslator
    from gtts import gTTS
    INTERNET = True
except ImportError:
    INTERNET = False

# --- 1. CONFIGURAÇÃO DE PALCO (BACKUP SETTINGS) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- 2. O DNA ESTÉTICO (CSS ORIGINAL) ---
st.markdown(f"""
    <style>
    footer {{visibility: hidden;}}
    .reportview-container .main .block-container{{
        padding-top: 0rem;
        padding-right: 0rem;
        padding-left: 0rem;
        padding-bottom: 0rem;
    }}
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {{
        width: 310px;
    }}
    .logo-text {{
        font-weight: 600;
        font-size: 18px;
        font-family: 'Courier New', Courier, monospace;
        color: #000000;
        padding-left: 15px;
    }}
    .ypo_box {{
        font-family: 'Courier New', Courier, monospace;
        background-color: #FAFAFA;
        padding: 30px;
        border: 1px solid #EEE;
        line-height: 1.4;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZAÇÃO DE ESTADOS (SESSION STATE) ---
states = {
    "lang": "pt", "last_lang": "pt", "tema": "Fatos",
    "draw": True, "talk": False, "vydo": False,
    "current_ypoema": ""
}
for key, val in states.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- 4. FUNÇÕES DE SUPORTE ---
def get_ypoema(tema):
    f_path = f"base/rol_{tema.lower()}.txt"
    if os.path.exists(f_path):
        with open(f_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        raw = "\n".join(random.sample(lines, min(len(lines), 6)))
        if st.session_state.lang != "pt" and INTERNET:
            try:
                return GoogleTranslator(source='pt', target=st.session_state.lang).translate(raw)
            except: return raw
        return raw
    return "VÁCUO DETECTADO."

# --- 5. SIDEBAR: COCKPIT ORIGINAL ---
with st.sidebar:
    # PICK_LANG (Pesos decimais do backup)
    b_pt, b_es, b_it, b_fr, b_en, b_xy = st.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
    if b_pt.button("pt"): st.session_state.lang = "pt"
    if b_es.button("es"): st.session_state.lang = "es"
    if b_it.button("it"): st.session_state.lang = "it"
    if b_fr.button("fr"): st.session_state.lang = "fr"
    if b_en.button("en"): st.session_state.lang = "en"
    if b_xy.button("⚒️"): st.session_state.lang = "ca"

    st.divider()
    
    # DRAW_CHECK_BUTTONS
    st.session_state.draw = st.checkbox("Arts", st.session_state.draw)
    st.session_state.talk = st.checkbox("Talk", st.session_state.talk)
    st.session_state.vydo = st.checkbox("Vídeo", st.session_state.vydo)

# --- 6. O PALCO (TABS) ---
paginas = ["Mini", "yPoemas", "Eureka", "Biblioteca", "Livro Vivo", "Ensaios", "Sobre"]
tabs = st.tabs([p.upper() for p in paginas])

for nome, tab in zip(paginas, tabs):
    with tab:
        col_txt, col_img = st.columns([2, 1])
        
        if col_txt.button(nome.upper(), key=f"btn_{nome}"):
            st.session_state.tema = nome
            st.session_state.current_ypoema = get_ypoema(nome)
        
        if st.session_state.current_ypoema:
            col_txt.markdown(f'<div class="ypo_box">{st.session_state.current_ypoema.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
            
            if st.session_state.talk and INTERNET:
                tts = gTTS(text=st.session_state.current_ypoema, lang=st.session_state.lang)
                tts.save("temp_voice.mp3")
                st.audio("temp_voice.mp3")

            if st.session_state.draw:
                img_path = f"images/{nome.lower()}.jpg"
                if os.path.exists(img_path):
                    col_img.image(img_path, use_column_width=True)
