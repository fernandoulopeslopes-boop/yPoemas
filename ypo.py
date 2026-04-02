import os
import re
import random
import base64
import streamlit as st
from lay_2_ypo import gera_poema 

# --- 1. CONFIGURAÇÃO E CSS REFORÇADO ---
st.set_page_config(page_title='yPoemas | Samizdàt', layout='wide', initial_sidebar_state='expanded')

st.markdown('''
    <style>
    header, footer {visibility: hidden;}
    
    /* BOTÕES: Ícones Pretos, Fundo Branco, Bordas Fortes */
    .stButton>button { 
        width: 100% !important; 
        height: 3.2em !important; 
        font-size: 28px !important; 
        color: #000 !important;
        background-color: #fff !important;
        border: 3px solid #000 !important;
        border-radius: 6px !important;
        font-weight: bold !important;
    }

    /* TÍTULO ISOLADO NO TOPO */
    .palco-titulo {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 20px;
        color: #999;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 6px;
        margin-bottom: 40px;
        margin-top: 20px;
    }

    /* O POEMA: SEM TAGS E COM QUEBRAS DE LINHA */
    .poema-container-final {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 32px;
        line-height: 1.7;
        font-weight: 600;
        color: #111;
        white-space: pre-wrap; /* Essencial para as quebras de linha (\n) */
        text-align: left;
        max-width: 850px;
        margin: 40px auto;
        padding: 0 20px;
    }

    /* IMAGEM CENTRALIZADA */
    .img-palco {
        display: block;
        margin: 0 auto 30px auto;
        max-width: 600px;
        height: auto;
        box-shadow: 0px 15px 45px rgba(0,0,0,0.1);
    }
    </style>
''', unsafe_allow_html=True)

# --- 2. LÓGICA DE NAVEGAÇÃO ---
if 'take' not in st.session_state: st.session_state.take = 0
if 'book' not in st.session_state: st.session_state.book = 'livro vivo'

path_base = f'./base/rol_{st.session_state.book}.txt'
temas = []
if os.path.exists(path_base):
    with open(path_base, 'r', encoding='utf-8') as f:
        temas = [l.strip() for l in f if l.strip() and not l.startswith('[source')]

# --- 3. SIDEBAR (CONTROLES) ---
with st.sidebar:
    st.image('logo_ypo.png')
    if temas:
        st.session_state.take = st.selectbox("Tema:", range(len(temas)), 
                                              index=st.session_state.take, 
                                              format_func=lambda x: temas[x])
    st.divider()
    draw_on = st.checkbox("Exibir Imagem", value=True)
    audio_on = st.checkbox("Habilitar Áudio", value=True)

# --- 4. O PALCO (GRANDE ÁREA LIVRE) ---
if temas:
    # NAVEGAÇÃO REFINADA COM SEUS ÍCONES
    c1, c2, c3, c4, c5 = st.columns(5)
    
    if c1.button("+", help="Nova variação (+)") : st.rerun()
    if c2.button("◀", help="Anterior (◀)") :
        st.session_state.take = (st.session_state.take - 1) % len(temas); st.rerun()
    if c3.button("✴", help="Sorteio (✴)") :
        st.session_state.take = random.randint(0, len(temas)-1); st.rerun()
    if c4.button("▶", help="Próximo (▶)") :
        st.session_state.take = (st.session_state.take + 1) % len(temas); st.rerun()
    if c5.button("?", help="Ajuda: Clique nos ícones para navegar ou variar o poema.") :
        st.info("Comandos: + Variação | ◀ Anterior | ✴ Sorte | ▶ Próximo")

    st.divider()

    # TÍTULO (Aparece isolado e limpo)
    tema_atual = temas[st.session_state.take]
    st.markdown(f'<div class="palco-titulo">—— {tema_atual} ——</div>', unsafe_allow_html=True)

    # GERAÇÃO E LIMPEZA PROFUNDA (MATA O HTML E RECURSOS)
    poema_raw = gera_poema(tema_atual, "")
    
    # Processa cada linha para remover tags residuais e converter recuo HTML em espaços
    corpo_limpo = []
    for linha in poema_raw:
        # Regex remove qualquer <tag> que tente aparecer como texto
        texto = re.sub(r'<[^>]*>', '', linha)
        texto = texto.replace("&emsp;", "    ")
        corpo_limpo.append(texto)

    # Une com \n (Quebra de linha real)
    texto_final = "\n".join(corpo_limpo).strip()

    # EXIBIÇÃO DA IMAGEM (Se selecionado)
    if draw_on:
        img_path = f"./images/machina/{tema_atual}.jpg"
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<img src="data:image/jpg;base64,{img_b64}" class="img-palco">', unsafe_allow_html=True)

    # EXIBIÇÃO DO TEXTO (Centralizado na tela, mas alinhado à esquerda internamente)
    st.markdown(f'<div class="poema-container-final">{texto_final}</div>', unsafe_allow_html=True)

    # ÁUDIO
    if audio_on:
        audio_path = f"./audio/machina/{tema_atual}.mp3"
        if os.path.exists(audio_path):
            st.audio(audio_path)
