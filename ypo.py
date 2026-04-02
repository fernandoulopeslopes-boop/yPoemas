import os
import random
import base64
import streamlit as st
import extra_streamlit_components as stx
from lay_2_ypo import gera_poema 

# --- 1. CONFIGURAÇÃO E RESET VISUAL (O "EXTERMINADOR" DE QUINTAL) ---
st.set_page_config(
    page_title='a Máquina de fazer Poesia - yPoemas',
    page_icon=':star:',
    layout='centered',
    initial_sidebar_state='auto',
)

# ESTA É A PARTE QUE O STREAMLIT ESTAVA IGNORANDO:
st.markdown('''
    <style>
    /* 1. Mata o fundo padrão e margens excessivas */
    .main { background-color: #ffffff; }
    .reportview-container .main .block-container { padding: 0rem !important; }
    
    /* 2. Força a Sidebar a ter a largura do YPO_OLD (310px) e não metade da tela */
    [data-testid="stSidebar"] { width: 310px !important; min-width: 310px !important; }
    
    /* 3. Estética dos textos e imagens (O abraço do texto na imagem) */
    mark { background-color: lightblue; color: black; }
    .container { display: flex; align-items: flex-start; }
    .logo-text {
        font-weight: 600;
        font-size: 18px;
        font-family: 'IBM Plex Sans', sans-serif;
        color: #000000;
        padding-left: 15px;
        line-height: 1.4;
    }
    .logo-img { float: right; max-width: 45%; margin-left: 20px; }
    
    /* Remove o header inútil do Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
''', unsafe_allow_html=True)

# --- 2. SESSION STATE (COMPLETO) ---
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'last_lang' not in st.session_state: st.session_state.last_lang = 'pt'
if 'poly_lang' not in st.session_state: st.session_state.poly_lang = 'la'
if 'book' not in st.session_state: st.session_state.book = 'livro_vivo'
if 'take' not in st.session_state: st.session_state.take = 0
if 'draw' not in st.session_state: st.session_state.draw = True
if 'talk' not in st.session_state: st.session_state.talk = False

# --- 3. SIDEBAR (A MARCA DA MACHINA) ---
def sidebar_machina():
    with st.sidebar:
        # Idiomas - Colunas com proporção exata do OLD
        c1, c2, c3, c4, c5, c6 = st.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
        if c1.button("pt"): st.session_state.lang = 'pt'
        if c2.button("es"): st.session_state.lang = 'es'
        if c3.button("it"): st.session_state.lang = 'it'
        if c4.button("fr"): st.session_state.lang = 'fr'
        if c5.button("en"): st.session_state.lang = 'en'
        if c6.button("⚒️"):
            st.session_state.last_lang = st.session_state.lang
            st.session_state.lang = st.session_state.poly_lang
        
        # Checkboxes (draw e talk)
        col_draw, col_talk = st.columns([1, 1])
        st.session_state.draw = col_draw.checkbox("imagem", st.session_state.draw)
        st.session_state.talk = col_talk.checkbox("áudio", st.session_state.talk)
        
        st.image('logo_ypo.png')
        st.info("INFO_MINI: a máquina em estado de sorteio.")

# --- 4. FUNÇÕES DE OUTPUT ---
def write_ypoema(text, img_path):
    if img_path and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        html = f'''<div class="container"><img class="logo-img" src="data:image/jpg;base64,{b64}"><p class="logo-text">{text}</p></div>'''
    else:
        html = f'<div class="container"><p class="logo-text">{text}</p></div>'
    st.markdown(html, unsafe_allow_html=True)

# --- 5. PÁGINA PRINCIPAL ---
def page_ypoemas():
    path = f'./base/rol_{st.session_state.book}.txt'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            temas = [line.strip() for line in f if line.strip()]
    else:
        temas = ["Fatos"]

    # Navegação (Grid Centralizado)
    _, m1, m2, m3, m4, m5, _ = st.columns([2, 1, 1, 1, 1, 1, 2])
    if m2.button("◀"): st.session_state.take = (st.session_state.take - 1) % len(temas)
    if m3.button("✻"): st.session_state.take = random.randint(0, len(temas)-1)
    if m4.button("▶"): st.session_state.take = (st.session_state.take + 1) % len(temas)
    
    # Seletor de Temas
    idx = st.selectbox("↓ Lista de Temas", range(len(temas)), index=st.session_state.take, format_func=lambda x: temas[x])
    st.session_state.take = idx
    tema_atual = temas[idx]

    # Geração
    poema = gera_poema(tema_atual, "")
    texto_final = "<br>".join(poema)
    
    # Busca de Imagem
    img_path = f"./images/machina/{tema_atual}.jpg"
    logo_img = img_path if st.session_state.draw and os.path.exists(img_path) else None
    
    st.divider()
    write_ypoema(texto_final, logo_img)

# --- 6. MAIN ---
def main():
    sidebar_machina()
    
    tab = stx.tab_bar(data=[
        stx.TabBarItemData(id="y", title="yPoemas", description=""),
        stx.TabBarItemData(id="a", title="about", description=""),
    ], default="y")

    if tab == "y":
        page_ypoemas()
    else:
        st.write("Samizdát Digital v2.0")

if __name__ == '__main__':
    main()
