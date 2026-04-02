import os
import random
import base64
import streamlit as st
from lay_2_ypo import gera_poema 

# --- 1. CONFIGURAÇÃO ESTÉTICA ---
st.set_page_config(page_title='yPoemas', layout='centered', initial_sidebar_state='expanded')

st.markdown('''
    <style>
    header, footer {visibility: hidden;}
    .main { background-color: #ffffff; }
    [data-testid="stSidebar"] { min-width: 310px !important; }
    .stButton>button { width: 100%; border-radius: 4px; height: 2.2em; font-weight: 600; }
    .palco-container { display: flex; flex-direction: row; align-items: flex-start; gap: 30px; margin-top: 20px; }
    .poema-texto { font-weight: 600; font-size: 19px; font-family: 'IBM Plex Sans', sans-serif; line-height: 1.6; color: #000; flex: 1; }
    .poema-img { max-width: 390px; border-radius: 4px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); }
    </style>
''', unsafe_allow_html=True)

# --- 2. ESTADO DA SESSÃO ---
if 'take' not in st.session_state: st.session_state.take = 0
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'book' not in st.session_state: st.session_state.book = 'livro_vivo'

# Estados de Mídia
if 'draw' not in st.session_state: st.session_state.draw = True
if 'video' not in st.session_state: st.session_state.video = False
if 'audio' not in st.session_state: st.session_state.audio = False

# --- 3. SIDEBAR (LOGOS, LIVROS E CONTROLES) ---
with st.sidebar:
    st.image('logo_ypo.png')
    
    # Seleção de Livro (Páginas)
    livros = {'Livro Vivo': 'livro_vivo', 'Zodiacaos': 'zodiacaos', 'Meteoro': 'meteoro', 'Avevida': 'avevida'}
    escolha_book = st.selectbox("📖 Biblioteca", list(livros.keys()), index=list(livros.values()).index(st.session_state.book))
    
    if st.session_state.book != livros[escolha_book]:
        st.session_state.book = livros[escolha_book]
        st.session_state.take = 0
        st.rerun()

    st.divider()

    
    # Controles de Mídia (Audio/Vídeo/Draw)
    st.write("🎬 **Modos de Saída**")
    st.session_state.draw = st.toggle("Imagem (Draw)", st.session_state.draw)
    st.session_state.video = st.toggle("Vídeo", st.session_state.video)
    st.session_state.audio = st.toggle("Áudio", st.session_state.audio)
    
    st.divider()
    st.info("Machina Poética v3.0 - Ação Direta")

# --- 4. TAB BAR DE IDIOMAS (O TOPO DO PALCO) ---
# Criamos uma linha de botões para os idiomas
idiomas = ["pt", "es", "it", "fr", "en", "la"]
cols_lang = st.columns(len(idiomas))

for idx, lang in enumerate(idiomas):
    # Destaque visual para o idioma selecionado
    label = f"**{lang.upper()}**" if st.session_state.lang == lang else lang
    if cols_lang[idx].button(label):
        st.session_state.lang = lang
        st.rerun()

st.divider()

# --- 5. NAVEGAÇÃO DE TEMAS ---
path = f'./base/rol_{st.session_state.book}.txt'
temas = [l.strip() for l in open(path, 'r', encoding='utf-8') if l.strip()] if os.path.exists(path) else ["Fatos"]
max_idx = len(temas) - 1

c_nav1, c_nav2, c_nav3 = st.columns([1, 1, 1])
if c_nav1.button("◀ Tema"):
    st.session_state.take = max_idx if st.session_state.take <= 0 else st.session_state.take - 1
    st.rerun()
if c_nav2.button("✻ Aleatório"):
    st.session_state.take = random.randint(0, max_idx)
    st.rerun()
if c_nav3.button("Tema ▶"):
    st.session_state.take = 0 if st.session_state.take >= max_idx else st.session_state.take + 1
    st.rerun()

# Seletor direto para busca rápida
st.session_state.take = st.selectbox("🔍 Localizar Tema", range(len(temas)), index=st.session_state.take, format_func=lambda x: temas[x])

# --- 6. EXECUÇÃO E PALCO ---
tema_atual = temas[st.session_state.take]
# Passamos o idioma atual para o motor
poema = gera_poema(tema_atual, "") 
texto_formatado = "<br>".join(poema)

# Lógica de exibição de Imagem
img_path = f"./images/machina/{tema_atual}.jpg"
imagem_html = ""
if st.session_state.draw and os.path.exists(img_path):
    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    imagem_html = f'<img class="poema-img" src="data:image/jpg;base64,{img_b64}">'

# Montagem do Palco Flexível
st.markdown(f'''
    <div class="palco-container">
        {imagem_html}
        <div class="poema-texto">{texto_formatado}</div>
    </div>
''', unsafe_allow_html=True)

# Placeholder para Áudio/Vídeo (Serão integrados conforme a evolução do lay_2)
if st.session_state.audio:
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") # Exemplo
