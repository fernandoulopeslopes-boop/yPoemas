import os
import random
import base64
import socket
import streamlit as st
import extra_streamlit_components as stx
from datetime import datetime

# MOTOR DA MACHINA
from lay_2_ypo import gera_poema

# 1. SETTINGS ORIGINAIS
st.set_page_config(
    page_title='a Máquina de fazer Poesia - yPoemas',
    page_icon=':star:',
    layout='centered',
    initial_sidebar_state='auto',
)

# 2. CSS DE PRECISÃO (O "PORTAL LIMPO" DO YPO_OLD)
st.markdown(
    ''' <style>
    footer {visibility: hidden;}
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 310px;
    }
    .logo-text {
        font-weight: 600;
        font-size: 18px;
        font-family: 'IBM Plex Sans';
        color: #000000;
        padding-left: 15px;
        border-left: 5px solid #000;
    }
    .logo-img {
        float: right;
        max-width: 280px;
        border: 1px solid #000;
        margin-left: 15px;
    }
    </style> ''',
    unsafe_allow_html=True,
)

# 3. INITIALIZE SESSION STATE (ORIGINAL)
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'tema' not in st.session_state: st.session_state.tema = 'Fatos'
if 'draw' not in st.session_state: st.session_state.draw = False
if 'mini' not in st.session_state: st.session_state.mini = 0

# 4. TOOLS & LOADERS
def load_temas(book):
    try:
        with open(os.path.join('./base/rol_' + book + '.txt'), 'r', encoding='utf-8') as f:
            return [line.strip('\n') for line in f]
    except: return ['Fatos']

def write_ypoema(LOGO_TEXT, LOGO_IMAGE=None):
    if LOGO_IMAGE and os.path.exists(LOGO_IMAGE):
        with open(LOGO_IMAGE, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"<div class='container'><img class='logo-img' src='data:image/jpg;base64,{img_b64}'><p class='logo-text'>{LOGO_TEXT}</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='container'><p class='logo-text'>{LOGO_TEXT}</p></div>", unsafe_allow_html=True)

def pick_lang():
    btn_pt, btn_es, btn_it, btn_fr, btn_en, btn_xy = st.sidebar.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
    if btn_pt.button("pt"): st.session_state.lang = 'pt'
    if btn_es.button("es"): st.session_state.lang = 'es'
    if btn_it.button("it"): st.session_state.lang = 'it'
    if btn_fr.button("fr"): st.session_state.lang = 'fr'
    if btn_en.button("en"): st.session_state.lang = 'en'
    if btn_xy.button("⚒️"): st.session_state.lang = 'ca'

# 5. PAGES
def page_mini():
    st.sidebar.info("INFO_MINI: a máquina em estado de sorteio.")
    
    temas_list = load_temas('todos os temas')
    foo1, more, rand, demo, foo2 = st.columns([4, 1, 1, 1, 4])
    
    if rand.button("✻", help="gera novo yPoema"):
        st.session_state.mini = random.randrange(0, len(temas_list))
        st.session_state.tema = temas_list[st.session_state.mini]
        
        # Execução direta
        script = gera_poema(st.session_state.tema.capitalize(), "")
        poema_html = "<br>".join(script)
        
        logo_img = None
        if st.session_state.draw:
            logo_img = f'./images/matrix/{st.session_state.tema.capitalize()}.jpg'
            
        write_ypoema(poema_html, logo_img)

# 6. MAIN (ESTRUTURA DE NAVEGAÇÃO DO YPO_OLD)
def main():
    # Tab Bar do Old
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="mini", description=''),
        stx.TabBarItemData(id=2, title="yPoemas", description=''),
        stx.TabBarItemData(id=3, title="eureka", description=''),
        stx.TabBarItemData(id=4, title="off-machina", description=''),
        stx.TabBarItemData(id=5, title="books", description=''),
        stx.TabBarItemData(id=6, title="poly", description=''),
        stx.TabBarItemData(id=7, title="about", description=''),
    ], default=1)

    pick_lang()
    
    with st.sidebar:
        st.write("---")
        st.session_state.draw = st.checkbox("imagem", st.session_state.draw)
        st.image('logo_ypo.png')
        st.markdown("<nav>facebook | e-mail | instagram</nav>", unsafe_allow_html=True)

    # Lógica de roteamento do Old
    if str(chosen_id) == '1':
        page_mini()
    else:
        st.warning("Under Construction")

if __name__ == "__main__":
    main()

