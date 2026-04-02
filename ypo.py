import os
import base64
import socket
import streamlit as st
import extra_streamlit_components as stx
from datetime import datetime

# O MOTOR ORIGINAL
from lay_2_ypo import gera_poema

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(
    page_title='a Máquina de fazer Poesia - yPoemas',
    page_icon=':star:',
    layout='centered',
    initial_sidebar_state='auto',
)

# 2. CSS DE PRECISÃO (RECUPERADO DO OLD)
st.markdown(
    ''' <style>
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {
        min-width: 310px !important;
        max-width: 310px !important;
    }
    .block-container {
        padding-top: 0rem !important;
    }
    .logo-text {
        font-weight: 600;
        font-size: 18px;
        font-family: 'IBM Plex Sans', sans-serif;
        color: #000000;
        border-left: 5px solid #000;
        padding-left: 15px;
        line-height: 1.5;
        margin-top: 20px;
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

# 3. ESTADOS INICIAIS
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'tema' not in st.session_state: st.session_state.tema = 'Fatos'
if 'mini' not in st.session_state: st.session_state.mini = 0

# 4. FUNÇÃO DE ESCRITA (IGUAL AO OLD)
def write_ypoema(LOGO_TEXT, LOGO_IMAGE=None):
    if LOGO_IMAGE is None or not os.path.exists(LOGO_IMAGE):
        st.markdown(f'<div class="container"><p class="logo-text">{LOGO_TEXT}</p></div>', unsafe_allow_html=True)
    else:
        with open(LOGO_IMAGE, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        st.markdown(
            f'''<div class="container">
                <img class="logo-img" src="data:image/jpg;base64,{img_b64}">
                <p class="logo-text">{LOGO_TEXT}</p>
            </div>''', unsafe_allow_html=True)

# 5. SIDEBAR (IDIOMAS)
with st.sidebar:
    st.image('logo_ypo.png')
    st.write("---")
    c1, c2, c3, c4, c5, c6 = st.columns([1.1, 1.1, 1.1, 1.1, 1.1, 1.2])
    if c1.button("pt"): st.session_state.lang = 'pt'
    if c2.button("es"): st.session_state.lang = 'es'
    if c3.button("it"): st.session_state.lang = 'it'
    if c4.button("fr"): st.session_state.lang = 'fr'
    if c5.button("en"): st.session_state.lang = 'en'
    if c6.button("⚒️"): st.session_state.lang = 'ca'
    
    st.write("---")
    st.session_state.draw = st.checkbox("imagem", value=False)

# 6. ABAS
chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id=1, title="mini", description=''),
    stx.TabBarItemData(id=2, title="yPoemas", description=''),
    stx.TabBarItemData(id=3, title="eureka", description=''),
    stx.TabBarItemData(id=7, title="about", description=''),
], default=1)

# 7. EXECUÇÃO DIRETA (PÁGINA MINI)
if str(chosen_id) == '1':
    # Layout de botões centralizados
    f1, more, rand, demo, f2 = st.columns([4, 1, 1, 1, 4])
    
    # O clique executa a máquina
    if rand.button("✻"):
        # Execução imediata sem rodeios
        script = gera_poema(st.session_state.tema.capitalize(), "")
        poema_html = "<br>".join(script)
        
        logo_img = None
        if st.session_state.draw:
            logo_img = f'./images/matrix/{st.session_state.tema.capitalize()}.jpg'
            
        write_ypoema(poema_html, logo_img)
