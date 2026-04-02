import os
import re
import random
import streamlit as st
from lay_2_ypo import gera_poema 

# --- CONFIGURAÇÃO E CSS ---
st.set_page_config(page_title='yPoemas | Samizdàt', layout='wide', initial_sidebar_state='expanded')

st.markdown('''
    <style>
    header, footer {visibility: hidden;}
    section[data-testid="stSidebar"] { width: 300px !important; }

    /* BOTÕES PALCO (GRANDES) */
    .stButton>button { 
        width: 100% !important; height: 3.2em !important; 
        font-size: 30px !important; font-weight: 900 !important;
        color: #000 !important; background-color: #fff !important;
        border: 3px solid #000 !important;
    }

    /* BOTÕES IDIOMA (PEQUENOS) */
    div[data-testid="stSidebar"] .stButton>button {
        height: 2.2em !important; font-size: 14px !important;
        font-weight: 600 !important; border: 1px solid #333 !important;
    }

    /* TÍTULO E TEXTO */
    .palco-titulo-fixo {
        font-family: sans-serif; font-size: 24px; font-weight: 700;
        color: #000; text-align: center; text-transform: uppercase;
        margin: 0px 0 10px 0 !important;
    }

    .poema-linha-estrita {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 32px !important; font-weight: 600 !important;
        line-height: 1.4 !important; color: #111 !important;
        margin: 0 !important; white-space: pre-wrap !important;
    }

    .container-palco { max-width: 850px; margin: 0 auto; }
    </style>
''', unsafe_allow_html=True)

# --- ESTADOS ---
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'take' not in st.session_state: st.session_state.take = 0

path_base = './base/rol_livro vivo.txt'
temas = []
if os.path.exists(path_base):
    with open(path_base, 'r', encoding='utf-8') as f:
        temas = [l.strip() for l in f if l.strip() and not l.startswith('[source')]

# --- SIDEBAR ---
with st.sidebar:
    st.image('logo_ypo.png')
    st.write("###### IDIOMA / LANGUAGE")
    c_pt, c_en = st.columns(2)
    if c_pt.button("PORTUGUÊS", key="l_pt"):
        st.session_state.lang = 'pt'
        st.rerun()
    if c_en.button("ENGLISH", key="l_en"):
        st.session_state.lang = 'en'
        st.rerun()
    
    st.divider()
    if temas:
        st.session_state.take = st.selectbox("TEMA:", range(len(temas)), 
                                              index=st.session_state.take, 
                                              format_func=lambda x: temas[x])
    st.divider()
    chk_art = st.checkbox("ARTE", value=True)
    chk_som = st.checkbox("SOM", value=True)

# --- PALCO ---
if temas:
    c1, c2, c3, c4, c5 = st.columns(5)
    if c1.button("+", key="bt_add"): st.rerun()
    if c2.button("◀", key="bt_pv"):
        st.session_state.take = (st.session_state.take - 1) % len(temas); st.rerun()
    if c3.button("✴", key="bt_rd"):
        st.session_state.take = random.randint(0, len(temas)-1); st.rerun()
    if c4.button("▶", key="bt_nx"):
        st.session_state.take = (st.session_state.take + 1) % len(temas); st.rerun()
    if c5.button("?", key="bt_hp"):
        st.info(f"Lang: {st.session_state.lang.upper()}")

    st.divider()
    tema_atual = temas[st.session_state.take]
    st.markdown(f'<div class="palco-titulo-fixo">{tema_atual}</div>', unsafe_allow_html=True)

    poema_raw = gera_poema(tema_atual, st.session_state.lang)
    
    st.markdown('<div class="container-palco">', unsafe_allow_html=True)
    if chk_art:
        img_path = f"./images/machina/{tema_atual}.jpg"
        if os.path.exists(img_path): st.image(img_path, use_container_width=True)

    for linha in poema_raw:
        txt = re.sub(r'<[^>]*>', '', linha).replace("&emsp;", "    ")
        if txt.strip() == "":
            st.markdown('<div style="height:1.2em;"></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p class="poema-linha-estrita">{txt}</p>', unsafe_allow_html=True)
    
    if chk_som:
        aud_path = f"./audio/machina/{tema_atual}.mp3"
        if os.path.exists(aud_path): st.audio(aud_path)
    st.markdown('</div>', unsafe_allow_html=True)
