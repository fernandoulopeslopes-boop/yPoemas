import os
import random
import base64
import streamlit as st
from lay_2_ypo import gera_poema 

# --- 1. CONFIGURAÇÃO E ESTÉTICA (SINAL LIMPO) ---
st.set_page_config(page_title='yPoemas', layout='centered', initial_sidebar_state='expanded')

st.markdown('''
    <style>
    header, footer {visibility: hidden;}
    .main { background-color: #ffffff; }
    /* Sidebar Travada em 310px para manter a identidade */
    [data-testid="stSidebar"] { min-width: 310px !important; max-width: 310px !important; width: 310px !important; }
    .block-container { padding-top: 1rem !important; max-width: 800px !important; }
    .container { display: flex; align-items: flex-start; }
    .logo-text { font-weight: 600; font-size: 19px; font-family: 'IBM Plex Sans', sans-serif; padding-left: 20px; line-height: 1.5; color: #000; }
    .logo-img { float: right; max-width: 400px; margin-left: 20px; }
    </style>
''', unsafe_allow_html=True)

# --- 2. ESTADO DA SESSÃO (A MEMÓRIA DA MÁQUINA) ---
if 'take' not in st.session_state: st.session_state.take = 0
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'poly_lang' not in st.session_state: st.session_state.poly_lang = 'la'
if 'draw' not in st.session_state: st.session_state.draw = True
if 'book' not in st.session_state: st.session_state.book = 'livro_vivo'

# --- 3. SIDEBAR (COMANDO IMEDIATO) ---
with st.sidebar:
    # Grid de Idiomas
    c1, c2, c3, c4, c5, c6 = st.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
    if c1.button("pt"): st.session_state.lang = 'pt'
    if c2.button("es"): st.session_state.lang = 'es'
    if c3.button("it"): st.session_state.lang = 'it'
    if c4.button("fr"): st.session_state.lang = 'fr'
    if c5.button("en"): st.session_state.lang = 'en'
    if c6.button("⚒️"): st.session_state.lang = st.session_state.poly_lang

    # Ordem de Imagem
    st.session_state.draw = st.checkbox("imagem", st.session_state.draw)
    
    st.image('logo_ypo.png')
    st.info("A ordem do leitor é o destino da Machina.")

# --- 4. O PALCO (NAVEGAÇÃO PELOS TEMAS) ---
path = f'./base/rol_{st.session_state.book}.txt'
temas = [line.strip() for line in open(path, 'r', encoding='utf-8') if line.strip()] if os.path.exists(path) else ["Fatos"]
max_idx = len(temas) - 1

# Botões de Navegação (Centralizados)
_, b1, b2, b3, _ = st.columns([3, 1, 1, 1, 3])
if b1.button("◀"): st.session_state.take = max_idx if st.session_state.take <= 0 else st.session_state.take - 1
if b2.button("✻"): st.session_state.take = random.randint(0, max_idx)
if b3.button("▶"): st.session_state.take = 0 if st.session_state.take >= max_idx else st.session_state.take + 1

# Selectbox (Apenas reflete e permite ajuste manual)
st.session_state.take = st.selectbox("↓ Lista de Temas", range(len(temas)), index=st.session_state.take, format_func=lambda x: temas[x])

# --- 5. GERAÇÃO E OUTPUT (O POEMA NO MUNDO) ---
tema_atual = temas[st.session_state.take]

# O motor recebe a ordem de idioma e tema simultaneamente
poema = gera_poema(tema_atual, "")
texto_final = "<br>".join(poema)

st.divider()

# Lógica de Imagem (Se a ordem 'draw' estiver ativa)
img_path = f"./images/machina/{tema_atual}.jpg"
if st.session_state.draw and os.path.exists(img_path):
    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    html_saida = f'''<div class="container">
                        <img class="logo-img" src="data:image/jpg;base64,{img_b64}">
                        <p class="logo-text">{texto_final}</p>
                     </div>'''
else:
    html_saida = f'<div class="container"><p class="logo-text">{texto_final}</p></div>'

st.markdown(html_saida, unsafe_allow_html=True)
