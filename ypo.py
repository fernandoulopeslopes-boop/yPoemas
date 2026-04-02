import os
import re
import random
import base64
import streamlit as st
from lay_2_ypo import gera_poema 

# --- 1. CONFIGURAÇÃO VISUAL (SAMIZDÀT) ---
st.set_page_config(page_title='yPoemas | Samizdàt', layout='wide', initial_sidebar_state='expanded')

st.markdown('''
    <style>
    header, footer {visibility: hidden;}
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }
    
    /* Botões de Comando */
    .stButton>button { 
        width: 100%; height: 2.8em; font-weight: 700; font-size: 22px;
        border-radius: 4px; border: 1px solid #e0e0e0; background-color: #fcfcfc;
    }
    
    /* ÁREA LIVRE DO PALCO */
    .palco-sagrado {
        padding: 40px 10%;
        text-align: left;
    }
    
    .poema-texto-final { 
        font-weight: 600; 
        font-size: 32px; 
        font-family: 'IBM Plex Sans', sans-serif; 
        line-height: 1.6; 
        color: #111;
        white-space: pre-wrap;
        margin-top: 30px;
    }
    
    .poema-img-palco { 
        max-width: 600px; 
        border-radius: 2px; 
        box-shadow: 0px 10px 40px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }
    </style>
''', unsafe_allow_html=True)

# --- 2. ESTADOS E BASE ---
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'book' not in st.session_state: st.session_state.book = 'livro vivo'
if 'take' not in st.session_state: st.session_state.take = 0
for m in ['draw', 'audio']:
    if m not in st.session_state: st.session_state[m] = True

path_base = f'./base/rol_{st.session_state.book}.txt'
temas = []
if os.path.exists(path_base):
    with open(path_base, 'r', encoding='utf-8') as f:
        temas = [l.strip() for l in f if l.strip() and not l.startswith('[source')]

# --- 3. SIDEBAR ---
with st.sidebar:
    st.image('logo_ypo.png')
    st.write(f"### 📖 {st.session_state.book.upper()}")
    if temas:
        st.session_state.take = st.selectbox("↓ Localizar Tema", range(len(temas)), 
                                              index=st.session_state.take, 
                                              format_func=lambda x: temas[x])
    st.divider()
    st.session_state.draw = st.checkbox("Imagem (Draw)", st.session_state.draw)
    st.session_state.audio = st.checkbox("Áudio", st.session_state.audio)
    st.markdown('<div style="margin-top: 50px; font-style: italic; opacity: 0.6;">Edição: Samizdàt</div>', unsafe_allow_html=True)

# --- 4. O PALCO ---
if temas:
    # Barra de Navegação Superior (Única exceção de colunas para os botões)
    _, c_nav, _ = st.columns([0.1, 0.8, 0.1])
    with c_nav:
        btn = st.columns(5)
        if btn[0].button("+"): st.rerun()
        if btn[1].button("<"):
            st.session_state.take = (st.session_state.take - 1) % len(temas); st.rerun()
        if btn[2].button("*"):
            st.session_state.take = random.randint(0, len(temas)-1); st.rerun()
        if btn[3].button(">"):
            st.session_state.take = (st.session_state.take + 1) % len(temas); st.rerun()
        if btn[4].button("?"): st.toast("Navegação Ativa")

    st.divider()

    # PRODUÇÃO E LIMPEZA
    tema_atual = temas[st.session_state.take]
    poema_raw = gera_poema(tema_atual, "")
    texto_limpo = re.sub(r'<[^>]*>', '', "\n".join(poema_raw))
    texto_limpo = texto_limpo.replace("&emsp;", "    ").strip()

    # Imagem (Base64 para injeção direta no Palco)
    img_html = ""
    img_path = f"./images/machina/{tema_atual}.jpg"
    if st.session_state.draw and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        img_html = f'<img class="poema-img-palco" src="data:image/jpg;base64,{img_b64}">'

    # EXIBIÇÃO NA GRANDE ÁREA LIVRE
    st.markdown(f'''
        <div class="palco-sagrado">
            {img_html}
            <div class="poema-texto-final">{texto_limpo}</div>
        </div>
    ''', unsafe_allow_html=True)

    # Áudio
    audio_path = f"./audio/machina/{tema_atual}.mp3"
    if st.session_state.audio and os.path.exists(audio_path):
        st.audio(audio_path)
