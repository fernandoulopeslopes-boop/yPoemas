import os
import re
import random
import streamlit as st
from lay_2_ypo import gera_poema 

# --- 1. CONFIGURAÇÃO VISUAL (SAMIZDÀT) ---
st.set_page_config(page_title='yPoemas | Samizdàt', layout='wide', initial_sidebar_state='expanded')

# CSS injetado para garantir a estética da tipografia e botões
st.markdown('''
    <style>
    header, footer {visibility: hidden;}
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }
    
    /* Botões de Comando do Palco */
    .stButton>button { 
        width: 100%; 
        height: 2.8em; 
        font-weight: 700; 
        font-size: 22px;
        border-radius: 4px;
        border: 1px solid #e0e0e0;
        background-color: #fcfcfc;
        color: #333;
        transition: 0.2s;
    }
    .stButton>button:hover { border-color: #000; background-color: #fff; color: #000; }
    
    /* Estilo do Poema (O Coração do Palco) */
    .poema-entregue { 
        font-weight: 600; 
        font-size: 30px; 
        font-family: 'IBM Plex Sans', sans-serif; 
        line-height: 1.6; 
        color: #111;
        white-space: pre-wrap; /* Mantém as quebras de linha do Python */
        padding-top: 20px;
    }
    </style>
''', unsafe_allow_html=True)

# --- 2. ESTADOS DE MEMÓRIA ---
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'book' not in st.session_state: st.session_state.book = 'livro vivo'
if 'take' not in st.session_state: st.session_state.take = 0
for mode in ['draw', 'audio']:
    if mode not in st.session_state: st.session_state[mode] = True

# --- 3. CARREGAMENTO DA BASE ---
path_base = f'./base/rol_{st.session_state.book}.txt'
temas = []
if os.path.exists(path_base):
    with open(path_base, 'r', encoding='utf-8') as f:
        temas = [l.strip() for l in f if l.strip() and not l.startswith('[source')]

# --- 4. SIDEBAR: CONFIGURAÇÕES ---
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
    
    st.markdown('<div style="margin-top: 50px; font-family: serif; font-style: italic; opacity: 0.6;">Edição: Samizdàt</div>', unsafe_allow_html=True)

# --- 5. O PALCO (COMANDOS E PRODUÇÃO) ---
if temas:
    # --- BARRA DE NAVEGAÇÃO SUPERIOR ---
    # Colunas para centralizar os 5 botões de comando
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
        if btn[4].button("?"):
            st.toast("Navegação: + (Variação), < (Anterior), * (Sorte), > (Próximo)")

    st.divider()

    # --- PROCESSAMENTO DO POEMA ---
    tema_atual = temas[st.session_state.take]
    poema_raw = gera_poema(tema_atual, "")
    
    # Limpeza absoluta de tags HTML indesejadas que venham do backend
    texto_sujo = "\n".join(poema_raw)
    texto_limpo = re.sub(r'<[^>]*>', '', texto_sujo) # Remove qualquer <tag>
    texto_limpo = texto_limpo.replace("&emsp;", "    ").strip()

    # --- EXIBIÇÃO NO PALCO ---
    # Uso de colunas nativas para garantir que Imagem e Texto fiquem lado a lado sem erro
    col_visual, col_texto = st.columns([0.45, 0.55])

    with col_visual:
        img_path = f"./images/machina/{tema_atual}.jpg"
        if st.session_state.draw and os.path.exists(img_path):
            st.image(img_path, use_container_width=True)

    with col_texto:
        # Injeção segura do texto limpo na classe CSS
        st.markdown(f'<p class="poema-entregue">{texto_limpo}</p>', unsafe_allow_html=True)

    # --- ÁUDIO ---
    audio_path = f"./audio/machina/{tema_atual}.mp3"
    if st.session_state.audio and os.path.exists(audio_path):
        st.audio(audio_path)

else:
    st.error(f"Erro: Base de dados não encontrada em {path_base}")
