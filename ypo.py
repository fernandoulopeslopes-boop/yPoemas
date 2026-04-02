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

# O MOTOR DE GERAÇÃO NONE_LHÕES DE COMBINAÇÕES)
from lay_2_ypo import gera_poema

### bof: settings
st.set_page_config(
    page_title='a Máquina de fazer Poesia - yPoemas',
    page_icon=':star:',
    layout='centered',
    initial_sidebar_state='auto',
)

# --- FUNÇÕES DE CONEXÃO E TRADUÇÃO ---
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

# --- CSS ORIGINAL (PRESERVAÇÃO DO LAYOUT) ---
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
if 'tema' not in st.session_state: st.session_state.tema = 'Olhares'
if 'poema_atual' not in st.session_state: st.session_state.poema_atual = ""
if 'draw' not in st.session_state: st.session_state.draw = False
if 'talk' not in st.session_state: st.session_state.talk = False

# --- FERRAMENTAS DE UI ---
def write_ypoema(LOGO_TEXT, LOGO_IMAGE=None):
    texto_html = LOGO_TEXT.replace('\n', '<br>')
    if LOGO_IMAGE is None:
        st.markdown(f"<div class='container'><p class='logo-text'>{texto_html}</p></div>", unsafe_allow_html=True)
    else:
        try:
            with open(LOGO_IMAGE, "rb") as img_file:
                img_b64 = base64.b64encode(img_file.read()).decode()
            st.markdown(
                f'''<div class='container'>
                    <img class='logo-img' src='data:image/jpg;base64,{img_b64}'>
                    <p class='logo-text'>{texto_html}</p>
                </div>''', 
                unsafe_allow_html=True
            )
        except:
            st.markdown(f"<div class='container'><p class='logo-text'>{texto_html}</p></div>", unsafe_allow_html=True)

# --- PÁGINAS ---

def page_mini():
    # Garante a Capitalização para casar com os nomes dos arquivos (.txt/.Pip)
    tema_formatado = st.session_state.tema.capitalize()
    
    col_rand, col_info = st.columns([1, 4])
    
    if col_rand.button("✻"):
        # Chamada corrigida com dois argumentos e tratamento de erro
        try:
            poema_lista = gera_poema(tema_formatado, "") 
            st.session_state.poema_atual = "\n".join(poema_lista)
        except Exception as e:
            st.error(f"Erro no motor (Tema: {tema_formatado}): {e}")

    if st.session_state.poema_atual:
        write_ypoema(st.session_state.poema_atual)
    else:
        st.info("Clique no ✻ para iniciar a Machina.")

# --- ROTEADOR E MAIN ---
def main():
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="mini", description=''),
        stx.TabBarItemData(id=2, title="yPoemas", description=''),
        stx.TabBarItemData(id=3, title="eureka", description=''),
        stx.TabBarItemData(id=4, title="off-machina", description=''),
        stx.TabBarItemData(id=5, title="books", description=''),
        stx.TabBarItemData(id=6, title="poly", description=''),
        stx.TabBarItemData(id=7, title="sobre", description=''),
    ], default=1)

    with st.sidebar:
        if os.path.exists('logo_ypo.png'):
            st.image('logo_ypo.png')
        else:
            st.title("yPoemas")
        
        st.write("---")
        # Grid de idiomas
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

    # Navegação por IDs das abas
    if chosen_id == '1':
        page_mini()
    elif chosen_id in ['2','3','4','5','6','7']:
        st.warning(f"A aba {chosen_id} será construída na próxima etapa.")

if __name__ == "__main__":
    main()
