import os
import re
import time
import random
import base64
import socket
import streamlit as st

from extra_streamlit_components import TabBar as stx
from datetime import datetime
from lay_2_ypo import gera_poema

# =================================================================
# 1. SETTINGS & INTERFACE (CORREÇÃO DE SOBREPOSIÇÃO)
# =================================================================

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# CSS REVISADO: Resolve a invasão da sidebar no palco
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    
    /* Ajuste de Margens para evitar sobreposição */
    [data-testid="stSidebarNav"] {padding-top: 2rem;}
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95%;
    }
    
    /* Estilização dos Containers de Poesia */
    .logo-text {
        font-weight: 400;
        font-size: 20px;
        font-family: 'serif';
        color: #1a1a1a;
        line-height: 1.6;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 10px;
    }
    .logo-img {
        float: right;
        margin-left: 20px;
        border-radius: 5px;
        max-width: 250px;
    }
    </style> """,
    unsafe_allow_html=True,
)

# =================================================================
# 2. FERRAMENTAS & MOTOR (RECHEIO REAL)
# =================================================================

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False

# Inicialização de dependências de Tradução/Voz
if have_internet():
    try:
        from deep_translator import GoogleTranslator
        from gtts import gTTS
    except ImportError:
        st.sidebar.warning("Módulos de Tradução/Voz ausentes.")

# IP para identificação de arquivos temporários (LYPO/TYPO)
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

def translate(input_text):
    if st.session_state.lang == "pt": return input_text
    if not have_internet(): return input_text
    try:
        output_text = GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
        return output_text.replace("<br>>", "<br>")
    except:
        return input_text

# =================================================================
# 3. INICIALIZAÇÃO DE ESTADO (PROTOCOLO OBRIGATÓRIO)
# =================================================================

def init_session():
    defaults = {
        "lang": "pt", "last_lang": "pt", "book": "livro vivo",
        "take": 0, "mini": 0, "tema": "Fatos", "visy": True,
        "draw": True, "talk": False, "vydo": False, "auto": False,
        "nany_visy": 0, "arts": []
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

# =================================================================
# 4. FUNÇÕES DE CARREGAMENTO (LOADERS)
# =================================================================

def load_temas(book):
    file_path = os.path.join("./base/rol_" + book + ".txt")
    if not os.path.exists(file_path): return ["Fatos"]
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip().replace(" ", "") for line in f if line.strip()]

def load_poema_real(nome_tema):
    # Chama o seu script lay_2_ypo.py
    script = gera_poema(nome_tema, "")
    lypo_user = f"LYPO_{IPAddres}"
    novo_ypoema = "<br>".join(script)
    
    # Salva para tradução futura
    with open(os.path.join("./temp/", lypo_user), "w", encoding="utf-8") as f:
        f.write(f"{nome_tema}\n{novo_ypoema}")
    return novo_ypoema

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    img_html = ""
    if LOGO_IMAGE:
        try:
            with open(LOGO_IMAGE, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            img_html = f'<img class="logo-img" src="data:image/jpg;base64,{data}">'
        except: pass
    
    st.markdown(
        f'<div class="container">{img_html}<p class="logo-text">{LOGO_TEXTO}</p></div>',
        unsafe_allow_html=True
    )

# =================================================================
# 5. ORQUESTRAÇÃO DAS PÁGINAS
# =================================================================

def main():
    init_session()
    
    # Lógica de primeira visita
    if st.session_state.visy:
        # update_visy() # Ativar quando o arquivo existir
        st.session_state.visy = False

    # Barra de Navegação
    chosen_id = stx(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
    ], default="2")

    # Controles Laterais
    st.sidebar.title("Machina")
    # pick_lang() # Insira sua função de botões aqui
    # draw_check_buttons() # Insira sua função de checkboxes aqui

    if chosen_id == "1":
        st.subheader("Pílula Poética")
        temas = load_temas("todos os temas")
        if st.button("✻ Aleatório"):
            st.session_state.mini = random.randrange(0, len(temas))
            st.session_state.tema = temas[st.session_state.mini]
        
        poema = load_poema_real(st.session_state.tema)
        write_ypoema(poema, None)

    elif chosen_id == "2":
        temas = load_temas(st.session_state.book)
        st.session_state.tema = temas[st.session_state.take]
        
        st.write(f"### {st.session_state.tema}")
        poema = load_poema_real(st.session_state.tema)
        
        # Renderiza com imagem se habilitado
        img = None
        # if st.session_state.draw: img = load_arts(st.session_state.tema)
        
        write_ypoema(poema, img)

    st.sidebar.write("---")
    st.sidebar.write("Máquina de Fazer Poesia © 2026")

if __name__ == "__main__":
    main()
