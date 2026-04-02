import os
import random
import base64
import streamlit as st
import extra_streamlit_components as stx
from lay_2_ypo import gera_poema 

# --- 1. ESTÉTICA DE COMBATE (YPO_OLD) ---
st.set_page_config(
    page_title='a Máquina de fazer Poesia - yPoemas',
    page_icon=':star:',
    layout='centered',
    initial_sidebar_state='expanded',
)

# CSS para matar o "layout padrão" e forçar a identidade da Machina
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

# --- 2. ESTADOS ---
if 'take' not in st.session_state: st.session_state.take = 0
if 'book' not in st.session_state: st.session_state.book = 'livro_vivo'
if 'draw' not in st.session_state: st.session_state.draw = True
if 'lang' not in st.session_state: st.session_state.lang = 'pt'

# --- 3. SIDEBAR (MARCA E INFO) ---
def sidebar_machina():
    with st.sidebar:
        # Grade de Idiomas
        c1, c2, c3, c4, c5, c6 = st.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
        if c1.button("pt"): st.session_state.lang = 'pt'
        if c2.button("es"): st.session_state.lang = 'es'
        if c3.button("it"): st.session_state.lang = 'it'
        if c4.button("fr"): st.session_state.lang = 'fr'
        if c5.button("en"): st.session_state.lang = 'en'
        if c6.button("⚒️"): st.session_state.lang = 'la'

        cd, ct = st.columns([1, 1])
        st.session_state.draw = cd.checkbox("imagem", st.session_state.draw)
        
        st.image('logo_ypo.png')
        st.info("INFO_MINI: a máquina em estado de sorteio.")

# --- 4. OUTPUT HTML ---
def write_ypoema(text, img_path):
    if img_path and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        html = f'<div class="container"><img class="logo-img" src="data:image/jpg;base64,{b64}"><p class="logo-text">{text}</p></div>'
    else:
        html = f'<div class="container"><p class="logo-text">{text}</p></div>'
    st.markdown(html, unsafe_allow_html=True)

# --- 5. O PALCO (INDIVIDUAL E INDEPENDENTE) ---
def page_ypoemas():
    path = f'./base/rol_{st.session_state.book}.txt'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            temas = [line.strip() for line in f if line.strip()]
    else:
        temas = ["Fatos"]
    
    max_idx = len(temas) - 1

    # BOTOES DE NAVEGAÇÃO DO PALCO
    col1, b_prev, b_rand, b_next, col5 = st.columns([3, 1, 1, 1, 3])
    
    if b_prev.button("◀"):
        st.session_state.take = max_idx if st.session_state.take <= 0 else st.session_state.take - 1
        
    if b_rand.button("✻"):
        st.session_state.take = random.randint(0, max_idx)
        
    if b_next.button("▶"):
        st.session_state.take = 0 if st.session_state.take >= max_idx else st.session_state.take + 1

    # SELECT BOX (Apenas para escolha direta, sem travar os botões)
    st.session_state.take = st.selectbox(
        "↓ Lista de Temas", 
        range(len(temas)), 
        index=st.session_state.take, 
        format_func=lambda x: temas[x]
    )

    tema_atual = temas[st.session_state.take]

    # Geração do Poema
    poema = gera_poema(tema_atual, "")
    
    # Imagem (Busca direta)
    img_path = f"./images/machina/{tema_atual}.jpg"
    logo_img = img_path if st.session_state.draw and os.path.exists(img_path) else None

    st.divider()
    write_ypoema("<br>".join(poema), logo_img)

# --- 6. MAIN ---
def main():
    sidebar_machina()
    
    tab = stx.tab_bar(data=[
        stx.TabBarItemData(id="y", title="yPoemas", description=""),
        stx.TabBarItemData(id="a", title="about", description=""),
    ], default="y")

    if str(tab) == "y":
        page_ypoemas()

if __name__ == '__main__':
    main()
