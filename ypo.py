import os
import random
import base64
import streamlit as st
from lay_2_ypo import gera_poema 

# --- 1. CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title='yPoemas', layout='centered', initial_sidebar_state='expanded')

st.markdown('''
    <style>
    header, footer {visibility: hidden;}
    [data-testid="stSidebar"] { min-width: 310px !important; }
    .stButton>button { width: 100%; height: 2.2em; font-weight: 600; }
    .poema-container { display: flex; flex-direction: row; align-items: flex-start; gap: 30px; margin-top: 20px; }
    .poema-texto { font-weight: 600; font-size: 20px; font-family: 'IBM Plex Sans', sans-serif; line-height: 1.6; color: #000; flex: 1; }
    .poema-img { max-width: 380px; border-radius: 4px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
''', unsafe_allow_html=True)

# --- 2. ESTADOS DE MEMÓRIA (SESSION STATE) ---
if 'take' not in st.session_state: st.session_state.take = 0
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'book' not in st.session_state: st.session_state.book = 'livro_vivo'
if 'draw' not in st.session_state: st.session_state.draw = True
if 'video' not in st.session_state: st.session_state.video = False
if 'audio' not in st.session_state: st.session_state.audio = False

# --- 3. SIDEBAR: CENTRO DE COMANDO ---
with st.sidebar:
    st.image('logo_ypo.png')
    
    # IDIOMAS (Define a chave para o seu motor poly_lang)
    st.write("### 🌍 Idioma")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    if c1.button("pt"): st.session_state.lang = 'pt'; st.rerun()
    if c2.button("es"): st.session_state.lang = 'es'; st.rerun()
    if c3.button("it"): st.session_state.lang = 'it'; st.rerun()
    if c4.button("fr"): st.session_state.lang = 'fr'; st.rerun()
    if c5.button("en"): st.session_state.lang = 'en'; st.rerun()
    if c6.button("la"): st.session_state.lang = 'la'; st.rerun()

    st.divider()

    # MODOS DE SAÍDA
    st.write("### 🎬 Modos")
    st.session_state.draw = st.checkbox("Imagem (Draw)", st.session_state.draw)
    st.session_state.video = st.checkbox("Vídeo", st.session_state.video)
    st.session_state.audio = st.checkbox("Áudio", st.session_state.audio)

# --- 4. O PALCO (TEMAS E NAVEGAÇÃO) ---
path_base = f'./base/rol_{st.session_state.book}.txt'

if os.path.exists(path_base):
    with open(path_base, 'r', encoding='utf-8') as f:
        temas = [l.strip() for l in f if l.strip()]
    
    max_idx = len(temas) - 1

    # Botoes de Navegação
    col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])
    if col_nav1.button("◀ Tema"):
        st.session_state.take = max_idx if st.session_state.take <= 0 else st.session_state.take - 1
        st.rerun()
    if col_nav2.button("✻ Aleatório"):
        st.session_state.take = random.randint(0, max_idx)
        st.rerun()
    if col_nav3.button("Tema ▶"):
        st.session_state.take = 0 if st.session_state.take >= max_idx else st.session_state.take + 1
        st.rerun()

    # Seletor Sincronizado
    st.session_state.take = st.selectbox("↓ Localizar Tema", range(len(temas)), 
                                          index=st.session_state.take, 
                                          format_func=lambda x: temas[x])

    # --- 5. PRODUÇÃO E RENDERIZAÇÃO ---
    tema_atual = temas[st.session_state.take]
    
    # Chama o motor original
    poema = gera_poema(tema_atual, "") 
    texto_corpo = "<br>".join(poema)

    st.divider()

    # Lógica da Imagem
    img_path = f"./images/machina/{tema_atual}.jpg"
    img_html = ""
    if st.session_state.draw and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            img_encoded = base64.b64encode(f.read()).decode()
        img_html = f'<img class="poema-img" src="data:image/jpg;base64,{img_encoded}">'

    # Saída no Palco
    st.markdown(f'''
        <div class="poema-container">
            {img_html}
            <div class="poema-texto">{texto_corpo}</div>
        </div>
    ''', unsafe_allow_html=True)

else:
    st.error(f"Erro Crítico: Arquivo {path_base} não encontrado.")
    st.stop()
