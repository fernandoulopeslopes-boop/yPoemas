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
    
    /* BOTÕES DE NAVEGAÇÃO: Símbolos Visíveis e Bordas Marcadas */
    .stButton>button { 
        width: 100%; 
        height: 3.2em; 
        font-weight: 900 !important; 
        font-size: 26px !important;
        font-family: 'Courier New', Courier, monospace;
        border-radius: 4px; 
        border: 2px solid #222 !important; 
        background-color: #ffffff !important;
        color: #000000 !important;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #f0f0f0 !important; border-color: #555 !important; }
    
    /* PALCO SAGRADO: Centralização e Fluidez */
    .palco-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        padding: 10px 0 60px 0;
        text-align: center;
    }

    .palco-conteudo {
        max-width: 850px;
        width: 90%;
    }

    .ypo-titulo {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 18px;
        font-weight: 400;
        font-style: italic;
        color: #888;
        margin-bottom: 40px;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    
    .poema-texto-final { 
        font-weight: 600; 
        font-size: 32px; 
        font-family: 'IBM Plex Sans', sans-serif; 
        line-height: 1.7; 
        color: #111;
        white-space: pre-wrap;
        margin-top: 30px;
        text-align: left; /* Alinhamento clássico do verso */
        display: inline-block; 
    }
    
    .poema-img-palco { 
        max-width: 100%; 
        height: auto;
        border-radius: 2px; 
        box-shadow: 0px 15px 50px rgba(0,0,0,0.1);
        margin: 0 auto 20px auto;
        display: block;
    }

    /* Player de áudio centralizado e discreto */
    .stAudio {
        max-width: 500px;
        margin: 40px auto;
    }
    </style>
''', unsafe_allow_html=True)

# --- 2. ESTADOS E CARREGAMENTO ---
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

# --- 3. SIDEBAR (CONFIGURAÇÕES GLOBAIS) ---
with st.sidebar:
    st.image('logo_ypo.png')
    st.write(f"### 📖 {st.session_state.book.upper()}")
    if temas:
        st.session_state.take = st.selectbox("Localizar Tema:", range(len(temas)), 
                                              index=st.session_state.take, 
                                              format_func=lambda x: temas[x])
    st.divider()
    st.session_state.draw = st.checkbox("Exibir Imagem", st.session_state.draw)
    st.session_state.audio = st.checkbox("Habilitar Áudio", st.session_state.audio)
    st.markdown('<div style="margin-top: 60px; font-style: italic; opacity: 0.5;">Edição: Samizdàt</div>', unsafe_allow_html=True)

# --- 4. O PALCO (AÇÃO E EXIBIÇÃO) ---
if temas:
    # COMANDOS SUPERIORES (Navegação com Identificação de Dicas)
    _, c_nav, _ = st.columns([0.1, 0.8, 0.1])
    with c_nav:
        btn = st.columns(5)
        if btn[0].button("+", help="Gerar outra variação deste tema"): st.rerun()
        if btn[1].button("<", help="Voltar para o tema anterior"):
            st.session_state.take = (st.session_state.take - 1) % len(temas); st.rerun()
        if btn[2].button("*", help="Sortear um tema aleatório"):
            st.session_state.take = random.randint(0, len(temas)-1); st.rerun()
        if btn[3].button(">", help="Avançar para o próximo tema"):
            st.session_state.take = (st.session_state.take + 1) % len(temas); st.rerun()
        if btn[4].button("?", help="Ajuda: Navegue ou gere variações do yPoema"):
            st.info("Utilize os botões acima para interagir com a máquina de poesia.")

    st.divider()

    # PRODUÇÃO E LIMPEZA DE TEXTO
    tema_atual = temas[st.session_state.take]
    poema_raw = gera_poema(tema_atual, "")
    
    # Limpeza profunda: Remove qualquer tag HTML <...> e converte recuos
    corpo_final = []
    for linha in poema_raw:
        limpa = re.sub(r'<[^>]*>', '', linha)
        limpa = limpa.replace("&emsp;", "    ")
        if limpa.strip():
            corpo_final.append(limpa)
    
    texto_para_exibir = "\n".join(corpo_final).strip()

    # IMAGEM (CENTRALIZADA NO PALCO)
    img_html = ""
    img_path = f"./images/machina/{tema_atual}.jpg"
    if st.session_state.draw and os.path.exists(img_path):
        with open(img_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        img_html = f'<img class="poema-img-palco" src="data:image/jpg;base64,{img_b64}">'

    # RENDERIZAÇÃO FINAL: Título + Imagem + Poema
    st.markdown(f'''
        <div class="palco-wrapper">
            <div class="palco-conteudo">
                <div class="ypo-titulo">—— {tema_atual.upper()} ——</div>
                {img_html}
                <div style="text-align: center;">
                    <div class="poema-texto-final">{texto_para_exibir}</div>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # ÁUDIO
    audio_path = f"./audio/machina/{tema_atual}.mp3"
    if st.session_state.audio and os.path.exists(audio_path):
        st.audio(audio_path)
