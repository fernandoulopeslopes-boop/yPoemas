# =================================================================
# 🚀 MACHINA DE FAZER POESIA (ABNP) - Versão Estruturada
# =================================================================
"""
yPoemas is an app that randomly collects words and phrases...
[Epitaph] Passei boa parte da minha vida escrevendo a "machina".
"""

import streamlit as st
import os
import re
import random
import time
import socket
import base64
import asyncio
from datetime import datetime
from PIL import Image

# --- MOTORES EXTERNOS ---
from lay_2_ypo import gera_poema

# =================================================================
# 1. LENTE: CONFIGURAÇÃO E FOCO (Obrigatório ser o 1º comando st)
# =================================================================
st.set_page_config(
    page_title="a Machina de fazer Poesia",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Consolidação do Visual (Lente)
st.markdown("""
    <style>
    footer {visibility: hidden;}
    .reportview-container .main .block-container { padding: 0rem; }
    [data-testid='stSidebar'] > div:first-child { width: 310px; }
    .logo-text {
        font-weight: 600; font-size: 18px; font-family: 'IBM Plex Sans', sans-serif;
        color: #000000; padding-left: 15px; text-align: left;
        display: block; line-height: 1.6; white-space: pre-wrap !important;
    }
    .logo-img { float: right; max-width: 300px; margin-left: 15px; }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 2. PAIOL: INICIALIZAÇÃO DO ESTADO (A Memória da Machina)
# =================================================================
if "initialized" not in st.session_state:
    # Identidade e Localização
    st.session_state.lang = 'pt'
    st.session_state.last_lang = 'pt'
    st.session_state.tema = 'Fatos'
    try:
        st.session_state.user_id = socket.gethostbyname(socket.gethostname())
    except:
        st.session_state.user_id = "local_user"
    
    # Interface (Padrão 'Y'/'N' para segurança)
    st.session_state.talk = 'N'
    st.session_state.vydo = 'N'
    st.session_state.draw = 'Y'
    st.session_state.auto = False
    st.session_state.visy = True
    
    # Navegação e Livros
    st.session_state.book = "livro vivo"
    st.session_state.take = 0
    st.session_state.mini = 0
    st.session_state.curr_ypoema = ""
    st.session_state.trad_ypoema = ""
    st.session_state.book_list = []
    st.session_state.arts = []
    
    # Trava de Segurança
    st.session_state.initialized = True

# =================================================================
# 3. PAIOL: CARREGADORES (CACHE)
# =================================================================

@st.cache_resource
def load_eureka_database():
    caminho_lexico = os.path.join("base", "lexico.pt")
    if os.path.exists(caminho_lexico):
        try:
            with open(caminho_lexico, "r", encoding="utf-8") as f:
                return [linha.strip() for linha in f if " : " in linha]
        except: return []
    return []

@st.cache_data
def load_help_system(lang):
    help_list = []
    caminho = os.path.join("base", "helpers.txt")
    if os.path.exists(caminho):
        with open(caminho, encoding="utf-8") as file:
            for line in file:
                help_list.append(line)
    return help_list

@st.cache_data(show_spinner=False)
def load_temas(book):
    book_list = []
    caminho = os.path.join("base", "rol_" + book + ".txt")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as file:
            for line in file:
                tema_limpo = line.replace(" ", "").strip()
                if tema_limpo: book_list.append(tema_limpo)
    return book_list

# =================================================================
# 4. MOTOR: LÓGICA DE GERAÇÃO E TRADUÇÃO
# =================================================================

def load_poema(nome_tema, seed_eureka=""):
    script = gera_poema(nome_tema, seed_eureka)
    # Salva no disco (LYPO) para manter a compatibilidade com sua versão anterior
    lypo_user = 'LYPO_' + st.session_state.user_id
    caminho_temp = os.path.join('temp', lypo_user)
    
    novo_ypoema = ""
    with open(caminho_temp, 'w', encoding='utf-8') as save_lypo:
        save_lypo.write(nome_tema + '\n')
        for line in script:
            save_lypo.write(line + '\n')
            novo_ypoema += (line if line != '\n' else '') + '<br>'
    
    return novo_ypoema

def translate(text):
    if st.session_state.lang == "pt": return text
    try:
        from deep_translator import GoogleTranslator
        translated = GoogleTranslator(source='pt', target=st.session_state.lang).translate(text)
        # Limpeza de tags HTML deformadas
        for tag in ["<br>>", "< br>", "<br >", "<br ", " br>", "<BR>"]:
            translated = translated.replace(tag, "<br>")
        return translated
    except: return text

# =================================================================
# 5. SALAS: INTERFACE E NAVEGAÇÃO
# =================================================================

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    if LOGO_IMAGE and os.path.exists(LOGO_IMAGE):
        with open(LOGO_IMAGE, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode()
        st.markdown(f"""
            <div class='container'>
                <img class='logo-img' src='data:image/jpg;base64,{img_b64}'>
                <p class='logo-text'>{LOGO_TEXTO}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"<p class='logo-text'>{LOGO_TEXTO}</p>", unsafe_allow_html=True)

def page_mini():
    temas_list = load_temas("todos os temas")
    if not temas_list: return
    
    # Navegação superior
    col1, more_col, rand_col, auto_col, col2 = st.columns([4, 1, 1, 1, 4])
    
    if rand_col.button("✻"):
        st.session_state.mini = random.randrange(len(temas_list))
    
    st.session_state.auto = auto_col.checkbox("auto", value=st.session_state.auto)
    st.session_state.tema = temas_list[st.session_state.mini % len(temas_list)]
    
    # Gerar Poema
    curr_ypoema = load_poema(st.session_state.tema)
    if st.session_state.lang != "pt":
        curr_ypoema = translate(curr_ypoema)
    
    # Formatação para Markdown
    LOGO_TEXTO = "  \n".join([l.strip() for l in curr_ypoema.split('<br>')])
    LOGO_IMAGE = load_arts(st.session_state.tema) if st.session_state.draw == 'Y' else None
    
    write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

# --- AUXILIARES ---
def load_arts(nome_tema):
    # Simplificação da sua lógica de busca de imagem
    path = "./images/machina/logo_ypoemas.jpg" # Fallback
    # (Aqui manteríamos sua lógica de sorteio de imagens da pasta images.txt)
    return path

# =================================================================
# 6. METAS: EXECUÇÃO PRINCIPAL
# =================================================================
def main():
    # Sidebar: Idiomas e Ferramentas
    with st.sidebar:
        st.title("yPoemas")
        # Aqui entram as suas funções pick_lang() e draw_check_buttons()
        st.write(f"Idioma: {st.session_state.lang}")
        st.write(f"ID: {st.session_state.user_id}")

    # Roteamento de Salas
    page_mini()

if __name__ == "__main__":
    main()
