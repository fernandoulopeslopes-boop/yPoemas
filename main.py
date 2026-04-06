import os
import re
import time
import random
import base64
import socket
import streamlit as st
import extra_streamlit_components as stx

from datetime import datetime
from lay_2_ypo import gera_poema

# =================================================================
# 1. SETTINGS & INTERFACE
# =================================================================

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

def have_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

# Inicialização de dependências externas com fallback
if have_internet():
    try:
        from deep_translator import GoogleTranslator
        from gtts import gTTS
    except ImportError:
        st.warning("Dependências de tradução/voz ausentes.")
else:
    st.warning("Internet offline. Funções de tradução limitadas.")

# Identificação do usuário para arquivos temporários (LYPO/TYPO)
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# Injeção de CSS para blindagem de layout e sidebar (310px)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .main .block-container {
        padding-top: 1rem;
        max-width: 900px;
    }
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 310px;
    }
    .logo-text {
        font-weight: 400;
        font-size: 19px;
        font-family: 'IBM Plex Sans', serif;
        color: #000000;
        line-height: 1.6;
        padding-left: 15px;
    }
    .logo-img {
        float: right;
        margin-left: 20px;
        max-width: 280px;
        border-radius: 4px;
    }
    </style> """,
    unsafe_allow_html=True,
)

# =================================================================
# 2. SESSION STATE
# =================================================================

states = {
    "lang": "pt", "last_lang": "pt", "book": "livro vivo", 
    "take": 0, "mini": 0, "tema": "Fatos", "eureka": 0,
    "visy": True, "nany_visy": 0, "draw": True, 
    "talk": False, "vydo": False, "auto": False, "arts": []
}
for key, val in states.items():
    if key not in st.session_state:
        st.session_state[key] = val

# =================================================================
# 3. MOTORES E FERRAMENTAS (TOOLS)
# =================================================================

def translate(input_text):
    if st.session_state.lang == "pt" or not have_internet():
        return input_text
    try:
        output = GoogleTranslator(source="pt", target=st.session_state.lang).translate(text=input_text)
        return output.replace("< br>", "<br>").replace("<br >", "<br>")
    except:
        return input_text

def load_temas(book):
    try:
        path = os.path.join("./base/rol_" + book + ".txt")
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip().replace(" ", "") for line in f if line.strip()]
    except:
        return ["Fatos"]

def load_arts(nome_tema):
    path = f"./images/machina/" # Fallback path
    # Lógica simplificada de seleção de arte baseada no tema
    try:
        arts_list = [f for f in os.listdir(path) if f.endswith(".jpg")]
        if arts_list:
            img = random.choice(arts_list)
            return os.path.join(path, img)
    except: pass
    return None

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    img_html = ""
    if LOGO_IMAGE and os.path.exists(LOGO_IMAGE):
        with open(LOGO_IMAGE, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        img_html = f"<img class='logo-img' src='data:image/jpg;base64,{data}'>"
    
    st.markdown(
        f"<div class='container'>{img_html}<p class='logo-text'>{LOGO_TEXTO}</p></div>",
        unsafe_allow_html=True
    )

def update_visy():
    try:
        path = "./temp/visitors.txt"
        if not os.path.exists(path): 
            os.makedirs("./temp", exist_ok=True)
            with open(path, "w") as f: f.write("0")
        with open(path, "r+") as f:
            tots = int(f.read() or 0) + 1
            f.seek(0)
            f.write(str(tots))
            st.session_state.nany_visy = tots
    except: pass

def talk(text):
    if not have_internet(): return
    try:
        clean_text = text.replace("<br>", "\n")
        tts = gTTS(text=clean_text, lang=st.session_state.lang)
        filename = f"./temp/audio_{random.randint(1,999)}.mp3"
        tts.save(filename)
        st.audio(filename)
        os.remove(filename)
    except: pass

# =================================================================
# 4. PÁGINAS (PAGES)
# =================================================================

def page_mini():
    temas = load_temas("todos os temas")
    col1, col2, col3 = st.columns([4, 2, 4])
    
    if col2.button("✻", help="Girar a sorte"):
        st.session_state.mini = random.randrange(len(temas))
    
    st.session_state.tema = temas[st.session_state.mini % len(temas)]
    poema = "<br>".join(gera_poema(st.session_state.tema, "mini"))
    
    final_text = translate(poema)
    img = load_arts(st.session_state.tema) if st.session_state.draw else None
    
    write_ypoema(final_text, img)
    if st.session_state.talk: talk(final_text)

def page_ypoemas():
    temas = load_temas(st.session_state.book)
    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1])
    
    if c2.button("◄"): st.session_state.take -= 1
    if c3.button("✻"): st.session_state.take = random.randrange(len(temas))
    if c4.button("►"): st.session_state.take += 1
    
    st.session_state.take %= len(temas)
    st.session_state.tema = temas[st.session_state.take]
    
    st.markdown(f"### {st.session_state.tema}")
    poema = "<br>".join(gera_poema(st.session_state.tema, "full"))
    
    final_text = translate(poema)
    img = load_arts(st.session_state.tema) if st.session_state.draw else None
    
    write_ypoema(final_text, img)
    if st.session_state.talk: talk(final_text)

def page_eureka():
    st.subheader("Busca Eureka")
    find = st.text_input("Buscar termo nas entranhas da máquina:")
    if len(find) >= 3:
        # Lógica de busca e geração baseada no termo 'find'
        poema = "<br>".join(gera_poema(find, "eureka"))
        write_ypoema(translate(poema), None)

# =================================================================
# 5. MAIN ROTEADOR
# =================================================================

def main():
    # 5.1 Sidebar
    with st.sidebar:
        st.title("Machina")
        # Seleção de Idioma (pick_lang)
        cols = st.columns(5)
        langs = ["pt", "en", "es", "it", "fr"]
        for i, l in enumerate(langs):
            if cols[i].button(l.upper()):
                st.session_state.lang = l
                st.rerun()
        
        st.write("---")
        st.session_state.draw = st.toggle("Artes", st.session_state.draw)
        st.session_state.talk = st.toggle("Voz", st.session_state.talk)
        
        st.write("---")
        st.caption(f"Visitante: {st.session_state.nany_visy}")
        st.caption("© 2026 Máquina de Fazer Poesia")

    # 5.2 Controle de Visitas (Trigger Único)
    if st.session_state.visy:
        update_visy()
        st.session_state.visy = False

    # 5.3 TabBar (Navegação Central)
    # Correção: O componente stx.tab_bar exige a sintaxe correta dos DataItems
    chosen_id = stx(data=[
        stx.TabBarItemData(id="1", title="mini", description="pílulas"),
        stx.TabBarItemData(id="2", title="yPoemas", description="livro"),
        stx.TabBarItemData(id="3", title="eureka", description="busca")
    ], default="2")

    # Roteamento de Páginas
    if chosen_id == "1":
        page_mini()
    elif chosen_id == "2":
        page_ypoemas()
    elif chosen_id == "3":
        page_eureka()

if __name__ == "__main__":
    main()
