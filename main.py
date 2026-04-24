# --- PROTOCOLO DE COMPATIBILIDADE PYTHON 3.13+ ---
import sys
try:
    import cgi
except ImportError:
    from types import ModuleType
    mock_cgi = ModuleType("cgi")
    mock_cgi.parse_header = lambda x: (x, {}) 
    sys.modules["cgi"] = mock_cgi

import streamlit as st
import streamlit_antd_components as sac
import extra_streamlit_components as stx
from googletrans import Translator
import edge_tts
import asyncio
import os
import random
import socket

# --- 1. MOTOR DE DADOS INTEGRADO (NÃO DEPENDE DE OUTROS .PY) ---

def load_md_file(file_name):
    """Carrega arquivos Markdown da pasta base."""
    path = os.path.join("./base/", file_name)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except: pass
    return f"ℹ️ Info: {file_name} não encontrado."

def load_temas(book_name):
    """Carrega a lista de temas conforme o livro selecionado."""
    base_path = "./base/"
    file_map = {
        "livro vivo": "temas_vivos.txt",
        "poemas": "temas_poemas.txt",
        "jocosos": "temas_jocosos.txt",
        "ensaios": "temas_ensaios.txt",
        "variações": "temas_variacoes.txt"
    }
    target = file_map.get(book_name, "temas_vivos.txt")
    path = os.path.join(base_path, target)
    
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return ["paz", "tempo", "silêncio"]

def load_poema(tema, semente=""):
    """Carrega o conteúdo do poema solicitado."""
    path = os.path.join("./base/poemas/", f"{tema}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "A variação poética está sendo processada..."

def update_readings(tema):
    """Registra log de leitura na pasta temp."""
    temp_dir = "./temp/"
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)
    try:
        with open(os.path.join(temp_dir, "read_list.txt"), "a", encoding="utf-8") as f:
            f.write(f"{tema}\n")
    except: pass

def load_help(lang):
    """Dicas de interface traduzidas."""
    helps = {
        "pt": ["Anterior", "Aleatório", "Próximo", "Salvar", "Mais"],
        "en": ["Previous", "Random", "Next", "Save", "More"]
    }
    return helps.get(lang, helps["pt"])

# --- 2. FERRAMENTAS MULTIMÍDIA ---

def translate(text):
    """Tradução via GoogleTrans."""
    if st.session_state.lang == "pt" or not text:
        return text
    try:
        translator = Translator()
        return translator.translate(text, dest=st.session_state.lang).text
    except:
        return text

def talk(text):
    """Voz Neural via Edge-TTS."""
    if not text: return
    voices = {"pt": "pt-BR-AntonioNeural", "en": "en-US-GuyNeural"}
    selected_voice = voices.get(st.session_state.lang, "pt-BR-AntonioNeural")

    async def generate_voice():
        clean_text = text.replace("<br>", " ").replace("\n", " ")
        communicate = edge_tts.Communicate(clean_text, selected_voice)
        temp_dir = "./temp/"
        if not os.path.exists(temp_dir): os.makedirs(temp_dir)
        temp_audio = os.path.join(temp_dir, f"voice_{st.session_state.user_ip}.mp3")
        await communicate.save(temp_audio)
        return temp_audio

    try:
        audio_file = asyncio.run(generate_voice())
        with open(audio_file, "rb") as f:
            st.audio(f.read(), format="audio/mp3")
    except: pass

# --- 3. PÁGINAS DA INTERFACE ---

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list) - 1
    if st.session_state.take > maxy: st.session_state.take = 0

    tips = load_help(st.session_state.lang)
    cols = st.columns([3, 1, 1, 1, 1, 1, 3])
    
    if cols[2].button("◀", help=tips[0]): 
        st.session_state.take = maxy if st.session_state.take <= 0 else st.session_state.take - 1
        st.rerun()
    if cols[3].button("✻", help=tips[1]): 
        st.session_state.take = random.randrange(0, maxy + 1)
        st.rerun()
    if cols[4].button("▶", help=tips[2]): 
        st.session_state.take = 0 if st.session_state.take >= maxy else st.session_state.take + 1
        st.rerun()

    opt_take = st.selectbox("↓ Temas", range(len(temas_list)), index=st.session_state.take, format_func=lambda z: temas_list[z])
    if opt_take != st.session_state.take:
        st.session_state.take = opt_take
        st.rerun()

    st.session_state.tema = temas_list[st.session_state.take]

    with st.expander(f"⚫ {st.session_state.lang.upper()} | {st.session_state.book.upper()}", expanded=True):
        txt = load_poema(st.session_state.tema)
        txt_trans = translate(txt)
        st.markdown(f"<div style='font-size:1.2em;'>{txt_trans}</div>", unsafe_allow_html=True)
        update_readings(st.session_state.tema)
    
    if st.session_state.talk: talk(txt_trans)

# --- 4. FUNÇÃO PRINCIPAL (MAIN) ---

def main():
    # Inicialização de Estado
    if "init" not in st.session_state:
        st.session_state.update({
            "init": True, "book": "livro vivo", "lang": "pt", "take": 0,
            "tema": "paz", "draw": False, "talk": False, "user_ip": "127.0.0.1"
        })
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            st.session_state.user_ip = s.getsockname()[0]
            s.close()
        except: pass

    # Barra de Abas
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
    ], default="2")

    pages = {
        "1": ("INFO_MINI.md", "img_mini.jpg", lambda: st.info("Modo Mini")),
        "2": ("INFO_YPOEMAS.md", "img_ypoemas.jpg", page_ypoemas),
        "3": ("INFO_EUREKA.md", "img_eureka.jpg", lambda: st.info("Modo Eureka"))
    }

    info, img, func = pages.get(str(chosen_id), pages["2"])
    
    # Sidebar Dinâmico
    st.sidebar.info(load_md_file(info))
    if os.path.exists(f"./images/{img}"):
        st.sidebar.image(f"./images/{img}")
    
    # Execução da Página Selecionada
    func()

if __name__ == "__main__":
    main()
