import os
import random
import base64
import streamlit as st
import extra_streamlit_components as stx
from lay_2_ypo import gera_poema

# --- 1. ESTÉTICA SAMIZDÁT (LITERAL DO OLD) ---
st.set_page_config(
    page_title='a Máquina de fazer Poesia - yPoemas',
    page_icon=':star:',
    layout='centered',
    initial_sidebar_state='expanded',
)

st.markdown('''
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .main { background-color: #ffffff; }
    [data-testid="stSidebar"] { min-width: 310px !important; max-width: 310px !important; }
    .block-container { padding-top: 1rem !important; max-width: 800px !important; }
    mark { background-color: lightblue; color: black; }
    .container { display: flex; align-items: flex-start; }
    .logo-text {
        font-weight: 600; font-size: 19px; font-family: 'IBM Plex Sans', sans-serif;
        color: #000000; padding-left: 20px; line-height: 1.5;
    }
    .logo-img { float: right; max-width: 400px; margin-left: 20px; }
    </style>
''', unsafe_allow_html=True)

# --- 2. ESTADOS DE SESSÃO ---
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'poly_lang' not in st.session_state: st.session_state.poly_lang = 'la'
if 'last_lang' not in st.session_state: st.session_state.last_lang = 'pt'
if 'book' not in st.session_state: st.session_state.book = 'livro_vivo'
if 'take' not in st.session_state: st.session_state.take = 0
if 'draw' not in st.session_state: st.session_state.draw = True

# --- 3. SIDEBAR (O PAINEL) ---
with st.sidebar:
    c1, c2, c3, c4, c5, c6 = st.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
    if c1.button("pt"): st.session_state.lang = 'pt'
    if c2.button("es"): st.session_state.lang = 'es'
    if c3.button("it"): st.session_state.lang = 'it'
    if c4.button("fr"): st.session_state.lang = 'fr'
    if c5.button("en"): st.session_state.lang = 'en'
    if c6.button("⚒️"):
        st.session_state.last_lang = st.session_state.lang
        st.session_state.lang = st.session_state.poly_lang

    col_d, _ = st.columns([1, 1])
    st.session_state.draw = col_d.checkbox("imagem", st.session_state.draw)
    
    st.image('logo_ypo.png')
    st.info("INFO_MINI: a máquina em estado de sorteio.")

# --- 4. O PALCO (A NAVEGAÇÃO) ---
tab = stx.tab_bar(data=[
    stx.TabBarItemData(id="y", title="yPoemas", description=""),
    stx.TabBarItemData(id="a", title="about", description=""),
], default="y")

if str(tab) == "y":
    # Carrega Temas
    path = f'./base/rol_{st.session_state.book}.txt'
    temas = [line.strip() for line in open(path, 'r', encoding='utf-8') if line.strip()] if os.path.exists(path) else ["Fatos"]
    max_idx = len(temas) - 1

    # Botões do Palco
    _, b1, b2, b3, _ = st.columns([3, 1, 1, 1, 3])
    if b1.button("◀"): st.session_state.take = max_idx if st.session_state.take <= 0 else st.session_state.take - 1
    if b2.button("✻"): st.session_state.take = random.randint(0, max_idx)
    if b3.button("▶"): st.session_state.take = 0 if st.session_state.take >= max_idx else st.session_state.take + 1

    # Lista de Temas
    st.session_state.take = st.selectbox("↓ Lista de Temas", range(len(temas)), index=st.session_state.take, format_func=lambda x: temas[x])
    
    tema_atual = temas[st.session_state.take]
    poema = gera_poema(tema_atual, "")

    # Exibição
    st.divider()
    
    img_path = f"./images/machina/{tema_atual}.jpg"
    if st.session_state.draw and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'''<div class="container"><img class="logo-img" src="data:image/jpg;base64,{b64}"><p class="logo-text">{"<br>".join(poema)}</p></div>''', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="container"><p class="logo-text">{"<br>".join(poema)}</p></div>', unsafe_allow_html=True)

else:
    st.write("Samizdát Digital v2.0")
