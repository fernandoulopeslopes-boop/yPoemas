import os
import random
import base64
import streamlit as st
from lay_2_ypo import gera_poema 

# --- 1. CONFIGURAÇÃO VISUAL (SAMIZDÀT) ---
st.set_page_config(page_title='yPoemas | Samizdàt', layout='wide', initial_sidebar_state='expanded')

st.markdown('''
    <style>
    header, footer {visibility: hidden;}
    [data-testid="stSidebar"] { min-width: 300px !important; max-width: 300px !important; }
    .stButton>button { width: 100%; height: 2.2em; font-weight: 600; }
    
    /* Palco Sagrado */
    .poema-container { 
        display: flex; 
        flex-direction: row; 
        align-items: flex-start; 
        gap: 60px; 
        padding: 60px 10% 20px 10%;
    }
    
    .poema-texto { 
        font-weight: 600; 
        font-size: 24px; 
        font-family: 'IBM Plex Sans', sans-serif; 
        line-height: 1.7; 
        color: #000; 
        flex: 1;
    }
    
    .poema-img { 
        max-width: 500px; 
        border-radius: 2px; 
        box-shadow: 0px 0px 25px rgba(0,0,0,0.05); 
    }
    </style>
''', unsafe_allow_html=True)

# --- 2. ESTADOS DE MEMÓRIA ---
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if "poly_lang" not in st.session_state: st.session_state.poly_lang = "ca"
if "poly_name" not in st.session_state: st.session_state.poly_name = "català"
if 'book' not in st.session_state: st.session_state.book = 'livro vivo'
if 'take' not in st.session_state: st.session_state.take = 0

for mode in ['draw', 'video', 'audio']:
    if mode not in st.session_state: st.session_state[mode] = (mode == 'draw')

# --- 3. SIDEBAR: COMANDOS E NAVEGAÇÃO ---
with st.sidebar:
    st.image('logo_ypo.png')
    
    st.write("### 🌍 Idioma")
    langs_fixos = ["pt", "es", "it", "fr", "en"]
    cols = st.columns(6)
    for i, l in enumerate(langs_fixos):
        if cols[i].button(l): 
            st.session_state.lang = l
            st.rerun()
    
    label_sexto = f"{st.session_state.poly_name} ({st.session_state.poly_lang})"
    if cols[5].button(label_sexto):
        st.session_state.lang = st.session_state.poly_lang
        st.rerun()

    st.divider()
    
    # NAVEGAÇÃO MOVIDA PARA A SIDEBAR
    st.write(f"### 📖 {st.session_state.book.upper()}")
    
    path_base = f'./base/rol_{st.session_state.book}.txt'
    temas = []
    if os.path.exists(path_base):
        with open(path_base, 'r', encoding='utf-8') as f:
            temas = [l.strip() for l in f if l.strip() and not l.startswith('[source')]
    
    if temas:
        c_nav1, c_nav2, c_nav3 = st.columns([1, 1, 1])
        if c_nav1.button("◀"):
            st.session_state.take = (st.session_state.take - 1) % len(temas)
            st.rerun()
        if c_nav2.button("✻"):
            st.session_state.take = random.randint(0, len(temas)-1)
            st.rerun()
        if c_nav3.button("▶"):
            st.session_state.take = (st.session_state.take + 1) % len(temas)
            st.rerun()

        st.session_state.take = st.selectbox("Temas do Livro:", range(len(temas)), 
                                              index=st.session_state.take, 
                                              format_func=lambda x: temas[x])

    st.divider()
    st.write("### 🎬 Modos")
    st.session_state.draw = st.checkbox("Imagem (Draw)", st.session_state.draw)
    st.session_state.audio = st.checkbox("Áudio", st.session_state.audio)
    st.session_state.video = st.checkbox("Vídeo", st.session_state.video)

    st.markdown('<div style="margin-top: 40px; font-family: serif; font-style: italic; opacity: 0.7;">Edição: Samizdàt</div>', unsafe_allow_html=True)

# --- 4. O PALCO (SAGRADO) ---
if temas:
    tema_atual = temas[st.session_state.take]
    poema = gera_poema(tema_atual, "") 
    
    # Renderização Condicional da Imagem
    img_html = ""
    img_path = f"./images/machina/{tema_atual}.jpg"
    if st.session_state.draw and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            img_encoded = base64.b64encode(f.read()).decode()
        img_html = f'<img class="poema-img" src="data:image/jpg;base64,{img_encoded}">'

    # Renderização do Poema e Imagem
    st.markdown(f'''
        <div class="poema-container">
            {img_html}
            <div class="poema-texto">{"<br>".join(poema)}</div>
        </div>
    ''', unsafe_allow_html=True)

    # Renderização Condicional do Áudio (Abaixo do conteúdo, discreto)
    audio_path = f"./audio/machina/{tema_atual}.mp3"
    if st.session_state.audio and os.path.exists(audio_path):
        st.audio(audio_path)

else:
    st.error(f"Volume '{st.session_state.book}' não disponível.")
