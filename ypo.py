import os
import random
import base64
import socket
import streamlit as st
import extra_streamlit_components as stx

# Import do motor de geração
from lay_2_ypo import gera_poema 

# --- SETTINGS ---
st.set_page_config(
    page_title='a Máquina de fazer Poesia - yPoemas',
    page_icon=':star:',
    layout='centered',
    initial_sidebar_state='auto',
)

# CSS Original para manter a "cara" do ypo_old
st.markdown(
    ''' <style>
    footer {visibility: hidden;}
    .reportview-container .main .block-container{
        padding-top: 0rem;
        padding-right: 0rem;
        padding-left: 0rem;
        padding-bottom: 0rem;
    }
    mark { background-color: lightblue; color: black; }
    .container { display: flex; }
    .logo-text {
        font-weight: 600;
        font-size: 18px;
        font-family: 'IBM Plex Sans';
        color: #000000;
        padding-left: 15px;
    }
    .logo-img { float:right; }
    </style> ''',
    unsafe_allow_html=True,
)

# --- INITIALIZE SESSION STATE ---
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'book' not in st.session_state: st.session_state.book = 'livro_vivo'
if 'take' not in st.session_state: st.session_state.take = 0
if 'tema' not in st.session_state: st.session_state.tema = 'Fatos'
if 'draw' not in st.session_state: st.session_state.draw = False
if 'talk' not in st.session_state: st.session_state.talk = False

# --- TOOLS EXTRAÍDAS DO OLD ---

def write_ypoema(LOGO_TEXT, LOGO_IMAGE):
    if LOGO_IMAGE == None:
        st.markdown(f"<div class='container'><p class='logo-text'>{LOGO_TEXT}</p></div>", unsafe_allow_html=True)
    else:
        img_base64 = base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()
        st.markdown(
            f'''
            <div class='container'>
                <img class='logo-img' src='data:image/jpg;base64,{img_base64}'>
                <p class='logo-text'>{LOGO_TEXT}</p>
            </div>
            ''',
            unsafe_allow_html=True,
        )

def pick_lang():
    btn_pt, btn_es, btn_it, btn_fr, btn_en, btn_xy = st.sidebar.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
    if btn_pt.button("pt", key=1): st.session_state.lang = 'pt'
    if btn_es.button("es", key=2): st.session_state.lang = 'es'
    if btn_it.button("it", key=3): st.session_state.lang = 'it'
    if btn_fr.button("fr", key=4): st.session_state.lang = 'fr'
    if btn_en.button("en", key=5): st.session_state.lang = 'en'
    if btn_xy.button("⚒️", key=6): st.session_state.lang = 'pt' # Fallback para o ícone

def draw_check_buttons():
    # Mantendo a organização de colunas da sidebar do ypo_old
    draw_col, talk_col, vyde_col = st.sidebar.columns([3.8, 3.2, 3])
    st.session_state.draw = draw_col.checkbox("imagem", st.session_state.draw)
    st.session_state.talk = talk_col.checkbox("áudio", st.session_state.talk)

def load_temas(book):
    path = os.path.join('./base/rol_' + book + '.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    return ["Fatos"]

def load_arts(nome_tema):
    # Lógica de busca de imagem conforme estrutura de pastas
    path_img = f'./images/machina/{nome_tema}.jpg'
    return path_img if os.path.exists(path_img) else None

# --- PAGES ---

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list) - 1

    # Grid de botões superior centralizado
    foo1, more, last, rand, nest, manu, foo2 = st.columns([3, 1, 1, 1, 1, 1, 3])
    
    if last.button("◀"):
        st.session_state.take = maxy if st.session_state.take <= 0 else st.session_state.take - 1
    if rand.button("✻"):
        st.session_state.take = random.randrange(0, maxy)
    if nest.button("▶"):
        st.session_state.take = 0 if st.session_state.take >= maxy else st.session_state.take + 1
    
    # Seletor de lista de temas
    st.session_state.take = st.selectbox(
        "↓ Lista de Temas",
        range(len(temas_list)),
        index=st.session_state.take,
        format_func=lambda z: temas_list[z]
    )
    
    st.session_state.tema = temas_list[st.session_state.take]

    # Geração do Poema via motor externo
    poema_raw = gera_poema(st.session_state.tema, '')
    LOGO_TEXT = "<br>".join(poema_raw)
    
    LOGO_IMAGE = None
    if st.session_state.draw:
        LOGO_IMAGE = load_arts(st.session_state.tema)

    # Exibição Final
    write_ypoema(LOGO_TEXT, LOGO_IMAGE)

# --- MAIN ---

def main():
    # Montagem da Sidebar exatamente como no old
    with st.sidebar:
        pick_lang()
        draw_check_buttons()
        st.image('logo_ypo.png')

    # Navegação por Tabs
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="yPoemas", description=''),
        stx.TabBarItemData(id=2, title="about", description=''),
    ], default=1)

    if str(chosen_id) == '1':
        page_ypoemas()
    else:
        st.write("Página Sobre em espera.")

if __name__ == '__main__':
    main()
