import streamlit as st
import extra_streamlit_components as stx
import random
import time
import os

# ==========================================
# 1. MOTOR DE LÓGICA E CARREGAMENTO (SUPORTE)
# ==========================================

def pick_lang():
    if 'lang' not in st.session_state:
        st.session_state.lang = "pt"
    
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
        st.session_state.auto = st.checkbox("🔄 Auto", value=st.session_state.get('auto', False))

def show_icons():
    st.sidebar.markdown("---")
    st.sidebar.caption("Máquina de Fazer Poesia © 2026")

def normalize_text(text):
    if not text: return ""
    return text.replace('\r\n', '\n').strip()

def get_processed_content(tema, seed=""):
    """
    IMPORTANTE: Esta função depende das suas funções 'load_poema', 'load_lypo', 
    'translate' e 'update_readings'. Elas devem estar no seu arquivo ou importadas.
    """
    try:
        curr = load_poema(tema, seed)
        curr += load_lypo()
        if st.session_state.lang != "pt":
            curr = translate(curr)
        update_readings(tema)
        return normalize_text(curr)
    except NameError as e:
        return f"Erro de Dependência: {e}. Certifique-se de que as funções de carregamento estão acessíveis."

def render_display(texto, tema):
    """
    IMPORTANTE: Depende de 'load_arts', 'write_ypoema' e 'talk'.
    """
    try:
        image = load_arts(tema) if st.session_state.draw else None
        write_ypoema(texto, image)
        if st.session_state.talk:
            talk(texto)
    except NameError as e:
        st.error(f"Erro ao renderizar: {e}")
        st.write(texto)

# ==========================================
# 2. DEFINIÇÃO DAS PÁGINAS (FLUXO COMPLETO)
# ==========================================

def page_mini():
    temas_list = load_temas("todos os temas")
    maxy = len(temas_list)
    wait_time = st.sidebar.slider("Segundos:", 5, 60, 10)
    
    placeholder = st.empty()
    
    # Lógica de Sorteio (Aleatório)
    if st.session_state.auto:
        st.session_state.mini = random.randrange(0, maxy)
        tema = temas_list[st.session_state.mini]
        texto = get_processed_content(tema)
        with placeholder.container():
            render_display(texto, tema)
        time.sleep(wait_time)
        st.rerun()
    else:
        # Se não houver índice na sessão, inicializa
        if 'mini' not in st.session_state:
            st.session_state.mini = 0
            
        if st.button("✻ Aleatório"):
            st.session_state.mini = random.randrange(0, maxy)
            # Sem rerun aqui para deixar o Streamlit processar a mudança naturalmente abaixo

        tema = temas_list[st.session_state.mini % maxy]
        render_display(get_processed_content(tema), tema)

def page_ypoemas():
    if 'book' not in st.session_state:
        st.session_state.book = "todos os temas"
    if 'take' not in st.session_state:
        st.session_state.take = 0
        
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    if col1.button("◀"):
        st.session_state.take -= 1
    if col2.button("✻ Aleatório"):
        st.session_state.take = random.randrange(0, maxy)
    if col3.button("▶"):
        st.session_state.take += 1
        
    # Garante que o índice esteja sempre dentro da lista
    st.session_state.take %= maxy
    
    tema = temas_list[st.session_state.take]
    render_display(get_processed_content(tema), tema)

def page_eureka():
    find_what = st.text_input("Buscar termo (min. 3 letras):")
    if len(find_what) >= 3:
        # Aqui deve-se chamar sua função 'load_eureka' original
        st.info(f"Buscando por: {find_what}")

def page_books():
    books = ["livro vivo", "poemas", "jocosos", "todos os temas"]
    opt = st.selectbox("Selecione o Livro:", books)
    if st.button("Carregar Biblioteca"):
        st.session_state.book = opt
        st.session_state.take = 0
        st.success(f"Livro '{opt}' ativo.")

# ==========================================
# 3. EXECUÇÃO PRINCIPAL (MAIN)
# ==========================================

def main():
    try:
        st.set_page_config(layout="wide", page_title="Máquina de Poesia")
    except:
        pass

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
            if os.path.exists(img_file):
                st.image(img_file)
        page_func()

    show_icons()

if __name__ == "__main__":
    main()
