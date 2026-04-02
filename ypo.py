import os
import re
import random
import base64
import streamlit as st
from lay_2_ypo import gera_poema 

# --- 1. CONFIGURAÇÃO (SEM MARGENS LATERAIS NO PALCO) ---
st.set_page_config(page_title='yPoemas | Samizdàt', layout='wide', initial_sidebar_state='expanded')

# CSS FORÇADO (!important em tudo para garantir que mude)
st.markdown('''
    <style>
    header, footer {visibility: hidden;}
    
    /* BOTÕES COM ÍCONES VISÍVEIS E BORDAS FORTES */
    .stButton>button { 
        width: 100% !important; 
        height: 3.5em !important; 
        font-weight: 900 !important; 
        font-size: 28px !important; /* Aumentado para ver o símbolo */
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 3px solid #000000 !important;
        border-radius: 8px !important;
    }

    /* TÍTULO DO YPOEMA */
    .titulo-ypoema {
        font-family: 'serif';
        font-size: 20px;
        letter-spacing: 5px;
        color: #888;
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 50px;
        width: 100%;
    }

    /* TEXTO DO POEMA: GRANDE E LIMPO */
    .texto-poema {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 32px;
        line-height: 1.6;
        font-weight: 600;
        color: #111;
        white-space: pre-wrap;
        text-align: left;
        display: block;
        margin: 40px auto;
        max-width: 800px;
    }

    /* IMAGEM CENTRALIZADA */
    .img-centro {
        display: block;
        margin-left: auto;
        margin-right: auto;
        max-width: 600px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
    }
    </style>
''', unsafe_allow_html=True)

# --- 2. MEMÓRIA E BASE ---
if 'take' not in st.session_state: st.session_state.take = 0
if 'book' not in st.session_state: st.session_state.book = 'livro vivo'

path_base = f'./base/rol_{st.session_state.book}.txt'
temas = []
if os.path.exists(path_base):
    with open(path_base, 'r', encoding='utf-8') as f:
        temas = [l.strip() for l in f if l.strip() and not l.startswith('[source')]

# --- 3. SIDEBAR ---
with st.sidebar:
    st.image('logo_ypo.png')
    if temas:
        st.session_state.take = st.selectbox("Escolha o Tema", range(len(temas)), 
                                              index=st.session_state.take, 
                                              format_func=lambda x: temas[x])
    st.divider()
    draw_on = st.checkbox("Exibir Imagem", value=True)
    audio_on = st.checkbox("Habilitar Áudio", value=True)

# --- 4. O PALCO ---
if temas:
    # NAVEGAÇÃO: 5 Botões com Help Tips
    c1, c2, c3, c4, c5 = st.columns(5)
    if c1.button("+", help="Nova variação do mesmo tema"): st.rerun()
    if c2.button("<", help="Tema anterior"):
        st.session_state.take = (st.session_state.take - 1) % len(temas); st.rerun()
    if c3.button("*", help="Tema aleatório"):
        st.session_state.take = random.randint(0, len(temas)-1); st.rerun()
    if c4.button(">", help="Próximo tema"):
        st.session_state.take = (st.session_state.take + 1) % len(temas); st.rerun()
    if c5.button("?", help="Ajuda sobre o palco"):
        st.info("Use os símbolos para navegar. + gera nova versão, * sorteia tema.")

    st.divider()

    # TÍTULO (Ponto 2: Garantindo que apareça)
    tema_atual = temas[st.session_state.take]
    st.markdown(f'<div class="titulo-ypoema">—— {tema_atual} ——</div>', unsafe_allow_html=True)

    # GERAÇÃO E LIMPEZA (Ponto 3: Impedir que a 1ª linha vire título)
    poema_raw = gera_poema(tema_atual, "")
    
    # Limpeza Regex de qualquer tag HTML remanescente
    texto_limpo = "\n".join([re.sub(r'<[^>]*>', '', l).replace("&emsp;", "    ") for l in poema_raw])

    # IMAGEM (Ponto 4: Se imagem não selecionada, texto centraliza)
    if draw_on:
        img_path = f"./images/machina/{tema_atual}.jpg"
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<img src="data:image/jpg;base64,{img_b64}" class="img-centro">', unsafe_allow_html=True)

    # EXIBIÇÃO DO TEXTO (Ponto 5: Sempre limpo e formatado)
    st.markdown(f'<div class="texto-poema">{texto_limpo}</div>', unsafe_allow_html=True)

    # ÁUDIO
    if audio_on:
        audio_path = f"./audio/machina/{tema_atual}.mp3"
        if os.path.exists(audio_path):
            st.audio(audio_path)
