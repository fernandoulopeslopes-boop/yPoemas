import os
import re
import random
import streamlit as st
from lay_2_ypo import gera_poema 

# --- 1. CONFIGURAÇÃO DE TELA ---
st.set_page_config(page_title='yPoemas | Samizdàt', layout='wide', initial_sidebar_state='expanded')

# CSS TRANCADO
st.markdown('''
    <style>
    header, footer {visibility: hidden;}
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] { width: 300px !important; }

    /* BOTÕES PALCO: + ◀ ✴ ▶ ? */
    .stButton>button { 
        width: 100% !important; height: 3em !important; 
        font-size: 30px !important; font-weight: 900 !important;
        color: #000 !important; background-color: #fff !important;
        border: 3px solid #000 !important;
    }

    /* TÍTULO: COLADO NO TEXTO (Ponto 2) */
    .palco-titulo-fixo {
        font-family: sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: #000;
        text-align: center;
        text-transform: uppercase;
        margin: 0px 0 15px 0 !important; /* Espaço de 1 linha apenas */
    }

    /* CORPO DO TEXTO: 32px FIXO */
    .poema-linha-estrita {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 32px !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
        color: #111 !important;
        margin: 0 !important;
        white-space: pre-wrap !important;
    }

    .container-palco { max-width: 850px; margin: 0 auto; }
    </style>
''', unsafe_allow_html=True)

# --- 2. GESTÃO DE ESTADOS ---
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'take' not in st.session_state: st.session_state.take = 0
if 'book' not in st.session_state: st.session_state.book = 'livro vivo'

path_base = f'./base/rol_{st.session_state.book}.txt'
temas = []
if os.path.exists(path_base):
    with open(path_base, 'r', encoding='utf-8') as f:
        temas = [l.strip() for l in f if l.strip() and not l.startswith('[source')]

# --- 3. SIDEBAR (AÇÃO REAL) ---
with st.sidebar:
    st.image('logo_ypo.png')
    
    st.write("#### IDIOMA")
    col_pt, col_en = st.columns(2)
    # Atribuição direta e rerun para garantir a troca
    if col_pt.button("PT", use_container_width=True):
        st.session_state.lang = 'pt'
        st.rerun()
    if col_en.button("EN", use_container_width=True):
        st.session_state.lang = 'en'
        st.rerun()
    
    st.write(f"Ativo: **{st.session_state.lang.upper()}**")
    st.divider()

    if temas:
        st.session_state.take = st.selectbox("TEMA:", range(len(temas)), 
                                              index=st.session_state.take, 
                                              format_func=lambda x: temas[x])
    st.divider()
    
    # Checkboxes funcionais
    st.write("#### VITRINE")
    chk_arte = st.checkbox("Arte", value=True)
    chk_som = st.checkbox("Som", value=True)
    chk_video = st.checkbox("Vídeo", value=False)
    
    st.divider()
    st.caption("SAMIZDÀT EDITORA")

# --- 4. PALCO ---
if temas:
    # NAVEGAÇÃO
    c1, c2, c3, c4, c5 = st.columns(5)
    if c1.button("+"): st.rerun() # Botão de mais visível e funcional
    if c2.button("◀"):
        st.session_state.take = (st.session_state.take - 1) % len(temas); st.rerun()
    if c3.button("✴"):
        st.session_state.take = random.randint(0, len(temas)-1); st.rerun()
    if c4.button("▶"):
        st.session_state.take = (st.session_state.take + 1) % len(temas); st.rerun()
    if c5.button("?"):
        st.info(f"Linguagem: {st.session_state.lang.upper()}")

    st.divider()

    tema_atual = temas[st.session_state.take]
    st.markdown(f'<div class="palco-titulo-fixo">{tema_atual}</div>', unsafe_allow_html=True)

    # Geração respeitando a escolha de idioma
    poema_raw = gera_poema(tema_atual, st.session_state.lang)
    
    st.markdown('<div class="container-palco">', unsafe_allow_html=True)
    
    # Exibição Condicional (Arte)
    if chk_arte:
        img_path = f"./images/machina/{tema_atual}.jpg"
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.write("*(Arte em processamento...)*")

    # Texto com Tamanho Único
    for linha in poema_raw:
        texto_limpo = re.sub(r'<[^>]*>', '', linha).replace("&emsp;", "    ")
        if texto_limpo.strip() == "":
            st.markdown('<div style="height:1.2em;"></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p class="poema-linha-estrita">{texto_limpo}</p>', unsafe_allow_html=True)
    
    # Exibição Condicional (Som)
    if chk_som:
        audio_path = f"./audio/machina/{tema_atual}.mp3"
        if os.path.exists(audio_path):
            st.audio(audio_path)
        else:
            st.write("*(Som em processamento...)*")

    st.markdown('</div>', unsafe_allow_html=True)
