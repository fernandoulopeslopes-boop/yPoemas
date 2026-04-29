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
        "poly_lang": "pt",
        "take": 0
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

# --- FUNÇÃO DE VOZ (EDGE-TTS) MASCULINA ---
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

# --- AUXILIARES DE CARREGAMENTO ---
@st.cache_data
def load_temas_seguro(book):
    file_path = os.path.join("./base", f"rol_{book}.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

# --- PÁGINAS REAIS ---

def page_ypoemas():
    temas = load_temas_seguro(st.session_state.book)
    if not temas:
        st.error(f"Índice rol_{st.session_state.book}.txt não encontrado.")
        return

    col_nav, col_info = st.columns([8, 2])
    with col_nav:
        f1, b_last, b_rand, b_next, f2 = st.columns([1, 1, 1, 1, 1])
        if b_last.button("◀"):
            st.session_state.take = len(temas)-1 if st.session_state.take <= 0 else st.session_state.take - 1
        if b_rand.button("✻"):
            st.session_state.take = random.randrange(len(temas))
        if b_next.button("▶"):
            st.session_state.take = 0 if st.session_state.take >= len(temas)-1 else st.session_state.take + 1

    tema_atual = temas[st.session_state.take]
    st.session_state.tema = tema_atual

    # Simulação da chamada de geração (ajuste conforme seu lay_2_ypo)
    try:
        from lay_2_ypo import gera_poema
        poema = gera_poema(tema_atual, st.session_state.lang)
    except:
        poema = f"Gerando versos sobre {tema_atual}..."

    with st.expander(f"⚫ {tema_atual.upper()}", expanded=True):
        st.markdown(f"<div style='text-align: center;'>{poema}</div>", unsafe_allow_html=True)
        if st.session_state.draw:
            img_path = f"./images/matrix/{tema_atual}.jpg"
            if os.path.exists(img_path): st.image(img_path)

    if st.session_state.talk:
        talk(poema)

def page_eureka():
    find_what = st.text_input(translate("digite algo para buscar..."))
    if len(find_what) >= 3:
        # Aqui você usaria sua função load_eureka real
        st.info(f"Buscando '{find_what}' nos arquivos rol_*.txt...")
        # Lógica de seleção de ocorrência...

def page_books():
    books_list = ["todos_os_livros", "livro_vivo", "poemas", "jocosos", "ensaios", "metalinguagem", "sociais", "outros autores", "signos_fem", "signos_mas"]
    
    idx = books_list.index(st.session_state.book) if st.session_state.book in books_list else 0
    opt_book = st.selectbox("↓ lista de Livros", range(len(books_list)), index=idx, format_func=lambda x: books_list[x])
    
    if st.button("✔ Confirmar Livro"):
        st.session_state.book = books_list[opt_book]
        st.session_state.take = 0
        st.rerun()

    temas = load_temas_seguro(st.session_state.book)
    st.write(f"**Temas neste livro:** {', '.join(temas[:10])}...")

# [Demais funções page_mini, page_polys, page_abouts seguem o mesmo padrão de integração]

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

    # Sidebar cockpit
    with st.sidebar:
        st.session_state.draw = st.checkbox("Exibir Artes", value=st.session_state.draw)
        st.session_state.talk = st.checkbox("Voz da Machina", value=st.session_state.talk)

    page_data = PAGES.get(str(chosen_id))
    if page_data:
        page_data["func"]()

if __name__ == "__main__":
    main()
