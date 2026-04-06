import streamlit as st
import extra_streamlit_components as stx
import random
import time
import os

# --- 1. FUNÇÕES DE SUPORTE E UTILIDADE ---
def normalize_text(text):
    if not text: return ""
    return text.replace('\r\n', '\n').strip()

def get_processed_content(tema, seed=""):
    # (Lógica interna omitida para brevidade, mantenha a versão anterior)
    curr_ypoema = load_poema(tema, seed)
    curr_ypoema = load_lypo()
    if st.session_state.lang != "pt":
        curr_ypoema = translate(curr_ypoema)
    update_readings(tema)
    return normalize_text(curr_ypoema)

def render_display(texto, tema):
    image = load_arts(tema) if st.session_state.draw else None
    write_ypoema(texto, image)
    if st.session_state.talk:
        talk(texto)

# --- 2. DEFINIÇÃO DAS PÁGINAS (Devem vir antes do Main) ---

def page_mini():
    # ... código da page_mini ...
    pass

def page_ypoemas():
    # ... código da page_ypoemas ...
    pass

def page_eureka():
    # ... código da page_eureka ...
    pass

# ... defina page_off_machina, page_books, page_polys, page_abouts aqui ...

# --- 3. FUNÇÃO PRINCIPAL (MAIN) ---
def main():
    # Configuração de página deve ser a PRIMEIRA coisa do Streamlit
    if 'setup_done' not in st.session_state:
        st.set_page_config(layout="wide", page_title="Máquina de Poesia")
        st.session_state.setup_done = True

    # Agora sim, chamadas de funções que já foram lidas acima
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="poly", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    # Funções globais de UI (certifique-se de que estão definidas no seu arquivo de funções importadas)
    pick_lang()
    draw_check_buttons()

    pages_config = {
        "1": ("INFO_MINI.md", "img_mini.jpg", page_mini),
        "2": ("INFO_YPOEMAS.md", "img_ypoemas.jpg", page_ypoemas),
        "3": ("INFO_EUREKA.md", "img_eureka.jpg", page_eureka),
        "4": ("INFO_OFF-MACHINA.md", "img_off-machina.jpg", page_off_machina),
        "5": ("INFO_BOOKS.md", "img_books.jpg", page_books),
        "6": ("INFO_POLY.md", "img_poly.jpg", page_polys),
        "7": ("INFO_ABOUT.md", "img_about.jpg", page_abouts),
    }

    if chosen_id in pages_config:
        info_md, img, func = pages_config[chosen_id]
        st.sidebar.info(load_md_file(info_md))
        st.sidebar.image(img)
        func() # Executa a página selecionada

    show_icons()

# --- 4. EXECUÇÃO FINAL (O GATILHO) ---
if __name__ == "__main__":
    main()
