import sys
import os
import streamlit as st

# --- PRIORIDADE 0: VINCULAÇÃO DE DIRETÓRIO ---
# Força o reconhecimento do diretório local antes de qualquer importação de terceiros
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# --- IMPORTAÇÃO DOS MÓDULOS EXTERNOS ---
try:
    import extra_streamlit_components as stx
    import random
except ImportError as e:
    st.error(f"Erro ao carregar dependências (requirements.txt): {e}")
    st.stop()

# --- IMPORTAÇÃO INTEGRAL DAS FUNÇÕES DA MACHINA ---
try:
    from funcs import (
        load_md_file, load_temas, load_poema, load_lypo, 
        load_arts, load_info, translate, talk, write_ypoema,
        update_readings, load_all_offs, load_off_book, 
        load_book_pages, list_readings, get_binary_file_downloader_html,
        load_typo, pick_lang, draw_check_buttons, show_icons
    )
except ModuleNotFoundError:
    st.error("Erro Crítico: O arquivo 'funcs.py' não foi detectado no diretório /ypoemas/")
    st.stop()
except ImportError as e:
    st.error(f"Erro de importação em funcs.py: {e}")
    st.stop()

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(
    page_title="yPoemas - a Machina de fazer Poesia", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Estilização da Sidebar (300px) e botões
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
def init_states():
    if "lang" not in st.session_state: st.session_state.lang = "pt"
    if "last_lang" not in st.session_state: st.session_state.last_lang = "pt"
    if "eureka" not in st.session_state: st.session_state.eureka = 0
    if "off_take" not in st.session_state: st.session_state.off_take = 0
    if "off_book" not in st.session_state: st.session_state.off_book = 0
    if "book" not in st.session_state: st.session_state.book = "poemas"
    if "tema" not in st.session_state: st.session_state.tema = "amor"
    if "poly_take" not in st.session_state: st.session_state.poly_take = 0
    if "poly_file" not in st.session_state: st.session_state.poly_file = "languages.txt"
    if "vydo" not in st.session_state: st.session_state.vydo = False
    if "draw" not in st.session_state: st.session_state.draw = True
    if "talk" not in st.session_state: st.session_state.talk = False

init_states()

# --- PÁGINAS ---

def page_eureka():
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

    opt_ocur = st.selectbox(
        "↓ " + str(len(seed_list)) + " " + info_find,
        range(len(seed_list)),
        index=st.session_state.eureka if st.session_state.eureka < len(seed_list) else 0,
        format_func=lambda y: seed_list[y],
        key="opt_ocur",
    )

    st.session_state.eureka = opt_ocur
    this_seed = seed_list[opt_ocur]
    seed_tema = this_seed.partition(" ➪ ")[2][0:-5]
    st.session_state.tema = seed_tema

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
        img = load_arts(seed_tema) if st.session_state.draw else None
        write_ypoema(curr_ypoema, img)
        update_readings(seed_tema)

    if st.session_state.talk:
        talk(curr_ypoema)

def page_off_machina():
    off_books = load_all_offs()
    book_idx = st.selectbox("↓ " + translate("lista de Livros"), range(len(off_books)), 
                            index=st.session_state.off_book, format_func=lambda x: off_books[x])
    
    if book_idx != st.session_state.off_book:
        st.session_state.off_book = book_idx
        st.session_state.off_take = 0
        st.rerun()

    book_name = off_books[book_idx]
    pages = load_book_pages(load_off_book(book_name))
    max_p = len(pages) - 1

    col1, col2, col3, col4 = st.columns(4)
    if col1.button("◀"): st.session_state.off_take = max_p if st.session_state.off_take <= 0 else st.session_state.off_take - 1
    if col2.button("✻"): st.session_state.off_take = random.randrange(0, max_p + 1)
    if col3.button("▶"): st.session_state.off_take = 0 if st.session_state.off_take >= max_p else st.session_state.off_take + 1
    if col4.button("❤"): list_readings()

    content = pages[st.session_state.off_take]
    if st.session_state.lang != "pt": content = translate(content)

    with st.expander(f"⚫ {st.session_state.lang.upper()} ({st.session_state.off_take + 1}/{max_p + 1})", expanded=True):
        img = load_arts(book_name) if st.session_state.draw else None
        write_ypoema(content, img)

def page_polys():
    try:
        with open(f"./base/{st.session_state.poly_file}", encoding="utf-8") as f:
            lines = [l.strip() for l in f if " : " in l]
        opt_poly = st.selectbox(f"↓ {len(lines)} idiomas", range(len(lines)), 
                                index=st.session_state.poly_take, format_func=lambda x: lines[x])
        if st.button("✔"):
            st.session_state.last_lang = st.session_state.lang
            st.session_state.lang = lines[opt_poly].split(" : ")[1]
            st.session_state.poly_take = opt_poly
            st.rerun()
    except Exception as e:
        st.error(f"Erro na base de idiomas: {e}")

# --- MAIN ---

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
        try:
            st.image(f"./images/img_{tag.lower()}.jpg")
        except:
            pass
        st.info(load_md_file(f"INFO_{tag}.md"))

    if chosen_id == "3": page_eureka()
    elif chosen_id == "4": page_off_machina()
    elif chosen_id == "6": page_polys()
    # Outras abas mantêm o estado conforme o ypo_seguro
    
    show_icons()

if __name__ == "__main__":
    main()
