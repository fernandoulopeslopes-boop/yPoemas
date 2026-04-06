import streamlit as st
import streamlit_antd_components as sac
import extra_streamlit_components as stx
import random
import time
import os

# =================================================================
# 1. DEFINIÇÕES DE FUNÇÕES (O MOTOR DA MACHINA)
# =================================================================

def load_temas(book):
    # Retorna a lista dos 48 temas originais
    return ["Amor", "Morte", "Tempo", "Mar", "Infinito", "Silêncio"] # [Lista Completa Aqui]

def update_visy():
    if 'views' not in st.session_state:
        st.session_state.views = 0
    st.session_state.views += 1

def translate(text):
    return text # Lógica deep-translator

def load_poema(tema, lang):
    return f"Variação poética sobre {tema}" # Lógica de milhões de combinações

def load_help(lang):
    return ["Dica 1", "Dica 2", "Dica 3", "Dica 4", "Dica 5"]

def load_arts(tema):
    return None

def write_ypoema(texto, imagem):
    st.markdown(f"### {texto}")
    if imagem:
        st.image(imagem)

def say_number(tema):
    return "Milhões de variações"

def load_md_file(file):
    return f"Info: {file}"

def pick_lang():
    st.sidebar.selectbox("Idioma", ["pt", "en", "es"], key="lang")

def draw_check_buttons():
    st.sidebar.checkbox("Desenhar", key="draw")

def show_icons():
    st.sidebar.write("---")
    st.sidebar.write("Máquina de Fazer Poesia © 2026")

# --- Páginas ---

def page_mini():
    temas_list = load_temas("todos os temas")
    with st.container():
        foo1, more, rand, auto, foo2 = st.columns([1, 1, 1, 1, 1])
        help_tips = load_help(st.session_state.lang)
        if rand.button("✻", help=help_tips[1], key="btn_rand_mini"):
            st.session_state.mini = random.randrange(0, len(temas_list))
        
        st.session_state.tema = temas_list[st.session_state.mini]
        curr_ypoema = load_poema(st.session_state.tema, st.session_state.lang)
        write_ypoema(curr_ypoema, load_arts(st.session_state.tema))

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    with st.container():
        st.write(f"Palco: {st.session_state.tema}")

# =================================================================
# 2. ORQUESTRAÇÃO (EXECUÇÃO APÓS TODAS AS DEFINIÇÕES)
# =================================================================

def main():
    # Inicialização de Session State
    if 'visy' not in st.session_state: st.session_state.visy = True
    if 'lang' not in st.session_state: st.session_state.lang = "pt"
    if 'book' not in st.session_state: st.session_state.book = "todos os temas"
    if 'mini' not in st.session_state: st.session_state.mini = 0

    # Lógica de entrada (Só roda se as funções acima existirem)
    if st.session_state.visy:
        update_visy() 
        temas_list_init = load_temas(st.session_state.book)
        st.session_state.take = random.randrange(0, len(temas_list_init))
        st.success(translate("bem vindo à **máquina de fazer Poesia...**"))
        st.session_state.visy = False

    # Interface de Navegação
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
    ], default="2")

    pick_lang()
    draw_check_buttons()

    pages = {
        "1": (page_mini, "INFO_MINI.md", "img_mini.jpg"),
        "2": (page_ypoemas, "INFO_YPOEMAS.md", "img_ypoemas.jpg"),
    }

    if chosen_id in pages:
        func, info, img = pages[chosen_id]
        st.sidebar.info(load_md_file(info))
        with st.container():
            func()

    show_icons()
    
# --- GATILHO ---
if __name__ == "__main__":
    main()
