import streamlit as st
import extra_streamlit_components as stx
import os
import random
import asyncio
import edge_tts

# --- CONFIGURAÇÃO E ESTADO INICIAL ---
def init_session():
    defaults = {
        "lang": "pt",
        "last_lang": "pt",
        "eureka": 0,
        "tema": "geral",
        "off_book": 0,
        "off_take": 0,
        "book": "livro_vivo",
        "poly_take": 0,
        "poly_file": "poly.txt",
        "draw": True,
        "talk": False,
        "poly_name": "Português",
        "poly_lang": "pt"
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

# --- FUNÇÃO DE VOZ (EDGE-TTS) ---
def talk(text):
    async def speak():
        voices = {
            "pt": "pt-BR-AntonioNeural",
            "en": "en-US-GuyNeural",
            "es": "es-ES-AlvaroNeural",
            "fr": "fr-FR-HenriNeural",
            "it": "it-IT-DiegoNeural"
        }
        selected_voice = voices.get(st.session_state.lang, "pt-BR-AntonioNeural")
        clean_text = text.replace("<br>", " ").replace("➪", "seta").replace("|", " ")
        
        communicate = edge_tts.Communicate(clean_text, selected_voice)
        output_path = "./temp/output.mp3"
        if not os.path.exists("./temp"): os.makedirs("./temp")
            
        await communicate.save(output_path)
        st.audio(output_path)

    if text: asyncio.run(speak())

# --- CORREÇÃO DIRETA DO CARREGAMENTO DE TEMAS ---
@st.cache_data
def load_temas_corrigido(book):
    """Lê os temas usando o padrão rol_nome.txt"""
    # Se o nome vier com espaços ou sublinhados, o padrão do arquivo é o que vale
    file_path = os.path.join("./base", f"rol_{book}.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

# --- PÁGINAS ---

def page_books():
    books_list = [
        "livro_vivo", "poemas", "jocosos", "ensaios", 
        "metalinguagem", "sociais", "outros autores", 
        "signos_fem", "signos_mas", "temas_demo"
    ]
    
    books_col, ok_col = st.columns([9.3, 0.7])
    with books_col:
        try:
            idx = books_list.index(st.session_state.book)
        except:
            idx = 0
        opt_book = st.selectbox("↓ " + translate("lista de Livros"), range(len(books_list)), index=idx, format_func=lambda x: books_list[x])
    
    with ok_col:
        if st.button("✔", key="btn_book_ok"):
            st.session_state.book = books_list[opt_book]
            st.session_state.take = 0
            st.rerun()

    temas = load_temas_corrigido(st.session_state.book)
    if temas:
        st.write(", ".join(temas) + f" ▶ {len(temas)} temas")
    else:
        st.error(f"Arquivo rol_{st.session_state.book}.txt não encontrado em ./base")

def page_eureka():
    # ... (mesma lógica anterior, mas garantindo o uso do load_temas_corrigido se necessário)
    pass

# --- MAIN ---

PAGES = {
    "1": {"func": page_mini, "img": "img_mini.jpg", "info": "INFO_MINI.md"},
    "2": {"func": page_ypoemas, "img": "img_ypoemas.jpg", "info": "INFO_YPOEMAS.md"},
    "3": {"func": page_eureka, "img": "img_eureka.jpg", "info": "INFO_EUREKA.md"},
    "4": {"func": page_off_machina, "img": "img_off-machina.jpg", "info": "INFO_OFF-MACHINA.md"},
    "5": {"func": page_books, "img": "img_books.jpg", "info": "INFO_BOOKS.md"},
    "6": {"func": page_polys, "img": "img_poly.jpg", "info": "INFO_POLY.md"},
    "7": {"func": page_abouts, "img": "img_about.jpg", "info": "INFO_ABOUT.md"},
}

def main():
    init_session()
    chosen_id = stx.tab_bar(
        data=[
            stx.TabBarItemData(id=1, title="mini", description=""),
            stx.TabBarItemData(id=2, title="yPoemas", description=""),
            stx.TabBarItemData(id=3, title="eureka", description=""),
            stx.TabBarItemData(id=4, title="off-machina", description=""),
            stx.TabBarItemData(id=5, title="books", description=""),
            stx.TabBarItemData(id=6, title="poly", description=""),
            stx.TabBarItemData(id=7, title="about", description=""),
        ], default=2,
    )

    pick_lang()
    draw_check_buttons()

    page_data = PAGES.get(str(chosen_id))
    if page_data:
        st.sidebar.info(load_md_file(page_data["info"]))
        with st.sidebar: st.image(page_data["img"])
        # Sobrescrita local para evitar que o erro no ypo_seguro.py bloqueie a execução
        page_data["func"]()

    show_icons()

if __name__ == "__main__":
    main()
