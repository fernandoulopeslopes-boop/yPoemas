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
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }
    
    .stButton>button { 
        width: 100%; 
        height: 2.8em; 
        font-weight: 700; 
        font-size: 20px;
        border-radius: 4px;
        border: 1px solid #e0e0e0;
        background-color: #f9f9f9;
        color: #333;
    }
    .stButton>button:hover { border-color: #000; background-color: #fff; color: #000; }
    
    /* Palco Sagrado */
    .poema-container { 
        display: flex; 
        flex-direction: row; 
        align-items: flex-start; 
        gap: 60px; 
        padding: 40px 5% 20px 5%;
    }
    
    .poema-texto-render { 
        font-weight: 600; 
        font-size: 28px; 
        font-family: 'IBM Plex Sans', sans-serif; 
        line-height: 1.8; 
        color: #000; 
        flex: 1;
        white-space: pre-wrap; /* Essencial para respeitar os Enters do Python */
    }
    
    .poema-img { 
        max-width: 500px; 
        border-radius: 2px; 
        box-shadow: 0px 10px 30px rgba(0,0,0,0.05); 
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

# --- 3. CARREGAMENTO DA BASE ---
path_base = f'./base/rol_{st.session_state.book}.txt'
temas = []
if os.path.exists(path_base):
    with open(path_base, 'r', encoding='utf-8') as f:
        temas = [l.strip() for l in f if l.strip() and not l.startswith('[source')]

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image('logo_ypo.png')
    st.write("### 🌍 Idioma")
    langs_fixos = ["pt", "es", "it", "fr", "en"]
    cols_lang = st.columns(6)
    for i, l in enumerate(langs_fixos):
        if cols_lang[i].button(l, key=f"side_{l}"): 
            st.session_state.lang = l
            st.rerun()
    
    label_sexto = f"{st.session_state.poly_name} ({st.session_state.poly_lang})"
    if cols_lang[5].button(label_sexto, key="side_poly"):
        st.session_state.lang = st.session_state.poly_lang
        st.rerun()

    st.divider()
    st.write(f"### 📖 {st.session_state.book.upper()}")
    if temas:
        st.session_state.take = st.selectbox("↓ Localizar Tema", range(len(temas)), 
                                              index=st.session_state.take, 
                                              format_func=lambda x: temas[x])

    st.divider()
    st.write("### 🎬 Modos")
    st.session_state.draw = st.checkbox("Imagem (Draw)", st.session_state.draw)
    st.session_state.audio = st.checkbox("Áudio", st.session_state.audio)
    st.session_state.video = st.checkbox("Vídeo", st.session_state.video)
    st.markdown('<div style="margin-top: 40px; font-family: serif; font-style: italic; opacity: 0.6;">Edição: Samizdàt</div>', unsafe_allow_html=True)

# --- 5. O PALCO ---
if temas:
    # Navegação Superior
    _, nav_container, _ = st.columns([0.2, 0.6, 0.2])
    with nav_container:
        btn_cols = st.columns(5)
        if btn_cols[0].button("+", key="cmd_plus"): st.rerun()
        if btn_cols[1].button("<", key="cmd_prev"):
            st.session_state.take = (st.session_state.take - 1) % len(temas)
            st.rerun()
        if btn_cols[2].button("*", key="cmd_rnd"):
            st.session_state.take = random.randint(0, len(temas)-1)
            st.rerun()
        if btn_cols[3].button(">", key="cmd_next"):
            st.session_state.take = (st.session_state.take + 1) % len(temas)
            st.rerun()
        if btn_cols[4].button("?", key="cmd_help"):
            st.toast("Navegação: + (Variação), < (Anterior), * (Sorte), > (Próximo)")

    # GERAÇÃO E FILTRAGEM RIGOROSA
    tema_atual = temas[st.session_state.take]
    poema_raw = gera_poema(tema_atual, "") 
    
    # Lista de termos a serem varridos para garantir o palco limpo
    sujeira = ["<div", "</div>", "class=", "poema-texto", "<br>", ">", "content="]
    
    linhas_limpas = []
    for linha in poema_raw:
        l = linha
        for termo in sujeira:
            l = l.replace(termo, "")
        l = l.replace("&emsp;", "    ") # Converte recuo HTML em espaços
        if l.strip() or l == "": # Mantém linhas em branco, mas remove o "lixo"
            linhas_limpas.append(l)

    poema_final = "\n".join(linhas_limpas).strip()
    
    # Imagem
    img_html = ""
    img_path = f"./images/machina/{tema_atual}.jpg"
    if st.session_state.draw and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            img_encoded = base64.b64encode(f.read()).decode()
        img_html = f'<img class="poema-img" src="data:image/jpg;base64,{img_encoded}">'

    # Renderização Final
    st.markdown(f'''
        <div class="poema-container">
            {img_html}
            <div class="poema-texto-render">{poema_final}</div>
        </div>
    ''', unsafe_allow_html=True)

    audio_path = f"./audio/machina/{tema_atual}.mp3"
    if st.session_state.audio and os.path.exists(audio_path):
        st.audio(audio_path)
