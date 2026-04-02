import os
import io
import re
import time
import random
import base64
import socket
import streamlit as st
import extra_streamlit_components as stx
from datetime import datetime

# O MOTOR ORIGINAL
from lay_2_ypo import gera_poema

# 1. CONFIGURAÇÃO DE PÁGINA (ESTRITO)
st.set_page_config(
    page_title='a Máquina de fazer Poesia - yPoemas',
    page_icon=':star:',
    layout='centered',
    initial_sidebar_state='auto',
)

# 2. CSS DE PRECISÃO (O "PORTAL LIMPO" DO OLD)
st.markdown(
    ''' <style>
    footer {visibility: hidden;}
    
    /* Força a Sidebar em 310px no Railway 2026 */
    [data-testid="stSidebar"] {
        min-width: 310px !important;
        max-width: 310px !important;
    }

    /* Padding Zero para colar os elementos */
    .block-container {
        padding-top: 0rem !important;
        padding-right: 1rem !important;
        padding-left: 1rem !important;
        padding-bottom: 0rem !important;
    }

    /* Estilo IBM Plex Sans para o Poema */
    .logo-text {
        font-weight: 600;
        font-size: 18px;
        font-family: 'IBM Plex Sans', sans-serif;
        color: #000000;
        border-left: 5px solid #000;
        padding-left: 15px;
        line-height: 1.5;
    }
    
    .logo-img {
        float: right;
        max-width: 250px;
        border: 1px solid #000;
        margin-left: 15px;
    }
    </style> ''',
    unsafe_allow_html=True,
)

# 3. LÓGICA DE REDE E TRADUÇÃO (RECUPERADA DO OLD)
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

def have_internet(host='8.8.8.8', port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except: return False

if have_internet():
    try:
        from deep_translator import GoogleTranslator
    except: pass

# 4. INICIALIZAÇÃO DE ESTADOS (TODOS OS ORIGINAIS)
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'last_lang' not in st.session_state: st.session_state.last_lang = 'pt'
if 'tema' not in st.session_state: st.session_state.tema = 'Feiras'
if 'poema_atual' not in st.session_state: st.session_state.poema_atual = ""
if 'draw' not in st.session_state: st.session_state.draw = False
if 'visy' not in st.session_state: st.session_state.visy = True

# 5. FUNÇÕES DE SUPORTE (AS "FERRAMENTAS" DO OLD)
def translate(input_text):
    if st.session_state.lang == 'pt' or not have_internet():
        return input_text
    try:
        return GoogleTranslator(source='pt', target=st.session_state.lang).translate(text=input_text)
    except: return input_text

def write_ypoema(text, img_path=None):
    text_html = text.replace('\n', '<br>')
    if img_path and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<div class="container"><img class="logo-img" src="data:image/jpg;base64,{img_b64}"><p class="logo-text">{text_html}</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="container"><p class="logo-text">{text_html}</p></div>', unsafe_allow_html=True)

# 6. SIDEBAR (O "CLIQUE" SECO)
with st.sidebar:
    st.image('logo_ypo.png')
    st.write("---")
    
    # Grid de idiomas original
    c1, c2, c3, c4, c5, c6 = st.columns([1.1, 1.1, 1.1, 1.1, 1.1, 1.2])
    if c1.button("pt"): st.session_state.lang = 'pt'
    if c2.button("es"): st.session_state.lang = 'es'
    if c3.button("it"): st.session_state.lang = 'it'
    if c4.button("fr"): st.session_state.lang = 'fr'
    if c5.button("en"): st.session_state.lang = 'en'
    if c6.button("⚒️"): st.session_state.lang = 'ca' # Exemplo de poly

    st.write("---")
    st.session_state.draw = st.checkbox(translate("imagem"), value=st.session_state.draw)

# 7. NAVEGAÇÃO E PÁGINAS
chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id=1, title="mini", description=''),
    stx.TabBarItemData(id=2, title="yPoemas", description=''),
    stx.TabBarItemData(id=3, title="eureka", description=''),
    stx.TabBarItemData(id=7, title="about", description=''),
], default=1)

if str(chosen_id) == '1':
    # PÁGINA MINI (RESTAURADA)
    col_space, col_btn, col_more, col_space2 = st.columns([4, 1, 1, 4])
    
    if col_btn.button("✻"):
        # Gera o poema e salva o estado
        poema_bruto = gera_poema(st.session_state.tema, "")
        st.session_state.poema_atual = "\n".join(poema_bruto)
    
    if st.session_state.poema_atual:
        texto_final = st.session_state.poema_atual
        if st.session_state.lang != 'pt':
            texto_final = translate(texto_final)
        
        img = None
        if st.session_state.draw:
            # Lógica de imagem simplificada para teste
            img = f'./images/matrix/{st.session_state.tema.capitalize()}.jpg'
            
        write_ypoema(texto_final, img)

# Rodapé de Ícones
st.sidebar.markdown("---")
st.sidebar.caption("facebook | e-mail | instagram")
