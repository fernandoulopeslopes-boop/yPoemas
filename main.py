import streamlit as st
import os
import random
import base64
from gtts import gTTS
from io import BytesIO
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=69 (PROTOCOLO INTEGRAL - ZERO TAGS)
# FOCO: O uso de st.write ou st.text conforme o original para respeitar a normalização do HD.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")
TEMP_PATH = os.path.join(BASE_DIR, "temp")

if not os.path.exists(TEMP_PATH):
    os.makedirs(TEMP_PATH)

def load_typo(user_id):
    path = os.path.join(TEMP_PATH, f"TYPO_{user_id}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_ypoema(text, image=None):
    # O original utiliza a renderização nativa que respeita a string normalizada
    st.text(text)
    if image:
        st.image(image)

def main():
    st.set_page_config(layout="wide")
    
    if 'seed' not in st.session_state: st.session_state.seed = random.randint(1, 9999)
    if 'lang' not in st.session_state: st.session_state.lang = 'Português'
    if 'last_lang' not in st.session_state: st.session_state.last_lang = 'Português'
    if 'tema_idx' not in st.session_state: st.session_state.tema_idx = 0
    if 'book' not in st.session_state: st.session_state.book = "todos os temas"
    if 'talk' not in st.session_state: st.session_state.talk = False
    if 'draw' not in st.session_state: st.session_state.draw = False

    IPAddress = "SESSION_USER"

    arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_")])
    LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
    
    try:
        path_rol = os.path.join(BASE_PATH, LIVROS.get(st.session_state.book, "rol_todos os temas.txt"))
        with open(path_rol, "r", encoding="utf-8") as f:
            temas_list = [l.strip() for l in f if l.strip() and not l.startswith("[")]
        st.session_state.tema = temas_list[st.session_state.tema_idx % len(temas_list)]
    except:
        st.stop()

    # --- COCKPIT ---
    _, col_nav, _ = st.columns([1, 2, 1])
    with col_nav:
        c = st.columns(6)
        if c[0].button("✚"): 
            st.session_state.seed = random.randint(1, 9999)
            st.rerun()
        if c[1].button("❰"): 
            st.session_state.tema_idx -= 1
            st.rerun()
        if c[2].button("✱"): 
            st.session_state.seed = random.randint(1, 9999)
            st.session_state.tema_idx = random.randint(0, len(temas_list)-1)
            st.rerun()
        if c[3].button("❱"): 
            st.session_state.tema_idx += 1
            st.rerun()
        with c[5]:
            with st.popover("@"):
                langs = ['Português', 'Español', 'Italiano', 'English', 'Français']
                st.session_state.lang = st.selectbox("Idioma", langs, index=langs.index(st.session_state.lang))
                st.session_state.talk = st.checkbox("Talk", value=st.session_state.talk)
                st.session_state.draw = st.checkbox("Arts", value=st.session_state.draw)
        
        tema_sel = st.selectbox("V", temas_list, index=st.session_state.tema_idx % len(temas_list), label_visibility="collapsed")
        st.session_state.tema = tema_sel
        st.session_state.tema_idx = temas_list.index(tema_sel)

    st.divider()

    # --- PALCO ---
    from lay_2_ypo import gera_poema

    header = f"⚫ {st.session_
