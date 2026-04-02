import os
import re
import random
import streamlit as st
from lay_2_ypo import gera_poema 

# --- 1. CONFIGURAÇÃO DE TELA E BLOQUEIO DE ESTILO ---
st.set_page_config(page_title='yPoemas | Samizdàt', layout='wide', initial_sidebar_state='expanded')

st.markdown('''
    <style>
    header, footer {visibility: hidden;}
    
    /* BLOQUEIO DA SIDEBAR (300px fixos) */
    section[data-testid="stSidebar"] {
        width: 300px !important;
        min-width: 300px !important;
        max-width: 300px !important;
    }

    /* BOTÕES DE NAVEGAÇÃO: + ◀ ✴ ▶ ? */
    .stButton>button { 
        width: 100% !important; 
        height: 3.5em !important; 
        font-size: 32px !important; 
        font-weight: 900 !important;
        color: #000 !important;
        background-color: #fff !important;
        border: 3px solid #000 !important;
        border-radius: 4px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* TÍTULO DO YPOEMA: Centralizado, Preto, Fixo */
    .palco-titulo-fixo {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #000 !important;
        text-align: center !important;
        text-transform: uppercase !important;
        letter-spacing: 4px !important;
        margin: 30px 0 50px 0 !important;
        display: block !important;
    }

    /* CORPO DO TEXTO: Tamanho Único (32px) para todas as linhas */
    .poema-linha-estrita {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 32px !important;
        font-weight: 600 !important;
        line-height: 1.6 !important;
        color: #111 !important;
        text-align: left !important;
        margin: 0 !important;
        padding: 0 !important;
        white-space: pre-wrap !important;
    }

    .container-palco {
        max-width: 850px;
        margin: 0 auto;
        padding-bottom: 100px;
    }
    </style>
''', unsafe_allow_html=True)

# --- 2. GESTÃO DE ESTADOS (IDIOMA E NAVEGAÇÃO) ---
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'take' not in st.session_state: st.session_state.take = 0
if 'book' not in st.session_state: st.session_state.book = 'livro vivo'

# Carregamento da base de temas
path_base = f'./base/rol_{st.session_state.book}.txt'
temas = []
if os.path.exists(path_base):
    with open(path_base, 'r', encoding='utf-8') as f:
        temas = [l.strip() for l in f if l.strip() and not l.startswith('[source')]

# --- 3. SIDEBAR (CONFIGURAÇÕES E VITRINE) ---
with st.sidebar:
    st.image('logo_ypo.png')
    
    # Seleção de Idioma
    st.write("### 🌐 IDIOMA")
    c_l1, c_l2 = st.columns(2)
    if c_l1.button("PT"): st.session_state.lang = 'pt'; st.rerun()
    if c_l2.button("EN"): st.session_state.lang = 'en'; st.rerun()
    st.write(f"Selecionado: **{st.session_state.lang.upper()}**")
    
    st.divider()
    
    if temas:
        st.session_state.take = st.selectbox("LOCALIZAR TEMA:", range(len(temas)), 
                                              index=st.session_state.take, 
                                              format_func=lambda x: temas[x])
    
    st.divider()
    st.write("### ⚙️ VITRINE")
    chk_arte = st.checkbox("ARTE", value=True)
    chk_som = st.checkbox("SOM", value=True)
    chk_video = st.checkbox("VÍDEO", value=False)
    
    st.divider()
    st.markdown('<div style="font-size:12px; opacity:0.6;">SAMIZDÀT EDITORA</div>', unsafe_allow_html=True)

# --- 4. O PALCO (EXIBIÇÃO) ---
if temas:
    # Navegação de Topo
    c1, c2, c3, c4, c5 = st.columns(5)
    if c1.button("+", help="Variação"): st.rerun()
    if c2.button("◀", help="Anterior"):
        st.session_state.take = (st.session_state.take - 1) % len(temas); st.rerun()
    if c3.button("✴", help="Sorteio"):
        st.session_state.take = random.randint(0, len(temas)-1); st.rerun()
    if c4.button("▶", help="Próximo"):
        st.session_state.take = (st.session_state.take + 1) % len(temas); st.rerun()
    if c5.button("?", help="Ajuda"):
        st.info("Comandos: + (Variação) | ◀ (Anterior) | ✴ (Sorte) | ▶ (Próximo)")

    st.divider()

    tema_atual = temas[st.session_state.take]
    
    # Título Fixo (Ponto 2)
    st.markdown(f'<div class="palco-titulo-fixo">{tema_atual}</div>', unsafe_allow_html=True)

    # Geração e Renderização Linha a Linha (Ponto 3 e 4)
    poema_raw = gera_poema(tema_atual, st.session_state.lang)
    
    st.markdown('<div class="container-palco">', unsafe_allow_html=True)
    
    # Placeholder para Imagem (Ponto 5)
    if chk_arte:
        img_path = f"./images/machina/{tema_atual}.jpg"
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)

    # Renderização estrita do texto
    for linha in poema_raw:
        # Limpeza absoluta de tags HTML antes da exibição
        texto_limpo = re.sub(r'<[^>]*>', '', linha).replace("&emsp;", "    ")
        
        if texto_limpo.strip() == "":
            st.markdown('<br>', unsafe_allow_html=True)
        else:
            # Cada linha recebe exatamente a mesma classe CSS
            st.markdown(f'<p class="poema-linha-estrita">{texto_limpo}</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Placeholder para Áudio (Ponto 5)
    if chk_som:
        audio_path = f"./audio/machina/{tema_atual}.mp3"
        if os.path.exists(audio_path):
            st.audio(audio_path)
