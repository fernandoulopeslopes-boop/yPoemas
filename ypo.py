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
    [data-testid="stSidebar"] { min-width: 280px !important; max-width: 280px !important; }
    .stButton>button { width: 100%; height: 2.2em; font-weight: 600; }
    
    .poema-container { 
        display: flex; 
        flex-direction: row; 
        align-items: flex-start; 
        gap: 50px; 
        padding: 20px 40px;
    }
    
    .poema-texto { 
        font-weight: 600; 
        font-size: 22px; 
        font-family: 'IBM Plex Sans', sans-serif; 
        line-height: 1.6; 
        color: #000; 
        flex: 1;
        max-width: 700px;
    }
    
    .poema-img { 
        max-width: 480px; 
        border-radius: 4px; 
        box-shadow: 2px 2px 20px rgba(0,0,0,0.1); 
    }
    </style>
''', unsafe_allow_html=True)

# --- 2. ESTADOS DE MEMÓRIA (SINCRONIA COM MOTOR) ---
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if "poly_lang" not in st.session_state: st.session_state.poly_lang = "ca"
if "poly_name" not in st.session_state: st.session_state.poly_name = "català"
if 'book' not in st.session_state: st.session_state.book = 'livro vivo'
if 'take' not in st.session_state: st.session_state.take = 0

for mode in ['draw', 'video', 'audio']:
    if mode not in st.session_state: st.session_state[mode] = (mode == 'draw')

# --- 3. SIDEBAR: COMANDOS ---
with st.sidebar:
    st.image('logo_ypo.png')
    
    st.write("### 🌍 Idioma")
    langs_fixos = ["pt", "es", "it", "fr", "en"]
    cols = st.columns(6)
    
    for i, l in enumerate(langs_fixos):
        if cols[i].button(l): 
            st.session_state.lang = l
            st.rerun()
    
    # O SEXTO BOTÃO: Dinâmico conforme poly_name (poly_lang)
    label_sexto = f"{st.session_state.poly_name} ({st.session_state.poly_lang})"
    if cols[5].button(label_sexto):
        st.session_state.lang = st.session_state.poly_lang
        st.rerun()

    st.divider()

    # O erro estava aqui. Agora usamos st.session_state.book de forma literal.
    # Se você quiser trocar de livro, basta alterar o valor padrão lá em cima.
    st.write(f"### 📖 Volume: {st.session_state.book.title()}")

    st.divider()
    st.write("### 🎬 Modos")
    st.session_state.draw = st.checkbox("Imagem (Draw)", st.session_state.draw)
    st.session_state.video = st.checkbox("Vídeo", st.session_state.video)
    st.session_state.audio = st.checkbox("Áudio", st.session_state.audio)

    st.markdown('<div style="margin-top: 50px; font-family: serif; font-style: italic;">Edição: Samizdàt</div>', unsafe_allow_html=True)

# --- 4. O PALCO ---
# Caminho respeitando exatamente o nome do arquivo enviado (ex: rol_livro vivo.txt)
path_base = f'./base/rol_{st.session_state.book}.txt'

if os.path.exists(path_base):
    with open(path_base, 'r', encoding='utf-8') as f:
        temas = [l.strip() for l in f if l.strip() and not l.startswith('[source')]
    
    if st.session_state.take >= len(temas): st.session_state.take = 0

    c_nav1, c_nav2, c_nav3 = st.columns([1, 1, 1])
    if c_nav1.button("◀ Tema"):
        st.session_state.take = (st.session_state.take - 1) % len(temas)
        st.rerun()
    if c_nav2.button("✻ Aleatório"):
        st.session_state.take = random.randint(0, len(temas)-1)
        st.rerun()
    if c_nav3.button("Tema ▶"):
        st.session_state.take = (st.session_state.take + 1) % len(temas)
        st.rerun()

    st.session_state.take = st.selectbox("↓ Localizar Tema", range(len(temas)), 
                                          index=st.session_state.take, 
                                          format_func=lambda x: temas[x])

    # --- 5. PRODUÇÃO ---
    tema_atual = temas[st.session_state.take]
    poema = gera_poema(tema_atual, "") 
    
    st.divider()
    
    header_col1, header_col2 = st.columns([0.8, 0.2])
    with header_col1:
        if 'poly_name' in st.session_state:
            st.subheader(st.session_state.poly_name)
    with header_col2:
        if 'poly_lang' in st.session_state:
            st.write(f"*{st.session_state.poly_lang}*")

    img_path = f"./images/machina/{tema_atual}.jpg"
    img_html = ""
    if st.session_state.draw and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            img_encoded = base64.b64encode(f.read()).decode()
        img_html = f'<img class="poema-img" src="data:image/jpg;base64,{img_encoded}">'

    st.markdown(f'''
        <div class="poema-container">
            {img_html}
            <div class="poema-texto">{"<br>".join(poema)}</div>
        </div>
    ''', unsafe_allow_html=True)
else:
    st.error(f"Arquivo não encontrado: {path_base}")
