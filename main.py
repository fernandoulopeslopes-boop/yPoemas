import streamlit as st
import extra_streamlit_components as stx
import random
import os
import time

# --- CONFIGURAÇÃO DE INTERFACE ---
st.set_page_config(page_title="yPoemas - A Máquina", layout="wide", initial_sidebar_state="expanded")

# CSS para Sidebar fixa (300px) e estética do projeto
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 300px;
        max-width: 300px;
    }
    .stSelectbox label { font-weight: bold; color: #555; }
    .stButton>button { width: 100%; border-radius: 2px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- INICIALIZAÇÃO DO SESSION STATE (Lógica Seguro) ---
def init_states():
    defaults = {
        "lang": "pt", "last_lang": "pt", "eureka": 0, "off_take": 0, 
        "off_book": 0, "book": "poemas", "tema": "amor", 
        "poly_take": 0, "draw": True, "talk": False, "vydo": False
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_states()

# --- FUNÇÕES DE SUPORTE (Mockups/Importações) ---
# Aqui entram suas funções de carregamento (load_poema, translate, etc.)
# Importe-as do seu arquivo de funções principal.
from funcs import (
    load_md_file, load_temas, load_poema, load_lypo, 
    load_arts, load_info, translate, talk, write_ypoema,
    update_readings, load_all_offs, load_off_book, 
    load_book_pages, list_readings, get_binary_file_downloader_html,
    load_typo, pick_lang, draw_check_buttons, show_icons, load_arts
)

# --- PÁGINAS DO SISTEMA ---

def page_eureka():
    # Recupera dados de busca globais
    find_what = st.session_state.get("find_word", "...")
    seed_list = st.session_state.get("seed_list", [])
    soma_tema = st.session_state.get("soma_tema", [])
    
    if not seed_list:
        st.warning(translate('nenhuma ocorrência encontrada...'))
        return

    # Seletor de Ocorrências
    info_find = translate('ocorrência de "') if len(seed_list) == 1 else translate('ocorrências de "')
    label = f"↓ {len(seed_list)} {info_find} {find_what}"
    
    opt_ocur = st.selectbox(
        label, range(len(seed_list)),
        index=st.session_state.eureka if st.session_state.eureka < len(seed_list) else 0,
        format_func=lambda y: seed_list[y],
        key="eureka_selector"
    )
    st.session_state.eureka = opt_ocur

    # Processamento do Poema Selecionado
    this_seed = seed_list[opt_ocur]
    nome_tema = this_seed.partition(" ➪ ")[2]
    seed_tema = nome_tema[0:-5]
    st.session_state.tema = seed_tema

    # Lógica de Tradução Segura
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

    # Display
    with st.expander("EUREKA RESULT", expanded=True):
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

    # Navegação Horizontal
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("◀"): st.session_state.off_take = max_p if st.session_state.off_take <= 0 else st.session_state.off_take - 1
    if c2.button("✻"): st.session_state.off_take = random.randint(0, max_p)
    if c3.button("▶"): st.session_state.off_take = 0 if st.session_state.off_take >= max_p else st.session_state.off_take + 1
    if c4.button("❤"): list_readings()

    # Renderização
    content = pages[st.session_state.off_take]
    if st.session_state.lang != "pt":
        content = translate(content)

    with st.expander(f"{book_name.upper()} ({st.session_state.off_take + 1}/{max_p + 1})", expanded=True):
        img = load_arts(book_name) if st.session_state.draw else None
        write_ypoema(content, img)

def page_polys():
    # Lógica de seleção de idioma integrada
    try:
        with open(f"./base/{st.session_state.poly_file}", encoding="utf-8") as f:
            lines = [l.strip() for l in f if " : " in l]
        
        idx = st.selectbox(f"↓ Idiomas Disponíveis", range(len(lines)), 
                           index=st.session_state.poly_take, format_func=lambda x: lines[x])
        
        if st.button("✔ ALTERAR IDIOMA"):
            selected_lang = lines[idx].split(" : ")[1]
            st.session_state.last_lang = st.session_state.lang
            st.session_state.lang = selected_lang
            st.session_state.poly_take = idx
            st.rerun()
    except:
        st.error("Erro ao carregar base de idiomas.")

# --- ENGINE PRINCIPAL ---

def main():
    # Tab Bar de Navegação
    tabs = [
        {"id": "1", "title": "mini"}, {"id": "2", "title": "yPoemas"},
        {"id": "3", "title": "eureka"}, {"id": "4", "title": "off-machina"},
        {"id": "5", "title": "books"}, {"id": "6", "title": "poly"},
        {"id": "7", "title": "about"}
    ]
    
    chosen_tab = stx.tab_bar(data=[stx.TabBarItemData(id=t["id"], title=t["title"], description="") for t in tabs], default="2")

    # Sidebar Dinâmica
    with st.sidebar:
        pick_lang()
        draw_check_buttons()
        st.divider()
        
        # Mapa de Imagens e Infos
        map_info = {
            "1": "MINI", "2": "YPOEMAS", "3": "EUREKA", 
            "4": "OFF-MACHINA", "5": "BOOKS", "6": "POLY", "7": "ABOUT"
        }
        tag = map_info.get(chosen_tab, "YPOEMAS")
        
        try:
            st.image(f"./images/img_{tag.lower()}.jpg")
        except:
            st.info(f"Modo: {tag}")
            
        st.info(load_md_file(f"INFO_{tag}.md"))

    # Roteamento
    if chosen_tab == "1": st.write("Página Mini em desenvolvimento...")
    elif chosen_tab == "2": st.write("Página yPoemas Principal...")
    elif chosen_tab == "3": page_eureka()
    elif chosen_tab == "4": page_off_machina()
    elif chosen_tab == "5": st.write("Página Books...")
    elif chosen_tab == "6": page_polys()
    elif chosen_tab == "7": st.write("Sobre a Machina...")

    show_icons()

if __name__ == "__main__":
    main()
