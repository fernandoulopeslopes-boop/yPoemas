import streamlit as st
import extra_streamlit_components as stx
import random
import os
import sys

# --- PROTOCOLO DE ACESSO: AJUSTE DE PATH ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# --- IMPORTAÇÃO DAS FUNÇÕES CORE ---
try:
    from funcs import (
        load_md_file, load_temas, load_poema, load_lypo, 
        load_arts, load_info, translate, talk, write_ypoema,
        update_readings, load_all_offs, load_off_book, 
        load_book_pages, list_readings, get_binary_file_downloader_html,
        load_typo, pick_lang, draw_check_buttons, show_icons, load_arts
    )
except ImportError as e:
    st.error(f"Erro de Módulo: {e}")
    st.stop()

# --- CONFIGURAÇÃO DA INTERFACE (IDENTIDADE PRESERVADA) ---
st.set_page_config(
    page_title="yPoemas - a Machina de fazer Poesia", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Customização de Interface
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 300px;
        max-width: 300px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- INICIALIZAÇÃO DO SESSION STATE ---
def init_session_state():
    defaults = {
        "lang": "pt", "last_lang": "pt", "eureka": 0, "off_take": 0, 
        "off_book": 0, "book": "poemas", "tema": "amor", 
        "poly_take": 0, "poly_file": "languages.txt",
        "vydo": False, "draw": True, "talk": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# --- DEFINIÇÃO DAS PÁGINAS ---

def page_eureka():
    # Recuperação de dados de busca
    find_what = st.session_state.get("find_word", "")
    seed_list = st.session_state.get("seed_list", [])
    soma_tema = st.session_state.get("soma_tema", [])
    
    if not seed_list:
        st.warning(translate('nenhuma ocorrência encontrada...'))
        return

    seed_list.sort()
    info_find = translate('ocorrência de "') if len(seed_list) == 1 else translate('ocorrências de "')
    info_find += find_what
    
    if len(soma_tema) > 1:
        info_find += translate('" em ' + str(len(soma_tema)) + " temas")

    options = list(range(len(seed_list)))
    opt_ocur = st.selectbox(
        "↓ " + str(len(seed_list)) + " " + info_find,
        options,
        index=st.session_state.eureka if st.session_state.eureka < len(seed_list) else 0,
        format_func=lambda y: seed_list[y],
        key="opt_ocur",
    )

    st.session_state.eureka = opt_ocur
    this_seed = seed_list[opt_ocur]
    part_line = this_seed.partition(" ➪ ")
    seed_tema = part_line[2][0:-5]
    st.session_state.tema = seed_tema

    # Lógica de Tradução e Carga
    if st.session_state.lang != st.session_state.last_lang:
        curr_ypoema = load_lypo()
    else:
        curr_ypoema = load_poema(seed_tema, this_seed)
        curr_ypoema = load_lypo()

    if st.session_state.lang != "pt":
        curr_ypoema = translate(curr_ypoema)
        with open("./temp/TYPO_TEMP.txt", "w", encoding="utf-8") as f:
            f.write(curr_ypoema)
        curr_ypoema = load_typo()

    with st.expander("", expanded=True):
        img_art = load_arts(seed_tema) if st.session_state.draw else None
        write_ypoema(curr_ypoema, img_art)
        update_readings(seed_tema)

    if st.session_state.talk:
        talk(curr_ypoema)

def page_off_machina():
    off_books_list = load_all_offs()
    opt_off_book = st.selectbox(
        "↓ " + translate("lista de Livros"),
        range(len(off_books_list)),
        index=st.session_state.off_book,
        format_func=lambda x: off_books_list[x],
        key="opt_off_book",
    )

    if opt_off_book != st.session_state.off_book:
        st.session_state.off_book = opt_off_book
        st.session_state.off_take = 0
        st.rerun()

    off_book_name = off_books_list[st.session_state.off_book]
    this_off_book = load_off_book(off_book_name)
    off_book_pagys = load_book_pages(this_off_book)
    maxy = len(off_book_pagys) - 1

    # Navegação Padrão
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("◀"): st.session_state.off_take = maxy if st.session_state.off_take <= 0 else st.session_state.off_take - 1
    if col2.button("✻"): st.session_state.off_take = random.randrange(0, maxy + 1)
    if col3.button("▶"): st.session_state.off_take = 0 if st.session_state.off_take >= maxy else st.session_state.off_take + 1
    if col4.button("❤"): list_readings()

    content = this_off_book[st.session_state.off_take]
    if st.session_state.lang != "pt":
        content = translate(content)

    with st.expander(f"⚫ {st.session_state.lang.upper()} ({st.session_state.off_take + 1}/{maxy + 1})", expanded=True):
        img_art = load_arts(off_book_name) if st.session_state.draw else None
        write_ypoema(content, img_art)
        update_readings(off_book_name)

def page_polys():
    try:
        with open(os.path.join("./base/", st.session_state.poly_file), encoding="utf-8") as f:
            poly_list = [line.strip() for line in f if " : " in line]
        
        opt_poly = st.selectbox(f"↓ {len(poly_list)} idiomas", range(len(poly_list)), 
                                index=st.session_state.poly_take, format_func=lambda x: poly_list[x])
        
        if st.button("✔"):
            selected = poly_list[opt_poly].split(" : ")
            st.session_state.last_lang = st.session_state.lang
            st.session_state.lang = selected[1]
            st.session_state.poly_take = opt_poly
            st.rerun()
    except Exception as e:
        st.error(f"Erro no processamento de idiomas: {e}")

# --- EXECUÇÃO PRINCIPAL ---

def main():
    # Componente de Abas
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="poly", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    # Sidebar Técnica (300px)
    with st.sidebar:
        pick_lang()
        draw_check_buttons()
        st.divider()
        
        menu_map = {
            "1": "MINI", "2": "YPOEMAS", "3": "EUREKA", 
            "4": "OFF-MACHINA", "5": "BOOKS", "6": "POLY", "7": "ABOUT"
        }
        tag = menu_map.get(chosen_id, "YPOEMAS")
        
        try:
            st.image(f"./images/img_{tag.lower()}.jpg")
        except:
            st.info(f"Interface: {tag}")
            
        st.sidebar.info(load_md_file(f"INFO_{tag}.md"))

    # Roteamento de Páginas
    if chosen_id == "3":
        page_eureka()
    elif chosen_id == "4":
        page_off_machina()
    elif chosen_id == "6":
        page_polys()
    # Outras abas em implementação seguindo o mesmo padrão CPC
    
    show_icons()

if __name__ == "__main__":
    main()
