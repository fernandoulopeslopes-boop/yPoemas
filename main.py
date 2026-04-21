import os
import sys

# --- PROTOCOLO DE ANCORAGEM (CPC) ---
# Força o diretório de execução para onde o main.py está
# Isso resolve o ModuleNotFoundError no Python 3.14/Streamlit Cloud
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
if dname not in sys.path:
    sys.path.insert(0, dname)

import streamlit as st

# --- IMPORTAÇÃO DAS DEPENDÊNCIAS ---
try:
    import extra_streamlit_components as stx
    import random
except ImportError as e:
    st.error(f"Dependências ausentes no requirements.txt: {e}")
    st.stop()

# --- IMPORTAÇÃO INTEGRAL DA MACHINA ---
try:
    from funcs import (
        load_md_file, load_temas, load_poema, load_lypo, 
        load_arts, load_info, translate, talk, write_ypoema,
        update_readings, load_all_offs, load_off_book, 
        load_book_pages, list_readings, get_binary_file_downloader_html,
        load_typo, pick_lang, draw_check_buttons, show_icons
    )
except ModuleNotFoundError:
    st.error(f"Caminho Atual: {os.getcwd()}")
    st.error(f"Arquivos no Diretório: {os.listdir('.')}")
    st.error("Erro Crítico: O arquivo 'funcs.py' não foi detectado no diretório /ypoemas/")
    st.stop()

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(
    page_title="yPoemas - a Machina de fazer Poesia", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

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

# --- ESTADOS DE SESSÃO ---
if "lang" not in st.session_state: st.session_state.lang = "pt"
if "last_lang" not in st.session_state: st.session_state.last_lang = "pt"
if "eureka" not in st.session_state: st.session_state.eureka = 0
if "off_take" not in st.session_state: st.session_state.off_take = 0
if "off_book" not in st.session_state: st.session_state.off_book = 0
if "tema" not in st.session_state: st.session_state.tema = "amor"
if "poly_file" not in st.session_state: st.session_state.poly_file = "languages.txt"
if "draw" not in st.session_state: st.session_state.draw = True
if "talk" not in st.session_state: st.session_state.talk = False

# --- PÁGINAS ---

def page_eureka():
    seed_list = st.session_state.get("seed_list", [])
    if not seed_list:
        st.warning(translate('nenhuma ocorrência encontrada...'))
        return

    opt_ocur = st.selectbox(
        "↓ Resultados",
        range(len(seed_list)),
        index=st.session_state.eureka if st.session_state.eureka < len(seed_list) else 0,
        format_func=lambda y: seed_list[y],
        key="opt_ocur"
    )
    st.session_state.eureka = opt_ocur
    this_seed = seed_list[opt_ocur]
    st.session_state.tema = this_seed.partition(" ➪ ")[2][0:-5]

    curr_ypoema = load_poema(st.session_state.tema, this_seed) if st.session_state.lang == "pt" else translate(load_poema(st.session_state.tema, this_seed))

    with st.expander("", expanded=True):
        write_ypoema(curr_ypoema, load_arts(st.session_state.tema) if st.session_state.draw else None)

def page_off_machina():
    off_books = load_all_offs()
    book_idx = st.selectbox("↓ Livros", range(len(off_books)), index=st.session_state.off_book)
    
    if book_idx != st.session_state.off_book:
        st.session_state.off_book = book_idx
        st.session_state.off_take = 0
        st.rerun()

    pages = load_book_pages(load_off_book(off_books[book_idx]))
    max_p = len(pages) - 1

    c1, c2, c3, c4 = st.columns(4)
    if c1.button("◀"): st.session_state.off_take = max_p if st.session_state.off_take <= 0 else st.session_state.off_take - 1
    if c2.button("✻"): st.session_state.off_take = random.randint(0, max_p)
    if c3.button("▶"): st.session_state.off_take = 0 if st.session_state.off_take >= max_p else st.session_state.off_take + 1
    if c4.button("❤"): list_readings()

    with st.expander(f"Página {st.session_state.off_take + 1}", expanded=True):
        write_ypoema(pages[st.session_state.off_take], load_arts(off_books[book_idx]) if st.session_state.draw else None)

# --- NAVEGAÇÃO ---

def main():
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="off-machina", description=""),
        stx.TabBarItemData(id="5", title="books", description=""),
        stx.TabBarItemData(id="6", title="poly", description=""),
        stx.TabBarItemData(id="7", title="about", description=""),
    ], default="2")

    with st.sidebar:
        pick_lang()
        draw_check_buttons()
        st.divider()
        menu = {"1":"MINI", "2":"YPOEMAS", "3":"EUREKA", "4":"OFF-MACHINA", "5":"BOOKS", "6":"POLY", "7":"ABOUT"}
        tag = menu.get(chosen_id, "YPOEMAS")
        st.info(load_md_file(f"INFO_{tag}.md"))

    if chosen_id == "3": page_eureka()
    elif chosen_id == "4": page_off_machina()
    
    show_icons()

if __name__ == "__main__":
    main()
