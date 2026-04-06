import streamlit as st
import extra_streamlit_components as stx
import random
import time
import os

# 1. UTILITÁRIOS E INFRAESTRUTURA
def normalize_text(text):
    if not text: return ""
    return text.replace('\r\n', '\n').strip()

def get_processed_content(tema, seed=""):
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

# 2. DEFINIÇÃO DAS PÁGINAS (ORDEM DE PRECEDÊNCIA)
def page_mini():
    temas_list = load_temas("todos os temas")
    maxy = len(temas_list)
    with st.sidebar:
        wait_time = st.slider(translate("tempo de exibição:"), 5, 60, 10)
    
    col_rand, col_auto = st.columns([1, 1])
    if col_rand.button("✻"):
        st.session_state.mini = random.randrange(0, maxy)
    
    st.session_state.auto = col_auto.checkbox("auto", value=st.session_state.get('auto', False))
    
    placeholder = st.empty()
    if st.session_state.auto:
        st.session_state.mini = random.randrange(0, maxy)
        tema = temas_list[st.session_state.mini]
        texto = get_processed_content(tema)
        with placeholder.container():
            render_display(texto, tema)
        time.sleep(wait_time)
        st.rerun()
    else:
        st.session_state.mini %= maxy
        tema = temas_list[st.session_state.mini]
        texto = get_processed_content(tema)
        with placeholder.container():
            render_display(texto, tema)

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list) - 1
    st.session_state.take %= (maxy + 1)
    
    col_nav = st.columns([1, 1, 1, 1])
    if col_nav[0].button("◀"): st.session_state.take -= 1
    if col_nav[1].button("✻"): st.session_state.take = random.randrange(0, maxy)
    if col_nav[2].button("▶"): st.session_state.take += 1
    
    tema = temas_list[st.session_state.take]
    texto = get_processed_content(tema)
    render_display(texto, tema)

def page_eureka():
    find_what = st.text_input(label=translate("buscar..."))
    if len(find_what) >= 3:
        eureka_list = load_eureka(find_what)
        if eureka_list:
            seed_data = []
            for line in eureka_list:
                p, _, f = line.partition(" : ")
                seed_data.append({"display": f"{p} ➪ {f}", "tema": f[0:-5], "seed": f"{p} ➪ {f}"})
            
            idx = st.selectbox("Ocorrências", range(len(seed_data)), format_func=lambda x: seed_data[x]["display"])
            item = seed_data[idx]
            texto = get_processed_content(item["tema"], item["seed"])
            render_display(texto, item["tema"])

def page_off_machina():
    off_books_list = load_all_offs()
    idx_book = st.selectbox(translate("Livros"), range(len(off_books_list)), format_func=lambda x: off_books_list[x])
    # Lógica simplificada de navegação interna
    page_func = lambda: None # Placeholder
    page_func()

def page_books():
    books_list = ["livro vivo", "poemas", "jocosos", "ensaios", "variações", "metalinguagem", "sociais", "todos os temas"]
    opt = st.selectbox(translate("lista de Livros"), range(len(books_list)), format_func=lambda x: books_list[x])
    if st.button("✔"):
        st.session_state.book = books_list[opt]
        st.session_state.take = 0

def page_polys():
    # Lógica de troca de idiomas
    pass

def page_abouts():
    # Lógica de sobre
    pass

# 3. CORE EXECUTION (MAIN DEFINIDO POR ÚLTIMO)
def main():
    try:
        st.set_page_config(layout="wide", page_title="Máquina de Poesia")
    except:
        pass

    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="poly", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    # Chamadas globais (Devem estar no namespace)
    pick_lang()
    draw_check_buttons()

    pages = {
        "1": ("INFO_MINI.md", "img_mini.jpg", page_mini),
        "2": ("INFO_YPOEMAS.md", "img_ypoemas.jpg", page_ypoemas),
        "3": ("INFO_EUREKA.md", "img_eureka.jpg", page_eureka),
        "4": ("INFO_OFF-MACHINA.md", "img_off-machina.jpg", page_off_machina),
        "5": ("INFO_BOOKS.md", "img_books.jpg", page_books),
        "6": ("INFO_POLY.md", "img_poly.jpg", page_polys),
        "7": ("INFO_ABOUT.md", "img_about.jpg", page_abouts),
    }

    if chosen_id in pages:
        info, img, func = pages[chosen_id]
        st.sidebar.info(load_md_file(info))
        st.sidebar.image(img)
        func()

    show_icons()

if __name__ == "__main__":
    main()
