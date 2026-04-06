import streamlit as st
import extra_streamlit_components as stx
import random
import time
import os

# ==========================================
# 1. INFRAESTRUTURA (Obrigatório no topo)
# ==========================================

def load_md_file(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        return f"Aviso: `{file_path}` não encontrado."
    except: return "Erro de leitura."

def normalize_text(text):
    if not text: return ""
    return text.replace('\r\n', '\n').strip()

def get_processed_content(tema, seed=""):
    """Motor central: Carrega, Traduz e Normaliza."""
    curr = load_poema(tema, seed)
    curr += load_lypo()
    if st.session_state.lang != "pt":
        curr = translate(curr)
    update_readings(tema)
    return normalize_text(curr)

def render_display(texto, tema):
    """Renderiza imagem e texto."""
    image = load_arts(tema) if st.session_state.draw else None
    write_ypoema(texto, image)
    if st.session_state.talk:
        talk(texto)

# ==========================================
# 2. DEFINIÇÃO DAS PÁGINAS (Lógica Completa)
# ==========================================

def page_mini():
    temas_list = load_temas("todos os temas")
    maxy = len(temas_list)
    wait_time = st.sidebar.slider("Segundos:", 5, 60, 10)
    
    col_rand, col_auto = st.columns([1, 1])
    if col_rand.button("✻ Aleatório"):
        st.session_state.mini = random.randrange(0, maxy)
    
    st.session_state.auto = col_auto.checkbox("Auto", value=st.session_state.get('auto', False))
    
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
        st.session_state.mini = st.session_state.get('mini', 0) % maxy
        tema = temas_list[st.session_state.mini]
        render_display(get_processed_content(tema), tema)

def page_ypoemas():
    if 'book' not in st.session_state: st.session_state.book = "todos os temas"
    if 'take' not in st.session_state: st.session_state.take = 0
    
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    if col1.button("◀"): st.session_state.take -= 1
    if col2.button("✻"): st.session_state.take = random.randrange(0, maxy)
    if col3.button("▶"): st.session_state.take += 1
    
    st.session_state.take %= maxy
    tema = temas_list[st.session_state.take]
    render_display(get_processed_content(tema), tema)

def page_eureka():
    find_what = st.text_input("Buscar termo (min. 3 letras):")
    if len(find_what) >= 3:
        eureka_list = load_eureka(find_what) # Requer que load_eureka exista
        if eureka_list:
            # Exemplo de processamento da lista eureka
            seed_data = [{"display": f"{line.partition(' : ')[0]} ➪ {line.partition(' : ')[2]}", 
                          "tema": line.partition(' : ')[2][0:-5], 
                          "seed": line} for line in eureka_list]
            idx = st.selectbox("Ocorrências", range(len(seed_data)), format_func=lambda x: seed_data[x]["display"])
            item = seed_data[idx]
            render_display(get_processed_content(item["tema"], item["seed"]), item["tema"])

def page_books():
    books_list = ["livro vivo", "poemas", "jocosos", "todos os temas"]
    opt = st.selectbox("Selecione o Livro:", range(len(books_list)), format_func=lambda x: books_list[x])
    if st.button("Confirmar Seleção"):
        st.session_state.book = books_list[opt]
        st.session_state.take = 0
        st.success(f"Livro atual: {books_list[opt]}")

# ==========================================
# 3. INTERFACE E EXECUÇÃO (Main)
# ==========================================

def pick_lang():
    if 'lang' not in st.session_state: st.session_state.lang = "pt"
    langs = {"pt": "🇧🇷", "en": "🇺🇸", "es": "🇪🇸", "fr": "🇫🇷", "it": "🇮🇹"}
    cols = st.sidebar.columns(5)
    for i, (lang, flag) in enumerate(langs.items()):
        if cols[i].button(flag, key=f"lang_{lang}"):
            st.session_state.lang = lang
            st.rerun()

def draw_check_buttons():
    with st.sidebar:
        st.markdown("### ⚙️ Configurações")
        st.session_state.talk = st.checkbox("📢 Voz", value=st.session_state.get('talk', False))
        st.session_state.draw = st.checkbox("🖼️ Imagens", value=st.session_state.get('draw', True))

def show_icons():
    st.sidebar.markdown("---")
    st.sidebar.caption("Máquina de Fazer Poesia © 2026")

def main():
    try:
        st.set_page_config(layout="wide", page_title="Máquina de Poesia")
    except: pass

    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="1", title="mini", description=""),
        stx.TabBarItemData(id="2", title="yPoemas", description=""),
        stx.TabBarItemData(id="3", title="eureka", description=""),
        stx.TabBarItemData(id="4", title="books", description=""),
        stx.TabBarItemData(id="5", title="about", description=""),
    ], default="2")

    pick_lang()
    draw_check_buttons()

    pages = {
        "1": ("INFO_MINI.md", "img_mini.jpg", page_mini),
        "2": ("INFO_YPOEMAS.md", "img_ypoemas.jpg", page_ypoemas),
        "3": ("INFO_EUREKA.md", "img_eureka.jpg", page_eureka),
        "4": ("INFO_BOOKS.md", "img_books.jpg", page_books),
        "5": ("INFO_ABOUT.md", "img_about.jpg", lambda: st.markdown(load_md_file("INFO_ABOUT.md")))
    }

    if chosen_id in pages:
        info_file, img_file, page_func = pages[chosen_id]
        with st.sidebar:
            st.info(load_md_file(info_file))
            if os.path.exists(img_file): st.image(img_file)
        page_func()

    show_icons()

if __name__ == "__main__":
    main()
    
