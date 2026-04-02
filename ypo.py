import os
import re
import random
import streamlit as st
from lay_2_ypo import gera_poema 

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title='yPoemas | Samizdàt', layout='wide', initial_sidebar_state='expanded')

st.markdown('''
    <style>
    header, footer {visibility: hidden;}
    
    /* LARGURA FIXA SIDEBAR */
    section[data-testid="stSidebar"] {
        width: 300px !important;
        min-width: 300px !important;
        max-width: 300px !important;
    }

    /* BOTÕES: SÍMBOLOS E BORDAS */
    .stButton>button { 
        width: 100% !important; 
        height: 3.5em !important; 
        font-size: 30px !important; 
        font-weight: 900 !important;
        color: #000 !important;
        background-color: #fff !important;
        border: 3px solid #000 !important;
    }

    /* TÍTULO */
    .palco-titulo {
        font-family: sans-serif;
        font-size: 18px;
        color: #999;
        text-align: center;
        letter-spacing: 5px;
        margin: 20px 0 40px 0;
    }

    /* CORPO DA LETRA ÚNICO */
    .poema-linha {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 30px !important;
        font-weight: 600 !important;
        line-height: 1.6 !important;
        color: #111 !important;
        text-align: left;
        margin: 0;
        padding: 0;
        white-space: pre-wrap;
    }

    .palco-central {
        max-width: 850px;
        margin: 0 auto;
    }
    </style>
''', unsafe_allow_html=True)

# --- 2. DADOS ---
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
        st.session_state.take = st.selectbox("Tema:", range(len(temas)), 
                                              index=st.session_state.take, 
                                              format_func=lambda x: temas[x])
    st.divider()
    st.markdown('<div style="font-style: italic; opacity: 0.5;">Edição: Samizdàt</div>', unsafe_allow_html=True)

# --- 4. PALCO ---
if temas:
    c1, c2, c3, c4, c5 = st.columns(5)
    
    if c1.button("+", help="Nova Variação"): st.rerun()
    if c2.button("◀", help="Anterior"):
        st.session_state.take = (st.session_state.take - 1) % len(temas); st.rerun()
    if c3.button("✴", help="Sorteio"):
        st.session_state.take = random.randint(0, len(temas)-1); st.rerun()
    if c4.button("▶", help="Próximo"):
        st.session_state.take = (st.session_state.take + 1) % len(temas); st.rerun()
    if c5.button("?", help="Ajuda"):
        st.info("+ Variação | ◀ Anterior | ✴ Sorte | ▶ Próximo")

    st.divider()

    tema_atual = temas[st.session_state.take]
    st.markdown(f'<div class="palco-titulo">—— {tema_atual.upper()} ——</div>', unsafe_allow_html=True)

    poema_raw = gera_poema(tema_atual, "")
    
    st.markdown('<div class="palco-central">', unsafe_allow_html=True)
    
    for linha in poema_raw:
        # Remoção de tags e tratamento de espaços
        texto_limpo = re.sub(r'<[^>]*>', '', linha).replace("&emsp;", "    ")
        if texto_limpo.strip() == "":
            st.markdown('<br>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p class="poema-linha">{texto_limpo}</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
