import os
import re
import random
import base64
import streamlit as st
from lay_2_ypo import gera_poema 

# --- 1. CONFIGURAÇÃO (SEM MARGENS LATERAIS) ---
st.set_page_config(page_title='yPoemas | Samizdàt', layout='wide', initial_sidebar_state='expanded')

# CSS Brutalista para forçar os botões e a fonte
st.markdown('''
    <style>
    header, footer {visibility: hidden;}
    
    /* BOTÕES COM BORDAS PRETAS GROSSAS */
    .stButton>button { 
        width: 100% !important; 
        height: 3em !important; 
        font-weight: 900 !important; 
        font-size: 30px !important; 
        color: #000 !important;
        background-color: #fff !important;
        border: 4px solid #000 !important; /* Borda bem grossa */
        border-radius: 0px !important;
    }

    /* TÍTULO EM DESTAQUE */
    .titulo-palco {
        font-family: serif;
        font-size: 24px;
        color: #777;
        text-align: center;
        letter-spacing: 4px;
        margin-bottom: 30px;
    }

    /* FORMATAÇÃO DO TEXTO DO POEMA */
    .poema-fonte {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 30px;
        font-weight: 600;
        line-height: 1.6;
        color: #111;
    }
    </style>
''', unsafe_allow_html=True)

# --- 2. LOGICA DE DADOS ---
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
        st.session_state.take = st.selectbox("Tema Selecionado", range(len(temas)), 
                                              index=st.session_state.take, 
                                              format_func=lambda x: temas[x])
    st.divider()
    draw_on = st.checkbox("Mostrar Imagem", value=True)
    audio_on = st.checkbox("Tocar Áudio", value=True)

# --- 4. O PALCO ---
if temas:
    # NAVEGAÇÃO (5 colunas)
    c1, c2, c3, c4, c5 = st.columns(5)
    # Usando ícones de texto puro para garantir visibilidade
    if c1.button("＋", help="Nova variação"): st.rerun()
    if c2.button("＜", help="Anterior"):
        st.session_state.take = (st.session_state.take - 1) % len(temas); st.rerun()
    if c3.button("＊", help="Aleatório"):
        st.session_state.take = random.randint(0, len(temas)-1); st.rerun()
    if c4.button("＞", help="Próximo"):
        st.session_state.take = (st.session_state.take + 1) % len(temas); st.rerun()
    if c5.button("？", help="Ajuda"):
        st.info("Comandos: + Variação | < Anterior | * Sorte | > Próximo")

    st.divider()

    # EXIBIÇÃO DO TÍTULO
    tema_atual = temas[st.session_state.take]
    st.markdown(f'<div class="titulo-palco">—— {tema_atual.upper()} ——</div>', unsafe_allow_html=True)

    # GERAÇÃO E LIMPEZA REAL DE TAGS
    poema_raw = gera_poema(tema_atual, "")
    
    # Processa linha por linha para garantir que o HTML suma e o recuo fique correto
    linhas_limpas = []
    for linha in poema_raw:
        # Remove qualquer coisa entre < > (Regex)
        texto = re.sub(r'<[^>]*>', '', linha)
        # Converte o recuo HTML para espaços de texto
        texto = texto.replace("&emsp;", "    ")
        linhas_limpas.append(texto)

    # Une com quebras de linha reais
    texto_final = "\n".join(linhas_limpas).strip()

    # ORGANIZAÇÃO DO CONTEÚDO NO CENTRO
    _, centro, _ = st.columns([0.15, 0.7, 0.15])
    
    with centro:
        # IMAGEM
        if draw_on:
            img_path = f"./images/machina/{tema_atual}.jpg"
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)

        # POEMA (Usando markdown mas injetando o texto limpo com suporte a quebra de linha)
        st.markdown(f'<div class="poema-fonte">{texto_final}</div>', unsafe_allow_html=True)

    # ÁUDIO
    if audio_on:
        audio_path = f"./audio/machina/{tema_atual}.mp3"
        if os.path.exists(audio_path):
            st.audio(audio_path)
