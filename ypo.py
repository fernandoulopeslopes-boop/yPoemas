import streamlit as st
import os
import random
import socket
import base64

# 1. CONFIGURAÇÃO DA PÁGINA (WIDE E SIDEBAR)
st.set_page_config(page_title="a Machina de fazer Poesia", layout="wide", initial_sidebar_state="expanded")

# --- MOTORES EXTERNOS ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(tema, seed=""): return ["Erro: motor lay_2_ypo não encontrado."]

def translate(texto): # Placeholder para não dar erro
    return texto 

# 2. A LENTE (EXIBIÇÃO) - ÚNICA E DEFINITIVA
def write_ypoema    
# 3. PAIOL E UTILITÁRIOS
if "initialized" not in st.session_state:
    st.session_state.lang, st.session_state.tema, st.session_state.take = 'pt', 'Fatos', 0
    st.session_state.book, st.session_state.initialized = "livro vivo", True

@st.cache_data(show_spinner=False)
def load_temas(book):
    caminho = os.path.join("base", f"rol_{book}.txt")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return ["Fatos"]

def load_poema(nome_tema):
    script = gera_poema(nome_tema, "")
    if isinstance(script, list): return "\n".join([str(l) for l in script if l])
    return str(script)

def load_arts(nome_tema): # Placeholder para o Help/Matrix
    return None

# 4. A SALA (YPOEMAS)
def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    
    # SEQUÊNCIA DE BOTÕES: ✚, ◀, ✻, ▶, ?
    c1, more, last, rand, nest, manu, c2 = st.columns([2, 0.5, 0.5, 0.5, 0.5, 0.5, 2])
    
    if more.button("✚", key="btn_more_ypo"): st.rerun()
    if last.button("◀", key="btn_last_ypo"):
        st.session_state.take = (st.session_state.take - 1) % len(temas_list)
        st.rerun()
    if rand.button("✻", key="btn_rand_ypo"):
        st.session_state.take = random.randrange(len(temas_list))
        st.rerun()
    if nest.button("▶", key="btn_nest_ypo"):
        st.session_state.take = (st.session_state.take + 1) % len(temas_list)
        st.rerun()
    with manu:
        with st.popover("?", help="Help !!!"):
            st.write(f"**Matriz: {st.session_state.tema}**")
            st.info("A contemporaneidade remete a Aldus Manutius.")

    st.session_state.tema = temas_list[st.session_state.take % len(temas_list)]
    poema_raw = load_poema(st.session_state.tema)
    write_ypoema(st.session_state.tema.upper(), poema_raw)

# 5. O MOTOR (MAIN)
def main():
    with st.sidebar:
        st.title("yPoemas")
        sala = st.radio("Navegar:", ["Exploração", "Sobre"])
    if sala == "Exploração": page_ypoemas()
    else: st.write("### Sobre a Machina")

if __name__ == "__main__":
    main()
