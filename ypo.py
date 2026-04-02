import os
import random
import base64
import socket
import streamlit as st
import extra_streamlit_components as stx

# O MOTOR ORIGINAL
from lay_2_ypo import gera_poema

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(
    page_title='a Máquina de fazer Poesia - yPoemas',
    page_icon=':star:',
    layout='centered',
    initial_sidebar_state='auto',
)

# 2. CSS DE PRECISÃO (EXTRAÍDO DO SEU OLD)
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

# 3. LÓGICA DE TRADUÇÃO E REDE (Mínimo para rodar)
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'tema' not in st.session_state: st.session_state.tema = 'Fatos'
if 'draw' not in st.session_state: st.session_state.draw = False

# 4. LOADERS (Essenciais para o Sorteio de Temas)
def load_temas(book):
    try:
        with open(os.path.join('./base/rol_' + book + '.txt'), 'r', encoding='utf-8') as f:
            return [line.strip('\n') for line in f]
    except:
        return ['Fatos'] # Fallback caso o arquivo falhe

def write_ypoema(LOGO_TEXT, LOGO_IMAGE=None):
    if LOGO_IMAGE and os.path.exists(LOGO_IMAGE):
        with open(LOGO_IMAGE, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'''<div class='container'><img class='logo-img' src='data:image/jpg;base64,{img_b64}'><p class='logo-text'>{LOGO_TEXT}</p></div>''', unsafe_allow_html=True)
    else:
        st.markdown(f'''<div class='container'><p class='logo-text'>{LOGO_TEXT}</p></div>''', unsafe_allow_html=True)

# 5. SIDEBAR (O Coração do Portal)
def sidebar_original():
    with st.sidebar:
        # Idiomas (Grid do Old)
        c1, c2, c3, c4, c5, c6 = st.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
        if c1.button("pt"): st.session_state.lang = 'pt'
        if c2.button("es"): st.session_state.lang = 'es'
        if c3.button("it"): st.session_state.lang = 'it'
        if c4.button("fr"): st.session_state.lang = 'fr'
        if c5.button("en"): st.session_state.lang = 'en'
        if c6.button("⚒️"): st.session_state.lang = 'ca'

        st.write("---")
        # Checkboxes
        st.session_state.draw = st.checkbox("imagem", value=st.session_state.draw)
        
        st.write("---")
        st.image('logo_ypo.png')
        
        # Ícones Sociais
        st.markdown("<nav><a href='#'>facebook</a> | <a href='#'>e-mail</a> | <a href='#'>instagram</a></nav>", unsafe_allow_html=True)

# 6. PÁGINAS
def page_mini():
    temas_list = load_temas('todos os temas')
    foo1, more, rand, demo, foo2 = st.columns([4, 1, 1, 1, 4])
    
    if rand.button("✻"):
        st.session_state.tema = random.choice(temas_list)
        poema = gera_poema(st.session_state.tema.capitalize(), "")
        poema_html = "<br>".join(poema)
        
        img = None
        if st.session_state.draw:
            img = f'./images/matrix/{st.session_state.tema.capitalize()}.jpg'
            
        write_ypoema(poema_html, img)

# 7. MAIN (Navegação por Abas)
sidebar_original()

chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="1", title="mini", description=''),
    stx.TabBarItemData(id="2", title="yPoemas", description=''),
    stx.TabBarItemData(id="3", title="eureka", description=''),
    stx.TabBarItemData(id="7", title="about", description=''),
], default="1")

if chosen_id == "1":
    page_mini()
else:
    st.title("Under Construction")
