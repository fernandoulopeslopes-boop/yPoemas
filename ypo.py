import os
import random
import base64
import socket
import streamlit as st
import extra_streamlit_components as stx

# Motor de geração
from lay_2_ypo import gera_poema 

# 1. SETTINGS DE LAYOUT (O que dá a "cara" de verdade)
st.set_page_config(
    page_title='a Máquina de fazer Poesia - yPoemas',
    page_icon=':star:',
    layout='centered',
    initial_sidebar_state='auto',
)

# 2. INJEÇÃO DE CSS (Copiado literalmente do ypo_old)
st.markdown(
    ''' <style>
    footer {visibility: hidden;}
    
    /* Zera os paddings para o texto encostar nas bordas se necessário */
    .reportview-container .main .block-container{
        padding-top: 0rem;
        padding-right: 0rem;
        padding-left: 0rem;
        padding-bottom: 0rem;
    } 

    /* Largura fixa da Sidebar */
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 310px;
    }

    mark { background-color: lightblue; color: black; }
    .container { display: flex; }
    
    .logo-text {
        font-weight: 600;
        font-size: 18px;
        font-family: 'IBM Plex Sans';
        color: #000000;
        padding-top: 0px;
        padding-left: 15px;
    }
    .logo-img { float:right; }
    </style> ''',
    unsafe_allow_html=True,
)

# 3. ESTADOS DE SESSÃO
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'book' not in st.session_state: st.session_state.book = 'livro_vivo'
if 'take' not in st.session_state: st.session_state.take = 0
if 'draw' not in st.session_state: st.session_state.draw = True
if 'talk' not in st.session_state: st.session_state.talk = False
if 'tema' not in st.session_state: st.session_state.tema = 'Fatos'

# 4. FUNÇÕES DE SUPORTE (Fiel ao ypo_old)
def write_ypoema(LOGO_TEXT, LOGO_IMAGE):
    if LOGO_IMAGE == None:
        st.markdown(f"<div class='container'><p class='logo-text'>{LOGO_TEXT}</p></div>", unsafe_allow_html=True)
    else:
        img_encoded = base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()
        st.markdown(
            f'''
            <div class='container'>
                <img class='logo-img' src='data:image/jpg;base64,{img_encoded}'>
                <p class='logo-text'>{LOGO_TEXT}</p>
            </div>
            ''',
            unsafe_allow_html=True,
        )

def pick_lang():
    btn_pt, btn_es, btn_it, btn_fr, btn_en, btn_xy = st.sidebar.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
    if btn_pt.button("pt"): st.session_state.lang = 'pt'
    if btn_es.button("es"): st.session_state.lang = 'es'
    if btn_it.button("it"): st.session_state.lang = 'it'
    if btn_fr.button("fr"): st.session_state.lang = 'fr'
    if btn_en.button("en"): st.session_state.lang = 'en'
    if btn_xy.button("⚒️"): st.session_state.lang = 'pt'

def draw_check_buttons():
    draw_text, talk_text, vyde_text = st.sidebar.columns([3.8, 3.2, 3])
    st.session_state.draw = draw_text.checkbox("imagem", st.session_state.draw)
    st.session_state.talk = talk_text.checkbox("áudio", st.session_state.talk)

def load_temas(book):
    path = f'./base/rol_{book}.txt'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    return ["Fatos"]

# 5. PÁGINA PRINCIPAL
def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list) - 1

    # Grid de controle idêntico ao old
    foo1, more, last, rand, nest, manu, foo2 = st.columns([3, 1, 1, 1, 1, 1, 3])
    
    if last.button("◀"):
        st.session_state.take = maxy if st.session_state.take <= 0 else st.session_state.take - 1
    if rand.button("✻"):
        st.session_state.take = random.randrange(0, maxy)
    if nest.button("▶"):
        st.session_state.take = 0 if st.session_state.take >= maxy else st.session_state.take + 1
    
    # Seletor de temas
    st.session_state.take = st.selectbox(
        "↓ Lista de Temas",
        range(len(temas_list)),
        index=st.session_state.take,
        format_func=lambda z: temas_list[z]
    )
    
    st.session_state.tema = temas_list[st.session_state.take]

    # Geração
    poema_raw = gera_poema(st.session_state.tema, '')
    texto_formatado = "<br>".join(poema_raw)
    
    # Imagem (Busca direta na pasta machina)
    img_path = f"./images/machina/{st.session_state.tema}.jpg"
    logo_img = img_path if st.session_state.draw and os.path.exists(img_path) else None

    # O "INFO_MINI" na sidebar como solicitado
    st.sidebar.info("INFO_MINI: a máquina em estado de sorteio.")

    # Renderização
    write_ypoema(texto_formatado, logo_img)

# 6. MAIN
def main():
    with st.sidebar:
        pick_lang()
        draw_check_buttons()
        st.image('logo_ypo.png')

    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="yPoemas", description=''),
        stx.TabBarItemData(id=2, title="About", description=''),
    ], default=1)

    if str(chosen_id) == '1':
        page_ypoemas()

if __name__ == '__main__':
    main()
