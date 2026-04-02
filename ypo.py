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

# O MOTOR DE GERAÇÃO (BILHÕES DE COMBINAÇÕES)
from lay_2_ypo import gera_poema

### bof: settings
st.set_page_config(
    page_title='a Máquina de fazer Poesia - yPoemas',
    page_icon=':star:',
    layout='centered',
    initial_sidebar_state='auto',
)

# --- FUNÇÕES DE CONEXÃO E TRADUÇÃO (ESTILO ORIGINAL) ---
def have_internet(host='8.8.8.8', port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False

if have_internet():
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        pass
else:
    st.sidebar.warning('Internet não conectada.')

# --- CSS ORIGINAL (PRESERVAÇÃO ARQUEOLÓGICA) ---
st.markdown(
    ''' <style>
    footer {visibility: hidden;}
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 310px;
    }
    mark { background-color: lightblue; color: black; }
    .container { display: flex; flex-direction: column; }
    .logo-text {
        font-weight: 600;
        font-size: 18px;
        font-family: 'IBM Plex Sans';
        color: #000000;
        padding-top: 0px;
        padding-left: 15px;
        line-height: 1.4;
    }
    .logo-img { float:right; max-width: 300px; border: 1px solid #000; }
    </style> ''',
    unsafe_allow_html=True,
)

# --- INITIALIZE SESSION STATE ---
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'poly_lang' not in st.session_state: st.session_state.poly_lang = 'ca'
if 'tema' not in st.session_state: st.session_state.tema = 'Fatos'
if 'poema_atual' not in st.session_state: st.session_state.poema_atual = ""
if 'draw' not in st.session_state: st.session_state.draw = False
if 'talk' not in st.session_state: st.session_state.talk = False
if 'demo' not in st.session_state: st.session_state.demo = False

# --- FERRAMENTAS DE UI ---
def write_ypoema(LOGO_TEXT, LOGO_IMAGE=None):
    texto_html = LOGO_TEXT.replace('\n', '<br>')
    if LOGO_IMAGE is None:
        st.markdown(f"<div class='container'><p class='logo-text'>{texto_html}</p></div>", unsafe_allow_html=True)
    else:
        with open(LOGO_IMAGE, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode()
        st.markdown(
            f'''<div class='container'>
                <img class='logo-img' src='data:image/jpg;base64,{img_b64}'>
                <p class='logo-text'>{texto_html}</p>
            </div>''', 
            unsafe_allow_html=True
        )

# --- ROTEADOR E MAIN ---
def main():
    # BARRA DE ABAS (CORRIGIDA)
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="mini", description=''),
        stx.TabBarItemData(id=2, title="yPoemas", description=''),
        stx.TabBarItemData(id=3, title="eureka", description=''),
        stx.TabBarItemData(id=4, title="off-machina", description=''),
        stx.TabBarItemData(id=5, title="books", description=''),
        stx.TabBarItemData(id=6, title="poly", description=''),
        stx.TabBarItemData(id=7, title="sobre", description=''),
    ], default=1)

    # SIDEBAR RESTAURADA
    with st.sidebar:
        try:
            st.image('logo_ypo.png') 
        except:
            st.title("yPoemas")
        
        st.write("---")
        # Idiomas conforme ypo_old
        btn_pt, btn_es, btn_it, btn_fr, btn_en, btn_xy = st.columns([1, 1, 1, 1, 1, 1])
        if btn_pt.button("pt"): st.session_state.lang = 'pt'
        if btn_es.button("es"): st.session_state.lang = 'es'
        if btn_it.button("it"): st.session_state.lang = 'it'
        if btn_fr.button("fr"): st.session_state.lang = 'fr'
        if btn_en.button("en"): st.session_state.lang = 'en'
        if btn_xy.button("⚒️"): st.session_state.lang = st.session_state.poly_lang

        st.write(f"**Idioma:** {st.session_state.lang}")
        st.write("---")
        st.session_state.draw = st.checkbox("imagem", value=st.session_state.draw)
        st.session_state.talk = st.checkbox("áudio", value=st.session_state.talk)

    # NAVEGAÇÃO
    if chosen_id == '1':
        page_mini()
    elif chosen_id == '2':
        page_ypoemas()
    elif chosen_id == '3':
        page_eureka()
    elif chosen_id == '4':
        page_off_machina()
    elif chosen_id == '5':
        page_books()
    elif chosen_id == '6':
        page_polys()
    elif chosen_id == '7':
        page_abouts()

# --- PÁGINAS (CONSTRUÇÃO POR PARTES) ---

def page_mini():
    # Exemplo de interação com o motor na página Mini
    st.write(f"### Tema atual: {st.session_state.tema}")
    if st.button("✻ (Sorteia Poesia)"):
        poema_lista = gera_poema(st.session_state.tema)
        st.session_state.poema_atual = "\n".join(poema_lista)
    
    if st.session_state.poema_atual:
        write_ypoema(st.session_state.poema_atual)

def page_ypoemas():
    st.info("Página yPoemas: Aguardando construção da navegação de temas.")

def page_eureka():
    st.info("Página Eureka: Aguardando integração do léxico.")

def page_off_machina():
    st.info("Página Off-Machina: Aguardando carregamento de .Pip.")

def page_books():
    st.info("Página Books: Aguardando lista de bibliotecas.")

def page_polys():
    st.info("Página Poly: Aguardando seleção de dialetos.")

def page_abouts():
    st.info("Página Sobre: Reconstrução das informações do projeto.")

if __name__ == "__main__":
    main()
